from django.db import models
from django.utils import timezone

from catalog.models import Title


class StreamingProvider(models.Model):
    tmdb_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=120)
    logo_path = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.name


class TitleStreamingAvailability(models.Model):
    class AvailabilityType(models.TextChoices):
        STREAM = "stream", "Stream"
        RENT = "rent", "Rent"
        BUY = "buy", "Buy"
        FREE = "free", "Free"
        ADS = "ads", "Ads"

    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="streaming_availability")
    provider = models.ForeignKey(StreamingProvider, on_delete=models.CASCADE, related_name="title_availability")
    country = models.CharField(max_length=2)
    link = models.URLField(blank=True)
    availability_type = models.CharField(max_length=20, choices=AvailabilityType.choices)
    last_checked_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("title", "provider", "country", "availability_type")
