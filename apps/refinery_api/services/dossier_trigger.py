"""Shared dossier-trigger logic.

Both the Slack webhook (/slack/interactions) and the first-party demo
endpoint (/api/demo/generate-briefing) need to enqueue a dossier
generation for a given prospect. The compute path is identical:
server-side signal_hash → KG-version-keyed Redis cache → uuid mint →
Celery dispatch. Extracted here so the two callers can't drift.

The Slack handler stays behind signature.verify(); the demo handler
stays behind a pre-bake-batch scope guard. Authorisation is each
caller's responsibility — this function only does the trigger work.
"""
import hashlib
import uuid

from fastapi import HTTPException
from sqlalchemy import text

from packages.knowledge_graph.loader import load_graph
from packages.schemas.dossier import DossierAck


async def compute_signal_hash(prospect_id: str, session) -> str:
    """Deterministic 16-char SHA256 prefix from the prospect's current state.

    Phase 1.7 Stage C: signal_hash is part of dossier_artifacts'
    idempotency key. Computed server-side rather than trusting any
    caller (Slack form payload or demo UI body) to prevent forgery and
    staleness.
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


async def trigger_dossier_generation(
    prospect_id: str,
    session,
    redis,
    celery,
) -> DossierAck:
    """Idempotently enqueue dossier generation for a prospect.

    Returns the existing dossier_id (status='cached') if the prospect's
    signal_hash + KG version produces a key already in Redis;
    otherwise mints a fresh uuid, caches it, and dispatches the
    generate_dossier Celery task (status='generating').
    """
    signal_hash = await compute_signal_hash(prospect_id, session)
    kg_version = load_graph().version
    key = f"dossier:{prospect_id}:{signal_hash}:{kg_version}"

    cached = await redis.get(key)
    if cached:
        return DossierAck(dossier_id=cached.decode("utf-8"), status="cached")

    new_id = str(uuid.uuid4())
    await redis.set(key, new_id, ex=86400 * 7)
    celery.send_task("refinery.generate_dossier", args=[prospect_id, new_id])
    return DossierAck(dossier_id=new_id, status="generating")
