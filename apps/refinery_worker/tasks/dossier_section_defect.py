from ..app import app
import asyncio
from google import genai
from google.genai.types import GenerateContentConfig, HttpOptions
from apps.refinery_api.config import settings
from packages.schemas.defect_hypothesis import LikelyDefectClassHypothesis
from packages.uncertainty.agreement import compute_agreement_set, CalibrationTable
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
        # Phase 1.7 Stage D: previously this silently returned, killing
        # the dossier composition chain for any prospect whose vertical
        # had no matching KG anchor (e.g. metal_casting after Stage C's
        # drop). The correct DS-CP behavior is to mark §2 as
        # UNVERIFIED_INSUFFICIENT_DATA via explicit deferral, persist a
        # minimal placeholder, and STILL dispatch the next section task.
        final_res = LikelyDefectClassHypothesis(
            agreement_set=[],
            coverage=0.0,
            calibration_version="phase1-demo-v1",
            requires_human_review=True,
            rationale=(
                "No matching KG anchor for this prospect's vertical; "
                "DS-CP (Tightening 4) gates the section to unverified."
            ),
            deferral_reason="insufficient_calibration_data",
            inter_model_agreement_score=0.0,
        )
        with engine.begin() as conn:
            conn.execute(
                text(
                    "UPDATE dossier_artifacts "
                    "SET defect_hypothesis = :res WHERE dossier_id = :did"
                ),
                {"res": final_res.model_dump_json(), "did": dossier_id},
            )
        app.send_task("refinery.dossier_section_comparable", args=[prospect_id, dossier_id])
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
                max_output_tokens=2048,
                # Stage E audit fix: explicit 60s timeout — Vertex stalls
                # previously hung tasks until Celery visibility_timeout.
                http_options=HttpOptions(timeout=60_000),
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
        
    result = compute_agreement_set(samples, calib)

    final_res = LikelyDefectClassHypothesis(
        agreement_set=result.agreement_set,
        coverage=result.coverage,
        calibration_version=calib.calibration_version,
        requires_human_review=result.requires_human_review,
        rationale="Computed via N=3 temperature-varied ensemble agreement gating",
        deferral_reason=result.deferral_reason,
        inter_model_agreement_score=result.inter_model_agreement_score,
    )
    
    with engine.begin() as conn:
        conn.execute(text("UPDATE dossier_artifacts SET defect_hypothesis = :res WHERE dossier_id = :did"), 
            {"res": final_res.model_dump_json(), "did": dossier_id})
        
    app.send_task("refinery.dossier_section_comparable", args=[prospect_id, dossier_id])
