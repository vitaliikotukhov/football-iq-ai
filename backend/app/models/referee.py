from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin
class Referee(TimestampMixin, Base):
    __tablename__="referees"
    id: Mapped[int]=mapped_column(primary_key=True)
    api_id: Mapped[int|None]=mapped_column(unique=True, nullable=True)
    name: Mapped[str]=mapped_column(String(150), index=True)
    nationality: Mapped[str|None]=mapped_column(String(100), nullable=True)
