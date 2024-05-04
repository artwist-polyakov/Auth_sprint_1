"""add-user-id-notification

Revision ID: d738942e570d
Revises: 3516c3b6d8d4
Create Date: 2024-05-05 00:30:10.551770

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'd738942e570d'
down_revision: Union[str, None] = '3516c3b6d8d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'notifications',
        sa.Column('user_id', sa.String(), nullable=False), schema='notifications'
    )
    op.create_index(
        'ix_notifications_user_id',
        'notifications',
        ['user_id'],
        unique=False,
        schema='notifications'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_notifications_user_id', table_name='notifications', schema='notifications')
    op.drop_column('notifications', 'user_id', schema='notifications')
    # ### end Alembic commands ###
