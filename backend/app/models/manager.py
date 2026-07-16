from datetime import date
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin
class Manager(TimestampMixin, Base):
    __tablename__="managers"
    id: Mapped[int]=mapped_column(primary_key=True)
    api_id: Mapped[int|None]=mapped_column(unique=True, nullable=True)
    name: Mapped[str]=mapped_column(String(150), index=True)
    nationality: Mapped[str|None]=mapped_column(String(100), nullable=True)
    date_of_birth: Mapped[date|None]=mapped_column(Date, nullable=True)
