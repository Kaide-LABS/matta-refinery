"""add vertical_ensemble_outputs to lead_prospects

Revision ID: 0004
Revises: 0003
Create Date: 2026-05-21 00:00:00.000000

Phase 1.7 Stage C — surfaces the N=3 vertical classification ensemble
outputs when they don't reach majority consensus, so compose_dossier
can render an explicit "vertical classification deferred" block in §1
instead of silently substituting a default vertical baseline.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'lead_prospects',
        sa.Column(
            'vertical_ensemble_outputs',
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column('lead_prospects', 'vertical_ensemble_outputs')
