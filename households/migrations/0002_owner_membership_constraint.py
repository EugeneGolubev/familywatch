# Generated manually for Phase 2 households
from django.db import migrations, models
from django.db.models import Q


class Migration(migrations.Migration):
    dependencies = [
        ("households", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="householdmembership",
            constraint=models.UniqueConstraint(
                condition=Q(role="owner"),
                fields=("household",),
                name="unique_owner_membership_per_household",
            ),
        ),
    ]
