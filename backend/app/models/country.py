from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin
class Country(TimestampMixin, Base):
    __tablename__="countries"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(100), unique=True, index=True)
    code: Mapped[str|None]=mapped_column(String(10), unique=True, nullable=True)
