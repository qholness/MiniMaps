"""empty message

Revision ID: dafc39798839
Revises: f289850cd0b2
Create Date: 2017-04-19 00:58:08.630153

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dafc39798839'
down_revision = 'f289850cd0b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('sqlite_sequence')
    op.add_column('matchLog', sa.Column('winner', sa.String(), nullable=True))
    pass
    # op.create_unique_constraint(None, 'users', ['username'])
    # op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('matchLog', 'winner')
    op.create_table('sqlite_sequence',
    sa.Column('name', sa.NullType(), nullable=True),
    sa.Column('seq', sa.NullType(), nullable=True)
    )
    # ### end Alembic commands ###
