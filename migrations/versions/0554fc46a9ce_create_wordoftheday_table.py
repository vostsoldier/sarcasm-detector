"""Create WordOfTheDay table

Revision ID: 0554fc46a9ce
Revises: 48a57012c95e
Create Date: 2024-12-04 11:30:02.592410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0554fc46a9ce'
down_revision = '48a57012c95e'
branch_labels = None
depends_on = None

def upgrade():
    # Create the WordOfTheDay table
    op.create_table(
        'word_of_the_day',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('word', sa.String(150), nullable=False),
        sa.Column('date', sa.Date, nullable=False, unique=True)
    )

def downgrade():
    # Drop the WordOfTheDay table
    op.drop_table('word_of_the_day')