from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any

import requests
from django.conf import settings
from django.core.cache import cache


class TMDbClientError(RuntimeError):
    pass


@dataclass(frozen=True)
class NormalizedTMDbTitle:
    tmdb_id: int
    media_type: str
    title: str
    original_title: str
    year: int | None
    overview: str
    poster_path: str

    @property
    def media_label(self) -> str:
        if self.media_type == "tv":
            return "TV"
        return "Movie"

    @property
    def poster_url(self) -> str:
        if not self.poster_path:
            return ""
        return f"https://image.tmdb.org/t/p/w185{self.poster_path}"


def _year_from_date(value: str | None) -> int | None:
    if not value or len(value) < 4:
        return None
    try:
        return int(value[:4])
    except ValueError:
        return None


def normalize_search_results(payload: dict[str, Any]) -> list[NormalizedTMDbTitle]:
    results: list[NormalizedTMDbTitle] = []
    for item in payload.get("results", []):
        media_type = item.get("media_type")
        if media_type not in {"movie", "tv"}:
            continue

        date_value = item.get("release_date") if media_type == "movie" else item.get("first_air_date")
        title = item.get("title") if media_type == "movie" else item.get("name")
        original_title = item.get("original_title") if media_type == "movie" else item.get("original_name")

        results.append(
            NormalizedTMDbTitle(
                tmdb_id=item["id"],
                media_type=media_type,
                title=title or "",
                original_title=original_title or "",
                year=_year_from_date(date_value),
                overview=item.get("overview") or "",
                poster_path=item.get("poster_path") or "",
            )
        )
    return results


@dataclass(frozen=True)
class TMDbClient:
    api_key: str = settings.TMDB_API_KEY
    base_url: str = "https://api.themoviedb.org/3"
    timeout_seconds: int = 10
    cache_seconds: int = 60 * 30

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self.api_key:
            raise TMDbClientError("TMDB_API_KEY is not configured")

        params = {**(params or {}), "api_key": self.api_key}
        cache_payload = json.dumps({"path": path, "params": params}, sort_keys=True)
        cache_key = f"tmdb:{hashlib.sha256(cache_payload.encode()).hexdigest()}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        response = requests.get(f"{self.base_url}{path}", params=params, timeout=self.timeout_seconds)
        if response.status_code == 429:
            raise TMDbClientError("TMDb rate limit exceeded")
        if response.status_code >= 400:
            raise TMDbClientError(f"TMDb request failed: {response.status_code}")

        data = response.json()
        cache.set(cache_key, data, self.cache_seconds)
        return data

    def search_multi(self, query: str, language: str = "en-US", page: int = 1) -> dict[str, Any]:
        return self._get("/search/multi", {"query": query, "language": language, "page": page})

    def movie_details(self, tmdb_id: int, language: str = "en-US") -> dict[str, Any]:
        return self._get(f"/movie/{tmdb_id}", {"language": language})

    def tv_details(self, tmdb_id: int, language: str = "en-US") -> dict[str, Any]:
        return self._get(f"/tv/{tmdb_id}", {"language": language})

    def watch_providers(self, media_type: str, tmdb_id: int) -> dict[str, Any]:
        if media_type not in {"movie", "tv"}:
            raise ValueError("media_type must be 'movie' or 'tv'")
        return self._get(f"/{media_type}/{tmdb_id}/watch/providers")
