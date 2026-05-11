from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from ..deps import RedisDep, CeleryDep
from packages.schemas.slack_ingress import SlackEventAck, SlackEventPayload
from packages.adapters.slack import signature
from ..config import settings

router = APIRouter()
SLACK_LOCK_TTL_SECONDS = 60

@router.post("/slack/events", response_model=SlackEventAck)
async def receive_slack_event(
    request: Request,
    redis: RedisDep,
    celery: CeleryDep,
) -> SlackEventAck | JSONResponse:
    raw_body = await request.body()
    try:
        signature.verify(headers=request.headers, body=raw_body, signing_secret=settings.slack_signing_secret, window_seconds=300)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        payload = SlackEventPayload.model_validate_json(raw_body)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    if payload.type == "url_verification":
        return JSONResponse(status_code=200, content={"challenge": payload.challenge})

    lock_acquired = await redis.set(
        f"slack:lock:{payload.event_id}", "1",
        ex=SLACK_LOCK_TTL_SECONDS, nx=True,
    )

    if not lock_acquired:
        return JSONResponse(status_code=202, content={"status": "duplicate_in_flight", "event_id": payload.event_id})

    cached = await redis.get(f"slack:event:{payload.event_id}")
    if cached:
        await redis.delete(f"slack:lock:{payload.event_id}")
        return SlackEventAck(status="duplicate", event_id=payload.event_id)

    if payload.event.get("type") == "file_shared":
        celery.send_task("refinery.parse_slack_ingress", kwargs={"slack_event_id": payload.event_id})
        
    return SlackEventAck(status="accepted", event_id=payload.event_id)
