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
from packages.knowledge_graph.loader import load_graph
from packages.scoring.weights import (
    VERTICAL_MATCH_WEIGHT,
    SIZE_BAND_WEIGHT,
    TRADE_SHOW_PROVENANCE_WEIGHT,
    CAPACITY_DECAY_WEIGHT,
)
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

    # JSONB columns deserialize to Python dicts via SQLAlchemy, not raw JSON strings,
    # so use model_validate(dict) not model_validate_json(str). Section tasks wrote
    # via taxonomy.model_dump_json() → Postgres parsed to JSONB → SELECT returns dict.
    def _load(model_cls, raw):
        if isinstance(raw, (str, bytes, bytearray)):
            return model_cls.model_validate_json(raw)
        return model_cls.model_validate(raw)

    taxonomy = _load(ProcessTaxonomy, taxonomy_json)
    defect = _load(LikelyDefectClassHypothesis, defect_json)
    comparable = _load(ComparableDeployment, comparable_json)
    risk = _load(RiskRegister, risk_json)
    approach = _load(SuggestedApproach, approach_json)
    if isinstance(unverified_sections_json, list):
        unverified_sections = unverified_sections_json
    else:
        unverified_sections = json.loads(unverified_sections_json or "[]")

    # Pull verified company facts from lead_prospects (one extra SELECT, reuses engine).
    with engine.connect() as conn:
        lp_row = conn.execute(
            text(
                "SELECT company_name, vertical, factory_size_band, trade_show_provenance, "
                "contact_email, contact_name, sector_hint, source_system, external_lead_id, "
                "raw_notes, fitness_score "
                "FROM lead_prospects WHERE id = :pid"
            ),
            {"pid": prospect_id},
        ).first()

    if lp_row is None:
        raise RuntimeError(f"lead_prospects row not found for prospect_id={prospect_id}")
    (
        lp_company_name, lp_vertical, lp_size_band, lp_trade_show,
        lp_contact_email, lp_contact_name, lp_sector_hint, lp_source_system,
        lp_external_lead_id, lp_raw_notes, lp_fitness_score,
    ) = lp_row
    lp_fitness_score = float(lp_fitness_score or 0.0)

    # KG anchor lookup for verified_kg_anchors enrichment.
    kg_anchor_obj = None
    if comparable.matta_customer_anchor != "no_comparable_available":
        kg = load_graph()
        # graph.json carries the "matta_deployment_" prefix; schema enum strips it.
        prefixed_id = f"matta_deployment_{comparable.matta_customer_anchor}"
        for a in kg.anchors:
            if a.anchor_id == prefixed_id:
                kg_anchor_obj = a
                break

    # Deterministic fitness-score breakdown — pure math from packages/scoring/weights.py.
    fitness_components = {
        "vertical_match": (
            VERTICAL_MATCH_WEIGHT if lp_vertical not in ("out_of_vertical", "vertical_uncertain") else 0.0
        ),
        "size_band": (SIZE_BAND_WEIGHT if lp_size_band in ("medium", "large") else 0.0),
        "trade_show_provenance": (TRADE_SHOW_PROVENANCE_WEIGHT if lp_trade_show else 0.0),
        "capacity_decay_max": CAPACITY_DECAY_WEIGHT,
    }
    fitness_score_breakdown = {
        "fitness_score": lp_fitness_score,
        "vertical": lp_vertical,
        "factory_size_band": lp_size_band,
        "trade_show_provenance": bool(lp_trade_show),
        "weights_applied": fitness_components,
        "weights_definitions": {
            "vertical_match": VERTICAL_MATCH_WEIGHT,
            "size_band": SIZE_BAND_WEIGHT,
            "trade_show_provenance": TRADE_SHOW_PROVENANCE_WEIGHT,
            "capacity_decay": CAPACITY_DECAY_WEIGHT,
        },
        "computation": (
            "score = vertical_match(0.40 if vertical in {electronics_assembly, additive_manufacturing, "
            "fnb_bottling, polymer_extrusion, metal_casting}) + size_band(0.25 if medium|large) + "
            "trade_show_provenance(0.20 if true) + capacity_decay(0.15 * (1 - decay)); clipped to [0, 1]"
        ),
        "signal_hash": signal_hash,
    }

    # Render deterministic-side payloads.
    company_facts_payload = {
        "company_name": lp_company_name or "",
        "vertical": lp_vertical or "vertical_uncertain",
        "factory_size_band": lp_size_band or "unknown",
        "trade_show_provenance": str(bool(lp_trade_show)),
        "contact_email": lp_contact_email or "",
        "contact_name": lp_contact_name or "",
        "sector_hint": lp_sector_hint or "",
        "source_system": lp_source_system or "",
        "external_lead_id": lp_external_lead_id or "",
        "raw_notes": (lp_raw_notes or "")[:400],
    }

    verified_kg_anchors_payload = {
        "matta_customer_anchor": comparable.matta_customer_anchor,
        "selection_method": comparable.selection_method,
        "citation_substrate_line": comparable.citation_substrate_line,
    }
    if kg_anchor_obj is not None:
        verified_kg_anchors_payload.update({
            "anchor_id": kg_anchor_obj.anchor_id,
            "deployment_type": kg_anchor_obj.deployment_type,
            "citation_substrate_lines": list(kg_anchor_obj.citation_substrate_lines),
            "citation_verbatim_excerpt": kg_anchor_obj.citation_verbatim_excerpt,
            "permitted_dimensions_of_comparability": list(kg_anchor_obj.permitted_dimensions_of_comparability),
            "knowledge_graph_version": kg_version,
        })

    # Full RiskFinding entries minus the `note` field (the prose lives on the LLM side).
    risk_checklist_baseline_payload = [
        {"category": f.category, "severity": f.severity}
        for f in risk.findings
    ]

    # SuggestedApproach structural fields minus the rationale prose (LLM-side).
    approach_template_baseline_payload = {
        "template": approach.template,
        "day_one_risks": list(approach.day_one_risks),
    }

    rendered_sections = {
        # Deterministic-content section renders (counted toward bytes(deterministic_content)).
        "company_facts": _render_section(company_facts_payload),
        "verified_kg_anchors": _render_section(verified_kg_anchors_payload),
        "fitness_score_rationale": _render_section(fitness_score_breakdown),
        "risk_checklist_baseline": _render_section(risk_checklist_baseline_payload),
        "approach_template_baseline": _render_section(approach_template_baseline_payload),
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
