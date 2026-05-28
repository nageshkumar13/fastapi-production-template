# FastAPI Production Template

A small, clean FastAPI starter template built for production-style backend projects.

## V2 Database, Auth, And Alembic Migrations

This branch adds production-style Alembic migrations on top of the existing PostgreSQL and authentication foundation.

What is included in this chunk:

- PostgreSQL integration with SQLAlchemy
- Signup and login with JWT access tokens
- Protected `GET /users/me`
- Service layer for reusable user/auth database operations
- Alembic migration setup
- Initial migration for the `users` table

What is intentionally not included yet:

- Refresh tokens
- Roles
- Permissions
- Email verification
- Password reset

## Why Alembic

Alembic is the migration tool used with SQLAlchemy to manage database schema changes over time.

Why migrations are needed:

- They make schema changes versioned and repeatable
- They keep local, staging, and production databases in sync
- They replace runtime table creation with explicit schema management

The app no longer creates tables at startup with `Base.metadata.create_all(...)`. Database schema is now managed through Alembic migrations instead.

## Project Structure

```text
fastapi-production-template/
|-- alembic/
|   |-- env.py
|   |-- script.py.mako
|   `-- versions/
|       `-- 20260528_1005_create_users_table.py
|-- alembic.ini
|-- app/
|   |-- config.py
|   |-- database.py
|   |-- dependencies/
|   |   `-- auth.py
|   |-- main.py
|   |-- models/
|   |   `-- user.py
|   |-- routes/
|   |   |-- auth.py
|   |   |-- health.py
|   |   `-- users.py
|   |-- schemas/
|   |   `-- auth.py
|   |-- security.py
|   |-- services/
|   |   `-- user_service.py
|   `-- token.py
|-- .env.example
|-- requirements.txt
`-- README.md
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Copy `.env.example` to `.env` and set your database and JWT configuration:

```env
APP_NAME=FastAPI Production Template
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/fastapi_template_db
JWT_SECRET_KEY=change-this-to-a-long-random-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Alembic Commands

Useful commands for local development:

```bash
dropdb fastapi_template_db
createdb fastapi_template_db
alembic upgrade head
alembic current
alembic history
alembic revision --autogenerate -m "message"
```

## Local Database Reset And Alembic Workflow

### Option A: Clean reset for local development

Use this when you want a fresh local database with the current migration history applied from scratch.

```bash
dropdb fastapi_template_db
createdb fastapi_template_db
alembic upgrade head
uvicorn app.main:app --reload
```

### Option B: Stamp existing local database

Use this only if your existing local database schema already matches the current migration state.

```bash
alembic stamp head
```

What this does:

- It marks the database as migration-managed
- It does not create tables again
- It does not apply missing schema changes

If your existing local database was created earlier with `create_all()` and the schema already matches the current migration, `alembic stamp head` is the practical way to start tracking it with Alembic.

## Warning

Do not use `Base.metadata.create_all()` anymore for this app.

Alembic is now the source of truth for schema changes.

## Future Workflow

When a model changes:

1. Edit the SQLAlchemy model.
2. Generate a migration.
3. Review the generated migration file carefully.
4. Run `alembic upgrade head`.
5. Test the app.

Example command:

```bash
alembic revision --autogenerate -m "add new field"
```

## Run The App

Apply migrations first:

```bash
alembic upgrade head
```

Then start the development server:

```bash
uvicorn app.main:app --reload
```

## Notes

- Routes stay thin while reusable database operations live in the service layer.
- Database schema is now migration-managed through Alembic.
- Application API behavior is unchanged in this chunk.
- No new auth features were added.
