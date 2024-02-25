"""empty message

Revision ID: 61b961cce125
Revises: 
Create Date: 2024-02-25 13:54:00.773674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61b961cce125'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA users")


def downgrade() -> None:
    op.execute("DROP SCHEMA users")
