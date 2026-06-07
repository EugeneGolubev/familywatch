# Generated manually for Phase 1 skeleton
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True
    dependencies = [("catalog", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="StreamingProvider",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tmdb_id", models.PositiveIntegerField(unique=True)),
                ("name", models.CharField(max_length=120)),
                ("logo_path", models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="TitleStreamingAvailability",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("country", models.CharField(max_length=2)),
                ("link", models.URLField(blank=True)),
                ("availability_type", models.CharField(choices=[("stream", "Stream"), ("rent", "Rent"), ("buy", "Buy"), ("free", "Free"), ("ads", "Ads")], max_length=20)),
                ("last_checked_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("provider", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="title_availability", to="streaming.streamingprovider")),
                ("title", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="streaming_availability", to="catalog.title")),
            ],
            options={"unique_together": {("title", "provider", "country", "availability_type")}},
        ),
    ]
