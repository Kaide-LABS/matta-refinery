import hashlib
import json
import urllib.parse
import uuid

from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import text

from ..config import settings
from ..deps import CeleryDep, RedisDep, SessionDep
from packages.adapters.slack import signature
from packages.adapters.slack.signature import SlackSignatureError
from packages.knowledge_graph.loader import load_graph
from packages.schemas.dossier import DossierAck
from packages.schemas.slack_ingress import SlackDossierAction

router = APIRouter()


async def compute_signal_hash_server_side(prospect_id: str, session) -> str:
    """Deterministic 16-char SHA256 prefix from the prospect's current state.

    Phase 1.7 Stage C: signal_hash is part of dossier_artifacts' idempotency
    key. Computing it server-side rather than trusting the frontend prevents
    forgery (overwriting another prospect's dossier) and staleness (lagging
    behind actual prospect state).
    """
    row = (
        await session.execute(
            text(
                "SELECT company_name, vertical, factory_size_band, "
                "fitness_score, raw_notes "
                "FROM lead_prospects WHERE id = :pid"
            ),
            {"pid": prospect_id},
        )
    ).first()
    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"prospect_id {prospect_id} not found",
        )
    fitness = float(row[3] or 0.0)
    signal_input = (
        f"{row[0] or ''}|{row[1] or ''}|{row[2] or ''}|"
        f"{fitness:.4f}|{row[4] or ''}"
    )
    return hashlib.sha256(signal_input.encode("utf-8")).hexdigest()[:16]


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

    # Phase 1.7 Stage C: server-side signal_hash compute. Drops trust on
    # client-supplied hash (action.signal_hash removed from schema).
    signal_hash = await compute_signal_hash_server_side(action.prospect_id, session)

    kg = load_graph()
    kg_version = kg.version

    key = f"dossier:{action.prospect_id}:{signal_hash}:{kg_version}"
    cached = await redis.get(key)

    if cached:
        return DossierAck(dossier_id=cached.decode("utf-8"), status="cached")

    new_id = str(uuid.uuid4())
    await redis.set(key, new_id, ex=86400*7)
    celery.send_task("refinery.generate_dossier", args=[action.prospect_id, new_id])

    return DossierAck(dossier_id=new_id, status="generating")
