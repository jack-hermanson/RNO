"""initial

Revision ID: 22da29189e08
Revises: 
Create Date: 2024-09-15 22:33:24.688371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22da29189e08'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=24), nullable=False),
    sa.Column('first_name', sa.String(length=16), nullable=False),
    sa.Column('last_name', sa.String(length=24), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('clearance', sa.Integer(), nullable=False),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('account_id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('account')
    # ### end Alembic commands ###
