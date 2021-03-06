"""empty message

Revision ID: f289850cd0b2
Revises: 8a21f2f29721
Create Date: 2017-04-18 23:33:47.553493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f289850cd0b2'
down_revision = '8a21f2f29721'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('sqlite_sequence')
    op.add_column('matchLog', sa.Column('timestamp', sa.String(), nullable=True))
    # op.create_unique_constraint(None, 'users', ['email'])
    # op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('matchLog', 'timestamp')
    op.create_table('sqlite_sequence',
    sa.Column('name', sa.NullType(), nullable=True),
    sa.Column('seq', sa.NullType(), nullable=True)
    )
    # ### end Alembic commands ###
