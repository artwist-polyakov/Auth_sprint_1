"""empty message

Revision ID: 648e9e37c3c9
Revises: 9d4fc6612143
Create Date: 2024-02-25 15:33:39.153422

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from migrations.roles.default_roles import default_roles

# revision identifiers, used by Alembic.
revision: str = '648e9e37c3c9'
down_revision: Union[str, None] = '9d4fc6612143'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    for role in default_roles:
        op.execute(
            sa.text(
                "INSERT INTO users.roles (uuid, role, resource, verb) "
                "VALUES (CAST(:uuid AS UUID), :role, :resource, :verb) "
                "ON CONFLICT (uuid) DO NOTHING"
            ).bindparams(
                sa.bindparam('uuid', value=str(role['uuid'])),
                sa.bindparam('role', value=role['role']),
                sa.bindparam('resource', value=role['resource']),
                sa.bindparam('verb', value=role['verb'])
            )
        )


def downgrade() -> None:
    for role in default_roles:
        op.execute(
            sa.text(
                "DELETE FROM users.roles WHERE uuid = CAST(:uuid AS UUID)"
            ).bindparams(
                sa.bindparam('uuid', value=str(role['uuid']))
            )
        )
