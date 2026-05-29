"""First-party demo endpoint for the Theater UI.

The Theater UI is a first-party browser frontend, not Slack. It cannot
produce a Slack signature (the signing secret is server-side; embedding
it in the React bundle would expose it). C1 (ddee9f5) correctly hardened
/slack/interactions to require a valid signature, which broke the
browser's Generate Briefing button.

This router exposes POST /api/demo/generate-briefing — a first-party
trigger that reuses the same trigger_dossier_generation service the
Slack handler uses, without requiring a Slack signature. The endpoint
is guarded to only operate on prospects belonging to a pre-bake batch
(user_id='demo-prebake') so it can't be abused to enqueue arbitrary
work. A production deployment would gate this behind real auth (session
cookie, JWT, etc.) — this guard is appropriate for the Phase 1.7 demo.
"""
from typing import Annotated

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import text

from ..deps import CeleryDep, RedisDep, SessionDep
from ..services.dossier_trigger import trigger_dossier_generation
from packages.schemas.dossier import DossierAck

router = APIRouter(prefix="/api/demo")


class DemoBriefingRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prospect_id: Annotated[str, Field(min_length=1, max_length=64)]
    batch_id: Annotated[str, Field(min_length=1, max_length=64)]


@router.post("/generate-briefing", response_model=DossierAck)
async def demo_generate_briefing(
    req: DemoBriefingRequest,
    session: SessionDep,
    redis: RedisDep,
    celery: CeleryDep,
) -> DossierAck:
    """Trigger dossier generation from the first-party demo UI.

    Guarded to pre-bake batches only: the prospect must belong to the
    provided batch_id, and that batch must be a pre-bake batch
    (user_id='demo-prebake'). Anything else returns 404.
    """
    row = (
        await session.execute(
            text(
                "SELECT 1 FROM lead_prospects p "
                "JOIN ingest_batches b ON b.id = p.batch_id "
                "WHERE p.id = :pid "
                "AND p.batch_id = :bid "
                "AND b.user_id = 'demo-prebake'"
            ),
            {"pid": req.prospect_id, "bid": req.batch_id},
        )
    ).first()
    if row is None:
        raise HTTPException(
            status_code=404,
            detail="prospect not found in pre-bake batch",
        )

    return await trigger_dossier_generation(
        prospect_id=req.prospect_id,
        session=session,
        redis=redis,
        celery=celery,
    )
