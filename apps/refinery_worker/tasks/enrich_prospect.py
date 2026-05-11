from ..app import app
from packages.enrichment.companies_house import CompaniesHouseAdapter
from packages.enrichment.web_scraper import WebScraperAdapter
from packages.enrichment.linkedin_signal import LinkedInSignalAdapter

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
    # In Phase 1 deterministic adapters
    adapters = [CompaniesHouseAdapter(), WebScraperAdapter(), LinkedInSignalAdapter()]
    status = "complete"
    for adapter in adapters:
        try:
            adapter.fetch(prospect_id)
        except Exception:
            status = "partial"
    
    from sqlalchemy import create_engine, text
    from apps.refinery_api.config import settings
    engine = create_engine(settings.postgres_url.replace('+asyncpg', ''))
    with engine.begin() as conn:
        conn.execute(text("UPDATE lead_prospects SET enrichment_status = :status WHERE id = :pid"), {"status": status, "pid": prospect_id})
    
    return prospect_id
