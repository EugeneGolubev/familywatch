# Household Categories And Catalog Add Flow Design

## Context

FamilyWatch currently lets household members add titles to shared household lists by entering a local title database ID. That is not usable for normal users because the ID is an internal implementation detail and only works for titles already synced into the local catalog.

Phase 3 already provides TMDb-backed catalog search and title detail syncing. Phase 4 added personal watch states and household lists. This design keeps the work inside the Phase 4 household-list area and reuses the existing catalog integration rather than introducing a new discovery system.

## Goals

- Replace the numeric "Title ID" household add flow with title search and selection.
- Treat household lists as household categories in the user interface.
- Create a small default set of household categories for every new household.
- Allow only the household owner to manage categories.
- Allow household members to add titles to existing categories.
- Keep personal watch state separate from household categories.

## Default Categories

Every new household should receive these categories:

- Plan to watch together
- Watching together
- Watched
- Watch with Kids

These are household-level categories. Adding a title to "Plan to watch together" must not create or update the current user's personal "Planned" state.

## Product Behavior

### Category Management

The UI should use the term "Household categories" instead of "Household lists" for user-facing screens.

Household owners can:

- Create a category.
- Remove a category.
- View all categories.

Household members can:

- View categories.
- Open a category.
- Add titles to a category.
- Remove titles from a category.

Members cannot create or remove categories. Category management is expected to be infrequent, so the owner-only flow can stay simple. The current household model has `owner` and `member` roles; in this phase, "admin" means the existing household owner.

### Add From Title Detail

The title detail page should include an "Add to household category" section when the signed-in user belongs to at least one household with at least one category.

The user chooses:

- Household.
- Category within that household.

Submitting the form adds the current title to the selected category. If the item already exists in the category, the app should show an informational message instead of creating a duplicate.

### Add From Household Category

The household category detail page should no longer ask for a local title ID.

Instead, the page should provide a clear path to add a title by name. For the first implementation, use a dedicated add-title page for the category:

1. User opens a household category.
2. User chooses "Add title".
3. User searches by movie or TV show name.
4. App shows TMDb catalog matches with title, type, year, poster when available, and overview.
5. User chooses "Add" on a result.
6. App syncs the selected TMDb title into the local catalog if needed and adds it to the current category.

This avoids HTMX complexity for the MVP and keeps the behavior easy to test.

## Architecture

### Models

Reuse the existing `HouseholdList` and `HouseholdListItem` models. Do not add a new `HouseholdCategory` model in this pass.

Rationale: the current model already represents a named household collection with unique titles. Renaming the model would create migration and refactor churn without changing behavior. The user-facing language can change now; a model rename can be considered later if the domain stabilizes around "category".

### Services

Keep business rules in services rather than views.

Add or update services for:

- Creating default categories when a household is created.
- Checking whether a user can manage categories for a household.
- Creating categories for household owners.
- Removing categories for household owners.
- Listing categories available to a user for title-detail forms.
- Adding an existing local title to a selected household category.
- Searching TMDb from a category add page.
- Syncing and adding a TMDb result to a category.

Existing `HouseholdListService.add_title` should continue to enforce household membership before adding items.

### Forms

Replace the integer title ID form with forms that represent user choices:

- Category create form: category name.
- Title-detail household add form: household/category selection.
- Category search form: query text.
- Category search result add form: hidden media type and TMDb ID.

The title-detail add form should not expose categories for households the user does not belong to.

### Views And URLs

Add or update list views for:

- Category overview with owner-only category management controls.
- Category detail with a link or button to add by search.
- Category add-title search page.
- Category add selected TMDb result action.
- Title-detail add-to-household-category action.

Existing routes can remain structurally similar, but templates should show "categories" in visible copy.

## Error Handling

- If TMDb search is unavailable or the API key is missing, show the existing friendly catalog error style.
- If a user tries to manage categories without owner rights, reject the action with a 404.
- If a category is removed, its items are removed by existing cascade behavior.
- If a duplicate title is added to a category, show an informational message.
- If the selected household/category is not available to the user, reject the form and show a validation error.

## Testing

Add focused tests for:

- New households receive the four default categories.
- Owner can create a custom category.
- Member cannot create a category.
- Owner can remove a category.
- Member cannot remove a category.
- Member can add an existing local title to a category.
- Adding a title to a household category does not create personal `UserTitleState`.
- Title detail exposes household category choices for the signed-in user's households.
- Category search page returns TMDb results.
- Adding a TMDb search result syncs the title and adds it to the selected category.
- Duplicate category item additions reuse the existing item.

## Out Of Scope

- Streaming availability data entry or provider selection.
- React or a new frontend framework.
- Bulk category templates per household type.
- Per-category privacy or permissions.
- Automatic mapping between household categories and personal watch states.
- Renaming database models from `HouseholdList` to `HouseholdCategory`.
