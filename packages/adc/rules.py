from typing import Literal, Union, Any
from packages.schemas.lead_intake import LeadIntakeBatch
from packages.schemas.slack_ingress import SlackEventPayload
from packages.schemas.crm import CRMLeadSignal
from packages.schemas.dossier import DossierRequest

EnvelopeType = Union[LeadIntakeBatch, SlackEventPayload, CRMLeadSignal, DossierRequest, Any]
Route = Literal["PRIORITIZATION", "DOSSIER_STUB", "DOSSIER_FULL", "HUMAN_REVIEW"]

def route_request(envelope: EnvelopeType) -> Route:
    """
    Deterministic two-route ADC. LLM never routes.
    """
    if isinstance(envelope, LeadIntakeBatch):
        return "PRIORITIZATION"
    elif isinstance(envelope, SlackEventPayload):
        return "PRIORITIZATION"
    elif isinstance(envelope, CRMLeadSignal):
        return "PRIORITIZATION"
    elif isinstance(envelope, DossierRequest):
        return "DOSSIER_FULL"
    return "HUMAN_REVIEW"
