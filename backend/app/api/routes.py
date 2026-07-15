from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.db.session import database_is_ready

router = APIRouter()
settings = get_settings()


@router.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {
        "application": settings.app_name,
        "message": "Project Athena is running.",
        "principle": "Every prediction must explain why.",
    }


@router.get("/version", tags=["system"])
def version() -> dict[str, str]:
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }


@router.get("/health", tags=["system"])
def health() -> JSONResponse:
    database_status = "connected" if database_is_ready() else "unavailable"
    is_healthy = database_status == "connected"

    payload = {
        "status": "healthy" if is_healthy else "degraded",
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "database": database_status,
    }

    return JSONResponse(
        status_code=200 if is_healthy else 503,
        content=payload,
    )
