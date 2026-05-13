from ..app import app
from sqlalchemy import create_engine, text
from apps.refinery_api.config import settings
from datetime import datetime
import json

@app.task(
    name="refinery.outbox_dispatcher",
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=3,
)
def outbox_dispatcher(self, outbox_id: str):
    engine = create_engine(settings.postgres_url.replace('+asyncpg', ''))
    with engine.begin() as conn:
        row = conn.execute(text("SELECT surface, payload_jsonb, delivery_attempts, next_attempt_at, state FROM outbox WHERE id = :id FOR UPDATE"), {"id": outbox_id}).first()
        if not row:
            return
            
        surface, payload, delivery_attempts, next_attempt_at, state = row
        
        if state != "pending" or (next_attempt_at and next_attempt_at > datetime.utcnow()):
            return
            
        conn.execute(text("UPDATE outbox SET state = 'in_flight' WHERE id = :id"), {"id": outbox_id})
        
    try:
        pass
        with engine.begin() as conn:
            conn.execute(text("UPDATE outbox SET state = 'delivered' WHERE id = :id"), {"id": outbox_id})
    except Exception as e:
        delivery_attempts += 1
        with engine.begin() as conn:
            if delivery_attempts >= 6:
                conn.execute(text("""
                    INSERT INTO outbox_dlq (id, original_outbox_id, surface, payload_jsonb, delivery_attempts, final_error, failed_at)
                    VALUES (gen_random_uuid(), :id, :surf, :payload, :attempts, :err, :now)
                """), {"id": outbox_id, "surf": surface, "payload": payload, "attempts": delivery_attempts, "err": str(e), "now": datetime.utcnow()})
                conn.execute(text("DELETE FROM outbox WHERE id = :id"), {"id": outbox_id})
            else:
                conn.execute(text("""
                    UPDATE outbox SET delivery_attempts = :attempts, state = 'pending', last_error = :err
                    WHERE id = :id
                """), {"attempts": delivery_attempts, "err": str(e), "id": outbox_id})
        raise e
