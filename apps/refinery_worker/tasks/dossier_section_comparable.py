from ..app import app
from google import genai
from google.genai.types import GenerateContentConfig
from apps.refinery_api.config import settings
from packages.schemas.dossier import ComparableDeployment
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from sqlalchemy import create_engine, text

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
    max_retries=8,
)
def dossier_section_comparable(self, prospect_id: str, dossier_id: str):
    from packages.knowledge_graph.select import select_comparable

    engine = create_engine(settings.postgres_url.replace('+asyncpg', ''))
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT vertical FROM lead_prospects WHERE id = :pid"), {"pid": prospect_id}
        ).first()
    vertical = (row[0] if row else None) or "metal_casting"

    anchor_id, line, dims = select_comparable(vertical, None)

    if anchor_id == "no_comparable_available":
        res = ComparableDeployment(
            matta_customer_anchor="no_comparable_available",
            citation_substrate_line=1,
            dimension_of_comparability="No verified Matta deployment in this vertical sub-path.",
            selection_method="no_comparable_available"
        )
        with engine.begin() as conn:
            conn.execute(
                text("UPDATE dossier_artifacts SET comparable_deployment = :payload WHERE dossier_id = :did"),
                {"payload": res.model_dump_json(), "did": dossier_id},
            )
        app.send_task("refinery.dossier_section_risk", args=[prospect_id, dossier_id])
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
    
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=[prompt],
        config=GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=DimensionOfComparabilityProse,
            temperature=0.3,
            max_output_tokens=128,
        ),
    )
    text_resp = response.text
    json_str = text_resp[text_resp.find('{'):text_resp.rfind('}')+1] if '{' in text_resp else text_resp
    prose_obj = DimensionOfComparabilityProse.model_validate_json(json_str)
    
    # Normalize KG-internal anchor_id (prefixed `matta_deployment_*`) to the
    # MATTA_CUSTOMER_ANCHOR_ENUM literal expected by ComparableDeployment.
    # Pre-existing latent inconsistency: select.py and graph.json carry the
    # prefix; packages/schemas/dossier.py:8-12 enum strips it. Strip at the boundary.
    schema_anchor = anchor_id.removeprefix("matta_deployment_")
    res = ComparableDeployment(
        matta_customer_anchor=schema_anchor,
        citation_substrate_line=line,
        dimension_of_comparability=prose_obj.prose,
        selection_method="deterministic_rules"
    )

    with engine.begin() as conn:
        conn.execute(
            text("UPDATE dossier_artifacts SET comparable_deployment = :payload WHERE dossier_id = :did"),
            {"payload": res.model_dump_json(), "did": dossier_id},
        )

    app.send_task("refinery.dossier_section_risk", args=[prospect_id, dossier_id])
