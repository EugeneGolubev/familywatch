# Household Categories Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace local title ID household-list adding with household categories, default category creation, owner-managed categories, and catalog-based add flows.

**Architecture:** Reuse `HouseholdList` and `HouseholdListItem` as the persistence layer while changing user-facing language to household categories. Put business rules in `HouseholdListService` and keep TMDb sync through `CatalogService`.

**Tech Stack:** Django, Django templates, pytest, Docker Compose.

---

## File Structure

- Modify `households/services.py`: create default household categories after household creation.
- Modify `lists/services.py`: add default category constants, owner permission helpers, category management, selectable category data, and TMDb-result add support.
- Modify `lists/forms.py`: replace title ID form with category and catalog add forms.
- Modify `catalog/views.py`: expose household category choices on title detail.
- Modify `catalog/urls.py`: add title-detail household category POST route.
- Modify `lists/views.py`: update category management and add-by-search views.
- Modify `lists/urls.py`: add category delete and catalog add routes.
- Modify `templates/catalog/title_detail.html`: add household category form.
- Modify `templates/lists/household_overview.html`: use category language and owner-only management.
- Modify `templates/lists/household_detail.html`: remove title ID form and link to search add page.
- Create `templates/lists/household_add_title.html`: search and add TMDb results to one category.
- Modify `templates/households/detail.html`: use category language.
- Modify `tests/test_phase4_lists.py`: service and view tests for the new behavior.

## Task 1: Defaults And Owner Category Management

- [ ] Write failing tests in `tests/test_phase4_lists.py`:
  - `test_household_creation_creates_default_categories`
  - `test_owner_can_create_custom_category`
  - `test_member_cannot_create_custom_category`
  - `test_owner_can_remove_category`
  - `test_member_cannot_remove_category`
- [ ] Run focused tests with `.venv\Scripts\python.exe -m pytest tests/test_phase4_lists.py -q`; expected failures are missing defaults and permission methods.
- [ ] Implement defaults and owner-only create/remove in `households/services.py` and `lists/services.py`.
- [ ] Run the same focused tests; expected pass.

## Task 2: Add Existing Local Title From Title Detail

- [ ] Write failing tests in `tests/test_phase4_lists.py`:
  - `test_title_detail_exposes_household_category_choices`
  - `test_title_detail_post_adds_title_to_household_category`
  - `test_title_detail_post_does_not_create_personal_state`
- [ ] Run focused tests; expected failures are missing form/view/URL/context.
- [ ] Implement household-category selection form, title-detail context, and POST view.
- [ ] Run focused tests; expected pass.

## Task 3: Add TMDb Result From Category Search

- [ ] Write failing tests in `tests/test_phase4_lists.py`:
  - `test_household_category_add_title_search_returns_catalog_results`
  - `test_add_tmdb_result_to_household_category_syncs_and_adds_title`
- [ ] Run focused tests; expected failures are missing add-title page and POST action.
- [ ] Implement category add-title search view, TMDb add form, URL routes, and template.
- [ ] Run focused tests; expected pass.

## Task 4: Templates And Copy

- [ ] Update templates to say "category" and "categories" instead of "list" and "lists" in household-list UI.
- [ ] Remove the numeric local title ID form from the category detail template.
- [ ] Show owner-only create/remove controls in the category overview.
- [ ] Run `rg "Local title ID|Title ID|Household Lists|Shared lists" templates lists catalog households` and confirm no stale visible copy remains.

## Task 5: Verification

- [ ] Run `.venv\Scripts\python.exe -m pytest tests/test_phase4_lists.py -q`.
- [ ] Run `.venv\Scripts\python.exe -m pytest -q`.
- [ ] Run `.venv\Scripts\python.exe -m compileall accounts catalog config discovery households integrations lists recommendations streaming tests`.
- [ ] Run `docker compose run --rm web python manage.py check`.
- [ ] Run `docker compose run --rm web pytest`.
- [ ] Review `git diff` for unrelated changes.
- [ ] Commit with `git add` and `git commit -m "feat: add household categories"`.
