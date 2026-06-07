import responses

from integrations.tmdb import TMDbClient


@responses.activate
def test_tmdb_search_multi_uses_api() -> None:
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
