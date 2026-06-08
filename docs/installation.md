# Installation Guide

This guide explains how to install and run FamilyWatch locally with Docker
Compose.

## Requirements

- Docker Desktop on Windows, or Docker Engine with Docker Compose on Linux
- A TMDb API key for catalog search and title details

The app can start without a TMDb API key, but catalog search will show a
configuration message until `TMDB_API_KEY` is set.

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

