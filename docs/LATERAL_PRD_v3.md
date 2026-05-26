# LATERAL_PRD_v3.md

## The Concept.

**Broken axes: Output shape, Statefulness location, Pipeline shape.** The Drive Corpus Refinery turns each prospect into a Google Drive knowledge object backed by Vertex AI Search-style retrieval, rather than a Postgres-resident entity ending in a Notion-style artifact. Ingested lead batches create a Drive folder per event and a lightweight corpus document per prospect. Stage 1 prioritization is a generated index document across the folder; Stage 2 is a Google Doc dossier grounded in the prospect corpus.

The pipeline becomes continuous-background rather than two-stage sequential. The system still solves both stages: it ranks raw inbound volume and generates per-candidate pre-visit context. But after initial ingest, background workers refresh public-data snapshots, citation anchors, and dossier sections as new evidence arrives. The FDE always opens the current Google Doc, not a frozen artifact.

This lateral is strongest where Matta wants shareability and source review. Drive is not Matta's product surface, and the architecture stays completely outside deployment systems. The Anti-Replication principle holds because Damjan's team is not trying to build a Google Drive research corpus for FDE pre-visit prep; this is an unplug-gable intelligence workspace around their lead pipeline.

## The Strategic Hook.

Drive fits the evidence because the bottleneck is asynchronous and document-heavy. `Matta_Intel_cleaned.md` line 114 says Matta has a "multi-year waitlist"; line 271 says they are "working with hundreds of factories in our pipeline"; and line 294 says one show produced "124 leads in two days." A corpus that evolves over months is more faithful to that reality than a one-off generation event.

The Strategic Hook for Special Projects is even sharper. Line 625 says the role must help close customer deals and distil technical, sometimes chaotic ideas into polished points for large corporate partners. A Drive dossier can be reviewed, commented on, and shared before an FDE visit or founder call. It also suits the FDE motion: line 716 says FDEs travel 10-20% to trade shows and customers, and line 705 says they shift from lead capture to factory problem-solving. A living doc is the preparation artifact they can read before travel and update after the call.

`Matta_Dossier.md` supports this with Pattinson and Denic psychology. Pattinson is described as academic, precise, and first-principles-oriented (sections 5-7, lines 128-142), which makes citation-visible corpus grounding more persuasive than a glossy dashboard. Denic's profile emphasizes schema cleanliness and idempotency (sections 4 and 6, lines 178-195), so the Drive surface must be backed by strict typed manifests and deterministic refresh rules, not free-form doc editing alone.

## The Agent Architecture.

All inference uses Vertex AI in `europe-west4` through `google-genai`. Model routing follows the modernized PRD: `gemini-3-flash-preview` for N=3 categorical ensemble tasks and `gemini-3.1-pro-preview` for synthesis sections. The global endpoint and all non-Google providers are forbidden. The system consumes only public corporate data, CRM exports, and Matta's citation-validated public deployment footprint.

Ingress contract: `POST /drive/ingest/batch` accepts CSV or CRM export plus `source_label`. The deterministic ADC maps to `CORPUS_BATCH`, `CORPUS_REFRESH`, `PRIORITY_INDEX`, or `DOSSIER_DOC`. `LeadIntakeBatch`, `ProspectCorpusManifest`, `PriorityIndex`, and `PreVisitDossierDoc` all use Pydantic `extra="forbid"`. The LLM is never allowed to decide whether a document is a prospect, a priority index, or a dossier.

Statefulness location: Drive documents and corpus manifests are the durable prospect surface. Postgres stores only references, idempotency keys, and background job state. Each prospect folder contains `manifest.json`, `public_sources.json`, `triage.md`, `dossier.md`, and rendered Google Doc IDs. The manifest carries `prospect_id`, `external_lead_id`, `signal_hash`, `knowledge_graph_version`, and citation pointers.

Stage 1: ingestion creates corpus manifests, deterministic enrichment snapshots, N=3 Flash vertical classification, and deterministic fit scores. The batch-level `PriorityIndex` Google Doc lists top candidates, score rationale, uncertain verticals, and links to each prospect corpus. Stage 2: dossier doc generation reads only the typed manifest plus retrieval snippets whose citations pass provenance validation. Process taxonomy uses Pro `medium`; defect-class hypothesis uses Flash N=3 with conformal calibration; comparable deployment, risk register, and suggested approach use Pro `low`.

Pipeline shape: continuous background jobs refresh manifests nightly or on explicit `Refresh` button. A refresh recomputes `signal_hash`; if changed, only stale sections regenerate. Conformal calibration artifacts are versioned, and a dossier section displays the calibration version. Graceful degradation: if Drive write fails, generated JSON remains in the job store and retries; if retrieval has no verified evidence, sections are marked `requires_human_review`; if background refresh is rate-limited, the doc displays `last_verified_at`.

## The Native Environment UI Spec.

The three-pane theater remains. Left pane is Google Drive: a folder named `UK Metals Expo 2025 - Matta Refinery` appears with `Priority Index` and prospect folders. The cursor opens the priority index, where William Cook Sheffield is first and has a "Generate dossier doc" action.

Center pane is the Theater: batch ingest, corpus manifest creation, ADC decision, Drive document IDs, retrieval snippets, schema validation, N=3 Flash ensemble, conformal calibration, and citation-provenance checks. It must show the distinction between Drive as document surface and Pydantic manifests as the typed truth.

Right pane is the Google Doc dossier. It materializes live: summary, process taxonomy, defect-class hypothesis with coverage set, comparable Matta deployment with line citation, integration risks, suggested approach, and evidence appendix. Cold-open timing: T+0 Drive folder import, T+12 Priority Index with ranked candidates, T+18 Generate dossier doc, T+35 taxonomy, T+48 conformal defect set, T+62 comparable deployment citation, T+80 final suggested approach, T+88 evidence appendix link. Under 90 seconds is mandatory.

## Phase 1 Execution Spec.

Repository structure:

```text
matta-refinery/
  apps/drive_refinery_api/
    routers/drive_ingest.py
    routers/drive_actions.py
  apps/refinery_worker/tasks/
    create_corpus_manifests.py
    refresh_prospect_corpus.py
    generate_priority_index_doc.py
    generate_google_dossier_doc.py
  packages/drive/
    client.py
    renderers.py
    retry_outbox.py
  packages/schemas/corpus.py
  packages/schemas/dossier.py
  packages/knowledge_graph/
  packages/prompts/
  apps/theater_ui/components/
    DriveLeftPane.tsx
    CorpusTheaterPane.tsx
    GoogleDocRightPane.tsx
```

Critical schemas:

```python
class ProspectCorpusManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prospect_id: str
    external_lead_id: str
    drive_folder_id: str
    source_label: str
    signal_hash: str
    knowledge_graph_version: str
    public_source_refs: list[str]
    last_verified_at: datetime

class PriorityIndexEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prospect_id: str
    company_name: str
    fit_score: float = Field(..., ge=0, le=1)
    dossier_doc_id: str | None = None
    requires_human_review: bool
```

FastAPI contracts: `POST /drive/ingest/batch` receives CSV, creates folder/job ack, and returns `batch_id`. `POST /drive/dossier/generate` accepts `prospect_id`, validates manifest, and returns `doc_pending`. `POST /drive/refresh` triggers recomputation of source snapshots and stale sections. All jobs use Celery with late acknowledgements and Drive write retries.

Prompt templates are retrieval-grounded. Each prompt receives `allowed_evidence[]` with citation line numbers and is forbidden to cite outside it. The comparable deployment prompt accepts only graph anchors validated at startup. Mock data seeds a fake Drive folder and corpus documents from UK Metals Expo line 294 plus public deployment anchors from line 540. Demo recording uses Drive-styled mocks unless Google credentials are present.

Magic Moment success criteria: Priority Index appears in under 12 seconds; dossier doc completes under 90 seconds; every section has schema validation; Drive document contains an evidence appendix; refresh does not duplicate prospect folders; if a citation line fails validation, the doc renders `requires_human_review` rather than a claim.

## Lateral-Specific Risk Register.

**Risk 1: Drive state feels less rigorous than Postgres.** Damjan may dislike document-native state. Mitigation: document state is a projection of typed manifests; the Theater shows manifest JSON, idempotency keys, and section hashes.

**Risk 2: Background refresh creates stale or surprising changes.** FDEs may open a doc that changed since last review. Mitigation: each section displays `last_verified_at`, `signal_hash`, and a change log at top.

**Risk 3: Google Doc output feels too close to generic research automation.** Mitigation: the differentiator is not doc generation; it is Matta-specific vertical scoring, conformal defect hypotheses, and citation-validated comparable deployment anchors.
