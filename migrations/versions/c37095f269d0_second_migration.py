"""Second migration

Revision ID: c37095f269d0
Revises: e43d7e02a1a8
Create Date: 2025-03-29 23:12:13.818002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c37095f269d0'
down_revision: Union[str, None] = 'e43d7e02a1a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('short_urls',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('original_url', sa.Text(), nullable=False),
    sa.Column('short_code', sa.String(), nullable=False),
    sa.Column('custom_alias', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('expires_at', sa.DateTime(), nullable=True),
    sa.Column('clicks', sa.Integer(), nullable=True),
    sa.Column('last_clicked', sa.DateTime(), nullable=True),
    sa.Column('owner_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('custom_alias', name='uq_custom_alias'),
    sa.UniqueConstraint('short_code', name='uq_short_code')
    )
    op.create_index(op.f('ix_short_urls_custom_alias'), 'short_urls', ['custom_alias'], unique=False)
    op.create_index(op.f('ix_short_urls_short_code'), 'short_urls', ['short_code'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_short_urls_short_code'), table_name='short_urls')
    op.drop_index(op.f('ix_short_urls_custom_alias'), table_name='short_urls')
    op.drop_table('short_urls')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
