from ..app import app
import asyncio
from google import genai
from google.genai.types import GenerateContentConfig
from apps.refinery_api.config import settings
from packages.schemas.defect_hypothesis import LikelyDefectClassHypothesis
from packages.uncertainty.conformal import compute_conformal_set, CalibrationTable
import json
from datetime import datetime

client = genai.Client(vertexai=True, project=settings.gcp_project, location=settings.vertex_location)

@app.task(
    name="refinery.dossier_section_defect",
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=8,
)
def dossier_section_defect(self, prospect_id: str, dossier_id: str):
    from packages.prompts.defect_flash import DEFECT_PROMPT
    from packages.knowledge_graph.evidence import compute_allowed_evidence
    from packages.uncertainty.dscp import semantic_distance, DSCP_SEVERE_SHIFT_THRESHOLD
    from sqlalchemy import create_engine, text
    
    engine = create_engine(settings.postgres_url.replace('+asyncpg', ''))
    with engine.connect() as conn:
        row = conn.execute(text("SELECT vertical FROM lead_prospects WHERE id = :pid"), {"pid": prospect_id}).first()
        vertical = row[0] if row else "unknown"
        
    signals = {} # Future: pull from lead_prospects.signals if added
    
    allowed_evidence = compute_allowed_evidence(vertical, "defect_hypothesis", signals)
    
    if not allowed_evidence:
        # Log or handle appropriately
        return
        
    prompt = DEFECT_PROMPT.format(
        vertical=vertical,
        process_taxonomy_json="{}",
        allowed_evidence=str(allowed_evidence)
    )
    
    def call_gemini(temp):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt],
            config=GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=LikelyDefectClassHypothesis,
                temperature=temp,
                max_output_tokens=256,
            ),
        )
        text = response.text
        json_str = text[text.find('{'):text.rfind('}')+1] if '{' in text else text
        return LikelyDefectClassHypothesis.model_validate_json(json_str)
        
    samples = []
    for t in [0.1, 0.5, 0.9]:
        samples.append(call_gemini(t))
    
    with open("packages/uncertainty/calibration_table.json") as f:
        calib = CalibrationTable.model_validate_json(f.read())
        
    conformal_set, coverage = compute_conformal_set(samples, calib)
    
    final_res = LikelyDefectClassHypothesis(
        conformal_set=conformal_set, coverage=coverage, calibration_version=calib.calibration_version,
        requires_human_review=False, rationale="Computed via conformal ensemble"
    )
    
    with engine.begin() as conn:
        conn.execute(text("UPDATE dossier_artifacts SET defect_hypothesis = :res WHERE dossier_id = :did"), 
            {"res": final_res.model_dump_json(), "did": dossier_id})
        
    app.send_task("refinery.dossier_section_comparable", args=[prospect_id, dossier_id])
