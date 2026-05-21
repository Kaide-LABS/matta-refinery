"""add website_url to lead_prospects

Revision ID: 0003
Revises: 0002
Create Date: 2026-05-21 00:00:00.000000

Adds optional website_url column to lead_prospects. Real-company seeded
rows (Stage C-prelim) carry the verified canonical URL so the Playwright
WebScraperAdapter can scrape the actual site instead of guessing
https://<snake-case-name>.co.uk.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'lead_prospects',
        sa.Column('website_url', sa.String(length=2048), nullable=True),
    )


def downgrade() -> None:
    op.drop_column('lead_prospects', 'website_url')
