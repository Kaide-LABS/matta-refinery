"""Deterministic phase-breakdown lookup for Stage 2 byte-density-rich rendering.

Maps APPROACH_TEMPLATE_ENUM literals (packages/schemas/dossier.py:21-24) to a list
of operational phase dicts. Used in `approach_template_baseline` to expand the
template enum into a Day-1-actionable plan: phase_name, duration_days,
deliverables, evaluation_criteria, exit_criteria.

Pure static data — no LLM, no runtime computation, no external dependencies.
The content is operationally specific (what gets installed, what gets measured,
what defines success) so the dossier renders without LLM round-trips.
"""
from typing import Final


APPROACH_PHASE_BREAKDOWN: Final[dict[str, list[dict[str, object]]]] = {
    "two_camera_pilot": [
        {
            "phase_name": "kickoff_install",
            "duration_days": 5,
            "deliverables": [
                "two-camera rig mounted on agreed inspection station",
                "edge-compute box racked and powered",
                "VPN/jumphost to Matta cloud provisioned",
                "first-week shift schedule confirmed with line lead",
            ],
            "evaluation_criteria": [
                "camera framing covers full part envelope at ±2mm tolerance",
                "frame-rate stable at 30fps for 4 consecutive hours",
                "round-trip latency to inference endpoint <250ms p95",
            ],
            "exit_criteria": "rig is recording continuously and frames are landing in the inference queue with zero packet loss across one full production shift",
        },
        {
            "phase_name": "shadow_inference",
            "duration_days": 10,
            "deliverables": [
                "inference pipeline running on live frames in observe-only mode",
                "daily disposition-disagreement report (model vs. human inspector)",
                "calibration-substrate anchor file finalised for this defect class",
            ],
            "evaluation_criteria": [
                "≥10,000 inspected frames per day with valid disposition",
                "false-reject rate vs. inspector baseline measured and logged",
                "DS-CP coverage ≥0.90 sustained across the shadow window",
            ],
            "exit_criteria": "model and inspector agree on ≥85% of dispositions across the last 3 shifts with no severe-shift DS-CP alerts",
        },
        {
            "phase_name": "parallel_inspection",
            "duration_days": 14,
            "deliverables": [
                "model disposition surfaced to inspector UI alongside inspector call",
                "weekly agreement-coverage report",
                "Slack canvas + CRM note + Drive doc surfaces wired to production outbox",
            ],
            "evaluation_criteria": [
                "inspector override rate trending below 10% by end-of-window",
                "no DS-CP severe-shift events for ≥7 consecutive days",
                "scrap-rate Pareto stable (no new defect modes outside agreement set)",
            ],
            "exit_criteria": "agreement rate ≥90% and inspector pull-the-cord events attributable to model error <1/week",
        },
        {
            "phase_name": "handoff_acceptance",
            "duration_days": 5,
            "deliverables": [
                "production runbook signed by line lead and quality manager",
                "on-call rotation for Matta SRE established",
                "calibration-substrate hash recorded in customer dossier",
                "final deployment-readiness review with Damjan or designated executive sponsor",
            ],
            "evaluation_criteria": [
                "runbook covers shift-handover, escalation, calibration-drift triggers",
                "customer sign-off on dispositional authority boundaries",
            ],
            "exit_criteria": "customer approves Matta call-of-record on the inspection station and pilot is converted to multi-station deployment scope",
        },
    ],
    "four_camera_pilot": [
        {
            "phase_name": "kickoff_install",
            "duration_days": 7,
            "deliverables": [
                "four-camera rig with synchronised triggering",
                "edge-compute capacity sized for 4-stream throughput",
                "multi-angle framing review with line lead",
            ],
            "evaluation_criteria": [
                "all four cameras frame-locked within 5ms drift",
                "aggregate frame-rate stable across 4 streams",
            ],
            "exit_criteria": "all 4 streams recording and landing in inference queue with zero packet loss across one shift",
        },
        {
            "phase_name": "shadow_inference",
            "duration_days": 14,
            "deliverables": [
                "4-stream inference pipeline in observe-only mode",
                "per-camera disposition-disagreement report",
                "multi-view calibration-substrate anchor finalised",
            ],
            "evaluation_criteria": [
                "≥30,000 inspected frames per day across 4 cameras",
                "cross-camera disposition consistency ≥0.85",
                "DS-CP coverage ≥0.90 per-camera",
            ],
            "exit_criteria": "all 4 streams meet shadow targets concurrently for 3 shifts",
        },
        {
            "phase_name": "parallel_inspection",
            "duration_days": 21,
            "deliverables": [
                "consolidated disposition (4-stream majority vote) to inspector UI",
                "weekly cross-camera agreement report",
                "production outbox to Slack/CRM/Drive at consolidated-disposition granularity",
            ],
            "evaluation_criteria": [
                "inspector override rate <8% on consolidated disposition",
                "no DS-CP severe-shift for ≥10 consecutive days",
            ],
            "exit_criteria": "consolidated agreement ≥92% across the 21-day window",
        },
        {
            "phase_name": "handoff_acceptance",
            "duration_days": 7,
            "deliverables": [
                "4-camera production runbook",
                "Matta SRE rotation with camera-specific escalation routing",
                "executive review with customer ops + quality sponsorship",
            ],
            "evaluation_criteria": [
                "runbook covers per-camera failure modes",
                "customer sign-off on multi-view dispositional authority",
            ],
            "exit_criteria": "customer approves Matta call-of-record on the 4-camera station and pilot converts to full-line deployment scope",
        },
    ],
    "full_line_deployment": [
        {
            "phase_name": "site_survey_and_design",
            "duration_days": 10,
            "deliverables": [
                "full-line camera placement plan",
                "edge-compute racking + network capacity plan",
                "OT/IT segmentation review with customer infra team",
            ],
            "evaluation_criteria": [
                "every inspection station has documented camera placement and framing",
                "network capacity plan validated with customer netops",
            ],
            "exit_criteria": "customer infra and ops sign off on the deployment plan",
        },
        {
            "phase_name": "staged_install",
            "duration_days": 21,
            "deliverables": [
                "stations installed in two waves",
                "wave-1 stations brought up to shadow-inference parity",
                "calibration-substrate anchors finalised for every station's defect classes",
            ],
            "evaluation_criteria": [
                "wave-1 stations meeting individual shadow targets before wave-2 install begins",
                "no production-line downtime attributable to install",
            ],
            "exit_criteria": "all stations recording continuously and in shadow-inference mode",
        },
        {
            "phase_name": "production_validation",
            "duration_days": 28,
            "deliverables": [
                "production parallel-inspection across all stations",
                "weekly line-level agreement-coverage report",
                "automated outbox to Slack/CRM/Drive at line granularity",
            ],
            "evaluation_criteria": [
                "line-aggregate inspector override rate <8%",
                "no DS-CP severe-shift events line-wide for ≥14 consecutive days",
                "scrap-rate improvement vs. baseline measured and signed off",
            ],
            "exit_criteria": "line-aggregate agreement ≥90% across the 28-day window",
        },
        {
            "phase_name": "handoff_acceptance",
            "duration_days": 14,
            "deliverables": [
                "line-wide production runbook",
                "24/7 Matta SRE rotation",
                "executive sponsorship review with both ops and quality leadership",
            ],
            "evaluation_criteria": [
                "runbook covers all station failure modes and cross-station correlation alerts",
                "customer sign-off on Matta call-of-record at line granularity",
            ],
            "exit_criteria": "customer accepts full-line Matta authority and the deployment converts to multi-line scope",
        },
    ],
    "caracol_am_oem_partnership": [
        {
            "phase_name": "joint_design_review",
            "duration_days": 14,
            "deliverables": [
                "OEM design alignment on print-head observation geometry",
                "joint calibration-substrate definition for AM defect classes",
                "shared IP and commercial framework executed",
            ],
            "evaluation_criteria": [
                "OEM and Matta engineering sign off on observation geometry",
                "calibration substrate documented in joint repository",
            ],
            "exit_criteria": "joint engineering team has a shared design-of-record for the integration",
        },
        {
            "phase_name": "prototype_integration",
            "duration_days": 21,
            "deliverables": [
                "Matta inference integrated into a Caracol AM print cell",
                "in-process layer-by-layer disposition feed to OEM controller",
                "calibration-substrate hash recorded for the AM defect class",
            ],
            "evaluation_criteria": [
                "inference round-trip latency compatible with print-speed",
                "disposition coverage ≥0.85 across pilot prints",
            ],
            "exit_criteria": "prototype prints completed with closed-loop Matta dispositions",
        },
        {
            "phase_name": "field_validation",
            "duration_days": 30,
            "deliverables": [
                "deployment at 2-3 OEM end-customer sites",
                "field disposition-disagreement reports",
                "joint customer-facing reference documentation",
            ],
            "evaluation_criteria": [
                "field sites meet individual agreement targets",
                "no DS-CP severe-shift events at any field site for ≥14 consecutive days",
            ],
            "exit_criteria": "OEM and field-customers accept Matta as the in-process inspection authority for AM cells",
        },
        {
            "phase_name": "commercial_launch_prep",
            "duration_days": 14,
            "deliverables": [
                "joint go-to-market plan",
                "OEM-bundled SKU defined",
                "joint executive sponsorship review",
            ],
            "evaluation_criteria": [
                "commercial bundle priced and quoted to at least one mutual prospect",
                "joint support model documented",
            ],
            "exit_criteria": "first commercially bundled order placed by an OEM end-customer",
        },
    ],
}
