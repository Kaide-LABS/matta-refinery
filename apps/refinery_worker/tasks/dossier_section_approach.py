from ..app import app
from google import genai
from google.genai.types import GenerateContentConfig
from apps.refinery_api.config import settings
from packages.schemas.dossier import SuggestedApproach
from sqlalchemy import create_engine, text

client = genai.Client(vertexai=True, project=settings.gcp_project, location=settings.vertex_location)

@app.task(
    name="refinery.dossier_section_approach",
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=8,
)
def dossier_section_approach(self, prospect_id: str, dossier_id: str):
    from packages.prompts.approach_pro import APPROACH_PROMPT

    engine = create_engine(settings.postgres_url.replace('+asyncpg', ''))
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT vertical FROM lead_prospects WHERE id = :pid"), {"pid": prospect_id}
        ).first()
    vertical = (row[0] if row else None) or "metal_casting"

    prompt = APPROACH_PROMPT.format(
        company_name="Mock",
        vertical=vertical,
        process_taxonomy_json="{}",
        conformal_set="[]",
        risk_findings="[]"
    )

    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=[prompt],
        config=GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=SuggestedApproach,
            temperature=0.2,
            max_output_tokens=2048,
        ),
    )
    text_resp = response.text
    json_str = text_resp[text_resp.find('{'):text_resp.rfind('}')+1] if '{' in text_resp else text_resp
    appr = SuggestedApproach.model_validate_json(json_str)

    with engine.begin() as conn:
        conn.execute(
            text("UPDATE dossier_artifacts SET suggested_approach = :payload WHERE dossier_id = :did"),
            {"payload": appr.model_dump_json(), "did": dossier_id},
        )

    app.send_task("refinery.compose_dossier", args=[dossier_id])
