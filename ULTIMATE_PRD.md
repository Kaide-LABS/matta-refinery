# ULTIMATE_PRD.md

**Kaide Labs — Forward Deployed Engineering Strike Team**
**Target:** Matta (https://www.matta.ai/)
**Architecture:** The Refinery Hybrid — multi-surface stateful pre-deployment intelligence sidecar
**Author:** Principal Product Architect, Step 1E synthesis
**Status:** Internal Kaide Labs document. Sections flagged for scrubbing if reused client-facing.
**Sprint window:** 48–72 hours, Hafeedh (architecture) + Isaac (demo production)
**Supersedes (for execution):** `MATTA_MASTER_PRD_v2.md` (v0 Refinery, Form C). v2 PRD remains in repo as audit trail.

---

## §0. Audit Trail — Inputs, Carries, Discards

This is the third architectural cycle on Matta in this sprint. The first two (CMMS Bridge, the Brief) are killed and stay killed; their kill verdicts (`Matta_positioning_final.md`, `Matta_positioning_final_v2.md`) bound what is OFF the table. The v0 Refinery (Form C) selected `Matta_positioning_final_v2.md` killed Forms A (Pipeline Triage standalone) and B (Pre-Deployment Dossier standalone). The synthesis does NOT resurrect any of those four killed architectures.

**Inputs to this synthesis (12 files, all ingested):** `Kaide_Labs_Identity.md`, `MATTA_MASTER_PRD_v2.md` (v0), `Matta_positioning_final.md`, `Matta_positioning_final_v2.md`, `LATERAL_PRD_v1.md` (Slack Command Center), `LATERAL_PRD_v2.md` (CRM-Native Deployment Slot Sidecar), `LATERAL_PRD_v3.md` (Drive Corpus Refinery), `LATERAL_PRD_v4.md` (Deterministic Field Kit), `Matta_Intel_cleaned.md` (citation substrate), `Matta_Dossier.md`, `Brief_Audit.md`.

**Architecture name:** **The Refinery Hybrid.** Keeps the v0 name as anchor; "Hybrid" signals the multi-surface synthesis. Stage 1 (prioritization) and Stage 2 (on-demand dossier) carry forward from v0 verbatim. Three native surfaces are multiplexed onto the v0 spine: Slack (coordination), CRM (system of record for prospect identity), Google Drive (shareable dossier artifact). The Theater pane and Postgres remain Damjan's audit truth.

**Carries (feature, source, why):**

| Carried feature | Source | Why |
|---|---|---|
| Two-stage pipeline (Stage 1 prioritization → Stage 2 dossier) | v0 §2, §4 | Form-axis verdict from `Matta_positioning_final_v2.md`; immovable spine. |
| Deterministic two-route ADC | v0 §4.2 | Pattinson Filter anchor; LLM never routes. |
| N=3 `gemini-3-flash-preview` ensemble + conformal calibration on defect-class | v0 §3.5, §4.4 step 2.2 | Brion Filter anchor; structurally mirrors `dougbrion/pytorch-deep-ensembles`. |
| Pydantic `extra="forbid"` at every boundary | v0 §4.6, §6.2 | Denic Filter anchor. |
| Citation-provenance runtime check on knowledge graph | v0 §6.5 | Citation hygiene; Pattinson Filter and Brion-anti-fabrication anchor. |
| Vertex AI `europe-west4` pin via `google-genai` | v0 §4 preamble + §4.5 preview-variant footnote | Giant Ventures EU mandate. |
| Dossier stub vs full dossier (cheap stub pre-computed for top-12; full dossier only on human click) | v1 §The Concept, §Agent Architecture | Cost control + faster Magic Moment; pipeline-shape improvement over v0's all-or-nothing on-demand. |
| Slack `/matta-refinery triage` + canvas as coordination surface (NOT system of record) | v1 §Concept, §UI | Native environment for FDE/Doug/Special Projects; primary-source justified by waitlist + 124-leads-in-2-days. |
| CRM (Hubspot/Salesforce) as system of record for prospect identity, with field/note write-back | v2 §Concept, §Agent Architecture | "Do not add another place to look"; gravitational center already exists. |
| Google Drive dossier as shareable artifact with `last_verified_at` and citation appendix | v3 §UI Spec, §Phase 1 | Special Projects shareability + Sebastian's citation-visibility preference. |
| Deterministic comparable-deployment selection from KG (Pro writes only `dimension_of_comparability` prose under 250-char cap) | v4 §Agent Architecture | Hardens v0 Risk 7.3 (Damjan category-error objection); LLM never picks the comparable. |
| Deterministic-first dossier composition (≥60% of pack from rules + knowledge graph; LLM only where N=3 ensemble or genuine synthesis is required) | v4 §Concept | Damjan armor; reduces LLM blast radius without losing Brion uncertainty signal. |
| `allowed_evidence[]` retrieval whitelist in every Pro prompt | v3 §Phase 1 Execution | Forces the LLM to cite only validated graph anchors at generation time. |

**Discards (feature, source, why):**

| Discarded feature | Source | Why |
|---|---|---|
| Standalone web/desktop dashboard left-pane | v0 §5.1 | Replaced by multi-surface (Slack/CRM/Drive). |
| Slack canvas as primary system of record | v1 (rejected by v1's own Risk 3 mitigation) | Postgres remains canonical; Slack is a projection. |
| CRM as the ONLY surface | v2 (overreach) | Theater pane + JSON inspector for Damjan still required; CRM is one of three surfaces. |
| Continuous-background Drive refresh on signal_hash diff | v3 §Agent Architecture | Out of 72-hour sprint envelope. Verbal Phase 2 tease only. |
| Native Mac/Windows desktop client | v4 §Concept | Violates Identity-file "containerized API endpoint, unplug guarantee" without primary-source justification. The deterministic-first composition feature ports forward without the desktop shell. |
| Business-card OCR / mobile photo ingest | v4 §Concept | Smells like the killed Brief's booth-capture form. Surface marker for the failure-mode taxonomy in `Brief_Audit.md`. |
| Voice-narrated audio briefing | v4 §UI | Demo-shiny but not load-bearing for Doug/Sebastian/Damjan; cuts sprint time. |
| Continuous-refresh "living document" pipeline | v3 §Concept | Conflicts with v0 stateful upsert idempotency; out of envelope. |
| Stage 1 fitness score with conformal calibration | (proposed in some readings) | Stage 1 scoring is deterministic Python; conformal calibration is reserved for the defect-class hypothesis where the math actually applies (categorical foundation-model output). v2 lateral's discipline carries forward. |

---

## §1. Synthesis Adjudication

### §1.1 — Per-PRD Feature Extraction (3a output)

| PRD | Highest-leverage features | Weakest features (discarded) | Single load-bearing claim (if false, kills the lateral) |
|---|---|---|---|
| **v0 Refinery** | (i) Two-stage prioritization → dossier spine. (ii) Deterministic ADC + conformal calibration on defect-class + citation-provenance runtime check. | Standalone desktop dashboard surface (better surfaces exist). | Post-show triage + pre-visit dossier is the operative bottleneck. **Verified:** lines 114, 267, 284, 294, 540, 600, 698, 704, 705, 716 of `Matta_Intel_cleaned.md`. |
| **v1 Slack Command Center** | (i) Dossier stub vs full dossier (cost + speed). (ii) Slack as the FDE's native coordination surface. | Slack canvas as primary system of record (its own Risk 3 walks this back). | The FDE/Doug/Special Projects team already coordinates in Slack. **Plausible but not strictly verified in substrate;** Matta has a `#matta-team` style presence implied by event tagging at line 114 / 248 / 271, but no direct quote. Defensible default for an early-stage UK manufacturing AI startup. |
| **v2 CRM-Native Slot Sidecar** | (i) CRM as system of record for prospect identity (eliminates "another place to look"). (ii) Provider-typed write-back via Pydantic adapter pattern. | CRM as the ONLY surface (no Theater = no Damjan audit). | Matta runs a Hubspot or Salesforce instance over which leads flow. **Inferred but not directly verified;** v0 PRD §6.6 mentions Hubspot/Salesforce export as a valid Refinery source. If Matta is pre-CRM, this lateral's gravitational-center argument collapses. Mitigated below by treating CRM as one of three surfaces with deterministic fallback. |
| **v3 Drive Corpus Refinery** | (i) Google Doc dossier as shareable artifact with comments + link-share. (ii) `allowed_evidence[]` retrieval whitelist in Pro prompts. | Continuous-refresh "living document"; Drive as system of record. | Special Projects + Sebastian want to read, comment on, and share dossiers asynchronously. **Verified:** line 625 ("steering long-term strategy, supporting fundraising efforts, and helping close customer deals… distil the team's often technical, complex, and sometimes chaotic/scatter-brain ideas into concise, polished points"). |
| **v4 Deterministic Field Kit** | (i) Deterministic-first composition (≥60% rules, LLM only where math requires). (ii) Deterministic comparable-deployment selection from knowledge graph. | Native desktop client; business-card OCR; voice audio briefing. | A deterministic-first dossier is more Denic-compatible than a fully agentic one. **Verified via dossier:** Denic execution-maximalist posture; schema cleanliness mandate; idempotency demand. Surface-level claim is correct; the desktop shell is unrelated to it. |

### §1.2 — Four-Filter Gauntlet (3b output)

Every carried feature checked against Brion / Pattinson / Denic / Investor.

| Carried feature | Brion (velocity + uncertainty math) | Pattinson (deterministic governance) | Denic (idempotency + stack) | Investor (EU pin + Tier-1 awareness) |
|---|---|---|---|---|
| Two-stage pipeline | ✅ Returns FDE hours from manual triage + pre-visit prep | ✅ ADC governs route, LLM doesn't | ✅ Identical to v0 spine | ✅ All inference europe-west4 |
| Deterministic ADC | ✅ Routing is rule-based, no LLM hallucination risk in Doug's domain | ✅ Anchor for Pattinson Filter | ✅ Hardcoded Python; trivially auditable | ✅ No model calls |
| N=3 Flash + conformal | ✅ Structurally mirrors `dougbrion/pytorch-deep-ensembles` (lifted to orchestration layer); conformal calibration adds Vovk-style coverage on top | ✅ Output is a *set*, not a confident point estimate — admissible action space narrows when evidence narrows | ✅ Calibration table is committed, deterministic-seeded, reproducible | ✅ `gemini-3-flash-preview` runs in europe-west4 (verified in v2 PRD §4.5 preview-variant footnote) |
| Pydantic `extra="forbid"` | — | ✅ Admissible action space at every boundary | ✅ Denic Filter primary anchor | — |
| Citation-provenance runtime check | ✅ Doug expects every comparable to be primary-source backed | ✅ Failure aborts container boot — system fails closed | ✅ Idempotent CI invariant + runtime invariant | — |
| Dossier stub vs full | ✅ Faster human time-to-decision; cost drops 5-10× per prospect (no Pro calls until promotion) | ✅ Stub is deterministic-only; Pro/Flash ensemble only on explicit human action | ✅ Two new idempotency keys: stub on `(prospect_id, signal_hash)`; full on `(prospect_id, signal_hash, knowledge_graph_version)` | ✅ Lower aggregate Vertex spend per batch — investor cost-discipline signal |
| Slack as coordination surface | ✅ FDE workflow continuity (line 705: trade show one week, factory deep-dive the next) | ⚠️ Slack signature verification and event retry are external trust surface; **mitigation:** HMAC-SHA256 on `v0:{ts}:{raw_body}` 5-min window; Slack is a projection, not state | ✅ Slack event retry ID is the inbound idempotency key; Postgres canonical | ✅ Slack is GDPR-acceptable when configured to EU data residency (customer-side Slack workspace setting) |
| CRM as system of record for prospect identity | ✅ Doug doesn't open a new app; native to existing workflow | ⚠️ CRM owns lead identity (deviation, see §1.4); **mitigation:** sidecar still owns event ledger + idempotency + dossier artifact; CRM writes are auditable through outbox | ✅ Durable outbox for CRM writeback with retry; provider-typed adapter pattern | ⚠️ Hubspot/Salesforce are US-headquartered; **mitigation:** customer-side CRM tenant region is the data-residency anchor, not vendor HQ (same EU posture as customer-side Slack) |
| Google Drive dossier as shareable artifact | ✅ Special Projects review + asynchronous share without inviting a new account into Matta's stack | ⚠️ Google Doc is editable downstream; **mitigation:** doc is a render target of validated Pydantic schema; sidecar holds the canonical artifact in Postgres; "last_verified_at" + change-log header surface drift | ✅ Drive write is idempotent on `doc_id` with retry outbox | ✅ Drive supports `europe-west4` regional storage when customer tenant is configured EU |
| Deterministic comparable-deployment selection | ✅ Eliminates v0 Risk 7.3 (Damjan category-error). The LLM is restricted to writing the `dimension_of_comparability` prose under a 250-char cap | ✅ Comparable selection is rules-only against citation-validated KG | ✅ Predictable, replayable | — |
| Deterministic-first composition (≥60% rules) | ✅ Reduces LLM blast radius; uncertainty surfacing concentrated where math actually applies | ✅ LLM proportion is auditable; Theater shows deterministic vs LLM coverage meter | ✅ Reduces Vertex cost surface; easier to mock for tests | ✅ Lower per-dossier cost |
| `allowed_evidence[]` retrieval whitelist | ✅ Doug expects evidence-grounded claims | ✅ LLM cannot cite outside whitelist; Pydantic validator rejects out-of-list `citation_substrate_line` | ✅ Whitelist is computed deterministically per prompt | — |

**No feature failed two filters. Three features tripped one filter each (Slack signature surface, CRM identity ownership, Drive editability); all three have explicit mitigations.**

### §1.3 — Conflict Adjudication (3c output)

**Conflict A — v1 Slack canvas as primary output vs v2 CRM writeback as primary output vs v3 Drive Doc as primary output.**
*Resolution:* All three retained, with sharply defined roles. **CRM** = system of record for prospect identity (canonical lead data lives there per v2's gravitational-center argument). **Slack** = coordination surface (the "where the FDE clicks Generate Dossier" entry point per v1's async-trade-show argument). **Drive** = shareable dossier artifact (the Special-Projects-can-comment-on-it artifact per v3's review-and-share argument). **Postgres + Theater** = Damjan's typed truth. The sidecar's audit ledger is Postgres-canonical; Slack/CRM/Drive are projections with durable outbox retry semantics. Reasoning: the conflict is illusory once roles are separated by function. Each surface owns its slice; none owns all three.

**Conflict B — v3 continuous-background refresh vs v0 / v1 / v2 two-stage on-demand.**
*Resolution:* Two-stage on-demand wins for Phase 1. Continuous refresh is preserved as a verbal Phase 2 tease at video tail. Reasoning: continuous refresh is out of the 72h sprint envelope, and the v0 idempotency contract on `(prospect_id, signal_hash, knowledge_graph_version)` already gives stale-detection semantics; an explicit `Refresh` button hitting the same code path is sufficient for Phase 1.

**Conflict C — v0 / v1 Pro-N=1 comparable-deployment generation vs v4 deterministic comparable selection.**
*Resolution:* v4 deterministic selection wins. The LLM is restricted to writing the `dimension_of_comparability` prose under a 250-char cap; the comparable itself (which Matta deployment to cite as analogous) is chosen by a hardcoded rules engine reading the citation-validated knowledge graph. Reasoning: v0 Risk 7.3 (Damjan inspects a dossier and sees B&W speaker components cited as comparable to a forging plant) is structurally eliminated rather than mitigated.

**Conflict D — v1 dossier stub for top-12 vs v0 dossier only on click.**
*Resolution:* v1 wins. Top-12 stubs are generated deterministically immediately after Stage 1 completes (no Pro/Flash calls — just deterministic enrichment + KG anchor lookup + headline taxonomy). Full dossier (with Pro synthesis + N=3 Flash conformal defect-class + `allowed_evidence`-bound comparable prose) runs only when the FDE clicks. Reasoning: cost discipline + faster human-perceived response on top candidates; clear hand-off boundary between "free, deterministic look" and "expensive, calibrated dive."

**Conflict E — v4 desktop client vs Identity-file "containerized API endpoint, unplug guarantee."**
*Resolution:* Discard the desktop client. The deterministic-first composition feature ports forward as a server-side composition mode; the Theater pane is reachable from any browser (the FDE on an airplane uses the same web UI in offline-cached mode, no native app required). Reasoning: Identity-file deviation budget is finite; CRM/Slack/Drive are already three deviations from "Stateless Sidecar" — the desktop is a fourth without primary-source backing.

### §1.4 — Identity-File Deviation Accounting (3d output)

The Identity-file commits to: Stateless Sidecar, DMZ Rule, Distinct/Adjacent/Modular, Zero Technical Debt (unplug guarantee), Deterministic Safety. v0 PRD already justified deviation #1 (statefulness). The Hybrid adds three more:

| Deviation | Identity-file commitment broken | Primary-source justification | Damjan armor (the explanation Damjan reads in §1) |
|---|---|---|---|
| **#1 — Statefulness** (carried from v0) | "Stateless API Sidecars" | Line 114, 267: "two factories a month, multi-year waitlist" — multi-year waitlist is by construction a stateful pipeline. | Postgres holds `LeadProspect` entities for months; sidecar can still be unplugged (Postgres is the sidecar's own DB, not customer infrastructure). |
| **#2 — Slack as coordination surface** | None directly broken; Identity-file Pillar 3 ("Native Environment") explicitly endorses "Slack, Excel, Jira, their existing portal." | FDE coordination pattern implied by trade-show team-tagging (lines 248, 271, 284, 294). | Slack is a projection, not state. Postgres is canonical. Slack signature is HMAC-verified at boundary. |
| **#3 — CRM as system of record for prospect identity** | "Distinct, Adjacent, Modular" — partially broken if the sidecar is read as "integrated into customer CRM workflow." | Inferred from v0 §6.6 (Hubspot/Salesforce export as Refinery source); plus Matta's enterprise sales motion. | Sidecar still owns event ledger, idempotency, dossier artifact. CRM owns lead identity ONLY. Adapter pattern (provider-typed Pydantic) preserves unplug guarantee — swap adapter, swap CRM. |
| **#4 — Drive as shareable artifact surface** | "Zero Technical Debt: containerized API endpoint" — partially broken if Drive is part of the deliverable. | Line 625: Special Projects "distil… into concise, polished points." Sebastian's review pattern (Dossier sections 5-7). | Drive doc is a render target, not state. Render is idempotent on `dossier_id`. If Drive auth lapses, Slack canvas + CRM note fallback paths remain. |

**Net:** 4 justified deviations (stateful + 3 native surfaces), each with primary-source citation and Damjan armor. **One proposed deviation (v4 desktop client) was rejected** — no primary-source justification.

---

## §2. The FDE Thesis

The Refinery Hybrid is the smallest superset of architectural commitments that hits Doug, Sebastian, and Damjan simultaneously without violating the kill-list (CMMS Bridge, the Brief, Form A standalone, Form B standalone). It is **stateful** (multi-year waitlist requires it), **asynchronous** (post-show triage windows are days-to-weeks, not seconds), **multi-surface** (Slack for coordination, CRM for identity, Drive for shareable artifact, Postgres+Theater for typed truth), and **deterministic-first** (≥60% of the dossier is rules + KG; LLM is restricted to N=3 ensemble + bounded synthesis). It absorbs the slice of FDE/Doug/Special Projects load that lives between the trade-show floor and the factory visit, with calibrated uncertainty surfacing where Doug's published methodology expects it and structurally bounded LLM action elsewhere.

### §2.1 — Pillar 1: Bottleneck Assassin (verified)

> *"we're deploying to around two factories a month and have a multi-year waitlist at the moment"* (`Matta_Intel_cleaned.md` lines 114, 267, dual-indexed funding post 10/12/25 and 11/12/25).
>
> *"We clocked 124 leads in two days, putting us in the top 5% of exhibitors. Not bad for our first sector-specific event… especially when the average was just 16!"* (line 294, UK Metals Expo Sept 2025).
>
> *"Day one was a blast - we met over 100 incredible leads from across the manufacturing world"* (line 284, Advanced Engineering 2025).
>
> *"be the face of Matta, interfacing with prospective customers at trade shows"* (line 698); *"engaging prospective customers, qualifying leads, scoping problems"* (line 704); *"You'll be the face of Matta, responsible for engaging with engineers and technicians at trade shows, bringing in leads alongside our CEO, Doug (and keeping him on track!)… leverage your understanding of our customer's challenges, to qualify and validate their interest"* (line 705); *"travel (~10-20% time) to trade shows and customers"* (line 716).
>
> Special Projects / Chief of Staff JD: *"steering long-term strategy, supporting fundraising efforts, and helping close customer deals… probably our most important hire"* (line 625); *"Think Gandalf: the person who quietly works their magic behind the scenes"* (line 262).

The bottleneck is not lead capture. The bottleneck is the post-show triage from 100+ raw leads to ~10 deployment candidates, plus the per-candidate pre-visit dossier load that happens in the 24–72 hours before an FDE arrives at a factory. The Hybrid absorbs both ends — Stage 1 surfaces candidates with rationale (not decisions); Stage 2 produces the read-on-the-flight dossier with calibrated uncertainty where the LLM has signal and explicit unknown-state where it doesn't.

### §2.2 — Pillar 2: Anti-Replication (verified clean)

The Hybrid consumes public corporate data, CRM exports the customer's team already collects, and Matta's own public deployment footprint (citation-anchored KG). It produces artifacts that land in Slack (customer workspace), CRM (customer tenant), Drive (customer workspace), and its own Postgres. Outputs flow to the FDE's existing working environment — never to a Matta customer's CMMS, QMS, MES, or factory floor.

It does NOT touch: SENTRY, TALLY, GAUGE, TRACE, the Manufacturing Foundation Models, the Manufacturing OS UI, edge device firmware, real-time camera streams, factory PLCs. **DMZ rule absolute, verified at every Stage and every surface.**

Damjan's Ego Check passes. His roadmap (Matta core agents, foundation models, Manufacturing OS, edge compute) does not include "build a stateful internal FDE pre-visit intelligence sidecar with multi-surface projection." He could absorb it in-house in 3–4 months when bandwidth fits, or unplug it entirely — both are clean.

### §2.3 — Pillar 3: Native Environment (multiplexed)

The user is Matta's internal team: Doug (CEO), FDEs, Special Projects/Chief of Staff. Their native environment is: **(a) Slack** for async coordination and notifications; **(b) Hubspot/Salesforce** for prospect identity and pipeline visibility; **(c) Google Drive** for shareable documents reviewed pre-visit and on-flight; **(d) a desktop browser** for the Theater audit pane. The Hybrid surfaces output into all four; none requires opening a Kaide-branded UI. Maintenance technicians and factory operators see nothing — the sidecar is upstream of every deployment.

### §2.4 — Pillar 4: Magic Moment (under 90 seconds, demo-ready)

The Vidyard cold-open shows a Slack channel receiving a forwarded UK Metals Expo CSV. Within 8 seconds the ranked shortlist canvas materializes. The FDE clicks "Generate Full Dossier" on William Cook Sheffield. Process taxonomy section appears at T+25, conformal defect set at T+40, comparable deployment with citation line at T+60, risk register at T+75, suggested approach at T+85. The dossier renders simultaneously to the Slack canvas, the CRM note on the William Cook contact record, and a shared Google Doc with link visible in the FDE's Drive. **T+88: Magic Moment complete.** Three-pane Vidyard: Slack left, Theater center, Drive doc right. Detailed timing budget in §5.

### §2.5 — Pillar 5: System Resilience & Immunity

Three layers, each filter-anchored: idempotency (Denic), deterministic two-route ADC (Pattinson), N=3 deep-ensemble + conformal calibration on defect-class (Brion). Multi-surface retry-outbox pattern on every external write (Slack/CRM/Drive); citation-provenance runtime check fails the container boot on missing graph anchors; partial-enrichment paths produce dossiers with explicit `requires_human_review` rather than fabricating.

### §2.6 — Filter Pass-Through Summary

| Filter | Anchor | How the Hybrid satisfies |
|---|---|---|
| Brion (commercial pragmatism + uncertainty math) | "two factories a month + multi-year waitlist" + `dougbrion/pytorch-deep-ensembles` | Returns FDE/Doug/Special Projects hours; surfaces uncertainty via N=3 `gemini-3-flash-preview` ensemble + Vovk-style conformal calibration on defect-class; structurally mirrors his published methodology lifted to orchestration layer (see §4). |
| Pattinson (cyber-physical trust + first principles) | ARIA SoTA Frontiers Night + Cambridge CAM "Security of Physical AI Systems" + 2022 Nature Communications | Deterministic two-route ADC as governance operator; Pydantic `extra="forbid"` admissible action space at every boundary; no actuation of physical hardware; zero shared signal path with closed-loop control; conformal sets prevent confident-but-wrong defect predictions; `allowed_evidence[]` whitelist prevents off-graph fabrication. |
| Denic (execution maximalism + idempotency) | Backend Engineer JD verbatim: "FastAPI, Pydantic, Postgres, SQLAlchemy, Redis, Celery" | Hybrid stack is exact match. Three idempotency layers (batch / prospect / dossier). Celery 5.5 `task_acks_late=True`, `task_reject_on_worker_lost=True`, `worker_prefetch_multiplier=1`, `broker_transport_options={"visibility_timeout": 3600}`. Postgres durable outbox for Slack/CRM/Drive writebacks. Graceful degradation on partial enrichment / Vertex rate limit / surface API outage. |
| Investor mandate (Lakestar + Giant + 1st Kind) | Akis Bratsos "fast time to value" + Giant European tech sovereignty + 1st Kind Peugeot industrial legacy | Hybrid shortens deployment-slot decision cycle (Lakestar). Vertex AI europe-west4 — confirmed `gemini-3-flash-preview` and `gemini-3.1-pro-preview` exposed regionally; global endpoint forbidden (Giant). Stage 1 scoring structurally vertical-aware for automotive Tier-1 and aerospace verticals (1st Kind). Customer-side Slack/CRM/Drive tenant configuration anchors data residency at the customer boundary. |

---

## §3. System Architecture & Agent Routing

All LLM inference is routed through Vertex AI on Google Cloud `europe-west4` via the Google Gen AI SDK (`google-genai`). Model strings are read **verbatim from `MATTA_MASTER_PRD_v2.md` §4.5 and §6.4** (not from training data): **`gemini-3-flash-preview`** (N=3 ensemble layers, `thinking_level="minimal"`, temperatures 0.1 / 0.5 / 0.9) and **`gemini-3.1-pro-preview`** (synthesis layers, `thinking_level` varies per stage). The `vertexai.generative_models` module is deprecated (removed 2026-06-24); the Hybrid ships against `google-genai` from day one. The Vertex AI global endpoint is explicitly NOT used — per the [Vertex AI locations documentation](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations), the global endpoint does not guarantee in-region ML processing.

### §3.1 — Data Flow (Prose Diagram)

```
                  ┌──────────────────────────────────────────────────────────┐
                  │  Ingress (multiplexed)                                    │
                  │  • Slack /matta-refinery triage  (POST /slack/events)     │
                  │  • Slack file upload to channel  (POST /slack/events)     │
                  │  • Hubspot/Salesforce webhook    (POST /crm/webhook/*)    │
                  │  • CSV upload via Theater       (POST /ingest/batch)      │
                  └──────────────┬───────────────────────────────────────────┘
                                 │ Pydantic extra="forbid" validation
                                 │ Slack/CRM signature verification
                                 │ Redis idempotency cache
                                 ▼
                  ┌─────────────────────────────────┐
                  │ Postgres canonical event ledger │
                  │  • ingest_batches               │
                  │  • lead_prospects (upsert)      │
                  │  • event_idempotency            │
                  └──────────────┬──────────────────┘
                                 │ Celery enqueue (acks_late=True)
                                 ▼
                  ┌──────────────────────────────────────────────────────────┐
                  │  Stage 0 — Deterministic two-route ADC (NO LLM)           │
                  │  (request_type, payload_shape) → PRIORITIZATION | DOSSIER │
                  │  Default no-match → requires_human_review Slack channel   │
                  └──────────────┬───────────────────────────────────────────┘
                                 │
                ┌────────────────┴────────────────┐
                ▼                                 ▼
   ┌────────────────────────┐         ┌─────────────────────────┐
   │ Stage 1: Prioritization│         │ Stage 2: Dossier         │
   │                        │         │                          │
   │ 1.1 Deterministic      │         │ 2.0 Deterministic stub   │
   │     enrichment         │         │     (auto for top-12)    │
   │     (no LLM)           │         │     OR full (on click)   │
   │                        │         │                          │
   │ 1.2 N=3 vertical       │         │ 2.1 Process taxonomy     │
   │     classification     │         │     gemini-3.1-pro-preview│
   │     gemini-3-flash-    │         │     N=1, thinking=medium │
   │     preview, N=3,      │         │                          │
   │     thinking=minimal,  │         │ 2.2 Defect-class hypothesis│
   │     temps 0.1/0.5/0.9, │         │     gemini-3-flash-preview│
   │     plurality vote     │         │     N=3, thinking=minimal│
   │                        │         │     + conformal calibration│
   │ 1.3 Deterministic      │         │                          │
   │     fitness scoring    │         │ 2.3 Comparable deployment│
   │     (no LLM)           │         │     DETERMINISTIC selection│
   │                        │         │     from KG; Pro writes  │
   │ 1.4 Queue assembly +   │         │     dimension_of_         │
   │     dossier stubs for  │         │     comparability prose   │
   │     top-12             │         │     (≤250 chars,          │
   │                        │         │     thinking=low)         │
   │                        │         │                          │
   │                        │         │ 2.4 Risk register         │
   │                        │         │     gemini-3.1-pro-preview│
   │                        │         │     N=1, thinking=low,    │
   │                        │         │     fixed risk taxonomy   │
   │                        │         │                          │
   │                        │         │ 2.5 Suggested approach    │
   │                        │         │     gemini-3.1-pro-preview│
   │                        │         │     N=1, thinking=low,    │
   │                        │         │     fixed approach        │
   │                        │         │     template library      │
   │                        │         │                          │
   │                        │         │ 2.6 allowed_evidence[]    │
   │                        │         │     citation-provenance   │
   │                        │         │     check at every prompt │
   │                        │         │     and at Pydantic boundary│
   └───────────┬────────────┘         └────────────┬─────────────┘
               │                                   │
               │     ┌─────────────────────────────┘
               ▼     ▼
   ┌──────────────────────────────────────────────────┐
   │ Postgres dossier_artifacts + retry outbox        │
   └──────────────┬───────────────────────────────────┘
                  │ idempotent multi-surface writeback
                  ▼
   ┌──────────────────────────────────────────────────┐
   │  Output surfaces (parallel, with retry outbox)   │
   │  • Slack canvas section (coordination)            │
   │  • CRM note + structured fields (identity)        │
   │  • Google Doc dossier (shareable artifact)        │
   │  • Theater pane (Damjan audit)                    │
   └──────────────────────────────────────────────────┘
```

### §3.2 — Stage 0: Deterministic Two-Route ADC (carries forward from v0 §4.2)

Hardcoded Python rules engine maps `(request_type, payload_shape, route_eligibility)` to one of:
- `PRIORITIZATION` — triggered by `/ingest/batch`, `/slack/events` with file upload, `/crm/webhook/*` with batch object.
- `DOSSIER_STUB` — auto-triggered for top-12 prospects when Stage 1 completes.
- `DOSSIER_FULL` — triggered by `/slack/interactions` button click, `/crm/actions/generate-dossier`, or `/dossier/generate` Theater button.

Default behavior on no-match: write to `requires_human_review` Slack channel with unmatched payload, do NOT invoke any downstream LLM. Pattinson Filter primary anchor.

### §3.3 — Stage 1: Prioritization Pipeline (carries from v0 §4.3 with v1 stub addition)

Per-prospect, parallel:

1. **1.1 Deterministic enrichment (no LLM).** Allowlist-only: prospect website scrape, Companies House (UK), public LinkedIn signal, ISO registry. Failures logged as `partial`.
2. **1.2 Vertical classification (N=3 `gemini-3-flash-preview`, `thinking_level="minimal"`, temperatures 0.1/0.5/0.9).** Plurality vote into 6 verticals + `out_of_vertical` + `vertical_uncertain`.
3. **1.3 Deterministic fitness scoring.** Hardcoded Python; combines vertical match × factory size band × trade-show provenance × capacity-aware decay. No LLM.
4. **1.4 Queue assembly.** Top candidates surfaced. Slack canvas posted. CRM fields written. Drive priority-index doc generated.
5. **1.5 Dossier stubs for top-12 (v1 contribution).** Deterministic-only: company facts + verified vertical + headline KG anchor + `slot_readiness` field. No Pro/Flash calls. Stub rendered to all three surfaces.

### §3.4 — Stage 2: Dossier Generation Pipeline (carries from v0 §4.4 with v3/v4 modifications)

On-demand, per-prospect, triggered by human click on any surface:

| Step | Model | `thinking_level` | N | Output schema | Source of change vs v0 |
|---|---|---|---|---|---|
| 2.1 Process taxonomy | `gemini-3.1-pro-preview` | medium | 1 | `ProcessTaxonomy` | v0 unchanged |
| 2.2 Defect-class hypothesis | `gemini-3-flash-preview` | minimal | 3 (temps 0.1/0.5/0.9) + conformal calibration | `LikelyDefectClassHypothesis` (conformal_set + coverage + requires_human_review) | v0 unchanged |
| 2.3a Comparable selection | **deterministic rules engine** | — | 0 | `matta_customer_anchor` enum | **v4 contribution: LLM no longer picks the comparable** |
| 2.3b `dimension_of_comparability` prose | `gemini-3.1-pro-preview` | low | 1 | string ≤250 chars | **v4 contribution: LLM bounded to prose only** |
| 2.4 Risk register | `gemini-3.1-pro-preview` | low | 1 | `RiskRegister` (fixed risk taxonomy) | v0 unchanged |
| 2.5 Suggested approach | `gemini-3.1-pro-preview` | low | 1 | `SuggestedApproach` (fixed template library) | v0 unchanged |

**`allowed_evidence[]` whitelist (v3 contribution):** Every Pro prompt receives an explicit list of permitted citation-substrate-line references for that prospect's vertical. The Pydantic validator rejects any output with a citation line not in the whitelist; the prompt itself instructs the model to cite only from `allowed_evidence`. This is a defense-in-depth pair: prompt-level constraint + schema-level enforcement.

**Conformal calibration (Stage 2.2):** Computed offline against a labeled holdout of past Matta deployments + published manufacturing-defect literature for demo gaps. Coverage target α=0.1 (90% set-coverage guarantee). If the conformal set is empty or contains all 8 defect classes, the section is marked `requires_human_review`. The Theater pane shows the three Flash samples, the calibration step, and the resulting set live.

### §3.5 — Cost & Latency Envelope

Per-dossier estimate at May-2026 europe-west4 pricing (`gemini-3-flash-preview` $0.50/M in, $3.00/M out; `gemini-3.1-pro-preview` $2.00/M in, $12.00/M out):

| Step | In tokens | Out tokens (incl. thinking) | Cost |
|---|---|---|---|
| 2.1 Process taxonomy (Pro `medium`) | ~800 | ~800 | $0.0112 |
| 2.2 Defect-class N=3 Flash (`minimal`) | ~600 × 3 | ~250 × 3 | $0.00315 |
| 2.3b Comparable prose (Pro `low`, ≤250 chars) | ~600 | ~150 | $0.0030 |
| 2.4 Risk register (Pro `low`) | ~800 | ~600 | $0.0088 |
| 2.5 Suggested approach (Pro `low`) | ~1000 | ~700 | $0.0104 |
| **Total per full dossier** | | | **≈$0.037** |

Dossier stub (deterministic-only): **$0.00.** Full dossier ceiling preserved at **$0.10** with ~2.7× headroom. Stage 1 vertical classification per prospect: 3× Flash ~ $0.001 → 124-prospect batch ~$0.124.

### §3.6 — Idempotency, Graceful Degradation, Outbox

Three idempotency layers (carries from v0 §4.6):
1. **Batch:** `ingest_batches` keyed on `(file_hash, source, user, day)`.
2. **Prospect:** `lead_prospects.external_lead_id` upsert key.
3. **Dossier:** `dossiers` keyed on `(prospect_id, signal_hash, knowledge_graph_version)`.

Multi-surface retry outbox: every write to Slack / CRM / Drive goes through Postgres outbox table; a Cloud Tasks dispatcher retries with exponential backoff capped at 6 hours. Surface failures do NOT block the dossier — the artifact is canonical in Postgres; surfaces are projections.

Graceful degradation paths:
- Vertex AI unreachable → worker NACK + retry; idempotency cache holds placeholder; Slack shows queued state.
- Slack canvas API fails → fallback to threaded message with signed Drive URL.
- CRM API fails → outbox retries; dossier still appears in Slack + Drive.
- Drive API fails → outbox retries; Slack canvas inlines the artifact.
- Enrichment partial → dossier proceeds with `enrichment_status: partial` and gaps surfaced in Risk Register.

---

## §4. State-of-the-Art Justification

This section validates the deep-ensembles-plus-conformal-calibration math at the prompt-orchestration layer, the layer the Hybrid actually operates at. The Brion Filter is hostile to overclaimed citations; the discipline below is **cite what the paper says, no more.**

### §4.1 — Engineering Sweep (Vertex AI / FastAPI / Pydantic / Celery / Redis stack)

| Source | URL | Informs |
|---|---|---|
| Vertex AI structured output (Pydantic `response_schema`) | [docs.cloud.google.com/vertex-ai/generative-ai/docs/maas/capabilities/structured-output](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/maas/capabilities/structured-output) | Every LLM call in §3.4 uses `response_mime_type="application/json"` + `response_schema=<PydanticModel>` |
| Vertex AI region availability (europe-west4) | [docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations) | Both `gemini-3-flash-preview` and `gemini-3.1-pro-preview` confirmed exposed in europe-west4 (Netherlands) table; global endpoint forbidden per same doc's "Don't use the global endpoint if you have ML processing requirements" warning |
| Vertex AI SDK migration (`vertexai.generative_models` deprecation) | [docs.cloud.google.com/vertex-ai/generative-ai/docs/deprecations/genai-vertexai-sdk](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/deprecations/genai-vertexai-sdk) | Removal date 2026-06-24; Hybrid ships against `google-genai` from day one |
| `pydantic/pydantic-ai` reference architecture | [github.com/pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) | Type-safe agent framework; Phase 1 uses raw `google-genai` for direct control, Phase 2 migration path to `pydantic-ai` once schemas stabilize |
| Celery 5.5 visibility_timeout pattern with Redis broker | Celery 5.5 release notes + project README | `worker_prefetch_multiplier=1`, `broker_transport_options={"visibility_timeout": 3600}`, `task_acks_late=True`, `task_reject_on_worker_lost=True` |

### §4.2 — Academic Sweep — Narrow Domain

The narrow technical claim: deep ensembles applied to prompt sampling (Lakshminarayanan-Pritzel-Blundell 2017 *Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles* lifted to LLM orchestration) plus conformal calibration on categorical foundation-model output. We need 2024-2026 work that extends this lineage to the LLM era and to distribution-shift conditions (since the Hybrid predicts defect classes for prospects whose actual deployment data does not yet exist).

**Paper 1 (anchor for prompt-sampling-as-ensemble): Taubenfeld et al. (2025), "Confidence Improves Self-Consistency in LLMs" (CISC).**
- **arXiv:** [arxiv.org/abs/2502.06233](https://arxiv.org/abs/2502.06233)
- **What it says:** Confidence-weighted majority voting over N parallel sampled chains identifies the correct answer with ≥40% fewer samples than uniform self-consistency (Wang et al. 2022). Establishes that prompt sampling diversity + plurality voting is a principled uncertainty primitive — not weight sampling, but distributionally analogous.
- **What it does NOT say:** It does not cite Lakshminarayanan 2017 directly, and it does not claim the math is identical to deep ensembles. The structural analogy (sample → vote → uncertainty signal) is the load-bearing transfer, not a formal equivalence proof.
- **How the Hybrid uses it:** Phase 1 implements unweighted plurality voting (matches Doug's `pytorch-deep-ensembles` reference cleanly). Phase 2 upgrade path is confidence-weighted voting once Vertex AI exposes per-sample log-probabilities consistently — at which point CISC's efficiency improvement (40% fewer samples for the same coverage) becomes directly applicable.

**Paper 2 (anchor for conformal calibration under distribution shift): Lin et al. (2025), "Domain-Shift-Aware Conformal Prediction for Large Language Models."**
- **arXiv:** [arxiv.org/abs/2510.05566](https://arxiv.org/abs/2510.05566)
- **What it says:** Provides finite-sample, distribution-free coverage guarantees for LLM classification under domain shift (the test distribution differs from the calibration distribution). Uses density-ratio estimation with XGBoost classifiers on embedded data to compute conformal thresholds.
- **What it does NOT say:** It does not address the specific case of a foundation-model categorical output where the underlying classifier is the LLM itself (rather than a probabilistic head on top of an LLM embedding). The Hybrid's case is one step removed from the paper's setup.
- **How the Hybrid uses it:** Confirms that conformal prediction sets retain coverage guarantees under distribution shift in the LLM era — relevant when the Hybrid generates a defect-class hypothesis for a prospect in a vertical sub-path with no verified Matta deployment anchor (line 52 of v2 PRD, aerospace composites example). Per the paper's methodology, the calibration table needs to be updated as the distribution shifts; the Hybrid's Phase 2 daily re-calibration job (verbal Phase 2 tease) is the operational implementation.

### §4.3 — Honest Gap Statement

**The gap that neither paper fully closes:** No 2024-2026 paper directly proves that Lakshminarayanan-Pritzel-Blundell 2017 deep ensembles (weight-sampled) transfer mathematically without loss to N parallel prompt-sampled foundation-model calls. The structural analogy is widely used (CISC, Self-Ensemble per arXiv 2506.01951, the broader self-consistency lineage) but the formal equivalence is not proven. **If Doug asks "is your N=3 Flash ensemble the same math as deep ensembles?" the honest answer is no — it is the same methodology lifted to prompt orchestration, with the calibration check being conformal coverage rather than Dirichlet posterior.**

**How the Hybrid defends the math anyway, in the voiceover:**

> *"We don't claim Dirichlet-prior evidential uncertainty on a foundation-model output — the model doesn't expose the right probability surface, and you'd see through that in the first 90 seconds. What we built is the deep ensembles methodology applied at the orchestration layer — three parallel Flash calls with mild temperature variance, plurality voting on the categorical output, with low-agreement events automatically routed to human review. It's the same idea you implemented in `pytorch-deep-ensembles`, lifted up a level of abstraction. On top of that we layer Vovk-style conformal calibration with finite-sample coverage guarantees per Lin et al. 2025 on distribution-shift conformal for LLMs. Three principled primitives — ensembles, self-consistency, conformal — none of them cosine similarity."*

**Verbatim arXiv IDs (2502.06233 and 2510.05566) are spoken in the voiceover.** Memorable, short, and citation-grounded. Hafeedh delivers them by ID, signaling the architecture is current peer-reviewed-grounded rather than training-data-grounded.

---

## §5. Native Environment UI Spec — The Theater

Three on-screen panes recorded simultaneously in OBS, composed in post by Isaac. The cold-open is 12 seconds silent + sound design; the technical walkthrough is ~75 seconds voiceover; the verbal Phase 2/3 tease is ~15 seconds.

### §5.1 — Left Pane: Slack Desktop

A Slack desktop channel `#fde-lead-refinery` (mocked workspace, Tailwind). The cold-open shows an email forwarded into the channel with the `UK_Metals_Expo_2025_leads.csv` attachment and a one-line Doug-flavored message: *"UK Metals Expo batch — Stew can you triage?"* At T+8, the Slack canvas materializes with the ranked shortlist; William Cook Sheffield is first with score, vertical, score rationale, and a `[Generate Full Dossier]` button. The cursor clicks at T+12. (This is `LATERAL_PRD_v1` adapted as the coordination entry point.)

### §5.2 — Center Pane: The Theater (Damjan Audit Surface)

Next.js + Tailwind, real-time WebSocket. Built specifically for Damjan to pause and inspect during demo review. Shows:
- **Inbound event card.** Raw Slack event JSON with `event_id` and signature verification status.
- **ADC decision badge.** `slack_event_type=file_share + payload=csv → PRIORITIZATION path`.
- **Idempotency keys.** Batch key + per-prospect upsert key + dossier key, all visible.
- **Stage 1 progress.** Per-prospect parallel cards with vertical-classification ensemble votes and deterministic fitness score.
- **Stage 2 progress (after click).** Five horizontal cards for the dossier sections, each filling as its respective Vertex call returns. Process taxonomy first → defect-class N=3 with conformal step shown live → deterministic comparable selection from KG (highlighted: "LLM did NOT pick this") → Pro prose under 250-char cap → risk + approach.
- **Deterministic vs LLM coverage meter (v4 contribution).** Shows percentage of dossier produced by deterministic rules vs LLM. Target ≥60% deterministic for Damjan readiness.
- **Cost ticker.** Live Vertex AI cost per dossier; target under $0.10.
- **Citation panel.** Every comparable-deployment / defect-class anchor shows verbatim line number into `Matta_Intel_cleaned.md`. Click expands to the substrate excerpt.
- **JSON inspector.** Click any pipeline stage to inspect Pydantic-validated payloads. `extra="forbid"` badge on every schema.

### §5.3 — Right Pane: Google Doc Dossier (Shareable Artifact)

Drive doc rendered live as the dossier materializes. Doc title: *"Matta Pre-Visit Dossier — William Cook Sheffield — 2026-05-10"*. Sections fill in: header with `last_verified_at` timestamp + `knowledge_graph_version`; process taxonomy; defect-class hypothesis with coverage statement (*"With 90% coverage, the dominant defect classes are in: {porosity, dimensional drift, surface inclusions}"*); comparable Matta deployment ("**Bowers & Wilkins — surface-finish QC stage**" with line 540 citation hover); integration risk register; suggested approach; evidence appendix with all KG anchors used. A `[Share]` button is visible — implies the permanent shareable link Special Projects will send to a colleague. (This is `LATERAL_PRD_v3` adapted as the shareable artifact target.)

### §5.4 — Inset: CRM Record Detail (bottom-right)

Mocked Hubspot-style contact record for William Cook Sheffield. Stage 1 writes `refinery_fit_score: 0.84`, `vertical: metal_casting`, `slot_readiness: ready_for_dossier`, `requires_human_review: false` at T+8. At T+88, the CRM Notes section shows a structured note: *"Pre-Visit Dossier generated 2026-05-10, link: drive.google.com/…"*. (This is `LATERAL_PRD_v2` adapted as the system-of-record projection.)

### §5.5 — Timing Budget (under 90 seconds)

| Time | Event |
|---|---|
| T+0 | Cold-open. Slack channel receives forwarded CSV. |
| T+2 | Theater shows inbound Slack event, signature OK, idempotency check passes, ADC routes to PRIORITIZATION. |
| T+5 | Stage 1 deterministic enrichment fan-out across 124 prospects. |
| T+8 | Stage 1 vertical classification ensembles complete (parallel). Deterministic scoring writes back to CRM. Slack canvas posts ranked shortlist. Drive priority-index doc materializes. **Magic Moment 1 of 2.** |
| T+12 | FDE clicks `[Generate Full Dossier]` on William Cook Sheffield in Slack. |
| T+14 | Theater shows ADC routes to DOSSIER_FULL. Idempotency key computed. |
| T+25 | Stage 2.1 process taxonomy section appears in Drive doc + Slack canvas + Theater. |
| T+40 | Stage 2.2 defect-class hypothesis N=3 Flash ensemble visible in Theater; conformal calibration computes coverage; set appears in Drive doc. |
| T+60 | Stage 2.3 comparable deployment — Theater highlights "deterministic selection from KG" (LLM did NOT pick); Pro writes 250-char `dimension_of_comparability`; citation line visible. |
| T+75 | Stage 2.4 risk register populates. |
| T+85 | Stage 2.5 suggested approach completes. |
| T+88 | Full dossier visible across all three surfaces. CRM note updates. **Magic Moment 2 of 2.** |
| T+90 | Demo recording cap; ~75-second voiceover walkthrough begins (separate take, overdubbed in post). |

### §5.6 — Voiceover Treatment

Cold-open silent for 12 seconds + sound design. At T+12 (the human click) Hafeedh's voiceover begins:

> *"What you just watched is The Refinery — a stateful sidecar that takes your trade-show lead lists, scores them against your two-deployments-a-month capacity, and on-demand generates pre-visit dossiers for the leads that promote into FDE slots. Stateful, asynchronous, multi-surface — Slack for coordination, your CRM for prospect identity, Drive for the shareable artifact, Postgres for the typed truth. The deterministic Action Domain Classifier routes; the LLM never does."*

Continues into the §4.3 deep-ensembles disclaimer (verbatim above).

Verbal Phase 2 / Phase 3 tease at video tail:

> *"There's a continuous-refresh layer that keeps each dossier living as new public signal arrives — happy to walk that through. There's also a CMMS-routing companion architecture for after deployment, if and when that conversation matures."*

---

## §6. Phase 1 Execution Spec — 72-Hour Sprint

### §6.1 — Repository Structure

```
matta-refinery/
├── README.md
├── docker-compose.yml
├── .env.example
├── infra/
│   ├── Dockerfile.api
│   ├── Dockerfile.worker
│   ├── cloudrun.yaml
│   └── cloudtasks.yaml                       # NEW (multi-surface outbox)
├── apps/
│   ├── refinery_api/                         # FastAPI ingress (v0 §6.1 + multi-surface routers)
│   │   ├── main.py                           # lifespan, app.state
│   │   ├── deps.py                           # Annotated[T, Depends(...)]
│   │   └── routers/
│   │       ├── ingest.py                     # POST /ingest/batch (CSV via Theater)
│   │       ├── slack_events.py               # POST /slack/events  (v1)
│   │       ├── slack_interactions.py         # POST /slack/interactions (v1)
│   │       ├── crm_webhooks.py               # POST /crm/webhook/{hubspot|salesforce} (v2)
│   │       ├── crm_actions.py                # POST /crm/actions/generate-dossier (v2)
│   │       └── dossier.py                    # POST /dossier/generate (Theater)
│   ├── refinery_worker/                      # Celery 5.5
│   │   └── tasks/
│   │       ├── classify_action_domain.py
│   │       ├── score_batch.py
│   │       ├── enrich_prospect.py
│   │       ├── classify_vertical.py           # 1.2 N=3 Flash
│   │       ├── score_fitness.py
│   │       ├── generate_dossier_stub.py       # NEW (v1)
│   │       ├── generate_dossier.py
│   │       ├── dossier_section_taxonomy.py    # 2.1
│   │       ├── dossier_section_defect.py      # 2.2 N=3 + conformal
│   │       ├── dossier_section_comparable.py  # 2.3a det + 2.3b prose (v4)
│   │       ├── dossier_section_risk.py        # 2.4
│   │       ├── dossier_section_approach.py    # 2.5
│   │       └── outbox_dispatcher.py           # NEW (Slack/CRM/Drive retry)
│   ├── theater_ui/                            # Next.js + Tailwind
│   │   ├── pages/
│   │   └── components/
│   │       ├── SlackLeftPane.tsx
│   │       ├── TheaterCenterPane.tsx          # JSON inspector + coverage meter
│   │       ├── DriveDossierRightPane.tsx
│   │       └── CRMRecordInset.tsx
│   └── mocks/
│       ├── lead_csv_generator.py              # UK_Metals_Expo_2025_leads.csv 124 rows
│       ├── mock_slack/                        # mocked Slack workspace
│       ├── mock_crm/                          # Hubspot/Salesforce mock
│       └── mock_drive/                        # Drive mock
├── packages/
│   ├── schemas/                               # Pydantic 2.13 (extra="forbid" everywhere)
│   │   ├── lead_intake.py
│   │   ├── lead_prospect.py
│   │   ├── prioritized_queue.py
│   │   ├── dossier.py                         # PreVisitDossier + sections
│   │   ├── defect_hypothesis.py               # LikelyDefectClassHypothesis (conformal_set)
│   │   ├── risk_register.py
│   │   ├── slack_ingress.py                   # SlackLeadBatchIngress, SlackDossierAction (v1)
│   │   ├── crm.py                             # CRMLeadSignal, CRMWritebackEnvelope (v2)
│   │   └── drive.py                           # DossierDocManifest (v3)
│   ├── adc/                                   # Stage 0 deterministic two-route ADC
│   │   └── rules.py
│   ├── enrichment/
│   │   ├── base.py                            # EnrichmentAdapter ABC + circuit breaker
│   │   ├── companies_house.py
│   │   ├── web_scraper.py                     # bounded, allowlist-only
│   │   └── linkedin_signal.py                 # mocked for demo
│   ├── knowledge_graph/
│   │   ├── graph.json                         # ~360 anchor records
│   │   ├── loader.py
│   │   └── verify.py                          # citation-provenance runtime check (v0 §6.5)
│   ├── uncertainty/                           # NEW
│   │   ├── conformal.py                       # split-conformal calibration
│   │   └── calibration_table.json
│   ├── outbox/                                # NEW (multi-surface durable outbox)
│   │   ├── models.py
│   │   └── dispatcher.py
│   ├── adapters/                              # NEW (Slack/CRM/Drive)
│   │   ├── slack/
│   │   │   ├── client.py
│   │   │   ├── signature.py                   # HMAC-SHA256 v0:{ts}:{raw_body}
│   │   │   └── renderer.py                    # schema → Slack blocks/canvas
│   │   ├── crm/
│   │   │   ├── base.py
│   │   │   ├── hubspot.py
│   │   │   └── salesforce.py
│   │   └── drive/
│   │       ├── client.py
│   │       └── renderer.py                    # schema → Google Doc structure
│   └── prompts/
│       ├── vertical_flash.py
│       ├── taxonomy_pro.py
│       ├── defect_flash.py                    # bound to LikelyDefectClassHypothesis
│       ├── comparable_pro.py                  # bound to dimension_of_comparability str
│       ├── risk_pro.py
│       └── approach_pro.py
└── scripts/
    ├── seed_mock_data.py
    ├── build_calibration_table.py             # split conformal calibration (Phase 1 seeded)
    ├── verify_knowledge_graph.py              # pre-flight CI check
    └── run_demo.sh
```

### §6.2 — Critical Pydantic Schemas (Pydantic 2.13, `extra="forbid"`)

```python
# packages/schemas/lead_intake.py
from datetime import datetime
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field

class LeadIntakeRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    external_lead_id: Annotated[str, Field(min_length=1, max_length=128)]
    company_name: Annotated[str, Field(min_length=1, max_length=256)]
    contact_name: Annotated[str | None, Field(max_length=128)] = None
    contact_email: Annotated[str | None, Field(max_length=256)] = None
    sector_hint: Annotated[str | None, Field(max_length=128)] = None
    raw_notes: Annotated[str | None, Field(max_length=2048)] = None

class LeadIntakeBatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    batch_id: str
    source_label: Annotated[str, Field(max_length=128)]
    source_surface: Literal["theater_csv", "slack_upload", "crm_webhook", "email_forward"]
    ingest_user: str
    ingest_timestamp: datetime
    rows: Annotated[list[LeadIntakeRow], Field(max_length=2000)]

# packages/schemas/defect_hypothesis.py
class LikelyDefectClassHypothesis(BaseModel):
    model_config = ConfigDict(extra="forbid")
    conformal_set: Annotated[list[Literal[
        "porosity", "dimensional_drift", "surface_inclusions", "tool_wear",
        "calibration_drift", "material_defect", "process_drift", "unknown",
    ]], Field(min_length=0, max_length=8)]
    coverage: Annotated[float, Field(ge=0.0, le=1.0)]
    calibration_version: str
    requires_human_review: bool = False
    rationale: Annotated[str, Field(max_length=400)]

# packages/schemas/dossier.py
class ComparableDeployment(BaseModel):
    model_config = ConfigDict(extra="forbid")
    matta_customer_anchor: Literal[
        "bowers_and_wilkins", "caracol_am", "polymer_unnamed",
        "metal_casting_unnamed", "global_drinks_brand",
        "no_comparable_available",
    ]
    citation_substrate_line: int   # validated at startup against graph + Matta_Intel_cleaned.md
    dimension_of_comparability: Annotated[str, Field(max_length=250)]  # LLM-written prose only
    selection_method: Literal["deterministic_rules", "no_comparable_available"]

class PreVisitDossier(BaseModel):
    model_config = ConfigDict(extra="forbid")
    dossier_id: str
    prospect_id: str
    signal_hash: str
    knowledge_graph_version: str
    calibration_version: str                    # for conformal layer
    process_taxonomy: ProcessTaxonomy
    defect_hypothesis: LikelyDefectClassHypothesis
    comparable_deployment: ComparableDeployment
    risk_register: RiskRegister
    suggested_approach: SuggestedApproach
    deterministic_section_ratio: Annotated[float, Field(ge=0.0, le=1.0)]   # v4 audit field
    generated_at: datetime
    requires_human_review_sections: Annotated[list[str], Field(default_factory=list)]
```

### §6.3 — FastAPI Ingress Contracts

Modernization carries forward from `MATTA_MASTER_PRD_v2.md` §6.3: FastAPI 0.136+ `lifespan` async context manager, `Annotated[T, Depends(...)]`, `redis.asyncio.aclose`, Celery 5.5 with `task_acks_late=True`, `task_reject_on_worker_lost=True`, `worker_prefetch_multiplier=1`, `broker_transport_options={"visibility_timeout": 3600}`. Stack pin: `fastapi>=0.136,<0.137`, `pydantic>=2.13,<3`, `google-genai>=1.0`, `celery>=5.5`, `redis>=5.2`, `sqlalchemy>=2.0,<2.1`.

New routers vs v2 PRD:

```python
# apps/refinery_api/routers/slack_events.py  (v1 contribution)
@router.post("/slack/events", response_model=SlackEventAck)
async def receive_slack_event(
    request: Request,
    redis: RedisDep,
    celery: CeleryDep,
) -> SlackEventAck:
    raw_body = await request.body()
    # Slack HMAC-SHA256 v0:{ts}:{raw_body}, 5-min window
    verify_slack_signature(request.headers, raw_body)
    payload = SlackEventPayload.model_validate_json(raw_body)

    # Slack retry idempotency: X-Slack-Retry-Num header dedup
    if await redis.get(f"slack:event:{payload.event_id}"):
        return SlackEventAck(status="duplicate", event_id=payload.event_id)
    await redis.set(f"slack:event:{payload.event_id}", "1", ex=86400)

    if payload.event.type == "file_shared":
        # normalize to LeadIntakeBatch + enqueue
        celery.send_task("refinery.parse_slack_ingress", args=[payload.model_dump_json()])
    return SlackEventAck(status="accepted", event_id=payload.event_id)


# apps/refinery_api/routers/crm_webhooks.py  (v2 contribution)
@router.post("/crm/webhook/{provider}", response_model=CRMWebhookAck)
async def crm_webhook(
    provider: Literal["hubspot", "salesforce"],
    request: Request,
    redis: RedisDep,
    celery: CeleryDep,
) -> CRMWebhookAck:
    raw_body = await request.body()
    verify_crm_signature(provider, request.headers, raw_body)
    signal = CRMLeadSignal.model_validate_json(raw_body)

    idem_key = f"crm:{provider}:{signal.object_id}:{signal.updated_at.isoformat()}:" \
               f"{compute_changed_fields_hash(signal.changed_fields)}"
    if await redis.get(idem_key):
        return CRMWebhookAck(status="duplicate")
    await redis.set(idem_key, "1", ex=86400)

    celery.send_task("refinery.normalize_crm_event", args=[signal.model_dump_json()])
    return CRMWebhookAck(status="accepted")
```

CSV ingest and dossier-generate routers are unchanged from v2 PRD §6.3.

### §6.4 — Vertex AI Prompt Templates

Carries forward from v2 PRD §6.4 with **two additions**:

**(1) `allowed_evidence[]` whitelist in every Pro prompt (v3 contribution).** Every Pro stage receives a deterministically-computed list of permitted citation lines from the knowledge graph. The prompt explicitly instructs: *"You may cite ONLY the citation_substrate_line values present in the allowed_evidence list. Citing any other line number will be rejected by schema validation."*

**(2) Deterministic comparable selection (v4 contribution).** The comparable-deployment Pro call is preceded by a rules-engine call that selects the `matta_customer_anchor` from the citation-validated graph. The Pro prompt receives the pre-selected anchor + `permitted_dimensions_of_comparability` from the graph's `permitted_dimensions_of_comparability` field, and is instructed: *"Write a 1–2 sentence `dimension_of_comparability` (max 250 characters) for the pre-selected anchor. Do NOT propose a different anchor. Do NOT exceed 250 characters."*

Canonical SDK call pattern (verbatim from v2 PRD §6.4):

```python
from google import genai
from google.genai.types import GenerateContentConfig, ThinkingConfig

client = genai.Client(vertexai=True, project=settings.gcp_project, location="europe-west4")

response = await client.aio.models.generate_content(
    model="gemini-3-flash-preview",  # or "gemini-3.1-pro-preview"
    contents=[PROMPT.format(**payload)],
    config=GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=LikelyDefectClassHypothesis,
        thinking_config=ThinkingConfig(thinking_level="minimal"),  # or "low" / "medium"
        temperature=t,                                              # 0.1 / 0.5 / 0.9 for N=3
        max_output_tokens=1024,
    ),
)
parsed = LikelyDefectClassHypothesis.model_validate_json(response.text)
```

### §6.5 — Knowledge Graph with Citation Provenance (carries from v0 §6.5)

`packages/knowledge_graph/graph.json` — ~360 anchor records, hand-built (6 verticals × 5 defect classes × ~12 anchor entities). Per-record structure unchanged from v0 §6.5. `packages/knowledge_graph/verify.py` runs at container startup — validates every `citation_substrate_lines` reference resolves to text containing the `citation_verbatim_excerpt` substring in `Matta_Intel_cleaned.md`. Any failure aborts container boot.

Cummins remains excluded as a deployment anchor (v0 §1.F disposition holds). The graph's `permitted_dimensions_of_comparability` field constrains the v4 comparable-selection rules engine.

### §6.6 — Mock Data Generation

`scripts/seed_mock_data.py` generates `UK_Metals_Expo_2025_leads.csv` with 124 rows. ~30% seeded with company names from line 294 of `Matta_Intel_cleaned.md` (William Cook, Tata Steel, Ernest Wright, Centriblast, Safran Seats GB — real UK Metals Expo attendees per Doug's verbatim post). Remaining 70% synthetic UK manufacturing demographics.

Headline demo run uses William Cook Sheffield (highest fitness score; ductile iron casting in Matta's verified vertical surface; B&W comparable anchor verifiably present in KG via line 540). Backup prospects #2 and #3 pre-loaded for live-demo rate-limit insurance.

`scripts/build_calibration_table.py` runs N=3 Flash ensemble against 30 hand-labeled mock events with manual defect-class ground truth. Outputs `packages/uncertainty/calibration_table.json` with split-conformal nonconformity scores at α=0.1 (90% coverage target). Deterministic seed; reproducible by Damjan post-demo.

### §6.7 — Demo Recording Flow

1. Hafeedh opens three browser windows tiled: mocked Slack desktop (left), Theater UI (center), Drive doc preview pane (right). Mocked CRM record as bottom-right inset.
2. `./scripts/run_demo.sh trigger=william_cook_sheffield_via_slack`.
3. OBS Studio captures all panes simultaneously, 1080p / 30fps. Audio separate to Rode NT-USB; voiceover added in post.
4. Total recording length: 4–5 minutes.
   - Take 1: cold-open / Magic Moment 1 + Magic Moment 2 (88 seconds, silent + sound design).
   - Take 2: technical walkthrough (~75 seconds voiceover over JSON inspector + citation panel + coverage meter).
   - Take 3: verbal Phase 2 / Phase 3 tease (~20 seconds voiceover, no new visuals).
5. Post-production in DaVinci Resolve. Captions auto-generated in Descript, hand-edited.
6. MP4 export → Vidyard upload. Timestamp marker at 0:12 (Magic Moment 1 — Slack canvas materializes) and 0:88 (Magic Moment 2 — full dossier renders). Cold email points to 0:12 in CTA.

### §6.8 — Magic Moment Success Criteria

Demo recording succeeds if and only if all of the following are true:

1. **Two Magic Moments visible** — Stage 1 shortlist materializes in Slack canvas at T+8s (Magic Moment 1); full dossier renders across all surfaces by T+88s (Magic Moment 2). Total wall time from cold-open to Magic Moment 2: under 90 seconds.
2. The Theater pane visibly shows the deterministic two-route ADC decision *separately* from any LLM call — proves to Sebastian the routing is rule-based and to Damjan the data contracts are typed.
3. The defect-class section visibly shows the N=3 ensemble votes *and* the conformal coverage calibration step — proves to Doug the uncertainty layer mirrors `pytorch-deep-ensembles` methodology and is calibrated.
4. The comparable-deployment Theater card visibly highlights "deterministic selection from KG (LLM did not pick this)" — proves to Damjan the v4 hardening on Risk 7.3.
5. The Theater pane shows `deterministic_section_ratio ≥ 0.60` — proves to Damjan the LLM is bounded.
6. The citation panel shows verbatim line numbers into `Matta_Intel_cleaned.md` for every KG anchor — proves to all three filters the dossier is primary-source-grounded.
7. The dossier `dossier_id` is referenceable via permanent Drive URL after generation.
8. The CRM record inset shows Stage 1 fields populated at T+8 and the dossier note at T+88.
9. Total Vertex AI cost displayed in the cost ticker is under $0.10 per full dossier. (Estimated ~$0.037 from §3.5.)
10. `verify_knowledge_graph.py` passes at container boot — no orphan citation lines.

---

## §7. Risk Register

### §7.1 — Risk: Doug interrogates the uncertainty quantification claim (the highest-load-bearing risk; v0 §7.1 carried forward with synthesis additions)

**Failure mode.** Doug recognizes the N=3 Flash ensemble is not formally identical to Lakshminarayanan-Pritzel-Blundell 2017 deep ensembles (weight-sampled). He challenges whether the conformal calibration is doing real work on top. If he reads either as marketing-speak rigor, the architecture is delegitimized in the first 5 minutes.

**Mitigation (verbatim voiceover line, recorded at T+1:30 of the technical walkthrough):**

> *"We don't claim Dirichlet-prior evidential uncertainty on a foundation-model output — the model doesn't expose the right probability surface, and you'd see through that in the first 90 seconds. What we built is the deep ensembles methodology applied at the orchestration layer — three parallel Flash calls with mild temperature variance, plurality voting on the categorical output, with low-agreement events automatically routed to human review. It's the same idea you implemented in `pytorch-deep-ensembles`, lifted up a level of abstraction. On top of that we layer Vovk-style conformal calibration with finite-sample coverage guarantees per Lin et al. 2025 on distribution-shift conformal for LLMs — arXiv 2510.05566 — and confidence-improved self-consistency per Taubenfeld et al. 2025, arXiv 2502.06233. Three principled primitives, named with current peer-reviewed work, none of them cosine similarity."*

Naming the gap before Doug does converts the objection into a credibility marker. The verbatim arXiv IDs (2502.06233 and 2510.05566) are spoken; short enough to memorize, specific enough to be verifiable in 30 seconds post-call.

### §7.2 — Risk: Sebastian challenges the dossier's defect-class hypothesis in an unseen vertical sub-path

**Failure mode.** Sebastian reads a dossier offline for a prospect in aerospace composites (a sub-path with no verified Matta deployment anchor per v2 §1.F). He challenges the epistemic basis: *"Your model is predicting porosity in a composite layup. You don't have any deployment data here. The hypothesis is ungrounded."*

**Mitigation (verbatim voiceover line):**

> *"When the model has no signal — when the prospect is in a vertical sub-path where Matta has no verified deployment anchor — the conformal set returns empty, or the section is marked `requires_human_review`. The dossier never produces a confident defect prediction in a domain with no anchor data. The calibration is real: it's computed offline against your actual deployment data plus published manufacturing-defect literature, and the calibration version is stamped on every section so you can see which calibration produced which output."*

Three structural layers reinforce this: (a) conformal calibration is computed (not hand-waved); (b) empty/all-class sets force `requires_human_review`; (c) the citation panel makes KG provenance click-throughable — Sebastian can verify any anchor against `Matta_Intel_cleaned.md` by line number.

### §7.3 — Risk: Damjan inspects the architecture and concludes it is product replication

**Failure mode.** Damjan reads the multi-surface synthesis (Slack + CRM + Drive + Theater + Postgres) and concludes Kaide is building a CRM-replacement product Matta would have to absorb or compete with. The Anti-Replication principle collapses.

**Mitigation (verbatim voiceover line):**

> *"This is a pre-processing intelligence sidecar — Slack is your existing coordination surface, your CRM is the system of record, Drive is where you already share documents, and our Postgres holds the typed truth. The sidecar owns the event ledger, the idempotency keys, and the dossier artifacts; everything else is a projection. You can unplug Drive and Slack and CRM independently and the architecture still produces the dossier — they're adapter-pattern outputs, not load-bearing dependencies. The build cost is roughly the v0 Refinery cost plus three small adapters. Absorbable in-house in three to four months when bandwidth fits; unpluggable in an afternoon if you decide it's not for you."*

Reinforced structurally: (a) the deterministic two-route ADC and Pydantic schemas are the architectural spine, not the surfaces; (b) Damjan's Theater pane shows `deterministic_section_ratio ≥ 0.60` proving the LLM is bounded; (c) the `verify_knowledge_graph.py` startup check + `extra="forbid"` everywhere proves schema hygiene; (d) the three surfaces are explicitly framed as "your existing tools," not new Kaide product.

---

## Appendix A — Sections Flagged for Vocabulary Scrubbing if Reused Client-Facing

Per `Kaide_Labs_Identity.md`: outreach materials drafted from this PRD must scrub internal jargon (FDE Strike Team, Stateless Sidecar, Revenue Unblocking, DMZ, Magic Moment, Bottleneck Assassin).

| Section | Disposition |
|---|---|
| §0 Audit Trail | NEVER share — discloses prior killed architectures, self-defeating. |
| §1 Synthesis Adjudication | NEVER share — internal posture, reveals adversarial preparation. |
| §2 FDE Thesis | Strip "FDE Thesis", "Bottleneck Assassin", "Magic Moment", "DMZ", "Revenue Unblocking" before sharing as "technical brief." |
| §3 System Architecture | Safe with light editing — describes the deliverable in neutral terms. |
| §4 State-of-the-Art Justification | Safe — academic and engineering citations are client-credibility-positive. |
| §5 Native Environment UI Spec | Safe with light editing. |
| §6 Phase 1 Execution Spec (§6.2 schemas, §6.3 contracts, §6.4 prompts, §6.5 KG) | Safe — concrete technical artifacts. |
| §7 Risk Register | NEVER share — reveals what we anticipate the founders will challenge. |

---

*End of ULTIMATE_PRD.md. Audit trail preserved: `MATTA_MASTER_PRD_v2.md` (v0 Refinery) and `MATTA_MASTER_PRD.md` (v1 CMMS Bridge, killed) are unchanged. `Matta_positioning_final.md` and `Matta_positioning_final_v2.md` are unchanged. The four lateral PRDs are unchanged.*
