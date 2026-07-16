"""add knowledge builder runs

Revision ID: 0003
Revises: 0002
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table("build_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("status", sa.String(40), nullable=False),
        sa.Column("season", sa.Integer(), nullable=False),
        sa.Column("include_countries", sa.Boolean(), nullable=False),
        sa.Column("dry_run", sa.Boolean(), nullable=False),
        sa.Column("stop_on_error", sa.Boolean(), nullable=False),
        sa.Column("requested_competitions", sa.Text(), nullable=False),
        sa.Column("total_items", sa.Integer(), nullable=False),
        sa.Column("successful_items", sa.Integer(), nullable=False),
        sa.Column("failed_items", sa.Integer(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_build_runs_status", "build_runs", ["status"])
    op.create_table("build_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("build_run_id", sa.Integer(), sa.ForeignKey("build_runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("competition_id", sa.Integer(), nullable=False),
        sa.Column("competition_name", sa.String(150), nullable=False),
        sa.Column("country_name", sa.String(100), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("result_json", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("build_run_id", "competition_id", name="uq_build_item_run_competition"))
    op.create_index("ix_build_items_build_run_id", "build_items", ["build_run_id"])
    op.create_index("ix_build_items_status", "build_items", ["status"])

def downgrade() -> None:
    op.drop_table("build_items")
    op.drop_table("build_runs")
