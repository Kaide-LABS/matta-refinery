"""Deterministic risk_pillar lookup for Stage 2 byte-density-rich rendering.

Maps RISK_CATEGORY_ENUM literals (packages/schemas/dossier.py:14-19) to operational
risk pillars used in the deterministic side of `risk_checklist_baseline`. Pure static
data — no LLM, no runtime computation, no external dependencies.

Also exposes a numerical severity_score mapping for the schema's severity enum.
"""
from typing import Final

RISK_PILLAR_LOOKUP: Final[dict[str, str]] = {
    "legacy_cmm_infrastructure": "infrastructure",
    "lighting_variance": "environmental",
    "emf_environment": "environmental",
    "network_topology": "infrastructure",
    "ot_it_segmentation": "infrastructure",
    "regulatory_audit_burden": "compliance",
    "operator_training_overhead": "human_factors",
    "calibration_baseline_unknown": "measurement_substrate",
}

# Numerical mapping for the severity literal — used in risk_checklist_baseline
# rendering to produce a deterministic severity_score (no LLM).
SEVERITY_SCORE_LOOKUP: Final[dict[str, float]] = {
    "identified": 1.0,
    "unknown": 0.5,
    "not_applicable": 0.0,
}

# Short deterministic evidence anchor per category (KG-line-equivalent excerpts,
# verbatim from PHASE_1_SPEC.md risk taxonomy). These are the audit-trail lines
# that back the risk classification when no LLM-emitted note is available.
RISK_KG_EVIDENCE_ANCHOR: Final[dict[str, str]] = {
    "legacy_cmm_infrastructure": "Pre-existing CMM/calibration hardware that constrains sensor placement and timing alignment.",
    "lighting_variance": "Ambient light variance on the inspection line that can confound vision-model output without normalization.",
    "emf_environment": "Induction furnaces and high-amperage motors generating EMF that interferes with sensor electronics.",
    "network_topology": "Plant network segmentation or VLAN constraints that affect real-time inference traffic routing.",
    "ot_it_segmentation": "OT/IT boundary policies that restrict where inference workloads and dashboards can run.",
    "regulatory_audit_burden": "Sector-specific audit obligations (e.g. ITAR, FDA, automotive PPAP) that compound deployment scope.",
    "operator_training_overhead": "Time-on-floor required to retrain inspectors on the new disposition workflow.",
    "calibration_baseline_unknown": "No anchored calibration substrate for this defect class — DS-CP coverage indeterminate until measured.",
}
