from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from catalog.models import Title
from households.models import Household


class UserTitleState(models.Model):
    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        WATCHING = "watching", "Watching"
        WATCHED = "watched", "Watched"
        DROPPED = "dropped", "Dropped"
        FAVORITE = "favorite", "Favorite"
        NOT_INTERESTED = "not_interested", "Not Interested"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="title_states")
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="user_states")
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PLANNED)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    watched_at = models.DateTimeField(null=True, blank=True)
    added_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "title")

    def clean(self) -> None:
        super().clean()
        if self.rating is not None and not 1 <= self.rating <= 10:
            raise ValidationError({"rating": "Rating must be between 1 and 10."})

    def __str__(self) -> str:
        return f"{self.user} - {self.title} - {self.status}"


class HouseholdList(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name="lists")
    name = models.CharField(max_length=120)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="created_household_lists")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("household", "name")

    def __str__(self) -> str:
        return f"{self.household}: {self.name}"


class HouseholdListItem(models.Model):
    household_list = models.ForeignKey(HouseholdList, on_delete=models.CASCADE, related_name="items")
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="household_list_items")
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="added_household_items")
    notes = models.TextField(blank=True)
    added_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("household_list", "title")
