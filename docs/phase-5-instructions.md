# Phase 5 Instructions: Streaming Availability Foundation

Use this prompt to start Phase 5 in a new Codex thread or branch.

```text
Implement Phase 5: Streaming Availability Foundation.

Context:
This repository has Phase 1 scaffold, Phase 2 accounts and household onboarding,
Phase 3 catalog search/title details, and Phase 4 personal watch states and
household shared lists complete. Before making changes, inspect the existing
apps, models, migrations, views, templates, URLs, admin, tests, README,
AGENTS.md, and the current PR/branch context if available.

Important:
- Keep Phase 5 focused on streaming availability only.
- Do not start recommendations, public reviews, invitations, social activity
  feeds, notifications, or background scheduled sync work.
- Do not add React.
- Use Django Templates and HTMX only where useful.
- Keep MVP simple.
- Keep external API clients inside the integrations app.
- Prefer service classes over business logic in views.
- Add tests for new models/services/forms/views.
- All commands should work through Docker Compose.

Phase 5 goals:
1. Implement a small streaming availability data model using the existing
   streaming app if possible.
2. Represent providers/services, countries, and title availability in a local
   normalized way.
3. Allow availability to be associated with existing local `Title` records.
4. Support basic availability types such as:
   - subscription
   - rent
   - buy
   - free
5. Store optional provider metadata only where appropriate:
   - provider display name
   - provider external id
   - provider logo path or URL
   - deep link / watch link when available
6. Do not duplicate title metadata in streaming models; use relationships to
   existing `Title` records.
7. Add service classes for:
   - listing availability for a title and country
   - upserting provider records
   - replacing or upserting availability records for a title/country
   - household-aware default country lookup when viewing title availability
8. Add a title-detail integration that shows locally stored availability for
   the viewer's country.
9. Use the user's active household/default country where the project already
   supports it; otherwise fall back to the user's profile preferred country or a
   simple project default.
10. Add a compact UI section on title detail pages:
    - show available providers grouped by availability type
    - show a helpful empty state when no availability is known
    - show country context
11. Add a simple admin experience for provider and availability records.
12. Add tests covering the local service behavior and title-detail display.

Suggested route shape:
- Availability can be shown on existing title detail pages.
- Optional simple debug/admin-like authenticated page if useful:
  `/streaming/titles/<int:title_pk>/`
- Do not build a public provider browsing product yet.

Expected files:
- Update or create streaming models only if needed.
- Add migration files for new streaming models/constraints.
- Add or improve streaming service classes.
- Add or modify catalog title detail view/template for availability context.
- Add or improve streaming admin registration.
- Add tests for models/services/views/templates.
- Update README with Phase 5 status, commands, and usage notes.
- Update AGENTS.md project status if appropriate.

Model guidance:
- Prefer a `StreamingProvider` model for provider identity.
- Prefer a `TitleAvailability` model linking:
  - `Title`
  - `StreamingProvider`
  - country code
  - availability type
  - optional watch/deep link
  - timestamps
- Preserve uniqueness to prevent duplicate rows for the same title/provider/
  country/type.
- Keep country codes simple for MVP, such as two-letter uppercase strings.
- Do not store external API payload blobs unless there is a clear MVP need.
- Do not create user-specific availability rows.

Integration guidance:
- If using an external availability API, add the client under `integrations`.
- Do not hardcode API keys.
- Read API keys from environment variables.
- The app must still work when the API key is missing.
- For this phase, local/manual availability data is acceptable. Live API sync is
  optional only if it stays small and well tested.
- Do not add Celery sync tasks in Phase 5; scheduled refresh belongs to a later
  phase.

Permission constraints:
- Title detail pages should follow the existing catalog authentication behavior.
- Any optional streaming-specific page should require authentication.
- Household membership should not be leaked when resolving country context.

UI constraints:
- Keep the MVP simple and template-based.
- Reuse the current base template and Tailwind style.
- Avoid introducing a new design system.
- Keep availability controls read-only for normal users unless a clear admin or
  staff-only path is added.
- Show helpful empty states:
  - no known availability for this title
  - no known availability for the selected country
- Keep provider grouping compact and easy to scan.

Service behavior:
- Availability listing should:
  - return only records for the requested title and country
  - group or order records consistently by availability type and provider name
  - avoid exposing unrelated title availability
- Upsert behavior should:
  - reuse existing providers by stable external id when present
  - avoid duplicate availability records
  - update changed links/provider metadata without duplicating rows
- Country resolution should:
  - prefer a household/default country where project context makes that clear
  - fall back to user profile preferred country
  - fall back to a project default such as `PL`

Testing requirements:
Add or improve tests for:
- streaming provider creation/upsert
- title availability creation/upsert
- duplicate availability behavior
- availability filtering by title
- availability filtering by country
- availability grouping or ordering by availability type/provider
- title detail page includes availability context
- title detail page shows provider names when availability exists
- title detail page shows an empty state when no availability exists
- country resolution fallback behavior
- unauthenticated users are redirected according to existing catalog behavior
- migrations are present and pass drift checks

Verification:
Run through Docker Compose:
- `docker compose config`
- `docker compose run --rm web python manage.py check`
- `docker compose run --rm web python manage.py makemigrations --check --dry-run`
- `docker compose run --rm web python manage.py migrate`
- `docker compose run --rm web pytest`

Output:
- Create a PR.
- Summarize what changed.
- List verification results.
- List remaining risks or missing items.
- Update project documentation.
```

Phase 5 should stay limited to streaming availability foundation. Recommendations,
notifications, background scheduled sync, invitations, and social features should
start in later phases.
