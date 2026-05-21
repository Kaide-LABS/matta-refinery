"""Conformal prediction set computation + deferral signal extraction.

Phase 1.7 Stage C refactor: returns deferral_reason + agreement_score
alongside the conformal_set so callers can populate the new
LikelyDefectClassHypothesis deferral fields. No "unknown" sentinel in
the set — deferral is a separate signal.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field

from packages.schemas.defect_hypothesis import (
    DEFECT_CLASS_COUNT,
    DEFERRAL_REASON_ENUM,
    LikelyDefectClassHypothesis,
)


class CalibrationTable(BaseModel):
    model_config = ConfigDict(extra="forbid")
    calibration_version: str
    alpha: Annotated[float, Field(ge=0.0, le=1.0)]
    coverage_target: Annotated[float, Field(ge=0.0, le=1.0)]
    nonconformity_thresholds_by_class: dict[str, float]
    built_at: datetime
    holdout_size: int
    seed: int


@dataclass
class ConformalResult:
    """Bundles the prediction set with the orthogonal deferral signal.

    conformal_set: defect classes within the conformal-coverage band.
        Empty when the model defers entirely.
    coverage: 0.0 when degenerate (empty/full set) — reflects total
        uncertainty; coverage_target otherwise.
    requires_human_review: True when deferral_reason is set.
    deferral_reason: one of DEFERRAL_REASON_ENUM when the ensemble didn't
        reach confident consensus; None when the prediction set is usable.
    inter_model_agreement_score: max class-vote-share across the ensemble
        (1.0 = all models agreed on at least one class; ~0.33 = 3-way split).
    """
    conformal_set: list[str]
    coverage: float
    requires_human_review: bool
    deferral_reason: Optional[str]
    inter_model_agreement_score: float


# Threshold below which the ensemble is considered to have failed consensus.
# 3-of-3 agreement on the same class → 1.0. 2-of-3 → ~0.67. 1-of-3 → ~0.33.
# We require at least one class to land in >= 2 ensemble samples to consider
# the result usable; that maps to agreement >= 0.5.
INTER_MODEL_AGREEMENT_FLOOR = 0.5


def compute_conformal_set(
    ensemble_outputs: list[LikelyDefectClassHypothesis],
    calibration: CalibrationTable,
) -> ConformalResult:
    """Return ConformalResult — prediction set + orthogonal deferral signal."""
    if not ensemble_outputs:
        return ConformalResult(
            conformal_set=[],
            coverage=0.0,
            requires_human_review=True,
            deferral_reason="insufficient_calibration_data",
            inter_model_agreement_score=0.0,
        )

    vote_counts: dict[str, int] = {}
    total = len(ensemble_outputs)

    for sample in ensemble_outputs:
        for defect in sample.conformal_set:
            vote_counts[defect] = vote_counts.get(defect, 0) + 1

    # Inter-model agreement = the maximum vote-share across all classes.
    # If no class appears in any sample (empty union), agreement is 0.
    max_vote_share = max(
        (count / total for count in vote_counts.values()),
        default=0.0,
    )

    # Build the candidate conformal set from the per-class nonconformity
    # thresholds. A class enters the set if its ensemble vote-share exceeds
    # (1 - nonconformity_threshold).
    conformal_set: list[str] = []
    for defect, count in vote_counts.items():
        share = count / total
        threshold = calibration.nonconformity_thresholds_by_class.get(defect, 1.0)
        if share >= (1.0 - threshold):
            conformal_set.append(defect)

    # Deferral cases: agreement below floor (no class got majority across
    # the ensemble), or degenerate set (empty / all classes).
    if max_vote_share < INTER_MODEL_AGREEMENT_FLOOR:
        return ConformalResult(
            conformal_set=[],
            coverage=0.0,
            requires_human_review=True,
            deferral_reason="low_inter_model_agreement",
            inter_model_agreement_score=max_vote_share,
        )

    if not conformal_set or len(conformal_set) >= DEFECT_CLASS_COUNT:
        return ConformalResult(
            conformal_set=conformal_set if len(conformal_set) < DEFECT_CLASS_COUNT else [],
            coverage=0.0,
            requires_human_review=True,
            deferral_reason="low_inter_model_agreement",
            inter_model_agreement_score=max_vote_share,
        )

    return ConformalResult(
        conformal_set=conformal_set,
        coverage=calibration.coverage_target,
        requires_human_review=False,
        deferral_reason=None,
        inter_model_agreement_score=max_vote_share,
    )
