import responses
from django.core.cache import cache

from integrations.tmdb import TMDbClient


@responses.activate
def test_tmdb_search_multi_uses_api() -> None:
    cache.clear()
    client = TMDbClient(api_key="fake-key", base_url="https://api.themoviedb.org/3")
    responses.add(
        responses.GET,
        "https://api.themoviedb.org/3/search/multi",
        json={"results": [{"id": 1, "title": "Dune"}]},
        status=200,
    )

    result = client.search_multi("Dune")

    assert result["results"][0]["title"] == "Dune"
    assert "api_key=fake-key" in responses.calls[0].request.url


@responses.activate
def test_tmdb_search_multi_uses_cache() -> None:
    cache.clear()
    client = TMDbClient(api_key="fake-key", base_url="https://api.themoviedb.org/3")
    responses.add(
        responses.GET,
        "https://api.themoviedb.org/3/search/multi",
        json={"results": [{"id": 1, "title": "Dune"}]},
        status=200,
    )

    first_result = client.search_multi("Dune")
    second_result = client.search_multi("Dune")

    assert first_result == second_result
    assert len(responses.calls) == 1
