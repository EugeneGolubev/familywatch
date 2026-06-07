# AGENTS.md

## Project
FamilyWatch: personal and household movie/TV tracking service.

## Current status
- Phase 1 scaffold and quality pass are complete.
- Phase 2 accounts and household onboarding is complete.
- Phase 3 catalog search and title details are complete.
- Phase 4 personal watch states and household lists are complete.
- Keep future changes focused on the active phase.

## Stack
- Django
- Django Templates + HTMX
- Tailwind CSS or DaisyUI
- PostgreSQL
- Redis
- Celery
- Docker Compose

## Rules
- Keep MVP simple.
- Do not add React.
- Do not hardcode API keys.
- Use environment variables.
- Keep external API clients inside integrations app.
- Prefer service classes over business logic in views.
- Add tests for new models/services.
- All commands should work through Docker Compose.

## Commands
- Start: docker compose up --build
- Check: docker compose run --rm web python manage.py check
- Migrate: docker compose run --rm web python manage.py migrate
- Migration drift check: docker compose run --rm web python manage.py makemigrations --check --dry-run
- Tests: docker compose run --rm web pytest
