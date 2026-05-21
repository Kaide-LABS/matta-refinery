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
from packages.scoring.risk_pillars import (
    RISK_PILLAR_LOOKUP,
    SEVERITY_SCORE_LOOKUP,
    RISK_KG_EVIDENCE_ANCHOR,
)
from packages.scoring.approach_phases import APPROACH_PHASE_BREAKDOWN
from ..app import app


def _render_section(value: object) -> str:
    """Stable utf-8 serialization of a section payload (Pydantic model or primitive)."""
    if hasattr(value, "model_dump_json"):
        return value.model_dump_json()
    return json.dumps(value, default=str, sort_keys=True)


def _format_enrichment_block(payload, status, fallback_reason):
    """Render an enrichment block for the dossier. Handles all five
    status values uniformly so downstream UI can render conditionally:
    fetched | not_applicable | fallback_empty | failed | not_attempted (NULL)."""
    if status == "fetched" and payload is not None:
        # JSONB → dict via SQLAlchemy
        return {"status": "fetched", "data": payload}
    if status == "not_applicable":
        return {"status": "not_applicable", "reason": fallback_reason or "not_applicable"}
    if status == "fallback_empty":
        return {"status": "fallback_empty", "reason": fallback_reason or "no_data_returned"}
    if status == "failed":
        return {"status": "failed", "reason": fallback_reason or "fetch_failed"}
    # status is NULL — enrichment task hasn't run yet for this prospect
    return {"status": "not_attempted", "reason": "enrichment_pending_or_skipped"}


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

    # Pull verified company facts + ingest provenance + enrichment payloads.
    # Three LEFT JOINs on enrichment_artifacts (one per source) — each
    # row is NULL when the adapter hasn't run yet for this prospect.
    with engine.connect() as conn:
        lp_row = conn.execute(
            text(
                "SELECT lp.company_name, lp.vertical, lp.factory_size_band, lp.trade_show_provenance, "
                "lp.contact_email, lp.contact_name, lp.sector_hint, lp.source_system, lp.external_lead_id, "
                "lp.raw_notes, lp.fitness_score, lp.batch_id, lp.last_scored_at, "
                "lp.enrichment_status, lp.requires_human_review, "
                "ib.file_sha256, ib.user_id, ib.day, ib.created_at, ib.source_surface, "
                "lp.vertical_ensemble_outputs, "
                "ch.payload AS ch_payload, ch.status AS ch_status, ch.fallback_reason AS ch_reason, "
                "ws.payload AS ws_payload, ws.status AS ws_status, ws.fallback_reason AS ws_reason, "
                "tn.payload AS tn_payload, tn.status AS tn_status, tn.fallback_reason AS tn_reason "
                "FROM lead_prospects lp "
                "LEFT JOIN ingest_batches ib ON ib.id = lp.batch_id "
                "LEFT JOIN enrichment_artifacts ch "
                "  ON ch.prospect_id = lp.id AND ch.source = 'companies_house' "
                "LEFT JOIN enrichment_artifacts ws "
                "  ON ws.prospect_id = lp.id AND ws.source = 'web_scrape' "
                "LEFT JOIN enrichment_artifacts tn "
                "  ON tn.prospect_id = lp.id AND tn.source = 'tavily_news' "
                "WHERE lp.id = :pid"
            ),
            {"pid": prospect_id},
        ).first()

    if lp_row is None:
        raise RuntimeError(f"lead_prospects row not found for prospect_id={prospect_id}")
    (
        lp_company_name, lp_vertical, lp_size_band, lp_trade_show,
        lp_contact_email, lp_contact_name, lp_sector_hint, lp_source_system,
        lp_external_lead_id, lp_raw_notes, lp_fitness_score, lp_batch_id,
        lp_last_scored_at, lp_enrichment_status, lp_requires_human_review,
        ib_file_sha256, ib_user_id, ib_day, ib_created_at, ib_source_surface,
        lp_vertical_ensemble_outputs,
        ch_payload, ch_status, ch_reason,
        ws_payload, ws_status, ws_reason,
        tn_payload, tn_status, tn_reason,
    ) = lp_row
    lp_fitness_score = float(lp_fitness_score or 0.0)

    # KG anchor lookup for verified_kg_anchors enrichment.
    # Load full graph + find primary anchor (by matched ID) + collect peer anchors
    # in the same vertical (used in the multi-anchor comparability table below).
    kg_anchor_obj = None
    peer_anchors: list = []
    kg_loaded = None
    if comparable.matta_customer_anchor != "no_comparable_available":
        kg_loaded = load_graph()
        # graph.json carries the "matta_deployment_" prefix; schema enum strips it.
        prefixed_id = f"matta_deployment_{comparable.matta_customer_anchor}"
        for a in kg_loaded.anchors:
            if a.anchor_id == prefixed_id:
                kg_anchor_obj = a
            elif kg_anchor_obj is not None and a.vertical == kg_anchor_obj.vertical:
                peer_anchors.append(a)
        if kg_anchor_obj is not None:
            # Second pass for peers whose order put them before the matched anchor.
            peer_anchors = [
                a for a in kg_loaded.anchors
                if a.vertical == kg_anchor_obj.vertical and a.anchor_id != kg_anchor_obj.anchor_id
            ]

    # Deterministic fitness-score breakdown — pure math from packages/scoring/weights.py.
    fitness_components = {
        "vertical_match": (
            VERTICAL_MATCH_WEIGHT if lp_vertical not in ("out_of_vertical", "vertical_uncertain") else 0.0
        ),
        "size_band": (SIZE_BAND_WEIGHT if lp_size_band in ("medium", "large") else 0.0),
        "trade_show_provenance": (TRADE_SHOW_PROVENANCE_WEIGHT if lp_trade_show else 0.0),
        "capacity_decay_max": CAPACITY_DECAY_WEIGHT,
    }
    # Per-component attribution table — each row is a deterministic branch evaluation
    # of the scoring formula. No LLM; pure math from packages/scoring/weights.py + actual
    # prospect fields.
    fitness_decision_tree = [
        {
            "component": "vertical_match",
            "weight": VERTICAL_MATCH_WEIGHT,
            "predicate": "vertical NOT IN {out_of_vertical, vertical_uncertain}",
            "predicate_satisfied": lp_vertical not in ("out_of_vertical", "vertical_uncertain"),
            "input_value": lp_vertical or "",
            "contribution": (VERTICAL_MATCH_WEIGHT if lp_vertical not in ("out_of_vertical", "vertical_uncertain") else 0.0),
        },
        {
            "component": "size_band",
            "weight": SIZE_BAND_WEIGHT,
            "predicate": "factory_size_band IN {medium, large}",
            "predicate_satisfied": lp_size_band in ("medium", "large"),
            "input_value": lp_size_band or "",
            "contribution": (SIZE_BAND_WEIGHT if lp_size_band in ("medium", "large") else 0.0),
        },
        {
            "component": "trade_show_provenance",
            "weight": TRADE_SHOW_PROVENANCE_WEIGHT,
            "predicate": "trade_show_provenance IS TRUE",
            "predicate_satisfied": bool(lp_trade_show),
            "input_value": str(bool(lp_trade_show)),
            "contribution": (TRADE_SHOW_PROVENANCE_WEIGHT if lp_trade_show else 0.0),
        },
        {
            "component": "capacity_decay",
            "weight": CAPACITY_DECAY_WEIGHT,
            "predicate": "weight * (1 - decay); decay sourced from QueueState",
            "predicate_satisfied": True,
            "input_value": "queue_state.capacity_decay",
            "contribution": "<= " + str(CAPACITY_DECAY_WEIGHT),
        },
    ]
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
        "decision_tree": fitness_decision_tree,
        "signal_hash": signal_hash,
    }

    # Render deterministic-side payloads.
    # (1) company_facts — restructured into three provenance buckets:
    #   csv_provided_facts: verbatim from the trade-show lead form (unaudited claims)
    #   verified_public_facts: fetched from external sources (Companies House,
    #                          Playwright scrape, Tavily news) — each block tagged
    #                          with status so UI can render conditionally
    #   ingest_provenance: batch + file hash + user + day (audit chain)
    csv_provided_facts = {
        "contact_name": lp_contact_name or "",
        "contact_email": lp_contact_email or "",
        "sector_hint": lp_sector_hint or "",
        "raw_notes": (lp_raw_notes or "")[:400],
    }
    verified_public_facts = {
        "companies_house": _format_enrichment_block(ch_payload, ch_status, ch_reason),
        "website_capabilities": _format_enrichment_block(ws_payload, ws_status, ws_reason),
        "recent_news": _format_enrichment_block(tn_payload, tn_status, tn_reason),
    }
    company_facts_payload = {
        "company_name": lp_company_name or "",
        "vertical": lp_vertical or "vertical_uncertain",
        "factory_size_band": lp_size_band or "unknown",
        "trade_show_provenance": str(bool(lp_trade_show)),
        "source_system": lp_source_system or "",
        "external_lead_id": lp_external_lead_id or "",
        "enrichment_status": lp_enrichment_status or "",
        "requires_human_review": str(bool(lp_requires_human_review)),
        "last_scored_at": str(lp_last_scored_at) if lp_last_scored_at else "",
        "csv_provided_facts": csv_provided_facts,
        "verified_public_facts": verified_public_facts,
        "ingest_provenance": {
            "batch_id": lp_batch_id or "",
            "file_sha256": ib_file_sha256 or "",
            "user_id": ib_user_id or "",
            "ingest_day": str(ib_day) if ib_day else "",
            "ingest_created_at": str(ib_created_at) if ib_created_at else "",
            "source_label": ib_source_surface or "",
        },
    }

    # (2) verified_kg_anchors — adds per-vertical multi-anchor cross-table with
    # verbatim citation excerpts for every peer anchor (substrate-grounded evidence).
    verified_kg_anchors_payload = {
        "matta_customer_anchor": comparable.matta_customer_anchor,
        "selection_method": comparable.selection_method,
        "citation_substrate_line": comparable.citation_substrate_line,
        "knowledge_graph_version": kg_version,
    }
    if kg_anchor_obj is not None:
        verified_kg_anchors_payload.update({
            "anchor_id": kg_anchor_obj.anchor_id,
            "vertical": kg_anchor_obj.vertical,
            "deployment_type": kg_anchor_obj.deployment_type,
            "citation_substrate_lines": list(kg_anchor_obj.citation_substrate_lines),
            "citation_verbatim_excerpt": kg_anchor_obj.citation_verbatim_excerpt,
            "permitted_dimensions_of_comparability": list(kg_anchor_obj.permitted_dimensions_of_comparability),
        })
        verified_kg_anchors_payload["peer_anchors_in_vertical"] = [
            {
                "anchor_id": a.anchor_id,
                "deployment_type": a.deployment_type,
                "citation_substrate_lines": list(a.citation_substrate_lines),
                "citation_verbatim_excerpt": a.citation_verbatim_excerpt,
                "permitted_dimensions_of_comparability": list(a.permitted_dimensions_of_comparability),
            }
            for a in peer_anchors
        ]

    # (4) risk_checklist_baseline — adds risk_pillar (categorical), severity_score
    # (numerical), and deterministic kg_evidence_anchor per finding.
    risk_checklist_baseline_payload = [
        {
            "category": f.category,
            "severity": f.severity,
            "risk_pillar": RISK_PILLAR_LOOKUP.get(f.category, "uncategorised"),
            "severity_score": SEVERITY_SCORE_LOOKUP.get(f.severity, 0.0),
            "kg_evidence_anchor": RISK_KG_EVIDENCE_ANCHOR.get(f.category, ""),
        }
        for f in risk.findings
    ]

    # (5) approach_template_baseline — adds deterministic_phase_breakdown with
    # full evaluation_criteria + exit_criteria per phase (Day-1 actionable plan).
    approach_template_baseline_payload = {
        "template": approach.template,
        "day_one_risks": list(approach.day_one_risks),
        "deterministic_phase_breakdown": APPROACH_PHASE_BREAKDOWN.get(approach.template, []),
    }

    # (6) process_taxonomy_with_enrichment — wraps the LLM-generated vertical
    # baseline with verified capabilities / customers / certifications pulled
    # from the Playwright scrape. The LLM taxonomy is a vertical-template
    # fallback; the enrichment block is company-specific ground truth.
    #
    # Phase 1.7 Stage C: when vertical is "vertical_uncertain" (the N=3
    # classifier ensemble didn't reach consensus), the section switches to an
    # explicit deferral block rather than silently rendering a default
    # vertical baseline.
    ws_data = ws_payload if (ws_status == "fetched" and isinstance(ws_payload, dict)) else {}
    if lp_vertical == "vertical_uncertain":
        ensemble_outputs_list = []
        if isinstance(lp_vertical_ensemble_outputs, dict):
            ensemble_outputs_list = lp_vertical_ensemble_outputs.get("ensemble_outputs", []) or []
        process_taxonomy_with_enrichment_payload = {
            "status": "vertical_classification_deferred",
            "ensemble_outputs": ensemble_outputs_list,
            "verified_capabilities_from_website": ws_data.get("extracted_capabilities", []),
            "verified_customers_from_website": ws_data.get("extracted_customers", []),
            "verified_certifications": ws_data.get("extracted_certifications", []),
            "vertical": "vertical_uncertain",
            "scope_note": (
                "The 3-model vertical classification ensemble did not reach "
                "consensus for this prospect. §1 Process Taxonomy is omitted "
                "to avoid silently substituting a default vertical baseline. "
                "Recommend reviewing the contact's raw_notes and sector_hint "
                "on the trade-show CSV. Per-model classifications above."
            ),
        }
    else:
        process_taxonomy_with_enrichment_payload = {
            "status": "ok",
            "llm_generated_taxonomy": taxonomy.model_dump(),
            "verified_capabilities_from_website": ws_data.get("extracted_capabilities", []),
            "verified_customers_from_website": ws_data.get("extracted_customers", []),
            "verified_certifications": ws_data.get("extracted_certifications", []),
            "vertical": lp_vertical or "vertical_uncertain",
            "phase_1_scope_note": (
                "§1 maps the prospect to a verified vertical baseline. Where the "
                "Playwright scrape returned capabilities, customers, or "
                "certifications, those are listed above as ground-truth from the "
                "company's own website. The LLM-generated taxonomy below is the "
                "vertical-template fallback — sub-processes and line-level steps "
                "characteristic of the vertical, not specific to this prospect."
            ),
        }

    rendered_sections = {
        # Deterministic-content section renders (counted toward bytes(deterministic_content)).
        "company_facts": _render_section(company_facts_payload),
        "process_taxonomy_with_enrichment": _render_section(process_taxonomy_with_enrichment_payload),
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
