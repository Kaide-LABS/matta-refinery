from ..app import app
import redis
from apps.refinery_api.config import settings

@app.task(name="refinery.release_slack_lock")
def release_slack_lock(slack_event_id: str, success: bool = False):
    r = redis.Redis.from_url(settings.redis_url)
    if success:
        r.set(f"slack:event:{slack_event_id}", "1", ex=86400)
    r.delete(f"slack:lock:{slack_event_id}")

@app.task(name="refinery.release_slack_lock_and_mark_complete")
def release_slack_lock_and_mark_complete(slack_event_id: str):
    release_slack_lock(slack_event_id, success=True)
