"""Add word entering limit fields to User model

Revision ID: 48a57012c95e
Revises: 73985a9bd4fb
Create Date: 2024-12-04 11:30:02.592410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48a57012c95e'
down_revision = '73985a9bd4fb'
branch_labels = None
depends_on = None

def upgrade():
    # Add columns with default values
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('words_entered_today', sa.Integer(), nullable=True, server_default='0'))
        batch_op.add_column(sa.Column('last_word_entry_date', sa.Date(), nullable=True))

    # Remove the server default after the columns have been added
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('words_entered_today', server_default=None)

def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('last_word_entry_date')
        batch_op.drop_column('words_entered_today')