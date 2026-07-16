"""add stadium provider id

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-15
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "stadiums",
        sa.Column("api_id", sa.Integer(), nullable=True),
    )
    op.create_unique_constraint(
        "uq_stadiums_api_id",
        "stadiums",
        ["api_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_stadiums_api_id",
        "stadiums",
        type_="unique",
    )
    op.drop_column("stadiums", "api_id")
