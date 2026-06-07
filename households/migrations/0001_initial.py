# Generated manually for Phase 1 skeleton
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="Household",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("default_country", models.CharField(default="PL", max_length=2)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="owned_households", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="HouseholdMembership",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("owner", "Owner"), ("member", "Member")], default="member", max_length=20)),
                ("joined_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("household", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="memberships", to="households.household")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="household_memberships", to=settings.AUTH_USER_MODEL)),
            ],
            options={"unique_together": {("household", "user")}},
        ),
    ]
