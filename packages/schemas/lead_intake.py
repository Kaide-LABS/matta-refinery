from datetime import datetime
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

class LeadIntakeRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    external_lead_id: Annotated[str, Field(min_length=1, max_length=128)]
    company_name: Annotated[str, Field(min_length=1, max_length=256)]
    contact_name: Annotated[str | None, Field(max_length=128)] = None
    contact_email: Annotated[str | None, Field(max_length=256)] = None
    sector_hint: Annotated[str | None, Field(max_length=128)] = None
    factory_size_band: Literal["small", "medium", "large", "unknown"] | None = None
    raw_notes: Annotated[str | None, Field(max_length=2048)] = None
    # Phase 1.7 Stage C-prelim: explicit website URL flows through to
    # WebScraperAdapter, bypassing the unreliable derive-from-name path.
    website_url: Annotated[str | None, Field(max_length=2048)] = None

class LeadIntakeBatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    batch_id: str
    source_label: Annotated[str, Field(max_length=128)]
    source_surface: Literal["theater_csv", "slack_upload", "crm_webhook", "email_forward"]
    ingest_user: str
    ingest_timestamp: datetime
    rows: Annotated[list[LeadIntakeRow], Field(min_length=1, max_length=2000)]

class IngestAck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    batch_id: str
    status: Literal["scoring", "duplicate", "rejected"]
    row_count: Annotated[int, Field(ge=0)]
    rejection_reason: str | None = None
