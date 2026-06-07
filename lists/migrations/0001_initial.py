# Generated manually for Phase 1 skeleton
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalog", "0001_initial"),
        ("households", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="UserTitleState",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("planned", "Planned"), ("watching", "Watching"), ("watched", "Watched"), ("dropped", "Dropped"), ("favorite", "Favorite"), ("not_interested", "Not Interested")], default="planned", max_length=30)),
                ("rating", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("notes", models.TextField(blank=True)),
                ("watched_at", models.DateTimeField(blank=True, null=True)),
                ("added_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("title", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="user_states", to="catalog.title")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="title_states", to=settings.AUTH_USER_MODEL)),
            ],
            options={"unique_together": {("user", "title")}},
        ),
        migrations.CreateModel(
            name="HouseholdList",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("created_by", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_household_lists", to=settings.AUTH_USER_MODEL)),
                ("household", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="lists", to="households.household")),
            ],
            options={"unique_together": {("household", "name")}},
        ),
        migrations.CreateModel(
            name="HouseholdListItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("notes", models.TextField(blank=True)),
                ("added_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("added_by", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="added_household_items", to=settings.AUTH_USER_MODEL)),
                ("household_list", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="lists.householdlist")),
                ("title", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="household_list_items", to="catalog.title")),
            ],
            options={"unique_together": {("household_list", "title")}},
        ),
    ]
