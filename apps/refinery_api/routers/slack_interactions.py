from fastapi import APIRouter, Request, HTTPException
from ..deps import RedisDep, CeleryDep, SessionDep
from packages.schemas.dossier import DossierAck
from packages.schemas.slack_ingress import SlackDossierAction
from packages.adapters.slack import signature
from ..config import settings
from packages.knowledge_graph.loader import load_graph
import uuid
import urllib.parse
import json

router = APIRouter()

@router.post("/slack/interactions", response_model=DossierAck)
async def receive_slack_interaction(
    request: Request,
    redis: RedisDep,
    celery: CeleryDep,
    session: SessionDep,
) -> DossierAck:
    raw_body = await request.body()
    try:
        signature.verify(headers=request.headers, body=raw_body, signing_secret=settings.slack_signing_secret, window_seconds=300)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid signature")

    form_data = await request.form()
    payload_str = form_data.get("payload")
    if not payload_str:
        raise HTTPException(status_code=422, detail="Missing payload")

    action = SlackDossierAction.model_validate_json(payload_str)
    
    kg = load_graph()
    kg_version = kg.version
    
    key = f"dossier:{action.prospect_id}:{action.signal_hash}:{kg_version}"
    cached = await redis.get(key)
    
    if cached:
        return DossierAck(dossier_id=cached.decode("utf-8"), status="cached")
        
    new_id = str(uuid.uuid4())
    await redis.set(key, new_id, ex=86400*7)
    celery.send_task("refinery.generate_dossier", args=[action.prospect_id, new_id])
    
    return DossierAck(dossier_id=new_id, status="generating")
