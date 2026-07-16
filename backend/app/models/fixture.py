from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin
class Fixture(TimestampMixin, Base):
    __tablename__="fixtures"
    id: Mapped[int]=mapped_column(primary_key=True)
    api_id: Mapped[int|None]=mapped_column(unique=True, nullable=True)
    season_id: Mapped[int]=mapped_column(ForeignKey("seasons.id"))
    home_team_id: Mapped[int]=mapped_column(ForeignKey("teams.id"))
    away_team_id: Mapped[int]=mapped_column(ForeignKey("teams.id"))
    referee_id: Mapped[int|None]=mapped_column(ForeignKey("referees.id"), nullable=True)
    stadium_id: Mapped[int|None]=mapped_column(ForeignKey("stadiums.id"), nullable=True)
    kickoff_at: Mapped[datetime]=mapped_column(DateTime(timezone=True))
    status: Mapped[str]=mapped_column(String(30), default="scheduled")
    home_score: Mapped[int|None]=mapped_column(nullable=True)
    away_score: Mapped[int|None]=mapped_column(nullable=True)
