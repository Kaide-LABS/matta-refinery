from datetime import datetime
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from packages.schemas.lead_prospect import VERTICAL_ENUM
from packages.schemas.defect_hypothesis import LikelyDefectClassHypothesis

MATTA_CUSTOMER_ANCHOR_ENUM = Literal[
    "bowers_and_wilkins", "caracol_am", "polymer_unnamed",
    "metal_casting_unnamed", "global_drinks_brand",
    "no_comparable_available",
]

RISK_CATEGORY_ENUM = Literal[
    "legacy_cmm_infrastructure", "lighting_variance",
    "emf_environment", "network_topology",
    "ot_it_segmentation", "regulatory_audit_burden",
    "operator_training_overhead", "calibration_baseline_unknown",
]

APPROACH_TEMPLATE_ENUM = Literal[
    "two_camera_pilot", "four_camera_pilot",
    "full_line_deployment", "caracol_am_oem_partnership",
]


class ProcessTaxonomy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    primary_process: Annotated[str, Field(max_length=200)]
    sub_processes: Annotated[list[str], Field(max_length=10)]
    line_level_steps: Annotated[list[str], Field(max_length=20)]
    rationale: Annotated[str, Field(max_length=600)]


class ComparableDeployment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    matta_customer_anchor: MATTA_CUSTOMER_ANCHOR_ENUM
    citation_substrate_line: Annotated[int, Field(ge=1, le=100000)]
    dimension_of_comparability: Annotated[str, Field(max_length=250)]  # Pro prose, ≤250 chars (v4 hardening)
    selection_method: Literal["deterministic_rules", "no_comparable_available"]


class RiskFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: RISK_CATEGORY_ENUM
    severity: Literal["identified", "unknown", "not_applicable"]
    note: Annotated[str, Field(max_length=300)]


class RiskRegister(BaseModel):
    model_config = ConfigDict(extra="forbid")

    findings: Annotated[list[RiskFinding], Field(min_length=1, max_length=10)]


class SuggestedApproach(BaseModel):
    model_config = ConfigDict(extra="forbid")

    template: APPROACH_TEMPLATE_ENUM
    rationale: Annotated[str, Field(max_length=600)]
    day_one_risks: Annotated[list[str], Field(max_length=8)]


DETERMINISTIC_BYTE_THRESHOLD = 0.60

DETERMINISTIC_SECTION_KEYS = frozenset({
    "company_facts",
    "verified_kg_anchors",
    "fitness_score_rationale",
    "risk_checklist_baseline",
    "approach_template_baseline",
})

LLM_SECTION_KEYS = frozenset({
    "process_taxonomy",
    "defect_hypothesis",
    "comparable_dimension_of_comparability_prose",
    "risk_register_narrative",
    "suggested_approach_narrative",
})


class PreVisitDossier(BaseModel):
    """The full Stage 2 artifact. Tightening 3 byte-density validator and Tightening 4 unverified_sections live here."""
    model_config = ConfigDict(extra="forbid")

    dossier_id: str
    prospect_id: str
    signal_hash: str
    knowledge_graph_version: str
    calibration_version: str

    process_taxonomy: ProcessTaxonomy
    defect_hypothesis: LikelyDefectClassHypothesis
    comparable_deployment: ComparableDeployment
    risk_register: RiskRegister
    suggested_approach: SuggestedApproach

    rendered_sections: dict[str, str]  # section_key -> rendered utf-8 bytes; source of truth for the recomputation

    deterministic_section_ratio: Annotated[
        float,
        Field(
            ge=0.0, le=1.0,
            description=(
                "Byte-density ratio: bytes(deterministic_content) / bytes(total_content). "
                "Recomputed inside _recompute_and_enforce_deterministic_byte_ratio model_validator "
                "from rendered_sections at validation time; caller-provided values are overwritten. "
                "Rejects payloads below DETERMINISTIC_BYTE_THRESHOLD."
            ),
        ),
    ]

    unverified_sections: Annotated[
        list[str],
        Field(
            default_factory=list,
            description=(
                "Section keys stripped from the dossier under section-granular DS-CP "
                "(Tightening 4; arXiv 2510.05566 per ULTIMATE_PRD.md §4.2). "
                "Renderers show explicit 'N sections marked unverified' note rather than silent omission."
            ),
        ),
    ]

    requires_human_review_sections: Annotated[list[str], Field(default_factory=list)]
    generated_at: datetime

    @model_validator(mode="after")
    def _recompute_and_enforce_deterministic_byte_ratio(self) -> "PreVisitDossier":
        det_bytes = sum(
            len(self.rendered_sections[k].encode("utf-8"))
            for k in DETERMINISTIC_SECTION_KEYS
            if k in self.rendered_sections
        )
        llm_bytes = sum(
            len(self.rendered_sections[k].encode("utf-8"))
            for k in LLM_SECTION_KEYS
            if k in self.rendered_sections
        )
        total = det_bytes + llm_bytes
        if total == 0:
            raise ValueError("PreVisitDossier.rendered_sections is empty")
        recomputed = det_bytes / total
        # NEVER trust the caller-provided value. Overwrite it.
        object.__setattr__(self, "deterministic_section_ratio", recomputed)
        if recomputed < DETERMINISTIC_BYTE_THRESHOLD:
            raise ValueError(
                f"deterministic_section_ratio={recomputed:.3f} is below threshold "
                f"{DETERMINISTIC_BYTE_THRESHOLD}; LLM byte volume exceeded the audit budget. "
                f"Payload rejected (Tightening 3 byte-density gate)."
            )
        return self


class DossierStub(BaseModel):
    """Stage 1.5 deterministic-only top-12 stub. Zero LLM calls in producing this."""
    model_config = ConfigDict(extra="forbid")

    stub_id: str
    prospect_id: str
    company_facts: dict[str, str]
    verified_vertical: VERTICAL_ENUM
    headline_kg_anchor: MATTA_CUSTOMER_ANCHOR_ENUM
    slot_readiness: Literal["ready_for_dossier", "requires_human_review", "low_signal"]
    generated_at: datetime


class DossierRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prospect_id: str
    force_regenerate: bool = False
    requested_surface: Literal["slack", "crm", "drive", "all"] = "all"


class DossierAck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dossier_id: str
    status: Literal["generating", "cached", "queued", "rejected"]
