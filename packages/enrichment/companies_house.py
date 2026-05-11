from packages.enrichment.base import EnrichmentAdapter, EnrichmentResult
from packages.schemas.lead_prospect import LeadProspect

class CompaniesHouseAdapter(EnrichmentAdapter):
    async def fetch(self, prospect: LeadProspect) -> EnrichmentResult:
        return EnrichmentResult(
            status="complete",
            data={"company_number": "mock_number", "status": "active"}
        )
