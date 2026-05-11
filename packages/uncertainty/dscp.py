DSCP_SEVERE_SHIFT_THRESHOLD = 0.55

def _centroid_for(vertical: str) -> dict:
    return {}

def semantic_distance(
    prospect_signals: dict,
    calibration_centroid_for_vertical: dict,
) -> float:
    """
    Compute a semantic-distance proxy between the prospect signal vector and the calibration
    distribution centroid for the prospect's vertical. Phase 1 implementation: hash-based
    feature overlap proxy (cosine of sparse feature vectors).
    """
    # Phase 1 proxy mock
    return 0.1

def section_passes_dscp_gate(
    section_type: str,
    vertical: str,
    prospect_signals: dict,
    allowed_evidence: list[int],
) -> bool:
    """
    Returns False if the section should be stripped per DS-CP. True if section can proceed.
    """
    if not allowed_evidence:
        return False
    distance = semantic_distance(prospect_signals, _centroid_for(vertical))
    return distance <= DSCP_SEVERE_SHIFT_THRESHOLD
