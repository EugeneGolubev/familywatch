from django.conf import settings
from django.db import models
from django.utils import timezone


class Household(models.Model):
    name = models.CharField(max_length=120)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_households")
    default_country = models.CharField(max_length=2, default="PL")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name


class HouseholdMembership(models.Model):
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        MEMBER = "member", "Member"

    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="household_memberships")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("household", "user")

    def __str__(self) -> str:
        return f"{self.user} in {self.household} ({self.role})"
