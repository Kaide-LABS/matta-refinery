from ..app import app
from google import genai
from google.genai.types import GenerateContentConfig
from apps.refinery_api.config import settings
from packages.schemas.dossier import RiskRegister
from sqlalchemy import create_engine, text

client = genai.Client(vertexai=True, project=settings.gcp_project, location=settings.vertex_location)

@app.task(
    name="refinery.dossier_section_risk",
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=8,
)
def dossier_section_risk(self, prospect_id: str, dossier_id: str):
    from packages.prompts.risk_pro import RISK_PROMPT

    engine = create_engine(settings.postgres_url.replace('+asyncpg', ''))
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT vertical, company_name FROM lead_prospects WHERE id = :pid"),
            {"pid": prospect_id},
        ).first()
    vertical = (row[0] if row else None) or "metal_casting"
    company_name = (row[1] if row else None) or "the prospect"

    prompt = RISK_PROMPT.format(
        company_name=company_name,
        vertical=vertical,
        process_taxonomy_json="{}",
        enrichment_payload="{}"
    )

    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=[prompt],
        config=GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RiskRegister,
            temperature=0.2,
            max_output_tokens=2048,
        ),
    )
    text_resp = response.text
    json_str = text_resp[text_resp.find('{'):text_resp.rfind('}')+1] if '{' in text_resp else text_resp
    risk = RiskRegister.model_validate_json(json_str)

    with engine.begin() as conn:
        conn.execute(
            text("UPDATE dossier_artifacts SET risk_register = :payload WHERE dossier_id = :did"),
            {"payload": risk.model_dump_json(), "did": dossier_id},
        )

    app.send_task("refinery.dossier_section_approach", args=[prospect_id, dossier_id])
