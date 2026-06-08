from django.db import migrations


DEFAULT_HOUSEHOLD_CATEGORIES = (
    "Plan to watch together",
    "Watching together",
    "Watched",
    "Watch with Kids",
)


def seed_default_household_categories(apps, schema_editor):
    Household = apps.get_model("households", "Household")
    HouseholdList = apps.get_model("lists", "HouseholdList")

    for household in Household.objects.all():
        for name in DEFAULT_HOUSEHOLD_CATEGORIES:
            HouseholdList.objects.get_or_create(
                household=household,
                name=name,
                defaults={"created_by_id": household.owner_id},
            )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("households", "0002_owner_membership_constraint"),
        ("lists", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_default_household_categories, noop_reverse),
    ]
