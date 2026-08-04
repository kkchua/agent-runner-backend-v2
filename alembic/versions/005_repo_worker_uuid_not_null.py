"""make repos.worker_uuid NOT NULL — it is the authoritative FK to worker_registry.id

Revision ID: 005
Revises: 004
Create Date: 2026-08-04
"""
import sqlalchemy as sa
from alembic import op

revision = "005"
down_revision = "004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Backfill any rows that still have NULL worker_uuid (shouldn't exist after
    # migration 003, but be safe)
    op.execute(
        "UPDATE repos SET worker_uuid = w.id FROM worker_registry w "
        "WHERE repos.worker_id = w.worker_id AND repos.worker_uuid IS NULL"
    )
    # Delete orphan repos whose worker no longer exists (cannot satisfy NOT NULL)
    op.execute(
        "DELETE FROM repos WHERE worker_uuid IS NULL"
    )
    op.alter_column(
        "repos", "worker_uuid",
        existing_type=sa.String(36),
        nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "repos", "worker_uuid",
        existing_type=sa.String(36),
        nullable=True,
    )
