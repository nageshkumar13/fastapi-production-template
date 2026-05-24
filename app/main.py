from fastapi import FastAPI

from app.config import settings
from app.exceptions import AppException, app_exception_handler
from app.logger_config import setup_logger
from app.routes.health import router as health_router

logger = setup_logger()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A clean, minimal FastAPI starter template for production-ready backend projects.",
    debug=settings.DEBUG,
)

app.add_exception_handler(AppException, app_exception_handler)
app.include_router(health_router)


@app.on_event("startup")
def startup_event():
    logger.info("Application started")
