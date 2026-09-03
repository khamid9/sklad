"""Initial database schema for My Sklad.

Revision ID: 0001_initial
Revises:
Create Date: 2026-09-02
"""
from alembic import op
from app.database.database import Base
from app.database import models  # noqa: F401

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    Base.metadata.create_all(bind=op.get_bind())

def downgrade():
    Base.metadata.drop_all(bind=op.get_bind())
