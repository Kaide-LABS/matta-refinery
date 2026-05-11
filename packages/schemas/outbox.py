from datetime import datetime
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

SurfaceEnum = Literal["slack_canvas", "crm_note", "crm_field", "drive_doc"]

class OutboxEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    surface: SurfaceEnum
    payload: dict
    delivery_attempts: Annotated[int, Field(ge=0, le=6)]
    state: Literal["pending", "in_flight", "delivered", "dlq"]
    next_attempt_at: datetime
    last_error: str | None = None


class OutboxDLQEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    original_outbox_id: str
    surface: SurfaceEnum
    payload: dict
    delivery_attempts: int
    final_error: str
    failed_at: datetime
