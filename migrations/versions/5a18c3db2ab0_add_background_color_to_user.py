"""Add background_color to User

Revision ID: 5a18c3db2ab0
Revises: ce3c6c017cb4
Create Date: 2025-01-15 16:20:22.843997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a18c3db2ab0'
down_revision = 'ce3c6c017cb4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('background_color', sa.String(length=7), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('background_color')

    # ### end Alembic commands ###
