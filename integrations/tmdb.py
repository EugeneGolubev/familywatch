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
