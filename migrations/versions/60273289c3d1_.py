"""empty message

Revision ID: 60273289c3d1
Revises: 6a105a919baf
Create Date: 2018-11-16 18:26:13.563300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60273289c3d1'
down_revision = '6a105a919baf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), nullable=True),
    sa.Column('date_created', sa.DATETIME(), nullable=True),
    sa.Column('is_admin', sa.BOOLEAN(), nullable=True),
    sa.Column('perm_twtimgdl', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=1)
    # ### end Alembic commands ###
