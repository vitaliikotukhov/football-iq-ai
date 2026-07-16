from datetime import date
from decimal import Decimal
from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin
class Transfer(TimestampMixin, Base):
    __tablename__="transfers"
    id: Mapped[int]=mapped_column(primary_key=True)
    player_name: Mapped[str]=mapped_column(String(150), index=True)
    from_team_id: Mapped[int|None]=mapped_column(ForeignKey("teams.id"), nullable=True)
    to_team_id: Mapped[int|None]=mapped_column(ForeignKey("teams.id"), nullable=True)
    transfer_date: Mapped[date]=mapped_column(Date)
    transfer_window: Mapped[str]=mapped_column(String(30))
    fee_amount: Mapped[Decimal|None]=mapped_column(Numeric(14,2), nullable=True)
    fee_currency: Mapped[str|None]=mapped_column(String(3), nullable=True)
    transfer_type: Mapped[str]=mapped_column(String(30))
