from ..app import app
from sqlalchemy import create_engine, text
from apps.refinery_api.config import settings

@app.task(
    name="refinery.assemble_queue_and_stubs",
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=60,
    max_retries=3,
)
def assemble_queue_and_stubs(self, *args, **kwargs):
    # args[0] might be the list of chord results, args[1] might be batch_id if passed as args=[batch_id]
    # Actually, Celery chords pass the results of the header tasks as the first argument to the body task.
    # If app.signature("refinery.assemble_queue_and_stubs", args=[batch_id]) is used, the chord results are prepended.
    # So args[0] = list of prospect_ids, args[1] = batch_id.
    if len(args) >= 2:
        batch_id = args[1]
    elif len(args) == 1:
        # If it was called directly without chord results
        batch_id = args[0]
    else:
        return
        
    engine = create_engine(settings.postgres_url.replace('+asyncpg', ''))
    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT id FROM lead_prospects 
            WHERE batch_id = :batch_id AND fitness_score IS NOT NULL
            ORDER BY fitness_score DESC
            LIMIT 12
        """), {"batch_id": batch_id})
        top_prospects = [row[0] for row in result]
        
    for pid in top_prospects:
        app.send_task("refinery.generate_dossier_stub", args=[pid, batch_id])
