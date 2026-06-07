# Phase 5 Instructions: Streaming Availability Deferred

Phase 5 streaming availability has been intentionally deferred.

Manual availability entry would create too much admin work for the MVP. Future
streaming availability should be API-backed, with local data used as a normalized
cache rather than as hand-maintained source data.

## Current decision

- Do not build manual streaming availability data-entry workflows.
- Do not add a title-detail "where to watch" UI until availability can be
  populated automatically.
- Do not add scheduled sync, Celery refresh tasks, recommendations,
  notifications, invitations, public reviews, or social feeds as part of this
  deferred phase.
- Keep the existing `streaming` app as a placeholder for future API-backed work.

## Future API-backed design

When streaming availability becomes active again, first choose an availability
API/provider. Then implement the feature as a small cached integration:

1. Add the external client under `integrations`.
2. Read credentials from environment variables.
3. Keep the app usable when credentials are missing.
4. Normalize provider identity, country, availability type, and watch links into
   local cache models.
5. Link cached availability to existing `catalog.Title` records. Do not
   duplicate title metadata.
6. Add services for fetching/syncing availability, listing availability for a
   title/country, and resolving viewer country.
7. Add title-detail UI only after automatic population is available.
8. Add tests for the integration boundary, cache update behavior, title-detail
   display, missing credentials, country fallback, and permission behavior.

## Guardrails

- Keep MVP simple.
- Do not add React.
- Use Django Templates and HTMX only where useful.
- Prefer service classes over business logic in views.
- Keep external API clients inside `integrations`.
- Store API keys only in environment variables.
- Avoid user-specific availability rows.
- Avoid admin/manual workflows as the primary data source.

## Verification for this deferral

After deferral-only changes, run:

```bash
docker compose config
docker compose run --rm web python manage.py check
docker compose run --rm web python manage.py makemigrations --check --dry-run
docker compose run --rm web pytest
```
