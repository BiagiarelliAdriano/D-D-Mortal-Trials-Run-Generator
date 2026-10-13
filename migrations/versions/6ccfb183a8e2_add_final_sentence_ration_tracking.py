"""Track the Final Sentence ration grant per hosted Run.

Revision ID: 6ccfb183a8e2
Revises: aff97875ef39
Create Date: 2026-10-13 17:30:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = '6ccfb183a8e2'
down_revision = 'aff97875ef39'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'hosted_run',
        sa.Column(
            'final_sentence_ration_used',
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        )
    )


def downgrade():
    op.drop_column('hosted_run', 'final_sentence_ration_used')
