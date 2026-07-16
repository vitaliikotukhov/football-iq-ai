from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.db.dependencies import get_db
from app.domain.competition_catalog import catalog_as_dicts
from app.models.build_run import BuildRun
from app.schemas.builder import BuildPlan, BuildRunRead, KnowledgeBuildRequest
from app.services.knowledge_builder import create_plan, create_run, execute_build

router = APIRouter(prefix="/builder", tags=["football knowledge builder"])
settings = get_settings()

@router.get("/catalog")
def catalog():
    return {"default_season": settings.knowledge_builder_default_season, "api_football_configured": settings.api_football_is_configured, "competitions": catalog_as_dicts()}

@router.post("/plan", response_model=BuildPlan)
def plan(request: KnowledgeBuildRequest):
    return create_plan(request, True)[0]

@router.post("/build", response_model=BuildRunRead)
async def build(request: KnowledgeBuildRequest, dry_run: bool = Query(default=True), db: Session = Depends(get_db)):
    plan, competitions = create_plan(request, dry_run)
    if not competitions:
        raise HTTPException(status_code=422, detail="No supported competitions were selected.")
    if not dry_run and not settings.api_football_is_configured:
        raise HTTPException(status_code=503, detail="API-Football is not configured. Add API_FOOTBALL_KEY to .env or use dry_run=true.")
    run = create_run(db, request, competitions, plan.dry_run)
    return await execute_build(db, run)

@router.get("/runs", response_model=list[BuildRunRead])
def runs(limit: int = Query(default=20, ge=1, le=100), db: Session = Depends(get_db)):
    return list(db.scalars(select(BuildRun).order_by(BuildRun.id.desc()).limit(limit)).all())
