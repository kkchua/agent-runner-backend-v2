"""merge 006 and 008_user_workers

Revision ID: af3d0ca4af92
Revises: 006, 008_user_workers
Create Date: 2026-08-13 10:44:03.787008
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'af3d0ca4af92'
down_revision: Union[str, None] = ('006', '008_user_workers')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
