from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.dependencies import get_db
from app.integrations.api_football import (
    ApiFootballClient,
    ApiFootballConfigurationError,
    ApiFootballResponseError,
)
from app.schemas.sync import LeagueSyncReport, ProviderStatus, SyncReport
from app.services.api_football_sync import sync_countries, sync_league

router = APIRouter(prefix="/sync", tags=["data synchronization"])
settings = get_settings()


def _service_unavailable(exc: Exception) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=str(exc),
    )


@router.get("/provider-status", response_model=ProviderStatus)
async def provider_status() -> ProviderStatus:
    if not settings.api_football_is_configured:
        return ProviderStatus(
            configured=False,
            account={},
            subscription={},
            requests={},
        )

    try:
        payload = await ApiFootballClient().get("status")
    except (ApiFootballConfigurationError, ApiFootballResponseError) as exc:
        raise _service_unavailable(exc) from exc

    rows = payload.get("response", [])
    row = rows[0] if rows else {}

    return ProviderStatus(
        configured=True,
        account=row.get("account") or {},
        subscription=row.get("subscription") or {},
        requests=row.get("requests") or {},
    )


@router.post("/countries", response_model=SyncReport)
async def synchronize_countries(
    db: Session = Depends(get_db),
) -> SyncReport:
    try:
        return await sync_countries(db)
    except (ApiFootballConfigurationError, ApiFootballResponseError) as exc:
        raise _service_unavailable(exc) from exc


@router.post("/league/{league_id}", response_model=LeagueSyncReport)
async def synchronize_league(
    league_id: int,
    season: int = Query(ge=2000, le=2100),
    db: Session = Depends(get_db),
) -> LeagueSyncReport:
    try:
        return await sync_league(
            db,
            league_id=league_id,
            season_year=season,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except (ApiFootballConfigurationError, ApiFootballResponseError) as exc:
        raise _service_unavailable(exc) from exc
