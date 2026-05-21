"""Stage D: pre-bake Stage 1 ranking on the default demo CSV at container
boot, so the quickdemo URL has a ready-to-serve queue.

Idempotent — checks if a completed Stage 1 batch already exists for the
default CSV's file_hash + user_id; only triggers ingest + dispatch if
missing. Subsequent boots reuse the existing baked batch.

The pre-bake completes asynchronously: this helper returns once the
batch + prospect rows are persisted and score_batch is queued. Stage 1
ranking itself runs over the next ~3 minutes via the worker.
"""
import hashlib
import logging
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Optional

from celery import Celery
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from packages.ingest.csv_parser import parse_csv_to_batch
from packages.models.prospects import IngestBatch, LeadProspect

logger = logging.getLogger(__name__)


DEFAULT_DEMO_CSV_PATH = Path(
    "/app/apps/theater_ui/public/seed_csvs/Industrial_AI_Summit_2025_leads.csv"
)
DEFAULT_DEMO_CSV_USER_ID = "demo-prebake"
DEFAULT_DEMO_CSV_SOURCE_LABEL = "industrial_ai_summit_2025"
# Industrial AI Summit has 65 rows; consider the bake complete when at
# least 60 have a fitness_score (handles rare Vertex retry timeouts).
PREBAKE_COMPLETION_THRESHOLD = 60


@dataclass
class _DuckUser:
    """Minimal user object for parse_csv_to_batch (expects user.id)."""
    id: str


async def maybe_prebake_default_csv(
    engine: AsyncEngine,
    celery: Celery,
) -> None:
    """Pre-bake Stage 1 on the default demo CSV if not already done.

    Safe to call on every refinery_api boot — idempotent on file_sha256
    + user_id. The first boot triggers ingest + dispatch; subsequent boots
    that find a completed batch (scored_count >= threshold) skip.
    """
    if not DEFAULT_DEMO_CSV_PATH.exists():
        logger.warning(
            "Default demo CSV not found at boot",
            extra={"path": str(DEFAULT_DEMO_CSV_PATH)},
        )
        return

    csv_bytes = DEFAULT_DEMO_CSV_PATH.read_bytes()
    file_sha256 = hashlib.sha256(csv_bytes).hexdigest()

    # Check for an existing baked batch on this file_hash + user_id.
    async with engine.connect() as conn:
        result = await conn.execute(
            text(
                """
                SELECT b.id, COUNT(p.fitness_score) AS scored_count
                FROM ingest_batches b
                LEFT JOIN lead_prospects p ON p.batch_id = b.id
                WHERE b.file_sha256 = :file_sha256
                  AND b.user_id = :user_id
                GROUP BY b.id
                ORDER BY b.created_at DESC
                LIMIT 1
                """
            ),
            {"file_sha256": file_sha256, "user_id": DEFAULT_DEMO_CSV_USER_ID},
        )
        existing = result.first()

    if existing and existing[1] >= PREBAKE_COMPLETION_THRESHOLD:
        logger.info(
            "Default demo CSV already pre-baked, skipping",
            extra={"batch_id": existing[0], "scored_count": existing[1]},
        )
        return

    # No completed bake — trigger ingest + dispatch.
    logger.info(
        "Pre-baking Stage 1 on default demo CSV",
        extra={"path": str(DEFAULT_DEMO_CSV_PATH), "file_sha256": file_sha256[:16]},
    )

    try:
        batch = parse_csv_to_batch(
            csv_bytes, DEFAULT_DEMO_CSV_SOURCE_LABEL, _DuckUser(id=DEFAULT_DEMO_CSV_USER_ID)
        )
    except Exception as e:
        logger.exception(
            "parse_csv_to_batch failed during pre-bake",
            extra={"exception_type": type(e).__name__},
        )
        return

    session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
        engine, expire_on_commit=False
    )

    try:
        async with session_maker() as session:
            db_batch = IngestBatch(
                id=batch.batch_id,
                source_surface=batch.source_surface,
                file_sha256=file_sha256,
                user_id=DEFAULT_DEMO_CSV_USER_ID,
                day=date.today(),
            )
            session.add(db_batch)
            for row in batch.rows:
                prospect_id = (
                    "pros_"
                    + hashlib.md5(
                        f"{batch.source_surface}:{row.external_lead_id}".encode()
                    ).hexdigest()[:12]
                )
                prospect = LeadProspect(
                    id=prospect_id,
                    batch_id=batch.batch_id,
                    source_system=batch.source_surface,
                    external_lead_id=row.external_lead_id,
                    company_name=row.company_name,
                    contact_name=row.contact_name,
                    contact_email=row.contact_email,
                    sector_hint=row.sector_hint,
                    raw_notes=row.raw_notes,
                    factory_size_band=row.factory_size_band or "unknown",
                    website_url=row.website_url,
                )
                await session.merge(prospect)
            await session.commit()
    except Exception as e:
        logger.exception(
            "Pre-bake INSERT failed",
            extra={"exception_type": type(e).__name__},
        )
        return

    celery.send_task("refinery.score_batch", args=[batch.batch_id])

    logger.info(
        "Pre-bake batch queued",
        extra={
            "batch_id": batch.batch_id,
            "row_count": len(batch.rows),
            "user_id": DEFAULT_DEMO_CSV_USER_ID,
        },
    )
