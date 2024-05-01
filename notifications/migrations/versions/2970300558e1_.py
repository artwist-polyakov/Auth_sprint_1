"""empty message

Revision ID: 2970300558e1
Revises: 52d5265d601e
Create Date: 2024-05-01 10:25:19.356970

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '2970300558e1'
down_revision: Union[str, None] = '52d5265d601e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавление поля created_at в таблицу tasks
    op.add_column('tasks', sa.Column(
        'created_at',
        sa.DateTime(),
        nullable=False,
        server_default=sa.func.now()
    ), schema='notifications')
    # Добавление поля created_at в таблицу notifications
    op.add_column('notifications', sa.Column(
        'created_at',
        sa.DateTime(),
        nullable=False,
        server_default=sa.func.now()
    ), schema='notifications')


def downgrade() -> None:
    # Удаление поля created_at из таблицы tasks
    op.drop_column('tasks', 'created_at', schema='notifications')
    # Удаление поля created_at из таблицы notifications
    op.drop_column('notifications', 'created_at', schema='notifications')
