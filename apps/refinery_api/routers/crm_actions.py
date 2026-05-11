from fastapi import APIRouter, HTTPException
from ..deps import RedisDep, CeleryDep, SessionDep
from packages.schemas.dossier import DossierAck
from packages.schemas.crm import CRMDossierActionRequest
from packages.knowledge_graph.loader import load_graph
from sqlalchemy import text
import uuid

router = APIRouter()

@router.post("/crm/actions/generate-dossier", response_model=DossierAck)
async def crm_generate_dossier(
    payload: CRMDossierActionRequest,
    redis: RedisDep, celery: CeleryDep, session: SessionDep,
) -> DossierAck:
    query = text("SELECT id, signal_hash FROM lead_prospects WHERE source_system = :provider AND external_lead_id = :crm_object_id")
    result = await session.execute(query, {"provider": payload.provider, "crm_object_id": payload.crm_object_id})
    row = result.first()
    
    if not row:
        raise HTTPException(status_code=404, detail="Prospect not found")
        
    prospect_id, signal_hash = row
    
    kg = load_graph()
    key = f"dossier:{prospect_id}:{signal_hash}:{kg.version}"
    
    cached = await redis.get(key)
    if cached:
        return DossierAck(dossier_id=cached.decode("utf-8"), status="cached")
        
    new_id = str(uuid.uuid4())
    await redis.set(key, new_id, ex=86400*7)
    celery.send_task("refinery.generate_dossier", args=[prospect_id, new_id])
    
    return DossierAck(dossier_id=new_id, status="generating")
