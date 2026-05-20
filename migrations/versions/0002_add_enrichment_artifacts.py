"""add enrichment_artifacts table

Revision ID: 0002
Revises: 0001
Create Date: 2026-05-20 00:00:00.000000

Adds one row per (prospect_id, source) pair for external enrichment
data (Companies House, Playwright web scrape, Tavily news). UNIQUE
constraint on (prospect_id, source) enables idempotent upserts;
ON DELETE CASCADE cleans up when a prospect is removed.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.create_table(
        'enrichment_artifacts',
        sa.Column(
            'id',
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.Column('prospect_id', sa.String(length=64), nullable=False),
        sa.Column('source', sa.String(length=32), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('fallback_reason', sa.Text(), nullable=True),
        sa.Column(
            'fetched_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ['prospect_id'],
            ['lead_prospects.id'],
            ondelete='CASCADE',
        ),
        sa.UniqueConstraint('prospect_id', 'source', name='uq_enrichment_prospect_source'),
    )
    op.create_index(
        'idx_enrichment_artifacts_prospect_id',
        'enrichment_artifacts',
        ['prospect_id'],
    )
    op.create_index(
        'idx_enrichment_artifacts_source_status',
        'enrichment_artifacts',
        ['source', 'status'],
    )


def downgrade() -> None:
    op.drop_index('idx_enrichment_artifacts_source_status', table_name='enrichment_artifacts')
    op.drop_index('idx_enrichment_artifacts_prospect_id', table_name='enrichment_artifacts')
    op.drop_table('enrichment_artifacts')
