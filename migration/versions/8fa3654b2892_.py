"""empty message

Revision ID: 8fa3654b2892
Revises: 926a2257be1e
Create Date: 2023-09-24 18:25:10.684562

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fa3654b2892'
down_revision: Union[str, None] = '926a2257be1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('UserItem',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user', sa.UUID(), nullable=True),
    sa.Column('item', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['item'], ['Items.id'], ),
    sa.ForeignKeyConstraint(['user'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('UserItem')
    # ### end Alembic commands ###
