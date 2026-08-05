"""add is_enabled column to worker_registry

Revision ID: 004
Revises: 003
Create Date: 2026-08-04
"""
from alembic import op
import sqlalchemy as sa

revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "worker_registry",
        sa.Column("is_enabled", sa.Boolean(), nullable=False, server_default="true"),
    )


def downgrade() -> None:
    op.drop_column("worker_registry", "is_enabled")
