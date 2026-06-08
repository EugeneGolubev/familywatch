from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from catalog.models import Title
from households.models import Household
from households.services import get_household_for_member, user_is_household_owner
from lists.models import HouseholdList, HouseholdListItem, UserTitleState

User = get_user_model()
_UNSET = object()

DEFAULT_HOUSEHOLD_CATEGORIES = (
    "Plan to watch together",
    "Watching together",
    "Watched",
    "Watch with Kids",
)


class PersonalTitleStateService:
    @staticmethod
    @transaction.atomic
    def add_or_update(
        *,
        user: User,
        title: Title,
        status: str = UserTitleState.Status.PLANNED,
        rating: int | None | object = _UNSET,
        notes: str | object = _UNSET,
        watched_at=_UNSET,
    ) -> tuple[UserTitleState, bool]:
        state, created = UserTitleState.objects.get_or_create(
            user=user,
            title=title,
            defaults={"status": status},
        )
        state.status = status
        if rating is not _UNSET:
            state.rating = rating
        if notes is not _UNSET:
            state.notes = notes
        if watched_at is not _UNSET:
            state.watched_at = watched_at
        elif status != UserTitleState.Status.WATCHED:
            state.watched_at = None
        state.full_clean()
        state.save()
        return state, created

    @staticmethod
    def list_for_user(*, user: User, status: str = "") -> QuerySet[UserTitleState]:
        states = UserTitleState.objects.filter(user=user).select_related("title").order_by("-added_at", "-id")
        if status in UserTitleState.Status.values:
            states = states.filter(status=status)
        return states

    @staticmethod
    def remove(*, user: User, title: Title) -> bool:
        deleted_count, _ = UserTitleState.objects.filter(user=user, title=title).delete()
        return deleted_count > 0


class HouseholdListService:
    @staticmethod
    def create_default_categories(*, household: Household, user: User) -> None:
        for name in DEFAULT_HOUSEHOLD_CATEGORIES:
            HouseholdList.objects.get_or_create(
                household=household,
                name=name,
                defaults={"created_by": user},
            )

    @staticmethod
    def lists_for_household(*, user: User, household_pk: int) -> tuple[Household, QuerySet[HouseholdList]]:
        household = get_household_for_member(user=user, pk=household_pk)
        household_lists = (
            HouseholdList.objects.filter(household=household)
            .select_related("household", "created_by")
            .prefetch_related("items__title")
            .order_by("name", "id")
        )
        return household, household_lists

    @staticmethod
    def _get_household_for_owner(*, user: User, household_pk: int) -> Household:
        household = get_household_for_member(user=user, pk=household_pk)
        if not user_is_household_owner(user, household):
            raise PermissionDenied("Only the household owner can manage categories.")
        return household

    @staticmethod
    @transaction.atomic
    def create_list(*, user: User, household_pk: int, name: str) -> tuple[HouseholdList, bool]:
        household = get_household_for_member(user=user, pk=household_pk)
        household_list, created = HouseholdList.objects.get_or_create(
            household=household,
            name=name.strip(),
            defaults={"created_by": user},
        )
        return household_list, created

    @staticmethod
    @transaction.atomic
    def create_category(*, user: User, household_pk: int, name: str) -> tuple[HouseholdList, bool]:
        household = HouseholdListService._get_household_for_owner(user=user, household_pk=household_pk)
        household_list, created = HouseholdList.objects.get_or_create(
            household=household,
            name=name.strip(),
            defaults={"created_by": user},
        )
        return household_list, created

    @staticmethod
    @transaction.atomic
    def remove_category(*, user: User, household_pk: int, list_pk: int) -> bool:
        household = HouseholdListService._get_household_for_owner(user=user, household_pk=household_pk)
        deleted_count, _ = HouseholdList.objects.filter(pk=list_pk, household=household).delete()
        return deleted_count > 0

    @staticmethod
    def categories_for_user(*, user: User) -> QuerySet[HouseholdList]:
        return (
            HouseholdList.objects.filter(household__memberships__user=user)
            .select_related("household")
            .order_by("household__name", "name", "id")
        )

    @staticmethod
    def get_list_for_member(*, user: User, household_pk: int, list_pk: int) -> HouseholdList:
        return HouseholdList.objects.select_related("household", "created_by").get(
            pk=list_pk,
            household_id=household_pk,
            household__memberships__user=user,
        )

    @staticmethod
    @transaction.atomic
    def add_title(*, user: User, household_pk: int, list_pk: int, title: Title) -> tuple[HouseholdListItem, bool]:
        household_list = HouseholdListService.get_list_for_member(
            user=user,
            household_pk=household_pk,
            list_pk=list_pk,
        )
        item, created = HouseholdListItem.objects.get_or_create(
            household_list=household_list,
            title=title,
            defaults={"added_by": user},
        )
        return item, created

    @staticmethod
    @transaction.atomic
    def remove_item(*, user: User, household_pk: int, list_pk: int, item_pk: int) -> bool:
        household_list = HouseholdListService.get_list_for_member(
            user=user,
            household_pk=household_pk,
            list_pk=list_pk,
        )
        deleted_count, _ = HouseholdListItem.objects.filter(pk=item_pk, household_list=household_list).delete()
        return deleted_count > 0


def get_title_or_404(*, pk: int) -> Title:
    return get_object_or_404(Title, pk=pk)
