"""create_index_devices

Revision ID: 8cb9a47d9dae
Revises: c685b9ba99cd
Create Date: 2024-03-02 12:14:49.141166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cb9a47d9dae'
down_revision: Union[str, None] = 'c685b9ba99cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        index_name='ix_users_sign_ins_user_device_type',
        table_name='users_sign_ins',
        columns=['user_device_type'],
        unique=False,
        schema='users'
    )


def downgrade() -> None:
    op.drop_index(
        index_name='ix_users_sign_ins_user_device_type',
        table_name='users.users_sign_ins'
    )
