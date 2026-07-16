from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.api.builder import router as builder_router
from app.api.knowledge import router as knowledge_router
from app.api.sync import router as sync_router
from app.core.config import get_settings
from app.db.session import database_is_ready
router = APIRouter(); settings=get_settings()
router.include_router(knowledge_router); router.include_router(sync_router); router.include_router(builder_router)

@router.get("/", tags=["system"])
def root(): return {"application": settings.app_name, "message": "Project Athena is running.", "principle": "Every prediction must explain why."}

@router.get("/version", tags=["system"])
def version(): return {"application": settings.app_name, "version": settings.app_version, "environment": settings.app_env}

@router.get("/health", tags=["system"])
def health():
    db = "connected" if database_is_ready() else "unavailable"; ok=db=="connected"
    return JSONResponse(status_code=200 if ok else 503, content={"status":"healthy" if ok else "degraded","application":settings.app_name,"version":settings.app_version,"environment":settings.app_env,"database":db,"api_football_configured":settings.api_football_is_configured,"knowledge_builder_ready":ok})
