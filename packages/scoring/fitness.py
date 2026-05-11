from packages.schemas.lead_prospect import LeadProspect
from typing import Any
from packages.scoring.weights import (
    VERTICAL_MATCH_WEIGHT,
    SIZE_BAND_WEIGHT,
    TRADE_SHOW_PROVENANCE_WEIGHT,
    CAPACITY_DECAY_WEIGHT
)

class QueueState:
    capacity_decay: float

def compute_fitness(prospect: LeadProspect, queue_state: Any) -> float:
    """
    Stage 1.3 deterministic fitness scoring. No LLM.
    """
    score = 0.0
    
    if prospect.vertical not in ("out_of_vertical", "vertical_uncertain"):
        score += VERTICAL_MATCH_WEIGHT
        
    if prospect.factory_size_band in ("medium", "large"):
        score += SIZE_BAND_WEIGHT
        
    if prospect.trade_show_provenance:
        score += TRADE_SHOW_PROVENANCE_WEIGHT
        
    capacity_decay = getattr(queue_state, "capacity_decay", 0.0)
    score += CAPACITY_DECAY_WEIGHT * (1.0 - capacity_decay)
    
    return min(1.0, max(0.0, score))
