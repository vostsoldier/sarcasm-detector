"""Add is_private column to user

Revision ID: 253f2915da9f
Revises: 2b479fa7a052
Create Date: 2025-01-09 11:34:49.131714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '253f2915da9f'
down_revision = '2b479fa7a052'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_private', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('is_private')

    # ### end Alembic commands ###