"""many_to_many

Revision ID: d2f631922446
Revises: 44c8595968dc
Create Date: 2025-04-01 21:13:07.964372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2f631922446'
down_revision = '44c8595968dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role_account',
sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['account_id'], ['account.account_id'], ),
        sa.ForeignKeyConstraint(['role_id'], ['role.role_id'], ),
        sa.PrimaryKeyConstraint('role_id', 'account_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('role_account')
    # ### end Alembic commands ###
