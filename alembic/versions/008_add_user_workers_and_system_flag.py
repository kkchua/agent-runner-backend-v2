"""add user_workers table and is_system flag to user_roles

Revision ID: 008_user_workers
Revises: 007_user_roles
Create Date: 2026-08-07 12:00:00.000000
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "008_user_workers"
down_revision: Union[str, None] = "007_user_roles"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "user_roles",
        sa.Column("is_system", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.create_table(
        "user_workers",
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("worker_id", sa.String(length=80), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user_roles.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "worker_id"),
    )


def downgrade() -> None:
    op.drop_table("user_workers")
    op.drop_column("user_roles", "is_system")
