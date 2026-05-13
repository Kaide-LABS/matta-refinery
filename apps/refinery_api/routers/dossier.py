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
    query = text("SELECT state, payload_json FROM dossier_artifacts WHERE dossier_id = :dossier_id")
    result = await session.execute(query, {"dossier_id": dossier_id})
    row = result.first()
    
    if not row:
        raise HTTPException(status_code=404, detail="Dossier not found")
        
    state, payload_json = row
    
    if state == "complete":
        return PreVisitDossier.model_validate_json(payload_json)
    elif state == "generating":
        return JSONResponse(status_code=202, content=DossierAck(dossier_id=dossier_id, status="generating").model_dump())
    
    raise HTTPException(status_code=400, detail=f"Dossier state: {state}")
