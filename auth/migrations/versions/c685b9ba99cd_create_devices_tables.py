"""create_devices_tables

Revision ID: c685b9ba99cd
Revises: f7fcdf76104d
Create Date: 2024-03-01 17:33:22.001407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from configs.devices import devices

# revision identifiers, used by Alembic.
revision: str = 'c685b9ba99cd'
down_revision: Union[str, None] = 'f7fcdf76104d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    for device in devices:
        op.execute(
            f"CREATE TABLE users.refresh_tokens_{device} "
            f"PARTITION OF users.refresh_tokens FOR VALUES IN ('{device}')"
        )


def downgrade() -> None:
    for device in devices:
        op.execute(f"DROP TABLE users.refresh_tokens_{device}")
