# Admin Guide

This guide covers administrative setup and current admin workflows for
FamilyWatch.

## Create an Admin User

Run:

```bash
docker compose run --rm web python manage.py createsuperuser
```

Follow the prompts to create a username, email address, and password.

## Open Django Admin

Start the app:

```bash
docker compose up --build
```

Open:

```text
http://localhost:8000/admin/
```

Log in with the superuser account.

## Manage Users

Use the **Users** section to:

- View user accounts
- Create users manually
- Change passwords
- Mark users as staff
- Mark users as superusers
- Activate or deactivate users

## Manage User Profiles

Each user should have a profile. Profiles are created automatically for new
users.

Profiles include:

- Display name
- Preferred country

The preferred country is used as a fallback for future country-aware features.

## Manage Households

Use the **Households** section to view and edit households.

Households include:

- Name
- Owner
- Default country
- Created timestamp

## Manage Household Memberships

Use household memberships to control which users belong to a household.

Membership roles:

- Owner
- Member

The database allows only one owner membership per household.

## Manage Catalog Data

Catalog data is mostly created from TMDb when users open title detail pages from
catalog search results.

Admin users can inspect or edit:

- Titles
- Genres
- People
- Cast credits
- Seasons
- Episodes

Avoid manually duplicating title metadata that should come from TMDb.

## Manage Personal Watch States

Personal watch states represent a user's relationship to a title.

Statuses:

- Planned
- Watching
- Watched
- Dropped
- Favorite
- Not Interested

Admin users can inspect or edit:

- Status
- Rating
- Notes
- Watched date and time

## Manage Household Lists

Admin users can inspect or edit:

- Household lists
- Household list items
- Who created a list
- Who added an item

Household list access in the app is restricted to household members.

## Streaming Availability

Do not manually enter streaming availability data.

Streaming availability is intentionally deferred until an API-backed provider is
selected. The `streaming` app remains a placeholder for future integration work,
but manual admin data entry is not part of the MVP.

## Configuration Checklist

Check `.env` if the app does not behave as expected:

```env
DJANGO_SECRET_KEY=change-this-to-any-long-random-string
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DATABASE_URL=postgres://familywatch:familywatch@db:5432/familywatch
REDIS_URL=redis://redis:6379/0
TMDB_API_KEY=your-tmdb-api-key
DEFAULT_COUNTRY=PL
```

If catalog search does not work, verify `TMDB_API_KEY`, restart Docker Compose,
and try again.

## Verification Commands

Run a system check:

```bash
docker compose run --rm web python manage.py check
```

Apply migrations:

```bash
docker compose run --rm web python manage.py migrate
```

Check migration drift:

```bash
docker compose run --rm web python manage.py makemigrations --check --dry-run
```

Run tests:

```bash
docker compose run --rm web pytest
```

