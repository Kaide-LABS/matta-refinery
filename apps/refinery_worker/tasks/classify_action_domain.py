from ..app import app
import json
from packages.adc.rules import route_request

@app.task(
    name="refinery.classify_action_domain",
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=3,
)
def classify_action_domain(self, envelope_json: str):
    envelope = json.loads(envelope_json)
    route = route_request(envelope)
    if route == "PRIORITIZATION":
        app.send_task("refinery.score_batch", args=[envelope["batch_id"]])
    elif route == "DOSSIER_STUB":
        pass
    elif route == "DOSSIER_FULL":
        app.send_task("refinery.generate_dossier", args=[envelope["prospect_id"], envelope["dossier_id"]])
    elif route == "HUMAN_REVIEW":
        pass
