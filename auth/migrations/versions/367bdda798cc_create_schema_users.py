"""create_schema_users

Revision ID: 367bdda798cc
Revises:
Create Date: 2024-02-29 19:45:47.895913

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '367bdda798cc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA users")


def downgrade() -> None:
    op.execute("DROP SCHEMA users")
