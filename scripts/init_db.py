import sys
import os
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from sqlalchemy import create_engine, text
from packages.models.prospects import Base as ProspectsBase
# Import EnrichmentArtifact so it registers on ProspectsBase.metadata
# (both share packages/models/base.py). Without this import the
# enrichment_artifacts table would never be created by create_all().
from packages.models.enrichment import EnrichmentArtifact  # noqa: F401
from packages.outbox.models import Base as OutboxBase
# Try to import settings, fallback to manual if fails
try:
    from apps.refinery_api.config import settings
    url = settings.postgres_url.replace('+asyncpg', '')
except Exception:
    url = os.environ.get("POSTGRES_URL", "postgresql+psycopg://postgres:password@localhost:5432/refinery").replace('+asyncpg', '')

def init_db():
    engine = create_engine(url)
    print(f"Connecting to {url}...")

    # pgcrypto provides gen_random_uuid() — used by enrichment_artifacts.id
    # server_default. Must be enabled before create_all so the column DDL's
    # default function resolves.
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto"))

    # Create tables
    ProspectsBase.metadata.drop_all(engine)
    ProspectsBase.metadata.create_all(engine)
    OutboxBase.metadata.create_all(engine)
    
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS prioritized_queues (id TEXT PRIMARY KEY, batch_id TEXT, payload_json JSONB)"))
        # Dropping and recreating to ensure correct columns
        conn.execute(text("DROP TABLE IF EXISTS dossier_artifacts"))
        conn.execute(text("""
            CREATE TABLE dossier_artifacts (
                id TEXT PRIMARY KEY,
                dossier_id TEXT,
                prospect_id TEXT,
                batch_id TEXT,
                signal_hash TEXT,
                knowledge_graph_version TEXT,
                calibration_version TEXT,
                state TEXT,
                process_taxonomy JSONB,
                defect_hypothesis JSONB,
                comparable_deployment JSONB,
                risk_register JSONB,
                suggested_approach JSONB,
                unverified_sections JSONB,
                deterministic_section_ratio FLOAT,
                validation_error TEXT,
                generated_at TIMESTAMP
            )
        """))
        conn.execute(text("DROP TABLE IF EXISTS dossier_stubs"))
        conn.execute(text("CREATE TABLE dossier_stubs (stub_id TEXT PRIMARY KEY, prospect_id TEXT, batch_id TEXT, company_facts JSONB, verified_vertical TEXT, headline_kg_anchor TEXT, slot_readiness TEXT, generated_at TIMESTAMP)"))
        conn.execute(text("CREATE TABLE IF NOT EXISTS event_idempotency (id TEXT PRIMARY KEY, event_id TEXT, processed_at TIMESTAMP)"))
        
    # Idempotent demo-enrichment seed — populates enrichment_artifacts for
    # any tracer prospects that already exist. On first boot, lead_prospects
    # is empty so this seeds nothing; on subsequent runs after CSV ingest
    # for a tracer batch, this populates the deterministic demo enrichment.
    try:
        from scripts.seed_demo_enrichment import seed_demo_enrichment
        seed_demo_enrichment()
    except Exception as e:
        print(f"  (demo enrichment seed skipped: {e})")

    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
