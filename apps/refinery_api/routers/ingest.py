from fastapi import APIRouter, Form, UploadFile, File, HTTPException, status
from typing import Annotated
import hashlib
from datetime import date
from ..deps import RedisDep, CeleryDep, SessionDep, UserDep
from packages.schemas.lead_intake import IngestAck
from packages.ingest.csv_parser import parse_csv_to_batch
from pydantic import ValidationError
from packages.models.prospects import IngestBatch, LeadProspect

router = APIRouter()

@router.post("/ingest/batch", response_model=IngestAck, status_code=200)
async def receive_batch(
    file: Annotated[UploadFile, File(...)],
    source_label: Annotated[str, Form(...)],
    redis: RedisDep,
    celery: CeleryDep,
    session: SessionDep,
    user: UserDep,
) -> IngestAck:
    file_bytes = await file.read()
    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large")
    
    file_sha256 = hashlib.sha256(file_bytes).hexdigest()
    idempotency_key = f"batch:{file_sha256}:{user.id}:{date.today().isoformat()}"
    
    cached = await redis.get(idempotency_key)
    if cached:
        return IngestAck.model_validate_json(cached)
        
    try:
        batch = parse_csv_to_batch(file_bytes, source_label, user)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
        
    try:
        # Tightening 1 transactional posture
        db_batch = IngestBatch(id=batch.batch_id, source_surface=batch.source_surface, file_sha256=file_sha256, user_id=user.id, day=date.today())
        session.add(db_batch)
        for row in batch.rows:
            prospect_id = f"pros_{hashlib.md5(f'{batch.source_surface}:{row.external_lead_id}'.encode()).hexdigest()[:12]}"
            prospect = LeadProspect(
                id=prospect_id,
                batch_id=batch.batch_id,
                source_system=batch.source_surface,
                external_lead_id=row.external_lead_id,
                company_name=row.company_name,
                factory_size_band=row.factory_size_band or "unknown",
            )
            await session.merge(prospect)
        await session.commit()
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Database transaction failed")
        
    ack = IngestAck(batch_id=batch.batch_id, status="scoring", row_count=len(batch.rows))
    await redis.set(idempotency_key, ack.model_dump_json(), ex=86400)
    
    celery.send_task("refinery.score_batch", args=[batch.batch_id])
    
    return ack
