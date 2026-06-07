# FamilyWatch Movies

Personal and household movie/TV tracking service built with Django, HTMX, PostgreSQL, Redis, Celery, and Docker Compose.

## Phase 1 scope

This repository currently includes:

- Django project skeleton
- Docker Compose setup
- PostgreSQL service
- Redis service
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

Copy the environment example:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set at least:

```env
DJANGO_SECRET_KEY=your-local-secret
TMDB_API_KEY=your-tmdb-key
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
docker compose run --rm web python manage.py makemigrations
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
docker compose run --rm web python manage.py shell
docker compose down
docker compose down -v
```

## Next phase

Phase 2 should implement full household creation and membership flows:

- Create household screen
- Auto-create owner membership
- Add/invite second household member
- Household dashboard with members and shared default lists
