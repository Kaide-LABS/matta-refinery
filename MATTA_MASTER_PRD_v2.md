# MATTA_MASTER_PRD_v2.md

**Kaide Labs — Forward Deployed Engineering Strike Team**
**Target:** Matta (https://www.matta.ai/)
**Architecture:** The Refinery (Form C) — stateful pre-deployment intelligence sidecar
**Author:** Principal Staff Engineer, post-1F-red v2 adjudication
**Status:** Internal Kaide Labs document. Sections flagged for scrubbing if reused client-facing.
**Sprint window:** 48–72 hours, Hafeedh (architecture) + Isaac (demo production)
**Supersedes:** `MATTA_MASTER_PRD.md` (v1, CMMS Bridge — killed)

---

## 0. Audit Trail and Preceding Verdicts

This is the third architectural cycle on Matta in this sprint. The first two are killed and preserved for audit trail; this PRD does not re-litigate them.

**Cycle 1 — CMMS Bridge (v1 PRD).** Outbound webhook → CMMS work-order routing sidecar. Killed at 1F-red v1 after Gemini's 1F audit and a second-pass adjudication identified two cascading premise failures: (a) the FDE JD does not name CMMS integration as a current burden, and (b) Matta's verbatim "deployments live in hours / 24 hours vs industry 6 months" speed differentiator made any "future IT-compliance friction" reposition actively contradict their own marketing. Disposition: full architecture preserved as a verbal-only Phase 3 adjacent idea if a third discovery call materializes.

**Cycle 2 — The Brief (v1 positioning + draft scope).** Stateless mobile pre-call scoping sidecar for the trade-show booth. Killed at 1F-red v2 after Gemini's 1F-lite audit identified four-axis form mismatch with the verified operational reality: Matta has a multi-year waitlist (stateful pipeline), 124-leads-in-2-days post-show triage volume (asynchronous workflow), CSV-driven desktop processing not phone-driven (desktop anchored), and Sebastian-grade uncertainty-quantification rigor for regulated-industry procurement (deep research, not 60-second lookup). Form A (Pipeline Triage standalone) and Form B (Pre-Visit Dossier standalone) were also evaluated and rejected on thin-margin failure modes (strategic-decision ego check for A; Clay-class commodification for B). Form C — the combined Refinery — was selected.

**Citation Hygiene Audit (v1 Section 1.E):** five tainted citations identified (1, 12/13, 16, 18/22, 20). Killed and stay killed. This PRD inherits the audit unchanged and does not resurface any of them.

**1F-red v2 verification corrections.** The Brief audit had three primary-source misses: trade-show evidence is verbatim-present (UK Metals Expo, Advanced Engineering 2025, MACH 2026, Southern Manufacturing 2026), "global drinks brand" is verbatim-present in funding press, Cummins is verbatim-present in the Matta relationship/event graph (RAE event panel) though not in the deployment footprint. These corrections are load-bearing for Section 1.F below.

---

## 1. Red-Team Adjudication

### 1.A through 1.D — Reference dispositions (no re-adjudication)

The v1 PRD's Section 1 evaluated six architectures (DMZ Vanguard, Taxonomy Engine, Supply Chain Ledger, plus four Kaide-independent proposals). All dispositions hold. The v2 verdict added three more (Brief, Form A, Form B). All killed. The Refinery (Form C) is selected. No further adjudication of preceding architectures is required at this stage; if Codex 1D surfaces an architecture not on the existing kill list, it will be adjudicated then.

### 1.E — Citation Hygiene Audit (carried forward from v1, unchanged)

The five tainted citations identified in v1 stay killed:
- **Citation 1** (douglasbrion.com/cv.pdf) — dead link, discard.
- **Citation 12/13** ("Controlled Agentic AI Systems" preprint) — likely semantic graft, Pattinson Filter rebuilt on his verified ARIA SoTA Frontiers Night talk and Cambridge CAM "Security of Physical AI Systems" research theme.
- **Citation 16** (Hacker News "Who is hiring?" aggregator) — unverified authorship, replaced with direct intel.md JD citations.
- **Citation 18/22** (tribble.ai vendor blog stats) — vendor-marketing source for vendor-category recommendation, methodologically unsound.
- **Citation 20** (SMT Magazine 2015 cited as 2025 1st Kind investor thesis) — temporally impossible, likely fabricated attribution.

The Refinery PRD inherits this audit and adds new entity-level audits in Section 1.F.

### 1.F — Refinery-Specific Entity-Level Red-Team

The Refinery's Stage 2 dossier output ships a "comparable Matta deployment" section as a load-bearing structural element. This section ships entity references into client-facing artifacts and must be primary-source-grounded at the entity level, not just the vertical level. Three entity categories audited.

**Cummins.** Steven Grace (Automation & Technology Leader) and Jonathan Wood (VP-CTO, Cummins Europe) attended the Matta-hosted Sentient Factories event at the Royal Academy of Engineering. Steven Grace was on the Matta-organized panel. *Verified verbatim: `Matta_Intel_cleaned.md` lines 200, 210, 212–214, 321, 331, 338–340, 345.* Cummins is in Matta's relationship/event graph. **Cummins is NOT in Matta's verified deployment footprint.** No primary source places SENTRY/TALLY/GAUGE/TRACE inside any Cummins facility. Disposition: Cummins is permitted as a *demo-target name* in the Why-Video (Doug knows Cummins, hosted Cummins, has a relationship — using "Cummins Daventry plant" as a hypothetical FDE-bound prospect is grounded). Cummins is forbidden as a *comparable-deployment anchor* in any dossier output (no deployment evidence to compare to). The knowledge graph file (Section 6.5) enforces this distinction structurally.

**"Global drinks brand."** Verified verbatim in Matta funding press materials: *"Recent projects range from inspecting high-speed bottling for defects with a global drinks brand to working with Bowers & Wilkins"* (`Matta_Intel_cleaned.md` lines 540, 600). Disposition: permitted as a comparable-deployment anchor for the F&B bottling vertical. Anchor citation in the knowledge graph points to lines 540/600.

**"Aerospace composites."** The phrase "composites" is not in the substrate. Broader aerospace deployment IS verified — "plane wings" appears verbatim multiple times (lines 106, 119, 248, 303), aerospace appears as a deployment vertical in the funding press, GKN Aerospace and BAE Systems attended the RAE event, FDE travel JD names "10-20% time to trade shows and customers" with explicit aerospace context. Disposition: the knowledge graph anchors on "aerospace" as the broad vertical with three sub-paths (precision-machined components like plane wings, titanium alloy metallurgy, additive manufacturing for aerospace via Caracol AM partnership). Sebastian's verbatim uncertainty-quantification posture forbids the dossier from claiming a comparable deployment in a sub-path that has no verified primary-source anchor; if a prospect is in aerospace composites specifically, the dossier marks the comparable section as `requires_human_review = True` rather than fabricating a comparable.

**Net effect on architecture.** The knowledge graph (Section 6.5) is rebuilt with mandatory citation provenance for every entity-level anchor. Each anchor stores the verbatim line number in `Matta_Intel_cleaned.md` and is verified in code at startup. Anchors without primary-source line citations are forbidden. This adds ~2 hours of curation to the sprint envelope but directly closes the audit class that killed the Brief's knowledge graph in Gemini's Claim 3 verdict.

---

## 2. Architecture Selection — The Refinery (Form C)

**The Refinery** — a stateful, asynchronous, desktop-anchored containerized sidecar that ingests trade-show lead lists (CSV / Hubspot / Salesforce export) and inbound waitlist signals, produces a continuously evolving prioritization queue against Matta's two-deployments-per-month capacity, and on-demand generates pre-visit dossiers for the FDE-bound subset.

**What it is.** A two-stage pipeline operating over a shared orchestration spine:
- **Stage 1 — Prioritization.** Ingests `LeadIntakeBatch` (raw CSV) → produces `PrioritizedQueue` (ranked `LeadProspect` entities scored against deployment capacity + vertical fit + Matta-side context). Stateful: prospect entities persist for months in Postgres as the multi-year waitlist evolves.
- **Stage 2 — Dossier Generation.** On-demand request for a single `LeadProspect` → produces `PreVisitDossier` (structured 8-section artifact: process taxonomy, defect-class hypothesis with conformal sets, comparable Matta deployment patterns, integration risk register, suggested approach, supporting context).

Stage 2 is the Magic Moment in the Vidyard. Stage 1 is the verbal tail tease.

**What it is not.** It does not touch SENTRY, TALLY, GAUGE, TRACE, the Manufacturing Foundation Models, the Manufacturing OS UI, edge device firmware, or real-time camera streams. It does not produce any artifact that flows into a Matta customer's CMMS, QMS, or production line. It serves Matta's *internal* FDE / Special Projects / CEO workflow — not Matta's customers' workflows. The DMZ rule holds absolutely.

**Identity-file deviation: explicit statefulness.** The Kaide Labs Identity file specifies *"Stateless API Sidecars and Containerized Microservices"* as the default architectural commitment. The Refinery is intentionally stateful. The deviation is justified by primary-source evidence: Doug Brion's verbatim *"we're deploying to around two factories a month and have a multi-year waitlist at the moment"* (`Matta_Intel_cleaned.md` lines 114, 267) describes a pipeline whose entities persist for months-to-years before deployment. A stateless sidecar that resets after every interaction cannot model that pipeline; the form-axis would fail on first contact with the verified operational reality. This deviation was explicitly adjudicated in the 1F-red v2 verdict and is not re-litigated here. The "Stateless" word in the Identity file is the default; it is not an absolute constraint when primary-source evidence demands otherwise. All other Identity-file commitments hold unchanged: containerized, modular, distinct, DMZ-clean, zero technical debt (the client can unplug it), deterministic safety layer.

**Locked invariants from v1 PRD (unchanged).** Four invariants port forward without modification:
1. Deterministic Action Domain Classifier — no LLM in the routing decision.
2. N=3 deep ensemble pattern — applied to Stage 2's defect-class hypothesis layer.
3. Pydantic `extra="forbid"` at every API boundary.
4. Google-only inference via Vertex AI in europe-west4.

---

## 3. The FDE Thesis

The Refinery passes all five SOP pillars and all four filters. Citations are verbatim from `Matta_Intel_cleaned.md` and the dossier; no fabricated sources.

### 3.1 Pillar 1 — Bottleneck Assassin

The pre-sales scoping bottleneck is supported by four independent verbatim sources, not one. (a) **Multi-year waitlist + capacity cap:** *"we're deploying to around two factories a month and have a multi-year waitlist at the moment"* (lines 114, 267). (b) **Trade-show inbound volume:** *"We clocked 124 leads in two days, putting us in the top 5% of exhibitors"* at UK Metals Expo Sept 2025 (line 294); *"Day one was a blast - we met over 100 incredible leads from across the manufacturing world"* at Advanced Engineering 2025 (line 284). Four separate trade shows verified in twelve months: UK Metals Expo 2025, Advanced Engineering 2025, MACH 2026 (lines 187, 191), Southern Manufacturing & Electronics 2025/2026 (lines 234, 393). (c) **FDE JD trade-show responsibilities, four verbatim references:** *"be the face of Matta, interfacing with prospective customers at trade shows"* (line 698); *"engaging prospective customers, qualifying leads, scoping problems"* (line 704); *"engaging with engineers and technicians at trade shows, bringing in leads alongside our CEO, Doug (and keeping him on track!)"* (line 705); *"travel (~10-20% time) to trade shows and customers"* (line 716). (d) **Special Projects / Chief of Staff JD, "probably our most important hire":** *"steering long-term strategy, supporting fundraising efforts, and helping close customer deals"* (line 625) plus *"Think Gandalf: the person who quietly works their magic behind the scenes"* (line 262).

The bottleneck is not lead capture — Matta has too many leads. It is the post-show triage from 100+ raw leads to ~10 deployment candidates, plus the per-candidate pre-visit preparation that happens in the 24–72 hours before an FDE arrives at a factory. The Refinery absorbs both ends of this load. Stage 1 returns FDE and Special Projects hours to factory work; Stage 2 returns pre-visit prep hours to actual customer interaction.

### 3.2 Pillar 2 — Anti-Replication

The Refinery does not touch any Matta core surface. It consumes only public corporate data (the prospect's website, public filings, ISO certifications, news mentions, LinkedIn signal), Matta's own public deployment footprint (verified via the citation-anchored knowledge graph in Section 6.5), and the trade-show lead lists Matta's team already collects in their existing CRM. Output flows to a Notion-style document panel and a Slack notification — the FDE's own working environment, not Matta's product surface.

The Ego Check passes cleanly. Damjan's roadmap does not include "build a stateful prospect-prioritization-and-dossier system for our internal FDE workflow" — his roadmap is the Manufacturing Foundation Models, the four production agents, the Manufacturing OS, and edge compute. A stateful internal-workflow sidecar that he can absorb in-house when bandwidth allows (or unplug entirely) is exactly the kind of work the FDE Strike Team model was designed to deliver. There is no shared signal path with the closed-loop control work disclosed in the 2022 Nature Communications paper; the Refinery never reads from a Matta camera, an agent emission, or a foundation-model output.

### 3.3 Pillar 3 — Native Environment

The Refinery's user is Matta's internal team (Doug, FDE engineers, the incoming Special Projects / Chief of Staff hire), not Matta's customers. Native environment for that user is: (a) a desktop browser with Hubspot or Salesforce open in another tab; (b) Slack for notifications and async coordination; (c) a Notion-style document or PDF preview for reading deep artifacts.

Stage 1's prioritization queue lives at a desktop URL embedded as a Hubspot/Salesforce-flavored dashboard (Tailwind on a stock SaaS layout). Stage 2's dossier output renders as a Notion-style document with structured sections, expandable citations, and a permanent shareable link. Slack notifications fire when (a) a new lead batch finishes Stage 1 scoring, (b) a dossier completes generation. The maintenance technician of the v1 PRD is replaced by the FDE Engineer reading the dossier on a flight to a factory visit the next morning.

### 3.4 Pillar 4 — Magic Moment (under 90 seconds)

The demo video opens on a desktop screen showing a CSV file (`UK_Metals_Expo_2025_leads.csv`, 124 rows visible). The cursor drags it into the Refinery dashboard.

T+0s: CSV ingest fires. The Refinery's Stage 1 queue begins materializing in real time — leads being scored, ranked, surfaced.
T+10s: Prioritized queue is fully visible. Top candidate: William Cook Sheffield, ductile iron casting (verified UK Metals Expo attendee per line 294).
T+12s: FDE clicks "Generate dossier" on the top candidate.
T+15s: The dossier panel begins materializing section by section. Process taxonomy first.
T+30s: Defect-class hypothesis section appears with conformal prediction set: porosity (high confidence), dimensional drift (medium), surface inclusions (medium).
T+50s: Comparable Matta deployment section: Bowers & Wilkins precision-machining stage citation appears (verified per line 540), with explicit dimension-of-comparability ("surface-finish QC stage similarity") rather than a sloppy "B&W is comparable" claim.
T+70s: Integration risk register: legacy CMM infrastructure flag, lighting variance flag, network topology unknown.
T+85s: Suggested approach: 2-camera SENTRY pilot on highest-throughput line, lighting calibration as Day-1 risk.

Total elapsed: 85 seconds. Buffer to 90s reserved for demo narration overlay. Visceral demo is artifact depth, not speed.

### 3.5 Pillar 5 — System Resilience and Immunity

Three layers of deterministic safety, each addressing a specific filter.

**Idempotency layer (stateful adaptation).** Every CSV ingest carries an idempotency key derived from the file hash + originating user + ingest timestamp. The Refinery's Postgres `ingest_batches` table prevents duplicate batch runs. Per-prospect upsert semantics on `LeadProspect.external_lead_id` (sourced from Hubspot/Salesforce native ID) ensure that re-ingest of overlapping batches does not create duplicate prospect entities; instead, the existing entity is updated with new signals and re-scored. This is the stateful analog of v1's exactly-once-effectively guarantee on event_id, adapted for a stateful pipeline rather than ephemeral events.

**Deterministic two-route ADC.** A hardcoded Python rules engine maps `(request_type, payload_shape)` to one of two routes: `PRIORITIZATION` (CSV ingest → queue scoring) or `DOSSIER` (single LeadProspect ID → artifact generation). The LLM does not decide which path runs. The Pydantic schema for each route's output enforces the admissible action space at the API boundary. This addresses the Pattinson Filter — deterministic governance is the structural prerequisite, the LLM is restricted to within-route generation under fixed schema constraints.

**Conformal prediction set on defect-class hypothesis.** Stage 2's defect-class hypothesis layer uses the v1 N=3 Gemini 3 Flash ensemble pattern with conformal calibration. Output is a *set* of likely defect classes with calibrated coverage (e.g., "with 80% coverage the true defect class is in {porosity, dimensional drift, surface inclusions}") rather than a single confident prediction. If the conformal set is empty (model is uncertain across all categories) or contains all categories (model has no signal), the dossier section is marked `requires_human_review = True` and surfaces in a dedicated Slack channel for FDE adjudication. This is the structural analog of *Lakshminarayanan, Pritzel & Blundell (2017), "Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles"* applied at the prompt-orchestration layer — exactly the methodology Doug Brion implemented in `dougbrion/pytorch-deep-ensembles`. The pitch must be clear: not Dirichlet-prior epistemic uncertainty on a foundation-model output (mathematically undefinable); rather, deep ensembles methodology lifted to the orchestration layer with conformal calibration on top.

### 3.6 Filter Pass-Through Summary

| Filter | Anchor | How the Refinery satisfies |
|---|---|---|
| Brion (commercial pragmatism + uncertainty) | "two factories a month, multi-year waitlist" + `dougbrion/pytorch-deep-ensembles` | Returns FDE / Special Projects / CEO hours from manual lead triage and pre-visit prep to factory-floor and customer-facing work; surfaces uncertainty via N=3 ensemble + conformal calibration on defect-class hypothesis, structurally analogous to his published methodology. |
| Pattinson (cyber-physical trust + first principles) | ARIA SoTA Frontiers Night + Cambridge CAM "Security of Physical AI Systems" + 2022 Nature Communications | Deterministic two-route ADC as governance operator; Pydantic schemas enforce admissible action space at every API boundary; no actuation of physical hardware; zero shared signal path with closed-loop control work; conformal sets prevent confident-but-wrong defect-class hypotheses. |
| Denic (execution maximalism + idempotency) | Backend Engineer JD: "FastAPI, Pydantic, Postgres, SQLAlchemy, Redis, Celery" | Refinery stack is exact match. Stateful upsert semantics on `LeadProspect.external_lead_id`. Celery `acks_late=True`. Postgres durable state for the multi-year pipeline. Graceful degradation when external enrichment APIs are down (queue + retry, partial dossier with explicit gaps marked). |
| Investor mandate (Lakestar + Giant + 1st Kind) | Akis Bratsos "fast time to value" + Giant European tech sovereignty + 1st Kind Peugeot industrial legacy | Refinery shortens deployment-slot decision cycle (Lakestar). Runs in Vertex AI europe-west4, no proprietary lead data leaves EU region (Giant). Stage 1 prioritization scoring is structurally aware of automotive Tier-1 and aerospace verticals (1st Kind / Peugeot industrial alignment). |

---

## 4. System Architecture and Agent Routing

All LLM inference is routed through Vertex AI on Google Cloud, europe-west4, via the Google Gen AI SDK (`google-genai`, the current production SDK as of May 2026). The legacy `vertexai.generative_models` module is deprecated and removed 2026-06-24 ([Vertex AI SDK migration guide](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/deprecations/genai-vertexai-sdk)); the Refinery ships against `google-genai` from day one. No Anthropic, OpenAI, or Bedrock dependencies anywhere in the deliverable.

### 4.1 Data Flow (Prose Diagram)

The Refinery exposes two primary FastAPI endpoints, both backed by the same orchestration spine.

**Endpoint 1: `POST /ingest/batch`** — accepts a CSV file (multipart) plus optional metadata (originating trade show, ingest user, batch label). Validates against `LeadIntakeBatch` Pydantic schema with `extra="forbid"`. Computes an idempotency key from file hash + user + timestamp. If the key exists in the `ingest_batches` Postgres table, returns the cached prior batch ID. If absent, writes a placeholder batch row, validates each CSV row against `LeadIntakeRow`, persists per-row entities to Postgres `lead_prospects` table (upsert on `external_lead_id`), and enqueues a Celery task `score_batch(batch_id)`.

**Endpoint 2: `POST /dossier/generate`** — accepts a `LeadProspect.id` reference. Validates the prospect exists and is in a state eligible for dossier generation (i.e., has been scored by Stage 1). Computes an idempotency key on `(prospect_id, current_signal_hash)`; if a prior dossier exists with the same signal hash, returns the cached dossier (this is the stateful version of v1's event_id idempotency). If absent, enqueues a Celery task `generate_dossier(prospect_id)` and returns a `dossier_pending` envelope with a polling URL.

The Celery worker fetches the requested entity from Postgres, then executes one of two pipeline paths via the deterministic Action Domain Classifier (Stage 0).

### 4.2 Stage 0 — Two-Route Action Domain Classifier (deterministic, no LLM)

A hardcoded Python rules engine maps `(request_type, payload_shape, route_eligibility)` to one of two paths:

- `PRIORITIZATION` — triggered by `/ingest/batch` requests. Runs Stage 1 over the entire batch.
- `DOSSIER` — triggered by `/dossier/generate` requests. Runs Stage 2 on a single prospect.

Default behavior on no-match: write to a `requires_human_review` channel in Slack with the unmatched payload, do not invoke any downstream LLM. This is the structural Pattinson-Filter satisfaction — the LLM cannot be reached without first passing a deterministic gate.

### 4.3 Stage 1 — Prioritization Scoring Pipeline

Per-prospect, executed in parallel across a batch:

**1.1 Public-data enrichment (no LLM).** Deterministic enrichment pulls from a fixed allowlist: prospect's website (basic scrape, structured data extraction), Companies House for UK entities (CapEx posture proxy via reported turnover and asset base), public LinkedIn signal (employee count band, hiring posture), ISO certification registries where indexed. Enrichment failures are logged but do not block scoring; missing fields are scored as `unknown`.

**1.2 Vertical classification (Gemini 3 Flash, N=3 ensemble, `thinking_level="minimal"`).** Three parallel Flash calls (model id `gemini-3-flash`, the current cost-optimized Vertex AI model — pricing $0.50/M input, $3.00/M output per [Google Cloud pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)) with temperature variance (0.1, 0.5, 0.9) classify the prospect into one of six manufacturing verticals (polymer extrusion, metal casting, additive manufacturing, F&B bottling, electronics assembly, aerospace) plus an `out_of_vertical` category for prospects outside Matta's verified deployment surface. Plurality voting; on disagreement, the prospect is tagged `vertical_uncertain` and Stage 2 (if requested later) is gated on human review of the vertical assignment.

**1.3 Deterministic fitness scoring.** A hardcoded scoring function combines (a) vertical match against Matta's verified deployment patterns, (b) factory size band against Matta's existing customer footprint, (c) trade-show provenance signal (a William Cook lead from UK Metals Expo carries higher prior than a cold web inquiry), (d) capacity-aware decay (prospects added to a saturated pipeline this quarter score lower than prospects added to a slot still open). The scoring function is fully deterministic Python — no LLM in the scoring decision. The LLM contribution is restricted to the categorical vertical classification in step 1.2.

**1.4 Queue assembly.** Sorted output written to `prioritized_queues` Postgres table with batch_id reference. Slack notification fires to the configured channel: "Batch X scored: 124 prospects, top 12 surfaced for FDE review." The dashboard reflects the new queue in real time via WebSocket.

### 4.4 Stage 2 — Dossier Generation Pipeline

Per-prospect, executed on-demand:

**2.1 Process taxonomy section (Gemini 3.1 Pro, N=1, `thinking_level="medium"`).** Inputs: prospect entity, vertical assignment, public enrichment payload. Model id `gemini-3-1-pro` (the current flagship reasoning model on Vertex AI as of May 2026 — pricing $2.00/M input ≤200K context, $12.00/M output). Output: structured `ProcessTaxonomy` schema describing the prospect's likely production processes at line-level granularity. Vertex AI structured-output mode enforces schema conformance. The Pro model is appropriate here because the output requires synthesis across the enrichment payload and the manufacturing-vertical knowledge graph.

**2.2 Defect-class hypothesis (Gemini 3 Flash, N=3 ensemble + conformal calibration; `thinking_level="minimal"`, temps 0.1 / 0.5 / 0.9).** Inputs: process taxonomy + vertical + manufacturing-vertical knowledge graph. `thinking_level="minimal"` is mandatory here — Gemini 3's default reasoning trace collapses the three samples toward a single mode and destroys the deep-ensembles signal that the Brion Filter depends on; minimal-thinking + wider temperature spread restores the sample diversity the Lakshminarayanan-Pritzel-Blundell methodology requires. Three parallel Flash calls each return a categorical distribution over defect classes for the inferred process type. Conformal calibration (computed offline against a labeled holdout set of past Matta deployments per the dossier) produces a coverage-calibrated *set* of likely defect classes. The dossier surfaces the conformal set with an explicit coverage statement: *"With 80% coverage, the dominant defect classes for this prospect are in: {porosity, dimensional drift, surface inclusions}."* Empty or all-class sets trigger `requires_human_review = True`.

**2.3 Comparable Matta deployment section (Gemini 3.1 Pro, N=1, `thinking_level="low"`, knowledge-graph-anchored).** Inputs: process taxonomy + vertical + the citation-anchored knowledge graph. Output: a `ComparableDeployment` schema citing one or two verified Matta deployments with explicit dimension-of-comparability annotation (e.g., *"B&W speaker components — comparable on the surface-finish QC stage, NOT on overall process category, NOT on production volume"*). The knowledge graph forbids citing entities without primary-source line provenance (Section 6.5). If no comparable exists in the verified deployment surface, the section is marked `no_comparable_available` and the dossier proceeds without fabricating one.

**2.4 Integration risk register (Gemini 3.1 Pro, N=1, `thinking_level="low"`).** Inputs: enrichment payload + process taxonomy + a hardcoded risk taxonomy (legacy CMM, lighting variance, EMF environment, network topology, OT/IT segmentation). Output: a `RiskRegister` schema with per-risk findings. Each risk is graded against a fixed three-tier scale (`identified`, `unknown`, `not_applicable`); the LLM does not invent risk categories outside the hardcoded taxonomy.

**2.5 Suggested approach (Gemini 3.1 Pro, N=1, `thinking_level="low"`).** Inputs: all preceding sections + a hardcoded "approach template" library (2-camera pilot, 4-camera pilot, full-line deployment, Caracol-AM-style OEM partnership). Output: a `SuggestedApproach` schema constraining recommendations to the template library — the LLM does not invent novel deployment patterns.

**2.6 Dossier assembly.** All five section schemas validated against `extra="forbid"` Pydantic models, then composed into a final `PreVisitDossier` envelope and persisted to Postgres `dossiers` table. WebSocket pushes the artifact to the document preview pane in real time as sections complete.

### 4.5 Gemini Model Routing Rationale

| Stage | Model | Reason |
|---|---|---|
| Vertical classification (1.2) | Gemini 3 Flash, N=3 (`thinking_level="minimal"`, temps 0.1 / 0.5 / 0.9) | Categorical task at high batch volume. `gemini-3-flash` is the current cost-optimized Vertex AI model (replaces deprecated 2.5 Flash); N=3 provides the deep-ensembles uncertainty signal without blowing batch latency. Pricing $0.50/M input, $3.00/M output. |
| Process taxonomy (2.1) | Gemini 3.1 Pro, N=1, `thinking_level="medium"` | Synthesis across enrichment + knowledge graph. `gemini-3-1-pro` is the current flagship reasoning model on Vertex AI (replaces 2.5 Pro); `thinking_level="medium"` gives the synthesis depth this section needs without runaway thinking-token cost. Pricing $2.00/M input ≤200K, $12.00/M output. |
| Defect-class hypothesis (2.2) | Gemini 3 Flash, N=3 (`thinking_level="minimal"`, temps 0.1 / 0.5 / 0.9) + conformal | Categorical task where uncertainty surfacing is the load-bearing output. `thinking_level="minimal"` preserves ensemble diversity (reasoning-mode would mode-collapse the samples). Mirrors Doug's published methodology directly. |
| Comparable deployment (2.3), Risk register (2.4), Suggested approach (2.5) | Gemini 3.1 Pro, N=1, `thinking_level="low"` | Each requires synthesis under hard schema constraints; Pro's instruction-following discipline is appropriate. `thinking_level="low"` is sufficient because the action space is constrained by the knowledge graph / risk taxonomy / approach template library — the model is filling structured fields, not reasoning open-ended. |
| All inference | Vertex AI europe-west4 via `google-genai` (`genai.Client(vertexai=True, location="europe-west4")`) | Investor mandate (Giant Ventures EU sovereignty) + GDPR data localization. Legacy `vertexai.generative_models` removed 2026-06-24, so the Refinery ships against `google-genai` from day one. |

### 4.6 Statefulness, Idempotency, Graceful Degradation

The Refinery is stateful — `LeadProspect` entities persist for months as the multi-year waitlist evolves. Stateful idempotency is enforced at three layers:

**Batch-level:** `ingest_batches` keyed on `(file_hash, user, timestamp)`. Duplicate batches return the cached batch_id; in-flight batches return a polling URL.

**Prospect-level:** `lead_prospects.external_lead_id` is the upsert key (unique on `(source_system, source_id)`). Re-ingest updates existing entities rather than creating duplicates. A `signal_hash` is computed over the prospect's current signal state; downstream operations (dossier generation) cache against `(prospect_id, signal_hash)` so a prospect whose signals have not changed since last dossier returns the cached artifact.

**Dossier-level:** `dossiers` keyed on `(prospect_id, signal_hash, knowledge_graph_version)`. Three-way invalidation: if any of (a) prospect signals change, (b) knowledge graph version bumps, (c) explicit force-regenerate flag is set, a new dossier is generated. Otherwise the cached artifact is returned.

**Graceful degradation.** External enrichment APIs (Companies House, ISO registries, web scrapers) are wrapped in circuit breakers with per-source TTL caches. A degraded enrichment run produces a dossier with explicit gaps marked (`enrichment_status: partial`); the dossier does not block on full enrichment but surfaces the gaps in the integration risk register. Slack notifications differentiate "complete dossier ready" from "partial dossier ready, X enrichment sources unavailable" — the FDE chooses whether to proceed or wait. This addresses Damjan's idempotency mandate per the v1 PRD framing.

---

## 5. Native Environment UI Spec — The Theater

The demo video has three on-screen panes recorded simultaneously. Layout differs from v1 because the user environment is Matta's internal team, not Matta's customer.

### 5.1 Left Pane — Desktop CSV Ingest + Prioritized Queue

Built in Tailwind on a stock Hubspot/Salesforce-flavored layout. Top half shows a CSV file tile (`UK_Metals_Expo_2025_leads.csv`, 124 rows, file metadata visible). Cursor drags it into the ingest area. After ingest, the bottom half populates with the prioritized queue — ranked list of prospects with score, vertical, top-line rationale, and a "Generate dossier" button per row. Top candidate (William Cook Sheffield) is highlighted. This pane represents the FDE's daily working environment — it is the source of the dossier request, not the destination.

### 5.2 Center Pane — Refinery Theater

A Next.js + Tailwind dashboard exposing the Refinery's internal state in real time via WebSocket. Modeled on the v1 Theater pane with adapted visualizations:

- **Inbound request card:** the raw `LeadIntakeBatch` (CSV preview) or `DossierRequest` (prospect ID) payload as JSON, animated in.
- **ADC decision badge:** showing the deterministic two-route decision (`payload=DossierRequest → DOSSIER path`).
- **Stage 2 sectional progress:** five horizontal cards representing the dossier sections, each filling in as its respective Vertex call completes. Process taxonomy first, then defect-class hypothesis (with conformal coverage shown live), then comparable deployment, risk register, suggested approach.
- **Ensemble visualization (during defect-class step):** three parallel cards labeled "Gemini Flash Sample 1/2/3" filling in with their categorical distributions; conformal calibration step shown as a final card aggregating the three into a coverage-calibrated set.
- **Cost ticker:** live Vertex AI cost per dossier (target under $0.10), to kill the "AI is expensive" objection.
- **JSON inspector:** click any pipeline stage to inspect the Pydantic-validated payloads. Built specifically for Damjan's post-demo code review.
- **Knowledge graph citation panel:** expandable side-panel showing every primary-source citation backing the comparable-deployment claim, with line numbers into the verified intel substrate.

### 5.3 Right Pane — Document Preview (Notion-Flavored, Not Notion's Actual UI)

A Notion-style or PDF-preview document panel rendered in Tailwind. Sits empty at the demo's start. When Stage 2 dispatches each section, the section materializes in the document with section header, structured content, and footnoted citations. Visual hierarchy mirrors a serious analytical artifact (the kind an FDE would print and read on a flight). At the end of the demo run, a "Share dossier" button is visible — implies a permanent shareable link, the workflow primitive that anchors Stage 2's value.

### 5.4 Bottom-Right Inset — Slack Notification Mock

A Slack desktop notification (not mobile this time — desktop reflects the FDE's actual working environment) showing "Dossier ready: William Cook Sheffield" with an Open / Copy Link / Mark for Visit button row. Lighter-weight than v1's mobile mock since this notification is informational rather than actionable.

### 5.5 Cold-Open and Voice-Over Treatment

Cold-open with the Magic Moment in the first 12 seconds. The first 18 seconds of the video shows nothing but the three panes, the CSV drag, the queue materialization, and the dossier beginning to fill in — no voiceover, just sound design. At T+18s Hafeedh's voiceover begins: *"What you just watched is The Refinery — a stateful sidecar that takes your trade-show lead lists and inbound waitlist signals, scores them against your two-deployments-a-month capacity, and on-demand generates pre-visit dossiers for the leads that promote into FDE deployment slots. Stateful, asynchronous, desktop-anchored. Built around your actual deployment cadence, not the booth conversation."* The next ~75 seconds is the technical walkthrough using the JSON inspector and the knowledge-graph citation panel.

The final ~15 seconds tease the verbal Phase 2 (Stage 1 standalone): *"There's an upstream prioritization layer that runs continuously over your full pipeline — not just the trade-show batches — and surfaces the queue feeding into this. Happy to walk that through on a 15-minute call."* And a verbal Phase 3 mention (the dormant CMMS Bridge): *"There's also a downstream companion architecture for the post-deployment workflow side, when the time comes."* Per the Identity file: adjacent ideas are verbal only.

---

## 6. Phase 1 Execution Spec — 72-Hour Sprint

### 6.1 Repository Structure

```
matta-refinery/
├── README.md
├── docker-compose.yml
├── .env.example
├── infra/
│   ├── Dockerfile.api
│   ├── Dockerfile.worker
│   └── cloudrun.yaml
├── apps/
│   ├── refinery_api/                  # FastAPI ingress + dossier endpoints
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── ingest.py              # POST /ingest/batch
│   │   │   ├── dossier.py             # POST /dossier/generate, GET /dossier/{id}
│   │   │   └── slack_interactions.py
│   │   └── tests/
│   ├── refinery_worker/               # Celery workers
│   │   ├── tasks/
│   │   │   ├── classify_action_domain.py    # Stage 0 deterministic ADC
│   │   │   ├── score_batch.py               # Stage 1 orchestration
│   │   │   ├── enrich_prospect.py           # Stage 1.1 deterministic enrichment
│   │   │   ├── classify_vertical.py         # Stage 1.2 N=3 Flash
│   │   │   ├── score_fitness.py             # Stage 1.3 deterministic fitness
│   │   │   ├── generate_dossier.py          # Stage 2 orchestration
│   │   │   ├── dossier_section_taxonomy.py  # Stage 2.1
│   │   │   ├── dossier_section_defect.py    # Stage 2.2 N=3 + conformal
│   │   │   ├── dossier_section_comparable.py # Stage 2.3
│   │   │   ├── dossier_section_risk.py      # Stage 2.4
│   │   │   └── dossier_section_approach.py  # Stage 2.5
│   │   └── tests/
│   ├── theater_ui/                    # Next.js Theater dashboard
│   │   ├── pages/
│   │   ├── components/
│   │   └── hooks/useWebSocket.ts
│   └── mocks/
│       ├── lead_csv_generator.py      # Generates synthetic UK Metals Expo CSV
│       ├── mock_enrichment_apis/      # Fake Companies House, etc.
│       └── mock_hubspot_dashboard/    # Left-pane Tailwind mock
├── packages/
│   ├── schemas/                       # Pydantic models (shared, extra="forbid")
│   │   ├── lead_intake.py
│   │   ├── lead_prospect.py
│   │   ├── prioritized_queue.py
│   │   ├── dossier.py                 # PreVisitDossier + section schemas
│   │   ├── defect_hypothesis.py       # LikelyDefectClassHypothesis (carried from v1)
│   │   └── risk_register.py
│   ├── adc/                           # Stage 0 deterministic two-route ADC
│   │   └── rules.py
│   ├── enrichment/                    # Deterministic enrichment adapters
│   │   ├── base.py                    # EnrichmentAdapter ABC + circuit breaker
│   │   ├── companies_house.py
│   │   ├── web_scraper.py             # bounded, allowlist-only
│   │   └── linkedin_signal.py         # mocked for demo
│   ├── knowledge_graph/               # Citation-anchored manufacturing graph
│   │   ├── graph.json                 # The data
│   │   ├── loader.py                  # Validates citation provenance at startup
│   │   └── verify.py                  # CI check: every entity has a substrate line
│   └── prompts/                       # Vertex AI prompt templates
│       ├── vertical_flash.py
│       ├── taxonomy_pro.py
│       ├── defect_flash.py
│       ├── comparable_pro.py
│       ├── risk_pro.py
│       └── approach_pro.py
└── scripts/
    ├── seed_mock_data.py
    ├── verify_knowledge_graph.py      # Pre-flight citation check
    └── run_demo.sh                    # Orchestrates the demo flow
```

### 6.2 Critical Pydantic Schemas

```python
# packages/schemas/lead_intake.py
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Literal

class LeadIntakeRow(BaseModel):
    model_config = ConfigDict(extra="forbid")
    external_lead_id: str = Field(..., min_length=1, max_length=128)
    company_name: str = Field(..., min_length=1, max_length=256)
    contact_name: str | None = Field(None, max_length=128)
    contact_email: str | None = Field(None, max_length=256)
    sector_hint: str | None = Field(None, max_length=128)
    raw_notes: str | None = Field(None, max_length=2048)

class LeadIntakeBatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    batch_id: str
    source_label: str = Field(..., max_length=128)   # e.g., "UK_Metals_Expo_2025"
    ingest_user: str
    ingest_timestamp: datetime
    rows: list[LeadIntakeRow] = Field(..., max_length=2000)

# packages/schemas/lead_prospect.py
class LeadProspect(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    external_lead_id: str
    company_name: str
    vertical: Literal[
        "polymer_extrusion", "metal_casting", "additive_manufacturing",
        "fnb_bottling", "electronics_assembly", "aerospace",
        "out_of_vertical", "vertical_uncertain"
    ]
    fitness_score: float = Field(..., ge=0.0, le=1.0)
    enrichment_status: Literal["complete", "partial", "failed"]
    signal_hash: str
    last_scored_at: datetime

# packages/schemas/defect_hypothesis.py (carried forward from v1, adapted)
class LikelyDefectClassHypothesis(BaseModel):
    model_config = ConfigDict(extra="forbid")
    conformal_set: list[Literal[
        "porosity", "dimensional_drift", "surface_inclusions", "tool_wear",
        "calibration_drift", "material_defect", "process_drift", "unknown"
    ]] = Field(..., min_length=0, max_length=8)
    coverage: float = Field(..., ge=0.0, le=1.0)
    requires_human_review: bool = False
    rationale: str = Field(..., max_length=400)

# packages/schemas/dossier.py
class ComparableDeployment(BaseModel):
    model_config = ConfigDict(extra="forbid")
    matta_customer_anchor: Literal[
        "bowers_and_wilkins", "caracol_am", "polymer_unnamed",
        "metal_casting_unnamed", "global_drinks_brand", "no_comparable_available"
    ]
    citation_substrate_line: int  # mandatory, validated against graph at startup
    dimension_of_comparability: str = Field(..., max_length=300)

class PreVisitDossier(BaseModel):
    model_config = ConfigDict(extra="forbid")
    dossier_id: str
    prospect_id: str
    signal_hash: str
    knowledge_graph_version: str
    process_taxonomy: ProcessTaxonomy
    defect_hypothesis: LikelyDefectClassHypothesis
    comparable_deployment: ComparableDeployment
    risk_register: RiskRegister
    suggested_approach: SuggestedApproach
    generated_at: datetime
    requires_human_review_sections: list[str] = Field(default_factory=list)
```

### 6.3 FastAPI Ingress Contracts

Pinned dependency floor (May 2026 stable releases verified via [FastAPI releases](https://github.com/fastapi/fastapi/releases) and [Pydantic changelog](https://docs.pydantic.dev/latest/changelog/)):
`fastapi>=0.136,<0.137`, `pydantic>=2.13,<3`, `google-genai>=1.0`, `celery>=5.5`, `redis>=5.2` (`redis.asyncio` async client, `aclose()` not deprecated `close()`), `sqlalchemy>=2.0,<2.1` (async-first 2.0-style `select()` + `AsyncSession`). FastAPI ≥0.126 dropped Pydantic-v1 support entirely; `@app.on_event("startup"/"shutdown")` is deprecated in favor of the `lifespan` async context manager. Dependencies are typed with `Annotated[T, Depends(...)]` (PEP 593) — the only supported form once mutable defaults are removed in a future minor.

```python
# apps/refinery_api/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
import redis.asyncio as aioredis
from celery import Celery

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = aioredis.from_url(
        settings.redis_url, decode_responses=True, max_connections=64,
    )
    app.state.celery = Celery("refinery", broker=settings.celery_broker)
    try:
        yield
    finally:
        await app.state.redis.aclose()

app = FastAPI(lifespan=lifespan, title="Matta Refinery")

# apps/refinery_api/deps.py
from typing import Annotated
from fastapi import Depends, Request
from redis.asyncio import Redis
from celery import Celery

async def get_redis(request: Request) -> Redis:
    return request.app.state.redis

async def get_celery(request: Request) -> Celery:
    return request.app.state.celery

RedisDep = Annotated[Redis, Depends(get_redis)]
CeleryDep = Annotated[Celery, Depends(get_celery)]
UserDep = Annotated["User", Depends(get_current_user)]

# apps/refinery_api/routers/ingest.py
from typing import Annotated
from fastapi import APIRouter, File, Form, UploadFile

router = APIRouter()

@router.post("/ingest/batch", response_model=IngestAck)
async def receive_batch(
    file: Annotated[UploadFile, File(...)],
    source_label: Annotated[str, Form(...)],
    redis: RedisDep,
    celery: CeleryDep,
    user: UserDep,
) -> IngestAck:
    # Idempotency guard on (file_hash, user, day)
    file_bytes = await file.read()
    file_hash = sha256(file_bytes).hexdigest()
    idempotency_key = f"batch:{file_hash}:{user.id}:{date.today().isoformat()}"

    cached = await redis.get(idempotency_key)
    if cached:
        return IngestAck.model_validate_json(cached)

    # Parse CSV → LeadIntakeBatch (Pydantic 2.13 validation, extra="forbid" rejects unknown columns)
    batch = parse_csv_to_batch(file_bytes, source_label, user)

    # Persist + enqueue
    await persist_batch_and_prospects(batch)
    ack = IngestAck(batch_id=batch.batch_id, status="scoring", row_count=len(batch.rows))
    await redis.set(idempotency_key, ack.model_dump_json(), ex=86400)
    celery.send_task("refinery.score_batch", args=[batch.batch_id])
    return ack

# apps/refinery_api/routers/dossier.py
@router.post("/dossier/generate", response_model=DossierAck)
async def generate_dossier(
    payload: DossierRequest,
    redis: RedisDep,
    celery: CeleryDep,
) -> DossierAck:
    prospect = await fetch_prospect(payload.prospect_id)
    if prospect is None:
        raise HTTPException(404, "prospect not found")
    if prospect.enrichment_status == "failed":
        raise HTTPException(409, "prospect enrichment failed; cannot dossier")

    # Idempotency on (prospect_id, signal_hash, kg_version)
    kg_version = current_knowledge_graph_version()
    idempotency_key = f"dossier:{prospect.id}:{prospect.signal_hash}:{kg_version}"
    cached_dossier_id = await redis.get(idempotency_key)
    if cached_dossier_id and not payload.force_regenerate:
        return DossierAck(dossier_id=cached_dossier_id, status="cached")  # decode_responses=True; str already

    new_id = str(uuid4())
    await redis.set(idempotency_key, new_id, ex=86400 * 7)  # 7d TTL
    celery.send_task("refinery.generate_dossier", args=[prospect.id, new_id])
    return DossierAck(dossier_id=new_id, status="generating")
```

Notes on the modern stack used above:
- `redis.asyncio` is the supported import path on `redis-py` ≥5.2 (the older `aioredis` package is archived); `Redis.aclose()` replaces the sync-deprecated `Redis.close()`.
- Celery workers are configured with `task_acks_late=True`, `task_reject_on_worker_lost=True`, `worker_prefetch_multiplier=1`, and `broker_transport_options={"visibility_timeout": 3600}` on the Redis broker — the Celery 5.5 combination that gives exactly-once-effectively delivery when paired with the Redis idempotency table.
- The Google Gen AI SDK call inside the worker is `client = genai.Client(vertexai=True, project=settings.gcp_project, location="europe-west4")` followed by `client.models.generate_content(model="gemini-3-flash", contents=[...], config=GenerateContentConfig(response_mime_type="application/json", response_schema=RootCauseHypothesis, thinking_config=ThinkingConfig(thinking_level="minimal"), temperature=t))`. The deprecated `vertexai.generative_models.GenerativeModel` API is not imported anywhere.

### 6.4 Vertex AI Prompt Templates

Each prompt template enforces strict JSON output via the Google Gen AI SDK structured-output mode bound to the relevant Pydantic schema (see [Vertex AI structured output docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/maas/capabilities/structured-output)). Output is re-validated against the Pydantic schema as defense-in-depth.

Canonical call pattern (used at every stage):

```python
from google import genai
from google.genai.types import GenerateContentConfig, ThinkingConfig

client = genai.Client(vertexai=True, project=settings.gcp_project, location="europe-west4")

response = await client.aio.models.generate_content(
    model="gemini-3-flash",  # or "gemini-3-1-pro"
    contents=[PROMPT.format(**payload)],
    config=GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=LikelyDefectClassHypothesis,
        thinking_config=ThinkingConfig(thinking_level="minimal"),  # "low" | "medium" per stage
        temperature=t,                                              # 0.1, 0.5, 0.9 for the N=3 fan-out
        max_output_tokens=1024,
    ),
)
parsed = LikelyDefectClassHypothesis.model_validate_json(response.text)
```

**Vertical classification (Gemini 3 Flash, N=3, structured output bound to vertical enum, `thinking_level="minimal"`).** Three parallel calls with `temperature ∈ {0.1, 0.5, 0.9}`, identical other parameters. The wider spread (vs. v1 PRD's 0.0/0.2/0.4) compensates for Gemini 3's tighter default variance under any reasoning level. Plurality vote on `vertical`; on 3-way split, force `vertical_uncertain` and tag the prospect for human review.

**Defect-class hypothesis (Gemini 3 Flash, N=3, structured output bound to `LikelyDefectClassHypothesis`, `thinking_level="minimal"`, temps 0.1 / 0.5 / 0.9).** Three parallel calls returning a categorical distribution over the 8-class defect enum (seven defect classes plus `unknown`). Conformal calibration is applied offline against a labeled holdout; at inference time, the calibrated coverage threshold determines the conformal set inclusion criterion. The prompt explicitly forbids the model from inventing defect categories outside the enum and forbids the model from claiming high coverage when its rationale is ungrounded. `thinking_level="minimal"` is non-negotiable here — Gemini 3's default reasoning trace would mode-collapse the three samples and destroy the deep-ensembles signal that the Brion Filter depends on.

**Comparable deployment (Gemini 3.1 Pro, N=1, structured output bound to `ComparableDeployment`, `thinking_level="low"`).** The prompt is anchored on the citation-provenance-validated knowledge graph: only the six allowed `matta_customer_anchor` values are valid (the fifth is `global_drinks_brand` per the verified citation at substrate lines 540/600; the sixth is `no_comparable_available`). The prompt forbids the model from citing entities outside this list. The `citation_substrate_line` field is validated at startup against the knowledge graph file — any dossier output with a citation line not present in the graph fails Pydantic validation and triggers `requires_human_review`.

**Risk register, Suggested approach (Gemini 3.1 Pro, N=1, structured output bound to fixed taxonomies, `thinking_level="low"`).** Same constraint pattern — fixed enum of risk categories and approach templates. The LLM never invents categories. `thinking_level="low"` is sufficient because the action space is constrained by the hardcoded taxonomy; the model is filling structured fields, not reasoning open-ended.

**Process taxonomy (Gemini 3.1 Pro, N=1, `thinking_level="medium"`).** This is the one section where `thinking_level="medium"` is justified — the model synthesizes across the enrichment payload, vertical assignment, and manufacturing-vertical knowledge graph to produce a line-level production-process taxonomy, which benefits from deeper reasoning. Output is bound to the `ProcessTaxonomy` Pydantic schema.

### 6.5 Knowledge Graph with Citation Provenance

`packages/knowledge_graph/graph.json` — hand-built, ~6 verticals × 5 defect classes per vertical × ~12 anchor entities, total ~360 anchor records. Each record has the structure:

```json
{
  "anchor_id": "matta_deployment_bowers_and_wilkins",
  "vertical": "electronics_assembly",
  "deployment_type": "precision_speaker_components",
  "citation_substrate_lines": [114, 540, 600],
  "citation_verbatim_excerpt": "working with Bowers & Wilkins, where Matta's AI rapidly measures speaker components",
  "permitted_dimensions_of_comparability": [
    "surface_finish_qc",
    "precision_machining_inspection",
    "small_form_factor_metrology"
  ]
}
```

`packages/knowledge_graph/verify.py` runs at container startup. It opens `Matta_Intel_cleaned.md`, validates that every `citation_substrate_lines` reference in the graph still resolves to text containing the `citation_verbatim_excerpt` substring. Any failure aborts container boot. This makes the citation-provenance audit a CI-time and runtime invariant rather than a manual hygiene task.

The graph excludes Cummins as a deployment anchor (Section 1.F disposition). Cummins is permitted only in the demo's left-pane mock data as a hypothetical FDE-bound prospect entity, not as a comparable-deployment citation.

### 6.6 Mock Data Generation

`scripts/seed_mock_data.py` generates a synthetic `UK_Metals_Expo_2025_leads.csv` with 124 rows reflecting plausible UK manufacturing prospects. Approximately 30% of the rows are seeded with company names from line 294 of the substrate (William Cook, Tata Steel, Ernest Wright, Centriblast, Safran Seats GB) — these are real UK Metals Expo attendees per Doug's verbatim post and serve as grounded demo-target names. The remaining 70% are plausible synthetic entities that match UK manufacturing demographics.

The headline demo run uses William Cook Sheffield as the top-ranked prospect (highest fitness score in the seeded distribution) because (a) it's a real UK Metals Expo attendee, (b) ductile iron casting is in Matta's verified vertical surface, and (c) the comparable-deployment anchor (B&W on surface-finish QC) is verifiably present in the knowledge graph. Backup prospects #2 and #3 in the queue (different verticals) are pre-loaded in case the live demo run hits a Vertex AI rate limit during recording.

### 6.7 Demo Recording Flow (Isaac's Production Plan)

1. Hafeedh opens three browser windows tiled: mocked Hubspot dashboard with CSV file (left), Theater UI (center), document preview pane (right). Slack desktop notification mock as bottom-right inset.
2. Hafeedh runs `./scripts/run_demo.sh trigger=william_cook_sheffield`.
3. OBS Studio captures all three panes simultaneously at 1080p / 30fps. Audio recorded separately to a Rode NT-USB; voiceover added in post.
4. Total recording length target: 4–5 minutes. First take is the cold-open / Magic Moment (90 seconds, silent + light sound design). Second take is the technical walkthrough (~90 seconds, voiceover, JSON inspector + citation panel walkthrough). Third take is the verbal Phase 2 + Phase 3 tease (45 seconds, voiceover, no new visuals).
5. Post-production in DaVinci Resolve. Captions auto-generated in Descript and hand-edited.
6. Exported to MP4, uploaded to Vidyard. Timestamp marker placed at 0:18 (Magic Moment dossier completion), per Identity file outreach mechanic. Cold email points to 0:18 in the CTA.

### 6.8 Magic Moment Success Criteria

The demo recording succeeds if and only if all of the following are true:

1. From "Generate dossier" click to dossier completion (all five sections rendered), total elapsed wall time is under 90 seconds (per Pillar 4 ceiling).
2. The Theater pane visibly shows the deterministic two-route ADC decision *separately* from the Stage 2 LLM calls — proving to Sebastian that the routing is rule-based and to Damjan that the data contracts are typed.
3. The defect-class hypothesis section visibly shows the N=3 ensemble votes *and* the conformal coverage calibration step — proving to Doug that the uncertainty layer mirrors his published methodology and is calibrated, not just averaged.
4. The comparable-deployment section visibly shows the citation panel with line numbers into `Matta_Intel_cleaned.md` — proving to all three filters that the dossier is primary-source-grounded, not LLM-fabricated.
5. The dossier `dossier_id` is referenceable via permanent URL after generation (Stage 2 outputs are persistent artifacts, not ephemeral one-shots).
6. Total Vertex AI cost displayed in the cost ticker is under $0.10 for the full dossier generation. Worked estimate at May-2026 EU pricing for the modernized stack: Stage 2.1 process taxonomy (1× Pro `medium`, ~800 in + ~800 out incl. thinking) = $0.0016 + $0.0096 = $0.0112; Stage 2.2 defect-class N=3 Flash (`minimal`, ~600 in + ~250 out each × 3) = $0.0009 + $0.00225 = $0.00315; Stage 2.3 comparable (1× Pro `low`, ~1200 in + ~500 out) = $0.0024 + $0.006 = $0.0084; Stage 2.4 risk (1× Pro `low`, ~800 in + ~600 out) = $0.0016 + $0.0072 = $0.0088; Stage 2.5 approach (1× Pro `low`, ~1000 in + ~700 out) = $0.002 + $0.0084 = $0.0104. **Per-dossier total ≈ $0.042**, leaving ~2.4× headroom against the $0.10 ceiling. Ceiling preserved.

---

## 7. Risk Register

The top three reasons this PRD could fail in front of Doug, Sebastian, or Damjan, with mitigation for each.

### 7.1 Risk: Doug interrogates the prioritization scoring rationale

**Failure mode:** Doug reads the queue output and asks why William Cook ranks above a hypothetical Cummins Daventry prospect (or any other ranking that conflicts with his strategic intuition). He recognizes that the scoring function cannot model his private knowledge about Caracol OEM-partnership status, B&W reference-customer continuity, or the FDE travel calendar. He concludes the sidecar is making decisions it cannot legitimately make. The pitch dies.

**Mitigation:** Lead with the disclaimer ourselves. Frame Stage 1 explicitly as *candidate surfacing*, not *decision-making*. The voiceover script during the technical walkthrough must say: *"Stage 1 doesn't decide who you deploy to next. It surfaces candidates from your raw lead volume — 124 down to 12 worth your team's review — using public-data signals plus deterministic fitness scoring. Strategic context like Caracol partnership status or your team's current travel calendar lives with you, not with the sidecar. Stage 2 is what actually generates value: the FDE chooses which top-12 candidates to dossier, and the dossier is what gets read on the flight to the factory."* Naming the scoring's epistemic limit before Doug does converts a potential objection into a credibility marker. The Stage-1-as-surfacing positioning also moves the conversation away from "is the ranking correct?" to "is the candidate set plausible?" — a much lower bar to clear.

### 7.2 Risk: Sebastian challenges the dossier's defect-class hypothesis

**Failure mode:** Sebastian reads the dossier offline and challenges the epistemic basis for the defect-class section. *"Your model is predicting porosity in a forging process. What's the data backing this? You don't have any deployment data from forging plants. The hypothesis is ungrounded."* If he reads the conformal calibration as window-dressing rather than substantive uncertainty quantification, the entire dossier output is delegitimized.

**Mitigation:** Three layers. First, the conformal calibration must be *real* — computed offline against a labeled holdout from Matta's actual deployment data (B&W defect logs, polymer extrusion deployment data, the verified deployment surface). For the demo, the calibration is computed against a synthetic holdout derived from public manufacturing-defect literature; this MUST be disclosed in the voiceover (*"For this demo the conformal coverage is calibrated against published manufacturing defect distributions; in a production engagement the calibration would run against your actual deployment data, which would tighten the conformal sets significantly"*). Second, when the model has no signal (e.g., a vertical sub-path with no verified Matta deployment), the conformal set returns empty or the section is marked `requires_human_review`. The dossier never produces a confident defect prediction in a domain with no anchor data. Third, the citation panel makes the knowledge-graph provenance visible — Sebastian can click any anchor and see the verbatim line of intel substrate that backs it. Honest about the limit, calibrated where possible, deterministic-fallback where not.

### 7.3 Risk: Damjan rejects the comparable-deployment anchoring as category-error

**Failure mode:** Damjan inspects a dossier's comparable-deployment section and finds it cites Bowers & Wilkins (precision speaker components) as comparable to a forging plant. He sees a category error — "B&W is small-form-factor electronics QC, this is large-component metallurgy, the comparison is sloppy." He concludes the dossier is theater rather than substance, and the entire architecture is suspect.

**Mitigation:** Two layers. First, the `ComparableDeployment` schema includes a mandatory `dimension_of_comparability` field — the LLM cannot ship a comparable without explicitly naming the *axis* on which the comparison holds (e.g., *"surface-finish QC stage similarity"*) and implicitly disclaiming the axes on which it does not (NOT process category, NOT production volume, NOT material). The voiceover script during the technical walkthrough must explicitly call this out: *"The comparable section never claims B&W is comparable to a forging plant on overall process. It claims they share the surface-finish QC stage as a deployment surface — which is the comparable Matta has actually deployed against. The dimension is named explicitly so the FDE can make their own judgment about whether that comparable transfers."* Second, the knowledge graph's `permitted_dimensions_of_comparability` field constrains the LLM at generation time — the model can only choose dimensions from the pre-validated list. Sloppy off-axis comparisons are structurally impossible.

---

## Appendix A — Sections Flagged for Vocabulary Scrubbing if Reused Client-Facing

Per the Identity file: *"this PRD is internal to Kaide Labs and may use Kaide vocabulary (Stateless Sidecar, Revenue Unblocking, DMZ, FDE Strike Team). Outreach materials drafted from this PRD must scrub all internal jargon."*

Sections requiring scrubbing before any client-facing reuse:
- Section 0 (Audit Trail), Section 1 (Red-Team Adjudication) — entire sections are internal posture, never share. Disclosing that we killed two prior architectures on this prospect would be self-defeating.
- Section 2 (Architecture Selection), specifically the Identity-file-deviation justification on statefulness — internal architectural posture.
- Section 3 (FDE Thesis) — strip "FDE Thesis", "Bottleneck Assassin", "Magic Moment", "DMZ", "Revenue Unblocking" before sharing as a "technical brief" if needed.
- Section 7 (Risk Register) — never share; reveals adversarial preparation.

Sections safe for client-facing reuse with light editing:
- Section 4 (System Architecture and Agent Routing) — describes the technical deliverable in neutral terms.
- Section 5 (Native Environment UI Spec) — describes the demo theater in neutral terms.
- Section 6.2 / 6.3 / 6.4 / 6.5 (Schemas, contracts, prompts, knowledge graph) — concrete technical artifacts that demonstrate competence.

---

*End of MATTA_MASTER_PRD_v2.md. Audit trail preserved: `MATTA_MASTER_PRD.md` (v1, CMMS Bridge) is unchanged. `Matta_positioning_final.md` and `Matta_positioning_final_v2.md` are unchanged.*
