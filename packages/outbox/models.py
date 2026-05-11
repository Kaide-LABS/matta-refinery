from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Outbox(Base):
    __tablename__ = "outbox"

    id = Column(String, primary_key=True)
    surface = Column(String, nullable=False)
    payload_jsonb = Column(JSON, nullable=False)
    delivery_attempts = Column(Integer, default=0, nullable=False)
    last_attempt_at = Column(DateTime, nullable=True)
    next_attempt_at = Column(DateTime, nullable=False)
    state = Column(String, nullable=False)
    last_error = Column(String, nullable=True)

class OutboxDLQ(Base):
    __tablename__ = "outbox_dlq"

    id = Column(String, primary_key=True)
    original_outbox_id = Column(String, nullable=False)
    surface = Column(String, nullable=False)
    payload_jsonb = Column(JSON, nullable=False)
    delivery_attempts = Column(Integer, nullable=False)
    final_error = Column(String, nullable=False)
    failed_at = Column(DateTime, nullable=False)
