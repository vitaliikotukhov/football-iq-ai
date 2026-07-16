from datetime import date
from sqlalchemy import Boolean, Date, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin
class Season(TimestampMixin, Base):
    __tablename__="seasons"
    __table_args__=(UniqueConstraint("competition_id","name",name="uq_season_competition_name"),)
    id: Mapped[int]=mapped_column(primary_key=True)
    competition_id: Mapped[int]=mapped_column(ForeignKey("competitions.id"))
    name: Mapped[str]=mapped_column(String(30))
    start_date: Mapped[date|None]=mapped_column(Date, nullable=True)
    end_date: Mapped[date|None]=mapped_column(Date, nullable=True)
    is_current: Mapped[bool]=mapped_column(Boolean, default=False)
