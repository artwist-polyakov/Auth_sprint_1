"""load default roles

Revision ID: e52593e48832
Revises: 8cb9a47d9dae
Create Date: 2024-03-02 18:59:47.937903

"""
from typing import Sequence, Union

from alembic import op
from migrations.roles.default_roles import default_roles

# revision identifiers, used by Alembic.
revision: str = 'e52593e48832'
down_revision: Union[str, None] = '8cb9a47d9dae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    for role in default_roles:
        op.execute(f"INSERT INTO users.roles(uuid, role, resource, verb) "
                   f"VALUES ('{role['uuid']}', '{role['role']}', "
                   f"'{role['resource']}', '{role['verb']}')")


def downgrade() -> None:
    for role in default_roles:
        op.execute(f"DELETE FROM users.roles WHERE uuid = {role['uuid']}")
