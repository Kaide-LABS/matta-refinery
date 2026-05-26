"""Criterion 15 — Section-granular DS-CP (Tightening 4).

When a section's allowed_evidence whitelist is empty for the prospect's vertical sub-path,
that section MUST be marked `UNVERIFIED_INSUFFICIENT_DATA` and stripped via PreVisitDossier.
unverified_sections rather than blocking the entire dossier.

The two failure modes this test catches:
1. compute_allowed_evidence returns a non-empty list for a vertical that has no KG anchor.
   (Would let the LLM generate against zero evidence and pass validation.)
2. PreVisitDossier rejects payloads with non-empty unverified_sections.
   (Would force whole-dossier human review instead of section-level handling.)
"""
from datetime import datetime

from packages.knowledge_graph.evidence import compute_allowed_evidence
from packages.schemas.defect_hypothesis import LikelyDefectClassHypothesis
from packages.schemas.dossier import (
    ComparableDeployment,
    PreVisitDossier,
    ProcessTaxonomy,
    RiskFinding,
    RiskRegister,
    SuggestedApproach,
)


def test_compute_allowed_evidence_returns_empty_for_vertical_without_anchor():
    """`vertical_uncertain` and `out_of_vertical` have no KG anchors — must return []."""
    for vertical in ("vertical_uncertain", "out_of_vertical"):
        evidence = compute_allowed_evidence(vertical, "defect_hypothesis", prospect_signals={})
        assert evidence == [], (
            f"vertical={vertical} has no KG anchor; compute_allowed_evidence must return []. "
            f"Got {evidence}. This is the DS-CP strip trigger."
        )


def test_compute_allowed_evidence_returns_lines_for_anchored_vertical():
    """Sanity: an anchored vertical (electronics_assembly → B&W) returns its substrate lines."""
    evidence = compute_allowed_evidence("electronics_assembly", "defect_hypothesis", prospect_signals={})
    assert evidence, "electronics_assembly has the Bowers & Wilkins anchor; evidence must be non-empty"
    assert 540 in evidence or 600 in evidence or 83 in evidence, \
        f"expected B&W citation lines (83, 540, 600); got {evidence}"


def test_dossier_accepts_unverified_sections_without_rejection():
    """A dossier with `unverified_sections=['defect_hypothesis']` must construct cleanly —
    section-granular DS-CP strips the section, the rest of the dossier still ships."""
    rendered_sections = {
        "company_facts": "D" * 1200,
        "verified_kg_anchors": "D" * 1200,
        "fitness_score_rationale": "D" * 1200,
        "risk_checklist_baseline": "D" * 1200,
        "approach_template_baseline": "D" * 1200,
        "process_taxonomy": "L" * 400,
        "defect_hypothesis": "L" * 1,  # stripped section renders as minimal stub
        "comparable_dimension_of_comparability_prose": "L" * 400,
        "risk_register_narrative": "L" * 400,
        "suggested_approach_narrative": "L" * 400,
    }
    # Stripped defect section stub — empty agreement_set + requires_human_review=True
    stripped_defect = LikelyDefectClassHypothesis(
        agreement_set=[],
        coverage=0.0,
        calibration_version="phase1-demo-v1",
        requires_human_review=True,
        rationale="DS-CP severe shift / no anchor data",
    )

    dossier = PreVisitDossier(
        dossier_id="d-strip",
        prospect_id="p-strip",
        signal_hash="sh-strip",
        knowledge_graph_version="kg-1",
        calibration_version="phase1-demo-v1",
        process_taxonomy=ProcessTaxonomy(
            primary_process="aerospace composites layup",
            sub_processes=["layup"], line_level_steps=["cure"],
            rationale="aerospace sub-path with no anchor",
        ),
        defect_hypothesis=stripped_defect,
        comparable_deployment=ComparableDeployment(
            matta_customer_anchor="no_comparable_available",
            citation_substrate_line=1,
            dimension_of_comparability="no anchor",
            selection_method="no_comparable_available",
        ),
        risk_register=RiskRegister(
            findings=[RiskFinding(category="calibration_baseline_unknown", severity="unknown", note="n/a")],
        ),
        suggested_approach=SuggestedApproach(
            template="two_camera_pilot",
            rationale="default template; section stripped due to DS-CP shift",
            day_one_risks=["calibration unknown"],
        ),
        rendered_sections=rendered_sections,
        deterministic_section_ratio=0.0,  # will be overwritten
        unverified_sections=["defect_hypothesis"],  # Tightening 4 strip outcome
        generated_at=datetime.utcnow(),
    )

    assert dossier.unverified_sections == ["defect_hypothesis"]
    assert dossier.deterministic_section_ratio >= 0.60
