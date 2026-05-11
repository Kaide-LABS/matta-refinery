from packages.enrichment.base import EnrichmentAdapter, EnrichmentResult
from packages.schemas.lead_prospect import LeadProspect

class LinkedinSignalAdapter(EnrichmentAdapter):
    async def fetch(self, prospect: LeadProspect) -> EnrichmentResult:
        return EnrichmentResult(
            status="complete",
            data={"linkedin_signal": "mock linkedin data"}
        )
