# FamilyWatch Movies

Personal and household movie/TV tracking service built with Django, HTMX, PostgreSQL, Redis, Celery, and Docker Compose.

## Current status

Phase 1 scaffold is complete and has passed the quality check. Phase 2 has not
started yet.

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

## Phase 1 quality checks

Before starting or reviewing Phase 2 work, verify the scaffold with:

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

### Phase 2: Household onboarding

Status: not started.

Planned:

- Create household screen
- Auto-create owner membership
- Add/invite second household member
- Household dashboard with members and shared default lists

### Later phases

Planned direction:

- Catalog search and title details backed by integrations
- Personal watch states and household lists
- Streaming availability and recommendations
- Background sync tasks and scheduled refreshes
