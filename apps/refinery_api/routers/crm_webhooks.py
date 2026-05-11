from fastapi import APIRouter, Request, HTTPException
from typing import Literal
from ..deps import RedisDep, CeleryDep
from packages.schemas.crm import CRMWebhookAck, CRMLeadSignal
from ..config import settings
import hashlib

router = APIRouter()

def compute_changed_fields_hash(changed_fields: dict) -> str:
    s = "".join(f"{k}:{v}" for k, v in sorted(changed_fields.items()))
    return hashlib.sha256(s.encode()).hexdigest()

@router.post("/crm/webhook/{provider}", response_model=CRMWebhookAck)
async def crm_webhook(
    provider: Literal["hubspot", "salesforce"],
    request: Request,
    redis: RedisDep,
    celery: CeleryDep,
) -> CRMWebhookAck:
    raw_body = await request.body()
    
    if provider == "hubspot":
        sig = request.headers.get("X-Mock-Signature") or request.headers.get("X-HubSpot-Signature-v3")
        if not sig: raise HTTPException(status_code=401, detail="Invalid signature")
    elif provider == "salesforce":
        sig = request.headers.get("X-Mock-Signature")
        if not sig: raise HTTPException(status_code=401, detail="Invalid signature")
        
    signal = CRMLeadSignal.model_validate_json(raw_body)
    
    idempotency_key = f"crm:{provider}:{signal.object_id}:{signal.updated_at.isoformat()}:{compute_changed_fields_hash(signal.changed_fields)}"
    
    cached = await redis.get(idempotency_key)
    if cached:
        return CRMWebhookAck(status="duplicate")
        
    await redis.set(idempotency_key, "1", ex=86400)
    celery.send_task("refinery.normalize_crm_event", args=[signal.model_dump_json()])
    
    return CRMWebhookAck(status="accepted")
