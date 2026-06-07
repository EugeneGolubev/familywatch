import pytest
from django.contrib.auth.models import User

from catalog.models import Title
from households.models import Household, HouseholdMembership
from lists.models import UserTitleState


@pytest.mark.django_db
def test_household_membership_unique_owner() -> None:
    user = User.objects.create_user(username="eugene", password="testpass123")
    household = Household.objects.create(name="Home", owner=user, default_country="PL")
    membership = HouseholdMembership.objects.create(
        household=household,
        user=user,
        role=HouseholdMembership.Role.OWNER,
    )

    assert str(household) == "Home"
    assert membership.role == HouseholdMembership.Role.OWNER


@pytest.mark.django_db
def test_user_title_state_defaults_to_planned() -> None:
    user = User.objects.create_user(username="wife", password="testpass123")
    title = Title.objects.create(type=Title.Type.MOVIE, tmdb_id=1, title="Dune")
    state = UserTitleState.objects.create(user=user, title=title)

    assert state.status == UserTitleState.Status.PLANNED
    assert state.rating is None
