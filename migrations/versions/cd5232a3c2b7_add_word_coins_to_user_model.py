"""Add word_coins to User model

Revision ID: cd5232a3c2b7
Revises: f2c63dcfa53d
Create Date: 2024-11-30 16:48:02.638614

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'cd5232a3c2b7'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('word_coins', sa.Integer(), nullable=False, server_default='0'))

    # Remove the server default after the column has been added
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('word_coins', server_default=None)

def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('word_coins')