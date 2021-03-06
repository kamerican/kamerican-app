"""empty message

Revision ID: 21b4754b767d
Revises: a4805e8d0a23
Create Date: 2018-11-24 14:23:48.769184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21b4754b767d'
down_revision = 'a4805e8d0a23'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('face')
    op.create_table('face',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('embedding', sa.PickleType(), nullable=True),
    sa.Column('_filepath', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('face')
    op.create_table('face',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('embedding', sa.PickleType(), nullable=True),
    sa.Column('_filepath', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
