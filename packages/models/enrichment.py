"""enrichment_artifacts table — one row per (prospect, source) pair.

UNIQUE(prospect_id, source) enables idempotent upserts via ON CONFLICT
DO UPDATE. ON DELETE CASCADE cleans up when a prospect is removed.
"""
import uuid

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Index, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func

from .base import Base


class EnrichmentArtifact(Base):
    __tablename__ = "enrichment_artifacts"

    # server_default = gen_random_uuid() so raw-SQL inserts that omit the id
    # column (e.g. the upsert path in enrich_prospect._upsert_artifact) get
    # a server-generated UUID. Python-side default=uuid.uuid4 is kept as a
    # safety net for ORM inserts. Requires pgcrypto extension (enabled in
    # init_db.py / alembic 0002).
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        default=uuid.uuid4,
    )
    prospect_id = Column(
        String(64),
        ForeignKey("lead_prospects.id", ondelete="CASCADE"),
        nullable=False,
    )
    # source: 'companies_house' | 'web_scrape' | 'tavily_news'
    source = Column(String(32), nullable=False)
    # status: 'fetched' | 'fallback_empty' | 'not_applicable' | 'failed'
    status = Column(String(32), nullable=False)
    payload = Column(JSONB)
    fallback_reason = Column(Text)
    fetched_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("prospect_id", "source", name="uq_enrichment_prospect_source"),
        Index("idx_enrichment_artifacts_prospect_id", "prospect_id"),
        Index("idx_enrichment_artifacts_source_status", "source", "status"),
    )
