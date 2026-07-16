from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin
class Team(TimestampMixin, Base):
    __tablename__="teams"
    id: Mapped[int]=mapped_column(primary_key=True)
    api_id: Mapped[int|None]=mapped_column(unique=True, nullable=True)
    name: Mapped[str]=mapped_column(String(150), index=True)
    short_name: Mapped[str|None]=mapped_column(String(50), nullable=True)
    founded_year: Mapped[int|None]=mapped_column(nullable=True)
    country_id: Mapped[int|None]=mapped_column(ForeignKey("countries.id"), nullable=True)
    stadium_id: Mapped[int|None]=mapped_column(ForeignKey("stadiums.id"), nullable=True)
    current_manager_id: Mapped[int|None]=mapped_column(ForeignKey("managers.id"), nullable=True)
