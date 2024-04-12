"""create unicity constraint on User name column

Revision ID: 63a8101fc2d8
Revises: c5ce2fa5e3b6
Create Date: 2024-01-18 14:27:49.077942

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '63a8101fc2d8'
down_revision: Union[str, None] = 'c5ce2fa5e3b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###
