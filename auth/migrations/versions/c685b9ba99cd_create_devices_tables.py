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
    op.execute(
        "CREATE TABLE users.users_sign_ins_ios_app "
        "PARTITION OF users.users_sign_ins FOR VALUES IN ('ios_app')"
    )
    op.execute(
        "CREATE TABLE users.users_sign_ins_android_app "
        "PARTITION OF users.users_sign_ins FOR VALUES IN ('android_app')"
    )
    op.execute(
        "CREATE TABLE users.users_sign_ins_web "
        "PARTITION OF users.users_sign_ins FOR VALUES IN ('web')"
    )
    op.execute(
        "CREATE TABLE users.users_sign_ins_smart_tv "
        "PARTITION OF users.users_sign_ins FOR VALUES IN ('smart_tv')"
    )


def downgrade() -> None:
    op.execute("DROP TABLE users.users_sign_ins_ios_app")
    op.execute("DROP TABLE users.users_sign_ins_android_app")
    op.execute("DROP TABLE users.users_sign_ins_web")
    op.execute("DROP TABLE users.users_sign_ins_smart_tv")
