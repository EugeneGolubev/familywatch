# End User Guide

This guide covers the main FamilyWatch workflows for regular users.

## Access the App

Open the app in a browser:

```text
http://localhost:8000
```

## Register and Log In

1. Open the registration page:

   ```text
   http://localhost:8000/accounts/register/
   ```

2. Create an account.

3. Log in:

   ```text
   http://localhost:8000/login/
   ```

The app creates a user profile automatically when your account is created.

## Create a Household

1. Open:

   ```text
   http://localhost:8000/households/create/
   ```

2. Enter a household name.

3. Choose the default country.

4. Submit the form.

You become the household owner automatically.

## View Your Households

Open:

```text
http://localhost:8000/households/
```

This page shows households you belong to. Open a household to view its details
and shared lists.

## Search for Movies and TV Shows

Open:

```text
http://localhost:8000/catalog/search/
```

Enter a movie or TV show name and submit the search. Catalog search requires
`TMDB_API_KEY` to be configured in `.env`.

## Open Title Details

Click a search result to open its title detail page. The app creates or updates
a local title record from TMDb when you open a result.

The title detail page can show:

- Poster
- Title
- Movie or TV type
- Release year
- Overview
- Runtime or source status when available
- TMDb ID

## Manage Your Personal Watch State

On a title detail page, use the **Update personal state** form.

Available statuses:

- Planned
- Watching
- Watched
- Dropped
- Favorite
- Not Interested

Optional fields:

- Rating from 1 to 10
- Watched date and time
- Notes

Save the form to add or update the title in your personal list.

## View Your Personal List

Open:

```text
http://localhost:8000/lists/mine/
```

You can:

- See titles you added to your personal list
- Filter by status
- Open title details
- Remove titles from your personal list

## Use Household Lists

Open a household from:

```text
http://localhost:8000/households/
```

From the household page, you can create and open shared household lists.

Typical list names might be:

- Weekend
- Family
- Watch Together
- Kids

Household lists are visible only to household members.

## Add Titles to Household Lists

1. Search for a title.

2. Open its detail page.

3. Use the household list action for an existing household list.

4. The title is added to that shared list.

Duplicate title additions reuse the existing list item instead of creating a
duplicate.

## Current Limitations

- Streaming availability is deferred until an API-backed provider is selected.
- There is no "where to watch" section yet.
- Household invitations are not implemented yet.
- Recommendations are not implemented yet.

