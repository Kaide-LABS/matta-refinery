from ..app import app
from packages.scoring.fitness import compute_fitness
from sqlalchemy import create_engine, text
from apps.refinery_api.config import settings

@app.task(
    name="refinery.score_fitness",
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=3,
)
def score_fitness(self, prospect_id: str):
    engine = create_engine(settings.postgres_url.replace('+asyncpg', ''))
    with engine.begin() as conn:
        row = conn.execute(text("SELECT vertical, factory_size_band, trade_show_provenance FROM lead_prospects WHERE id = :pid"), {"pid": prospect_id}).first()
        prospect = {
            "vertical": row[0],
            "factory_size_band": row[1],
            "trade_show_provenance": row[2]
        }
        score = compute_fitness(prospect, {})
        conn.execute(text("UPDATE lead_prospects SET fitness_score = :s WHERE id = :pid"), {"s": score, "pid": prospect_id})
    return prospect_id
