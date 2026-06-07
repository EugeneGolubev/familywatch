# FamilyWatch Movies

Personal and household movie/TV tracking service built with Django, HTMX, PostgreSQL, Redis, Celery, and Docker Compose.

## Current status

Phase 1 scaffold is complete and has passed the quality check. Phase 2 accounts
and household onboarding is complete. Phase 3 catalog search and title details
are complete. Phase 4 personal watch states and household lists are complete.

Verified in Docker Compose:

- Compose configuration loads without requiring a local `.env`
- Django system check passes
- Migrations are present and match the current models
- Migrations apply successfully against PostgreSQL
- Pytest suite passes

## Phase 1 scope

This repository currently includes:

- Django project skeleton
- Docker Compose setup with PostgreSQL and Redis health checks
- PostgreSQL service used by app containers by default
- Redis service used by Celery by default
- Celery worker and beat services
- Basic Django apps
- Initial domain models
- TMDb client skeleton with caching and basic rate-limit error handling
- Minimal templates and routes
- Django admin registration
- Initial pytest tests

## Phase 2 scope

This repository now includes:

- User registration with Django auth
- Login and POST-based logout behavior with Django auth views
- Automatic `UserProfile` creation for registered and directly created users
- Household creation flow for logged-in users
- Automatic owner membership creation during household setup
- Database rules preventing duplicate memberships and more than one owner
  membership per household
- Household dashboard and detail pages restricted to household members
- Explicit admin configuration for profiles, households, and memberships
- Tests for account/profile creation, household creation, membership roles, and
  dashboard/detail permissions

## Phase 3 scope

This repository now includes:

- Authenticated catalog search backed by the TMDb integration
- Normalized TMDb movie and TV search results with title, type, year, overview,
  and poster metadata
- Title detail pages that sync local `Title` rows from TMDb on first open
- Local title upserts that preserve existing metadata when TMDb omits optional
  fields
- Duplicate protection for the same TMDb id and title type through the existing
  `(type, tmdb_id)` database constraint
- Helpful UI messages when `TMDB_API_KEY` is not configured
- Tests for TMDb normalization, catalog services, missing API key behavior,
  authenticated/unauthenticated access, detail sync, and duplicate prevention

## Phase 4 scope

This repository now includes:

- Personal title states for authenticated users: planned, watching, watched,
  dropped, favorite, and not interested
- Personal rating, notes, and watched date/time metadata
- Add/update personal state from local title detail pages
- "My List" page with status filtering and remove actions
- Household shared lists restricted to household members
- Household list creation, detail pages, local title add actions, and remove
  actions
- Duplicate-safe service behavior for personal states, household list names, and
  household list items
- Tests for personal services/forms/views, catalog integration, household list
  permissions, duplicate handling, and removal behavior

## Requirements

- Docker Desktop on Windows, or Docker Engine + Docker Compose on Linux
- TMDb API key for later catalog search work

## Setup

The Compose file works with built-in development defaults, but copying the example
is recommended before running the app:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set:

```env
DJANGO_SECRET_KEY=your-local-secret
TMDB_API_KEY=your-tmdb-key-for-tmdb-backed-features
```

## Run development server

```bash
docker compose up --build
```

Open:

```text
http://localhost:8000
```

Useful app routes:

```text
http://localhost:8000/accounts/register/
http://localhost:8000/login/
http://localhost:8000/households/
http://localhost:8000/households/create/
http://localhost:8000/catalog/search/
http://localhost:8000/lists/mine/
```

Catalog search requires login. Set `TMDB_API_KEY` in `.env` to enable live TMDb
search and detail sync. Without the key, the app stays usable and shows a
configuration message on catalog pages.

Personal list actions are available from local title detail pages. Household
lists are available from each household detail page and require household
membership.

## Run migrations

```bash
docker compose run --rm web python manage.py migrate
```

## Create superuser

```bash
docker compose run --rm web python manage.py createsuperuser
```

Admin:

```text
http://localhost:8000/admin/
```

## Run tests

```bash
docker compose run --rm web pytest
```

## Useful commands

```bash
docker compose run --rm web python manage.py check
docker compose run --rm web python manage.py makemigrations --check --dry-run
docker compose run --rm web python manage.py shell
docker compose down
docker compose down -v
```

## Quality checks

Before reviewing changes, verify the app with:

```bash
docker compose config
docker compose run --rm web python manage.py check
docker compose run --rm web python manage.py makemigrations --check --dry-run
docker compose run --rm web python manage.py migrate
docker compose run --rm web pytest
```

## Project plan

### Phase 1: Scaffold and quality pass

Status: complete.

Completed:

- Dockerized Django app scaffold
- PostgreSQL, Redis, Celery worker, and Celery beat services
- Initial apps, models, migrations, admin registration, templates, routes, and tests
- TMDb client skeleton inside the integrations app
- Phase 1 setup fixes and Docker Compose verification

### Phase 2: Accounts and household onboarding

Status: complete.

Completed:

- Create household screen
- Auto-create owner membership
- User registration, login, and logout behavior
- Automatic user profiles
- Household dashboard and detail pages
- Membership uniqueness and single-owner constraints
- Member-only household access checks

Deferred:

- Inviting additional household members
- Shared default lists

### Phase 3: Catalog search and title details

Status: complete.

Completed:

- TMDb-backed catalog search for authenticated users
- Movie and TV result normalization
- Search result pages with metadata and poster images when available
- Title detail pages that create or update local `Title` records from TMDb
- Missing TMDb API key handling in services and UI
- Service and view tests for Phase 3 behavior

### Phase 4: Personal watch states and household lists

Status: complete.

Completed:

- Add and update personal title state from title detail pages
- Personal "My List" page with status filtering and remove actions
- Rating validation for personal title states
- Household shared list overview and detail pages
- Household list creation by members
- Add and remove existing local titles from household lists
- Household membership checks for all shared-list pages and actions
- Duplicate-safe services for existing personal states, list names, and list
  items

### Later phases

Planned direction:

- Streaming availability and recommendations
- Background sync tasks and scheduled refreshes

Phase implementation instructions remain available for reference in:

```text
docs/phase-3-instructions.md
docs/phase-4-instructions.md
```
