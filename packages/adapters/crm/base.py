from typing import Protocol, Literal

class CRMAdapter(Protocol):
    provider: Literal["hubspot", "salesforce"]

    async def create_or_update_record_fields(self, object_id: str, fields: dict) -> None:
        ...

    async def append_record_note(self, object_id: str, note: str) -> None:
        ...
