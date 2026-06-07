from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=120, blank=True)
    preferred_country = models.CharField(max_length=2, default="PL")

    def __str__(self) -> str:
        return self.display_name or self.user.get_username()
