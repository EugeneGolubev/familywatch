# Phase 3 Catalog Search Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build authenticated catalog search and title detail pages backed by TMDb while preserving local `Title` records.

**Architecture:** Keep TMDb HTTP access in `integrations.tmdb`, put catalog business behavior in `catalog.services`, and keep Django views limited to request parsing and rendering. Reuse the existing `Title` model and its `(type, tmdb_id)` uniqueness constraint.

**Tech Stack:** Django, Django Templates, HTMX-ready templates, pytest, responses, Docker Compose.

---

### Task 1: TMDb Result Normalization

**Files:**
- Modify: `integrations/tmdb.py`
- Test: `tests/test_tmdb_client.py`

- [ ] Write failing tests for movie/TV result normalization and filtering out unsupported media types.
- [ ] Run `docker compose run --rm web pytest tests/test_tmdb_client.py -q` and confirm the new tests fail because normalization is missing.
- [ ] Add a small normalized result dataclass and normalization helpers in `integrations.tmdb`.
- [ ] Re-run the TMDb client tests and confirm they pass.

### Task 2: Catalog Service Layer

**Files:**
- Create: `catalog/services.py`
- Test: `tests/test_catalog_services.py`

- [ ] Write failing tests for search behavior, missing API key handling, detail fetching, upsert behavior, preserving existing data when TMDb omits optional fields, and avoiding duplicate titles.
- [ ] Run `docker compose run --rm web pytest tests/test_catalog_services.py -q` and confirm failures are for missing services.
- [ ] Implement `CatalogService` with `search`, `get_or_sync_title`, and title upsert helpers.
- [ ] Re-run service tests and confirm they pass.

### Task 3: Catalog Views And Templates

**Files:**
- Modify: `catalog/views.py`
- Modify: `templates/catalog/search.html`
- Modify: `templates/catalog/title_detail.html`
- Test: `tests/test_catalog_views.py`

- [ ] Write failing tests for authenticated search access, unauthenticated redirects, missing key UI context, result rendering context, title detail access, and local title creation/update from TMDb.
- [ ] Run `docker compose run --rm web pytest tests/test_catalog_views.py -q` and confirm the expected failures.
- [ ] Wire thin views to `CatalogService`.
- [ ] Update templates to render helpful empty/error states, results, posters, metadata, and detail pages.
- [ ] Re-run view tests and confirm they pass.

### Task 4: Documentation And Verification

**Files:**
- Modify: `README.md`
- Modify: `AGENTS.md`

- [ ] Update project status and Phase 3 usage notes.
- [ ] Run `docker compose config`.
- [ ] Run `docker compose run --rm web python manage.py check`.
- [ ] Run `docker compose run --rm web python manage.py makemigrations --check --dry-run`.
- [ ] Run `docker compose run --rm web python manage.py migrate`.
- [ ] Run `docker compose run --rm web pytest`.
