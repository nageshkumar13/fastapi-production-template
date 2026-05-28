from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import AppException

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "fastapi-production-template",
    }


@router.get("/health/db")
def database_health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1")).scalar()
    except SQLAlchemyError as exc:
        raise AppException("Database connection failed", status_code=503) from exc

    return {
        "status": "ok",
        "database": "postgresql",
    }
