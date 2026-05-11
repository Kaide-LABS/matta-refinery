from packages.adapters.crm.base import CRMAdapter
from typing import Literal
import httpx

class SalesforceAdapter(CRMAdapter):
    provider: Literal["salesforce"] = "salesforce"

    def __init__(self, base_url: str = "http://localhost:8091/salesforce"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def create_or_update_record_fields(self, object_id: str, fields: dict) -> None:
        resp = await self.client.patch(f"{self.base_url}/contacts/{object_id}", json=fields)
        resp.raise_for_status()

    async def append_record_note(self, object_id: str, note: str) -> None:
        resp = await self.client.post(f"{self.base_url}/contacts/{object_id}/notes", json={"note": note})
        resp.raise_for_status()
