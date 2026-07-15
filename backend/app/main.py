from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI

from app.api.routes import router
from app.core.config import get_settings
from app.core.logging import configure_logging

configure_logging()
logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info(
        "Starting %s version %s in %s mode",
        settings.app_name,
        settings.app_version,
        settings.app_env,
    )
    yield
    logger.info("Stopping %s", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Explainable football intelligence powered by Project Athena."
    ),
    lifespan=lifespan,
)

app.include_router(router)
