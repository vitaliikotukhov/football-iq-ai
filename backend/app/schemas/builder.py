from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class KnowledgeBuildRequest(BaseModel):
    season: int = Field(ge=2000, le=2100)
    competition_ids: list[int] | None = None
    include_countries: bool = True
    stop_on_error: bool | None = None

class BuildPlanItem(BaseModel):
    competition_id: int
    competition_name: str
    country_name: str
    season: int
    estimated_provider_calls: int = 2

class BuildPlan(BaseModel):
    season: int
    dry_run: bool
    include_countries: bool
    estimated_provider_calls: int
    competitions: list[BuildPlanItem]

class BuildRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    season: int
    include_countries: bool
    dry_run: bool
    stop_on_error: bool
    requested_competitions: str
    total_items: int
    successful_items: int
    failed_items: int
    started_at: datetime | None
    finished_at: datetime | None
    created_at: datetime
