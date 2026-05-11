from ..app import app
from sqlalchemy import create_engine, text
from apps.refinery_api.config import settings

@app.task(
    name="refinery.generate_dossier",
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=3,
)
def generate_dossier(self, prospect_id: str, dossier_id: str):
    engine = create_engine(settings.postgres_url.replace('+asyncpg', ''))
    with engine.begin() as conn:
        conn.execute(text("UPDATE dossier_artifacts SET state = 'generating' WHERE dossier_id = :did"), {"did": dossier_id})
        
    app.send_task("refinery.dossier_section_taxonomy", args=[prospect_id, dossier_id])
