from datetime import datetime
from typing import Annotated, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from packages.schemas.lead_prospect import VERTICAL_ENUM

# Phase 1.7 Stage C: "unknown" REMOVED from the enum. It was used as a
# sentinel inside conformal_set, conflating prediction-set membership
# (defect classes within conformal coverage) with deferral (model
# cannot confidently classify). These are now distinct: conformal_set
# carries only real defect classes; deferral_reason + requires_human_review
# carry the deferral signal.
DEFECT_CLASS_ENUM = Literal[
    "porosity", "dimensional_drift", "surface_inclusions", "tool_wear",
    "calibration_drift", "material_defect", "process_drift",
]

# 7 defect classes total — used by conformal logic to detect "set is all
# classes" (total uncertainty) without hardcoding the count separately.
DEFECT_CLASS_COUNT = 7

DEFERRAL_REASON_ENUM = Literal[
    "low_inter_model_agreement",
    "out_of_distribution_input",
    "insufficient_calibration_data",
]


class VerticalClassification(BaseModel):
    """Per-sample output for the N=3 Stage 1.2 ensemble."""
    model_config = ConfigDict(extra="forbid")

    vertical: VERTICAL_ENUM
    rationale: Annotated[str, Field(max_length=1000)]


class LikelyDefectClassHypothesis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Real defect classes only — no "unknown" sentinel. Empty list permitted
    # when the model defers (requires_human_review=True).
    conformal_set: Annotated[list[DEFECT_CLASS_ENUM], Field(min_length=0, max_length=DEFECT_CLASS_COUNT)]
    coverage: Annotated[float, Field(ge=0.0, le=1.0)]
    calibration_version: str
    requires_human_review: bool = False
    rationale: Annotated[str, Field(max_length=1000)]

    # Phase 1.7 Stage C: explicit deferral semantics, separate from the
    # conformal prediction set. deferral_reason / agreement_score are
    # populated when the post-hoc conformal computation determines the
    # ensemble didn't reach confident consensus.
    deferral_reason: Optional[DEFERRAL_REASON_ENUM] = None
    inter_model_agreement_score: Optional[Annotated[float, Field(ge=0.0, le=1.0)]] = None
