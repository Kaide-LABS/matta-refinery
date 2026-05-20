from sqlalchemy import Column, String, Integer, DateTime, Date, Float, Boolean, JSON
from datetime import datetime

from .base import Base

class IngestBatch(Base):
    __tablename__ = "ingest_batches"

    id = Column(String, primary_key=True)
    source_surface = Column(String, nullable=False) # Added
    file_sha256 = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    day = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class LeadProspect(Base):
    __tablename__ = "lead_prospects"

    id = Column(String, primary_key=True)
    batch_id = Column(String, nullable=True) # Added to link to batch
    external_lead_id = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    contact_name = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    sector_hint = Column(String, nullable=True)
    source_system = Column(String, nullable=False)
    vertical = Column(String, nullable=True)
    factory_size_band = Column(String, nullable=True)
    trade_show_provenance = Column(Boolean, default=False)
    fitness_score = Column(Float, nullable=True)
    enrichment_status = Column(String, default="complete")
    signal_hash = Column(String, nullable=True)
    last_scored_at = Column(DateTime, nullable=True)
    requires_human_review = Column(Boolean, default=False)
    raw_notes = Column(String, nullable=True)
    defect_hypothesis = Column(JSON, nullable=True) # Added for Stage 2
