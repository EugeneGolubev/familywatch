from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from .models import Household, HouseholdMembership

User = get_user_model()


class HouseholdService:
    @staticmethod
    @transaction.atomic
    def create_household_for_user(*, user: User, name: str, default_country: str = "PL") -> Household:
        household = Household.objects.create(
            name=name.strip(),
            owner=user,
            default_country=default_country,
        )
        HouseholdMembership.objects.create(
            household=household,
            user=user,
            role=HouseholdMembership.Role.OWNER,
        )
        from lists.services import HouseholdListService

        HouseholdListService.create_default_categories(household=household, user=user)
        return household


def households_for_user(user: User) -> QuerySet[Household]:
    return (
        Household.objects.filter(memberships__user=user)
        .select_related("owner")
        .prefetch_related("memberships__user")
        .order_by("name", "id")
    )


def get_household_for_member(*, user: User, pk: int) -> Household:
    return get_object_or_404(households_for_user(user), pk=pk)


def get_membership(*, user: User, household: Household) -> HouseholdMembership:
    return get_object_or_404(
        HouseholdMembership.objects.select_related("household", "user"),
        household=household,
        user=user,
    )


def user_is_household_owner(user: User, household: Household) -> bool:
    return HouseholdMembership.objects.filter(
        household=household,
        user=user,
        role=HouseholdMembership.Role.OWNER,
    ).exists()
