from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin
class Competition(TimestampMixin, Base):
    __tablename__="competitions"
    id: Mapped[int]=mapped_column(primary_key=True)
    api_id: Mapped[int|None]=mapped_column(unique=True, nullable=True)
    name: Mapped[str]=mapped_column(String(150), index=True)
    competition_type: Mapped[str]=mapped_column(String(50))
    country_id: Mapped[int|None]=mapped_column(ForeignKey("countries.id"), nullable=True)
