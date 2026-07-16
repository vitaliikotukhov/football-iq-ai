from pydantic import BaseModel, Field


class SyncReport(BaseModel):
    resource: str
    received: int = 0
    created: int = 0
    updated: int = 0
    skipped: int = 0
    details: dict[str, int | str] = Field(default_factory=dict)


class LeagueSyncReport(BaseModel):
    league_id: int
    season: int
    competition_created: bool
    season_created: bool
    country_created: bool
    teams_received: int
    teams_created: int
    teams_updated: int
    stadiums_created: int
    stadiums_updated: int


class ProviderStatus(BaseModel):
    configured: bool
    provider: str = "API-Football"
    account: dict = Field(default_factory=dict)
    subscription: dict = Field(default_factory=dict)
    requests: dict = Field(default_factory=dict)
