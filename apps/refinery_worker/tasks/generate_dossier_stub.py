from ..app import app
from packages.knowledge_graph.select import select_comparable
from sqlalchemy import create_engine, text
from apps.refinery_api.config import settings
import uuid
from datetime import datetime

@app.task(
    name="refinery.generate_dossier_stub",
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=3,
)
def generate_dossier_stub(self, prospect_id: str):
    engine = create_engine(settings.postgres_url.replace('+asyncpg', ''))
    with engine.begin() as conn:
        row = conn.execute(text("SELECT vertical, fitness_score, enrichment_status, requires_human_review FROM lead_prospects WHERE id = :pid"), {"pid": prospect_id}).first()
        vertical = row[0]
        
        anchor_id, _, _ = select_comparable(vertical, None)
        
        slot_readiness = "ready_for_dossier"
        if row[3]:
            slot_readiness = "requires_human_review"
        elif row[1] < 0.5:
            slot_readiness = "low_signal"
            
        stub_id = str(uuid.uuid4())
        
        conn.execute(text("""
            INSERT INTO dossier_stubs (stub_id, prospect_id, company_facts, verified_vertical, headline_kg_anchor, slot_readiness, generated_at)
            VALUES (:stub_id, :pid, '{}', :vertical, :anchor, :slot, :now)
        """), {
            "stub_id": stub_id,
            "pid": prospect_id,
            "vertical": vertical,
            "anchor": anchor_id,
            "slot": slot_readiness,
            "now": datetime.utcnow()
        })
        
        for surface in ["slack_canvas", "crm_field", "drive_doc"]:
            outbox_id = str(uuid.uuid4())
            conn.execute(text("""
                INSERT INTO outbox (id, surface, payload, delivery_attempts, state, next_attempt_at)
                VALUES (:id, :surf, '{}', 0, 'pending', :now)
            """), {
                "id": outbox_id, "surf": surface, "now": datetime.utcnow()
            })
            
            app.send_task("refinery.outbox_dispatcher", args=[outbox_id])
