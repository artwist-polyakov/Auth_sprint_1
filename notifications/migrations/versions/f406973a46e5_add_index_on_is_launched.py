"""Add index on is_launched

Revision ID: f406973a46e5
Revises: 05933464dddb
Create Date: 2024-05-01 21:09:39.657841

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f406973a46e5'
down_revision: Union[str, None] = '05933464dddb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        'idx_is_launched',
        'tasks',
        ['is_launched'],
        unique=False,
        schema='notifications'
    )


def downgrade() -> None:
    op.drop_index('idx_is_launched', table_name='tasks', schema='notifications')
