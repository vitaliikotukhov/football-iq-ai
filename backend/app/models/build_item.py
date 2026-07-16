from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin

class BuildItem(TimestampMixin, Base):
    __tablename__ = "build_items"
    __table_args__ = (UniqueConstraint("build_run_id", "competition_id", name="uq_build_item_run_competition"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    build_run_id: Mapped[int] = mapped_column(ForeignKey("build_runs.id", ondelete="CASCADE"), index=True)
    competition_id: Mapped[int] = mapped_column(Integer)
    competition_name: Mapped[str] = mapped_column(String(150))
    country_name: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(30), default="pending", index=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    result_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
