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


def _prebake_lock_key(file_sha256: str, user_id: str) -> int:
    """Stable 64-bit signed int for pg_advisory_xact_lock.

    Hash is intentionally deterministic across replicas so the same
    (user_id, file_sha256) pair always collapses to the same lock
    namespace.
    """
    h = hashlib.md5(f"{user_id}:{file_sha256}".encode()).digest()
    return int.from_bytes(h[:8], byteorder="big", signed=True)


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

    # Stage E audit fix: wrap existence check + insert in a single
    # transaction with a Postgres advisory lock keyed on
    # hash(user_id + file_sha256). Concurrent API replica boots
    # previously raced — both observed no existing batch and both
    # inserted, leaving the /api/batch/prebaked endpoint resolving
    # to the empty duplicate. The advisory lock serializes the
    # check-then-act across replicas; it auto-releases when the
    # transaction commits or rolls back.
    lock_key = _prebake_lock_key(file_sha256, DEFAULT_DEMO_CSV_USER_ID)

    async with engine.begin() as conn:
        await conn.execute(text("SELECT pg_advisory_xact_lock(:k)"), {"k": lock_key})

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

        if existing is not None:
            # Stage E hotfix (Bug C): skip whenever any batch already exists
            # for this file_sha256 + user_id, regardless of scored_count.
            # The advisory lock above serializes concurrent boots, but on a
            # cold start worker 2 still saw worker 1's just-inserted batch
            # with scored_count=0 (below the old threshold) and created a
            # duplicate. Scored-count gating is now solely the
            # /api/batch/prebaked endpoint's job (it orders by scored_count
            # DESC so legacy duplicates resolve to the populated one).
            logger.info(
                "Default demo CSV batch already exists; skipping re-creation",
                extra={
                    "batch_id": existing[0],
                    "scored_count": existing[1] if existing[1] is not None else 0,
                },
            )
            return

        logger.info(
            "Pre-baking Stage 1 on default demo CSV",
            extra={
                "path": str(DEFAULT_DEMO_CSV_PATH),
                "file_sha256": file_sha256[:16],
            },
        )

        try:
            batch = parse_csv_to_batch(
                csv_bytes,
                DEFAULT_DEMO_CSV_SOURCE_LABEL,
                _DuckUser(id=DEFAULT_DEMO_CSV_USER_ID),
            )
        except Exception as e:
            logger.exception(
                "parse_csv_to_batch failed during pre-bake",
                extra={"exception_type": type(e).__name__},
            )
            return

        # Build a session bound to this connection so the ORM inserts
        # participate in the same advisory-locked transaction.
        session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=conn, expire_on_commit=False, join_transaction_mode="create_savepoint",
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
                # Stage E hotfix (Bug B): session.flush() wrote to a
                # savepoint that was never released; the outer
                # engine.begin() committed empty. session.commit()
                # releases the savepoint into the outer transaction so
                # the writes actually land.
                await session.commit()
        except Exception as e:
            logger.exception(
                "Pre-bake INSERT failed",
                extra={"exception_type": type(e).__name__},
            )
            raise

    # Lock released; safe to dispatch the score_batch task.
    celery.send_task("refinery.score_batch", args=[batch.batch_id])

    logger.info(
        "Pre-bake batch queued",
        extra={
            "batch_id": batch.batch_id,
            "row_count": len(batch.rows),
            "user_id": DEFAULT_DEMO_CSV_USER_ID,
        },
    )
