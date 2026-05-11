from ..app import app
import asyncio
from google import genai
from google.genai.types import GenerateContentConfig, ThinkingConfig
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
    max_retries=3,
)
def dossier_section_defect(self, prospect_id: str, dossier_id: str):
    from packages.prompts.defect_flash import DEFECT_PROMPT
    from packages.knowledge_graph.evidence import compute_allowed_evidence
    from packages.uncertainty.dscp import semantic_distance, DSCP_SEVERE_SHIFT_THRESHOLD
    
    vertical = "metal_casting" 
    signals = {}
    
    allowed_evidence = compute_allowed_evidence(vertical, "defect_hypothesis", signals)
    
    if not allowed_evidence:
        res = LikelyDefectClassHypothesis(
            conformal_set=[], coverage=0.0, calibration_version="current", 
            requires_human_review=True, rationale="DS-CP severe shift / no anchor data"
        )
        return
        
    distance = semantic_distance(signals, {})
    if distance > DSCP_SEVERE_SHIFT_THRESHOLD:
        res = LikelyDefectClassHypothesis(
            conformal_set=[], coverage=0.0, calibration_version="current", 
            requires_human_review=True, rationale="DS-CP severe shift / no anchor data"
        )
        return
        
    prompt = DEFECT_PROMPT.format(
        vertical=vertical,
        process_taxonomy_json="{}",
        allowed_evidence=str(allowed_evidence)
    )
    
    async def call_gemini(temp):
        response = await client.aio.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[prompt],
            config=GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=LikelyDefectClassHypothesis,
                thinking_config=ThinkingConfig(thinking_level="minimal"),
                temperature=temp,
                max_output_tokens=512,
            ),
        )
        return LikelyDefectClassHypothesis.model_validate_json(response.text)
        
    async def run_all():
        temps = [0.1, 0.5, 0.9]
        return await asyncio.gather(*[call_gemini(t) for t in temps])
        
    samples = asyncio.run(run_all())
    
    with open("packages/uncertainty/calibration_table.json") as f:
        calib = CalibrationTable.model_validate_json(f.read())
        
    conformal_set, coverage = compute_conformal_set(samples, calib)
    
    final_res = LikelyDefectClassHypothesis(
        conformal_set=conformal_set, coverage=coverage, calibration_version=calib.calibration_version,
        requires_human_review=False, rationale="Computed via conformal ensemble"
    )
