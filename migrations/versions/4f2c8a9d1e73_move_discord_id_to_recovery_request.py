"""Move Discord IDs from user accounts to recovery requests.

Revision ID: 4f2c8a9d1e73
Revises: 6ccfb183a8e2
Create Date: 2026-11-17 19:11:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = '4f2c8a9d1e73'
down_revision = '6ccfb183a8e2'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('recovery_request', schema=None) as batch_op:
        batch_op.add_column(sa.Column('discord_id', sa.String(length=19), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('discord_id')


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('discord_id', sa.String(length=255), nullable=True))

    with op.batch_alter_table('recovery_request', schema=None) as batch_op:
        batch_op.drop_column('discord_id')
