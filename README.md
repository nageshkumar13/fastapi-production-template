# FastAPI Production Template

A small, clean FastAPI starter template built for production-style backend projects.

## V2 Database, Signup, Login, And Current User Auth

This branch introduces the PostgreSQL foundation for version 2 and the first authentication-related flows: user signup, login with JWT access token generation, and a protected current-user endpoint.

What is included in this chunk:

- SQLAlchemy database setup
- PostgreSQL connection via `DATABASE_URL`
- A basic `users` table/model
- Startup table creation with `Base.metadata.create_all(...)`
- API health checks for both app and database
- Password hashing with `passlib[bcrypt]`
- `POST /auth/signup` for creating users
- `POST /auth/login` for verifying email and password
- JWT access token generation on successful login
- `GET /users/me` protected by Bearer token authentication

What is intentionally not included yet:

- Refresh tokens
- Roles
- Permissions
- Email verification
- Password reset
- Complex auth middleware

Refresh tokens and broader auth flows will be added later.

## Project Structure

```text
fastapi-production-template/
|-- app/
|   |-- config.py
|   |-- database.py
|   |-- dependencies/
|   |   `-- auth.py
|   |-- exceptions.py
|   |-- logger_config.py
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
|   |-- token.py
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

## Login Route

Verify user credentials and receive an access token:

```http
POST /auth/login
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
  "message": "Login credentials verified successfully",
  "access_token": "jwt-token-here",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "is_active": true,
    "created_at": "2026-05-28T12:00:00Z"
  }
}
```

Token payload:

- `sub` contains the user email
- `user_id` contains the user id
- `exp` contains the token expiry time

## Current User Route

Call `POST /auth/login` first and copy the `access_token` from the response.

Then call:

```http
GET /users/me
Authorization: Bearer <access_token>
```

Successful response:

```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2026-05-28T12:00:00Z"
}
```

Invalid authentication behavior:

- Missing token returns HTTP `401`
- Invalid token returns HTTP `401`
- Expired token returns HTTP `401`
- Inactive user returns HTTP `403`

The password hash is never returned in any API response.

## Notes

- Login returns a JWT access token with token type `bearer`.
- `GET /users/me` is the first protected route in the project.
- Routes stay thin while reusable database operations now live in the service layer.
- This keeps auth and user data access easier to maintain as the app grows.
- Refresh tokens are intentionally not implemented yet.
