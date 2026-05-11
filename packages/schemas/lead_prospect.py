from datetime import datetime
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

VERTICAL_ENUM = Literal[
    "polymer_extrusion", "metal_casting", "additive_manufacturing",
    "fnb_bottling", "electronics_assembly", "aerospace",
    "out_of_vertical", "vertical_uncertain",
]

class LeadProspect(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    external_lead_id: str
    source_system: Literal["hubspot", "salesforce", "csv_upload", "slack_upload"]
    company_name: Annotated[str, Field(max_length=256)]
    vertical: VERTICAL_ENUM
    factory_size_band: Literal["small", "medium", "large", "unknown"]
    trade_show_provenance: bool
    fitness_score: Annotated[float, Field(ge=0.0, le=1.0)]
    enrichment_status: Literal["complete", "partial", "failed"]
    signal_hash: str
    last_scored_at: datetime
    requires_human_review: bool = False


class PrioritizedQueueEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prospect_id: str
    rank: Annotated[int, Field(ge=1)]
    fitness_score: Annotated[float, Field(ge=0.0, le=1.0)]
    vertical: VERTICAL_ENUM
    slot_readiness: Literal["ready_for_dossier", "requires_human_review", "low_signal"]


class PrioritizedQueue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    batch_id: str
    generated_at: datetime
    entries: Annotated[list[PrioritizedQueueEntry], Field(min_length=0, max_length=2000)]
