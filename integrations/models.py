from django.db import models
from django.utils import timezone


class ExternalSyncLog(models.Model):
    source = models.CharField(max_length=50)
    task_name = models.CharField(max_length=120)
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True, blank=True)
    success = models.BooleanField(default=False)
    message = models.TextField(blank=True)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self) -> str:
        return f"{self.source}:{self.task_name} success={self.success}"
