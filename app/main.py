from fastapi import FastAPI

import app.models  # noqa: F401
from app.config import settings
from app.database import Base, engine
from app.exceptions import AppException, app_exception_handler
from app.logger_config import setup_logger
from app.routes.auth import router as auth_router
from app.routes.health import router as health_router

logger = setup_logger()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A clean, minimal FastAPI starter template for production-ready backend projects.",
    debug=settings.DEBUG,
)

app.add_exception_handler(AppException, app_exception_handler)
app.include_router(auth_router)
app.include_router(health_router)


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ensured")
    logger.info("Application started")
