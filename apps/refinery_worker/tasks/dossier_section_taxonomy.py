from ..app import app
from google import genai
from google.genai.types import GenerateContentConfig
from apps.refinery_api.config import settings
from packages.schemas.dossier import ProcessTaxonomy
from sqlalchemy import create_engine, text
import json
import asyncio

client = genai.Client(vertexai=True, project=settings.gcp_project, location=settings.vertex_location)

@app.task(
    name="refinery.dossier_section_taxonomy",
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=3,
)
def dossier_section_taxonomy(self, prospect_id: str, dossier_id: str):
    from packages.prompts.taxonomy_pro import TAXONOMY_PROMPT
    prompt = TAXONOMY_PROMPT.format(
        company_name="Mock Company",
        vertical="metal_casting",
        enrichment_payload="{}",
        allowed_evidence="[]"
    )
    
    async def run():
        response = await client.aio.models.generate_content(
            model="gemini-2.5-pro",
            contents=[prompt],
            config=GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ProcessTaxonomy,
                temperature=0.2,
                max_output_tokens=2048,
            ),
        )
        text = response.text
        json_str = text[text.find('{'):text.rfind('}')+1] if '{' in text else text
        return ProcessTaxonomy.model_validate_json(json_str)
        
    taxonomy = asyncio.run(run())

    engine = create_engine(settings.postgres_url.replace('+asyncpg', ''))
    with engine.begin() as conn:
        conn.execute(
            text("UPDATE dossier_artifacts SET process_taxonomy = :payload WHERE dossier_id = :did"),
            {"payload": taxonomy.model_dump_json(), "did": dossier_id},
        )

    app.send_task("refinery.dossier_section_defect", args=[prospect_id, dossier_id])
    app.send_task("refinery.dossier_section_comparable", args=[prospect_id, dossier_id])
