"""create_device_tables

Revision ID: d35170a7fae2
Revises: f7fcdf76104d
Create Date: 2024-03-01 16:40:43.662494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd35170a7fae2'
down_revision: Union[str, None] = 'f7fcdf76104d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DEVICES = ['mac_app', 'android_app', 'web', 'smart']


def upgrade() -> None:
    for device in DEVICES:
        op.execute(
            sa.text(
                f"CREATE TABLE IF NOT EXISTS users.users_sign_in_{device} "
                f"PARTITION OF users_sign_in FOR VALUES IN ('{device}')"
            )
        )


def downgrade() -> None:
    for device in DEVICES:
        op.drop_table('user_sign_ins_{device}', schema='users')
