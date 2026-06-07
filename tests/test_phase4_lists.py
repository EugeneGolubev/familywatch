from datetime import datetime

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from catalog.models import Title
from households.models import HouseholdMembership
from households.services import HouseholdService
from lists.forms import PersonalTitleStateForm
from lists.models import HouseholdList, HouseholdListItem, UserTitleState
from lists.services import HouseholdListService, PersonalTitleStateService


def create_title(*, title: str = "Dune", tmdb_id: int = 1) -> Title:
    return Title.objects.create(type=Title.Type.MOVIE, tmdb_id=tmdb_id, title=title)


@pytest.mark.django_db
def test_personal_state_service_creates_state_for_title() -> None:
    user = User.objects.create_user(username="viewer", password="StrongPass123")
    title = create_title()
    watched_at = timezone.make_aware(datetime(2026, 1, 2, 20, 30))

    state, created = PersonalTitleStateService.add_or_update(
        user=user,
        title=title,
        status=UserTitleState.Status.WATCHED,
        rating=9,
        notes="Great family pick.",
        watched_at=watched_at,
    )

    assert created is True
    assert state.user == user
    assert state.title == title
    assert state.status == UserTitleState.Status.WATCHED
    assert state.rating == 9
    assert state.notes == "Great family pick."
    assert state.watched_at == watched_at


@pytest.mark.django_db
def test_personal_state_service_updates_without_creating_duplicate() -> None:
    user = User.objects.create_user(username="viewer", password="StrongPass123")
    title = create_title()
    state, _ = PersonalTitleStateService.add_or_update(
        user=user,
        title=title,
        status=UserTitleState.Status.PLANNED,
        rating=7,
        notes="Keep this note.",
    )

    updated, created = PersonalTitleStateService.add_or_update(
        user=user,
        title=title,
        status=UserTitleState.Status.WATCHING,
    )

    assert created is False
    assert updated.pk == state.pk
    assert updated.status == UserTitleState.Status.WATCHING
    assert updated.rating == 7
    assert updated.notes == "Keep this note."
    assert UserTitleState.objects.filter(user=user, title=title).count() == 1


@pytest.mark.django_db
def test_personal_state_form_validates_rating_range() -> None:
    form = PersonalTitleStateForm(
        data={
            "status": UserTitleState.Status.PLANNED,
            "rating": "11",
            "notes": "",
            "watched_at": "",
        }
    )

    assert form.is_valid() is False
    assert "rating" in form.errors


@pytest.mark.django_db
def test_personal_state_service_removes_state() -> None:
    user = User.objects.create_user(username="viewer", password="StrongPass123")
    title = create_title()
    PersonalTitleStateService.add_or_update(user=user, title=title)

    removed = PersonalTitleStateService.remove(user=user, title=title)

    assert removed is True
    assert not UserTitleState.objects.filter(user=user, title=title).exists()


@pytest.mark.django_db
def test_my_list_requires_authentication(client) -> None:
    response = client.get(reverse("my_list"))

    assert response.status_code == 302
    assert response.url.startswith(f"{reverse('login')}?next=")


@pytest.mark.django_db
def test_my_list_shows_only_current_user_records(client) -> None:
    user = User.objects.create_user(username="viewer", password="StrongPass123")
    other = User.objects.create_user(username="other", password="StrongPass123")
    visible = create_title(title="Dune", tmdb_id=1)
    hidden = create_title(title="Silo", tmdb_id=2)
    PersonalTitleStateService.add_or_update(user=user, title=visible)
    PersonalTitleStateService.add_or_update(user=other, title=hidden)
    client.force_login(user)

    response = client.get(reverse("my_list"))

    assert response.status_code == 200
    assert list(response.context["states"]) == list(UserTitleState.objects.filter(user=user))
    assert b"Dune" in response.content
    assert b"Silo" not in response.content


@pytest.mark.django_db
def test_my_list_filters_by_status(client) -> None:
    user = User.objects.create_user(username="viewer", password="StrongPass123")
    planned = create_title(title="Dune", tmdb_id=1)
    watched = create_title(title="Arrival", tmdb_id=2)
    PersonalTitleStateService.add_or_update(user=user, title=planned, status=UserTitleState.Status.PLANNED)
    PersonalTitleStateService.add_or_update(user=user, title=watched, status=UserTitleState.Status.WATCHED)
    client.force_login(user)

    response = client.get(reverse("my_list"), {"status": UserTitleState.Status.WATCHED})

    assert response.status_code == 200
    assert list(response.context["states"]) == list(UserTitleState.objects.filter(user=user, status=UserTitleState.Status.WATCHED))
    assert b"Arrival" in response.content
    assert b"Dune" not in response.content


@pytest.mark.django_db
def test_title_detail_exposes_personal_state_context(client) -> None:
    user = User.objects.create_user(username="viewer", password="StrongPass123")
    title = create_title()
    PersonalTitleStateService.add_or_update(user=user, title=title, status=UserTitleState.Status.FAVORITE)
    client.force_login(user)

    response = client.get(reverse("title_detail", kwargs={"pk": title.pk}))

    assert response.status_code == 200
    assert response.context["personal_state"].status == UserTitleState.Status.FAVORITE
    assert "personal_form" in response.context
    assert b"Update personal state" in response.content


@pytest.mark.django_db
def test_personal_state_post_adds_title_from_detail(client) -> None:
    user = User.objects.create_user(username="viewer", password="StrongPass123")
    title = create_title()
    client.force_login(user)

    response = client.post(
        reverse("personal_title_state", kwargs={"title_pk": title.pk}),
        {
            "status": UserTitleState.Status.WATCHING,
            "rating": "8",
            "notes": "Started with the household.",
            "watched_at": "",
        },
    )

    assert response.status_code == 302
    state = UserTitleState.objects.get(user=user, title=title)
    assert state.status == UserTitleState.Status.WATCHING
    assert state.rating == 8
    assert state.notes == "Started with the household."


@pytest.mark.django_db
def test_household_list_creation_by_member() -> None:
    user = User.objects.create_user(username="owner", password="StrongPass123")
    household = HouseholdService.create_household_for_user(user=user, name="Home")

    household_list, created = HouseholdListService.create_list(
        user=user,
        household_pk=household.pk,
        name="Weekend",
    )

    assert created is True
    assert household_list.household == household
    assert household_list.name == "Weekend"
    assert household_list.created_by == user


@pytest.mark.django_db
def test_duplicate_household_list_name_reuses_existing_list() -> None:
    user = User.objects.create_user(username="owner", password="StrongPass123")
    household = HouseholdService.create_household_for_user(user=user, name="Home")
    existing, _ = HouseholdListService.create_list(user=user, household_pk=household.pk, name="Weekend")

    household_list, created = HouseholdListService.create_list(
        user=user,
        household_pk=household.pk,
        name="Weekend",
    )

    assert created is False
    assert household_list.pk == existing.pk
    assert HouseholdList.objects.filter(household=household, name="Weekend").count() == 1


@pytest.mark.django_db
def test_household_list_overview_shows_member_lists_only(client) -> None:
    user = User.objects.create_user(username="viewer", password="StrongPass123")
    other = User.objects.create_user(username="other", password="StrongPass123")
    visible_household = HouseholdService.create_household_for_user(user=user, name="Visible Home")
    hidden_household = HouseholdService.create_household_for_user(user=other, name="Hidden Home")
    visible, _ = HouseholdListService.create_list(user=user, household_pk=visible_household.pk, name="Visible List")
    hidden, _ = HouseholdListService.create_list(user=other, household_pk=hidden_household.pk, name="Hidden List")
    client.force_login(user)

    response = client.get(reverse("household_lists", kwargs={"household_pk": visible_household.pk}))

    assert response.status_code == 200
    assert visible in response.context["household_lists"]
    assert hidden not in response.context["household_lists"]
    assert b"Visible List" in response.content
    assert b"Hidden List" not in response.content


@pytest.mark.django_db
def test_household_list_detail_access_for_member(client) -> None:
    owner = User.objects.create_user(username="owner", password="StrongPass123")
    member = User.objects.create_user(username="member", password="StrongPass123")
    household = HouseholdService.create_household_for_user(user=owner, name="Home")
    HouseholdMembership.objects.create(household=household, user=member, role=HouseholdMembership.Role.MEMBER)
    household_list, _ = HouseholdListService.create_list(user=owner, household_pk=household.pk, name="Family")
    client.force_login(member)

    response = client.get(reverse("household_list_detail", kwargs={"household_pk": household.pk, "list_pk": household_list.pk}))

    assert response.status_code == 200
    assert response.context["household_list"] == household_list


@pytest.mark.django_db
def test_household_list_detail_denied_for_non_member(client) -> None:
    owner = User.objects.create_user(username="owner", password="StrongPass123")
    outsider = User.objects.create_user(username="outsider", password="StrongPass123")
    household = HouseholdService.create_household_for_user(user=owner, name="Home")
    household_list, _ = HouseholdListService.create_list(user=owner, household_pk=household.pk, name="Family")
    client.force_login(outsider)

    response = client.get(reverse("household_list_detail", kwargs={"household_pk": household.pk, "list_pk": household_list.pk}))

    assert response.status_code == 404


@pytest.mark.django_db
def test_add_title_to_household_list() -> None:
    user = User.objects.create_user(username="owner", password="StrongPass123")
    household = HouseholdService.create_household_for_user(user=user, name="Home")
    household_list, _ = HouseholdListService.create_list(user=user, household_pk=household.pk, name="Family")
    title = create_title()

    item, created = HouseholdListService.add_title(
        user=user,
        household_pk=household.pk,
        list_pk=household_list.pk,
        title=title,
    )

    assert created is True
    assert item.household_list == household_list
    assert item.title == title
    assert item.added_by == user
    assert not UserTitleState.objects.filter(user=user, title=title).exists()


@pytest.mark.django_db
def test_duplicate_household_list_item_reuses_existing_item() -> None:
    user = User.objects.create_user(username="owner", password="StrongPass123")
    household = HouseholdService.create_household_for_user(user=user, name="Home")
    household_list, _ = HouseholdListService.create_list(user=user, household_pk=household.pk, name="Family")
    title = create_title()
    existing, _ = HouseholdListService.add_title(user=user, household_pk=household.pk, list_pk=household_list.pk, title=title)

    item, created = HouseholdListService.add_title(user=user, household_pk=household.pk, list_pk=household_list.pk, title=title)

    assert created is False
    assert item.pk == existing.pk
    assert HouseholdListItem.objects.filter(household_list=household_list, title=title).count() == 1


@pytest.mark.django_db
def test_remove_household_list_item() -> None:
    user = User.objects.create_user(username="owner", password="StrongPass123")
    household = HouseholdService.create_household_for_user(user=user, name="Home")
    household_list, _ = HouseholdListService.create_list(user=user, household_pk=household.pk, name="Family")
    title = create_title()
    item, _ = HouseholdListService.add_title(user=user, household_pk=household.pk, list_pk=household_list.pk, title=title)

    removed = HouseholdListService.remove_item(
        user=user,
        household_pk=household.pk,
        list_pk=household_list.pk,
        item_pk=item.pk,
    )

    assert removed is True
    assert not HouseholdListItem.objects.filter(pk=item.pk).exists()


@pytest.mark.django_db
def test_household_list_actions_reject_non_members() -> None:
    owner = User.objects.create_user(username="owner", password="StrongPass123")
    outsider = User.objects.create_user(username="outsider", password="StrongPass123")
    household = HouseholdService.create_household_for_user(user=owner, name="Home")
    household_list, _ = HouseholdListService.create_list(user=owner, household_pk=household.pk, name="Family")
    title = create_title()

    with pytest.raises(HouseholdList.DoesNotExist):
        HouseholdListService.add_title(
            user=outsider,
            household_pk=household.pk,
            list_pk=household_list.pk,
            title=title,
        )
