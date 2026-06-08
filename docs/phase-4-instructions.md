# Phase 4 Instructions: Personal Watch States and Household Lists

Use this prompt to start Phase 4 in a new Codex thread or branch.

```text
Implement Phase 4: Personal Watch States and Household Lists.

Context:
This repository has Phase 1 scaffold, Phase 2 accounts/household onboarding,
and Phase 3 catalog search/title details complete. Before making changes,
inspect the existing apps, models, migrations, views, templates, URLs, admin,
tests, README, AGENTS.md, and the current PR/branch context if available.

Important:
- Do not duplicate existing models or migrations.
- Reuse and improve the existing lists, catalog, and households app code.
- Keep Phase 4 focused on personal watch states and household lists only.
- Do not start streaming availability, recommendations, public reviews,
  invitations, social activity feeds, notifications, or background sync work.
- Do not add React.
- Use Django Templates and HTMX only where useful.
- Keep views thin.
- Prefer service classes over business logic in views.
- Add tests for new models/services/forms/views.
- All commands should work through Docker Compose.

Phase 4 goals:
1. Implement personal title state management using the existing
   `UserTitleState` model if it exists.
2. Allow authenticated users to add a local `Title` to their personal list from
   a title detail page or another existing catalog entry point.
3. Allow authenticated users to update their own title state:
   - planned
   - watching
   - watched
   - dropped
   - favorite
   - not interested
4. Allow users to optionally store personal metadata already supported by the
   existing model:
   - rating
   - notes
   - watched date/time when status is watched
5. Implement a usable "My List" page that shows only the current user's title
   states.
6. Add basic filtering on "My List" by status.
7. Allow users to remove a title from their personal list.
8. Implement household shared lists using the existing `HouseholdList` and
   `HouseholdListItem` models if they exist.
9. Allow household members to view household lists for households they belong
   to.
10. Allow household members to create a simple household list with a name.
11. Allow household members to add existing local `Title` records to a
    household list.
12. Allow household members to remove titles from a household list.
13. Enforce household membership permissions for all household list pages and
    actions.
14. Preserve existing uniqueness constraints:
    - one `UserTitleState` per `(user, title)`
    - one `HouseholdList` per `(household, name)`
    - one `HouseholdListItem` per `(household_list, title)`
15. Handle duplicate add/create attempts gracefully:
    - app should not crash
    - existing records should be reused or a helpful message should be shown
    - tests should cover this behavior
16. Keep personal state separate from household shared lists. A title appearing
    in a household list should not automatically change an individual user's
    personal watch state.
17. Keep Phase 4 pages simple and useful with Django templates:
    - "My List"
    - household list overview
    - household list detail
    - small forms or POST actions for add/update/remove flows

Suggested route shape:
- `/lists/mine/`
- `/lists/mine/?status=planned`
- `/lists/mine/titles/<int:title_pk>/`
- `/lists/mine/titles/<int:title_pk>/remove/`
- `/lists/households/<int:household_pk>/`
- `/lists/households/<int:household_pk>/create/`
- `/lists/households/<int:household_pk>/<int:list_pk>/`
- `/lists/households/<int:household_pk>/<int:list_pk>/add/`
- `/lists/households/<int:household_pk>/<int:list_pk>/items/<int:item_pk>/remove/`
- Optional HTMX partials for list updates if they fit the current template style

Expected files:
- Update existing lists models only if needed.
- Include migration files only if model changes are required.
- Add or improve list service classes for:
  - personal state upsert/update/remove
  - personal list filtering
  - household list creation
  - household list item add/remove
  - household membership permission checks
- Add or improve list forms for:
  - personal title state
  - household list creation
  - adding titles to household lists
- Add or modify list views, URLs, templates, admin, and tests.
- Add a small integration point from catalog title detail to personal list
  actions if appropriate.
- Update README with Phase 4 status, commands, and usage notes.
- Update AGENTS.md project status if appropriate.

Model constraints:
- Prefer the existing `UserTitleState`, `HouseholdList`, and
  `HouseholdListItem` models.
- Do not add a duplicate personal watchlist model.
- Do not add a duplicate household list model.
- Validate personal rating if the existing model does not already constrain it:
  use a simple MVP range such as 1-10.
- If adding validation or constraints requires a migration, keep it small and
  explain why it is needed.
- Do not store external API data in list models.
- Do not add denormalized title metadata to list models; use the existing
  `Title` relationships.

Permission constraints:
- Unauthenticated users should be redirected to login.
- Users can view and mutate only their own `UserTitleState` records.
- Users can view and mutate household lists only for households where they are
  members.
- Non-members should receive 404 or another project-consistent denial response;
  do not leak household or list existence.
- Household list actions should validate that the target list belongs to the
  household in the URL.

UI constraints:
- Keep the MVP simple and template-based.
- Reuse the current base template and Tailwind style.
- Avoid introducing a new design system.
- Prefer POST forms for state-changing actions.
- Include CSRF tokens on all POST forms.
- Show helpful empty states:
  - no personal titles yet
  - no titles for the selected status
  - no household lists yet
  - no titles in a household list yet
- Keep controls compact and clear:
  - status select
  - rating input/select
  - notes textarea
  - watched date/time input
  - add/update/remove buttons

Service behavior:
- Personal state service should:
  - create a `UserTitleState` when a title is first added
  - update an existing state for the same user/title instead of duplicating it
  - allow partial updates without clearing existing notes/rating unless the
    user intentionally submits blank values
  - set `watched_at` when status becomes watched if the user supplies a value
  - clear or leave `watched_at` consistently when status changes away from
    watched; choose one behavior and cover it with tests
- Household list service should:
  - create lists only for households where the user is a member
  - prevent duplicate household list names per household
  - add existing local titles to household lists
  - avoid duplicate list items for the same title
  - remove list items only when the user is a household member

Testing requirements:
Add or improve tests for:
- personal state creation for a title
- personal state update without creating duplicates
- personal state rating validation
- personal state removal
- personal list page access for authenticated users
- unauthenticated users redirected to login
- personal list shows only the current user's records
- personal list status filtering
- title detail page exposes a personal list action or state context
- household list creation by a household member
- duplicate household list name behavior
- household list overview shows only memberships for the current user
- household list detail access for members
- household list detail denied for non-members
- adding a title to a household list
- duplicate household list item behavior
- removing a title from a household list
- household list actions reject non-members

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

Phase 4 should stay limited to personal watch states and household shared lists.
Streaming availability, recommendations, invitations, public reviews,
notifications, and background sync should start in later phases.
