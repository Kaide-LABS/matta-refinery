"""Batch-status endpoints — read-only lookups against lead_prospects.

Added in Phase 1.6 follow-on so the Theater UI can resolve the rank-1
tracer prospect per batch after Stage 1 fitness scoring completes. The
front-end calls GET /api/batch/{batch_id}/top_prospect post-M3 to
populate the click-trigger payload with whichever prospect the engine
actually ranked first for the currently-active CSV.

Pydantic boundary count: this module adds one new BaseModel
(TopProspectResponse) — additive, not a mutation of any existing
schema. Total Pydantic-bounded boundaries across packages/schemas/
plus this module goes from 28 to 29.
"""

from typing import Annotated
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import text
from ..deps import SessionDep

router = APIRouter()


class TopProspectResponse(BaseModel):
    """Rank-1 prospect for a given ingest batch, after Stage 1 fitness
    scoring has populated the lead_prospects.fitness_score column."""

    model_config = ConfigDict(extra="forbid")

    prospect_id: Annotated[str, Field(min_length=1, max_length=64)]
    company_name: Annotated[str, Field(min_length=1, max_length=256)]
    fitness_score: Annotated[float, Field(ge=0.0, le=1.0)]
    # Phase 1.7 Stage D hotfix: vertical surfaced here so the dossier UI's
    # CRM strip and §1 caveat box can render the prospect's actual vertical
    # instead of the hardcoded "metal_casting" placeholder that leaked
    # through from Stage A scaffolding.
    vertical: Annotated[str, Field(max_length=64)] = "unknown"


@router.get(
    "/api/batch/{batch_id}/top_prospect",
    response_model=TopProspectResponse,
    status_code=status.HTTP_200_OK,
)
async def get_top_prospect(batch_id: str, session: SessionDep) -> TopProspectResponse:
    """Returns the rank-1 prospect for a batch, ordered by fitness_score DESC.

    Returns 404 if no prospect with a non-null fitness_score exists yet
    (Stage 1 still in flight). The Theater UI front-end is expected to
    retry once after a brief delay before falling back to a graceful
    'Awaiting ranking...' state.
    """
    query = text(
        """
        SELECT id, company_name, fitness_score, vertical
        FROM lead_prospects
        WHERE batch_id = :batch_id AND fitness_score IS NOT NULL
        -- Phase 1.7 Stage D hotfix: external_lead_id ASC is the
        -- deterministic tiebreaker. Without it, ties at fitness_score
        -- (5-way at 0.8 in the AI Summit cohort) resolve to whatever
        -- postgres returns first — non-portable across replicas /
        -- reorganizations. external_lead_id is stable per source CSV row.
        ORDER BY fitness_score DESC, external_lead_id ASC
        LIMIT 1
        """
    )
    result = await session.execute(query, {"batch_id": batch_id})
    row = result.first()
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No scored prospects yet for this batch — Stage 1 still in flight",
        )
    return TopProspectResponse(
        prospect_id=row.id,
        company_name=row.company_name,
        vertical=row.vertical or "unknown",
        fitness_score=float(row.fitness_score),
    )


class Top12Item(BaseModel):
    """Single ranked prospect row in the top-12 list returned to the UI.

    Phase 1.7 Stage E: every card in the Slack pane's top-12 is now
    independently clickable (was rank-1 only). The UI uses these
    authoritative prospect_ids — the hardcoded TOP_12_PROSPECTS
    placeholder in components/prospectData.ts is computed for the
    legacy uk_metals_expo_2025 CSV and won't match the current
    industrial_ai_summit_2025 cohort.
    """

    model_config = ConfigDict(extra="forbid")

    rank: Annotated[int, Field(ge=1, le=12)]
    prospect_id: Annotated[str, Field(min_length=1, max_length=64)]
    company_name: Annotated[str, Field(min_length=1, max_length=256)]
    vertical: Annotated[str, Field(max_length=64)] = "unknown"
    fitness_score: Annotated[float, Field(ge=0.0, le=1.0)]


class Top12Response(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: list[Top12Item]


@router.get(
    "/api/batch/{batch_id}/top_12",
    response_model=Top12Response,
    status_code=status.HTTP_200_OK,
)
async def get_top_12(batch_id: str, session: SessionDep) -> Top12Response:
    """Return the top-12 ranked prospects for a batch.

    Same ordering as /top_prospect (fitness_score DESC, external_lead_id
    ASC) — extended to 12 rows with explicit rank. Empty list if no
    scored prospects exist yet (Stage 1 in flight).
    """
    query = text(
        """
        SELECT id, company_name, vertical, fitness_score
        FROM lead_prospects
        WHERE batch_id = :batch_id AND fitness_score IS NOT NULL
        ORDER BY fitness_score DESC, external_lead_id ASC
        LIMIT 12
        """
    )
    result = await session.execute(query, {"batch_id": batch_id})
    rows = result.fetchall()
    items = [
        Top12Item(
            rank=i + 1,
            prospect_id=r.id,
            company_name=r.company_name,
            vertical=r.vertical or "unknown",
            fitness_score=float(r.fitness_score),
        )
        for i, r in enumerate(rows)
    ]
    return Top12Response(items=items)


class PrebakedBatchResponse(BaseModel):
    """Status of the startup pre-bake on the default demo CSV.

    Phase 1.7 Stage D: the /sandbox?mode=quickdemo URL handler polls
    this to decide whether to render the ranked queue immediately or
    show a "warming up, refresh in 30s" message.
    """

    model_config = ConfigDict(extra="forbid")

    status: Annotated[str, Field(min_length=1, max_length=32)]
    batch_id: Annotated[str | None, Field(max_length=64)] = None
    scored_count: int = 0


PREBAKE_USER_ID = "demo-prebake"
PREBAKE_COMPLETION_THRESHOLD = 60


@router.get(
    "/api/batch/prebaked",
    response_model=PrebakedBatchResponse,
    status_code=status.HTTP_200_OK,
)
async def get_prebaked_batch_status(session: SessionDep) -> PrebakedBatchResponse:
    """Return the most recent pre-baked Stage 1 batch's status.

    status values:
      - "not_started": no batch ever queued by the startup pre-bake hook
      - "warming":     batch exists but Stage 1 ranking hasn't reached
                       the completion threshold yet
      - "complete":    >=60 prospects have a fitness_score; queue is
                       ready for quickdemo render
    """
    # Stage E audit fix: select the *most populated* prebake batch, not
    # the most recent. If a TOCTOU race (now closed by advisory lock in
    # startup_prebake.py) ever produced duplicate batches in the past,
    # we still want to resolve to the populated one rather than an
    # empty wedged duplicate. Sort by scored_count DESC then created_at
    # DESC, and require >0 scored prospects to be considered.
    result = await session.execute(
        text(
            """
            SELECT b.id, COUNT(p.fitness_score) AS scored_count
            FROM ingest_batches b
            LEFT JOIN lead_prospects p ON p.batch_id = b.id
            WHERE b.user_id = :user_id
            GROUP BY b.id, b.created_at
            ORDER BY COUNT(p.fitness_score) DESC, b.created_at DESC
            LIMIT 1
            """
        ),
        {"user_id": PREBAKE_USER_ID},
    )
    row = result.first()
    if row is None:
        return PrebakedBatchResponse(status="not_started")
    scored = int(row[1] or 0)
    if scored < PREBAKE_COMPLETION_THRESHOLD:
        return PrebakedBatchResponse(
            status="warming", batch_id=row[0], scored_count=scored
        )
    return PrebakedBatchResponse(status="complete", batch_id=row[0], scored_count=scored)
