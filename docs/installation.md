# Installation Guide

This guide explains how to install and run FamilyWatch locally with Docker
Compose.

## Requirements

- Docker Desktop on Windows, or Docker Engine with Docker Compose on Linux
- A TMDb API key for catalog search and title details

The app can start without a TMDb API key, but catalog search will show a
configuration message until `TMDB_API_KEY` is set.

## Environment Values

### Django secret key

`DJANGO_SECRET_KEY` is used by Django to sign security-sensitive data such as
sessions and password reset tokens. For local development, any long random value
is enough.

For shared, staging, or production environments:

- Generate a unique secret key per environment.
- Keep it outside Git in `.env`, a deployment secret store, or your hosting
  platform's environment variable settings.
- Do not reuse the example value from `.env.example`.
- Do not share the same key between local development and production.
- If the key is exposed, replace it immediately and restart the app.

Changing `DJANGO_SECRET_KEY` later can invalidate existing sessions and signed
tokens, so plan rotations carefully. Users may need to log in again after a
rotation.

You can generate a local development key with Django:

```bash
docker compose run --rm web python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Paste the generated value into `.env`:

```env
DJANGO_SECRET_KEY=generated-secret-key
```

### TMDb API key

`TMDB_API_KEY` enables catalog search and title detail sync.

To get a TMDb API key:

1. Open [TMDb](https://www.themoviedb.org/) in a desktop browser.
2. Create an account or log in.
3. Open your account settings.
4. Select **API** from the settings sidebar.
5. Agree to the TMDb API terms.
6. Register an API application and copy the API key.
7. Add it to `.env`:

   ```env
   TMDB_API_KEY=your-tmdb-api-key
   ```

8. Restart Docker Compose so the app reads the updated environment:

   ```bash
   docker compose down
   docker compose up --build
   ```

TMDb's developer documentation says API key registration is available from the
API link in account settings and is best completed from a desktop browser:
[TMDb Getting Started](https://developer.themoviedb.org/v4/docs/getting-started).

## Windows

1. Start Docker Desktop.

2. Open PowerShell and go to the project folder:

   ```powershell
   cd D:\Foxminded\Familywatch
   ```

3. Create the local environment file:

   ```powershell
   Copy-Item .env.example .env
   ```

4. Open `.env` in an editor and configure these values:

   ```env
   DJANGO_SECRET_KEY=change-this-to-any-long-random-string
   DEBUG=1
   ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
   POSTGRES_DB=familywatch
   POSTGRES_USER=familywatch
   POSTGRES_PASSWORD=familywatch
   DATABASE_URL=postgres://familywatch:familywatch@db:5432/familywatch
   REDIS_URL=redis://redis:6379/0
   TMDB_API_KEY=your-tmdb-api-key
   DEFAULT_COUNTRY=PL
   ```

   Leave `TRAKT_CLIENT_ID`, `TRAKT_CLIENT_SECRET`, and `OMDB_API_KEY` empty for
   now. They are placeholders for future integrations.

5. Build and start the app:

   ```powershell
   docker compose up --build
   ```

6. Open the app:

   ```text
   http://localhost:8000
   ```

7. Apply migrations if this is the first run:

   ```powershell
   docker compose run --rm web python manage.py migrate
   ```

8. Create an admin user:

   ```powershell
   docker compose run --rm web python manage.py createsuperuser
   ```

## Linux

1. Make sure Docker is running.

2. Open a terminal and go to the project folder:

   ```bash
   cd /path/to/Familywatch
   ```

3. Create the local environment file:

   ```bash
   cp .env.example .env
   ```

4. Open `.env` in an editor and configure these values:

   ```env
   DJANGO_SECRET_KEY=change-this-to-any-long-random-string
   DEBUG=1
   ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
   POSTGRES_DB=familywatch
   POSTGRES_USER=familywatch
   POSTGRES_PASSWORD=familywatch
   DATABASE_URL=postgres://familywatch:familywatch@db:5432/familywatch
   REDIS_URL=redis://redis:6379/0
   TMDB_API_KEY=your-tmdb-api-key
   DEFAULT_COUNTRY=PL
   ```

   Leave `TRAKT_CLIENT_ID`, `TRAKT_CLIENT_SECRET`, and `OMDB_API_KEY` empty for
   now. They are placeholders for future integrations.

5. Build and start the app:

   ```bash
   docker compose up --build
   ```

6. Open the app:

   ```text
   http://localhost:8000
   ```

7. Apply migrations if this is the first run:

   ```bash
   docker compose run --rm web python manage.py migrate
   ```

8. Create an admin user:

   ```bash
   docker compose run --rm web python manage.py createsuperuser
   ```

## Useful Commands

Run a Django system check:

```bash
docker compose run --rm web python manage.py check
```

Check for missing migrations:

```bash
docker compose run --rm web python manage.py makemigrations --check --dry-run
```

Run tests:

```bash
docker compose run --rm web pytest
```

Stop containers:

```bash
docker compose down
```

Stop containers and remove the local database volume:

```bash
docker compose down -v
```
