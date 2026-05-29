"""First-party demo endpoint for the Theater UI.

The Theater UI is a first-party browser frontend, not Slack. It cannot
produce a Slack signature (the signing secret is server-side; embedding
it in the React bundle would expose it). C1 (ddee9f5) correctly hardened
/slack/interactions to require a valid signature, which broke the
browser's Generate Briefing button.

This router exposes POST /api/demo/generate-briefing — a first-party
trigger that reuses the same trigger_dossier_generation service the
Slack handler uses, without requiring a Slack signature.

The endpoint resolves the prospect's batch authoritatively from the
prospect record (the client doesn't get to assert which batch a
prospect belongs to) and rejects anything that isn't a demo-context
batch. A production deployment would gate this behind real auth
(session cookie, JWT, etc.).
"""
from typing import Annotated

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import text

from ..deps import CeleryDep, RedisDep, SessionDep
from ..services.dossier_trigger import trigger_dossier_generation
from packages.schemas.dossier import DossierAck

router = APIRouter(prefix="/api/demo")

# Batches whose user_id is one of these are considered demo-context and
# may be triggered via this endpoint. demo-prebake is the quickdemo
# pre-baked batch; demo_user is the placeholder user_id used by the
# "Run Demo" CSV-ingest flow in Phase 1.7 (no real auth yet).
DEMO_ALLOWED_USER_IDS = ("demo-prebake", "demo_user")


class DemoBriefingRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prospect_id: Annotated[str, Field(min_length=1, max_length=64)]


@router.post("/generate-briefing", response_model=DossierAck)
async def demo_generate_briefing(
    req: DemoBriefingRequest,
    session: SessionDep,
    redis: RedisDep,
    celery: CeleryDep,
) -> DossierAck:
    """Trigger dossier generation from the first-party demo UI.

    Server-authoritative: looks up the prospect by id, resolves its
    batch, and rejects if the batch isn't a demo-context batch. The
    client never gets to assert which batch a prospect belongs to.
    """
    row = (
        await session.execute(
            text(
                "SELECT b.user_id "
                "FROM lead_prospects p "
                "JOIN ingest_batches b ON b.id = p.batch_id "
                "WHERE p.id = :pid"
            ),
            {"pid": req.prospect_id},
        )
    ).first()
    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"prospect {req.prospect_id} not found",
        )
    if row[0] not in DEMO_ALLOWED_USER_IDS:
        raise HTTPException(
            status_code=403,
            detail="demo generation is only available for demo-context batches",
        )

    return await trigger_dossier_generation(
        prospect_id=req.prospect_id,
        session=session,
        redis=redis,
        celery=celery,
    )
