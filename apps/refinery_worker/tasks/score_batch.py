from ..app import app
from celery import chain, chord
from sqlalchemy import create_engine, text
from apps.refinery_api.config import settings

engine = create_engine(settings.postgres_url.replace('+asyncpg', ''))

@app.task(
    name="refinery.score_batch",
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=3,
)
def score_batch(self, batch_id: str):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT p.id 
            FROM lead_prospects p
            JOIN ingest_batches b ON p.source_system = b.source_surface
            WHERE b.id = :batch_id
        """), {"batch_id": batch_id})
        prospect_ids = [row[0] for row in result]
    
    chains = []
    for pid in prospect_ids:
        chains.append(
            chain(
                app.signature("refinery.enrich_prospect", args=[pid]),
                app.signature("refinery.classify_vertical", args=[pid]),
                app.signature("refinery.score_fitness", args=[pid])
            )
        )
        
    if chains:
        chord(chains)(app.signature("refinery.assemble_queue_and_stubs", args=[batch_id]))
