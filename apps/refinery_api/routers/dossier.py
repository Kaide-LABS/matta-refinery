from typing import Any
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from ..deps import RedisDep, CeleryDep, SessionDep
from packages.schemas.dossier import DossierRequest, DossierAck, PreVisitDossier
from packages.knowledge_graph.loader import load_graph
from sqlalchemy import text
import uuid

router = APIRouter()

@router.post("/dossier/generate", response_model=DossierAck)
async def generate_dossier(
    payload: DossierRequest,
    redis: RedisDep, celery: CeleryDep, session: SessionDep,
) -> DossierAck:
    query = text("SELECT signal_hash, enrichment_status FROM lead_prospects WHERE id = :prospect_id")
    result = await session.execute(query, {"prospect_id": payload.prospect_id})
    row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail="Prospect not found")

    signal_hash, enrichment_status = row

    if enrichment_status == "failed":
        raise HTTPException(status_code=409, detail="Enrichment failed")

    kg = load_graph()
    key = f"dossier:{payload.prospect_id}:{signal_hash}:{kg.version}"

    cached = await redis.get(key)
    if cached and not payload.force_regenerate:
        return DossierAck(dossier_id=cached.decode("utf-8"), status="cached")

    new_id = str(uuid.uuid4())
    await redis.set(key, new_id, ex=86400*7)
    celery.send_task("refinery.generate_dossier", args=[payload.prospect_id, new_id])

    return DossierAck(dossier_id=new_id, status="generating")

@router.get("/dossier/{dossier_id}")
async def fetch_dossier(dossier_id: str, session: SessionDep) -> Any:
    # dossier_artifacts stores each section in its own JSONB column rather
    # than a single payload_json blob. Return the columns that have been
    # populated so far — the Theater UI polls this and renders sections as
    # they land. state='generating' returns 202 with any partial sections
    # available; state='complete' returns 200 with the full payload.
    query = text("""
        SELECT state, process_taxonomy, defect_hypothesis, comparable_deployment,
               risk_register, suggested_approach, unverified_sections,
               deterministic_section_ratio, validation_error, generated_at
        FROM dossier_artifacts
        WHERE dossier_id = :dossier_id
    """)
    result = await session.execute(query, {"dossier_id": dossier_id})
    row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail="Dossier not found")

    (
        state,
        process_taxonomy,
        defect_hypothesis,
        comparable_deployment,
        risk_register,
        suggested_approach,
        unverified_sections,
        deterministic_section_ratio,
        validation_error,
        generated_at,
    ) = row

    body = {
        "dossier_id": dossier_id,
        "state": state,
        "process_taxonomy": process_taxonomy,
        "defect_hypothesis": defect_hypothesis,
        "comparable_deployment": comparable_deployment,
        "risk_register": risk_register,
        "suggested_approach": suggested_approach,
        "unverified_sections": unverified_sections or [],
        "deterministic_section_ratio": deterministic_section_ratio,
        "validation_error": validation_error,
        "generated_at": generated_at.isoformat() if generated_at else None,
    }

    if state == "complete":
        return body
    if state == "generating":
        return JSONResponse(status_code=202, content=body)
    if state in ("failed", "rejected"):
        return JSONResponse(status_code=422, content=body)
    return body
