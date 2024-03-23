"""Added User model

Revision ID: 4914f00ae14a
Revises: 
Create Date: 2024-03-22 12:23:37.993976

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4914f00ae14a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'users',
        sa.Column(
            'telegram_id', sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column('username', sa.String(length=32), nullable=False),
        sa.Column('age', sa.SmallInteger(), nullable=False),
        sa.Column('bio', sa.String(length=100), nullable=True),
        sa.Column('sex', sa.String(length=6), nullable=True),
        sa.Column('country', sa.Text(), nullable=False),
        sa.Column('city', sa.Text(), nullable=False),
        sa.Column(
            'date_joined',
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint('telegram_id'),
        sa.UniqueConstraint('username'),
    )
    op.create_index(
        op.f('ix_users_telegram_id'), 'users', ['telegram_id'], unique=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_telegram_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###