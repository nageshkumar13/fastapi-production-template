from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.models  # noqa: F401
from app.config import get_settings
from app.exceptions import AppException, app_exception_handler
from app.logger_config import setup_logger
from app.routes.auth import router as auth_router
from app.routes.health import router as health_router
from app.routes.users import router as users_router

settings = get_settings()
logger = setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application started")
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "A clean, minimal FastAPI starter template for "
        "production-ready backend projects."
    ),
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_exception_handler(AppException, app_exception_handler)
app.include_router(auth_router)
app.include_router(health_router)
app.include_router(users_router)
