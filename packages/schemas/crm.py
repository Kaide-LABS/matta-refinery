from datetime import datetime
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from packages.schemas.lead_prospect import VERTICAL_ENUM

class CRMLeadSignal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: Literal["hubspot", "salesforce"]
    object_type: Literal["lead", "contact", "account"]
    object_id: str
    updated_at: datetime
    changed_fields: dict[str, str | int | float | None]
    source_label: str | None = None


class CRMWritebackEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    object_id: str
    fit_score: Annotated[float, Field(ge=0.0, le=1.0)]
    vertical: VERTICAL_ENUM
    slot_readiness: Literal["ready_for_dossier", "requires_human_review", "low_signal"]
    dossier_url: str | None = None
    requires_human_review: bool


class CRMWebhookAck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["accepted", "duplicate"]


class CRMDossierActionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: Literal["hubspot", "salesforce"]
    crm_object_id: str
