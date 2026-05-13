from ..app import app
import asyncio
from google import genai
from google.genai.types import GenerateContentConfig, ThinkingConfig
from apps.refinery_api.config import settings
from packages.schemas.dossier import ComparableDeployment
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated

client = genai.Client(vertexai=True, project=settings.gcp_project, location=settings.vertex_location)

class DimensionOfComparabilityProse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prose: Annotated[str, Field(max_length=250)]

@app.task(
    name="refinery.dossier_section_comparable",
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=3,
)
def dossier_section_comparable(self, prospect_id: str, dossier_id: str):
    from packages.knowledge_graph.select import select_comparable
    vertical = "metal_casting"
    anchor_id, line, dims = select_comparable(vertical, None)
    
    if anchor_id == "no_comparable_available":
        res = ComparableDeployment(
            matta_customer_anchor="no_comparable_available",
            citation_substrate_line=0,
            dimension_of_comparability="No verified Matta deployment in this vertical sub-path.",
            selection_method="no_comparable_available"
        )
        return
        
    from packages.prompts.comparable_pro import COMPARABLE_PROMPT
    prompt = COMPARABLE_PROMPT.format(
        matta_customer_anchor=anchor_id,
        citation_substrate_line=line,
        permitted_dimensions_of_comparability=str(dims),
        company_name="Mock",
        vertical=vertical,
        process_taxonomy_json="{}"
    )
    
    async def run():
        response = await client.aio.models.generate_content(
            model="gemini-2.5-pro",
            contents=[prompt],
            config=GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=DimensionOfComparabilityProse,
                thinking_config=ThinkingConfig(thinking_level="low"),
                temperature=0.3,
                max_output_tokens=256,
            ),
        )
        return DimensionOfComparabilityProse.model_validate_json(response.text)
        
    prose_obj = asyncio.run(run())
    
    res = ComparableDeployment(
        matta_customer_anchor=anchor_id,
        citation_substrate_line=line,
        dimension_of_comparability=prose_obj.prose,
        selection_method="deterministic_rules"
    )
    
    app.send_task("refinery.dossier_section_risk", args=[prospect_id, dossier_id])
    app.send_task("refinery.dossier_section_approach", args=[prospect_id, dossier_id])
