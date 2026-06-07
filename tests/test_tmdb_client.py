import responses
from django.core.cache import cache

from integrations.tmdb import TMDbClient, normalize_search_results


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


def test_normalize_search_results_keeps_movies_and_tv_only() -> None:
    payload = {
        "results": [
            {
                "id": 1,
                "media_type": "movie",
                "title": "Dune",
                "original_title": "Dune",
                "release_date": "2021-10-22",
                "overview": "A desert planet epic.",
                "poster_path": "/dune.jpg",
            },
            {
                "id": 2,
                "media_type": "tv",
                "name": "Silo",
                "original_name": "Silo",
                "first_air_date": "2023-05-05",
                "overview": "Underground mystery.",
                "poster_path": "/silo.jpg",
            },
            {"id": 3, "media_type": "person", "name": "Performer"},
        ]
    }

    results = normalize_search_results(payload)

    assert [result.media_type for result in results] == ["movie", "tv"]
    assert results[0].tmdb_id == 1
    assert results[0].title == "Dune"
    assert results[0].year == 2021
    assert results[1].title == "Silo"
    assert results[1].year == 2023


def test_normalize_search_results_handles_missing_optional_metadata() -> None:
    payload = {"results": [{"id": 10, "media_type": "movie", "title": "Untimed"}]}

    result = normalize_search_results(payload)[0]

    assert result.title == "Untimed"
    assert result.year is None
    assert result.overview == ""
    assert result.poster_path == ""
