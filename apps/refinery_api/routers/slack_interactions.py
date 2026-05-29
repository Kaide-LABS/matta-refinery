from fastapi import APIRouter, HTTPException, Request

from ..config import settings
from ..deps import CeleryDep, RedisDep, SessionDep
from ..services.dossier_trigger import trigger_dossier_generation
from packages.adapters.slack import signature
from packages.adapters.slack.signature import SlackSignatureError
from packages.schemas.dossier import DossierAck
from packages.schemas.slack_ingress import SlackDossierAction

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
        signature.verify(
            headers=request.headers,
            body=raw_body,
            signing_secret=settings.slack_signing_secret,
            window_seconds=300,
        )
    except SlackSignatureError as e:
        raise HTTPException(status_code=401, detail=f"slack signature: {e}")

    form_data = await request.form()
    payload_str = form_data.get("payload")
    if not payload_str:
        raise HTTPException(status_code=422, detail="Missing payload")

    action = SlackDossierAction.model_validate_json(payload_str)
    return await trigger_dossier_generation(
        prospect_id=action.prospect_id,
        session=session,
        redis=redis,
        celery=celery,
    )
