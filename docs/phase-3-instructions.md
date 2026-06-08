# Phase 3 Instructions: Catalog Search and Title Details

Use this prompt to start Phase 3 in a new Codex thread or branch.

```text
Implement Phase 3: Catalog Search and Title Details.

Context:
This repository has Phase 1 scaffold and Phase 2 accounts/household onboarding complete. Before making changes, inspect the existing apps, models, migrations, views, templates, URLs, admin, tests, README, AGENTS.md, and the current PR/branch context if available.

Important:
- Do not duplicate existing models or migrations.
- Reuse and improve the existing catalog and integrations app code.
- Keep Phase 3 focused on catalog search and title details only.
- Do not start watchlist, streaming availability, recommendations, ratings, reviews, invitations, or shared list features.
- Do not add React.
- Use Django Templates and HTMX only where useful.
- Keep external API clients inside the integrations app.
- Do not hardcode API keys.
- Use environment variables.
- Keep views thin.
- Prefer services over business logic in views.
- Add tests for new models/services/views.
- All commands should work through Docker Compose.

Phase 3 goals:
1. Implement catalog search backed by the existing TMDb integration.
2. Allow authenticated users to search for movies and TV shows.
3. Display search results with basic metadata:
   - title/name
   - media type: movie or TV
   - release year or first air year when available
   - overview/description when available
   - poster path/image when available
4. Implement title detail page.
5. When a user opens a title detail:
   - fetch detail data from TMDb if needed
   - create or update the local Title record
   - display local + TMDb metadata
6. Reuse existing Title model if it exists.
7. Add or improve a catalog service layer for:
   - searching TMDb
   - normalizing TMDb search results
   - upserting local Title records
   - fetching title details
8. Keep TMDb API access inside integrations app.
9. Handle missing TMDb API key gracefully:
   - app should not crash
   - show a helpful message in the UI
   - tests should cover this behavior
10. Add basic templates/routes for:
   - catalog search page
   - search results
   - title detail page

Suggested route shape:
- `/catalog/search/`
- `/catalog/titles/<int:pk>/`
- Optional HTMX partial for search results if it fits the current template style

Expected files:
- Update existing catalog models only if needed.
- Include migration files only if model changes are required.
- Add/modify catalog services.
- Add/modify integrations TMDb client only inside integrations app.
- Add/modify catalog forms, views, URLs, templates, admin, and tests.
- Update README with Phase 3 status, commands, and usage notes.
- Update AGENTS.md project status if appropriate.

Model constraints:
- Do not create duplicate Title rows for the same TMDb title.
- Preserve existing data when updating a Title from TMDb.
- If the existing Title model has `tmdb_id` and `type`, enforce or preserve uniqueness for that pair.
- Keep the model simple. Do not add user-specific watch state in Phase 3.

Testing requirements:
Add or improve tests for:
- TMDb client search normalization
- catalog service search behavior
- missing API key behavior
- local Title upsert behavior
- search page access for authenticated users
- unauthenticated users redirected to login
- title detail page access
- title detail creates or updates local Title
- no duplicate Title for same TMDb id/type

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

Phase 3 should stay limited to catalog search and title detail pages. Personal
watch states, household lists, streaming availability, and recommendations should
start in later phases.
