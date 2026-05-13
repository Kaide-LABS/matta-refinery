from datetime import datetime
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from packages.schemas.lead_prospect import VERTICAL_ENUM

DEFECT_CLASS_ENUM = Literal[
    "porosity", "dimensional_drift", "surface_inclusions", "tool_wear",
    "calibration_drift", "material_defect", "process_drift", "unknown",
]

class VerticalClassification(BaseModel):
    """Per-sample output for the N=3 Stage 1.2 ensemble."""
    model_config = ConfigDict(extra="forbid")

    vertical: VERTICAL_ENUM
    rationale: Annotated[str, Field(max_length=1000)]


class LikelyDefectClassHypothesis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    conformal_set: Annotated[list[DEFECT_CLASS_ENUM], Field(min_length=0, max_length=8)]
    coverage: Annotated[float, Field(ge=0.0, le=1.0)]
    calibration_version: str
    requires_human_review: bool = False
    rationale: Annotated[str, Field(max_length=1000)]

    @model_validator(mode="after")
    def _flag_review_on_degenerate_set(self) -> "LikelyDefectClassHypothesis":
        # Empty set or all-class set → uncertainty is total → flag review.
        if len(self.conformal_set) == 0 or len(self.conformal_set) == 8:
            object.__setattr__(self, "requires_human_review", True)
        return self
