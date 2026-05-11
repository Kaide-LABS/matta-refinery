"""initial

Revision ID: 0001
Revises: 
Create Date: 2026-05-11 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('ingest_batches',
        sa.Column('id', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lead_prospects',
        sa.Column('id', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('prioritized_queues',
        sa.Column('id', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dossier_artifacts',
        sa.Column('id', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dossier_stubs',
        sa.Column('id', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('outbox',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('state', sa.String(), nullable=False),
        sa.Column('delivery_attempts', sa.Integer(), nullable=False),
        sa.Column('payload_jsonb', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('outbox_dlq',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('final_error', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event_idempotency',
        sa.Column('id', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('event_idempotency')
    op.drop_table('outbox_dlq')
    op.drop_table('outbox')
    op.drop_table('dossier_stubs')
    op.drop_table('dossier_artifacts')
    op.drop_table('prioritized_queues')
    op.drop_table('lead_prospects')
    op.drop_table('ingest_batches')
