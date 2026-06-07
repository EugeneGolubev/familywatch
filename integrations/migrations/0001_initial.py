# Generated manually for Phase 1 skeleton
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="ExternalSyncLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("source", models.CharField(max_length=50)),
                ("task_name", models.CharField(max_length=120)),
                ("started_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                ("success", models.BooleanField(default=False)),
                ("message", models.TextField(blank=True)),
            ],
            options={"ordering": ["-started_at"]},
        ),
    ]
