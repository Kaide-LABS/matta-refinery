"""Ensemble agreement-set computation + deferral signal extraction.

This is ensemble vote-share thresholding with per-class calibrated
thresholds — NOT split-conformal prediction (Vovk/Shafer). There is no
nonconformity score and no marginal coverage guarantee. The mechanism
is honest about what it does: when the N=3 ensemble's vote-share on a
defect class meets a per-class threshold, the class enters the
agreement set; below the inter-model agreement floor the section
defers to human review.

Renamed from conformal.py in Stage E audit remediation. See
docs/CALIBRATION.md (Stage F) for full methodology and known
limitations.
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
    agreement_target: Annotated[float, Field(ge=0.0, le=1.0)]
    per_class_agreement_thresholds: dict[str, float]
    built_at: datetime
    holdout_size: int
    seed: int


@dataclass
class AgreementResult:
    """Bundles the agreement set with the orthogonal deferral signal.

    agreement_set: defect classes whose ensemble vote-share meets the
        per-class threshold. Empty when the model defers entirely.
    coverage: 0.0 when degenerate (empty/full set) — reflects total
        uncertainty; agreement_target otherwise.
    requires_human_review: True when deferral_reason is set.
    deferral_reason: one of DEFERRAL_REASON_ENUM when the ensemble didn't
        reach confident consensus; None when the agreement set is usable.
    inter_model_agreement_score: max class-vote-share across the ensemble
        (1.0 = all models agreed on at least one class; ~0.33 = 3-way split).
    """
    agreement_set: list[str]
    coverage: float
    requires_human_review: bool
    deferral_reason: Optional[str]
    inter_model_agreement_score: float


# Threshold below which the ensemble is considered to have failed consensus.
INTER_MODEL_AGREEMENT_FLOOR = 0.5


def compute_agreement_set(
    ensemble_outputs: list[LikelyDefectClassHypothesis],
    calibration: CalibrationTable,
) -> AgreementResult:
    """Return AgreementResult — agreement set + orthogonal deferral signal."""
    if not ensemble_outputs:
        return AgreementResult(
            agreement_set=[],
            coverage=0.0,
            requires_human_review=True,
            deferral_reason="insufficient_calibration_data",
            inter_model_agreement_score=0.0,
        )

    vote_counts: dict[str, int] = {}
    total = len(ensemble_outputs)

    for sample in ensemble_outputs:
        for defect in sample.agreement_set:
            vote_counts[defect] = vote_counts.get(defect, 0) + 1

    max_vote_share = max(
        (count / total for count in vote_counts.values()),
        default=0.0,
    )

    agreement_set: list[str] = []
    for defect, count in vote_counts.items():
        share = count / total
        threshold = calibration.per_class_agreement_thresholds.get(defect, 1.0)
        if share >= (1.0 - threshold):
            agreement_set.append(defect)

    if max_vote_share < INTER_MODEL_AGREEMENT_FLOOR:
        return AgreementResult(
            agreement_set=[],
            coverage=0.0,
            requires_human_review=True,
            deferral_reason="low_inter_model_agreement",
            inter_model_agreement_score=max_vote_share,
        )

    if not agreement_set or len(agreement_set) >= DEFECT_CLASS_COUNT:
        return AgreementResult(
            agreement_set=agreement_set if len(agreement_set) < DEFECT_CLASS_COUNT else [],
            coverage=0.0,
            requires_human_review=True,
            deferral_reason="low_inter_model_agreement",
            inter_model_agreement_score=max_vote_share,
        )

    return AgreementResult(
        agreement_set=agreement_set,
        coverage=calibration.agreement_target,
        requires_human_review=False,
        deferral_reason=None,
        inter_model_agreement_score=max_vote_share,
    )
