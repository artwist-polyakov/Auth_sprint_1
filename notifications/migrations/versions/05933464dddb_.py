"""empty message

Revision ID: 05933464dddb
Revises: 2970300558e1
Create Date: 2024-05-01 20:40:06.498905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05933464dddb'
down_revision: Union[str, None] = '2970300558e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notifications', sa.Column(
        'is_error',
        sa.Boolean(),
        nullable=False,
        server_default=sa.text('false')
    ), schema='notifications')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notifications', 'is_error', schema='notifications')
    # ### end Alembic commands ###