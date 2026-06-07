import pytest

from catalog.models import Title
from catalog.services import CatalogService
from integrations.tmdb import NormalizedTMDbTitle, TMDbClientError


class SearchClient:
    def __init__(self, payload=None, error=None):
        self.payload = payload or {"results": []}
        self.error = error
        self.queries = []

    def search_multi(self, query):
        self.queries.append(query)
        if self.error:
            raise self.error
        return self.payload


class DetailClient:
    def __init__(self, movie_payload=None, tv_payload=None):
        self.movie_payload = movie_payload or {}
        self.tv_payload = tv_payload or {}

    def movie_details(self, tmdb_id):
        return {**self.movie_payload, "id": tmdb_id}

    def tv_details(self, tmdb_id):
        return {**self.tv_payload, "id": tmdb_id}


def test_search_returns_normalized_tmdb_results() -> None:
    client = SearchClient(
        {
            "results": [
                {
                    "id": 1,
                    "media_type": "movie",
                    "title": "Dune",
                    "release_date": "2021-10-22",
                }
            ]
        }
    )
    service = CatalogService(client=client)

    response = service.search("Dune")

    assert client.queries == ["Dune"]
    assert response.error_message == ""
    assert response.results == [
        NormalizedTMDbTitle(
            tmdb_id=1,
            media_type="movie",
            title="Dune",
            original_title="",
            year=2021,
            overview="",
            poster_path="",
        )
    ]


def test_search_does_not_call_tmdb_for_blank_query() -> None:
    client = SearchClient()
    service = CatalogService(client=client)

    response = service.search("   ")

    assert client.queries == []
    assert response.results == []
    assert response.error_message == ""


def test_search_reports_missing_tmdb_api_key_without_crashing() -> None:
    service = CatalogService(client=SearchClient(error=TMDbClientError("TMDB_API_KEY is not configured")))

    response = service.search("Dune")

    assert response.results == []
    assert "TMDb API key is not configured" in response.error_message


@pytest.mark.django_db
def test_get_or_sync_title_creates_movie_from_tmdb_details() -> None:
    service = CatalogService(
        client=DetailClient(
            movie_payload={
                "title": "Dune",
                "original_title": "Dune",
                "overview": "A desert planet epic.",
                "poster_path": "/dune.jpg",
                "backdrop_path": "/dune-backdrop.jpg",
                "release_date": "2021-10-22",
                "status": "Released",
                "runtime": 155,
            }
        )
    )

    title = service.get_or_sync_title(media_type="movie", tmdb_id=1)

    assert title.type == Title.Type.MOVIE
    assert title.tmdb_id == 1
    assert title.title == "Dune"
    assert title.release_date.isoformat() == "2021-10-22"
    assert title.runtime == 155


@pytest.mark.django_db
def test_get_or_sync_title_updates_existing_without_duplicates() -> None:
    existing = Title.objects.create(
        type=Title.Type.TV,
        tmdb_id=2,
        title="Old Silo",
        overview="Keep this when omitted.",
        poster_path="/existing.jpg",
    )
    service = CatalogService(
        client=DetailClient(
            tv_payload={
                "name": "Silo",
                "first_air_date": "2023-05-05",
                "status": "Returning Series",
            }
        )
    )

    title = service.get_or_sync_title(media_type="tv", tmdb_id=2)

    assert title.pk == existing.pk
    assert title.title == "Silo"
    assert title.overview == "Keep this when omitted."
    assert title.poster_path == "/existing.jpg"
    assert title.first_air_date.isoformat() == "2023-05-05"
    assert Title.objects.filter(type=Title.Type.TV, tmdb_id=2).count() == 1


@pytest.mark.django_db
def test_get_or_sync_title_handles_tv_details_without_episode_runtime() -> None:
    service = CatalogService(
        client=DetailClient(
            tv_payload={
                "name": "Silo",
                "episode_run_time": [],
            }
        )
    )

    title = service.get_or_sync_title(media_type="tv", tmdb_id=2)

    assert title.title == "Silo"
    assert title.runtime is None


@pytest.mark.django_db
def test_get_or_sync_title_reports_missing_key_without_creating_title() -> None:
    class MissingKeyClient:
        def movie_details(self, tmdb_id):
            raise TMDbClientError("TMDB_API_KEY is not configured")

    service = CatalogService(client=MissingKeyClient())

    with pytest.raises(TMDbClientError, match="TMDB_API_KEY is not configured"):
        service.get_or_sync_title(media_type="movie", tmdb_id=1)

    assert Title.objects.count() == 0
