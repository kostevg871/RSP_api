"""create access_token table

Revision ID: 301666df4f19
Revises: 87824eb8ca25
Create Date: 2024-09-04 21:24:29.515131

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '301666df4f19'
down_revision: Union[str, None] = '87824eb8ca25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accesstoken',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='cascade'),
    sa.UniqueConstraint('token')
    )
    op.drop_table('access_token')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('access_token',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='access_token_user_id_fkey', ondelete='CASCADE')
    )
    op.drop_table('accesstoken')
    # ### end Alembic commands ###
