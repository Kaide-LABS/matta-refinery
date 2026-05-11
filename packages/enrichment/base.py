from abc import ABC, abstractmethod
from pydantic import BaseModel
from packages.schemas.lead_prospect import LeadProspect
from typing import Literal, Any

class EnrichmentResult(BaseModel):
    status: Literal["complete", "partial", "failed"]
    data: dict[str, Any]

class EnrichmentAdapter(ABC):
    @abstractmethod
    async def fetch(self, prospect: LeadProspect) -> EnrichmentResult:
        pass
