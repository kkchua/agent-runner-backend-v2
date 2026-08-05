"""add job_dir field to workflow_runs

Revision ID: 002
Revises: 001
Create Date: 2026-08-04
"""
from alembic import op
import sqlalchemy as sa

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "workflow_runs",
        sa.Column("job_dir", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("workflow_runs", "job_dir")
