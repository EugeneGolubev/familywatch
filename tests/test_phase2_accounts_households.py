import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse

from accounts.models import UserProfile
from households.models import Household, HouseholdMembership
from households.services import HouseholdService, user_is_household_owner


@pytest.mark.django_db
def test_registration_creates_user_profile(client) -> None:
    response = client.post(
        reverse("register"),
        {
            "username": "parent",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
        },
    )

    user = User.objects.get(username="parent")

    assert response.status_code == 302
    assert hasattr(user, "profile")
    assert user.profile.preferred_country == "PL"


@pytest.mark.django_db
def test_profile_is_created_for_direct_user_creation() -> None:
    user = User.objects.create_user(username="direct", password="StrongPass123")

    assert UserProfile.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_create_household_service_creates_owner_membership() -> None:
    user = User.objects.create_user(username="owner", password="StrongPass123")

    household = HouseholdService.create_household_for_user(user=user, name="Movie Home", default_country="US")

    membership = HouseholdMembership.objects.get(household=household, user=user)
    assert household.name == "Movie Home"
    assert household.owner == user
    assert household.default_country == "US"
    assert membership.role == HouseholdMembership.Role.OWNER


@pytest.mark.django_db
def test_duplicate_household_memberships_are_rejected() -> None:
    user = User.objects.create_user(username="member", password="StrongPass123")
    household = HouseholdService.create_household_for_user(user=user, name="Home")

    with pytest.raises(IntegrityError):
        HouseholdMembership.objects.create(
            household=household,
            user=user,
            role=HouseholdMembership.Role.MEMBER,
        )


@pytest.mark.django_db
def test_household_allows_only_one_owner_membership() -> None:
    owner = User.objects.create_user(username="owner", password="StrongPass123")
    other = User.objects.create_user(username="other", password="StrongPass123")
    household = HouseholdService.create_household_for_user(user=owner, name="Home")

    with pytest.raises(IntegrityError):
        HouseholdMembership.objects.create(
            household=household,
            user=other,
            role=HouseholdMembership.Role.OWNER,
        )


@pytest.mark.django_db
def test_user_is_household_owner_only_for_owner_membership() -> None:
    owner = User.objects.create_user(username="owner", password="StrongPass123")
    member = User.objects.create_user(username="member", password="StrongPass123")
    household = HouseholdService.create_household_for_user(user=owner, name="Home")
    HouseholdMembership.objects.create(
        household=household,
        user=member,
        role=HouseholdMembership.Role.MEMBER,
    )

    assert user_is_household_owner(owner, household) is True
    assert user_is_household_owner(member, household) is False


@pytest.mark.django_db
def test_create_household_view_creates_household_for_current_user(client) -> None:
    user = User.objects.create_user(username="creator", password="StrongPass123")
    client.force_login(user)

    response = client.post(reverse("household_create"), {"name": "Weekend Watchers", "default_country": "GB"})

    household = Household.objects.get(name="Weekend Watchers")
    assert response.status_code == 302
    assert response.url == reverse("household_detail", kwargs={"pk": household.pk})
    assert HouseholdMembership.objects.filter(
        household=household,
        user=user,
        role=HouseholdMembership.Role.OWNER,
    ).exists()


@pytest.mark.django_db
def test_household_dashboard_lists_only_member_households(client) -> None:
    user = User.objects.create_user(username="viewer", password="StrongPass123")
    other = User.objects.create_user(username="other", password="StrongPass123")
    visible = HouseholdService.create_household_for_user(user=user, name="Visible Home")
    hidden = HouseholdService.create_household_for_user(user=other, name="Hidden Home")
    client.force_login(user)

    response = client.get(reverse("household_dashboard"))

    assert response.status_code == 200
    assert list(response.context["households"]) == [visible]
    assert hidden not in response.context["households"]


@pytest.mark.django_db
def test_user_can_access_household_detail_when_member(client) -> None:
    owner = User.objects.create_user(username="owner", password="StrongPass123")
    member = User.objects.create_user(username="member", password="StrongPass123")
    household = HouseholdService.create_household_for_user(user=owner, name="Home")
    HouseholdMembership.objects.create(
        household=household,
        user=member,
        role=HouseholdMembership.Role.MEMBER,
    )
    client.force_login(member)

    response = client.get(reverse("household_detail", kwargs={"pk": household.pk}))

    assert response.status_code == 200
    assert response.context["household"] == household
    assert response.context["membership"].role == HouseholdMembership.Role.MEMBER
    assert response.context["is_owner"] is False


@pytest.mark.django_db
def test_user_cannot_access_household_detail_when_not_member(client) -> None:
    owner = User.objects.create_user(username="owner", password="StrongPass123")
    outsider = User.objects.create_user(username="outsider", password="StrongPass123")
    household = HouseholdService.create_household_for_user(user=owner, name="Private Home")
    client.force_login(outsider)

    response = client.get(reverse("household_detail", kwargs={"pk": household.pk}))

    assert response.status_code == 404
