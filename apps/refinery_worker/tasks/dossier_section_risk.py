from ..app import app
import asyncio
from google import genai
from google.genai.types import GenerateContentConfig, ThinkingConfig
from apps.refinery_api.config import settings
from packages.schemas.dossier import RiskRegister

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
    max_retries=3,
)
def dossier_section_risk(self, prospect_id: str, dossier_id: str):
    from packages.prompts.risk_pro import RISK_PROMPT
    prompt = RISK_PROMPT.format(
        company_name="Mock",
        vertical="metal_casting",
        process_taxonomy_json="{}",
        enrichment_payload="{}"
    )
    
    async def run():
        response = await client.aio.models.generate_content(
            model="gemini-2.5-pro",
            contents=[prompt],
            config=GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=RiskRegister,
                thinking_config=ThinkingConfig(thinking_level="low"),
                temperature=0.2,
                max_output_tokens=768,
            ),
        )
        return RiskRegister.model_validate_json(response.text)
        
    risk = asyncio.run(run())
