"""fix4 migration

Revision ID: 6c125a0d7f03
Revises: 9f6e5fb522b2
Create Date: 2025-03-31 12:30:41.236983

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c125a0d7f03'
down_revision: Union[str, None] = '9f6e5fb522b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
