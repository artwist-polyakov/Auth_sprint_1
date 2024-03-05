"""create_tables

Revision ID: f7fcdf76104d
Revises: 367bdda798cc
Create Date: 2024-03-01 16:24:21.908848

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f7fcdf76104d'
down_revision: Union[str, None] = '367bdda798cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
                    sa.Column('uuid', sa.UUID(), nullable=False),
                    sa.Column('role', sa.String(length=255), nullable=False),
                    sa.Column('resource', sa.String(length=255), nullable=False),
                    sa.Column('verb', sa.String(length=255), nullable=False),
                    sa.PrimaryKeyConstraint('uuid'),
                    sa.UniqueConstraint('uuid'),
                    schema='users'
                    )
    op.create_table('users',
                    sa.Column('uuid', sa.UUID(), nullable=False),
                    sa.Column('email', sa.String(length=255), nullable=False),
                    sa.Column('password', sa.String(length=255), nullable=False),
                    sa.Column('first_name', sa.String(length=50), nullable=True),
                    sa.Column('last_name', sa.String(length=50), nullable=True),
                    sa.Column('is_superuser', sa.Boolean(), nullable=False),
                    sa.Column('role', sa.String(length=255), nullable=False),
                    sa.Column('is_verified', sa.Boolean(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('uuid'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('uuid'),
                    schema='users'
                    )
    op.create_table('refresh_tokens',
                    sa.Column('uuid', sa.UUID(), nullable=False),
                    sa.Column('user_id', sa.UUID(), nullable=False),
                    sa.Column('active_till', sa.BigInteger(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('user_device_type', sa.Text(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.users.uuid'], ),
                    sa.PrimaryKeyConstraint('uuid', 'user_device_type'),
                    sa.UniqueConstraint('uuid', 'user_device_type'),
                    schema='users',
                    postgresql_partition_by='list(user_device_type)'
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('refresh_tokens', schema='users')
    op.drop_table('users', schema='users')
    op.drop_table('roles', schema='users')
    # ### end Alembic commands ###