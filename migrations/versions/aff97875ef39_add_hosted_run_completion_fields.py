"""Add hosted run completion fields

Revision ID: aff97875ef39
Revises: 08105591dfef
Create Date: 2026-09-02 17:17:41.825743

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'aff97875ef39'
down_revision = '08105591dfef'
branch_labels = None
depends_on = None

def upgrade():
    # Add completion tracking fields to HostedRun.
    #
    # Existing HostedRun records are assumed to be incomplete when this
    # migration is first applied, so is_completed defaults to False.

    op.add_column(
        'hosted_run',
        sa.Column(
            'is_completed',
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        )
    )

    op.add_column(
        'hosted_run',
        sa.Column(
            'completed_at',
            sa.DateTime(),
            nullable=True
        )
    )

def downgrade():
    op.drop_column('hosted_run', 'completed_at')
    op.drop_column('hosted_run', 'is_completed')