"""create_devices_tables

Revision ID: c685b9ba99cd
Revises: f7fcdf76104d
Create Date: 2024-03-01 17:33:22.001407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c685b9ba99cd'
down_revision: Union[str, None] = 'f7fcdf76104d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DEVICES = ['ios_app', 'android_app', 'web', 'smart_tv']


def upgrade() -> None:
    for device in DEVICES:
        op.execute(
            f"CREATE TABLE users.users_sign_ins_{device} "
            f"PARTITION OF users.users_sign_ins FOR VALUES IN ('{device}')"
        )


def downgrade() -> None:
    for device in DEVICES:
        op.execute(f"DROP TABLE users.users_sign_ins_{device}")
