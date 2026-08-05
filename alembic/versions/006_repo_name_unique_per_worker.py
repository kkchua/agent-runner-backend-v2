"""repo name unique per worker — replace global unique on name with (name, worker_uuid)

Revision ID: 006
Revises: f8216aeb1886
Create Date: 2026-08-05
"""
from alembic import op

revision = "006"
down_revision = "f8216aeb1886"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop any existing unique constraint/index on name alone.
    # The constraint name may vary, so try common names with IF EXISTS.
    op.execute("ALTER TABLE repos DROP CONSTRAINT IF EXISTS repos_name_key")
    op.execute("DROP INDEX IF EXISTS ix_repos_name")
    # Add composite unique constraint: name per worker
    op.create_unique_constraint("uq_repo_name_worker", "repos", ["name", "worker_uuid"])


def downgrade() -> None:
    op.drop_constraint("uq_repo_name_worker", "repos", type_="unique")
