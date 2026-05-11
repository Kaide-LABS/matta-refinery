from ..app import app
import asyncio
from google import genai
from google.genai.types import GenerateContentConfig, ThinkingConfig
from apps.refinery_api.config import settings
from packages.schemas.defect_hypothesis import VerticalClassification
from collections import Counter
from sqlalchemy import create_engine, text

client = genai.Client(vertexai=True, project=settings.gcp_project, location=settings.vertex_location)

async def call_gemini(prospect_data, temp):
    from packages.prompts.vertical_flash import VERTICAL_PROMPT
    prompt = VERTICAL_PROMPT.format(**prospect_data)
    response = await client.aio.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[prompt],
        config=GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=VerticalClassification,
            thinking_config=ThinkingConfig(thinking_level="minimal"),
            temperature=temp,
            max_output_tokens=128,
        ),
    )
    return VerticalClassification.model_validate_json(response.text)

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
        prospect_data = {
            "company_name": row[0],
            "sector_hint": row[1] or "",
            "enrichment_summary": "",
            "raw_notes": row[2] or "",
        }
        
    async def run_all():
        temps = [0.1, 0.5, 0.9]
        return await asyncio.gather(*[call_gemini(prospect_data, t) for t in temps])
        
    samples = asyncio.run(run_all())
    
    votes = Counter([s.vertical for s in samples])
    most_common = votes.most_common(1)[0]
    
    requires_human_review = False
    if most_common[1] == 1:
        vertical = "vertical_uncertain"
        requires_human_review = True
    else:
        vertical = most_common[0]
        
    with engine.begin() as conn:
        conn.execute(text("UPDATE lead_prospects SET vertical = :v, requires_human_review = :r WHERE id = :pid"), 
            {"v": vertical, "r": requires_human_review, "pid": prospect_id})
            
    return prospect_id
