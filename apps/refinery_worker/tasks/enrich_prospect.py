"""Real enrichment fan-out — three adapters in sequence, each result
persisted as an enrichment_artifacts row via upsert.

Status semantics on lead_prospects.enrichment_status:
- 'complete' : all three adapters returned 'fetched' OR 'not_applicable'
- 'partial'  : at least one 'fetched' AND at least one 'failed' or 'fallback_empty'
- 'failed'   : nothing 'fetched' at all (only failures + empties)
"""
import logging
from datetime import datetime, timezone

from sqlalchemy import create_engine, text

from ..app import app
from apps.refinery_api.config import settings
from packages.enrichment.companies_house import CompaniesHouseAdapter
from packages.enrichment.web_scraper import WebScraperAdapter
from packages.enrichment.tavily_news import TavilyNewsAdapter

logger = logging.getLogger(__name__)


def _upsert_artifact(conn, prospect_id, source, status, payload, fallback_reason):
    """Idempotent upsert per (prospect_id, source) — UNIQUE constraint
    on (prospect_id, source) drives ON CONFLICT DO UPDATE."""
    payload_json = payload.model_dump_json() if payload is not None else None
    conn.execute(
        text("""
            INSERT INTO enrichment_artifacts
                (prospect_id, source, status, payload, fallback_reason, fetched_at)
            VALUES
                (:pid, :src, :status, CAST(:payload AS JSONB), :reason, :now)
            ON CONFLICT (prospect_id, source) DO UPDATE SET
                status = EXCLUDED.status,
                payload = EXCLUDED.payload,
                fallback_reason = EXCLUDED.fallback_reason,
                fetched_at = EXCLUDED.fetched_at
        """),
        {
            "pid": prospect_id,
            "src": source,
            "status": status,
            "payload": payload_json,
            "reason": fallback_reason,
            "now": datetime.now(timezone.utc),
        },
    )


@app.task(
    name="refinery.enrich_prospect",
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=3,
)
def enrich_prospect(self, prospect_id: str):
    engine = create_engine(settings.postgres_url.replace('+asyncpg', ''))

    # Load prospect context for adapter args
    with engine.connect() as conn:
        row = conn.execute(
            text("""
                SELECT company_name, contact_email, raw_notes
                FROM lead_prospects WHERE id = :pid
            """),
            {"pid": prospect_id},
        ).first()
    if row is None:
        raise ValueError(f"prospect_id {prospect_id} not found")
    company_name = row[0] or ""
    contact_email = row[1] or ""
    raw_notes = row[2] or ""

    # Fan-out — synchronous, sequential. Phase 2 could parallelize via a
    # celery chord, but sequential keeps the demo flow simple and the
    # 8-second-per-adapter ceiling means worst-case 24s end-to-end.
    fetched_count = 0
    failed_count = 0

    for source_name, adapter, args in [
        ("companies_house", CompaniesHouseAdapter(),
         (prospect_id, company_name, contact_email, raw_notes)),
        ("web_scrape", WebScraperAdapter(),
         (prospect_id, company_name, contact_email)),
        ("tavily_news", TavilyNewsAdapter(),
         (prospect_id, company_name)),
    ]:
        try:
            status, payload, fallback_reason = adapter.fetch(*args)
        except Exception as e:
            logger.exception(
                "Adapter raised unexpected exception",
                extra={
                    "prospect_id": prospect_id,
                    "source": source_name,
                    "exception_type": type(e).__name__,
                },
            )
            status = "failed"
            payload = None
            fallback_reason = f"unexpected_exception_{type(e).__name__}"

        with engine.begin() as conn:
            _upsert_artifact(
                conn, prospect_id, source_name,
                status, payload, fallback_reason,
            )

        if status == "fetched":
            fetched_count += 1
        elif status in ("failed", "fallback_empty"):
            failed_count += 1
        # 'not_applicable' counts as neither — it's expected and benign.

        logger.info(
            "Enrichment adapter completed",
            extra={
                "prospect_id": prospect_id,
                "source": source_name,
                "status": status,
                "fallback_reason": fallback_reason,
            },
        )

    # Status semantics
    if fetched_count == 0 and failed_count >= 1:
        prospect_status = "failed"
    elif fetched_count >= 1 and failed_count >= 1:
        prospect_status = "partial"
    else:
        prospect_status = "complete"

    with engine.begin() as conn:
        conn.execute(
            text("""
                UPDATE lead_prospects
                SET enrichment_status = :status
                WHERE id = :pid
            """),
            {"status": prospect_status, "pid": prospect_id},
        )

    return prospect_id
