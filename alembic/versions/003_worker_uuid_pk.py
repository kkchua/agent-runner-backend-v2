"""refactor worker_registry PK to UUID, add worker_uuid FK to repos

Revision ID: 003
Revises: 002
Create Date: 2026-08-04
"""
from alembic import op
import sqlalchemy as sa

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Drop the old FK constraint on repos.worker_id
    op.drop_constraint("repos_worker_id_fkey", "repos", type_="foreignkey")

    # 2. Add UUID id column to worker_registry
    op.add_column(
        "worker_registry",
        sa.Column("id", sa.String(36), nullable=True),
    )
    # Backfill existing rows with UUIDs
    op.execute("UPDATE worker_registry SET id = gen_random_uuid()::text WHERE id IS NULL")
    # Set NOT NULL after backfill
    op.alter_column("worker_registry", "id", nullable=False)

    # 3. Drop old PK, add new PK on id
    op.drop_constraint("worker_registry_pkey", "worker_registry", type_="primary")
    op.create_primary_key("worker_registry_pkey", "worker_registry", ["id"])

    # 4. Add unique constraint on worker_id (was PK before, now just unique)
    op.create_unique_constraint("uq_worker_registry_worker_id", "worker_registry", ["worker_id"])

    # 5. Add worker_uuid FK column to repos
    op.add_column(
        "repos",
        sa.Column("worker_uuid", sa.String(36), nullable=True),
    )
    # Backfill worker_uuid from existing worker_id
    op.execute(
        "UPDATE repos SET worker_uuid = w.id FROM worker_registry w WHERE repos.worker_id = w.worker_id"
    )
    op.create_foreign_key(
        "fk_repos_worker_uuid", "repos", "worker_registry",
        ["worker_uuid"], ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_repos_worker_uuid", "repos", type_="foreignkey")
    op.drop_column("repos", "worker_uuid")
    op.drop_constraint("uq_worker_registry_worker_id", "worker_registry", type_="unique")

    # Restore old PK on worker_id
    op.drop_constraint("worker_registry_pkey", "worker_registry", type_="primary")
    op.create_primary_key("worker_registry_pkey", "worker_registry", ["worker_id"])
    op.drop_column("worker_registry", "id")

    # Restore old FK
    op.create_foreign_key(
        "repos_worker_id_fkey", "repos", "worker_registry",
        ["worker_id"], ["worker_id"],
    )
