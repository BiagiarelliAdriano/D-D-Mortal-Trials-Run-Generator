"""add rations to hosted run

Revision ID: b0f4c8d9a123
Revises: 0da48c2cad39
Create Date: 2026-06-03 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'b0f4c8d9a123'
down_revision = '0da48c2cad39'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('hosted_run', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rations', sa.Float(), nullable=False, server_default='3.0'))

    with op.batch_alter_table('hosted_run', schema=None) as batch_op:
        batch_op.alter_column('rations', server_default=None)


def downgrade():
    with op.batch_alter_table('hosted_run', schema=None) as batch_op:
        batch_op.drop_column('rations')
