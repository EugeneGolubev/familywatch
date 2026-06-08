import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from catalog.models import Title
from integrations.tmdb import NormalizedTMDbTitle, TMDbClientError


class FakeSearchService:
    def search(self, query):
        return type(
            "SearchResponse",
            (),
            {
                "query": query,
                "results": [
                    NormalizedTMDbTitle(
                        tmdb_id=1,
                        media_type="movie",
                        title="Dune",
                        original_title="Dune",
                        year=2021,
                        overview="A desert planet epic.",
                        poster_path="/dune.jpg",
                    )
                ]
                if query
                else [],
                "error_message": "",
            },
        )()


class MissingKeyService:
    def search(self, query):
        return type(
            "SearchResponse",
            (),
            {"query": query, "results": [], "error_message": "TMDb API key is not configured."},
        )()


@pytest.mark.django_db
def test_search_page_requires_authentication(client) -> None:
    response = client.get(reverse("catalog_search"))

    assert response.status_code == 302
    assert response.url.startswith(f"{reverse('login')}?next=")


@pytest.mark.django_db
def test_authenticated_user_can_search_catalog(client, monkeypatch) -> None:
    user = User.objects.create_user(username="viewer", password="StrongPass123")
    client.force_login(user)
    monkeypatch.setattr("catalog.views.CatalogService", lambda: FakeSearchService())

    response = client.get(reverse("catalog_search"), {"q": "Dune"})

    assert response.status_code == 200
    assert response.context["query"] == "Dune"
    assert response.context["results"][0].title == "Dune"
    assert b"Dune" in response.content
    assert b"2021" in response.content


@pytest.mark.django_db
def test_search_page_shows_missing_api_key_message(client, monkeypatch) -> None:
    user = User.objects.create_user(username="viewer", password="StrongPass123")
    client.force_login(user)
    monkeypatch.setattr("catalog.views.CatalogService", lambda: MissingKeyService())

    response = client.get(reverse("catalog_search"), {"q": "Dune"})

    assert response.status_code == 200
    assert "TMDb API key is not configured" in response.context["error_message"]
    assert b"TMDb API key is not configured" in response.content


@pytest.mark.django_db
def test_title_detail_requires_authentication(client) -> None:
    response = client.get(reverse("title_detail", kwargs={"pk": 1}), {"type": "movie"})

    assert response.status_code == 302
    assert response.url.startswith(f"{reverse('login')}?next=")


@pytest.mark.django_db
def test_title_detail_creates_local_title_from_tmdb(client, monkeypatch) -> None:
    user = User.objects.create_user(username="viewer", password="StrongPass123")
    client.force_login(user)

    class DetailService:
        def get_or_sync_title(self, media_type, tmdb_id):
            return Title.objects.create(type=media_type, tmdb_id=tmdb_id, title="Dune")

    monkeypatch.setattr("catalog.views.CatalogService", lambda: DetailService())

    response = client.get(reverse("title_detail", kwargs={"pk": 1}), {"type": "movie"})

    title = Title.objects.get(type=Title.Type.MOVIE, tmdb_id=1)
    assert response.status_code == 200
    assert response.context["title"] == title
    assert b"Dune" in response.content


@pytest.mark.django_db
def test_title_detail_can_load_existing_local_title_without_type_query(client) -> None:
    user = User.objects.create_user(username="viewer", password="StrongPass123")
    title = Title.objects.create(type=Title.Type.TV, tmdb_id=2, title="Silo")
    client.force_login(user)

    response = client.get(reverse("title_detail", kwargs={"pk": title.pk}))

    assert response.status_code == 200
    assert response.context["title"] == title


@pytest.mark.django_db
def test_title_detail_shows_missing_api_key_message(client, monkeypatch) -> None:
    user = User.objects.create_user(username="viewer", password="StrongPass123")
    client.force_login(user)

    class DetailService:
        def get_or_sync_title(self, media_type, tmdb_id):
            raise TMDbClientError("TMDB_API_KEY is not configured")

    monkeypatch.setattr("catalog.views.CatalogService", lambda: DetailService())

    response = client.get(reverse("title_detail", kwargs={"pk": 1}), {"type": "movie"})

    assert response.status_code == 200
    assert "TMDB_API_KEY is not configured" in response.context["error_message"]
    assert b"TMDB_API_KEY is not configured" in response.content
