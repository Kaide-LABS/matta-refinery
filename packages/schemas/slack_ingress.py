from datetime import datetime
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

class SlackEventPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str
    team_id: str
    api_app_id: str
    event: dict  # untyped passthrough; the handler narrows on event.type
    type: Literal["event_callback", "url_verification"]
    challenge: str | None = None  # for url_verification handshake


class SlackLeadBatchIngress(BaseModel):
    model_config = ConfigDict(extra="forbid")

    slack_event_id: str
    workspace_id: str
    channel_id: str
    user_id: str
    source_label: Annotated[str, Field(max_length=128)]
    file_sha256: str | None = None
    raw_text: Annotated[str | None, Field(max_length=4000)] = None


class SlackDossierAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action_id: Literal["generate_full_dossier"]
    prospect_id: str
    signal_hash: str
    slack_response_url: str  # ephemeral response URL Slack provides


class SlackEventAck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["accepted", "duplicate", "duplicate_in_flight"]
    event_id: str
