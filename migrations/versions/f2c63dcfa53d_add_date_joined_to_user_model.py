from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'f2c63dcfa53d'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_joined', sa.DateTime(), nullable=False, server_default=sa.func.now()))

    # Update existing rows to have a default value
    op.execute('UPDATE "user" SET date_joined = CURRENT_TIMESTAMP WHERE date_joined IS NULL')

    # Remove the server default
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('date_joined', server_default=None)

def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('date_joined')