# LATERAL_PRD_v4.md

## The Concept.

**Broken axes: Determinism boundary, Ingress shape, Buyer/user surface, Output shape.** The Deterministic Field Kit is a Mac/Windows desktop client for post-show lead processing under bad trade-show and travel conditions. It accepts CSV exports, pasted email tables, and optional mobile photos of business cards after the show. Unlike the Refinery, 80% of the dossier is produced by deterministic rules, curated manufacturing taxonomies, and citation-validated templates; LLMs fill only tightly bounded narrative fields.

The system still spans both stages. Stage 1 runs a rules-heavy capacity and vertical-fit pass over the raw lead batch. Stage 2 generates a pre-visit pack for selected candidates, but the pack is mostly assembled from deterministic modules: company facts, vertical taxonomy, known Matta deployment anchors, risk checklist, and visit-prep checklist. Gemini is reserved for process-taxonomy synthesis and the defect-class ensemble where the locked invariants require N=3 and conformal calibration.

This lateral deliberately tests the opposite of a heavier agentic path. It is less magical but more Denic-compatible: local-first queue, offline cache, replayable event log, typed exports, and deterministic sections that can be audited. The output breaks the Refinery artifact too: the FDE receives a compact PDF pack plus optional voice-narrated audio briefing generated from the validated dossier schema for listening during travel.

## The Strategic Hook.

The Field Kit is justified by the FDE operating reality. `Matta_Intel_cleaned.md` line 705 says an FDE can be at trade shows one week and then "deep in a factory" the next; line 716 says they travel "10-20% time" to trade shows and customers. Line 294 shows UK Metals Expo generated "124 leads in two days," and line 284 shows Advanced Engineering generated "over 100 incredible leads" in one day. A desktop client with offline-friendly ingest and deterministic replay respects that travel-heavy handoff without reviving the killed 60-second booth pitch.

The rules-heavy posture also fits Doug and Sebastian. Line 528 quotes Doug's physical-first stance: the hard part is making things work at scale, not "dreaming things up inside a computer." Line 540 says most deployments are live within hours and cites 99% defect detection with ten minutes of data plus real deployment anchors. A deterministic pack that refuses to overclaim defect classes is safer than an agent that writes beautifully but invents a comparable.

`Matta_Dossier.md` makes the Denic hook explicit. His section says he is an execution maximalist who writes code, enforces schema hygiene, and values pristine database state (lines 170-172). It also says strict schema validation and idempotency are core mandates (lines 178-183). The Field Kit gives him a replayable local event log, Pydantic exports, and deterministic module outputs. Brion's dossier section also supports the uncertainty stance: lines 59-61 describe his deep ensemble and uncertainty preferences, so the only model-heavy part remains the N=3 conformal defect hypothesis.

## The Agent Architecture.

All cloud inference uses Vertex AI in `europe-west4` via `google-genai`, with only `gemini-3-flash-preview` and `gemini-3.1-pro-preview`. The desktop client can run offline for ingest, parsing, deterministic scoring, and cached dossier assembly. It queues Vertex calls until connectivity returns. It never touches Matta production systems, camera streams, factory agents, foundation models, Manufacturing OS UI, edge firmware, CMMS, QMS, or customer production lines.

Ingress contract: desktop imports normalize into `FieldKitLeadBatch`. CSV and pasted tables are deterministic parses. Business-card photos use Google OCR only if configured; otherwise the photo remains an attachment requiring human review. The deterministic ADC routes `BATCH_IMPORT`, `PHOTO_OCR_IMPORT`, `LOCAL_PRIORITIZE`, `CLOUD_DOSSIER_SECTION`, `EXPORT_PACK`, or `HUMAN_REVIEW`. Unknown columns or OCR ambiguity stop at review.

Stage 1: deterministic rules produce the first ranking from vertical hints, company size bands, trade-show provenance, and Matta-verified vertical map. `gemini-3-flash-preview` N=3 vertical classification is optional only when deterministic fields are insufficient; if used, it is schema-bound and `thinking_level="minimal"`. Fitness score remains deterministic and explainable.

Stage 2: deterministic modules assemble 80% of the pre-visit pack: executive summary skeleton, company facts, public-source checklist, verified Matta deployment anchors, integration-risk checklist, visit questions, and unknowns. Process taxonomy uses `gemini-3.1-pro-preview`, N=1, `thinking_level="medium"`, bounded to a schema. Defect-class hypothesis always uses N=3 `gemini-3-flash-preview` with conformal calibration. Comparable deployment selection is deterministic from the citation-validated graph; Pro may write only the `dimension_of_comparability` prose under a 250-character cap.

Schema enforcement happens at import, route decision, section generation, pack assembly, PDF render, audio script render, and export. The audio briefing is generated from a validated `AudioBriefingScript` schema and rendered with OS/browser text-to-speech for the demo, avoiding another AI provider. Idempotency: local SQLite event log keys imports by file hash/photo hash, prospects by `(source_label, external_lead_id)`, and packs by `(prospect_id, signal_hash, knowledge_graph_version, template_version)`. Graceful degradation: no network means deterministic pack still exports with cloud sections marked queued; OCR ambiguity produces a review card; failed Vertex calls never block PDF export.

## The Native Environment UI Spec.

The three-pane theater remains. Left pane is the desktop Field Kit import screen. The cursor drops `UK_Metals_Expo_2025_leads.csv`, then adds two photographed business cards as optional post-show cleanup. The ranked batch appears locally with offline status and deterministic score explanations.

Center pane is the Theater: local event log, ADC route, schema validation, deterministic module coverage meter, queued Vertex calls, N=3 Flash ensemble, conformal calibration, and PDF/audio render state. It must make the heavier deterministic boundary visible.

Right pane is the output pack: a compact PDF preview plus a small audio player. The PDF fills first with deterministic sections, then cloud-generated taxonomy and defect hypothesis. Cold-open timing: T+0 import, T+8 ranked local shortlist, T+15 select William Cook Sheffield, T+25 deterministic pack scaffold, T+45 taxonomy returns, T+58 conformal defect set, T+70 PDF complete, T+82 audio briefing ready. The visceral payoff is an FDE-ready travel pack under 90 seconds.

## Phase 1 Execution Spec.

Repository structure:

```text
matta-refinery/
  apps/fieldkit_desktop/
    main.tsx
    src/import/
    src/local_event_log/
    src/pdf_pack/
    src/audio_briefing/
  apps/fieldkit_api/
    routers/vertex_sections.py
    routers/sync.py
  apps/refinery_worker/tasks/
    process_taxonomy.py
    defect_hypothesis.py
    render_pack.py
  packages/schemas/fieldkit.py
  packages/schemas/dossier.py
  packages/rules/
    deterministic_scoring.py
    comparable_selection.py
    risk_checklist.py
  packages/prompts/
  apps/theater_ui/components/
    FieldKitLeftPane.tsx
    DeterminismTheaterPane.tsx
    PackRightPane.tsx
```

Critical schemas:

```python
class FieldKitLeadBatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    batch_id: str
    source_label: str
    import_mode: Literal["csv", "pasted_table", "business_card_photo"]
    local_file_hash: str
    rows: list[LeadIntakeRow]

class TravelPack(BaseModel):
    model_config = ConfigDict(extra="forbid")
    pack_id: str
    prospect_id: str
    deterministic_sections: dict[str, str]
    process_taxonomy: ProcessTaxonomy | None
    defect_hypothesis: LikelyDefectClassHypothesis | None
    audio_script: str | None = Field(None, max_length=2500)
    queued_cloud_sections: list[str] = Field(default_factory=list)
```

FastAPI contracts: `POST /fieldkit/sync` receives local event batches and returns accepted event IDs. `POST /fieldkit/vertex/process-taxonomy` and `POST /fieldkit/vertex/defect-hypothesis` accept strict section requests and return schema-bound outputs. The desktop client signs sync payloads and can replay from the local event log after network recovery.

Prompt templates are shorter than the Refinery's. The taxonomy prompt synthesizes only from deterministic facts and public snippets. The defect prompt uses fixed defect enums, N=3 Flash, `thinking_level="minimal"`, and conformal calibration. The comparable prompt is mostly removed; comparable selection is rules-only from the verified knowledge graph. Mock data includes the UK Metals Expo 124-row CSV and two business-card images with deterministic OCR fixtures.

Magic Moment success criteria: local shortlist appears without network; PDF scaffold exists before Vertex returns; cloud sections complete under 90 seconds when online; audio script is generated only from validated schema; duplicate imports produce no duplicate prospects; the Theater shows that deterministic sections outnumber LLM sections.

## Lateral-Specific Risk Register.

**Risk 1: The desktop client feels heavier than a sidecar.** A native app can look like product sprawl. Mitigation: package it as a demo-only field kit with a small sync API and prove the same core can run as a web app later.

**Risk 2: Rules-heavy output feels less intelligent than the Refinery.** Doug may expect deep research. Mitigation: emphasize reliability and uncertainty: deterministic pack first, Gemini only where synthesis or conformal defect hypotheses add value.

**Risk 3: Business-card OCR drifts toward booth capture.** That risks the killed Brief form. Mitigation: position photo OCR as optional post-show cleanup only; the main workflow remains batch triage plus pre-visit pack generation.
