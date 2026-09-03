"""Add manual approval state for new users."""
from alembic import op
import sqlalchemy as sa

revision = '0003_user_approval'
down_revision = '0002_product_indexes'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('users', sa.Column('is_approved', sa.Boolean(), server_default=sa.false(), nullable=False))
    op.execute('UPDATE users SET is_approved = TRUE')
    op.alter_column('users', 'is_approved', server_default=None)

def downgrade():
    op.drop_column('users', 'is_approved')