from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from catalog.models import Title
from integrations.tmdb import NormalizedTMDbTitle, TMDbClient, TMDbClientError, normalize_search_results


@dataclass(frozen=True)
class CatalogSearchResponse:
    query: str
    results: list[NormalizedTMDbTitle]
    error_message: str = ""


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _runtime_from_payload(media_type: str, payload: dict[str, Any]) -> int | None:
    if media_type == Title.Type.MOVIE:
        return payload.get("runtime")

    episode_run_time = payload.get("episode_run_time") or []
    if not episode_run_time:
        return None
    return episode_run_time[0]


class CatalogService:
    def __init__(self, client: TMDbClient | None = None):
        self.client = client or TMDbClient()

    def search(self, query: str) -> CatalogSearchResponse:
        normalized_query = query.strip()
        if not normalized_query:
            return CatalogSearchResponse(query=normalized_query, results=[])

        try:
            payload = self.client.search_multi(normalized_query)
        except TMDbClientError as exc:
            return CatalogSearchResponse(query=normalized_query, results=[], error_message=self._friendly_error(exc))

        return CatalogSearchResponse(query=normalized_query, results=normalize_search_results(payload))

    def get_or_sync_title(self, media_type: str, tmdb_id: int) -> Title:
        if media_type not in {Title.Type.MOVIE, Title.Type.TV}:
            raise ValueError("media_type must be 'movie' or 'tv'")

        if media_type == Title.Type.MOVIE:
            payload = self.client.movie_details(tmdb_id)
        else:
            payload = self.client.tv_details(tmdb_id)

        return self.upsert_title_from_tmdb(media_type=media_type, payload=payload)

    def upsert_title_from_tmdb(self, media_type: str, payload: dict[str, Any]) -> Title:
        tmdb_id = payload["id"]
        defaults = self._title_defaults(media_type=media_type, payload=payload)
        title, created = Title.objects.get_or_create(
            type=media_type,
            tmdb_id=tmdb_id,
            defaults=defaults,
        )
        if created:
            return title

        update_fields: list[str] = []
        for field, value in defaults.items():
            if value in {"", None}:
                continue
            if getattr(title, field) != value:
                setattr(title, field, value)
                update_fields.append(field)

        if update_fields:
            title.save(update_fields=[*update_fields, "updated_at"])
        return title

    def _title_defaults(self, media_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        if media_type == Title.Type.MOVIE:
            title = payload.get("title") or payload.get("original_title") or "Untitled movie"
            original_title = payload.get("original_title") or ""
            release_date = _parse_date(payload.get("release_date"))
            first_air_date = None
        else:
            title = payload.get("name") or payload.get("original_name") or "Untitled TV show"
            original_title = payload.get("original_name") or ""
            release_date = None
            first_air_date = _parse_date(payload.get("first_air_date"))

        return {
            "title": title,
            "original_title": original_title,
            "overview": payload.get("overview") or "",
            "poster_path": payload.get("poster_path") or "",
            "backdrop_path": payload.get("backdrop_path") or "",
            "release_date": release_date,
            "first_air_date": first_air_date,
            "source_status": payload.get("status") or "",
            "runtime": _runtime_from_payload(media_type, payload),
        }

    def _friendly_error(self, exc: TMDbClientError) -> str:
        message = str(exc)
        if "TMDB_API_KEY" in message:
            return "TMDb API key is not configured. Add TMDB_API_KEY to the environment to enable catalog search."
        return message
