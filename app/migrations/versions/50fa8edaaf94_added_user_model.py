"""Added user model

Revision ID: 50fa8edaaf94
Revises: 
Create Date: 2024-03-21 18:31:15.864426

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50fa8edaaf94'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('telegram_id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('age', sa.SmallInteger(), nullable=False),
    sa.Column('bio', sa.String(length=100), nullable=True),
    sa.Column('sex', sa.String(length=6), nullable=True),
    sa.Column('country', sa.Text(), nullable=False),
    sa.Column('city', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('telegram_id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_telegram_id'), 'users', ['telegram_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_telegram_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
