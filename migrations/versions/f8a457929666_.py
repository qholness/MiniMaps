"""empty message

Revision ID: f8a457929666
Revises: 5c4bf894ba90
Create Date: 2017-04-15 18:20:33.810811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8a457929666'
down_revision = '5c4bf894ba90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('sqlite_sequence')
    # op.create_unique_constraint(None, 'client_status', ['text_color'])
    # op.create_unique_constraint(None, 'client_status', ['color'])
    # op.create_unique_constraint(None, 'users', ['username'])
    op.add_column('clients', sa.Column('import_notes', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('clients', 'import_notes')
    op.drop_constraint(None, 'client_status', type_='unique')
    op.drop_constraint(None, 'client_status', type_='unique')
    op.create_table('sqlite_sequence',
    sa.Column('name', sa.NullType(), nullable=True),
    sa.Column('seq', sa.NullType(), nullable=True)
    )
    # ### end Alembic commands ###