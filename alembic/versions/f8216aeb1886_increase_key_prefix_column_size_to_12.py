"""increase key_prefix column size to 12

Revision ID: f8216aeb1886
Revises: 85a4f77176f3
Create Date: 2026-08-04 23:05:53.538988
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'f8216aeb1886'
down_revision: Union[str, None] = '85a4f77176f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'api_keys',
        'key_prefix',
        existing_type=sa.String(length=8),
        type_=sa.String(length=12),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        'api_keys',
        'key_prefix',
        existing_type=sa.String(length=12),
        type_=sa.String(length=8),
        existing_nullable=False,
    )
