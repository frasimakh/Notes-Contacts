"""add meta index

Revision ID: 20240314_02
Revises: 20240314_01
Create Date: 2024-03-14 12:10:00.000000
"""

from alembic import op


revision = "20240314_02"
down_revision = "20240314_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE INDEX note_meta_idx ON notes ((meta->>'source'))")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS note_meta_idx")
