from ..app import app
import asyncio
from google import genai
from google.genai.types import GenerateContentConfig, HttpOptions
from apps.refinery_api.config import settings
from packages.schemas.defect_hypothesis import VerticalClassification
from collections import Counter
from sqlalchemy import create_engine, text

client = genai.Client(vertexai=True, project=settings.gcp_project, location=settings.vertex_location)

def call_gemini(prospect_data, temp):
    from packages.prompts.vertical_flash import VERTICAL_PROMPT
    prompt = VERTICAL_PROMPT.format(**prospect_data)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt],
        config=GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=VerticalClassification,
            temperature=temp,
            max_output_tokens=2048,
            # Stage E audit fix: explicit 60s timeout — Vertex stalls
            # previously hung tasks until Celery visibility_timeout.
            http_options=HttpOptions(timeout=60_000),
        ),
    )
    text = response.text
    json_str = text[text.find('{'):text.rfind('}')+1] if '{' in text else text
    return VerticalClassification.model_validate_json(json_str)

@app.task(
    name="refinery.classify_vertical",
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=3,
)
def classify_vertical(self, prospect_id: str):
    engine = create_engine(settings.postgres_url.replace('+asyncpg', ''))
    with engine.connect() as conn:
        row = conn.execute(text("SELECT company_name, sector_hint, raw_notes FROM lead_prospects WHERE id = :pid"), {"pid": prospect_id}).first()
        if row is None:
            raise ValueError(f"prospect_id {prospect_id} not found in lead_prospects (stale task?)")
        prospect_data = {
            "company_name": row[0],
            "sector_hint": row[1] or "",
            "enrichment_summary": "",
            "raw_notes": row[2] or "",
        }
        
    samples = []
    for t in [0.1, 0.5, 0.9]:
        samples.append(call_gemini(prospect_data, t))
    
    classifications = [s.vertical for s in samples]
    votes = Counter(classifications)
    most_common = votes.most_common(1)[0]

    requires_human_review = False
    if most_common[1] == 1:
        # All three models disagreed — no majority. Phase 1.7 Stage C:
        # surface the uncertainty explicitly rather than silently picking
        # a default vertical (was: metal_casting via downstream code).
        vertical = "vertical_uncertain"
        requires_human_review = True
        vertical_ensemble_outputs = {
            "ensemble_outputs": classifications,
            "fallback_strategy": "explicit_uncertain_signal_no_default",
        }
    else:
        vertical = most_common[0]
        # Even on consensus, persist the per-model classifications for audit.
        vertical_ensemble_outputs = {
            "ensemble_outputs": classifications,
            "fallback_strategy": "majority_consensus",
        }

    import json
    with engine.begin() as conn:
        conn.execute(
            text(
                "UPDATE lead_prospects "
                "SET vertical = :v, "
                "    requires_human_review = :r, "
                "    vertical_ensemble_outputs = CAST(:veo AS JSONB) "
                "WHERE id = :pid"
            ),
            {
                "v": vertical,
                "r": requires_human_review,
                "veo": json.dumps(vertical_ensemble_outputs),
                "pid": prospect_id,
            },
        )

    return prospect_id
