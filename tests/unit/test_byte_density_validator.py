"""Criterion 12 — Tightening 3 Goodhart-resistance.

Construct a real PreVisitDossier with caller-provided deterministic_section_ratio=0.95
but rendered_sections whose actual byte ratio is well below 0.60. The model_validator
MUST recompute from rendered_sections (overwriting the caller's value) and reject the
payload. If the validator just trusts the caller, that is the Goodhart's-Law failure mode
the spec was written to close.
"""
from datetime import datetime

import pytest
from pydantic import ValidationError

from packages.schemas.defect_hypothesis import LikelyDefectClassHypothesis
from packages.schemas.dossier import (
    ComparableDeployment,
    PreVisitDossier,
    ProcessTaxonomy,
    RiskFinding,
    RiskRegister,
    SuggestedApproach,
)


def _valid_sections():
    return {
        "process_taxonomy": ProcessTaxonomy(
            primary_process="ductile iron casting",
            sub_processes=["pour", "cool", "shake-out"],
            line_level_steps=["ladle", "pour", "demold"],
            rationale="metal casting line; verified by KG anchor",
        ),
        "defect_hypothesis": LikelyDefectClassHypothesis(
            conformal_set=["porosity", "dimensional_drift"],
            coverage=0.9,
            calibration_version="phase1-demo-v1",
            requires_human_review=False,
            rationale="N=3 ensemble plurality on porosity; conformal coverage 0.9",
        ),
        "comparable_deployment": ComparableDeployment(
            matta_customer_anchor="metal_casting_unnamed",
            citation_substrate_line=271,
            dimension_of_comparability="casting surface-finish QC stage similarity; NOT process category.",
            selection_method="deterministic_rules",
        ),
        "risk_register": RiskRegister(
            findings=[RiskFinding(category="lighting_variance", severity="identified",
                                  note="overhead pour glare anticipated on Line A")],
        ),
        "suggested_approach": SuggestedApproach(
            template="two_camera_pilot",
            rationale="2-camera pilot on highest-throughput pour line; lighting Day-1 risk.",
            day_one_risks=["lighting calibration"],
        ),
    }


def test_byte_density_validator_rejects_when_actual_ratio_below_threshold():
    """Caller LIES with deterministic_section_ratio=0.95; actual byte ratio is far below 0.60.
    The validator MUST recompute and reject."""
    sections = _valid_sections()
    rendered_sections = {
        "company_facts": "x",
        "verified_kg_anchors": "x",
        "fitness_score_rationale": "x",
        "risk_checklist_baseline": "x",
        "approach_template_baseline": "x",
        "process_taxonomy": "L" * 2000,
        "defect_hypothesis": "L" * 2000,
        "comparable_dimension_of_comparability_prose": "L" * 2000,
        "risk_register_narrative": "L" * 2000,
        "suggested_approach_narrative": "L" * 2000,
    }

    with pytest.raises(ValidationError) as exc_info:
        PreVisitDossier(
            dossier_id="d-1",
            prospect_id="p-1",
            signal_hash="sh-1",
            knowledge_graph_version="kg-1",
            calibration_version="phase1-demo-v1",
            process_taxonomy=sections["process_taxonomy"],
            defect_hypothesis=sections["defect_hypothesis"],
            comparable_deployment=sections["comparable_deployment"],
            risk_register=sections["risk_register"],
            suggested_approach=sections["suggested_approach"],
            rendered_sections=rendered_sections,
            deterministic_section_ratio=0.95,
            generated_at=datetime.utcnow(),
        )

    msg = str(exc_info.value).lower()
    assert "byte-density gate" in msg or "below threshold" in msg


def test_byte_density_validator_overwrites_caller_value_when_actual_ratio_passes():
    """Even when actual ratio passes, validator MUST overwrite a wrong caller-provided value
    (object.__setattr__ pattern). Verifies the value can never be trusted as caller-asserted."""
    sections = _valid_sections()
    rendered_sections = {
        "company_facts": "D" * 1200,
        "verified_kg_anchors": "D" * 1200,
        "fitness_score_rationale": "D" * 1200,
        "risk_checklist_baseline": "D" * 1200,
        "approach_template_baseline": "D" * 1200,
        "process_taxonomy": "L" * 400,
        "defect_hypothesis": "L" * 400,
        "comparable_dimension_of_comparability_prose": "L" * 400,
        "risk_register_narrative": "L" * 400,
        "suggested_approach_narrative": "L" * 400,
    }

    dossier = PreVisitDossier(
        dossier_id="d-2",
        prospect_id="p-2",
        signal_hash="sh-2",
        knowledge_graph_version="kg-1",
        calibration_version="phase1-demo-v1",
        process_taxonomy=sections["process_taxonomy"],
        defect_hypothesis=sections["defect_hypothesis"],
        comparable_deployment=sections["comparable_deployment"],
        risk_register=sections["risk_register"],
        suggested_approach=sections["suggested_approach"],
        rendered_sections=rendered_sections,
        deterministic_section_ratio=0.10,
        generated_at=datetime.utcnow(),
    )

    assert abs(dossier.deterministic_section_ratio - 0.75) < 0.01, \
        f"validator did not recompute; got {dossier.deterministic_section_ratio}"
