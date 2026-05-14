"""Stage 2 final orchestration task (PHASE_1_SPEC §E.17).

Aggregates the five section outputs, renders each to bytes, constructs `PreVisitDossier`
(which triggers Tightening 3 byte-density validator and retains Tightening 4 unverified_sections),
and writes `dossier_artifacts` row + 3 outbox envelopes (Slack/CRM/Drive) in ONE Postgres
transaction (Tightening 1 transactional outbox).

If the byte-density validator rejects (`ValidationError`), the dossier is NOT persisted;
the dossier_artifacts row is marked `rejected_byte_ratio` outside the tx; outbox is not written.
"""
import json
import uuid
from datetime import datetime

from pydantic import ValidationError
from sqlalchemy import create_engine, text

from apps.refinery_api.config import settings
from packages.schemas.dossier import (
    ComparableDeployment,
    PreVisitDossier,
    ProcessTaxonomy,
    RiskRegister,
    SuggestedApproach,
)
from packages.schemas.defect_hypothesis import LikelyDefectClassHypothesis
from ..app import app


def _render_section(value: object) -> str:
    """Stable utf-8 serialization of a section payload (Pydantic model or primitive)."""
    if hasattr(value, "model_dump_json"):
        return value.model_dump_json()
    return json.dumps(value, default=str, sort_keys=True)


@app.task(
    name="refinery.compose_dossier",
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=8,
)
def compose_dossier(self, dossier_id: str):
    engine = create_engine(settings.postgres_url.replace("+asyncpg", ""))

    # Load section outputs from the intermediate dossier_artifacts row.
    with engine.connect() as conn:
        row = conn.execute(
            text(
                "SELECT prospect_id, signal_hash, knowledge_graph_version, calibration_version, "
                "process_taxonomy, defect_hypothesis, comparable_deployment, "
                "risk_register, suggested_approach, unverified_sections "
                "FROM dossier_artifacts WHERE dossier_id = :did"
            ),
            {"did": dossier_id},
        ).first()

    if row is None:
        raise RuntimeError(f"dossier_artifacts row not found for dossier_id={dossier_id}")

    (
        prospect_id, signal_hash, kg_version, calibration_version,
        taxonomy_json, defect_json, comparable_json, risk_json, approach_json,
        unverified_sections_json,
    ) = row

    taxonomy = ProcessTaxonomy.model_validate_json(taxonomy_json)
    defect = LikelyDefectClassHypothesis.model_validate_json(defect_json)
    comparable = ComparableDeployment.model_validate_json(comparable_json)
    risk = RiskRegister.model_validate_json(risk_json)
    approach = SuggestedApproach.model_validate_json(approach_json)
    unverified_sections = json.loads(unverified_sections_json or "[]")

    rendered_sections = {
        # Deterministic-content section renders (counted toward bytes(deterministic_content)).
        "company_facts": _render_section({"prospect_id": prospect_id}),
        "verified_kg_anchors": _render_section({"anchor": comparable.matta_customer_anchor,
                                                "citation_line": comparable.citation_substrate_line}),
        "fitness_score_rationale": _render_section({"signal_hash": signal_hash}),
        "risk_checklist_baseline": _render_section([f.category for f in risk.findings]),
        "approach_template_baseline": _render_section({"template": approach.template}),
        # LLM-content section renders (counted toward bytes(total) − bytes(deterministic)).
        "process_taxonomy": _render_section(taxonomy),
        "defect_hypothesis": _render_section(defect),
        "comparable_dimension_of_comparability_prose": comparable.dimension_of_comparability,
        "risk_register_narrative": _render_section([f.note for f in risk.findings]),
        "suggested_approach_narrative": approach.rationale,
    }

    # Construct PreVisitDossier — this triggers Tightening 3 byte-density model_validator.
    # The caller-provided deterministic_section_ratio is intentionally a placeholder; the validator
    # overwrites it via object.__setattr__ from the actual rendered_sections bytes.
    try:
        dossier = PreVisitDossier(
            dossier_id=dossier_id,
            prospect_id=prospect_id,
            signal_hash=signal_hash,
            knowledge_graph_version=kg_version,
            calibration_version=calibration_version,
            process_taxonomy=taxonomy,
            defect_hypothesis=defect,
            comparable_deployment=comparable,
            risk_register=risk,
            suggested_approach=approach,
            rendered_sections=rendered_sections,
            deterministic_section_ratio=0.0,  # placeholder; validator recomputes and overwrites
            unverified_sections=unverified_sections,
            requires_human_review_sections=[
                s for s in unverified_sections
            ] + (["defect_hypothesis"] if defect.requires_human_review else []),
            generated_at=datetime.utcnow(),
        )
    except ValidationError as e:
        # Tightening 3 byte-density rejection path: mark rejected, do NOT persist outbox.
        with engine.begin() as conn:
            conn.execute(
                text(
                    "UPDATE dossier_artifacts SET state = 'rejected_byte_ratio', "
                    "validation_error = :err WHERE dossier_id = :did"
                ),
                {"err": str(e), "did": dossier_id},
            )
        return {"status": "rejected_byte_ratio", "dossier_id": dossier_id}

    # Tightening 1 Transactional Outbox: dossier row + 3 outbox envelopes commit atomically.
    with engine.begin() as conn:
        conn.execute(
            text(
                "UPDATE dossier_artifacts SET state = 'complete', "
                "deterministic_section_ratio = :ratio, "
                "unverified_sections = :unverified, "
                "generated_at = :now "
                "WHERE dossier_id = :did"
            ),
            {
                "ratio": dossier.deterministic_section_ratio,
                "unverified": json.dumps(dossier.unverified_sections),
                "now": dossier.generated_at,
                "did": dossier_id,
            },
        )
        outbox_ids = []
        for surface in ("slack_canvas", "crm_note", "drive_doc"):
            outbox_id = str(uuid.uuid4())
            outbox_ids.append(outbox_id)
            conn.execute(
                text(
                    "INSERT INTO outbox (id, surface, payload_jsonb, delivery_attempts, state, next_attempt_at) "
                    "VALUES (:id, :surf, :payload, 0, 'pending', :now)"
                ),
                {
                    "id": outbox_id,
                    "surf": surface,
                    "payload": dossier.model_dump_json(),
                    "now": datetime.utcnow(),
                },
            )

    # Cloud Tasks dispatch (out-of-tx; outbox is the source of truth either way).
    for outbox_id in outbox_ids:
        app.send_task("refinery.outbox_dispatcher", args=[outbox_id])

    return {"status": "complete", "dossier_id": dossier_id}
