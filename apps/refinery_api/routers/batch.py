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
        SELECT id, company_name, fitness_score
        FROM lead_prospects
        WHERE batch_id = :batch_id AND fitness_score IS NOT NULL
        ORDER BY fitness_score DESC
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
        fitness_score=float(row.fitness_score),
    )
