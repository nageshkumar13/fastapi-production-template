# FastAPI Production Template

A small, clean FastAPI starter template built for production-style backend projects.

## V2 Database, Auth, Alembic, And Tests

This branch includes PostgreSQL, SQLAlchemy, Alembic migrations, JWT-based authentication, protected routes, a service layer, and a foundational pytest suite.

## Settings Structure

Application configuration now uses a centralized `Settings` class in `app/config.py` powered by `pydantic-settings`.

What this gives us:

- typed settings with centralized defaults
- `.env` loading for local development
- one cached `get_settings()` entry point
- cleaner config usage across the app

This matters because database, JWT, logging, and app metadata now all read from the same source instead of relying on scattered environment handling.

## Environment Configuration

Copy `.env.example` to `.env` and update values as needed.

Current settings:

```env
APP_NAME=FastAPI Production Template
APP_VERSION=1.0.0
APP_ENV=development
DEBUG=true
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/fastapi_template_db
JWT_SECRET_KEY=replace-this-with-a-long-random-secret-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Required application settings:

- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `JWT_ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`

Useful app metadata and runtime settings:

- `APP_NAME`
- `APP_VERSION`
- `APP_ENV`
- `DEBUG`

## Development vs Production

Typical development configuration:

- `APP_ENV=development`
- `DEBUG=true`
- more verbose logging
- local `.env` driven setup

Typical production configuration:

- `APP_ENV=production`
- `DEBUG=false`
- cleaner `INFO`-level logging
- real production secrets and database URL

## PostgreSQL And Alembic

Alembic is the source of truth for schema changes.

Do not use `Base.metadata.create_all()` anymore for this app.

Useful commands:

```bash
dropdb fastapi_template_db
createdb fastapi_template_db
alembic upgrade head
alembic current
alembic history
alembic revision --autogenerate -m "message"
```

### Local Database Reset And Alembic Workflow

Option A: Clean reset for local development

```bash
dropdb fastapi_template_db
createdb fastapi_template_db
alembic upgrade head
uvicorn app.main:app --reload
```

Option B: Stamp existing local database

Use this only when the existing schema already matches the current migration history.

```bash
alembic stamp head
```

This marks the database as migration-managed without creating tables again.

### Future Migration Workflow

When a model changes:

1. Edit the SQLAlchemy model.
2. Generate a migration.
3. Review the migration file.
4. Run `alembic upgrade head`.
5. Test the app.

## Run The App

Apply migrations first:

```bash
alembic upgrade head
```

Then start the server:

```bash
uvicorn app.main:app --reload
```

## Run Tests

Run the test suite with:

```bash
pytest
```

Current automated coverage includes:

- `GET /health`
- `GET /health/db`
- signup success and duplicate signup handling
- login success and invalid credential handling
- protected `GET /users/me` with valid, missing, and invalid tokens

The current test setup uses a reusable `TestClient`, dependency overrides, and an isolated SQLite test database for fast local runs.

## Notes

- Routes stay thin while reusable database operations live in the service layer.
- Database schema is migration-managed through Alembic.
- Configuration is centralized through the settings layer.
- Application behavior is unchanged in this chunk.
