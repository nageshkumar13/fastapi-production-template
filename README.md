# FastAPI Production Template

A small, clean FastAPI starter template built for production-style backend projects.

## What this project shows

- FastAPI app structure
- Centralized config management
- Environment variable usage
- Logging setup
- Health check endpoint
- Basic custom error handling
- Simple deployment-ready thinking

## Project Structure

```text
fastapi-production-template/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── logger_config.py
│   ├── exceptions.py
│   ├── routes/
│   │   └── health.py
│   └── utils/
├── logs/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv venv
```

Activate virtual environment:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python -m uvicorn app.main:app --reload
```

## Health Check

`GET /health`

Response:

```json
{
  "status": "ok",
  "service": "fastapi-production-template"
}
```

## Environment Variables

Copy `.env.example` to `.env` and update values if needed.

```env
APP_NAME=FastAPI Production Template
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=true
```

## V1 Scope

This version intentionally does not include authentication, database, Docker, Redis, Celery, frontend, or payment features.

The goal is to provide a clean FastAPI backend foundation.
