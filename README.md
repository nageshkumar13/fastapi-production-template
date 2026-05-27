# FastAPI Production Template

A small, clean FastAPI starter template built for production-style backend projects.

## V2 Database And Signup Foundation

This branch introduces the PostgreSQL foundation for version 2 and the first authentication-related feature: user signup.

What is included in this chunk:

- SQLAlchemy database setup
- PostgreSQL connection via `DATABASE_URL`
- A basic `users` table/model
- Startup table creation with `Base.metadata.create_all(...)`
- API health checks for both app and database
- Password hashing with `passlib[bcrypt]`
- `POST /auth/signup` for creating users

What is intentionally not included yet:

- Login
- JWT
- Refresh tokens
- Roles
- Email verification
- Password reset
- Auth middleware

Login and JWT-based authentication will be added later.

## Project Structure

```text
fastapi-production-template/
|-- app/
|   |-- config.py
|   |-- database.py
|   |-- exceptions.py
|   |-- logger_config.py
|   |-- main.py
|   |-- models/
|   |   |-- __init__.py
|   |   `-- user.py
|   |-- routes/
|   |   |-- auth.py
|   |   `-- health.py
|   |-- schemas/
|   |   `-- auth.py
|   |-- security.py
|   `-- utils/
|-- logs/
|-- .env.example
|-- requirements.txt
`-- README.md
```

## Setup

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## PostgreSQL Setup

Create a local PostgreSQL database named `fastapi_template_db`.

If you already have PostgreSQL installed, one simple option is:

```bash
createdb fastapi_template_db
```

Or from `psql`:

```sql
CREATE DATABASE fastapi_template_db;
```

## Environment Variables

Copy `.env.example` to `.env` and set your database connection:

```env
APP_NAME=FastAPI Production Template
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/fastapi_template_db
```

## Run The App

Start the development server:

```bash
uvicorn app.main:app --reload
```

On startup, the app will connect to PostgreSQL and create the `users` table if it does not already exist.

## Health Checks

Application health:

```http
GET /health
```

Database health:

```http
GET /health/db
```

## Signup Route

Create a new user:

```http
POST /auth/signup
```

Request body:

```json
{
  "email": "user@example.com",
  "password": "strongpass123"
}
```

Successful response:

```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2026-05-27T12:00:00Z"
}
```

Duplicate email behavior:

- If the email already exists, the API returns HTTP `409`.
- The password hash is stored in the database but is never returned in the response.

## Notes

- PostgreSQL is introduced in v2 as the backend foundation.
- Signup is the only user-auth related feature added in this chunk.
- Login and JWT are intentionally not implemented yet.
