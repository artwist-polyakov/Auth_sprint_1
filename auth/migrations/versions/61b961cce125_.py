from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '61b961cce125'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA users")


def downgrade() -> None:
    op.execute("DROP SCHEMA users")
