from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Annotated
from packages.schemas.defect_hypothesis import LikelyDefectClassHypothesis

class CalibrationTable(BaseModel):
    model_config = ConfigDict(extra="forbid")
    calibration_version: str
    alpha: Annotated[float, Field(ge=0.0, le=1.0)]
    coverage_target: Annotated[float, Field(ge=0.0, le=1.0)]
    nonconformity_thresholds_by_class: dict[str, float]
    built_at: datetime
    holdout_size: int
    seed: int

def compute_conformal_set(
    ensemble_outputs: list[LikelyDefectClassHypothesis],
    calibration: CalibrationTable,
) -> tuple[list[str], float]:
    """
    Given N=3 ensemble outputs and the calibrated table, return (conformal_set, coverage).
    """
    if not ensemble_outputs:
        return [], 0.0

    vote_counts = {}
    total = len(ensemble_outputs)
    
    for sample in ensemble_outputs:
        for defect in sample.conformal_set:
            vote_counts[defect] = vote_counts.get(defect, 0) + 1
            
    conformal_set = []
    for defect, count in vote_counts.items():
        share = count / total
        threshold = calibration.nonconformity_thresholds_by_class.get(defect, 1.0)
        if share >= (1.0 - threshold):
            conformal_set.append(defect)
            
    if not conformal_set or len(conformal_set) == 8: # 8 is the total classes
        return conformal_set, 0.0
        
    return conformal_set, calibration.coverage_target
