from packages.enrichment.base import EnrichmentAdapter, EnrichmentResult
from packages.schemas.lead_prospect import LeadProspect

class WebScraperAdapter(EnrichmentAdapter):
    async def fetch(self, prospect: LeadProspect) -> EnrichmentResult:
        return EnrichmentResult(
            status="complete",
            data={"website_summary": "mock web scraped content"}
        )
