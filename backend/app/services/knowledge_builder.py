import asyncio, json, logging
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.domain.competition_catalog import resolve_competitions
from app.models.build_item import BuildItem
from app.models.build_run import BuildRun
from app.schemas.builder import BuildPlan, BuildPlanItem, KnowledgeBuildRequest
from app.services.api_football_sync import sync_countries, sync_league

logger = logging.getLogger(__name__)
settings = get_settings()
def now(): return datetime.now(timezone.utc)

def create_plan(request: KnowledgeBuildRequest, dry_run: bool):
    competitions = resolve_competitions(request.competition_ids)
    items = [BuildPlanItem(competition_id=x.id, competition_name=x.name, country_name=x.country, season=request.season) for x in competitions]
    estimate = len(items) * 2 + (1 if request.include_countries else 0)
    return BuildPlan(season=request.season, dry_run=dry_run, include_countries=request.include_countries, estimated_provider_calls=estimate, competitions=items), competitions

def create_run(db: Session, request: KnowledgeBuildRequest, competitions, dry_run: bool):
    stop = request.stop_on_error if request.stop_on_error is not None else settings.knowledge_builder_stop_on_error
    run = BuildRun(status="planned", season=request.season, include_countries=request.include_countries, dry_run=dry_run, stop_on_error=stop, requested_competitions=json.dumps([x.id for x in competitions]), total_items=len(competitions))
    db.add(run); db.flush()
    for x in competitions:
        db.add(BuildItem(build_run_id=run.id, competition_id=x.id, competition_name=x.name, country_name=x.country, status="pending"))
    db.commit(); db.refresh(run); return run

async def execute_build(db: Session, run: BuildRun):
    run.started_at = now()
    if run.dry_run:
        run.status = "completed"; run.finished_at = now(); db.commit(); db.refresh(run); return run
    run.status = "running"; db.commit()
    if run.include_countries:
        try: await sync_countries(db)
        except Exception as exc:
            logger.exception("Country sync failed")
            if run.stop_on_error:
                run.status="failed"; run.finished_at=now(); db.commit(); return run
    items = list(db.scalars(select(BuildItem).where(BuildItem.build_run_id==run.id).order_by(BuildItem.id)).all())
    for item in items:
        item.status="running"; item.started_at=now(); db.commit()
        try:
            report = await sync_league(db, league_id=item.competition_id, season_year=run.season)
            item.status="completed"; item.result_json=report.model_dump_json(); run.successful_items += 1
        except Exception as exc:
            logger.exception("Competition build failed")
            item.status="failed"; item.error_message=str(exc)[:4000]; run.failed_items += 1
            if run.stop_on_error:
                item.finished_at=now(); db.commit(); break
        item.finished_at=now(); db.commit()
        await asyncio.sleep(max(0, settings.knowledge_builder_delay_seconds))
    run.finished_at=now()
    run.status = "completed" if run.failed_items==0 else ("completed_with_errors" if run.successful_items else "failed")
    db.commit(); db.refresh(run); return run
