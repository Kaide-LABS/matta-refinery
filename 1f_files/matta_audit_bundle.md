═══════════════════════════════════════════════════════════════
FILE: ULTIMATE_PRD.md
PURPOSE: The architecture to audit. The Refinery Hybrid — multi-surface stateful pre-deployment intelligence sidecar synthesized from the v0 Master PRD plus four lateral PRDs.
═══════════════════════════════════════════════════════════════

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


═══════════════════════════════════════════════════════════════
END FILE: ULTIMATE_PRD.md
═══════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════
FILE: Matta_Intel_cleaned_numbered.md
PURPOSE: Primary citation substrate. Every line is prefixed with its original 1-indexed line number (format: NNNN\t<content>). When citing in the audit, reference these original line numbers, NOT positions in the merged bundle. The file is the same content as Matta_Intel_cleaned.md at the repo root, with line-number prefixes added for citation addressability.
═══════════════════════════════════════════════════════════════

0001	CLEANUP REPORT
0002	Original file lines: 2702
0003	Cleaned file lines: 635
0004	UI chrome lines removed: 2067
0005	Duplicate blocks flagged: 2
0006	Ambiguous content flagged: 3
0007	Approximate signal density: 4 founder-attributed claims per 50 lines (target: ≥1)
0008	
0009	[CLEANER NOTE: inferred section boundary]
0010	Company & Team Roster
0011	
0012	Matta
0013	Creating industrial AI for factory sentience
0014	Software Development
0015	London
0016	11-50 employees
0017	
0018	14 associated members
0019	
0020	Madelene Larsson
0021	Partner @ Giant Ventures | ex-Revolut, ex-JPM
0022	[CLEANER NOTE: unclear if signal — (Hamza Fetuga is a mutual connection)]
0023	
0024	Damjan Denic
0025	CTO, Matta MPhil Advanced Computer Science, Cambridge
0026	
0027	Zhiyu Shang
0028	AI Msc in Imperial College
0029	
0030	Tom Walker
0031	Product Lead at Matta | MPhil ISMM at University of Cambridge | Berkeley SkyDeck Batch 16
0032	
0033	Nikhil Raghavan
0034	MSc AI @ Imperial
0035	
0036	Sebastian Pattinson
0037	Associate Professor at University of Cambridge; Co-Founder at Matta
0038	
0039	Douglas Brion
0040	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0041	
0042	Mickie Guinea Oyamburu
0043	Venture Capital at Lakestar
0044	
0045	Jake Moll
0046	FDE at Matta
0047	
0048	Carmelo del Coso Ameijide
0049	Backend Engineer at Matta
0050	
0051	Matthew Judge
0052	Founding Engineer at Matta
0053	
0054	Sri Ayangar
0055	Investor @ Lakestar (ML, Dev Tools, Cyber)
0056	
0057	Ollie Rosen
0058	Founding AI Scientist at Matta Labs
0059	
0060	Ashir Sharjeel
0061	[CLEANER NOTE: unclear if signal — (--)]
0062	[CLEANER NOTE: unclear if signal — (LinkedIn Member)]
0063	Field Staff at Matta
0064	
0065	Ulysse Laroche
0066	Investor | 1stkind (backed by Peugeot FO)
0067	
0068	[CLEANER NOTE: inferred section boundary]
0069	Recent Activity & Announcements
0070	
0071	We've been waiting to announce this for almost two years...
0072	
0073	Giant portfolio company Matta is out of stealth - and they've raised $14 million to use AI to build sentient factories.
0074	
0075	We led Cambridge spin-out Matta’s pre-seed. Now in their latest round they’ve been backed by Lakestar, InMotion Ventures, Redseed, 1st Kind (Peugeot family), Unruly Capital, and Boost VC.
0076	
0077	Douglas Brion's core vision is to change how everything is made.
0078	
0079	Factories still rely on the human skill of people who just know when something is off. The engineer who hears a wobble. The operator who spots a flaw before anyone else. Matta is capturing that tacit knowledge in AI.
0080	
0081	Matta’s AI system learns any production line within days. Their fastest learning was just 5 minutes. It spots defects, traces root causes, and then helps the line fix itself.
0082	
0083	It is already running in polymer plants, casting lines, bottling halls and with global clients like Caracol AM and Bowers & Wilkins.
0084	
0085	Matta is reducing waste, speeding up production, allowing Europe and UK to radically innovate manufacturing and how we make everything.
0086	
0087	Congatulations to Douglas Brion, Sebastian Pattinson, and the whole Matta team! Article by Freya Pratty in comments.
0088	
0089	[CLEANER NOTE: duplicate of Giant Ventures announcement at L165-181]
0090	
0091	[CLEANER NOTE: inferred section boundary]
0092	Career History
0093	
0094	Contact www.linkedin.com/in/sebastianpattinson-09519010b (LinkedIn) www.sebastianpattinson.com/ (Personal) Languages English (Native or Bilingual) German (Native or Bilingual) Honors-Awards NSF Science, Engineering, and Education for Sustainability Postdoctoral Fellowship EPSRC Doctoral Training Grant MIT Translational Fellowship EPSRC Masters Training Grant Best Poster Prize MIT Mechanical Engineering Department Micro/Nano Conference Publications Google Scholar Profile Sebastian Pattinson Associate Professor at University of Cambridge; Co-Founder at Matta Cambridge, England, United Kingdom Summary Associate Professor at Cambridge and Co-Founder of Matta Labs, developing manufacturing systems that learn how to make things better. Experience University of Cambridge 7 years 9 months Associate Professor March 2023 - Present (3 years 3 months) Assistant Professor September 2018 - March 2023 (4 years 7 months) Department of Engineering Matta Co-Founder 2022 - Present (4 years) MIT NSF Postdoctoral Fellow 2014 - 2018 (4 years) Department of Mechanical Engineering X, the moonshot factory X Moonshot Fellow June 2017 - November 2017 (6 months) Analysis of early pipeline projects Education Massachusetts Institute of Technology Postdoc, Mechanical Engineering University of Cambridge Doctor of Philosophy (PhD), Materials Science University of Cambridge Master of Philosophy - MPhil, Micro- and Nanotechnology Enterprise University of York Bachelor of Science - BS, Physics with Philosophy
0095	
0096	Contact www.linkedin.com/in/damjandenic-5212b3166 (LinkedIn) Top Skills Python (Programming Language) Computer Vision Machine Learning Honors-Awards ZenHire Hackathon WHOIS Hackaton SUMA Hackaton Jane Street International Estimation Competition Studentship For Young Talents Of Serbia Damjan Denic CTO, Matta MPhil Advanced Computer Science, Cambridge London, England, United Kingdom Summary Empowering the world through - and innovative solutions is my passion! Currently, I am pursuing my MPhil in Advanced Computer Science at the , where I am diving deep into the latest advancements in the field. My MPhil thesis is a testament to my drive for innovation and impact, as I work on decoupling dynamic from static objects from large scale monocular video using s. I gained hands-on experience thanks to my prior work, which includes estimation and applications in producing . I have also worked on - of Gaussian Processes, further solidifying my expertise in ML. My journey began at Mathematical Grammar High School where I developed a strong foundation in mathematics and . This inspired me to pursue my Bachelor's degree in Control Systems Engineering where I honed my - skills. My true passion lies between and Computer Vision, where I get to bring my ideas to life and make a real-world impact . I am proud to have had the opportunity to work with industry leaders such as , where I worked on Document generation from results, and the AI Institute, where I developed solutions for energy networks. Currently, I work for SignAvatar, where I leveraged my expertise to work on development of avatar to bridge the communication gap for the deaf community. I am motivated by the potential of technology to shape our world for the better and I am determined to be at the forefront of this change. Let's connect and make a together! Experience Matta Machine Learning Engineer July 2023 - Present (2 years 11 months) London, England, United Kingdom Red!Tech Software - Machine Learning Engineer March 2021 - Present (5 years 3 months) What happens when your team wins 4 hackathons in a row? You start realizing that you're a great team ➡ You want to make money off it. Maybe start a company? We are a team of CS Enthusiasts. We are eager to work hard and learn more every day. We have a Senior Architect with more that 30 years of experience. All the pieces are there. RedTech was born. At RedTech, we believe that technology should make life easier, not more complex. As the Machine Learning Engineer, I have been dedicated to helping organizations streamline their workflow with innovative enterprise software that uses AI. With a background in machine learning, I have leveraged my expertise to contribute to the research and development of RedTech's cutting-edge solutions. I was also a dev It’s a startup, so everyone is doing everything! The Institute for Artificial Intelligence of Serbia Machine Learning Intern July 2022 - October 2022 (4 months) Novi Sad, Vojvodina, Serbia Research, what is the first thing that comes to mind? Some would say boring, slow paced environment, big uncertainty, papers for the sake of papers… For me research is the field of endless possibilities in which solving the problems that will make an impact is most important. The Institute's dedication to applying AI research to real world challenges society impressed me, and I felt privileged to join their team. I helped develop RL solutions for energy networks as part of my job, and I quickly realized how crucial it is to create algorithms that are both efficient and scalable. I developed a thorough understanding of the problems energy providers face and the opportunities presented by AI to address these problems during my time at the institute. I constantly pushed myself to learn new things and to think creatively. My continued work as a machine learning engineer has benefited greatly from these experiences, which have also enabled me to approach my projects from a different angle. Microsoft Software Engineer July 2020 - December 2020 (6 months) Belgrade, Serbia What better way to start in the industry? Starting from the interview, then learning about company culture and at the end learning from the experienced experts helped me get better understanding of the industry standards and . I strengthened my talents at Microsoft by applying machine learning OCR system to Document generation software and cooperated with teams of experts from around the world. This experience has been extremely helpful to my for current and future work, as I learned to perceive scope of the larger project. I can use my practical knowledge to assist drive growth and make a genuine difference. The knowledge I gained while working at Microsoft inspired me to dive deeper in algorithmic approaches for image recognition and computer vision. Education University of Cambridge Master of Philosophy - MPhil, Computer Science · (October 2022 - July 2023) University of Belgrade, School of Electrical Engineering Bachelor of Engineering - BE, Control Systems Mathematical Grammar School High School for Gifted Students in Mathematics, Physics and Computer Science
0097	
0098	Contact www.linkedin.com/in/dougbrion (LinkedIn) douglasbrion.com (Personal) github.com/dougbrion (Portfolio) matta.ai (Company) Top Skills C++ Python (Programming Language) Project Management Honors-Awards Royal Commission for the Exhibition of 1851 Industrial Design Scholarship Ash Music Scholar Governors’ Prize Best 1st Year Project Prize Dean’s List Douglas Brion Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge London, England, United Kingdom Summary Founder & CEO of Matta - a startup creating industrial AI for factory sentience. Rough about me: - Awarded Enterprise Fellowship from Royal Academy of Engineering - Completed award winning PhD at the University of Cambridge on "AI for Manufacturing" in the Department of Engineering. - Graduated with 1st Class Honours in EECS from Imperial College London with the Governors' Prize for the outstanding student. - Held Ash Music Scholarship at the Royal College of Music strangely for the recorder... - In 2021 I drank exactly 1325 teas and 641 coffees... don't ask me why I know! Experience Matta Founder & CEO January 2023 - Present (3 years 5 months) Greater London Royal Academy of Engineering Enterprise Fellowship June 2023 - June 2024 (1 year 1 month) London, England, United Kingdom Institute for Manufacturing (IfM), University of Cambridge Researcher October 2019 - April 2023 (3 years 7 months) Cambridge, England, United Kingdom Cambridge Judge Business School Accelerate Cambridge April 2021 - April 2022 (1 year 1 month) Cambridge, England, United Kingdom Royal Commission for the Exhibition of 1851 Industrial Design Studentship October 2018 - September 2019 (1 year) London, England, United Kingdom Internet of Business Software Engineering Contractor November 2016 - February 2017 (4 months) London, United Kingdom Created architecture of solution and started development of both front and backend systems. Testing of custom neural nets in C++. Created documentation for handover to a team in Portugal to implement. Ricardo Summer Intern August 2014 - August 2014 (1 month) Shoreham Experienced different facets of the business, fully dismantling and pressure testing a V8 diesel, rigging up test beds whilst working with equipment calibration. Insight gained into error spotting and deducing whether if a technical issue or just calibration error. Education University of Cambridge PhD in Engineering, Institute for Manufacturing, Department of Engineering · (2019 - 2023) Imperial College London Bachelor of Engineering - BEng, Electronic and Information Engineering · (2015 - 2018) Royal College of Music LRSM, Music Performance, Recorder · (2015 - 2018)
0099	
0100	[CLEANER NOTE: inferred section boundary]
0101	Posts & Comments
0102	
0103	Douglas Brion
0104	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0105	12/01/26, 08:08 PDT • 3mo • Edited •
0106	if you love manufacturing and how things are made, this is probably the best job in the world rn. avg week could be visiting factories for plane wings/soup tins/electronics… you name it.help us install sensors, AI models, and our factory nervous system across UK, EU, and US factories in EVERY sector.we have 100s of factories in the pipeline so don’t be shy. there are not a finite number of places. if you are exceptional… we will take you.
0107	Forward Deployed Engineer
0108	Job by Matta
0109	London, England, United Kingdom (Hybrid)
0110	
0111	Douglas Brion
0112	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0113	11/12/25, 09:18 PDT • 4mo • Edited •
0114	Very exciting day for the Matta team today! 🚀We’re excited to share that we’ve raised $14M to accelerate our work on industrial AI and build sentient factories – factories that can see, understand, and improve themselves in real time.Huge thanks to the team for being exceptional at everything they do. We genuinely have some of the best AI scientists, engineers, and manufacturing experts out there, bringing insane intensity and energy every day. I can’t wait to see what we build together – love you all. ❤️We’re also super excited to be working with some great investors on this journey, including Lakestar, Giant Ventures, Redseed, 1st Kind, and InMotion Ventures.For our current customers, this funding will allow us to dramatically improve our existing AI deployments with you and scale to new use cases. For any new manufacturers out there, we’re deploying to around two factories a month and have a multi-year waitlist at the moment – so do reach out and let’s see how we can dramatically improve your processes with industrial AI. 🏭🧠2025 was a big year. Can't wait for 2026 - we have even bigger plans! 🔥Let's go Sebastian Pattinson Tom Walker Damjan Denic Matthew Judge Ollie Rosen Daniel Crimp Christos Margadji Ashir Sharjeel Carmelo del Coso Ameijide Jake Moll Kian Shamsaie!
0115	
0116	Douglas Brion
0117	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0118	24/07/25, 05:59 PDT • 9mo •
0119	Physical AI is the most impactful space to work in today and for the next decade.Join our incredibly gifted team and help build the infrastructure powering industrial AI in factories around the world. Explore roles: https://lnkd.in/eGdBEzNGWe’re deploying AI at scale into real factories - from automotive and electronics to aerospace, nuclear submarines, waterproof coats and even gourmet cheese... 🚗💻✈️🚢🧥🧀You’ll be building the backend systems that let AI actually touch machines. Robust, low latency infrastructure powering the best industrial AI, while transforming how our customers run their factories through our data driven platform.We’re a world class team of engineers, operators and scientists, backed by top VCs and moving fast ⚡If you’re tired of working on stuff that doesn’t matter, this is your moment.This Mattas.#AI #IndustrialAI #Manufacturing #BackendEngineering #StartupJobs #DeepTech #MachineLearning #Industry40 #Hiring #InfrastructureEngineering
0120	
0121	Matta
0122	31/10/24, 12:32 PDT • 1yr • Edited •
0123	🎃 Nothing gets the Matta team more excited than building a Halloween LEGO pumpkin! 👻 Thank goodness our fully unsupervised AI model trained itself for quality inspection in less than 15 minutes to catch any mistakes.It actually took us longer to write this post and edit the video than to gather the data and train the model from scratch! 🤖Does your quality inspection need a boost? Let our AI do all the work – and in record time! 🕒🎉#happyhalloween #ai #computervision #manufacturing #mattamagic #nerds #easyaspumpkinpie
0124	
0125	Damjan Denic
0126	CTO, Matta MPhil Advanced Computer Science, Cambridge
0127	21/01/24, 16:07 PDT • 2yr •
0128	Extremely happy to share that I started a new position as a Machine Learning Engineer at Matta! Very excited to be a part of such a motivated and hard-working office that steers the ship towards revolutionising manufacturing. We have come a long way since this tea-infused Lego building session, but the most exciting times are yet to come! Stay tuned 📻
0129	
0130	Damjan Denic
0131	CTO, Matta MPhil Advanced Computer Science, Cambridge
0132	30/01/23, 11:06 PDT • 3yr •
0133	The big reveal is here! We are excited to announce that Red!Tech is rebranding as SignAvatar! 👇SignAvatar will be a spin-off fromRedTech, while RedTech will still operate as an enterprise software develompent company, BUT with focus on web3!So what is SignAvatar?SignAvatar is a revolutionary software that translates speech into sign language, making it easier for deaf and hard of hearing individuals to communicate with the hearing world.Our software uses cutting-edge AI technology to accurately translate speech into sign language on an avatar, providing an interactive and engaging way to communicate.Not only is SignAvatar a valuable tool for personal communication, it's also a valuable tool for businesses and organizations that prioritize accessibility and inclusivity.By using SignAvatar, companies can ensure that they are able to effectively communicate with deaf customers and employees, and demonstrate their commitment to social responsibility.We are excited to embark on this new journey as SignAvatar and to continue developing innovative solutions that improve communication and increase inclusivity.Thank you for your support as we make this transition!• If share the news, 200 more people will see it, so please do!---------Please follow SignAvatar and tell us what you think about our product.#deaf #asl #csr
0134	
0135	Damjan Denic
0136	CTO, Matta MPhil Advanced Computer Science, Cambridge
0137	27/01/23, 07:52 PDT • 3yr •
0138	Something is cooking in the office. Can't wait for the big reveal!We're looking to impact the #csr market and #deafcommunityJoin the waiting, Sunday is the big day!
0139	
0140	George Dimitrijevic
0141	CEO @SignAvatar | Founder in Residence @Garaza | Sigma² Fellow
0142	26/01/23, 03:34 PDT • 3yr •
0143	We're on the brink of announcing something truly revolutionary – a software solution that will change the way you communicate. Stay tuned for more details on our newest venture, and get ready to experience the power of improved communication.We've been hard at work developing a groundbreaking new software solution, and we're almost ready to share it with the world. Keep an eye out for updates on our latest project – it's going to be a game-changer!We're looking to impact the #csr market and #deafcommunity
0144	
0145	Damjan Denic
0146	CTO, Matta MPhil Advanced Computer Science, Cambridge
0147	04/11/22, 07:33 PDT • 3yr • Edited •
0148	I’m happy to share that I’ve started my MPhil Advanced Computer Science at University of Cambridge!
0149	
0150	Damjan Denic
0151	CTO, Matta MPhil Advanced Computer Science, Cambridge
0152	16/05/22, 05:06 PDT • 3yr •
0153	Really proud to be part of the Red!Tech team and achieving first place 🏆 at the ML hackathon focused on HR interview analysis!Huge thanks to ZenHire for organizing this inspiring event!
0154	
0155	George Dimitrijevic
0156	CEO @SignAvatar | Founder in Residence @Garaza | Sigma² Fellow
0157	16/05/22, 04:46 PDT • 3yr •
0158	We did it boiz😎Another 1st place hackaton for RedTech!🥇🥇🥇Yesterday our team competed in ZenHire ML hackaton, and in 12 hours we implemented a new algorithm for recognizing vocabulary strenghts in applicants!We had an AMAZING time, met new people and of course learned something new📚🤓Huge shoutout to Vladimir Bozovic and his team at ZenHire for organizing the eventEvent actually had two challenges (ML and brainstorm) and both were really fun.PS: Had a great party afterwards 😎🍻Follow Red!Tech for more! #ml #hackathon #tech
0159	
0160	Damjan Denic
0161	CTO, Matta MPhil Advanced Computer Science, Cambridge
0162	14/04/22, 05:57 PDT • 4yr •
0163	Thanks again to Mathematical Grammar School in Belgrade (Serbia) for the opportunity to give a lecture at the Week of Informatics. I hope that my lecture at least intrigued ambitious high schoolers for one of my interests.And huge thanks to all the students that actively participated in the lecture, you really proved that generations may change, but dedication and ambition are still the first things that come to mind when Mathematical Grammar School is mentioned.
0164	
0165	Damjan Denic
0166	CTO, Matta MPhil Advanced Computer Science, Cambridge
0167	27/09/21, 13:08 PDT • 4yr •
0168	I am feeling proud for working past three days and making another milestone with teammates Andrija Jelenkovic and Milan Cupac from Red!Tech. And thanks to Zeljko Lucic and Igor Stevanovic, without you this team would not be complete!🎉
0169	
0170	Red!Tech
0171	27/09/21, 13:00 PDT • 4yr •
0172	As a prologue our #RedTechTeam story, we are happy to annouce that our team, partnered with Igor Stevanovic and Zeljko Lucic has won FIRST PLACE 🏆🏆🏆 on WHOIS Online hackaton, powered by Quantox Technology and Регистар националног интернет домена Србије (РНИДС): https://lnkd.in/eHQMbYSTOur team designed an app that checks availability and basic information about a wide selection of domains that works for both iOS and Android, in just 48hrs!Congratulations to Damjan Denić, Milan Cupac, Andrija Jelenkovic, Igor Stevanovic and Zeljko LucicYou can check our git repo: https://lnkd.in/eibEwm7SCheck our demo below! 👇 #redtech #android #ios #hackaton #winnersmindset
0173	
0174	Damjan Denic
0175	CTO, Matta MPhil Advanced Computer Science, Cambridge
0176	19/03/21, 09:00 PDT • 5yr •
0177	Looking forward to lecturing as a member of team Red!Tech. Don't miss out this great initiative!
0178	
0179	George Dimitrijevic
0180	CEO @SignAvatar | Founder in Residence @Garaza | Sigma² Fellow
0181	19/03/21, 08:20 PDT • 5yr • Edited •
0182	We are Red!TechA team of undergraduates that decided to give back to the community of developers by sharing some of our interests in topics that are not covered by our university courses. Our mission is to give people an incentive to learn more about the technology trends of 2021.For our very first series of live events we've partnered with Google Developer Group on Campus, University of Belgrade to bring you:IT isn't Rocket ScienceWe'll cover the following topics (times are displayed in CET):25.03. 18h Asp .NET Core - Make a REST API in 1 hour!27.03. 18h Spring and Spring Boot Overview- Why doing things the easy way is always the right choice?28.03. 18h Quantum Computing - Future or just another research paper? 01.04. 18H [ML] Naive Bayes Spam filter using Naive Bayes. 02.04. 18H [ML] AI in Games Can Gamers stand to AI? These events are for everyone, no matter whether you are in tech or not!Be there with us. For more information check out:Facebook Event: https://lnkd.in/eJntHkcOur website: https://lnkd.in/e2ceVEZGoogle Club Event: https://cutt.ly/0xyXocyAll events will be streamed live on: https://lnkd.in/eGECdTu #google #googlestudents #ml #computing #spring
0183	
0184	Douglas Brion
0185	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0186	21/04/26, 06:33 PDT • 2w •
0187	Look mum, we're in Machinery.Excited for Matta to be in the MACH 2026 edition of Machinery with a spotlight article. Thanks Ellie McCann! So cool to be part of this over 100 year old manufacturing publication.Speaking of MACH, come see us at stand 17-121 and have a play with our industrial AI demos.#manufacturing #ai #mach2026
0188	
0189	Matta
0190	20/04/26, 02:16 PDT • 2w •
0191	MACH 2026 – we’re ready.Calling all UK manufacturers... come find us on the Matta stand (17-121) to see how industrial AI can make your factory sentient and drive real gains in productivity, quality, and waste reduction on the factory floor.Live demos, fun conversations, and plenty of industrial AI chat with Damjan Denic, Carmelo del Coso Ameijide, and Douglas Brion.See you there.#mach2026 #manfuacturing #nec #ukmanufacturing
0192	
0193	Douglas Brion
0194	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0195	10/04/26, 02:00 PDT • 3w •
0196	Spoke at Giant Ventures last week to a room full of aspiring founders about the no-BS reality of building an AI company out of academia.We talked about spinouts, co-founders, fundraising, UK vs US, and how research only becomes a company when it collides with real-world customers, urgency, and lots of failures... we love learning!!Also, proud to see the nerd posture making such a strong appearance in the photo.Thanks to Madelene Larsson and the Giant team for having me.
0197	
0198	Matta
0199	01/04/26, 02:15 PDT • 1mo •
0200	We recently held a landmark event bringing together the best of British AI and manufacturing.Hosted at the Royal Academy of Engineering, "Sentient Factories: AI and the Future of Manufacturing" brought together around 80 leaders from industry, startups, government, academia, and investment to discuss how we build the future of manufacturing here in the UK.We were honoured to hear from Sir John Lazar, Kanishka Narayan MP, and Prof. Tim Minshall, each bringing a different and important perspective on the opportunity ahead for British industry.What made the evening special was not just the calibre of the room, but the fact that it brought together people who do not speak to one another often enough: manufacturers, startups, government, academia, and investors.We had people with us from organisations including BAE Systems, GKN Aerospace, McLaren Racing, Alpine Formula One Team, Cummins Inc., Bowers & Wilkins, Domino Printing Sciences, Chivas Brothers, Husqvarna Group, ABB, Pragmatic Semiconductor, Advanced Research + Invention Agency (ARIA), Innovate UK, Department for Science, Innovation and Technology, and the Institute for Manufacturing (IfM), University of Cambridge, among many more.From aerospace and semiconductors to robotics, food and drink, consumer products, automotive, and advanced engineering, the message was clear: the UK has an incredible industrial base. We also have the third-largest AI ecosystem in the world. The opportunity now is to bring those two strengths together.If the UK is serious about building the factories of the future, these worlds need to collide far more often.This evening felt like the start of something important.And yes, as you may notice from the backing track to the video, the whole thing may or may not feel like the start of a new reign for British industry.Huge thanks to everyone who joined us and helped make it such a special evening.#Manufacturing #BritishIndustry #IndustrialAI #ArtificialIntelligence #Innovation #AdvancedManufacturing #FutureOfManufacturing
0201	
0202	Douglas Brion
0203	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0204	01/04/26, 00:37 PDT • 1mo •
0205	Had a great time in Paris with 1st Kind and some of the Peugeot family.Huge thanks to Sophia Martin (Ktiri) and Ulysse Laroche for the invite.We had some brilliant conversations about European industry, manufacturing, and the feeling that momentum is starting to shift. It genuinely feels like Europe could be at the start of a resurgence.We are past the point of yet more committees and yet more reports. We know what is wrong. Now it is about action. About working together. About actually backing industry and statups properly and building with unlimited ambition.Europe has the industrial base. The know-how. The talent. The AI capability. The capital.The ingredients are there. The real challenge is bringing them together, thinking big enough, and not mistaking another report or committee for action.We cannot afford to be timid.And for the people who believe this is Europe’s moment: come and build with us at Matta.We are building a crazy talent-dense team and hiring across software, hardware, AI, operations, and sales to help build sentient factories.#EuropeanIndustry #Manufacturing #IndustrialAI #Innovation #Startups #Reindustrialisation
0206	
0207	Douglas Brion
0208	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0209	24/03/26, 05:15 PDT • 1mo •
0210	Last week, the Matta team had the pleasure of hosting "Sentient Factories: AI and the Future of Manufacturing" at The Royal Academy of Engineering, bringing together around 80 guests from industry, government, academia, startups and investment.We had people in the room from every part of the country, from CTOs of multinationals to manufacturing engineers with decades of experience. And that was exactly the point.If the UK is serious about using AI to strengthen manufacturing, we need far more conversations that bring together the people building the technology, the people shaping policy, and the people living the reality of the factory floor.The evening featured brilliant talks from John Lazar, President of the Royal Academy of Engineering, Kanishka Narayan MP, Minister for AI and Online Safety, Tim Minshall, Head of the Institute for Manufacturing (IfM), University of Cambridge, and, somehow, myself too.We also had a fantastic panel with Sophia Martin (Ktiri) (1st Kind), Alan Patterson (BeyondMath), Jerry Gray (Bowers & Wilkins) and Steven Grace (Cummins Inc.).What made the evening special was the energy in the room. There was real ambition, real curiosity, and a clear sense that the UK has a major opportunity to combine its industrial heritage with its strength in AI to build the factories of the future.We have had an overwhelming number of kind messages afterwards, and lots of requests to do more evenings like this, so hopefully this was just the first.Royal Academy of Engineering Enterprise Hub University of Cambridge Department for Science, Innovation and Technology The ERA Foundation Royal Commission for the Exhibition of 1851 #AI #Manufacturing #IndustrialAI #FutureOfManufacturing #UKManufacturing
0211	
0212	Cummins Europe
0213	23/03/26, 08:57 PDT • 1mo •
0214	Exploring the future of manufacturing through AI Last week, Jonathan Wood (Vice President - Chief Technical Officer) and Steven Grace (Automation & Technology Leader) attended Sentient Factories: AI and the Future of Manufacturing at the Royal Academy of Engineering hosted by AI technology company Matta.The event brought together leaders across UK manufacturing to discuss, share best practices, and explore how AI can be effectively developed and deployed across the industry.Steven also joined a panel discussion, contributing real-world insights on implementation, challenges, and opportunities as manufacturers adapt to this rapidly evolving landscape.With contributions from industry, academia, and government, the event highlighted a clear message: collaboration will be key to unlocking the full potential of AI in manufacturing.#Cummins
0215	
0216	Douglas Brion
0217	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0218	23/02/26, 04:22 PDT • 2mo •
0219	Cracked the fountain pen out this weekend. 🖋️Exciting things are coming. To the great and the good in UK manufacturing: check your post this week!
0220	
0221	Douglas Brion
0222	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0223	12/02/26, 09:18 PDT • 2mo •
0224	Manufacturing is the bedrock of our lives, help us improve it and keep it punching in the West. We’re now deploying into two new factories every month – and we need to move faster.If you’re excited about applying the latest industrial AI models in the physical world, we’re hiring across multiple roles:- AI Scientists: Push the state of the art in manufacturing foundation models and few-shot vision. Real research. Real application. Big impact.- Forward Deployed Engineers: Deploy hardware into factories and work side-by-side with customers to solve real manufacturing challenges. Your life is basically ‘How It’s Made’.- Product Engineers: Build the next-generation UI and platform for managing and controlling factories. Industrial software that actually feels modern.- Founding GTM: - Help us convert the 400+ factories already in our pipeline. Develop the playbook and scale it properly.- Business / Operations: From expanding into new geographies to securing major customers and keeping the team running smoothly.- Open Application: If you’re exceptional at what you do and believe the physical world is where it’s at, apply anyway.Reach out to careers@matta.ai!
0225	
0226	Stuart Whitehead
0227	Founder of Jefferson, Co-founder of FactoryNOW
0228	06/02/26, 02:00 PDT • 3mo • Edited •
0229	🇬🇧 We don't make anything anymore? January's UK manufacturing highlights:🔸 Cummins Inc. announced plans to invest $50m expanding its power systems manufacturing plant in Daventry, Northamptonshire.The huge 435,000 sq. ft. Daventry site manufactures and distributes 38 litre to 95 litre engines for use across a range of global sectors, including data centres, healthcare, oil and gas, rail and marine applications.🔸 AESC UK officially opened its new battery manufacturing plant in Sunderland. Production is now underway at the new 15.8 GWh gigafactory that will manufacture lithium-Ion batteries for electric vehicles made in the UK, including the new Nissan LEAF. 🔸 Oxford-based Airbus Helicopters was awarded a £33.6m contract by the Ministry of Defence to support the UK Armed Forces' new H145 fleet.The two-year contract covers the upkeep of the six H145 helicopters, known in UK service as Jupiter HC2, which were ordered under a £122m procurement agreement signed just over 18 months ago. 🔸 GE Aerospace announced plans to invest £19m upgrading its Welsh site - the American aerospace giant's largest single investment in Wales for more than 25 years.🔸 Following a £450m investment programme, the new electric LEAF entered production at Nissan Motor Corporation's Sunderland plant. To launch its most advanced vehicle yet, Nissan has transformed the Sunderland plant, enabling EV manufacturing on production Line Two for the first time.🔸 Diageo opened its new £73m Guinness Open Gate Brewery in London, marking a return of brewing to Covent Garden. The new world-class visitor experience and working microbrewery has transformed Old Brewer’s Yard – a site that first brewed beer back over 300 years ago.🔸 Airbus opened a new central manufacturing hub at its Broughton site to support its Beluga transport network. This first-of-its-kind facility within the Airbus network represents an investment of circa £6.8m in Broughton and strengthens the role the site plays within the UK’s aerospace industry.🔸 Safran announced plans to open its first Research and Technology Centre outside of France in the UK. This initiative is part of Safran’s strategy to support the Group’s expanding presence in the UK and is a first step in the global expansion of its R&T activities.🔸 BAE Systems announced plans to recruit 2,300 apprentices, graduates and undergraduates in the UK this year.Since 2020, BAE Systems - which currently has a record 6,800 young people in training across its UK operations - has recruited more than 10,000 apprentices and graduates and invested over £1 billion in education and skills.🔸 50 years after production of the iconic original ended, the Jensen Interceptor is to be reborn as a new British-built, V8-powered GT.The limited number of new cars will be built by Banbury-based Jensen International Automotive (JIA), the engineering firm that specialises in restoring and modernising Interceptors.
0230	
0231	Douglas Brion
0232	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0233	02/02/26, 02:00 PDT • 3mo •
0234	Over the next 3 days, Matta is exhibiting at Southern Manufacturing & Electronics 2026.It also marks one year since our very first trade show (Southern last year) so it’s a bit of a full-circle moment. Really looking forward to catching up with so many familiar faces from UK manufacturing.If you’re curious about how to increase productivity, reduce waste, and improve quality through practical, shopfloor-ready AI, come and say hi. We’ve brought fun real-world demos (and we genuinely love people trying them out).Come join us getting a little too excited about manufacturing! Let’s chat. 🙂#manufacturing #ukmanufacturing #industrialai #quality #continuousimprovement #automation #machinevision #southernmanufacturing2026Tom Walker Christos Margadji Sebastian Pattinson Ollie Rosen Damjan Denic
0235	
0236	Douglas Brion
0237	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0238	19/01/26, 05:38 PDT • 3mo • Edited •
0239	Excited to be giving this talk at the old haunt! Wonder if my lab slippers are still around in my old drawer… 👀
0240	
0241	Institute for Manufacturing (IfM), University of Cambridge
0242	19/01/26, 05:30 PDT • 3mo • Edited •
0243	Manufacturing Innovators – 29 January 2026Douglas Brion, Founder and CEO of Matta, will be joining us as the first speaker in the Manufacturing Innovators talk series.In his talk, he will discuss ‘Creating industrial AI for factory sentience’, sharing his story behind his work; the why, what, and how of developing new products and systems, and the challenges and opportunities they encountered along the way. 🕕  6-7pm, followed by informal drinks📍  Institute for Manufacturing, University of Cambridge👉 Register your place: https://lnkd.in/eMdb2hrs Manufacturing Innovators is a bi-monthly talks, hosted at the IfM. During the sessions, we will bring together science, technology, and manufacturing to explore how new ideas become real products, and why closer collaboration between these worlds really matters.#ManufacturingInnovators #TalkSeries #ManufactureABetterWorld Tim Minshall, Department of Engineering at the University of Cambridge
0244	
0245	Douglas Brion
0246	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0247	12/01/26, 05:30 PDT • 3mo • Edited •
0248	if you love manufacturing and how things are made, this is probably the best job in the world rn. avg week could be visiting factories for plane wings/soup tins/electronics… you name it.help us install sensors, AI models, and our factory nervous system across UK, EU, and US factories in EVERY sector.we have 100s of factories in the pipeline so don’t be shy. there are not a finite number of places. if you are exceptional… we will take you.
0249	
0250	Douglas Brion
0251	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0252	12/01/26, 02:30 PDT • 3mo •
0253	Great start to 2026! Honoured to be featured in The Engineer UK’s 170th-anniversary issue.This publication first started in 1856, back when the giants of the Industrial Revolution were still alive and building the modern world. I believe they used to publish things like raw material prices in each issue which I think is pretty cool!Big thank you to their editor Jon Excell, who stopped by our Shoreditch loft to chat about our work building the AI nervous system for "sentient factories" – production lines that see, learn, and actually understand the messy reality of the shop floor.We believe AI shouldn't just be for boring tasks like automating lawyer's emails. It belongs in The Engineers who build the physical world. Learning everything from how to find a scratch (without inhaling, licking your finger, and running it over it), to assembling an entire jet engine.The UK has a real edge in developing and deploying applied AI for the real world. What other areas do you think we have a unique advantage to build in? 🚀#IndustrialAI #UKManufacturing #BritishDynamism #Matta 🏭
0254	
0255	The Engineer UK
0256	09/01/26, 03:21 PDT • 3mo • Edited •
0257	📣 Check out the January edition of The Engineer UK☀️ Our 170th anniversary kicks off with a look at developments in #renewable and #nuclear energy, but also looks back through the magazine's archive to show early developments in these fields⚛️ President of the Nuclear Institute, Dr Fiona Rayment, discusses the importance of the nuclear sector to the UK, highlighting key trends and the tech shaping its future🏎️ In our panel report, F1 leaders gathered at Silverstone to discuss the sport's direction of travel🏭 Jon Excell looks at how Cambridge spinout Matta is developing sentient factories📢 Climate campaigner and author Bill McKibben discusses the exponential rise of solar energy👩‍🌾 #Lategreatengineers takes a look back on the achievements of Victorian #agritech pioneer, John Fowler💡 Jason Ford reflects on The Engineer's 1877 obituary of Sir Titus Salt, the pioneering industrial philanthropist who established a factory and workers village at Saltaire in West Yorkshire ➕ Articles on #AIInspection, how IBM is helping to map natural disasters, an Anglo-US collaboration developing sustainable #photoluminescence, and a #smartbra that tracks #breastcancer riskRead the digital edition here 👇 https://lnkd.in/etTgz2fc#theengineeruk #170thAnniversary #solarenergy #nuclearenergy #SMRs #SmallModularReactors #philanphropy #SmartFactories #AI #TechnologyNews #BusinessNews #agritech
0258	
0259	Douglas Brion
0260	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0261	14/12/25, 06:22 PDT • 4mo •
0262	We’re hiring a Chief of Staff.At Matta, we’re building industrial AI to give factories the ability to see, understand, and improve themselves in real time. We're scaling fast after our recently announced raise and need more people to join our incredible team. This role is for a high-IQ/EQ generalist who loves hard problems and learns fast. Maybe you started in strategy consulting and then moved into startups. Or perhaps you have spent time in VC and now want a proper taste of building. Either way, you are happiest owning the messy middle between idea and execution.🧙‍♂️ Think Gandalf: the person who quietly works their magic behind the scenes, making sure everything runs smoothly (yet pulls off heroic deeds when needed).What you’ll do:- Work directly with the founders and CEO on the company’s top priorities- Turn ambiguous problems into clear plans, then drive them through to completion- Unblock teams across product, engineering, ops, and commercial- Add just enough structure to help us ship faster as we scaleIf you want real responsibility from day 1, this is it. It is close to the best parts of being a founder, but with funding sorted and a world-class team already around you.📍 Our office is 5 mins from Old Street. Message me or email careers@matta.ai with a short note on something you have helped build (and what you would do differently now).
0263	
0264	Douglas Brion
0265	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0266	10/12/25, 07:22 PDT • 4mo • Edited •
0267	Very exciting day for the Matta team today! 🚀We’re excited to share that we’ve raised $14M to accelerate our work on industrial AI and build sentient factories – factories that can see, understand, and improve themselves in real time.Huge thanks to the team for being exceptional at everything they do. We genuinely have some of the best AI scientists, engineers, and manufacturing experts out there, bringing insane intensity and energy every day. I can’t wait to see what we build together – love you all. ❤️We’re also super excited to be working with some great investors on this journey, including Lakestar, Giant Ventures, Redseed, 1st Kind, and InMotion Ventures.For our current customers, this funding will allow us to dramatically improve our existing AI deployments with you and scale to new use cases. For any new manufacturers out there, we’re deploying to around two factories a month and have a multi-year waitlist at the moment – so do reach out and let’s see how we can dramatically improve your processes with industrial AI. 🏭🧠2025 was a big year. Can't wait for 2026 - we have even bigger plans! 🔥Let's go Sebastian Pattinson Tom Walker Damjan Denic Matthew Judge Ollie Rosen Daniel Crimp Christos Margadji Ashir Sharjeel Carmelo del Coso Ameijide Jake Moll Kian Shamsaie!
0268	
0269	Matta
0270	10/12/25, 04:17 PDT • 4mo •
0271	Big news from Team Matta today.We’re excited to share that we’ve raised $14M to accelerate our work on industrial AI and build what we call sentient factories – factories that can see, understand, and improve themselves in real time.Our plug-and-play AI is already running on lines from polymer manufacturing and metal casting to bottling and consumer electronics and in the factories of quality brands like Bowers & Wilkins. With a system that can learn a new line in days (sometimes minutes) from very little data, we’re now working with hundreds of factories in our pipeline and adding new installations every few weeks.We’re super excited to have Lakestar and Giant Ventures as lead investors, and to be working with Redseed, InMotion Ventures, 1st Kind, Unruly Capital and Boost VC.Huge thanks as well to Innovate UK and the Royal Academy of Engineering for their amazing support. We’re incredibly grateful to our supporters, early customers, the University of Cambridge and Institute for Manufacturing (IfM), University of Cambridge for enabling our initial research, and the wider UK manufacturing community who have believed in this mission from the start.Now the fun part: putting capital to work!! We’ll be:• Rolling out Matta to many more factories across the UK, Europe, and the US• Doubling down on self-tuning machines with OEM partners like Caracol AM• Growing our team of world-class cracked engineers, researchers, and operators who love real factories as much as we doIf you’re running a factory and want to boost quality, cut waste, or just make your line a lot smarter – we’d love to talk. And if you’re an engineer or operator who gets excited about cameras, AI, how things are made, and gnarly real-world data, keep an eye out… we’re hiring!! #IndustrialAI #FactorySentience #Manufacturing #UKManufacturing #DeepTech #BritishDynamism
0272	
0273	UK House of Lords
0274	07/11/25, 08:44 PDT • 5mo •
0275	UK’s failure to retain and scale science and technology causing economy to bleed out, warns Lords Committee The House of Lords Science and Technology Committee has published a new report 'Bleeding to death: the science and technology growth emergency' warning the government that the UK’s failure to retain and scale its science and technology companies has now reached crisis point and is causing the UK economy to bleed out. Without urgent and radical reform, the government risks acting too late to seize the enormous opportunities for technological and economic growth that are currently slipping through its fingers. The committee calls on the government to: 🟥establish a new high level National Council for Science, Technology and Growth🟥reform visa policies for global talent🟥consider measures to incentivise pension funds to invest in UK science and technology companies🟥take risks on new technologies and provide the contracts to companies that can help them grow and anchor them in the UK 📄Read the full report https://lnkd.in/eBGT_sck
0276	
0277	Douglas Brion
0278	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0279	05/11/25, 05:59 PDT • 6mo •
0280	Today is National Engineering Day 👷‍♀️🛠️ – a day to celebrate the people who built the world around us and are now re-engineering it for the future.At Matta, we’re lucky to work with engineers on factory floors who are embracing industrial AI for factory sentience, giving factories the ability to see, understand and improve themselves in real time.It’s exactly the kind of future-facing engineering the Royal Academy of Engineering is highlighting today – blending physical craft with digital intelligence to tackle the UK’s biggest manufacturing challenges.We’re proud to be working alongside the teams making that transformation real. If you’re building smarter production lines, we’d love to compare notes and help make UK engineering even more world-class.#NationalEngineeringDay #Engineering #ManufacturingAI #FactorySentience #Engineers2030
0281	
0282	Matta
0283	30/10/25, 06:15 PDT • 6mo • Edited •
0284	What a start to Advanced Engineering 2025! ⚙️🔥Day one was a blast - we met over 100 incredible leads from across the manufacturing world, and the buzz around our demo was unreal.Here’s a peek at the action at Booth P198 - our team showing how AI-powered quality control is already transforming real factories. We’re back at it today ready to show even more of you what happens when AI meets real-time production.Come say g’day, get hands-on, and let’s talk about the future of industrial AI.#AI #IndustrialAI #Manufacturing #AdvancedEngineering #SmartFactories #DeepTech #QualityControlDouglas Brion Daniel Crimp Sebastian Pattinson Bonnie Zhang Jake Moll Tom Walker Ollie Rosen Damjan Denic Christos Margadji Matthew Judge
0285	
0286	Douglas Brion
0287	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0288	16/09/25, 07:59 PDT • 7mo • Edited •
0289	We’re hiring and not messing around. 🧠🏭Matta is growing fast – with new factory installations every month, from electronics and castings to aerospace parts and whisky bottles. We’re building industrial AI that actually works – deploying software, hardware, and AI models into some of the messiest, noisiest, most fascinating real-world environments you can imagine. And we need more brilliant people to do it with!Right now, we’re especially looking for:- 👩‍🎨 Frontend Engineers who want to invent the interface layer for how factories are monitored and controlled- 🧱 Backend Engineers who love building the scalable infrastructure to handle thousands of connected and streaming systems- 🧠 AI Scientists & Vision Researchers from top labs- 🔌 Forward-Deployed & Hardware Engineers who love getting stuck in on the factory floorThis is hard stuff. We’re not in a cozy ML sandbox. We’re doing AI at the edge. With flaky networks, weird lighting, moving robots, tight latencies, and high stakes. We’re building general-purpose systems that can adapt to a thousand different factory settings – not a brittle solution. But that’s exactly what makes it fun.You’ll be joining a small, high-functioning team from places like Google X, Microsoft, IBM, BBC R&D, Cambridge, MIT, and Imperial. We’re tight-knit, a bit batty, and truly "full-stack": from lens calibration and building gantries to foundation model research, factory OS design, and AI infra at scale.We like:- High-agency builders who’ve shipped serious things (startups? even better)- People who learn fast and don’t mind breaking a few things along the way- Engineers who can hold their own in Python and the outskirts of Birmingham- A love for manufacturing, mess, and the sheer joy of learning how things are made- Furious tea and coffee drinkers (bonus points if you delete cake 🍰)📬 Our office is 5 mins from Old Street. Drop us a message and/or email careers@matta.ai – or just send something cool you’ve built. Rebels welcome.#AI #ComputerVision #Robotics #FactorySentience #FrontendEngineering #BackendEngineering #IndustrialAI #SmartManufacturing #UKManufacturing #MattaAI #Hiring #BritishDynamism
0290	
0291	Douglas Brion
0292	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0293	12/09/25, 06:42 PDT • 7mo •
0294	Just wrapped our first ever UK Metals Expo – and safe to say, it didn’t disappoint. What a show! 🇬🇧🔥We clocked 124 leads in two days, putting us in the top 5% of exhibitors. Not bad for our first sector-specific event… especially when the average was just 16!More importantly, it was a total joy to spend time with the brilliant people building the future of UK manufacturing – from heritage steelworks to precision aerospace.Special shoutout to those we met from:William Cook, Tata Steel, Ernest Wright, Centriblast, Safran Seats GB, Make UK, Department for Business and Trade – and many others doing proper manufacturing.At Matta, we're building industrial AI that clicks immediately – no fluff, no smoke and mirrors, just visual systems that see what operators see, learn what good looks like, and catch what others miss. Seeing that click with engineers across forgings, castings, metals and more? Hugely validating.If we didn’t get to speak at the show (or you want a deeper demo), drop us a note. We love talking shop – especially about how AI can help make your factory sentient. 🏭🧠Next stop: Advanced Engineering, NEC Birmingham, 29–30 Oct. Come say hi!#UKMetalsExpo #IndustrialAI #FactorySentience #BritishManufacturing #SmartManufacturing #ForgingTheFuture #ComputerVision #Matta
0295	
0296	Matta
0297	10/09/25, 04:15 PDT • 7mo •
0298	We’re live at the NEC in Birmingham for UK Metals Expo 2025! ⚡🏭Come find us on the show floor today and tomorrow - our team is here with interactive demos of our next-gen quality control systems, showing how AI is transforming QC and production in real factories. From aerospace to automotive, metals to pharma, we’re deploying physical AI at scale.If you’ve ever wondered what it looks like when artificial intelligence actually interfaces with real time production, now’s your chance to see it in action!We’d love to meet manufacturers, engineers, and anyone curious about the future of industrial AI. Stop by, get hands-on, and let’s talk about what this technology can do for your production lines.See you at Stand E90 at UK Metals Expo - let’s build the future of manufacturing together.#AI #IndustrialAI #Manufacturing #UKMetalsExpo #SmartFactories #DeepTech #QualityControl
0299	
0300	Douglas Brion
0301	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0302	24/07/25, 05:56 PDT • 9mo •
0303	Physical AI is the most impactful space to work in today and for the next decade.Join our incredibly gifted team and help build the infrastructure powering industrial AI in factories around the world. Explore roles: https://lnkd.in/eGdBEzNGWe’re deploying AI at scale into real factories - from automotive and electronics to aerospace, nuclear submarines, waterproof coats and even gourmet cheese... 🚗💻✈️🚢🧥🧀You’ll be building the backend systems that let AI actually touch machines. Robust, low latency infrastructure powering the best industrial AI, while transforming how our customers run their factories through our data driven platform.We’re a world class team of engineers, operators and scientists, backed by top VCs and moving fast ⚡If you’re tired of working on stuff that doesn’t matter, this is your moment.This Mattas.#AI #IndustrialAI #Manufacturing #BackendEngineering #StartupJobs #DeepTech #MachineLearning #Industry40 #Hiring #InfrastructureEngineering
0304	
0305	Cambridge Industrial Innovation Policy
0306	05/07/25, 10:36 PDT • 10mo • Edited •
0307	📣 The Economist has published a counterargument from the Institute for Manufacturing (IfM), University of Cambridge & Cambridge Industrial Innovation Policy in response to its June 14 editorial, “The world must escape the manufacturing delusion.”Carlos López-Gómez & Mateus Labrunie, along with Professor Tim Minshall, Head of the IfM, argue that manufacturing is not a delusion – it is a critical driver of innovation, productivity, and regional prosperity. Turning away from it, they argue, would be a strategic error.🔗 Read the response in The Economist:https://lnkd.in/eH2zKpFz📄 Read the response in full on our website:https://lnkd.in/ehsKGQhU #Manufacturing #InnovationPolicy #IndustrialStrategy #IfM #CambridgeUniversity #EconomistDebate #FutureOfWork IfM Engage Department of Engineering at the University of Cambridge University of Cambridge
0308	
0309	Douglas Brion
0310	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0311	01/07/25, 01:50 PDT • 10mo •
0312	🏛️ Recently I had the privilege of being invited to give evidence to the UK House of Lords Science & Technology Committee for their inquiry into Financing and Scaling UK Science and Technology. A big thank you to Lord Mair for the invite!The UK is an incredible place to build. We’ve got a world-class research base, strong institutions, deep industrial heritage - and enough tea to 10x any engineer’s productivity 🫖. Ignore the gloomerism: this country is a fantastic place to build. But we can do even better, especially if we get the next decade right.One area that could use a bit more love? Networks and convening! I shared a quick story: I once landed in San Francisco and grabbed a coffee with a stranger who a few hours later took me to a hardware VC party. The thought of something like that happening in the UK… We do have brilliant networks here - particularly in long-established institutions like the Royal Academy of Engineering - but too often we operate in parallel universes. Startups don’t bump into big incumbents. AI folks rarely cross paths with manufacturers.I see it all the time: one day I’m at a black tie dinner in a grand dining room - Rolls-Royce, Cambridge, Royal Society vibe - and the next I’m in shorts with a cold beer at a chill startup VC meetup. Both sides want to talk. Both sides have a lot to offer. But there’s little cross-pollination.This stuff matters. Serendipity is still where business gets done, where unlikely collaborations start. If we’re serious about scaling UK science and tech, we need to build more of these collisions into the system. Come on Blighty! 🇬🇧#UKInnovation #SciencePolicy #Manufacturing #StartupLife #IndustrialAI #BritishDynamism
0313	
0314	Tim Minshall
0315	Dr John C Taylor Professor of Innovation and Head of Institute for Manufacturing, University of Cambridge
0316	30/04/26, 03:13 PDT • 1w •
0317	We are delighted to announce that we are recruiting for two new academic posts at the Institute for Manufacturing (IfM), University of Cambridge.+ University Assistant/Associate Professor in Industrial Engineering and Operations Management (details here https://lnkd.in/eAFmnH-R)+ Assistant Teaching Professor in Manufacturing Engineering (details here https://lnkd.in/e-g2x8kj)#manufacturing #education #research #impact #Cambridge
0318	
0319	Matta
0320	01/04/26, 03:00 PDT • 1mo •
0321	We recently held a landmark event bringing together the best of British AI and manufacturing.Hosted at the Royal Academy of Engineering, "Sentient Factories: AI and the Future of Manufacturing" brought together around 80 leaders from industry, startups, government, academia, and investment to discuss how we build the future of manufacturing here in the UK.We were honoured to hear from Sir John Lazar, Kanishka Narayan MP, and Prof. Tim Minshall, each bringing a different and important perspective on the opportunity ahead for British industry.What made the evening special was not just the calibre of the room, but the fact that it brought together people who do not speak to one another often enough: manufacturers, startups, government, academia, and investors.We had people with us from organisations including BAE Systems, GKN Aerospace, McLaren Racing, Alpine Formula One Team, Cummins Inc., Bowers & Wilkins, Domino Printing Sciences, Chivas Brothers, Husqvarna Group, ABB, Pragmatic Semiconductor, Advanced Research + Invention Agency (ARIA), Innovate UK, Department for Science, Innovation and Technology, and the Institute for Manufacturing (IfM), University of Cambridge, among many more.From aerospace and semiconductors to robotics, food and drink, consumer products, automotive, and advanced engineering, the message was clear: the UK has an incredible industrial base. We also have the third-largest AI ecosystem in the world. The opportunity now is to bring those two strengths together.If the UK is serious about building the factories of the future, these worlds need to collide far more often.This evening felt like the start of something important.And yes, as you may notice from the backing track to the video, the whole thing may or may not feel like the start of a new reign for British industry.Huge thanks to everyone who joined us and helped make it such a special evening.#Manufacturing #BritishIndustry #IndustrialAI #ArtificialIntelligence #Innovation #AdvancedManufacturing #FutureOfManufacturing
0322	
0323	Sebastian Pattinson
0324	Associate Professor at University of Cambridge; Co-Founder at Matta
0325	30/03/26, 23:30 PDT • 1mo •
0326	Very excited that our new paper on 'High-performance ionic conductive 3d-printed cell-free hydrogel for soft tissue engineering scaffolds' has been published in Advanced Composites and Hybrid Materials! Soft tissue repair remains a major challenge, and better scaffold materials are needed to match both the structure and function of native tissue. Because many soft tissues rely on ionic signalling, scaffolds need to do more than provide mechanical support. One of the main challenges in scaffold design is balancing ionic conductivity with mechanical strength. In this work, we show a tunable and scalable route to achieving both. This opens up exciting possibilities for tissue repair, bioelectronic interfaces, and implantable devices.Dick Ferieno Firdaus, Andi Kuswoyo, Andrés García Sampedro, PhD, Sebastiaan Hoek, Mohd Ifwat Mohd Ghazali, Miaomiao Zou and Ljiljana Fruk #biomaterials #3Dprinting #medicaldevices
0327	
0328	Sebastian Pattinson
0329	Associate Professor at University of Cambridge; Co-Founder at Matta
0330	26/03/26, 16:44 PDT • 1mo •
0331	Last week, Matta hosted 'Sentient Factories: AI and the Future of Manufacturing' at the Royal Academy of Engineering.We brought together around 80 people from industry, government, academia, startups and investment, from CTOs of multinationals to engineers with decades of factory-floor experience.We heard excellent talks from John Lazar, President of the Royal Academy of Engineering, Kanishka Narayan MP, Minister for AI and Online Safety, Tim Minshall, Head of the Institute for Manufacturing (IfM), University of Cambridge, and Douglas Brion, Co-Founder and CEO of Matta.I was also delighted to chair a panel on Manufacturing AI in practice, and am especially grateful to our panellists: Sophia Martin (Ktiri) (1st Kind), Alan Patterson (BeyondMath), Jerry Gray (Bowers & Wilkins) and Steven Grace (Cummins Inc.).The clearest takeaway from the evening was a genuine willingness to collaborate. What it also reinforced for me is that making AI work for UK manufacturing will depend on getting manufacturers, technologists, policymakers and investors in the room together more often.We have had a lot of encouragement to do more events like this, and we are looking forward to doing exactly that.Royal Academy of Engineering The ERA Foundation Department of Engineering at the University of Cambridge Department for Science, Innovation and Technology #AI #Manufacturing #IndustrialAI #FutureOfManufacturing #UKManufacturing
0332	
0333	Alex Obadia
0334	Programme Director at ARIA
0335	25/03/26, 11:08 PDT • 1mo • Edited •
0336	🚨 We are on the lookout for a partner to help us build the Scaling Trust Arena 🚨 £10m contract. 2-page proposals. Apply by April 14th. More details below, link at the end!AI agents are increasingly negotiating, transacting, coordinating with other agents on our behalf. Right now, there's no rigorous way to know whether those interactions are secure. We're funding the tools to change that as part of the Advanced Research + Invention Agency (ARIA) Scaling Trust r&d programme, the Arena is where they'll be stress-tested in a live, multi-agent adversarial environment. Anyone in the world will be able to participate in it, and compete for a portion of the multi-million pound prize pool.For the right team, this is a chance to build critical infrastructure for AI security from the ground up, with real resources, lots of autonomy, and high stakes.This will be extremely challenging, but also very fun 🤠🎢🏟️Who You AreWe have no hard constraints on org type. You might be a startup, a consultancy, a research group, a frontier AI lab, a nonprofit, or a group mobilising specifically for this. What matters is that you're deeply technical, you're ambitious, you move fast, and you want to embed with us as part of the team.Apply & Learn More: https://lnkd.in/d-8Rbijg
0337	
0338	Cummins Europe
0339	24/03/26, 09:17 PDT • 1mo •
0340	Exploring the future of manufacturing through AI Last week, Jonathan Wood (Vice President - Chief Technical Officer) and Steven Grace (Automation & Technology Leader) attended Sentient Factories: AI and the Future of Manufacturing at the Royal Academy of Engineering hosted by AI technology company Matta.The event brought together leaders across UK manufacturing to discuss, share best practices, and explore how AI can be effectively developed and deployed across the industry.Steven also joined a panel discussion, contributing real-world insights on implementation, challenges, and opportunities as manufacturers adapt to this rapidly evolving landscape.With contributions from industry, academia, and government, the event highlighted a clear message: collaboration will be key to unlocking the full potential of AI in manufacturing.#Cummins
0341	
0342	Douglas Brion
0343	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0344	24/03/26, 08:32 PDT • 1mo •
0345	Last week, the Matta team had the pleasure of hosting "Sentient Factories: AI and the Future of Manufacturing" at The Royal Academy of Engineering, bringing together around 80 guests from industry, government, academia, startups and investment.We had people in the room from every part of the country, from CTOs of multinationals to manufacturing engineers with decades of experience. And that was exactly the point.If the UK is serious about using AI to strengthen manufacturing, we need far more conversations that bring together the people building the technology, the policy, and the people living the reality of the factory floor.The evening featured brilliant talks from John Lazar, President of the Royal Academy of Engineering, Kanishka Narayan MP, Minister for AI and Online Safety, Tim Minshall, Head of the Institute for Manufacturing (IfM), University of Cambridge, and, somehow, myself too.We also had a fantastic panel with Sophia Martin (Ktiri) (1st Kind), Alan Patterson (BeyondMath), Jerry Gray (Bowers & Wilkins) and Steven Grace (Cummins Inc.).What made the evening special was the energy in the room. There was real ambition, real curiosity, and a clear sense that the UK has a major opportunity to combine its industrial heritage with its strength in AI to build the factories of the future.We have had an overwhelming number of kind messages afterwards, and lots of requests to do more evenings like this, so hopefully this was just the first.Royal Academy of Engineering Enterprise Hub University of Cambridge Department for Science, Innovation and Technology The ERA Foundation Royal Commission for the Exhibition of 1851 #AI #Manufacturing #IndustrialAI #FutureOfManufacturing #UKManufacturing
0346	
0347	Sebastian Pattinson
0348	Associate Professor at University of Cambridge; Co-Founder at Matta
0349	17/03/26, 03:56 PDT • 1mo •
0350	Enjoyed talking about vision-based control at the 3D printing workshop at the University of Exeter yesterday. Thank you for the invitation Jingchao Jiang and the interesting discussion!
0351	
0352	Sebastian Pattinson
0353	Associate Professor at University of Cambridge; Co-Founder at Matta
0354	09/03/26, 15:55 PDT • 1mo •
0355	Trust will be one of the defining challenges for AI in the physical world. I enjoyed presenting at SoTA/ARIA’s Frontiers Night and seeing these questions explored so thoughtfully. Thank you to the speakers, organisers, and everyone who joined the conversation.
0356	
0357	Society for Technological Advancement (SoTA)
0358	04/03/26, 06:43 PDT • 2mo • Edited •
0359	SoTA's Frontiers Night on Cyber-Physical TrustLast night we explored the frontiers of multi-agent systems navigating, negotiating, and enforcing agreements in our physical reality — from agent-to-agent communication and secret collusion, to verifiable manufacturing, world models for critical infrastructure, and cryptographic identities for embodied AI.Thank you to our Demonstrators and attendees for the questions and discussion.​- Sebastian Pattinson, Cofounder & Chief Scientist at Matta; Associate Professor at the University of Cambridge- Nicola Greco, Technical Adviser at ARIA & Co-Designer of the Scaling Trust programme- ​Christian Schroeder de Witt, Head of the University of Oxford Witt Lab for Trust in AI; defined the field of multi-agent security​- Enrico Bottazzi, PI for NDAI Zones; Cofounder of Machina-iO- Otter Quarks, Cofounder & CTO of Humanis- Mary Maller, Senior Cryptography R&D at InversedThank you to the Advanced Research + Invention Agency (ARIA) for the support and to Netholabs for the space.Join our Trust Everything, Everywhere Hackathon this weekend (7-8th March) to build the security primitives necessary to deploy AI into critical cyber-physical systems. Link in the comments below.
0360	
0361	Imaging and Machine Vision Europe
0362	05/03/26, 04:53 PDT • 2mo •
0363	⚡👁️🏭 Douglas Brion CEO of Matta AI , explains why manufacturing stands to be the biggest beneficiary of real-world AI... 🔎🤖🔧 From self-supervised inspection to global operational analytics, he outlines how Matta is combining simple yet robust hardware with unsupervised AI learning and data to improve manufacturing."If you can’t measure something, you can’t make it.”Register for free to Imaging and Machine Vision Europe to read the full interview 👉 https://lnkd.in/eqnhQH7v#MachineVision #AIInspection #DeepLearning #AnomalyDetection #FewShotLearning #QualityControl #IndustrialVision #DefectDetection #SmartManufacturing #ComputerVision #EdgeAI #IndustrialAIImage: Matta AI
0364	
0365	Sebastian Pattinson
0366	Associate Professor at University of Cambridge; Co-Founder at Matta
0367	25/02/26, 15:56 PDT • 2mo •
0368	Delighted that the #MSCA Marie Skłodowska-Curie Postdoctoral Fellowship applicant I supported last year was successful. They’ll be joining my group to work on multimodal models for industrial robotic processes. If you’re considering an MSCA application in a related area, I’m always happy to chat with prospective applicants.
0369	
0370	Sebastian Pattinson
0371	Associate Professor at University of Cambridge; Co-Founder at Matta
0372	23/02/26, 06:32 PDT • 2mo •
0373	Matta is hiring AI Scientists to build foundational models for manufacturing. Messy real datasets, real impact on real problems!
0374	
0375	Sebastian Pattinson
0376	Associate Professor at University of Cambridge; Co-Founder at Matta
0377	19/02/26, 09:02 PDT • 2mo •
0378	We’ve just published a new open-access paper on predicting geometric accuracy in metal filament 3D printing, using high-resolution CT scanning before and after sintering.'Characterisation of Geometric Accuracy in Metal Fused Filament Fabricated Parts Using X-ray Computed Tomography.'Congrats to Roham Sadeghi Tabar, Andi Kuswoyo and Christos Margadji_UVpT
0379	
0380	Douglas Brion
0381	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0382	12/02/26, 09:22 PDT • 2mo •
0383	Manufacturing is the bedrock of our lives, help us improve it and keep it punching in the West. We’re now deploying into two new factories every month – and we need to move faster.If you’re excited about applying the latest industrial AI models in the physical world, we’re hiring across multiple roles:- AI Scientists: Push the state of the art in manufacturing foundation models and few-shot vision. Real research. Real application. Big impact.- Forward Deployed Engineers: Deploy hardware into factories and work side-by-side with customers to solve real manufacturing challenges. Your life is basically ‘How It’s Made’.- Product Engineers: Build the next-generation UI and platform for managing and controlling factories. Industrial software that actually feels modern.- Founding GTM: - Help us convert the 400+ factories already in our pipeline. Develop the playbook and scale it properly.- Business / Operations: From expanding into new geographies to securing major customers and keeping the team running smoothly.- Open Application: If you’re exceptional at what you do and believe the physical world is where it’s at, apply anyway.Reach out to careers@matta.ai!
0384	
0385	Sebastian Pattinson
0386	Associate Professor at University of Cambridge; Co-Founder at Matta
0387	03/02/26, 06:30 PDT • 3mo •
0388	Excited to share that our recent paper, IDfRA: Self-Verification for Iterative Design in Robotic Assembly, has been accepted at IEEE International Conference on Robotics and Automation (ICRA)! If robotic assembly is going to scale beyond carefully controlled setups, we need workflows that don’t depend on heavy manual effort or brittle, hard-coded assumptions. This work moves toward an iterative loop where the system plans, executes, and then verifies its actions, using that verification to improve the design and the assembly plan over time.Congratulations to authors Nishka Khendry and Christos Margadji
0389	
0390	Douglas Brion
0391	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0392	03/02/26, 01:24 PDT • 3mo •
0393	Over the next 3 days, Matta is exhibiting at Southern Manufacturing & Electronics 2026.It also marks one year since our very first trade show (Southern last year) so it’s a bit of a full-circle moment. Really looking forward to catching up with so many familiar faces from UK manufacturing.If you’re curious about how to increase productivity, reduce waste, and improve quality through practical, shopfloor-ready AI, come and say hi. We’ve brought fun real-world demos (and we genuinely love people trying them out).Come join us getting a little too excited about manufacturing! Let’s chat. 🙂#manufacturing #ukmanufacturing #industrialai #quality #continuousimprovement #automation #machinevision #southernmanufacturing2026Tom Walker Christos Margadji Sebastian Pattinson Ollie Rosen Damjan Denic
0394	
0395	Sebastian Pattinson
0396	Associate Professor at University of Cambridge; Co-Founder at Matta
0397	19/01/26, 06:57 PDT • 3mo •
0398	Matta is hiring Forward Deployed Engineers following its recently announced $14m fundraising.If you like fast, hands-on problem solving in real production environments, combining software, hardware, and customer work, this role could be for you. You’ll help turn Matta’s AI systems into something factories can rely on, and shape how deployments scale.
0399	
0400	Sebastian Pattinson
0401	Associate Professor at University of Cambridge; Co-Founder at Matta
0402	05/01/26, 08:22 PDT • 4mo •
0403	We have published a new paper in Advanced Functional Materials on “Viscoelasticity-Induced Controllable Periodic Meso-Textures of Liquid Crystal Polymers in Additive Manufacturing.”In extrusion 3D printing of liquid crystalline polymers, we show that periodic meso-scale textures form spontaneously and can be tuned through processing parameters, providing a simple route to programmed structure. Since the anisotropy that drives texture formation can also weaken interlayer bonding, we identify processing conditions that strengthen layer-to-layer adhesion and increase puncture energy absorption. Beyond mechanics, these controllable textures enable terahertz wave manipulation and can guide nerve cell alignment, opening paths to new biomedical and other devices.This was a genuinely collaborative, interdisciplinary effort. Special congratulations to first author, Miaomiao Zou, who drove the work forward.https://lnkd.in/eHVbxXmH#AdditiveManufacturing #3DPrinting #MaterialsScience #AdvancedFunctionalMaterials #medicaldevices
0404	
0405	Sebastian Pattinson
0406	Associate Professor at University of Cambridge; Co-Founder at Matta
0407	29/12/25, 06:30 PDT • 4mo •
0408	Had a great time on the Startup Insider podcast talking about what it takes to get AI working in real factories, beyond demos and into production. We also discuss how Matta makes this practical with plug-and-play systems that deliver granular and high-level process insights and can support closed-loop control.Episode is in German!
0409	
0410	Startup Insider
0411	22/12/25, 07:51 PDT • 4mo •
0412	Der schwierige Teil ist nicht, sich Dinge im Computer auszudenken, es ist, sie im großen Maßstab zum Laufen zu bringen. Sebastian Pattinson, Co-Gründer von Matta, spricht in der neuen Startup Spotlight Folge über die Herausforderungen der industriellen Fertigung. Sein Team baut KI-Systeme, die Fabrikwissen erfassen und skalieren. Von Polymerherstellung bis Automotive: Mattas Plug-and-Play-Vision-Systeme sind bereits in über 300 Fabriken in der Pipeline. Im Dezember sicherte sich das Cambridge Spin-out 14 Millionen Dollar von Lakestar.Link in den Kommentaren!
0413	
0414	Sebastian Pattinson
0415	Associate Professor at University of Cambridge; Co-Founder at Matta
0416	10/12/25, 08:51 PDT • 4mo •
0417	Very excited to finally share that Matta has raised $14M to push forward industrial AI and move closer to sentient factories that can see, understand and improve themselves autonomously.Also very grateful to be working with investors who care deeply about the future of manufacturing, including Lakestar, Giant Ventures, InMotion Ventures, Redseed, 1st Kind, Unruly Capital and Boost VC.Most of all, thank you to the Matta team, an exceptional group of engineers, scientists and operators. It has been an incredible few years taking this research from the lab into real factories, and I am even more excited about what comes next.
0418	
0419	Matta
0420	10/12/25, 04:10 PDT • 4mo •
0421	Big news from Team Matta today.We’re excited to share that we’ve raised $14M to accelerate our work on industrial AI and build what we call sentient factories – factories that can see, understand, and improve themselves in real time.Our plug-and-play AI is already running on lines from polymer manufacturing and metal casting to bottling and consumer electronics and in the factories of quality brands like Bowers & Wilkins. With a system that can learn a new line in days (sometimes minutes) from very little data, we’re now working with hundreds of factories in our pipeline and adding new installations every few weeks.We’re super excited to have Lakestar and Giant Ventures as lead investors, and to be working with Redseed, InMotion Ventures, 1st Kind, Unruly Capital and Boost VC.Huge thanks as well to Innovate UK and the Royal Academy of Engineering for their amazing support. We’re incredibly grateful to our supporters, early customers, the University of Cambridge and Institute for Manufacturing (IfM), University of Cambridge for enabling our initial research, and the wider UK manufacturing community who have believed in this mission from the start.Now the fun part: putting capital to work!! We’ll be:• Rolling out Matta to many more factories across the UK, Europe, and the US• Doubling down on self-tuning machines with OEM partners like Caracol AM• Growing our team of world-class cracked engineers, researchers, and operators who love real factories as much as we doIf you’re running a factory and want to boost quality, cut waste, or just make your line a lot smarter – we’d love to talk. And if you’re an engineer or operator who gets excited about cameras, AI, how things are made, and gnarly real-world data, keep an eye out… we’re hiring!! #IndustrialAI #FactorySentience #Manufacturing #UKManufacturing #DeepTech #BritishDynamism
0422	
0423	St John's Innovation Centre Ltd
0424	13/11/25, 07:09 PDT • 5mo • Edited •
0425	We enjoyed a very special Cambridge-style book club last night, featuring a fascinating and lively discussion chaired by Barnaby Perks, CEO of SJIC, with an inimitable duo: David Cleevely CBE FREng FIET and Professor Tim Minshall.Key takeaways included the power of storytelling and the importance of networks for growth. David emphasised the need, in the wake of AI, to “ensure events unfold to your advantage.” Tim referenced the forthcoming House of Lords paper Bleeding to Death, noting that although the UK has a strong global R&D base, it has historically struggled to commercialise it and remains insufficiently networked. In manufacturing, he also highlighted innovators like Matta.ai, who are developing industrial AI solutions for factories.Many thanks to Wilson Partners for sponsoring the event, and to everyone who attended. David and Tim’s books — Serendipity and Your Life is Manufactured — are available here:David Cleevely: https://lnkd.in/dGzykVQ6Tim Minshall: https://lnkd.in/dzakQiwVPlease follow our events at the Centre at https://lnkd.in/draKA52g including our forthcoming First Flight Venture Center Delegation to North Carolina on 19th-21st November, and Finance Masterclass on Tuesday 18th November.
0426	
0427	Sebastian Pattinson
0428	Associate Professor at University of Cambridge; Co-Founder at Matta
0429	27/10/25, 16:33 PDT • 6mo •
0430	Had a great time talking about AI for manufacturing research and Matta at Heriot-Watt University last week. Thank you Assylbek Nurgabdeshov and Luciana Blaha, PhD for the invitation and excellent hosting! #AI #manufacturing
0431	
0432	Sebastian Pattinson
0433	Associate Professor at University of Cambridge; Co-Founder at Matta
0434	13/10/25, 13:22 PDT • 6mo •
0435	Really enjoyed giving a seminar at the The University of Manchester last week on some of our recent work on hybrid reasoning in manufacturing processes. Thank you to Charlie C.L. Wang for the invitation!
0436	
0437	Sebastian Pattinson
0438	Associate Professor at University of Cambridge; Co-Founder at Matta
0439	17/09/25, 07:00 PDT • 7mo •
0440	Come build AI systems that run in factories, not demos. Matta is hiring frontend, backend, AI scientists, and forward-deployed & hardware engineers.#AI #MattaAI #Hiring
0441	
0442	Douglas Brion
0443	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0444	16/09/25, 07:59 PDT • 7mo • Edited •
0445	We’re hiring and not messing around. 🧠🏭Matta is growing fast – with new factory installations every month, from electronics and castings to aerospace parts and whisky bottles. We’re building industrial AI that actually works – deploying software, hardware, and AI models into some of the messiest, noisiest, most fascinating real-world environments you can imagine. And we need more brilliant people to do it with!Right now, we’re especially looking for:- 👩‍🎨 Frontend Engineers who want to invent the interface layer for how factories are monitored and controlled- 🧱 Backend Engineers who love building the scalable infrastructure to handle thousands of connected and streaming systems- 🧠 AI Scientists & Vision Researchers from top labs- 🔌 Forward-Deployed & Hardware Engineers who love getting stuck in on the factory floorThis is hard stuff. We’re not in a cozy ML sandbox. We’re doing AI at the edge. With flaky networks, weird lighting, moving robots, tight latencies, and high stakes. We’re building general-purpose systems that can adapt to a thousand different factory settings – not a brittle solution. But that’s exactly what makes it fun.You’ll be joining a small, high-functioning team from places like Google X, Microsoft, IBM, BBC R&D, Cambridge, MIT, and Imperial. We’re tight-knit, a bit batty, and truly "full-stack": from lens calibration and building gantries to foundation model research, factory OS design, and AI infra at scale.We like:- High-agency builders who’ve shipped serious things (startups? even better)- People who learn fast and don’t mind breaking a few things along the way- Engineers who can hold their own in Python and the outskirts of Birmingham- A love for manufacturing, mess, and the sheer joy of learning how things are made- Furious tea and coffee drinkers (bonus points if you delete cake 🍰)📬 Our office is 5 mins from Old Street. Drop us a message and/or email careers@matta.ai – or just send something cool you’ve built. Rebels welcome.#AI #ComputerVision #Robotics #FactorySentience #FrontendEngineering #BackendEngineering #IndustrialAI #SmartManufacturing #UKManufacturing #MattaAI #Hiring #BritishDynamism
0446	
0447	Sebastian Pattinson
0448	Associate Professor at University of Cambridge; Co-Founder at Matta
0449	27/08/25, 03:32 PDT • 8mo •
0450	Our new paper in Additive Manufacturing presents an uncertainty-aware reinforcement learning agent for quality assurance in extrusion additive manufacturing. The agent adjusts key parameters in real time, leveraging a vision-based uncertainty module to robustly correct defects and transfer reliably from simulation to real-world printing. The work illustrates how adaptive agents could reshape the future of manufacturing through robustness, intelligence, and scalability.Congratulations to Xiaohan L.!#manufacturing #ai #computervision #additivemanufacturinghttps://lnkd.in/gYGbRixs
0451	
0452	Douglas Brion
0453	Industrial AI for factories. CEO @ Matta | PhD Engineering, Uni. of Cambridge
0454	24/07/25, 05:58 PDT • 9mo •
0455	Physical AI is the most impactful space to work in today and for the next decade.Join our incredibly gifted team and help build the infrastructure powering industrial AI in factories around the world. Explore roles: https://lnkd.in/eGdBEzNGWe’re deploying AI at scale into real factories - from automotive and electronics to aerospace, nuclear submarines, waterproof coats and even gourmet cheese... 🚗💻✈️🚢🧥🧀You’ll be building the backend systems that let AI actually touch machines. Robust, low latency infrastructure powering the best industrial AI, while transforming how our customers run their factories through our data driven platform.We’re a world class team of engineers, operators and scientists, backed by top VCs and moving fast ⚡If you’re tired of working on stuff that doesn’t matter, this is your moment.This Mattas.#AI #IndustrialAI #Manufacturing #BackendEngineering #StartupJobs #DeepTech #MachineLearning #Industry40 #Hiring #InfrastructureEngineering
0456	
0457	Sebastian Pattinson
0458	Associate Professor at University of Cambridge; Co-Founder at Matta
0459	20/07/25, 05:23 PDT • 9mo •
0460	Matta is also hiring a Senior Software Engineer #hiring #AI #manufacturing #deeptech
0461	
0462	Sebastian Pattinson
0463	Associate Professor at University of Cambridge; Co-Founder at Matta
0464	20/07/25, 05:19 PDT • 9mo •
0465	Matta is hiring a Senior Backend Engineer to help build and scale its manufacturing OS
0466	
0467	Sebastian Pattinson
0468	Associate Professor at University of Cambridge; Co-Founder at Matta
0469	23/06/25, 02:46 PDT • 10mo •
0470	Matta is hiring its first Forward Deployed Engineer!This is a great opportunity if you like solving real-world problems, getting hands-on in factories, and making cutting-edge AI actually work where it matters.#hiring #AI #manufacturing #deeptech
0471	
0472	Sebastian Pattinson
0473	Associate Professor at University of Cambridge; Co-Founder at Matta
0474	16/05/25, 08:30 PDT • 11mo •
0475	Great to join the West Suffolk Manufacturing Group and share what we're working on at Matta alongside Douglas Brion. Fantastic turnout and discussions about how AI could help local manufacturers. Thanks to James Talbot and Richard Bridgman OBE for the invitation!
0476	
0477	James Talbot
0478	Principal Growth Officer, West Suffolk
0479	15/05/25, 08:04 PDT • 11mo •
0480	Just to re-iterate what my colleague Clare Harding said yesterday.A fantastic meeting yesterday of the West Suffolk Manufacturing Group. If not a record turnout, then it was close to it! Thanks to all those who came along.Thanks to our Chair Richard Bridgman OBE from Warren and Cllr Indy Wijenayaka at West Suffolk Council for his continued support.Special thanks to Babette Norman and Chloe Ludkin CMgr MCMI from the brilliant Treatt. More special thanks to Sebastian Pattinson and Douglas Brion from the amazing https://www.matta.ai/. If you're in manufacturing then you have to check out what Matta is doing. Finally, special thanks to Ben Courts at Make UK, for his update on the Q1 Manufacturing Outlook Report and James Williamson at Made Smarter UK.Amir Farboud Andrew Lyes Andy Connacher Andy Fairs Anthony Pateman Barry Dowman Brian Prince David Harris Dr Dorian H. Emilianne Buisson Esther Cornell Gary Cocksedge, DipNEBOSH PCQI GradIOSH Raoul Watson James Gulliver James Hobbs John Fordham Mark N. Keith Carver Michael Nelson Phil Stittle Oliver Claydon Sharon Eighteen Steve Logan Phil Smailes Julie Baird Andrea Mayley Annie Richardson
0481	
0482	Tim Minshall
0483	Dr John C Taylor Professor of Innovation and Head of Institute for Manufacturing, University of Cambridge
0484	30/04/25, 05:08 PDT • 1yr •
0485	"[..] we are rediscovering something fundamental: the ability to make things is a vital capability for any national economy and local community that wishes to be resilient, secure and sustainable. And with that restored visibility, hopefully we won’t again forget how vital it is to all our lives."#manufacturing #sustainability #industrialpolicy #tariffs #globalisation #resiliencehttps://lnkd.in/e7GzEDz2
0486	
0487	Churchill College, University of Cambridge
0488	13/02/25, 09:23 PDT • 1yr •
0489	Congratulations to Churchill College Fellow Prof. Tim Minshall on the publication of his compelling new book 'Your Life Is Manufactured: How We Make Things, Why It Matters and How We Can Do It Better'.Tim reveals the hidden pathways and intricate stories behind everyday products, guiding readers through a fascinating exploration of the worldwide manufacturing ecosystem. The book is published by Faber and Faber and is available now in hardback, digital, and audiobook formats from all major booksellers.Tim's primary goal was to create an accessible resource that communicates a vital message, particularly to those outside the manufacturing sector. This message, which he powerfully articulates in the book's closing paragraph, captures his core belief:"Despite the scale, uncertainty and complexity of the challenges our planet and our communities face today, there is one thing of which I am now more than ever convinced: it is manufacturing that will deliver a more sustainable, more resilient and more equitable future for us all. And despite what I said at the start of this book, manufacturing is clearly not 'another world' – it is something of which we are all a part, and in which we all play a role. And together, we really can manufacture a better world."Institute for Manufacturing (IfM), University of Cambridge Department of Engineering at the University of Cambridge University of Cambridge #manufacturing #sustainability
0490	
0491	[CLEANER NOTE: inferred section boundary]
0492	Company Insights
0493	
0494	Matta
0495	Creating industrial AI for factory sentience
0496	Software Development
0497	London
0498	11-50 employees
0499	
0500	Total employee count
0501	14 total employees
0502	
0503	Median employee tenure ‧ 0.8 years
0504	
0505	Employee distribution and headcount growth by function
0506	Engineering 43%
0507	Business Development 21%
0508	Entrepreneurship 21%
0509	Product Management 7%
0510	
0511	[CLEANER NOTE: inferred section boundary]
0512	External Mentions & Quotes
0513	
0514	IfM spin-out Matta raises $14M to transform how products are designed and manufactured
0515	
0516	Matta, an industrial AI spin-out from the Institute for Manufacturing (IfM), has raised $14M in funding to transform how products are designed and manufactured.
0517	
0518	Matta’s AI gives factories the ability to see, understand, and improve themselves in real time, understanding any production line within days. It spots defects, traces root causes, and helps teams fix problems before they become costly.
0519	
0520	The technology is highly adaptable, capable of working across everything from electronics and automotive to defence and apparel, whether on manual inspection stations, conveyor lines, or robot arms to redefine how products are conceived and created. This generalisation capability is driving strong demand, with 300+ factories in the pipeline and a new installation every two weeks.
0521	
0522	Matta was founded on pioneering research from the IfM, where co-founders Douglas Brion, who completed a PhD in deep learning-enabled control, and Sebastian Pattinson, Associate Professor of Engineering and leader of the IfM's Computer-Aided Manufacturing group, first met.
0523	
0524	The seed round was led by Lakestar alongside investors Giant Ventures - who led the pre-seed - RedSeed VC, InMotion Ventures, 1st Kind (Peugeot family), Unruly Capital, and Boost VC, with grant support from Innovate UK and the Royal Academy of Engineering.
0525	
0526	Doug Brion, Co-founder and CEO of Matta, said: “Everything around us is manufactured, from the mug on your desk to the optical cables carrying our Netflix binges. Everyone talks about the glamorous side of manufacturing: generative design, material discovery, digital twins, but few spend time on the factory floor.
0527	
0528	"The hard part isn’t dreaming things up inside a computer; it’s making them work at scale. Manufacturing still runs on human know-how, the kind that lets someone on the line kick a machine just right, or run a finger over a scratch, and say ‘that’s thirty-four microns wide.’ We’re using AI to capture and scale that tacit knowledge, so engineers can design things that actually work in the real world. It’s time to manufacture the impossible."
0529	
0530	Manufacturing is at an inflection point
0531	Manufacturing underpins a third of global economic output yet remains plagued by inefficiencies that waste up to 20 per cent of production value and raise emissions.
0532	
0533	After decades of deindustrialisation, factories are exposed to external geopolitical shocks and must do more with less. Matta provides a practical route to productivity, quality and resilience on today’s shop floor.
0534	
0535	At the same time, energy costs are rising, supply chains are fragile, and workforces are ageing. Factories must reshore, decarbonise, and do more with fewer skilled hands. In the UK, vacancies already outnumber qualified engineers, and costs continue to rise. Across Europe and the US, the story is the same.
0536	
0537	Matta: building the first sentient factories
0538	Matta develops AI that learns the physical rules of production and applies them on the line. Its first product uses unsupervised and self-supervised computer vision to automate quality control and anomaly detection, perform measurements, diagnose root causes, and recommend corrective actions in real time. A central platform lets teams monitor every camera, analyse results and trace parts across the factory for live visibility of issues and bottlenecks.
0539	
0540	Matta delivers this as a full plug-and-play system combining hardware, factory integration, AI research, and software. Most deployments are live within hours, with cameras inspecting automatically after a short learning period. In one polymer manufacturing deployment, Matta achieved over 99% defect-detection accuracy with just ten minutes of data. Recent projects range from inspecting high-speed bottling for defects with a global drinks brand to working with Bowers & Wilkins, where Matta’s AI rapidly measures speaker components to catch issues before assembly.
0541	
0542	Beyond detection, Matta partners with OEMs to enable machines to tune themselves. One of these OEMs, Caracol, is integrating Matta’s vision AI for closed-loop control, linking real-time inspection to automatic parameter adjustments on industrial printers and large-format robot additive manufacturing cells.
0543	
0544	Led by world-class academic founders
0545	Today, Matta is a fast-growing team with experience from MIT, Imperial, BBC R&D, Google X, and Microsoft. Akis Bratsos of Lakestar said: “We are thrilled to be supporting Doug, Sebastian and the Matta team as they go on to revolutionise manufacturing through the use of industrial AI. Their approach combines cutting-edge technology together with fast time to value that is rare in the sector.”
0546	
0547	Madelene Larsson of Giant Ventures said: “Doug and the team have developed a transformative approach to rapidly training factory-ready AI with minimal data, which has the potential to reshape how products are made. We're excited to back the team as they sprint towards a future defined by autonomous manufacturing and inverse design."
0548	
0549	The latest funding will accelerate customer adoption and AI development, expand self-serve deployment, and support Matta’s expansion into key manufacturing regions across Europe and the US, advancing the company’s vision for fully autonomous, end-to-end production.
0550	
0551	About Matta
0552	Matta is building industrial AI for factory sentience, enabling factories to sense, understand, and adapt in real time. Based on pioneering Cambridge research and driven by a team with experience from MIT, Google X, and Microsoft, Matta is replacing the traditional designengineer- build workflow with AI. By cutting waste, boosting productivity, and opening new frontiers in manufacturing, Matta is redefining the future of industrial innovation.
0553	
0554	Date published
0555	10 December 2025
0556	
0557	Industrialtech
0558	Matta raises $14M to develop “sentient factory” technology
0559	The Cambridge spin-out’s self-learning system adapts to a wide range of production lines within days and delivers high accuracy with minimal training data.
0560	Tamara Djurickovic
0561	10 December 2025
0562	
0563	London-based Matta, an industrial AI spin-out from the University of Cambridge, has raised $14M in seed funding to transform how products are designed and manufactured. The round was led by Lakestar, with participation from Giant Ventures, RedSeed VC, InMotion Ventures, 1st Kind (Peugeot family), Unruly Capital, and Boost VC, alongside grant support from Innovate UK and the Royal Academy of Engineering.
0564	
0565	After decades of deindustrialisation, many factories are now exposed to geopolitical shocks and under pressure to deliver more with fewer resources. At the same time, energy costs are rising, supply chains remain fragile, and workforces are ageing. Manufacturers are being asked to reshore, decarbonise, and operate with fewer skilled workers. Workforce gaps and increasing operational costs are becoming common across Europe, and the US.
0566	
0567	Matta offers a practical way to improve productivity, quality, and resilience on today’s shop floors. The company develops AI that learns the physical rules of production and applies them directly on the line. Its first product uses unsupervised and self-supervised computer vision to automate quality control and anomaly detection, perform measurements, diagnose root causes, and recommend corrective actions in real time.
0568	
0569	A central platform allows teams to monitor every camera, analyse results, and trace parts across the factory, giving live visibility into issues and bottlenecks. Matta delivers this as a plug-and-play system that combines hardware, factory integration, AI research, and software. Most deployments become operational within hours, with cameras inspecting automatically after a short learning period.
0570	
0571	Manufacturing still runs on human know-how, the kind that lets someone on the line kick a machine just right, or run a finger over a scratch, and say, ‘that’s thirty-four microns wide.’ We’re using AI to capture and scale that tacit knowledge, so engineers can design things that actually work in the real world. It’s time to manufacture the impossible,
0572	explains Doug Brion, Co-founder and CEO of Matta.
0573	
0574	Matta’s AI enables factories to monitor, analyse, and optimise their operations in real time, learning any production line within days. It detects defects, identifies root causes, and helps teams address issues before they become costly.
0575	
0576	The technology is general-purpose and highly adaptable, operating across sectors such as electronics, automotive, defence, and apparel, and integrating with manual inspection stations, conveyor lines, and robotic systems. Beyond defect detection, Matta also collaborates with OEMs to enable machines to adjust their own settings.
0577	
0578	The new investment will accelerate the rollout of Matta’s technology, enhance its AI capabilities, expand self-serve deployment, and support the company’s entry into key manufacturing regions in Europe and the US as it pursues increasingly autonomous, end-to-end production.
0579	
0580	Industrial AI startup Matta raises $14M to build Sentient Factories
0581	Matta, an industrial AI spin-out from the University of Cambridge, has raised $14M in funding to transform how products are designed and manufactured.
0582	The seed round was led by Lakestar alongside investors Giant Ventures - who led the pre-seed - RedSeed VC, InMotion Ventures, 1st Kind (Peugeot family), Unruly Capital, and Boost VC, with grant support from Innovate UK and the Royal Academy of Engineering.
0583	
0584	Matta's AI gives factories the ability to see, understand, and improve themselves in real time, understanding any production line within days. It spots defects, traces root causes, and helps teams fix problems before they become costly.
0585	
0586	The technology is generalist and highly adaptable, capable of working across everything from electronics and automotive to defence and apparel, whether on manual inspection stations, conveyor lines, or robot arms, to redefine how products are conceived and created. This generalisation capability is driving strong demand, with 300+ factories in the pipeline and a new installation every two weeks.
0587	
0588	Doug Brion, Co-founder and CEO of Matta, said: "Everything around us is manufactured, from the mug on your desk to the optical cables carrying our Netflix binges. Everyone talks about the glamorous side of manufacturing: generative design, material discovery, digital twins, but few spend time on the factory floor.
0589	
0590	"The hard part isn't dreaming things up inside a computer; it's making them work at scale. Manufacturing still runs on human know-how, the kind that let someone on the line kick a machine just right, or run a finger over a scratch, and say, 'that's thirty-four microns wide.' We're using AI to capture and scale that tacit knowledge, so engineers can design things that actually work in the real world. It's time to manufacture the impossible."
0591	
0592	Manufacturing is at an inflection point.
0593	Manufacturing underpins a third of global economic output yet remains plagued by inefficiencies that waste up to 20 per cent of production value and raise emissions. After decades of deindustrialisation, factories are exposed to external geopolitical shocks and must do more with less. Matta provides a practical route to productivity, quality and resilience on today's shop floor.
0594	
0595	At the same time, energy costs are rising, supply chains are fragile, and workforces are ageing. Factories must reshore, decarbonise, and do more with fewer skilled hands. In the UK, vacancies already outnumber qualified engineers, and costs keep climbing. Across Europe and the US, the story is the same.
0596	
0597	Building the first sentient factories
0598	Matta develops AI that learns the physical rules of production and applies them on the line. Its first product uses unsupervised and self-supervised computer vision to automate quality control and anomaly detection, perform measurements, diagnose root causes, and recommend corrective actions in real time. A central platform lets teams monitor every camera, analyse results and trace parts across the factory for live visibility of issues and bottlenecks. Matta delivers this as a full plug-and-play system combining hardware, factory integration, AI research, and software. Most deployments are live within hours, with cameras inspecting automatically after a short learning period.
0599	
0600	In one polymer manufacturing deployment, Matta achieved over 99% defect-detection accuracy with just ten minutes of data. Recent projects range from inspecting high-speed bottling for defects with a global drinks brand to working with Bowers & Wilkins, where Matta's AI rapidly measures speaker components to catch issues before assembly.
0601	
0602	Beyond detection, Matta partners with OEMs to enable machines to tune themselves. One of these OEMs, Caracol, is integrating Matta's vision AI for closed-loop control, linking real-time inspection to automatic parameter adjustments on industrial printers and large-format robot additive manufacturing cells.
0603	
0604	[CLEANER NOTE: inferred section boundary]
0605	Job Postings
0606	
0607	Special Projects
0608	London
0609	Operations
0610	
0611	TL;DR
0612	This job is for you if you enjoy:
0613	the idea of being a founder but with VC funding sorted and a world-class team already around you
0614	a highly visible and key role that is responsible for managing the rhythm of the business and driving strategic initiatives
0615	diving into diverse challenges, from crafting impactful presentations to ensuring seamless operations during high-stakes moments
0616	helping redefine how we as humans manufacture the world around us
0617	
0618	About Matta
0619	Matta is creating industrial AI for factories. We are a group of engineers, scientists, and company builders developing manufacturing foundation models (MFMs) and a general-purpose manufacturing OS to improve the sustainability of manufacturing today and to unlock the unimaginable technologies of tomorrow. What we actually do:
0620	Build insane AI models that understand the physics of manufacturing processes (think futuristic stuff like machines that watch and correct themselves on the fly or even learn how to use brand-new, never-seen-before materials autonomously).
0621	Research new foundational models for manufacturing enabling users to install vision-based inspection and quality control AIs in less than 24 hours! (for context the industry standard is about 6 months).
0622	Think really hard about how manufacturing will look in 10+ years and build a brand-new intuitive OS and interfaces for orchestrating factories, monitoring machines, controlling production, etc. all with AI. For context, we are a small dynamic team from Google X, Microsoft, Cambridge, MIT, Imperial, BBC R&D to name a few. We work a lot and are all close friends – come join the family!
0623	
0624	Special Projects @ Matta
0625	We’re searching for someone to join Special Projects, who will be at the heart of everything we do - steering long-term strategy, supporting fundraising efforts, and helping close customer deals. This role is pivotal to our success, and we’re looking for someone who is ready to partner closely with our CEO, Doug, to bounce ideas around and turn them into reality. This is probably our most important hire and you should be up for learning about and diving into anything. This might even include engineering tasks (for example the other day a massive steel company sent us a bunch of samples and it was all hands on deck to build a rig and demo internally). Clear and effective communication will be at the heart of your role. We’re looking for someone who can distil the team’s often technical, complex, and sometimes chaotic/scatter-brain ideas into concise, polished points that resonate with diverse audiences. This skill will be especially critical when engaging with large corporate partners, where a professional and business-oriented communication style is essential.
0626	
0627	This isn’t your typical gig - expect to work hard and collaborate with an exceptional team of top engineers, scientists, and builders, all obsessed with embodied AI reshaping the manufacturing world.
0628	
0629	About You
0630	A Gandalf - the kind of person who quietly works their magic behind the scenes, making sure everything runs seamlessly (yet pulling off heroic deeds when needed).
0631	Commercially minded – you think in terms of value creation, customer impact, and ROI, not just activity. You can spot opportunities, shape a pitch, and help translate tech into business outcomes that excite partners and investors alike.
0632	You are a problem-solver who proactively tackles challenges before they even surface, keeping the team one step ahead and turning roadblocks into opportunities.
0633	People person: you love working in teams, sharing knowledge, mentoring/teaching others, and embracing feedback (and yes, you’re always game for a team Lego-building break).
0634	You’re adaptable and thrive in dynamic environments where every day brings new challenges.
0635	Optionally a startup veteran with hands-on experience navigating uncertainty, wearing multiple hats, and making the impossible possible - whether as a founder or a core early team member.
0636	Bonus points for familiarity in engineering, AI, software, or manufacturing making you an even stronger fit for the team.
0637	
0638	Above all, we are looking to build a team of creative, out-of-the-box problem solvers. For this, candidates should be:
0639	Capable of setting and reaching ambitious goals, and taking a project from concept to completion.
0640	Self-directed, self-organised, proactive, and comfortable in a dynamic, multi-disciplinary work environment.
0641	Team players with excellent communication and interpersonal skills.
0642	Enthusiastic tea or coffee drinkers who enjoy a good biscuit or two and a good slice of cake (this is the most important criteria).
0643	
0644	What will impress us
0645	Being proactive. Building or sending us example AI or data related projects – even better if related to the role.
0646	Whether you’re a chess grandmaster, a world champion at tiddlywinks, or a badass musician, we’d love to see the hobbies, skills, or activities you take to the next level – we’re always impressed by those who go all in!
0647	Clear passion in our mission, not a random reason to work with us.
0648	
0649	Location
0650	Our London office, 5 minutes from Old Street Station. Think vibrant startup attic vibes with a team that knows when to laugh and when to focus.
0651	
0652	AI Scientist
0653	London
0654	Research
0655	
0656	TL;DR
0657	the incredibly exciting task of building the first foundational models for manufacturing
0658	working at the crossover of software and hardware (we are truly full stack and often are in factories)
0659	dealing with horrible messy real-world datasets and being high IQ to achieve SOTA performance whilst adhering to severe computational constraints
0660	delivering real impact on how we manufacture the world around us
0661	
0662	AI Scientist @ Matta
0663	We’re looking for an AI Scientist to join us in creating a brand-new class of foundation models designed specifically for manufacturing. You’ll get to tackle exciting challenges like:
0664	Inventing new capabilities, such as building models that understand causality – not just predicting what went wrong, but explaining why (e.g., “The temperature here was too high, mate. Lower it in this spot and you’re sorted!”).
0665	Boosting data efficiency and robustness to achieve top-notch accuracy with minimal data. Think teaching our models to learn from a handful of examples and transfer their smarts from one manufacturing setup to another like seasoned pros.
0666	
0667	Oh, and here’s the kicker: all of this needs to work in real-time and run on low compute systems (because let’s face it, factories aren’t exactly decked out with H100 clusters). To give you an idea of the variety you’ll be diving into, one day you might be monitoring beer bottles, and the next, solving challenges with aerospace components. It’s a proper mix making life fun!
0668	This isn’t your typical gig – expect to work hard and collaborate with an exceptional team of top engineers, scientists, and builders, all obsessed with embodied AI reshaping the manufacturing world.
0669	
0670	About You
0671	A machine learning mage: You write clean, scalable, high-performance deep learning code. You take pride in your craft. Proficiency in PyTorch, Tensorflow, Jax, or equivalent is a must (ideally PyTorch).
0672	Knowledge on some of the latest good stuff from transformers to VLMs and NERFs.
0673	Happy to get down and dirty with cleaning our own in-house datasets (no nice benchmarks here) and building custom dataloaders, dataset classes, preprocessing functions etc.
0674	An understanding of classic signal processing approaches and computer vision techniques is super helpful (e.g. fourier, convolutions, cross-correlations, Bhattacharya distance).
0675	You’ve led projects or research from start to finish, overcoming hurdles to create AI for products or high-impact publications (in startups? even better) plus you are a bit batty and want to learn more!
0676	People person: you love working in teams, sharing knowledge, mentoring/teaching others, and embracing feedback (and yes, you’re always game for a team Lego-building break).
0677	You’re adaptable and thrive in dynamic environments where every day brings new challenges.
0678	
0679	Machine Learning Engineer
0680	London
0681	Engineering
0682	
0683	Machine Learning Engineer @ Matta
0684	We’re looking for an ML Engineer to join us in creating a brand-new class of foundation models designed specifically for manufacturing. You’ll get to tackle exciting challenges like:
0685	Inventing new capabilities, such as building models that understand causality – not just predicting what went wrong, but explaining why (e.g., “The temperature here was too high, mate. Lower it in this spot and you’re sorted!”).
0686	Boosting data efficiency and robustness to achieve top-notch accuracy with minimal data. Think teaching our models to learn from a handful of examples and transfer their smarts from one manufacturing setup to another like seasoned pros.
0687	
0688	Forward Deployed Engineer
0689	London
0690	Engineering
0691	
0692	TL;DR
0693	This job is for you if you love variety and real-world problem-solving. No two days will be the same, but you can expect to:
0694	solve hairy engineering problems under pressure; deploying software and hardware on factory floors (Haribo one day, aerospace the next)
0695	own relationships with customers end-to-end, from first conversations to scoping out solutions on the factory floor
0696	pick up and understand unfamiliar manufacturing processes at breakneck speed
0697	work closely with Matta’s AI broader research and engineering team to improve and iterate on our solutions
0698	be the face of Matta, interfacing with prospective customers at trade shows (most often lovely 50-year old technicians called Kevin)
0699	deliver real impact on how we manufacture the world around us
0700	
0701	Forward Deployed Engineer @ Matta
0702	We’re hiring Forward Deployed Engineers to lead the charge on implementing and operationalising our AI solutions in factories. You’ll be the person who makes our tech real for our customers – and makes sure it actually works.
0703	
0704	This is a full-stack role – but not just technically! You’ll work across the entire customer journey, doing the jobs of multiple people and specialties in one: engaging prospective customers, qualifying leads, scoping problems, deploying solutions, and fixing things when they break (and they will break). No two days will be the same!
0705	One week, you’ll be the face of Matta, responsible for engaging with engineers and technicians at trade shows, bringing in leads alongside our CEO, Doug (and keeping him on track!). You’ll leverage your understanding of our customer’s challenges, to qualify and validate their interest in the Matta product. The next, you’ll be deep in a factory, perhaps figuring out why our system is picking up too much static interference, or how to optimise the lighting to improve our images. You’ll roll up your sleeves and get problems sorted – collaborating with our backend, frontend, and research teams to ship fixes and redesign product features based on customer feedback.
0706	
0707	This isn’t a role with a playbook – you’ll shape how Matta scales deployments across the UK, Europe, and the US. And this isn’t your typical gig – expect to work hard and collaborate with an exceptional team of top engineers, scientists, and builders, all obsessed with embodied AI reshaping the manufacturing world.
0708	
0709	About You
0710	A practical problem solver: you can pull on your expertise to solve hairy engineering challenges in real-world environments.
0711	Ideally you don’t just problem solve, but love being customer facing, and can craft world-class customer experiences (the manufacturing sector deserves Apple-esque experiences!).
0712	People person: you’re comfortable being the face of Matta, and want to get to know more Kevins.
0713	You’ve built or deployed projects from start to finish, overcoming hurdles and shipping brilliant products (in startups? even better) and you are a bit batty and want to learn more!
0714	Highly collaborative: you love working in teams, sharing knowledge, mentoring/teaching others, and embracing feedback (and yes, you’re always game for a team Lego-building break).
0715	Ideally (but not essential), you have a Master's in engineering / manufacturing / industrial systems, or may come from a sector specific related background like automotive or aero.
0716	Bonus: you’re open to travel (~10-20% time) to trade shows and customers, to kick start our expansion into Europe and the US.
0717	
0718	Backend Engineer
0719	London
0720	Engineering
0721	
0722	TL;DR
0723	This job is for you if you enjoy:
0724	the ambitious goal of building the data, AI and software infrastructure for the future of manufacturing
0725	working at the crossover of software and hardware (we are truly full stack and often are in factories)
0726	designing efficient architectures to handle large amounts of data and 10,000s of connected machines (working on everything from embedded systems and edge compute, to cloud deployments)
0727	delivering real impact on how we manufacture the world around us
0728	
0729	Backend Engineer @ Matta
0730	We’re looking for a Backend Engineer to help design, build, and scale our manufacturing OS. You’ll work directly on our FastAPI-based backend with the challenging task of designing highly-scalable system architectures to handles 1000s of real-time data streams across 100s of manufacturing processes. What makes this especially challenging is generalising across different use cases and customer environments. We need to be super flexible without compromising on performance and code sanity – from beer bottle factories to aerospace components. You’ll juggle back and forth between: 1) creating API endpoints for our edge devices, 2) improving the efficiency of database queries, 3) integrating new features in our frontend dashboard 4) plus more.
0731	
0732	About You
0733	A backend behemoth: You write clean, scalable, high-performance backend code. You take pride in your craft.
0734	Bonus points for familiarity or mastery with our tech stack: FastAPI and pydantic, postgres, sqlalchemy, etc.
0735	Happy with (or ready to learn about) all the usual add-ons like Redis, Celery, New Relic, Sentry; and deploying to production with good CI/CD/testing/logging practices.
0736	You’ve led projects from start to finish, overcoming hurdles and shipping brilliant products (in startups? even better) and you are a bit batty and want to learn more!
0737	Probably have a master's in engineering / computer science / maths or related field.
0738	Ideally 3+ years of industry experience.
0739	
0740	Frontend Engineer
0741	London
0742	Engineering
0743	
0744	TL;DR
0745	This job is for you if you enjoy:
0746	the crazy challenge of inventing the future UI / UX for manufacturing
0747	working at the crossover of software and hardware (we are truly full stack and often are in factories)
0748	writing performant code that can handle and visualise a ton of data at scale
0749	delivering real impact on how we manufacture the world around us
0750	
0751	Frontend Engineer @ Matta
0752	We’re looking for a Frontend Engineer to own, build, and scale the face of our manufacturing OS. You’ll work directly on our Vue.js-based frontend, with the fun and challenging task of designing interfaces for the future of manufacturing, whilst also making internal tools / demos for showcasing and testing our AI. You’ll juggle back and forth between proper engineering around efficiency of WebRTC and WebSockets, to creating new user experiences and interfaces for AI visualisations and data, and prototyping designs faster than our CTO can make cups of tea for the team (btw the whole team can juggle… so get practicing).
0753	
0754	About You
0755	A proper frontend wizard: You write clean, scalable, high-performance frontend code. Bonus points for Vue.js mastery and its state management.
0756	Ideally you don’t just code but can craft experiences. You are rapid at prototyping in tools like Figma or even sketches and turning ideas into stunning, intuitive designs.
0757	All the usual things like RESTful APIs, WebSockets, WebRTC, and real-time data pipelines plus CI/CD are chill.
0758	You’ve led web projects from start to finish, overcoming hurdles and shipping brilliant products (in startups? even better) and you are a bit batty and want to learn more!
0759	Ideally you have a master's in engineering / computer science / or may come from a design related background.
0760	You probably have 3+ years industry experience.
0761	
0762	Edge Systems Engineer
0763	London
0764	Engineering
0765	
0766	TL;DR
0767	In this role, you’ll help us:
0768	build the framework that lets us unlock even more powerful AI capabilities
0769	speed up deployment time on site, leading to less factory downtime and disruption
0770	enable customers to self-serve our solutions (we are super excited about this!)
0771	eliminate potential issues and errors before they happen
0772	deliver bullet-proof OTA updates to enable our best features to roll out seamlessly
0773	
0774	Edge Systems Engineer @ Matta
0775	We’re hiring a Factory Systems Engineer to turn that capability into a rock-solid, shippable product: an industrial “Matta Box” that ingests high-bandwidth video, processes it locally, and syncs with the cloud. You’ll design, build, optimise and productise our edge compute and machine vision pipeline and hardware, keeping thousands of deployed units patched and humming along.
0776	
0777	One week, you might be figuring out how to best mount our cameras in the majority of factories; the next, you’re optimising the frame acquisition code running on our Matta boxes. We’d love for you to live and breathe productising and optimising the Matta solution that gets deployed to customer sites – everything from packaging to lighting, mounting, cameras, boxes, and the code that ties it all together.
0778	
0779	About You
0780	A multi-disciplinary solutions / embedded systems engineer (you likely don’t fit into any one box), with a strong grasp of both hardware (Raspberry Pi / Nvidia Jetson / Camera Optics are bonuses) and software (Linux, Gstreamer, Mender, Over-the-air updates)
0781	You’ve done this before. We’re looking for someone who’s designed end-to-end solutions from scratch, navigated plenty of hurdles, and shipped brilliant products (in startups? even better)
0782	A practical problem-solver: things won’t work! Your success will hinge on how well you manage unpredictability and moving parts – both on the customer side and within the evolving development of our AI models
0783	You’ve got a Master’s or PhD in Integrated Systems (or similar), or solid experience building embedded solutions
0784	Bonus extras: machine-vision experience - illumination, optics, sensors, exposure tuning. PoE camera networks or similar high-throughput, low-latency wiring schemes. OTA/CI-CD experience (Mender, Azure Device Update, or AWS IoT Jobs). Gnarly Linux package understanding and at home in horrendous Makefile compilations.


═══════════════════════════════════════════════════════════════
END FILE: Matta_Intel_cleaned_numbered.md
═══════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════
FILE: MATTA_MASTER_PRD_v2.md
PURPOSE: The v0 Refinery PRD. The Hybrid supersedes this for execution but inherits its locked invariants (deterministic two-route ADC, N=3 deep ensemble, Pydantic extra='forbid', Vertex AI europe-west4 pin).
═══════════════════════════════════════════════════════════════

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

**1.2 Vertical classification (Gemini 3 Flash, N=3 ensemble, `thinking_level="minimal"`).** Three parallel Flash calls (model id `gemini-3-flash-preview`, the current cost-optimized Vertex AI model — pricing $0.50/M input, $3.00/M output per [Google Cloud pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)) with temperature variance (0.1, 0.5, 0.9) classify the prospect into one of six manufacturing verticals (polymer extrusion, metal casting, additive manufacturing, F&B bottling, electronics assembly, aerospace) plus an `out_of_vertical` category for prospects outside Matta's verified deployment surface. Plurality voting; on disagreement, the prospect is tagged `vertical_uncertain` and Stage 2 (if requested later) is gated on human review of the vertical assignment.

**1.3 Deterministic fitness scoring.** A hardcoded scoring function combines (a) vertical match against Matta's verified deployment patterns, (b) factory size band against Matta's existing customer footprint, (c) trade-show provenance signal (a William Cook lead from UK Metals Expo carries higher prior than a cold web inquiry), (d) capacity-aware decay (prospects added to a saturated pipeline this quarter score lower than prospects added to a slot still open). The scoring function is fully deterministic Python — no LLM in the scoring decision. The LLM contribution is restricted to the categorical vertical classification in step 1.2.

**1.4 Queue assembly.** Sorted output written to `prioritized_queues` Postgres table with batch_id reference. Slack notification fires to the configured channel: "Batch X scored: 124 prospects, top 12 surfaced for FDE review." The dashboard reflects the new queue in real time via WebSocket.

### 4.4 Stage 2 — Dossier Generation Pipeline

Per-prospect, executed on-demand:

**2.1 Process taxonomy section (Gemini 3.1 Pro, N=1, `thinking_level="medium"`).** Inputs: prospect entity, vertical assignment, public enrichment payload. Model id `gemini-3.1-pro-preview` (the current flagship reasoning model on Vertex AI as of May 2026 — pricing $2.00/M input ≤200K context, $12.00/M output). Output: structured `ProcessTaxonomy` schema describing the prospect's likely production processes at line-level granularity. Vertex AI structured-output mode enforces schema conformance. The Pro model is appropriate here because the output requires synthesis across the enrichment payload and the manufacturing-vertical knowledge graph.

**2.2 Defect-class hypothesis (Gemini 3 Flash, N=3 ensemble + conformal calibration; `thinking_level="minimal"`, temps 0.1 / 0.5 / 0.9).** Inputs: process taxonomy + vertical + manufacturing-vertical knowledge graph. `thinking_level="minimal"` is mandatory here — Gemini 3's default reasoning trace collapses the three samples toward a single mode and destroys the deep-ensembles signal that the Brion Filter depends on; minimal-thinking + wider temperature spread restores the sample diversity the Lakshminarayanan-Pritzel-Blundell methodology requires. Three parallel Flash calls each return a categorical distribution over defect classes for the inferred process type. Conformal calibration (computed offline against a labeled holdout set of past Matta deployments per the dossier) produces a coverage-calibrated *set* of likely defect classes. The dossier surfaces the conformal set with an explicit coverage statement: *"With 80% coverage, the dominant defect classes for this prospect are in: {porosity, dimensional drift, surface inclusions}."* Empty or all-class sets trigger `requires_human_review = True`.

**2.3 Comparable Matta deployment section (Gemini 3.1 Pro, N=1, `thinking_level="low"`, knowledge-graph-anchored).** Inputs: process taxonomy + vertical + the citation-anchored knowledge graph. Output: a `ComparableDeployment` schema citing one or two verified Matta deployments with explicit dimension-of-comparability annotation (e.g., *"B&W speaker components — comparable on the surface-finish QC stage, NOT on overall process category, NOT on production volume"*). The knowledge graph forbids citing entities without primary-source line provenance (Section 6.5). If no comparable exists in the verified deployment surface, the section is marked `no_comparable_available` and the dossier proceeds without fabricating one.

**2.4 Integration risk register (Gemini 3.1 Pro, N=1, `thinking_level="low"`).** Inputs: enrichment payload + process taxonomy + a hardcoded risk taxonomy (legacy CMM, lighting variance, EMF environment, network topology, OT/IT segmentation). Output: a `RiskRegister` schema with per-risk findings. Each risk is graded against a fixed three-tier scale (`identified`, `unknown`, `not_applicable`); the LLM does not invent risk categories outside the hardcoded taxonomy.

**2.5 Suggested approach (Gemini 3.1 Pro, N=1, `thinking_level="low"`).** Inputs: all preceding sections + a hardcoded "approach template" library (2-camera pilot, 4-camera pilot, full-line deployment, Caracol-AM-style OEM partnership). Output: a `SuggestedApproach` schema constraining recommendations to the template library — the LLM does not invent novel deployment patterns.

**2.6 Dossier assembly.** All five section schemas validated against `extra="forbid"` Pydantic models, then composed into a final `PreVisitDossier` envelope and persisted to Postgres `dossiers` table. WebSocket pushes the artifact to the document preview pane in real time as sections complete.

### 4.5 Gemini Model Routing Rationale

| Stage | Model | Reason |
|---|---|---|
| Vertical classification (1.2) | Gemini 3 Flash, N=3 (`thinking_level="minimal"`, temps 0.1 / 0.5 / 0.9) | Categorical task at high batch volume. `gemini-3-flash-preview` is the current cost-optimized Vertex AI model (replaces deprecated 2.5 Flash); N=3 provides the deep-ensembles uncertainty signal without blowing batch latency. Pricing $0.50/M input, $3.00/M output. |
| Process taxonomy (2.1) | Gemini 3.1 Pro, N=1, `thinking_level="medium"` | Synthesis across enrichment + knowledge graph. `gemini-3.1-pro-preview` is the current flagship reasoning model on Vertex AI (replaces 2.5 Pro); `thinking_level="medium"` gives the synthesis depth this section needs without runaway thinking-token cost. Pricing $2.00/M input ≤200K, $12.00/M output. |
| Defect-class hypothesis (2.2) | Gemini 3 Flash, N=3 (`thinking_level="minimal"`, temps 0.1 / 0.5 / 0.9) + conformal | Categorical task where uncertainty surfacing is the load-bearing output. `thinking_level="minimal"` preserves ensemble diversity (reasoning-mode would mode-collapse the samples). Mirrors Doug's published methodology directly. |
| Comparable deployment (2.3), Risk register (2.4), Suggested approach (2.5) | Gemini 3.1 Pro, N=1, `thinking_level="low"` | Each requires synthesis under hard schema constraints; Pro's instruction-following discipline is appropriate. `thinking_level="low"` is sufficient because the action space is constrained by the knowledge graph / risk taxonomy / approach template library — the model is filling structured fields, not reasoning open-ended. |
| All inference | Vertex AI europe-west4 via `google-genai` (`genai.Client(vertexai=True, location="europe-west4")`) | Investor mandate (Giant Ventures EU sovereignty) + GDPR data localization. Legacy `vertexai.generative_models` removed 2026-06-24, so the Refinery ships against `google-genai` from day one. |

**Preview-variant note (Damjan readiness).** Both Gemini 3 models above are currently exposed in `europe-west4` under their preview suffixes — `gemini-3-flash-preview` and `gemini-3.1-pro-preview` — per the Vertex AI region-availability documentation ([locations doc](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations), europe-west4 / Netherlands table, retrieved 2026-05-10). Preview models are subject to deprecation or behavior change on Google's schedule. The Refinery's demo recording and reference-architecture handoff timeline (72-hour sprint plus ~2-week client handoff) is well inside typical Vertex AI preview-model stability windows. Production deployment by the client should re-pin both model strings to whichever variants (preview, GA, or successor SKU) are current at production-build time; the `model` parameter is the only line of code that changes, since the `google-genai` SDK call signature, the structured-output `response_schema` contract, the `thinking_config` parameter, and the `europe-west4` region pin are all stable surfaces. The global endpoint is explicitly NOT used — per the same locations doc, *"Don't use the global endpoint if you have ML processing requirements, because you can't control or know which region your ML processing requests are sent to"* — so the Giant Ventures EU data-residency mandate is preserved regardless of which preview-or-GA variant is in production.

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
- The Google Gen AI SDK call inside the worker is `client = genai.Client(vertexai=True, project=settings.gcp_project, location="europe-west4")` followed by `client.models.generate_content(model="gemini-3-flash-preview", contents=[...], config=GenerateContentConfig(response_mime_type="application/json", response_schema=RootCauseHypothesis, thinking_config=ThinkingConfig(thinking_level="minimal"), temperature=t))`. The deprecated `vertexai.generative_models.GenerativeModel` API is not imported anywhere.

### 6.4 Vertex AI Prompt Templates

Each prompt template enforces strict JSON output via the Google Gen AI SDK structured-output mode bound to the relevant Pydantic schema (see [Vertex AI structured output docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/maas/capabilities/structured-output)). Output is re-validated against the Pydantic schema as defense-in-depth.

Canonical call pattern (used at every stage):

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


═══════════════════════════════════════════════════════════════
END FILE: MATTA_MASTER_PRD_v2.md
═══════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════
FILE: Matta_positioning_final_v2.md
PURPOSE: 1F-red v2 verdict that killed the Brief architecture and selected Form C (the v0 Refinery). Defines what is OFF the table for this audit.
═══════════════════════════════════════════════════════════════

# Matta Brief Architecture — 1F-red Verdict (v2)

## Verdict

**REPOSITION-REQUIRED.**

The pre-sales scoping bottleneck **category** survives the audit substantively — and survives more strongly than the prior 1F-red captured, once Gemini's missed primary-source evidence is restored. The Brief's architectural **form** (stateless, mobile, in-the-moment, 60-second-at-the-booth, lead-capture-flavored) does not survive. The reshape to a stateful, asynchronous, desktop-anchored, deep-research-flavored, pipeline-prioritization-aware sidecar is required.

The recommended form is **Form C — The Refinery**, a stateful sidecar with two output modes that operate over a shared underlying pipeline: (Stage 1) deployment-capacity-aware prioritization queue ingesting trade-show lead lists and waitlist signals, and (Stage 2) on-demand pre-visit dossier generation for the FDE-bound subset. Stage 2 is the demoed Magic Moment; Stage 1 is the verbal tail tease. Justification for selecting C over A or B is in the Form Selection section.

The orchestration spine from `ULTIMATE_PRD.md` continues to transfer at approximately 70%. The schemas, ADC routing rules, demo theater, and knowledge graph all change. The N=3 deep ensemble, conformal prediction set, parallel verifier, durable outbox, Pydantic `extra="forbid"` posture, and Vertex AI europe-west4 pinning carry forward unchanged.

## Verification Findings

Direct verification of the load-bearing quote claims, run against `Matta_Intel_cleaned.md` line-by-line. Gemini's audit had three significant primary-source misses that materially affect the verdict mechanics, though not the directional conclusion.

**Multi-year waitlist quote (load-bearing).** Verified verbatim. Lines 114 and 267, both from Doug's $14M funding announcement post (10/12/25 and 11/12/25 — same post, dual indexing in the substrate): *"we're deploying to around two factories a month and have a multi-year waitlist at the moment – so do reach out and let's see how we can dramatically improve your processes with industrial AI."* Gemini cited this correctly. The quote is the strongest single anchor in the audit and survives the verification pass intact.

**"100s of factories in the pipeline" quote.** Verified verbatim, but misframed by Gemini. Lines 106 and 248. The quote IS Doug's, but it appears in a hiring post (Forward Deployed Engineer JD), not a sales-pipeline post. The next sentence is *"if you are exceptional… we will take you."* The substantive conclusion (massive pipeline volume) holds independently from the multi-year-waitlist quote, so the misframing does not cascade. Note for SOP: Gemini's citation hygiene was sloppy here. Flag.

**Advanced Engineering 2025 trade-show post.** Verified verbatim. Line 284: *"What a start to Advanced Engineering 2025! ⚙️🔥 Day one was a blast - we met over 100 incredible leads from across the manufacturing world… Here's a peek at the action at Booth P198."* Tagged: Doug, Daniel Crimp, Sebastian Pattinson, Bonnie Zhang, Jake Moll, Tom Walker, Ollie Rosen, Damjan Denic, Christos Margadji, Matthew Judge — ten team members including both founders and the CTO. **This is a primary-source miss by Gemini.** Gemini's Claim 1 audit explicitly searched for "MACH 2026" and "Southern Manufacturing" and concluded *"complete absence of empirical evidence supporting the trade-show hypothesis."* The substrate contradicts that conclusion at line 284 (Advanced Engineering 2025), line 187/191 (MACH 2026 — *"come find us on the Matta stand (17-121)… industrial AI chat with Damjan Denic, Carmelo del Coso Ameijide, and Douglas Brion"*), line 234/393 (Southern Manufacturing & Electronics 2026 — *"It also marks one year since our very first trade show (Southern last year)"*), and line 294 (UK Metals Expo Sept 2025 — *"We clocked 124 leads in two days, putting us in the top 5% of exhibitors"*). Four trade shows in twelve months. Doug and Damjan personally attend MACH 2026. Trade shows are not the absent vector Gemini described — they are a verified, founder-attributed, twelve-month-old, named-customer-disclosing acquisition channel.

**Cummins as "hallucinated entity" claim.** Partially refuted. Lines 200, 210, 212–214, 321, 331, 338–340, 345 — Cummins Inc. (specifically Steven Grace, Automation & Technology Leader, and Jonathan Wood, VP-CTO, Cummins Europe) attended the Matta-hosted "Sentient Factories" event at the Royal Academy of Engineering. Steven Grace was on the Matta-organized panel. Cummins is in Matta's verified relationship/event graph. **However**, Cummins is not in the verified deployment footprint — the verbatim deployment list is Bowers & Wilkins, Caracol AM, polymer manufacturing (unnamed customer), metal casting, bottling (the "global drinks brand"), consumer electronics. Gemini's specific framing ("Cummins is hallucinated") is wrong; Gemini's structural concern (using Cummins as a "comparable Matta deployment" anchor in the knowledge graph is not deployment-evidence-grounded) is correct. The implication for the demo: using "Cummins" or a Cummins-adjacent entity as a demo-target name is grounded and safe (Doug knows Cummins, hosted Cummins, has a relationship). Using Cummins as a "comparable deployment pattern" anchor in the dossier output is not safe.

**"Global drinks brand" quote.** Verified verbatim. Lines 540 and 600, both from Matta funding press materials: *"Recent projects range from inspecting high-speed bottling for defects with a global drinks brand to working with Bowers & Wilkins, where Matta's AI rapidly measures speaker components to catch issues before assembly."* **This is a second primary-source miss by Gemini.** The audit flagged this as "Not Verified (Implicit)" — incorrect. The exact phrase is in the substrate.

**FDE JD trade-show responsibilities.** Verified verbatim. Lines 698, 704, 705, 716. The FDE role JD names trade-show responsibilities four times: *"be the face of Matta, interfacing with prospective customers at trade shows"* (698), *"engaging prospective customers, qualifying leads, scoping problems"* (704), *"One week, you'll be the face of Matta, responsible for engaging with engineers and technicians at trade shows, bringing in leads alongside our CEO, Doug (and keeping him on track!). You'll leverage your understanding of our customer's challenges, to qualify and validate their interest in the Matta product."* (705), *"travel (~10-20% time) to trade shows and customers"* (716). **Gemini's audit did not surface any of this.** The Brief_Audit.md focuses entirely on the Special Projects/Chief of Staff JD and never quotes the FDE JD on trade-show or lead-qualification language. This is the third primary-source miss.

**Sebastian's uncertainty-quantification rigor.** Verified. Doug's Cambridge thesis pedigree, Sebastian's Nature Communications 2022 paper on closed-loop neural-network correction, and the substrate's references to "nuclear submarines, waterproof coats and even gourmet cheese" deployment surface confirm the regulated-environment risk-aversion claim. Gemini's Claim 2 use of this evidence holds.

**Special Projects/Chief of Staff Gandalf framing.** Verified verbatim. Line 262 (Doug's Chief of Staff hiring post): *"Think Gandalf: the person who quietly works their magic behind the scenes, making sure everything runs smoothly."* Plus line 625 (Special Projects JD): *"steering long-term strategy, supporting fundraising efforts, and helping close customer deals… probably our most important hire."* Gemini's Claim 4 use of this evidence holds. (Note: the role appears to have been posted as both "Chief of Staff" and "Special Projects" — same role, two titles. Either label is supportable in outreach.)

**Net.** Gemini's directional verdict (escalate, reshape required) is correct. Gemini's audit methodology has three primary-source misses (trade-show evidence, "global drinks brand" verbatim, Cummins-in-relationship-graph) that would have softened the Claim 1 and Claim 3 framings substantially. None of those misses recover the original Brief shape, because the form-axis problems (stateless vs stateful, mobile vs desktop, in-the-moment vs asynchronous, lookup vs deep research) are independently load-bearing and survive the corrections.

## Justification

The category-vs-form distinction holds, and it holds harder than the original 1F-red captured.

The category — pre-sales scoping consuming founder, FDE, and Special Projects/Chief-of-Staff hours — is supported by four independent verbatim sources: the multi-year-waitlist quote (Doug, funding post), the FDE JD trade-show language (four separate verbatim references), the Chief of Staff "Gandalf" JD (Doug, hiring post), and the trade-show post-event summaries (124 leads at UK Metals Expo, 100+ at Advanced Engineering 2025, full team tagged at MACH 2026 and Southern Manufacturing 2026). Pre-sales scoping is real, current, founder-attributed, and quantifiable. The category survives the audit by a wide margin.

The form fails because four independent form-axes all collapse under primary-source pressure. (1) Stateful vs stateless: a multi-year waitlist with two-deployments-per-month capacity is by construction a stateful pipeline problem; the prospects sit in queue for months or years before deployment. A stateless sidecar that resets after every interaction cannot model that pipeline. (2) Asynchronous vs in-the-moment: the FDE workflow is "trade show one week, factory deployment the next." The bottleneck sits BETWEEN those two weeks — in the post-show triage and pre-visit prep windows — not in the booth conversation itself. (3) Desktop vs mobile: 124 leads from UK Metals Expo are processed via CSV/Hubspot/Salesforce on a desktop, not via Slack-on-phone at the booth. (4) Deep research vs lookup: Sebastian's verbatim uncertainty-quantification rigor and Doug's nuclear-submarine/aerospace-deployment surface are incompatible with collapsing technical scoping to 60 seconds. All four form-axes point in the same direction; the booth-anchored framing is wrong on every one.

The 1F-sim simulation against Damjan fires cleanly. Damjan reads the cold email at minute 0, sees "60-second pre-call brief, for Hannover and beyond," and within five minutes notes the architectural mismatch: the vendor is optimizing speed at the top of the funnel for a company whose actual constraint is downstream — *which 6 of the 100 leads from last week's show, and which 24 of the 400+ in the multi-year waitlist, do we move into deployment slots this quarter*. He archives. Gemini's implicit 1F-sim signal — *"Matta is actively managing an overwhelming asynchronous pipeline, deploying highly complex physical AI infrastructure into strictly regulated environments"* — fires as a contradiction in his read because the substrate genuinely supports it. This is not Damjan being uncharitable; this is the architecture proposing the wrong end of the pipeline.

## Form Selection

**Form C — The Refinery.** A stateful, asynchronous, desktop-anchored sidecar with two output modes operating over a shared underlying pipeline: Stage 1 (deployment-capacity-aware prioritization queue) and Stage 2 (on-demand pre-visit dossier per FDE-bound deployment). Stage 2 is the demoed Magic Moment in the Vidyard. Stage 1 is the verbal tail tease.

Form A (Pipeline Triage Sidecar in isolation) and Form B (Pre-Deployment Dossier Sidecar in isolation) each fit the verified operational reality, but each has a thin failure mode that Form C resolves. Form A's risk is the strategic-decision ego check: a sidecar that ranks Matta's deployment queue can be perceived as overreaching into territory Doug and Damjan reserve for their own judgment (Caracol OEM partnership status, B&W reference-customer continuity, capacity scheduling against existing FDE travel calendars). Damjan's likely challenge: "We have a Notion doc for this, what does your sidecar know that we don't." Form A survives that challenge but with a thin margin. Form B's risk is the build-vs-buy commodification challenge: deep-research artifact generation is a contested vendor category (Clay, Crystal, ZoomInfo Engage, GPT-Researcher startups) and a bespoke sidecar built around six manufacturing verticals × five defect classes is structurally small enough that Damjan's team could plausibly assemble equivalent capability in a sprint. Damjan's likely challenge: "Why not Clay plus a Cursor agent." Form B survives that challenge but more thinly than Form A.

Form C addresses both weaknesses by combining them. Stage 1 supplies a deployment-capacity-aware prioritization signal that pure data-enrichment vendors cannot produce (Clay does not know Matta's deployment cadence or current FDE travel roster). Stage 2 inherits Stage 1's prioritization signal as input, which means the dossier-generation step is operating on a triaged subset rather than spraying enrichment across the whole pipeline. Stage 1 retains its strategic-decision-respect posture by surfacing CANDIDATES with structured rationale, not making decisions — the FDE team controls which dossiers to actually generate. The two stages share the same orchestration spine (ADC routing, N=3 ensemble, conformal calibration, Pydantic envelopes, durable outbox), so Form C is structurally one product with two output modes, not two products jammed together. Build cost is roughly Form B's cost plus a small Stage-1 prioritization layer, well within the 72-hour sprint envelope given the orchestration spine reuse.

The chosen demo theater (Stage 2) is the more visceral output. Showing a ranked list (Stage 1) is harder to make visually magic in 60 seconds than showing a deep dossier materializing on screen. The verbal tail tease at video end ("there's an upstream prioritization layer that ingests your raw trade-show CSVs and produces the queue feeding into this") is structurally identical to the prior version's Phase 2 tail tease and uses the verbal-only adjacent-idea mechanic from the Identity manifesto.

## Positioning Edits

### FDE Thesis

The Refinery is a stateful pre-deployment intelligence sidecar that absorbs the post-trade-show, pre-FDE-deployment scoping load currently distributed across Doug, the FDE team, and the incoming Special Projects/Chief of Staff hire. It ingests trade-show lead lists (CSV/Hubspot/Salesforce export) and inbound waitlist signals, produces a continuously evolving prioritization queue against Matta's two-deployments-per-month capacity, and on-demand generates pre-visit dossiers for the leads that promote into FDE deployment slots. It operates strictly upstream of any factory deployment — it never reads from a Matta camera, agent, foundation model, factory OS surface, or edge firmware. It exists between the trade-show floor and the factory visit, not at either endpoint.

### Magic Moment

The FDE clicks "generate dossier" on the top-ranked candidate from their prioritization queue (e.g., a forging plant from UK Metals Expo, or a polymer line from Advanced Engineering). Sixty to ninety seconds later, a structured eight-page artifact materializes on their desktop: process taxonomy, likely defect classes with conformal sets, comparable Matta deployment patterns drawn from the verified deployment surface (B&W speaker components for precision-machining contexts, Caracol AM for additive contexts, polymer manufacturing for extrusion contexts, bottling for high-speed F&B contexts), integration risk register (legacy CMM infrastructure, lighting variance, network topology, EMF environment), suggested approach. The visceral demo is artifact depth — the document the FDE reads on the flight to the factory the next morning. Explicitly NOT "60 seconds at the booth." The Magic Moment is depth and structure, not speed.

### Sebastian Readiness Check

> The Refinery operates entirely upstream of any factory deployment — it consumes public corporate data, your verified deployment patterns from your published case studies, and the trade-show lead intake your team already collects, then produces formatted intelligence for your FDEs to read before a factory visit. The architecture has zero shared signal path with the closed-loop control work disclosed in your 2022 Nature Communications paper; The Refinery never reads from a Matta camera, an agent emission, or a foundation-model output. Its conformal calibration on defect-class hypotheses respects the uncertainty-quantification posture you've publicly insisted on — when the model is unsure, the dossier says so explicitly rather than hallucinating a confident defect taxonomy.

### Damjan Readiness Check

> You absolutely could build this in-house — a senior FDE plus an MLE plus a manufacturing-vertical knowledge graph plus the prioritization scoring layer plus the deep-research orchestration, call it three to four months and ongoing maintenance for the knowledge graph and scoring rules. We've already built it; you'd have it running against a CSV export from Hubspot or a Salesforce webhook in under two weeks, with the orchestration patterns documented as a reference architecture your team can absorb when the bandwidth fits. The £10k/month is structured against the deployment-slot cost — your two-a-month cadence makes each deployment slot worth a meaningful slice of ARR, and a Refinery-improved deployment-target selection that earns a single Cummins-class commitment pays the year.

### Demo theater (left pane / center pane / right pane)

**Left pane:** Replaced. Booth simulation is dropped. The new left pane is a desktop screen showing a trade-show lead intake — a CSV preview of `UK_Metals_Expo_2025_leads.csv` with 124 rows, file dropped into the Refinery dashboard. Stylized Hubspot-style UI overlay. (Production cost: lower than the trade-show booth simulation; uses Tailwind on a stock SaaS layout.)

**Center pane:** Architecturally identical to the prior version. The pipeline visualization (ingress → ADC → N=3 ensemble → conformal calibration → parallel verifier → narrative generation → outbox → ack) is the same. Schemas and demo data change. The center pane shows two routing paths in the ADC — one for prioritization requests (Stage 1), one for dossier requests (Stage 2). The demo run exercises Stage 2 with a single dossier generation; Stage 1's queue is visible as static data in the left pane to anchor the workflow context.

**Right pane:** Replaced. The Slack mobile mock is dropped. The new right pane is a Notion-style or PDF-preview document panel showing the dossier materializing section by section — process taxonomy first, then defect-class hypothesis with conformal interval, then comparable-deployment section, then integration risk register, then suggested approach. Cost ticker bottom-right, ticks under ten cents per dossier. (Production cost: roughly the same as the Slack mobile mock; standard React/Tailwind document component.)

If a secondary screen is needed for the verbal tail tease at video end, use a 3-second freeze-frame of the prioritization queue from Stage 1 — sourced as the Refinery's own UI mock, not invented external collateral. Visual reference only, not a working demo. Keeps the Stage 1 option open without committing the build.

### Why-video script (~95 seconds)

```
[0:00–0:08]  COLD OPEN — silent. Desktop screen.
             CSV file "UK_Metals_Expo_2025_leads.csv"
             with 124 rows visible. Cursor drags the
             file into the Refinery dashboard.

[0:08–0:18]  SILENT — Refinery's prioritization queue
             materializes. 124 raw leads → ranked list
             with fit scores against Matta's two-a-month
             deployment cadence. Top candidate visible:
             a forging plant from UK Metals Expo.
             FDE clicks "generate dossier."

[0:18–0:35]  DOSSIER MATERIALIZES — document scrolls on
             screen section by section. Process taxonomy.
             Likely defect classes (porosity, dimensional
             drift, surface inclusions) with conformal
             sets. Comparable Matta deployment: polymer
             extrusion case study. Integration risk:
             legacy CMM, lighting variance. Suggested
             approach.

[0:35–0:55]  VOICEOVER (Hafeedh) — "What you just watched
             is The Refinery — a stateful sidecar that
             takes the lead lists you collect at trade
             shows and the inbound signals from your
             waitlist, scores them against your two-a-month
             deployment capacity, and on-demand generates
             pre-visit dossiers for the leads that promote
             into FDE deployment slots. Stateful.
             Asynchronous. Desktop-anchored. Built around
             your actual deployment cadence."

[0:55–1:15]  TECHNICAL WALKTHROUGH — three-pane theater.
             Show the deterministic Action Domain
             Classifier routing prioritization vs dossier
             requests. Show the N=3 Gemini Pro ensemble
             running with conformal calibration on the
             defect-class hypothesis. Show the Pydantic
             schema validation. Cost ticker — under ten
             cents per dossier.

[1:15–1:30]  THE FDE JD CITATION — "Your FDE JD names
             trade-show qualification, lead validation,
             and pre-deployment scoping in the
             responsibilities. The Refinery absorbs the
             slice of that load that today happens between
             the show floor and the factory visit."

[1:30–1:35]  TAIL TEASE (verbal only) — "There's an
             upstream prioritization layer that ingests
             your raw trade-show CSVs and produces the
             queue feeding into the dossier generator.
             Happy to walk that through on a call."

[1:35]       SIGN-OFF.
```

### Cold email — Subject line

`The Refinery: pre-visit dossier sidecar, for Matta's deployment cadence`

### Cold email — Doug's tagged line

> Doug — your team has been on the trade-show calendar all year (UK Metals Expo, Advanced Engineering 2025, MACH 2026, Southern Manufacturing 2026), and the FDE JD makes pre-deployment scoping and lead qualification an explicit part of the role. We built a thing that turns a trade-show lead list — say the 124 you brought back from UK Metals Expo — into a triaged queue against your two-a-month deployment capacity, and generates a deep pre-visit dossier on the leads your team promotes. Built for the work that happens between the show floor and the factory visit, not at either endpoint.

### Cold email — Damjan's tagged line

> Damjan — stateful sidecar, FastAPI ingress, Pydantic everywhere with `extra="forbid"`, deterministic rules engine for the routing decision (no LLM in the load-bearing path), N=3 Gemini Pro ensemble with conformal prediction sets for the defect-class inference, durable outbox so a queued dossier ships even when an FDE drops connectivity in transit. CSV in, structured artifact out. Reference architecture you can read; absorbable in-house when the bandwidth fits.

### Cold email — CTA

> 95-second video at the link — skip to 0:18 if you want the magic moment first, technical walkthrough follows. If the architecture lands, 15 minutes to scope. If not, no follow-up from me.

## Phase 1 Build Implications

### Schema changes (PHASE_1_SPEC.md needs revision)

`MattaDefectEvent` is replaced by `LeadIntakeBatch` (CSV ingest envelope: lead rows with company name, contact, sector hints, trade-show provenance) and `LeadProspect` (per-lead enriched envelope post-Stage-1 scoring). `RootCauseHypothesis` becomes `LikelyDefectClassHypothesis` with the same structural shape (categorical enum, conformal set, confidence band) but a different domain (defect classes for the inferred manufacturing process type). `CMMSWorkOrder` is replaced by `PreVisitDossier` — a structured Pydantic envelope with sections for process taxonomy, defect-class hypothesis, comparable Matta deployment patterns (drawn ONLY from verified deployment surface — Bowers & Wilkins, Caracol AM, polymer manufacturing, metal casting, bottling, consumer electronics; never relationship-edge entities like Cummins), integration risk register, suggested approach.

### Action Domain Classifier rules

Rewritten for two-route discrimination. Route 1: prioritization request (input is `LeadIntakeBatch`, output is `PrioritizedQueue`). Route 2: dossier request (input is a single `LeadProspect`, output is a single `PreVisitDossier`). The deterministic mapping is `(request_type, payload_shape, vertical_keyword) → route_path`. Default route on no-match: `requires_human_review = True`, queued for manual triage.

### Knowledge graph

The six-vertical macro-structure (polymer extrusion, metal casting, additive manufacturing, F&B bottling, electronics assembly, aerospace) holds. Per Gemini's Claim 3 verdict (which holds even after my methodology corrections), the load-bearing entity-level anchors must be cleaned up. Specifically: `Cummins` is removed from any "comparable deployment" anchor (it's a relationship-graph entity, not a deployment-graph entity); the demo-target name of "Cummins Daventry plant" can be retained for the Why-Video because Doug knows Cummins via the RAE event. `global drinks brand` is retained as a deployment-pattern anchor for the F&B bottling vertical because it IS verbatim in the funding press materials. `aerospace composites` is replaced with a broader `aerospace` vertical anchor that includes plane wings, titanium alloys, and metallurgy contexts to avoid the rigid-ontology vulnerability Gemini flagged. The knowledge graph file remains a small hand-built JSON (six verticals, five defect classes each, with citation provenance for each anchor pointing back to a verbatim line in `Matta_Intel_cleaned.md`); approximately eight hours of curation work, two hours longer than the prior version because the citation-provenance pass is now mandatory.

### Demo theater

Per the Demo Theater section above. Left-pane and right-pane mocks are both replaced. Center pane is structurally identical. Production cost is roughly equivalent to the prior version (lower-cost SaaS UI mocks replace a stock-footage-trade-show mock and a Slack-mobile mock).

### Architecture preserved (no changes needed)

The N=3 Gemini ensemble pattern, the conformal prediction set computation, the parallel Stage 2.5 verifier fan-out, the Pydantic `extra="forbid"` posture, the Vertex AI europe-west4 pinning, the deterministic-routing-over-LLM-routing principle, the deep-ensembles voiceover disclaimer, the Damjan idempotency primitives — all transfer unchanged.

### Sprint impact

72-hour sprint envelope holds. Schema rewrite, demo theater change, knowledge-graph citation-provenance pass, and Stage 1 prioritization scoring layer net to roughly the same total work as the original Brief schema change, given that the orchestration spine ports across cleanly. The Vidyard recording flow is unchanged in structure (cold open, technical walkthrough, verbal tail tease) — only the on-screen content changes. Cold-email subject and tagged lines redrafted; structural shape unchanged.

### Outreach delivery sequencing

Cold email CTA links to a Vidyard timestamped to the Magic Moment (0:18). Verbal Phase 2 tease at 1:30 references the upstream prioritization layer (Stage 1). If Doug or Damjan asks about it on the discovery call, Stage 1 is ready to scope as a Phase 2 engagement after Stage 2 proves itself. The dormant CMMS Bridge architecture remains a deeper Phase 3 verbal-only adjacent idea if a third call materializes.

## Meta-Observation for Hafeedh

This is the second mid-sprint architectural-form falsification on Matta inside the same sprint cycle. The pattern across CMMS Bridge → Brief → Refinery is consistent: the FORM-axis problems (stateful vs stateless, mobile vs desktop, in-the-moment vs asynchronous, lookup vs deep research) survived the Step 1A → 1B Master PRD writing process and only died at the 1F or 1F-lite audit gate. Both architectures had verbatim primary-source contradictions of their form-axes already present in the cleaned intel substrate at the time the Master PRD was written. This suggests the four form-axes are a candidate for promotion to the Step 1D divergent-generation gate as an explicit per-axis primary-source justification check, BEFORE the Master PRD is committed. Each of the four binary axes would require a verbatim citation defending the proposed direction. On the Brief, that pre-1B check would have caught the form mismatch before resources were spent on the 1B PRD and the orchestration spine schema work. Secondary observation, smaller weight: Gemini's audit methodology has a consistent retrieval gap (verbatim-present-in-substrate evidence not surfaced — three misses on this audit, one on the prior CMMS Bridge audit). 1F/1F-lite gates may benefit from requiring per-claim line-citations rather than summary verdicts, which would make Gemini's retrieval gaps visible to the audit consumer rather than requiring the consumer to re-derive primary sources. Both observations are SOP-iteration questions, not part of the v2 positioning artifact. Carrying them into the strategy thread for sprint-meta discussion separately.

---

*End of Matta_positioning_final_v2.md. Audit trail preserved: Matta_positioning_final.md (the prior CMMS Bridge kill verdict and Brief proposal) is unchanged.*


═══════════════════════════════════════════════════════════════
END FILE: Matta_positioning_final_v2.md
═══════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════
FILE: Matta_positioning_final.md
PURPOSE: 1F-red v1 verdict that killed the CMMS Bridge architecture. Audit trail only.
═══════════════════════════════════════════════════════════════

# Matta CMMS Bridge — 1F-red Verdict

## Verdict

**KILL-AND-RESTART**

The CMMS Bridge architecture has now had two distinct foundational premises falsified against Matta's primary-source ground truth: the original "current FDE CMMS burden" premise (killed by Gemini's 1F audit), and Gemini's proposed replacement "future IT compliance threat" premise (killed by this 1F-red adjudication). The architecture itself is technically clean and IP-defensible, but it has no surviving commercial premise that Matta's own public substrate supports. A structurally stronger architecture — addressing a current, JD-attributed, founder-confirmed pain — exists and should replace it.

The replacement architecture is **The Brief**: a stateless pre-deployment factory scoping sidecar that absorbs the trade-show lead-qualification and pre-call discovery burden currently carried by Matta's FDEs and CEO. It reuses approximately 70% of the orchestration patterns built for the CMMS Bridge — deterministic Action Domain Classifier, N=3 Gemini Flash ensemble with conformal sets, parallel verifier, durable outbox, Pydantic-extra-forbid throughout — but reverses the data flow and changes the demo theater entirely.

## Justification

Gemini's audit was correct on Claim C (the original FDE CMMS burden is fabricated — the FDE JD makes zero mention of integration work) and correct on Claim B (the Fiix mock should never have shipped to a B&W / Caracol / Cummins audience that lives in SAP). Gemini was also broadly correct on Claim A's substantive verdict (the closed-loop cyber-physical patent doesn't read on a webhook-to-CMMS sidecar), even though the ✅ was inferred from the Nature Communications 2022 disclosure rather than from a primary read of claim 1 of US 18/846,155.

But Gemini's proposed replacement premise has not been audited at the same rigor. Stress-testing it against Matta's primary substrate produces a worse failure than the original. Matta has three separate verbatim statements on their public surface — the Tech.eu funding piece, the IfM news page, and the Special Projects JD — explicitly claiming deployments go live "within hours" and that the install time is "less than 24 hours, when the industry standard is about 6 months." Speed of deployment is Matta's stated commercial differentiator, the headline claim in their funding announcement and their case studies. Walking into Doug or Damjan's inbox with "as you scale, enterprise IT departments will inevitably demand integration that slows your deployment timeline" actively contradicts Matta's own marketing. The vendor isn't just speculating about a future pain; the vendor is telling Matta their public commercial positioning is wrong. That's a worse failure than the original misframe, because it lands on a more sensitive nerve — Matta's go-to-market story.

Gemini's own latent-bottleneck inventory surfaces the answer. The FDE JD explicitly carves trade-show lead qualification, customer engagement, and pre-deployment scoping into the FDE role: *"engaging prospective customers, qualifying leads… at trade shows."* The Special Projects JD doubles down: *"steering long-term strategy, supporting fundraising efforts, and helping close customer deals… probably our most important hire."* Doug's own posting cadence — speaking at Giant Ventures, Paris meetings with 1st Kind, MACH 2026, Southern Manufacturing & Electronics — confirms pre-sales work is consuming founder hours, not just FDE hours. This is a JD-anchored, currently-attributed pain with a second-source confirmation. Gemini surfaced it and dismissed it without architectural analysis. A stateless software sidecar can absorb a meaningful slice of it.

Note for Hafeedh: I am not uncertain on the verdict. Two falsified premises plus a stronger alternative pivot meet both of the conditions specified for KILL-AND-RESTART. If the goal is to ship credible cold outreach that survives Damjan's first 5-minute test, the CMMS Bridge cannot ship under any framing the available substrate supports. If you want to push back on this call, the discussion to have is whether The Brief is in fact the strongest replacement — not whether the CMMS Bridge can be salvaged with a third pivot.

## Patent Citation Disposition

Remove all references to US Patent Application 18/846,155 from client-facing material — cold email, video, deck, sandbox copy. Gemini's Claim A audit confirmed the application's existence via aggregator indexing but explicitly admitted the substantive claims of the US application "remain obscured from standard bulk retrieval." This means the substantive verdict (Bridge / The Brief sits cleanly outside closed-loop cyber-physical control) was inferred from the Nature Communications 2022 paper, not from reading claim 1.

The substantive verdict still holds — the Brion-Pattinson 2022 disclosure in *Nature Communications 13, 4654* describes a closed-loop neural-network correction system for 3D printing in-process parameters, which is a fundamentally different action space from anything The Brief touches. But the cite goes to the *Nature Communications* paper (which is real, public, and verifiable), not to the patent application number. Sebastian Pattinson is a co-author of that paper; he cannot dispute its existence or its scope.

Where the patent boundary needs to be addressed in conversation, frame it as: *"We respect the closed-loop control work disclosed in your 2022 Nature Communications paper. The Brief operates entirely upstream of any factory deployment — it never reads from a Matta camera, a Matta agent, or a Matta-emitted signal."* No application number cited.

## Reposition Adjudication

### Gemini's proposed premise (verbatim from audit)

> "As Matta scales its aggressive 400+ factory pipeline, enterprise IT departments will inevitably demand strict SAP/Maximo integration as a prerequisite for deployment. A stateless, webhook-consuming sidecar absorbs this impending logical integration burden, preemptively preventing your FDEs from being repurposed into IT middleware consultants and keeping them focused strictly on physical deployment and factory sentience."

### 1F-red verdict on the proposed premise

**FAILS.**

### Second 1F-sim outcome

Damjan reads the new email at minute 0. His skepticism is already elevated because he just verified four minutes ago that the original premise was fabricated.

Minute 1: He reads "enterprise IT departments will inevitably demand strict SAP/Maximo integration." He notes the use of *"inevitably"* and *"impending"* — speculation language, not evidence language. He searches for any Doug post or company statement that calls IT compliance a deployment friction.

Minute 2: He searches matta.ai and Doug's recent LinkedIn for "compliance," "IT," "ERP," "procurement," "security review." He finds zero matches. He searches for "deployment" instead, and finds the company's own marketing: *"Most deployments are live within hours."* He finds the IfM funding announcement: *"users install vision-based inspection and quality control AIs in less than 24 hours."*

Minute 3: He notes that the vendor is asserting a future deployment friction that contradicts Matta's stated 24-hours-vs-industry-6-months differentiator. He reads this as the vendor either not knowing Matta's positioning or actively trying to sell against it.

Minute 4: He concludes the vendor has now produced two unfalsifiable framings about Matta's operational reality in succession — first about FDE workload, now about IT compliance. The pattern looks like positioning theater rather than research. He archives both emails.

Time to contradiction: 3 minutes. The premise dies faster than the original because Damjan is now primed to look for fabrication.

### Final premise (replacing both Gemini's reposition and the original)

The CMMS Bridge does not ship. The Brief does. Its premise:

> "Matta's FDEs are explicitly tasked with trade-show lead qualification and pre-deployment customer discovery in their own job description, and the Special Projects role exists in part to absorb that load — a load Doug himself is currently carrying via his founder-led trade show calendar. The Brief is a stateless sidecar that takes a factory name plus a five-question intake at a trade-show booth and returns a 90-second scoped opportunity brief — likely production lines, likely defect classes for that vertical, comparable Matta deployment patterns, suggested pitch angle, calendar link — formatted as a Slack mobile card the FDE can read during the conversation. It absorbs the discovery work that today happens in the 24 hours after the booth conversation and compresses it into the 60 seconds during the booth conversation."

This premise is anchored in two JD-verbatim sources (FDE and Special Projects), confirmed by Doug's own posting pattern, and structurally compatible with Matta's "speed wins" commercial narrative — it accelerates rather than contradicts their stated edge.

## Alternative Pivot Consideration

Gemini's three latent-bottleneck candidates were optical/lighting friction, EMF interference, and pre-sales burden. The first two are hardware-domain problems incompatible with Kaide's stateless-software-sidecar model — software cannot shield EMF or auto-tune photometric environments without becoming a hardware product. They are correctly identified as Matta-internal pains but they fall outside Kaide's deliverable surface.

Pre-sales burden is the only candidate that is (a) currently-attributable in JD-verbatim language, (b) confirmed by a second independent public source (Special Projects JD), (c) structurally addressable by a stateless software sidecar that reuses our existing orchestration patterns, and (d) compatible with — actually reinforcing — Matta's stated commercial differentiator on deployment speed.

The CMMS Bridge build work is not wasted. The deterministic Action Domain Classifier transfers (mapping inquiry-type to vertical-specific scoping path). The N=3 Gemini Flash ensemble with conformal set transfers (categorical confidence on likely-defect-class predictions). The parallel verifier and durable outbox transfer (the FDE may be offline at a trade show; the brief queues and ships when connectivity returns). The Pydantic-extra-forbid posture and the Theater UI scaffolding transfer with cosmetic changes. Approximately 70% of the codebase ports across; the schemas and the demo theater change.

## Sentence-Level Positioning Edits

### Cold email — Subject line

`The 60-second pre-call brief, for Hannover and beyond`

### Cold email — Doug's tagged line

> Doug — you've been carrying the trade-show calendar yourself this season (Giant Ventures, Paris with 1st Kind, MACH 2026), and the FDE JD makes pre-sales discovery and lead qualification an explicit part of the role. We built a thing that turns a factory name and a five-question intake into a scoped opportunity brief on your phone in under 60 seconds — likely production lines, likely defect classes, comparable Matta deployment, suggested pitch angle. Built specifically for the booth conversation, not the post-conversation follow-up.

### Cold email — Damjan's tagged line

> Damjan — stateless sidecar, FastAPI ingress, Pydantic everywhere with `extra="forbid"`, deterministic rules engine for the routing decision (no LLM in the load-bearing path), N=3 Gemini Flash ensemble with conformal prediction sets for the categorical inference layer, durable outbox so an FDE on factory-floor wifi doesn't drop the brief. Reference architecture you can read; absorbable in-house when the bandwidth fits.

### Cold email — CTA

> 90-second video at the link — skip to 0:14 if you want the magic moment first, technical walkthrough follows. If the architecture lands we can scope a 15-minute call. If not, no follow-up from me.

### Why-video script (75 seconds)

```
[0:00–0:08]  COLD OPEN — silent. Trade show booth simulation,
             stock footage of Hannover Messe floor, an engineer
             walks up to a booth labeled "Industrial AI." FDE
             pulls out phone.

[0:08–0:14]  SILENT — FDE types "Cummins Daventry plant" plus
             three quick questions into a Slack slash command.
             Submit.

[0:14–0:18]  THE BRIEF MATERIALIZES — Slack mobile card fills in
             on screen. Engine block production. Likely defects:
             porosity, dimensional drift, surface finish.
             Comparable deployment: polymer extrusion case study.
             Calendar link.

[0:18–0:30]  VOICEOVER (Hafeedh) — "What you just watched is a
             stateless sidecar built for the conversation that
             happens at a trade-show booth, not the conversation
             that happens after. Factory name plus five questions,
             returns a scoped opportunity brief in under 60 seconds."

[0:30–0:55]  TECHNICAL WALKTHROUGH — three-pane theater. Show the
             deterministic Action Domain Classifier routing the
             inquiry to vertical-specific scoping. Show the three
             parallel Gemini Flash calls running in ensemble. Show
             the conformal prediction set on likely-defect-class.
             Show the Pydantic schema validation. Cost ticker
             ticks under one cent.

[0:55–1:10]  THE FDE JD CITATION — "The FDE role at Matta makes
             trade-show qualification and pre-deployment discovery
             part of the job description. The Brief absorbs the
             slice of that work that today happens in the 24 hours
             after the booth conversation, and compresses it into
             the 60 seconds during the booth conversation."

[1:10–1:15]  TAIL TEASE (verbal only) — "There's a downstream
             companion architecture for the post-deployment
             workflow side. Happy to walk that through on a call."

[1:15]       SIGN-OFF.
```

### Demo right-pane mock

The CMMS-pane debate is moot — The Brief doesn't terminate in a CMMS. The new right pane is the FDE's Slack mobile mock, in a phone frame, showing the materialized Brief card. No SAP, no Maximo, no Fiix.

The left pane changes too: from a mocked SENTRY camera feed to a stylized trade-show booth context (stock Hannover Messe footage with a Tailwind overlay). The center Theater pane is structurally identical to the CMMS Bridge demo — the orchestration is the same, only the schemas and the input/output endpoints change.

If you want a secondary screen later in the video to acknowledge the post-deployment workflow companion architecture (the verbal tail tease), use a single freeze-frame mock of an SAP PM work-order screen — sourced from SAP's own marketing screenshots, not invented — but only as a 3-second visual reference for the verbal tease, not a working demo. That keeps the option open without committing the build.

### Magic Moment framing

The Magic Moment is no longer "defect appears, work order materializes." It is "engineer approaches booth, FDE punches name into phone, scoped opportunity brief appears on FDE's phone before the engineer finishes their second sentence." The visceral demo is the FDE *reading the brief while the prospect is still standing there*. Doug recognizes this scene immediately because he's lived it for twelve months at every trade show on his calendar. Damjan recognizes it because his FDE JD describes it.

The 60-second budget holds: roughly 8 seconds for ingress and ADC, 18 seconds for the N=3 ensemble plus parallel verifier, 12 seconds for the Gemini Pro narrative generation inside the OpportunityBrief schema, 4 seconds for Slack dispatch. Cost per brief: well under one cent at current Gemini 3 pricing.

## Sebastian Readiness Check

> The Brief operates entirely upstream of any factory deployment — it's a pre-sales discovery sidecar that helps an FDE walk into a trade-show conversation with the right context, not a system that touches anything your foundation models produce. The architecture has no shared signal path with the closed-loop control work disclosed in your 2022 Nature Communications paper; The Brief consumes public corporate data and the patterns from your published case studies to produce a personalized pitch context, then disappears. If a Cummins engineer walks up to your booth, The Brief gives your FDE in 60 seconds what a senior solutions architect would prepare in two hours — and it never reads from anything your cameras emit.

## Damjan Readiness Check

> You absolutely could build this in-house — six months, a senior FDE plus an MLE plus an ongoing maintenance burden of the manufacturing-vertical knowledge graph and the per-vertical scoping templates. We've already built it; you'd have it running against your existing webhook contract in under two weeks, with the orchestration patterns documented as a reference architecture your team can absorb when the bandwidth fits. The £10k/month is structured against the FDE-day saved per qualified trade show contact — a single qualified Cummins-class lead earned by walking into the second meeting better-prepared pays the year.

## Phase 1 Build Implications

### Architecture changes (PHASE_1_SPEC.md needs revision)

**Schemas.** `MattaDefectEvent` is replaced by `FactoryProspectInquiry` (factory name, 5-question intake, FDE identifier, trade show context). `RootCauseHypothesis` becomes `LikelyDefectClassHypothesis` with the same structural shape (categorical enum, conformal set, confidence band) but a different domain (defect classes for the inferred manufacturing process type). `CMMSWorkOrder` is replaced by `OpportunityBrief` (factory facts, likely defect classes, comparable Matta deployment, suggested pitch angle, calendar booking link).

**Action Domain Classifier rules.** Rewritten for inquiry routing. The deterministic mapping is `(stated_industry_keyword, factory_size_band, intake_question_pattern) → vertical_scoping_path`, with vertical paths covering polymer extrusion, metal casting, additive manufacturing, food and beverage bottling, electronics assembly, and aerospace composites. Default route on no-match: a generic "industrial AI scoping" path that flags `requires_human_review = True`.

**Ingress.** The webhook receiver becomes a Slack slash-command handler plus a fallback CRM webhook listener (HubSpot or Salesforce, polymorphic adapter). The Matta-side mock event publisher in the demo flow becomes a Slack-side mock command sender.

**Right-pane mock.** Replaces the Fiix CMMS UI with a Slack mobile mock in a phone frame. Drop the SAP/Maximo decision entirely from the build scope — those mocks were tied to the CMMS Bridge premise.

**Left-pane mock.** Replaces the mocked SENTRY camera feed with a stylized trade-show booth scene. Lower production cost than the camera-feed mock; can use stock footage from Hannover Messe / MACH 2026 as the visual base layer.

**Theater pane.** Architecturally identical to the CMMS Bridge version. The pipeline visualization (ingress → ADC → ensemble → conformal → verifier → narrative → outbox → ack) is the same; only the schema labels and the demo data change.

**Outbox.** Renamed from `cmms_outbox` to `brief_dispatch_outbox` but functionally identical. The graceful-degradation story (FDE on flaky trade-show wifi, brief queues until connectivity returns) is structurally the same as the air-gapped factory story but more visceral and easier to demo.

### Architecture preserved (no changes needed)

The N=3 Gemini Flash deep ensemble pattern, the conformal prediction set computation, the parallel Stage 2.5 verifier fan-out, the Pydantic `extra="forbid"` posture, the Vertex AI europe-west4 pinning, the deterministic-routing-over-LLM-routing principle, the deep ensembles voiceover disclaimer, the Damjan idempotency primitives — all transfer unchanged.

### Knowledge graph

The Brief depends on a manufacturing-vertical knowledge graph (vertical → likely production processes → likely defect classes → comparable Matta case study patterns). For the demo this is a small hand-built JSON file covering six verticals with five defect classes each. Production scaling is a Phase 2 concern. Building the demo-quality version is approximately six hours of curation work.

### Sprint impact

The 72-hour sprint is unaffected in length. The schema rewrite, the demo theater change, and the knowledge-graph curation are roughly offset by the work already completed on the orchestration spine. The Vidyard recording flow is unchanged in its structure (cold open, technical walkthrough, verbal tail tease) — only the on-screen content changes.

### Outreach delivery sequencing

The cold email's CTA links to a Vidyard timestamped to the magic moment (0:14). The verbal Phase 2 tease at 1:10 references "the downstream companion architecture for the post-deployment workflow side" — that is the dormant CMMS Bridge architecture, retained as a verbal-only adjacent idea per the Identity manifesto's outreach mechanic. If Doug or Damjan asks about it on the discovery call, we have it ready to scope as a Phase 2 engagement after The Brief proves itself.

---

*End of Matta_positioning_final.md*


═══════════════════════════════════════════════════════════════
END FILE: Matta_positioning_final.md
═══════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════
FILE: LATERAL_PRD_v1.md
PURPOSE: Lateral architecture v1 (Slack Command Center). Synthesis input.
═══════════════════════════════════════════════════════════════

# LATERAL_PRD_v1.md

## The Concept.

**Broken axes: Ingress shape, Output shape, Buyer/user surface, Pipeline shape.** The Slack Command Center replaces the Refinery's CSV-to-desktop dashboard with a Slack-native intake and review loop. FDEs or Doug forward a Hubspot/Salesforce export email to a monitored Slack channel, upload the CSV directly, or paste a prospect name into `/matta-refinery triage`. The system parses the payload, creates a batch, posts the ranked shortlist into a live Slack canvas, and lets the FDE click "Generate pre-visit dossier" inside Slack.

This is not the killed mobile booth Brief. It is asynchronous post-show-to-pre-visit workflow, but it lives where Doug, Special Projects, and FDEs already coordinate. Stage 1 and Stage 2 both exist: Stage 1 produces a capacity-aware shortlist thread, while Stage 2 promotes selected prospects into structured dossier sections inside the same Slack canvas. The pipeline is slightly more parallel than the Refinery: a lightweight dossier stub runs for every top-12 prospect as soon as ranking completes, then full dossier generation expands only when a human promotes one.

The Anti-Replication posture is clean. Matta's core roadmap is factory sentience, Manufacturing Foundation Models, agents, the Manufacturing OS, and edge infrastructure. A Slack coordination sidecar that consumes public lead data and produces internal pre-visit intelligence is adjacent, detachable, and DMZ-clean. Damjan should feel relieved because the system preserves typed API contracts behind a familiar coordination surface rather than asking him to absorb a new strategic dashboard.

## The Strategic Hook.

The Slack-native surface is justified by the bottleneck evidence, not by a generic "teams use Slack" claim. `Matta_Intel_cleaned.md` line 114 says Doug is "deploying to around two factories a month" with "a multi-year waitlist"; line 294 says UK Metals Expo produced "124 leads in two days"; and line 284 says Advanced Engineering day one produced "over 100 incredible leads." That is too much post-show triage for a founder and FDE team to manage through ad hoc threads, but it is exactly the kind of async coordination Slack can absorb without pretending to decide deployment strategy.

The user psychology is specific. The Special Projects role is "probably our most important hire" and must "distil the team's often technical, complex, and sometimes chaotic/scatter-brain ideas into concise, polished points" (`Matta_Intel_cleaned.md` line 625). A Slack canvas that continuously compresses raw lead volume into ranked candidate briefs gives that hire a native coordination surface. The FDE JD says FDEs handle "engaging prospective customers, qualifying leads, scoping problems" (line 704) and then one week later may be "deep in a factory" (line 705). Slack keeps the workflow reachable while FDEs are moving, without reviving the killed "60-second at the booth" premise.

Founder psychology from `Matta_Dossier.md` also supports this lateral. The Brion section describes him as metric-driven and focused on deployment velocity (sections 2, 5, and 6; especially lines 43, 67, 75-76). The Denic section says he is an execution maximalist who values schema hygiene, idempotency, and working code over pitches (sections 2, 4, and 6; lines 162-195). Slack is only the shell: the persuasive artifact for Denic is the typed event ledger, OpenAPI contract, and idempotent worker path behind every button.

## The Agent Architecture.

All inference runs through Vertex AI in `europe-west4` using `google-genai`. The only model IDs are the modernized PRD's `gemini-3-flash-preview` and `gemini-3.1-pro-preview`. No global endpoint, no non-Google provider, and no call path touches Matta cameras, agents, foundation models, product UI, edge firmware, factory systems, CMMS, QMS, or real-time streams.

Ingress contract: Slack events enter `POST /slack/events` and interactive buttons enter `POST /slack/interactions`. CSV upload, forwarded email attachment, and slash-command text are normalized into `SlackLeadBatchIngress`, then into `LeadIntakeBatch`. Every Pydantic model sets `model_config = ConfigDict(extra="forbid")`. The deterministic ADC maps `slack_event_type + payload_shape` into `PRIORITIZATION`, `DOSSIER_STUB`, `DOSSIER_FULL`, or `HUMAN_REVIEW`. The LLM never chooses a route.

Stage 1: deterministic parsers extract rows, compute `batch_id`, and upsert `LeadProspect` by `(workspace_id, channel_id, external_lead_id)`. Enrichment remains non-LLM and allowlist-only. Vertical classification fans out to N=3 `gemini-3-flash-preview` calls with `thinking_level="minimal"` and temperatures 0.1, 0.5, 0.9. Plurality vote yields vertical; disagreement yields `vertical_uncertain`. Fitness scoring is deterministic Python. The shortlist is posted to Slack as a canvas plus thread, not as a desktop queue.

Stage 2: for top-12 prospects, the worker immediately creates `DossierStub` with deterministic fields and a low-cost process headline. Full dossier runs only after the FDE clicks `Generate Full Dossier`. Process taxonomy uses `gemini-3.1-pro-preview`, N=1, `thinking_level="medium"`. Defect-class hypothesis uses N=3 `gemini-3-flash-preview` with conformal calibration. Comparable deployment, risk register, and suggested approach use `gemini-3.1-pro-preview`, N=1, `thinking_level="low"`, each bound to fixed Pydantic schemas. Citation-provenance checks validate every knowledge-graph anchor against `Matta_Intel_cleaned.md` line references before Slack receives the section.

Idempotency is layered: Slack event retry ID prevents duplicate receipt; file hash plus Slack user plus channel plus day prevents duplicate batch scoring; `(prospect_id, signal_hash, knowledge_graph_version)` prevents duplicate full dossier generation. Graceful degradation: if Slack canvas APIs fail, the API posts a threaded fallback message with a signed document URL; if enrichment fails, the canvas marks `partial_enrichment`; if Vertex AI rate-limits, the stub remains available and full dossier buttons show queued state.

## The Native Environment UI Spec.

The demo keeps the three-pane Vidyard theater pattern. Left pane is Slack desktop, not a CSV dashboard: a channel named `#fde-lead-refinery` receives a forwarded Hubspot export and a short note, "UK Metals Expo batch, please triage." The top of the pane shows the upload, then the live-updating Slack canvas with ranked candidates and buttons.

Center pane is the Theater state view. It shows inbound Slack event JSON, deterministic ADC route, idempotency keys, N=3 Gemini Flash cards, conformal calibration, and schema validation badges. The JSON inspector must reveal `extra="forbid"` Pydantic payloads and the Slack event retry ID.

Right pane is the Slack canvas output. It starts empty, then fills with "Batch scored: 124 leads, top 12 for review." When the FDE clicks "Generate Full Dossier" on William Cook Sheffield, the same canvas expands section by section. Cold-open timing: T+0 Slack upload, T+8 ranked shortlist, T+12 human click, T+25 taxonomy section, T+40 conformal defect set, T+60 comparable deployment with citation line, T+78 risk and approach sections, T+85 Slack canvas complete. The visceral payoff is under 90 seconds.

## Phase 1 Execution Spec.

Repository structure:

```text
matta-refinery/
  apps/slack_refinery_api/
    main.py
    routers/slack_events.py
    routers/slack_interactions.py
  apps/refinery_worker/tasks/
    parse_slack_ingress.py
    score_slack_batch.py
    generate_dossier_stub.py
    generate_full_dossier.py
  apps/theater_ui/components/
    SlackLeftPane.tsx
    TheaterStatePane.tsx
    SlackCanvasRightPane.tsx
  packages/schemas/slack_ingress.py
  packages/schemas/lead_intake.py
  packages/schemas/dossier.py
  packages/adc/rules.py
  packages/prompts/
  scripts/seed_slack_demo.py
```

Critical schemas:

```python
class SlackLeadBatchIngress(BaseModel):
    model_config = ConfigDict(extra="forbid")
    slack_event_id: str
    workspace_id: str
    channel_id: str
    user_id: str
    source_label: str
    file_sha256: str | None = None
    raw_text: str | None = Field(None, max_length=4000)

class SlackDossierAction(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action_id: Literal["generate_stub", "generate_full_dossier"]
    prospect_id: str
    signal_hash: str
    slack_response_url: str
```

FastAPI contracts: `POST /slack/events` validates Slack signature, dedupes `slack_event_id`, normalizes files or text into `LeadIntakeBatch`, and enqueues `score_slack_batch`. `POST /slack/interactions` validates button payloads, computes dossier idempotency key, and enqueues full dossier generation. Both return within Slack's timeout while work continues in Celery with `task_acks_late=True`.

Prompt templates mirror the Refinery but add a Slack output discipline: every section must include a compact `canvas_summary` plus a full `structured_section`. `gemini-3.1-pro-preview` never writes directly to Slack; it writes to Pydantic, then a renderer converts schema to Slack blocks/canvas sections. Mock data seeds the 124-row UK Metals Expo batch with William Cook, Tata Steel, Ernest Wright, Centriblast, and Safran Seats GB from line 294. Demo recording begins with a real Slack mock, not a landing page.

Magic Moment success criteria: Slack shortlist visible within 10 seconds; full dossier complete within 90 seconds after upload; Theater proves deterministic ADC before model calls; defect section shows three Flash samples and conformal set; every comparable deployment shows citation line provenance; duplicate Slack retries do not create duplicate prospects.

## Lateral-Specific Risk Register.

**Risk 1: Slack surface looks too lightweight for Sebastian.** A canvas can feel conversational rather than rigorous. Mitigation: center-pane JSON inspector and citation panel stay visible, and the right pane includes compact but explicit coverage, provenance, and human-review flags.

**Risk 2: Doug treats Slack ranking as a decision engine.** A ranked Slack thread could feel like it is telling the founder who to deploy to. Mitigation: label output "candidate shortlist for review," require a human click before full dossier generation, and show strategic-context fields as `unknown_to_sidecar`.

**Risk 3: Damjan distrusts Slack API state.** Slack event retries and canvas edits are messy. Mitigation: Slack is never the system of record; Postgres stores canonical events, idempotency keys, prospect state, and dossier artifacts, while Slack is a projection.


═══════════════════════════════════════════════════════════════
END FILE: LATERAL_PRD_v1.md
═══════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════
FILE: LATERAL_PRD_v2.md
PURPOSE: Lateral architecture v2 (CRM-Native Deployment Slot Sidecar). Synthesis input.
═══════════════════════════════════════════════════════════════

# LATERAL_PRD_v2.md

## The Concept.

**Broken axes: Ingress shape, Output shape, Statefulness location, Buyer/user surface.** The CRM-Native Deployment Slot Sidecar breaks the Refinery's separate dashboard and Postgres-first product surface. Hubspot or Salesforce becomes the operating surface and primary prospect system of record. The sidecar subscribes to CRM export/webhook events, enriches and scores leads in the background, then writes back a custom object or note: `Matta Deployment Intelligence`.

Stage 1 is not a standalone queue UI. It appears as CRM list views and per-lead fields: `refinery_fit_score`, `vertical`, `slot_readiness`, `requires_human_review`, and `next_best_action`. Stage 2 appears as a dossier note or attached Google Doc link on the promoted prospect. This solves the continuous post-show-to-pre-visit bottleneck without asking Doug or the Special Projects hire to maintain another system.

The lateral breaks a real assumption rather than reskinning the Refinery: state lives in the CRM where the lead already lives. The sidecar keeps only an idempotency/event ledger and cache, not canonical prospect ownership. Anti-Replication holds because Matta is not building CRM workflow software as core IP; this is an adjacent integration layer that can be unplugged without touching any Matta product surface.

## The Strategic Hook.

The strongest hook is "do not add another place to look." `Matta_Intel_cleaned.md` line 294 says UK Metals Expo produced "124 leads in two days," and line 284 says Advanced Engineering produced "over 100 incredible leads" on day one. The existing workflow almost certainly starts in a CRM or export because the modernized PRD already names Hubspot/Salesforce export as a valid Refinery source. This lateral accepts that gravitational center and turns the CRM itself into the triage board.

The CRM-native output also matches the Special Projects job. Line 625 says the hire will support strategy, fundraising, and customer deals, and must turn complex ideas into concise, polished points for corporate partners. A dossier written back to the CRM account/contact record is immediately reusable for founder review, FDE prep, and follow-up. The FDE JD line 704 names "engaging prospective customers, qualifying leads, scoping problems"; line 705 says the same person moves from trade shows to factories. CRM-native continuity keeps that handoff traceable.

`Matta_Dossier.md` supports the founder-specific psychology. Brion is described as the commercial force driving two-factory-per-month scaling (section 2, line 43) and as pragmatic and metric-driven (section 5, line 67). Damjan's section says he is the gatekeeper for FastAPI, Pydantic, Postgres, SQLAlchemy, Redis, and Celery patterns (line 164), but also that he rejects hand-wavy architecture and demands idempotency (lines 178-183). This lateral gives Brion the least new operational drag and gives Damjan a small, typed integration adapter rather than a new application to own.

## The Agent Architecture.

All model calls route through Vertex AI `europe-west4` via `google-genai`, using only `gemini-3-flash-preview` and `gemini-3.1-pro-preview`. The sidecar remains upstream of deployment and never reads or writes Matta production systems, factory data, camera streams, edge firmware, Manufacturing Foundation Models, or Manufacturing OS surfaces.

Ingress contract: `POST /crm/webhook/hubspot`, `POST /crm/webhook/salesforce`, and `POST /crm/export/email` normalize CRM records into `CRMLeadSignal`. The deterministic ADC routes events by `(crm_provider, object_type, changed_fields, action)` into `PRIORITIZE_RECORD`, `PRIORITIZE_BATCH`, `DOSSIER_REQUEST`, or `HUMAN_REVIEW`. Unknown objects stop at human review. Schemas use `extra="forbid"` and provider-specific adapters map native CRM IDs to `external_lead_id`.

Stage 1: deterministic enrichment runs on changed or newly imported leads. N=3 `gemini-3-flash-preview` classifies vertical with `thinking_level="minimal"` and temperatures 0.1, 0.5, 0.9. Deterministic scoring writes back CRM fields and appends an audit note explaining the score as candidate surfacing, not decision automation. Conformal calibration is not used on the fit score because scoring is deterministic; it is reserved for defect-class hypotheses where the PRD requires it.

Stage 2: the FDE clicks a CRM button or changes `Generate_Dossier__c=true`. The sidecar reads the CRM record plus public enrichment cache and produces `PreVisitDossier`. Process taxonomy uses `gemini-3.1-pro-preview`, N=1, `thinking_level="medium"`. Defect-class hypothesis uses the N=3 Flash ensemble plus conformal calibration. Comparable deployment, risk register, and suggested approach use Pro N=1 `thinking_level="low"` under fixed schemas. Citation-provenance validation runs before the sidecar writes the CRM note or attachment link.

Statefulness location: the CRM owns prospect state. The sidecar owns only `crm_event_ledger`, `signal_hash_cache`, `dossier_generation_runs`, and `knowledge_graph_version`. Idempotency keys are `(crm_provider, crm_object_id, crm_updated_at, changed_field_hash)` for lead updates and `(crm_object_id, signal_hash, knowledge_graph_version)` for dossiers. Graceful degradation: if CRM writeback fails, output goes to a retry queue and Slack fallback; if enrichment is partial, CRM fields explicitly show `partial`; if Vertex AI is unavailable, the CRM note says dossier queued, not failed.

## The Native Environment UI Spec.

The three-pane theater keeps the Vidyard pattern. Left pane is a Hubspot/Salesforce-style lead list after UK Metals Expo import. Rows include William Cook, Tata Steel, Ernest Wright, Centriblast, and Safran Seats GB. As the sidecar runs, the CRM fields fill in: score, vertical, reason, and "Generate dossier."

Center pane is the system theater with webhook event JSON, ADC route, CRM object ID, idempotency hash, worker state, N=3 Flash cards, conformal set, and citation validation. It must show that the CRM is the system of record and the sidecar is a typed adapter.

Right pane is the CRM record detail. The dossier appears as a CRM note with structured sections and a link to a rendered document. Cold-open timing: T+0 CRM webhook receives 124-lead import, T+10 list fields populate for top candidates, T+15 FDE toggles `Generate dossier`, T+30 taxonomy appears in note, T+45 conformal defect set, T+60 comparable deployment citation, T+80 full CRM note with suggested approach. The payoff is under 90 seconds.

## Phase 1 Execution Spec.

Repository structure:

```text
matta-refinery/
  apps/crm_refinery_api/
    routers/hubspot_webhook.py
    routers/salesforce_webhook.py
    routers/crm_actions.py
  apps/refinery_worker/tasks/
    normalize_crm_event.py
    prioritize_crm_batch.py
    writeback_crm_fields.py
    generate_crm_dossier.py
  packages/crm/
    base.py
    hubspot.py
    salesforce.py
    retry_outbox.py
  packages/schemas/crm.py
  packages/schemas/dossier.py
  packages/adc/rules.py
  apps/theater_ui/components/
    CRMLeftPane.tsx
    TheaterStatePane.tsx
    CRMRecordRightPane.tsx
```

Critical schemas:

```python
class CRMLeadSignal(BaseModel):
    model_config = ConfigDict(extra="forbid")
    provider: Literal["hubspot", "salesforce"]
    object_type: Literal["lead", "contact", "account"]
    object_id: str
    updated_at: datetime
    changed_fields: dict[str, str | int | float | None]
    source_label: str | None = None

class CRMWritebackEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    object_id: str
    fit_score: float = Field(..., ge=0, le=1)
    vertical: str
    dossier_url: str | None = None
    requires_human_review: bool
```

FastAPI contracts: webhooks validate provider signature, persist event ledger rows, compute idempotency key, and enqueue Celery tasks. `POST /crm/actions/generate-dossier` accepts a CRM object ID and returns a `DossierAck`. Workers use `task_acks_late=True`, `worker_prefetch_multiplier=1`, and provider writeback retries through a durable outbox.

Prompt templates are identical in reasoning structure to the Refinery but produce CRM-safe summaries. The comparable deployment prompt accepts only knowledge-graph anchors with verified `citation_substrate_line`. Mock data creates a CRM import event for `UK_Metals_Expo_2025` and a Salesforce custom action. Demo recording uses fake CRM UI, not live CRM credentials.

Magic Moment success criteria: CRM fields update without page change; top candidates visible within 10 seconds; dossier note complete within 90 seconds; duplicate webhook delivery creates one ledger entry and one writeback; all generated sections validate with `extra="forbid"`; citation line provenance is visible in the CRM note.

## Lateral-Specific Risk Register.

**Risk 1: CRM dependency slows the 72-hour demo.** Real Hubspot/Salesforce APIs can eat sprint time. Mitigation: build provider adapters against mocked fixtures first, then add one real sandbox only if credentials are available.

**Risk 2: Damjan sees CRM as a messy source of truth.** CRMs contain duplicates and stale fields. Mitigation: make source-of-truth explicit: CRM owns lead identity, sidecar owns only derived intelligence and event ledger. Conflicts go to `requires_human_review`.

**Risk 3: Doug worries CRM writeback creates operational noise.** Too many fields and notes can clutter sales workflow. Mitigation: write only four Stage 1 fields plus one dossier note, and allow per-batch dry-run mode before writeback.


═══════════════════════════════════════════════════════════════
END FILE: LATERAL_PRD_v2.md
═══════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════
FILE: LATERAL_PRD_v3.md
PURPOSE: Lateral architecture v3 (Drive Corpus Refinery). Synthesis input.
═══════════════════════════════════════════════════════════════

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


═══════════════════════════════════════════════════════════════
END FILE: LATERAL_PRD_v3.md
═══════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════
FILE: LATERAL_PRD_v4.md
PURPOSE: Lateral architecture v4 (Deterministic Field Kit). Synthesis input.
═══════════════════════════════════════════════════════════════

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


═══════════════════════════════════════════════════════════════
END FILE: LATERAL_PRD_v4.md
═══════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════
FILE: Matta_Dossier.md
PURPOSE: Forensic founder dossier (Brion / Pattinson / Denic psychology). SECONDARY INDEX ONLY — do not cite as primary evidence. Primary citations must reference Matta_Intel_cleaned_numbered.md line numbers.
═══════════════════════════════════════════════════════════════

# **Forensic Founder Dossier: Matta**

## **Executive Intelligence Summary & Corporate Substrate**

The forensic analysis of Matta, a University of Cambridge spin-out operating out of the Institute for Manufacturing (IfM), reveals a highly sophisticated industrial artificial intelligence entity operating at the intersection of materials science, edge computing, and multi-modal computer vision \[1, 2\]. Founded in 2022 and headquartered at 77 East Road, London, Matta operates with a stated mission of establishing "factory sentience" to recover the estimated 20% of value lost in traditional manufacturing processes \[3\]. The company closed a $14M Seed funding round on December 10, 2025, led by Lakestar and Giant Ventures, augmented by strategic capital from deep-tech and industrial legacy investors including 1st Kind (the Peugeot family office), InMotion Ventures, RedSeed VC, Unruly Capital, and Boost VC \[4, 5\].

Matta's architectural footprint is defined by its rapid deployment capability. The intelligence indicates the organization is currently scaling at a rate of two new factory deployments per month, with individual customer go-live timelines compressed to mere weeks, feeding a pipeline of 300 to over 400 factory deployments \[3\]. The technology stack is distinctly physical-first, deploying hardware and software directly to the factory floor to execute unsupervised and self-supervised computer vision protocols \[2\]. The commercial product suite is delineated into four distinct industrial agents designed to bypass legacy constraints.

| Industrial Agent | Core Functionality | Operational Implication & Architecture |
| :---- | :---- | :---- |
| **Sentry** | Edge-deployed defect detection. | Operates without manual calibration, learning "good" states directly on the line \[3\]. Implies self-supervised anomaly detection models requiring low-latency edge inference. |
| **Tally** | Dimensional measurement and metrology. | Achieves micron-accurate measurements in seconds, bypassing Coordinate Measuring Machines (CMMs) \[3\]. Suggests highly calibrated stereoscopic or structured-light camera integrations. |
| **Gauge** | Parts counting and kitting verification. | Utilizes video feeds to eliminate manual tallying and mis-kits during assembly \[3\]. Indicates continuous temporal tracking and state-management algorithms. |
| **Trace** | High-speed part traceability. | Tracks origin and history to answer audit queries in seconds rather than hours \[3\]. Requires deep database indexing, likely utilizing their Postgres/Alchemy stack \[intel.md: All open Matta job listings\]. |

The organizational structure is driven by three primary decision-makers, each occupying a distinct functional and philosophical domain: Douglas Brion (Co-Founder & CEO, the commercial and applied engineering vector), Sebastian Pattinson (Co-Founder & Chief Scientist, the materials science and cyber-physical security vector), and Damjan Denic (Chief Technology Officer, the architectural and execution gatekeeper) \[3\]. Understanding the interplay between Brion's commercial velocity, Pattinson's academic rigor, and Denic's execution constraints is the fundamental key to successfully navigating the Matta procurement and technical vetting process.

## ---

**Subject 1: Douglas Brion – Co-Founder & Chief Executive Officer**

### **1\. Background (Career History, Education, Family, Pre-Matta Context)**

Douglas Brion’s academic and professional trajectory demonstrates a highly unusual but potent synthesis of creative discipline and rigorous deep-tech engineering. His undergraduate foundation was established at Imperial College London, where he earned a Bachelor of Engineering in Electronic and Information Engineering \[6, 7\]. His tenure at Imperial was marked by exceptional performance; he achieved First Class Honours and secured the prestigious Governors' Prize for outstanding academic performance, laying the mathematical groundwork for his future work in algorithmic control systems \[7\]. Prior to this, his secondary education culminated in AAA at A-Level in Mathematics, Further Mathematics, and Physics, indicating a deeply ingrained quantitative orientation \[7\].

Concurrently, the intelligence reveals a high-level classical music background. Brion was an Ash Music Scholar at the Royal College of Music, specializing in recorder performance \[7\]. This dual capability in advanced physics and classical music training strongly indicates a cognitive profile optimized for highly structured, precise, and pattern-oriented problem-solving. Musical training at a conservatory level requires an obsession with micro-adjustments, timing, and structural architecture—traits that map directly onto the requirements of micron-accurate industrial control systems.

Prior to his doctoral studies, Brion acquired practical engineering exposure during a summer internship at Ricardo, a global engineering and environmental consulting firm known for automotive and industrial powertrains, which likely provided his first exposure to heavy industrial processes \[7\]. He also developed pedagogical skills as a personal tutor specializing in Mathematics and Programming at Chiswick Tutoring, demonstrating an early aptitude for distilling complex technical concepts \[7\].

His subsequent transition to the University of Cambridge (Gonville & Caius College) marked his entry into the Complex Additive Materials Group (CAM Group) within the Department of Engineering, funded by the EPSRC DTP initiative \[7\]. Under the supervision of Dr. Sebastian Pattinson, Brion completed a seminal PhD thesis titled *"Deep learning enabled error detection and correction for 3D printing"* in 2023 \[8, 9\]. The research, housed in the Cambridge Apollo repository, systematically dismantled the limitations of existing error detection in additive manufacturing. He moved beyond single-modality recognition to develop multi-head neural networks capable of real-time, multi-parameter correction \[8, 9\]. To achieve this, Brion built a proprietary data collection and labeling engine to generate process monitoring data from a fleet of 3D printers, training models for generalizable error detection, flow rate prediction, and long-term thermal deformation correction \[8\].

Brion's tenure at Cambridge was highly decorated. He was awarded the IET Postgraduate Scholarship for an Outstanding Researcher and the Royal Commission for the Exhibition of 1851 Industrial Design Fellowship, underscoring his status as an elite engineering talent within the UK ecosystem \[7, 10, 11, 12\]. Furthermore, he was selected as a Google X Moonshot Fellow. Anecdotal evidence from his time at X suggests exposure to highly ambitious, massive-scale engineering projects; a fragmented quotation linked to his fellowship references a project initially aiming for 20km but subsequently targeting the "Karman line" (the boundary of space at 100km altitude), indicating a structural conditioning from X to think in terms of exponential scale, extreme physical environments, and audacious engineering \[13\]. During this period, the early iteration of Matta, initially conceptualized as "Mattalabs," was launched and recognized as a finalist in the Imperial College Venture Capitalist Challenge \[6, 7\].

| Biographical Artifact | Detail & Source Verification | Implication for Outreach |
| :---- | :---- | :---- |
| **Imperial College Degree** | BEng Electronic and Information Engineering, First Class Honours, Governors' Prize \[7\]. | Understands the lowest levels of hardware/software integration. Pitching high-level software abstraction will fail. |
| **Royal College of Music** | Ash Music Scholar, Recorder performance \[7\]. | Appreciation for extreme precision, timing, and pattern recognition. Values aesthetic and structural elegance in code. |
| **Google X Fellowship** | Moonshot Fellow, exposed to Karman line/aerospace ambition scaling \[13\]. | Receptive to massive, audacious technical scaling. Thinks in orders of magnitude, not incremental improvements. |
| **Cambridge PhD Thesis** | "Deep learning enabled error detection and correction for 3D printing" \[8\]. | Uniquely understands the pain of data labeling in physical space. Built a fleet labeling engine himself \[8\]. |

### **2\. Current Role and Responsibilities at Matta**

As Chief Executive Officer, Brion operates as the primary commercial force and external interface for Matta, while remaining deeply embedded in the underlying engineering philosophy \[3\]. His responsibilities encompass driving the corporate scaling strategy. Matta is not pursuing a slow, consultative integration model; Brion is enforcing a deployment tempo of two new facilities every month, aiming to fulfill a pipeline of hundreds of factories \`\`. He directly manages the relationships with tier-one manufacturing partners, evident in his face-to-face interactions with entities like BAE Systems, McLaren Racing, Cummins, and his Paris meetings with the Peugeot family office (1st Kind) \[4\].

Operationally, Brion bridges the critical gap between academic AI research and the uncompromising realities of the factory floor. He serves as the primary evangelist for the company's "plug-and-play" deployment model, aggressively pushing for AI hardware solutions that do not require manufacturers to rip out or replace existing capital expenditure (CapEx) investments \[3, 14\]. Furthermore, he is the driving force behind the company's aggressive talent acquisition, actively authoring hiring posts and recruiting for roles across edge systems, forward-deployed engineering, and specialized AI research to sustain the company's rapid deployment cadence \[3\].

### **3\. Stated Public Positions and Thought Leadership**

Brion’s public posture is intentionally anti-hype, contrasting sharply with the prevailing narratives of pure software-as-a-service (SaaS) or generative AI startups. He actively critiques the theoretical elements of his own industry, arguing that concepts like digital twins and generative design fail to address the gritty, physical realities of the shop floor \[4, 15\].

His central philosophical thesis is built around the quantification, digitization, and scaling of tacit human knowledge. This is best encapsulated in his frequently cited public statement to the press: *"Manufacturing still runs on human know-how, the kind that lets someone on the line kick a machine just right, or run a finger over a scratch, and say, 'that's thirty-four microns wide.' We're using AI to capture and scale that tacit knowledge, so engineers can design things that actually work in the real world. It's time to manufacture the impossible."* \[4, 14, 15\]. This quote is critical intelligence; it reveals his belief that the human operator is not obsolete, but rather possesses physical intuition that current data models lack. Matta's goal is to digitize that specific intuition.

Brion actively champions a post-deindustrialization narrative, emphasizing the macroeconomic need to rebuild European and American manufacturing sovereignty. He frequently speaks at events like the Royal Academy of Engineering's "Sentient Factories" panel, framing physical AI as a mechanism for sustainability and resilience against fragile global supply chains \[2, 14\]. He views Matta’s technology as a critical mechanism to offset the dual pressures of a shrinking skilled workforce and the geopolitical mandate to reshore operations \[14, 15\]. Furthermore, his public communications reveal a focus on verifiable return on investment (ROI); he frequently highlights metrics such as achieving greater than 99% defect detection accuracy with only ten minutes of training data on a polymer manufacturing deployment \[15\].

(Note regarding the Imaging and Machine Vision Europe interview: The prompt requested extraction of specific technical details from this source. However, the primary URL \[[https://lnkd.in/eqnhQH7v](https://lnkd.in/eqnhQH7v)\] and the base domain result in inaccessible portals.16 Therefore, specific hardware configurations discussed in that specific interview remain \`\`. Null evidence confirms the payload is locked behind a strict paywall or expired session).

### **4\. Technical Decisions and Architectural Preferences**

Brion’s architectural preferences are deeply rooted in his doctoral research, specifically focusing on the interface between deep learning and physical closed-loop control \[8\]. His technical footprint on GitHub provides critical forensic intelligence into his engineering methodologies and what he demands from subordinate technical architectures \[17\].

Most notably, his pinned repository pytorch-classification-uncertainty contains a highly starred PyTorch implementation of the paper *"Evidential Deep Learning to Quantify Classification Uncertainty"* \[17\]. In the context of industrial automation, uncertainty quantification is the difference between a successful intervention and a catastrophic machine failure. A manufacturing model must be able to calculate its own confidence intervals and defer to human operators—or halt a PLC (Programmable Logic Controller)—when certainty drops, rather than making high-confidence errors that damage million-dollar equipment. Similarly, his repository pytorch-deep-ensembles focuses on scalable predictive uncertainty estimation using deep ensembles \[17\]. This indicates a rigid intolerance for "black-box" AI models; he demands explainability, probabilistic safeguards, and rigorous uncertainty mapping, directly mirroring his PhD thesis focus on "explainable AI... to create visualisations which shed light on how the deep learning models make their decisions" \[8\].

Brion also exhibits a preference for robust, interoperable edge-control software that operates close to the bare metal. His fork of OctoRest (a Python client library for the OctoPrint REST API) and his development of an automated part-removal system using raw G-code demonstrate a hands-on capability with the low-level communication protocols required to command physical hardware \[17\]. Furthermore, he is named as the primary inventor on US Patent Application 18/846,155 for a "Method, apparatus and system for closed-loop control of a manufacturing process," co-authored with Sebastian Pattinson, solidifying his commitment to patentable, defensible hardware-software architectures \[9\].

### **5\. Communication Style and Apparent Decision-Making Patterns**

Forensic analysis of Brion’s public footprint reveals a communication style that is highly assertive, pragmatic, and metric-driven. He deliberately distances himself from the vernacular of Silicon Valley software-as-a-service (SaaS) and the broader generative AI hype cycle. Instead, he speaks the lexicon of industrial engineering: "shop floor," "scrap," "rework," "micron-accuracy," and "root cause" \[2, 3, 4\].

His decision-making appears heavily weighted toward empirical physical validation. He values rapid deployment speed—highlighting the ability to go "live within weeks"—and immediate physical impact over protracted, theoretical integration phases \[3\]. His background orchestrating large datasets from a fleet of 3D printers suggests he makes technical procurement decisions based on data volume efficiency, the reduction of manual calibration overhead, and how quickly a system can achieve statistical significance on the edge \[3, 8\].

### **6\. Recommended Outreach Angles**

When architecting outreach directed at Douglas Brion, the intelligence dictates a strict adherence to physical-first, pragmatic realities.

* **Anchor on Uncertainty Quantification**: Pitching AI models, telemetry pipelines, or edge architecture should explicitly address how the system handles edge-case uncertainty. Referencing evidential deep learning or Bayesian confidence intervals will immediately align with his core technical philosophy and his GitHub artifacts \[8, 17\].  
* **Emphasize Deployment Velocity & Minimal Calibration**: Brion is hyper-focused on scaling to two new factories per month and achieving 99% accuracy with 10 minutes of data \[15\]. Any proposed architectural solution must definitively prove how it reduces friction in hardware deployment, eliminates manual data labeling constraints, and achieves "plug-and-play" interoperability with legacy factory systems \[3, 14\].  
* **Leverage Industrial Realism**: Discard theoretical AI terminology. Frame proposals in terms of reducing physical scrap, accelerating dimensional metrology (referencing his Tally product), and surviving the hostile environment of a polymer plant or casting line \[2, 3\]. Use the phrase "shop floor" rather than "cloud environment."

### **7\. Red Flags / Things to Avoid**

* **Pitching Pure Software/Digital Twin Paradigms**: Brion has explicitly stated that the "hard part isn't dreaming things up inside a computer; it is making them work at scale" \[4\]. Proposals that ignore the physics of the manufacturing environment, the latency of hardware actuators, or the Faraday-cage reality of a factory floor will be immediately dismissed.  
* **Black Box Neural Networks**: Given his doctoral work incorporating explainable AI, opaque models lacking transparency or uncertainty estimation are a critical red flag \[8, 17\]. He requires knowing *why* a model made a classification.  
* **Referencing Outdated Personal Domains**: His personal website (douglasbrion.com) is currently inaccessible, and his legacy Udemy/GitHub Pages tutorials on deploying personal brands appear to be obsolete SEO artifacts \[18, 19, 20, 21\]. Referencing these will signal superficial, automated, or outdated research.

## ---

**Subject 2: Sebastian Pattinson – Co-Founder & Chief Scientist**

### **1\. Background (Career History, Education, Family, Pre-Matta Context)**

Dr. Sebastian Pattinson represents the foundational academic and materials science bedrock of Matta. His academic journey began with a Bachelor of Science in Physics with Philosophy at the University of York \`\`. This unique combination is a critical indicator of his cognitive framework; it suggests a capacity for rigorous empirical analysis of physical forces coupled with foundational, first-principles systems thinking. He subsequently moved to the University of Cambridge, completing an MPhil in Micro- and Nanotechnology Enterprise, followed by a PhD in Materials Science \[1\].

Following his doctoral studies, Pattinson secured the highly competitive US National Science Foundation (NSF) SEES Postdoctoral Fellowship, relocating to the Department of Mechanical Engineering at the Massachusetts Institute of Technology (MIT) from 2014 to 2018 \[1\]. During this tenure, he was also selected for a Google X Moonshot Fellowship (June–November 2017), where he focused on the "analysis of early pipeline projects" \[1\].

*(Note regarding the founding origin story: While the exact chronological moment Brion and Pattinson met at Google X remains \`\` due to null evidence in the snippets, the intelligence explicitly confirms they formally founded Matta based on their relationship at the Cambridge IfM, where Brion was Pattinson's PhD student within the CAM group \[2, 5\].)*

Upon his return to Cambridge in 2018 as an Assistant Professor (promoted to Associate Professor in 2023\) in the Department of Engineering, he established the Computer-Aided Manufacturing (CAM) group within the Institute for Manufacturing (IfM) \[1\]. Pattinson is highly decorated within the UK and international research ecosystem, holding a UK Academy of Medical Sciences Springboard award, alongside EPSRC Doctoral and Masters Training Grants \[1\]. He is a native speaker of both German and English, providing Matta with a strategic linguistic and cultural advantage in penetrating the DACH (Germany, Austria, Switzerland) precision manufacturing sector 22.

### **2\. Current Role and Responsibilities at Matta**

As Chief Scientist, Pattinson is insulated from the day-to-day commercial friction managed by Brion, focusing instead on the fundamental physics, material science implications, and advanced research pipeline that powers Matta's foundational models \[3, 12\]. His core mandate is to translate cutting-edge academic research from the Cambridge CAM group into the commercial intellectual property fortress of the company \[2, 5\].

He is fundamentally responsible for the architecture of models that do not merely observe manufacturing geometrically, but understand the underlying physics of the materials being manipulated \[12\]. As he stated publicly, his objective is to ensure the AI learns the "fundamental physics of manufacturing processes" to "prevent scrap and rework at the source, delivering a direct, scalable cut to industrial emissions" \[2, 12\]. Furthermore, Pattinson acts as the primary conduit between Matta and the elite academic research ecosystem. He utilizes his position at Cambridge to continuously source top-tier talent from his PhD and postdoctoral advisees, staffing Matta's research division with experts in biomimetic structures, data-driven manufacturing, and robotic perception \[1\].

### **3\. Stated Public Positions and Thought Leadership**

Pattinson’s thought leadership is highly concentrated on the intersection of physical manufacturing, artificial intelligence, and cyber-physical security. His overarching research philosophy is categorized into three themes on his Cambridge CAM group platform: Learning Manufacturing Systems, Digitally Tailored Medical Devices, and the Security of Physical AI Systems \[1\].

He is a vocal proponent of "cyber-physical trust," a concept he presented at the ARIA (Advanced Research and Invention Agency) SoTA Frontiers Night alongside other leading researchers \`\`. This thesis is profound: as AI assumes closed-loop control over physical machinery (like robotic arms or polymer extruders), establishing cryptographic and probabilistic trust protocols to prevent catastrophic physical failure or malicious interference becomes an existential requirement \[1\]. An error in a chatbot is a hallucination; an error in an AI-controlled 5-axis CNC machine is a potentially fatal shrapnel event.

His environmental and macroeconomic positions align with the broader Matta narrative, framing physical AI primarily as a mechanism for sustainability. He views the reduction of physical waste (scrap) as the most direct method to cut industrial CO2 emissions and water usage, contrasting this grounded physical approach with carbon-offsetting software solutions \[2, 12\]. Furthermore, he regularly participates in specialized manufacturing forums, having delivered talks at the West Suffolk Manufacturing Group and presented heavily at robotics and automation conferences, such as his upcoming ICRA 2026 paper on self-verification for iterative robotic assembly \`\`.

(Note regarding the German Startup Insider podcast: The prompt requested a detailed transcript or summary capturing quotes about deployment friction. The primary evidence 22 only provides the episode title "Der schwierige Teil ist es zum Laufen zu bringen" and confirms the December 2025 date. The full audio transcript remains \`\`. However, the title itself serves as a verified quote indicating his focus on the friction of physical implementation over theoretical design).

### **4\. Technical Decisions and Architectural Preferences**

Analysis of Pattinson's publication record (possessing an h-index of 5 on his Matta-adjacent AI works, though his broader materials science footprint is extensive) reveals a highly sophisticated approach to manufacturing AI \[9\]. His architectural preferences are heavily biased toward multi-modal sensing and physics-informed neural networks \[1, 9\].

| Key Technical Publication/Artifact | Architectural Preference Implication |
| :---- | :---- |
| **"Viscoelasticity-Induced Controllable Periodic Meso-Textures"** \[intel.md\] | Deep understanding of non-Newtonian fluid dynamics. Demands AI that accounts for phase changes and thermal dynamics, not just rigid geometric kinematics. |
| **"Iterative learning for efficient additive mass production"** (2024) \[9\] | Preference for systems that learn continuously from cycle to cycle, updating internal representations dynamically rather than relying on static, pre-trained weights. |
| **CAM Group: Deformable Photoelastic Sensors** \[1\] | Strong preference for sensor modality diversity. Evaluates architectures on their ability to fuse standard visual data with novel tactile and photoelastic data streams. |
| **"Self-verification for iterative robotic assembly"** (ICRA 2026\) \[intel.md\] | Requires systems to possess self-checking cryptographic or logic loops before executing physical actions, tying back to his cyber-physical trust thesis. |

### **5\. Communication Style and Apparent Decision-Making Patterns**

Pattinson’s communication style is deeply academic, precise, and heavily weighted toward peer-reviewed validation \[1, 9\]. While Brion provides the aggressive commercial narrative, Pattinson supplies the unassailable empirical proof points. His decision-making is characterized by a "first principles" approach derived from his physics background; he will intuitively deconstruct any proposed software architecture down to its foundational mathematical and physical assumptions \[1\].

He is highly collaborative within the academic sphere, fostering a large network of PhDs and postdocs. For example, he supervises researchers like Christos Margadji, who is working on integrating "reasoning, imagination and memory into advanced manufacturing," and researchers focused on agri-food robotics \[1\]. This suggests he evaluates third-party technical proposals not just on their immediate functional capabilities, but on their theoretical runway and capacity to integrate with future, highly complex cognitive manufacturing tasks \[1\].

### **6\. Recommended Outreach Angles**

* **Focus on Cyber-Physical Security & Trust**: Given his explicitly stated research interest in the "Security of Physical AI Systems," outreach addressing how proposed architectures maintain edge data integrity, resist adversarial physical inputs, and ensure fail-safe operational boundaries will capture his attention immediately \[1\].  
* **Highlight Physics-Informed Architecture**: Software proposals must be framed in the context of physical realities. Demonstrate an understanding of how edge compute architectures specifically accommodate high-frequency sensor data relevant to viscoelasticity, thermal deformation, or flow dynamics \[1, 9\].  
* **Acknowledge Implementation Friction**: Referencing the title of his German podcast appearance ("The hard part is getting it to run") demonstrates a nuanced understanding of his core challenge: the friction between beautiful academic models and messy factory deployments 22. Propose engineering solutions that specifically bridge this gap.

### **7\. Red Flags / Things to Avoid**

* **Treating Manufacturing as a Pure Data Problem**: Pattinson views manufacturing as a physical physics problem that is merely augmented by data \[12\]. Proposing standard LLM architectures or purely statistical computer vision models without physical or material grounding will trigger immediate academic skepticism.  
* **Ignoring Edge-Case Safety for Speed**: Architectures that optimize for inference speed or cloud accuracy at the expense of deterministic safety guarantees run directly counter to his cyber-physical trust mandate \[1\].  
* **Superficial Academic References**: Misrepresenting or oversimplifying his work on multi-head neural networks or self-verifying robotic assembly \[9\] will destroy credibility. Outreach must demonstrate genuine technical comprehension of his ICRA 2026 and *Nature Communications* publications, not just title-dropping.

## ---

**Subject 3: Damjan Denic – Chief Technology Officer**

### **1\. Background (Career History, Education, Family, Pre-Matta Context)**

Damjan Denic serves as the critical translation layer between Matta's academic hypotheses and its functional, scalable cloud/edge architecture. Unlike the Cambridge-native founders, Denic’s origins lie in the highly competitive, execution-focused technology ecosystem of Belgrade, Serbia \[23\].

Denic's pre-Cambridge career is characterized by deep involvement in the Balkan hackathon and student engineering community. As a Full Member of the BEST Niš (Board of European Students of Technology) IT team from 2017 to 2022, he managed complex logistical and technical architectures, eventually serving as the NRR Coordinator for the entire EBEC Balkan Region, managing local rounds across multiple jurisdictions \[23\]. His hackathon pedigree is exceptional; operating within the "Red\!Tech" team, he secured first place at the WHOIS Online hackathon (September 2021\) and the ZenHire ML hackathon (May 2022), demonstrating a consistent ability to rapid-prototype functional machine learning applications under extreme time constraints \`\`.

Furthermore, he held leadership roles in developing the Artificial Intelligence BattleGround Nis (AIBG) video game environment as the "Topic Responsible" between 2021 and 2022 \[23\]. Game development requires foundational skills in low-latency event loops, state management, and memory optimization—skills highly transferable to managing live computer vision streams in a factory.

Professionally, Denic built a robust foundation in highly structured, asynchronous web and mobile development before moving to AI. At Codemancy Studio, he operated as a Junior Team Lead, architecting eCommerce solutions utilizing strict TypeScript and React \[23\]. Concurrently, at Mihajlovic Soft, he deployed web and mobile applications using React and Xamarin \[23\]. This background in state-heavy UI and asynchronous data fetching provides the precise skill set necessary to visualize complex, real-time factory data streams without locking the main thread.

In late 2022, Denic transitioned to the University of Cambridge to undertake an MPhil in Advanced Computer Science, pivoting his focus from commercial full-stack development to the rigorous mathematical and architectural demands of advanced computing, positioning him to assume the CTO role at Matta \`\`. *(Note: Denic's undergraduate university in Belgrade is linked via GitHub to the Faculty of Mathematics, University of Belgrade, evidenced by the MATF Computer Networks repository collection \[24\]).*

### **2\. Current Role and Responsibilities at Matta**

As Chief Technology Officer, Denic is the absolute architectural gatekeeper for Matta \`\`. While Brion and Pattinson define *what* the system must do physically and scientifically, Denic dictates *how* the system is built, scaled, secured, and deployed digitally \[3\].

He is responsible for managing a distributed, high-latency-intolerant tech stack that bridges physical edge nodes inside factories with centralized cloud oversight \[intel.md: All open Matta job listings\]. Analysis of Matta's engineering job descriptions reveals Denic's operational domain: he oversees a highly modern, python-centric architecture built on FastAPI, Pydantic, Postgres, SQLAlchemy, Redis, and Celery for the backend, coupled with Vue.js for the frontend, monitored via New Relic and Sentry \[intel.md: All open Matta job listings\].

Crucially, he manages the integration of WebSockets and WebRTC. These protocols are strictly required to stream and process live video data from industrial cameras (feeding the Sentry and Gauge modules) with millisecond latency to edge computers \[3\]. His operational reality involves guaranteeing uptime and data integrity across "1000s of real-time data streams across 100s of manufacturing processes," ensuring that local factory instances can operate completely disconnected from the cloud (air-gapped or intermittent connection) while still synchronizing state asynchronously when a connection is restored \[intel.md: All open Matta job listings\].

### **3\. Stated Public Positions and Thought Leadership**

In stark contrast to the CEO and Chief Scientist, Denic maintains a near-zero public thought leadership profile post-2022 \[23\]. His digital footprint is almost entirely defined by his pre-Cambridge technical execution and his teaching engagements, such as his April 2022 lecture at the Mathematical Grammar School in Belgrade \`\`.

This absence of public posturing is highly indicative of his operational posture: he is an execution maximalist. He does not spend time theorizing on LinkedIn; he writes code, enforces schema hygiene, and unblocks deployment pipelines. His thought leadership is entirely expressed internally through the strictness of his pull request reviews and his architectural mandates. To Denic, working code and pristine database state are the only valid forms of professional communication.

*(Note regarding personal projects: The prompt requested details on an offline Android voice assistant. Forensic analysis of his LinkedIn profile clarifies that this project belongs to a colleague, Vlada Radivojevic, and the EvaluMate math platform belongs to Robert Dumitru. Denic's personal projects are strictly focused on the AIBG video game architecture and CV management systems \[23\]).*

### **4\. Technical Decisions and Architectural Preferences**

Denic’s technical preferences define the absolute boundaries of what Matta will integrate. The intelligence explicitly identifies him as a judge who severely penalizes "hand-wavy architecture" and mandates strict adherence to schema cleanliness and idempotency \`\`.

| Architectural Mandate | Technical Reality & Forensic Evidence |
| :---- | :---- |
| **Idempotency Maximalism** | Factory networks drop packets constantly due to heavy machinery interference. If an edge node tells the cloud "Part X is defective," network retries must not count Part X twice. Denic's reliance on Postgres and Celery indicates he engineers heavily around distributed task queuing and robust state reconciliation \[intel.md: All open Matta job listings\]. |
| **Strict Schema Validation** | The explicit inclusion of Pydantic alongside FastAPI in the Matta stack is the hallmark of a CTO who enforces rigid data validation at the application boundary \[intel.md: All open Matta job listings\]. He will not tolerate dynamically typed, unstructured data flows between the edge and the cloud. |
| **Low-Latency Video Streaming** | His requirement for WebRTC and WebSockets confirms that Matta’s agents operate on live, unbuffered video streams \[3\]. Architectures must process or route these streams without introducing frame latency. |
| **End-to-End Type Safety** | His deep background in TypeScript (Codemancy Studio) \[23\] heavily influences his frontend/backend integration philosophy, demanding strict typing from database to UI. |

### **5\. Communication Style and Apparent Decision-Making Patterns**

Denic’s communication is highly technical, binary, and devoid of marketing rhetoric \`\`. He evaluates external vendors, software architectures, and internal engineers strictly on their ability to demonstrate operational, scalable code. His decision-making pattern follows a strict engineering hierarchy: reliability first, latency second, feature completeness third. He is likely to reject any tool or platform that obscures underlying complexity (such as visual low-code tools) in favor of deterministic, code-first infrastructure that he can version-control, audit, and trace via Sentry/New Relic \[intel.md: All open Matta job listings\].

### **6\. Recommended Outreach Angles**

Outreach destined for Denic must bypass the commercial value proposition entirely and speak directly to his architectural pain points and engineering realities.

* **Lead with Schema and State Management**: Explicitly detail how your solution handles idempotent operations across distributed, occasionally connected edge networks. Mentioning strict Pydantic payload validation, TypeScript generation from OpenAPI specs, and SQLAlchemy database transaction rollbacks will immediately signal deep architectural alignment \`\`.  
* **Address WebRTC and Video Streaming Latency**: Acknowledge the extreme difficulty of maintaining synchronous WebRTC video streams across isolated, noisy factory networks \[intel.md: All open Matta job listings\]. Proposing optimizations for edge video encoding, or zero-copy memory architectures for computer vision inference, maps directly to his daily operational challenges with the Sentry and Gauge products \[3\].  
* **Provide Technical Proof, Not Pitches**: Outreach to Denic should bypass sales decks and include links to GitHub repositories, API documentation, and systems architecture diagrams. Let the schema do the talking \`\`.

### **7\. Red Flags / Things to Avoid**

* **Vague Integration Promises**: Using terms like "seamless integration" without providing the specific REST API schemas, WebSocket protocols, or authentication mechanisms (e.g., JWT) will result in immediate rejection \`\`.  
* **Non-Idempotent Architectures**: Any system that relies on exactly-once delivery guarantees (which are practically impossible in hostile factory networks) rather than robust at-least-once idempotent design will fail his technical review \`\`.  
* **Ignoring the Edge Constraint**: Pitching solutions that require constant, high-bandwidth cloud connectivity ignores the reality of Matta's operational environment. Proposals must accommodate fully air-gapped or intermittently connected edge inference \[3\].

## ---

**Ecosystem and Investor Intelligence Context (The Strategic Substrate)**

To effectively engage the founders of Matta, outreach and architectural proposals must be contextualized within the strategic macroeconomic pressures exerted by their board and lead investors. The $14M Seed round was syndicated among highly opinionated, philosophically distinct venture capital entities. Each of these entities imposes specific macroeconomic and strategic expectations upon Brion, Pattinson, and Denic, which ultimately dictate the company's product roadmap and procurement thresholds \[4, 5\].

Understanding the composition of this cap table reveals *why* Matta is making specific technical choices, and provides the ultimate leverage for aligning external proposals with the board's mandates.

### **Giant Ventures and the "British Dynamism" Mandate**

Giant Ventures (the Pre-Seed Lead and Seed Co-Lead), represented by Madelene Larsson, operates under a highly specific and publicly articulated investment thesis termed "British Dynamism" and the "European Stack" \[25, 26\]. The firm’s public commentary explicitly positions Matta not just as a software company, but as a critical sovereign asset necessary to solve "national priorities like climate change, energy resilience and healthcare," specifically citing Matta's ability to enable "low-carbon advanced manufacturing" \[25\].

Giant Ventures' founding partners, Cameron McLain and Tommy Stadlen, aggressively advocate for European technological sovereignty and reshoring industrial capacity to escape a "national malaise" \[25, 26\]. They are structurally opposed to the dominance of US-based hyperscalers controlling the foundational layers of AI, writing extensively on how horizontal platforms (like OpenAI) lack defensible moats beyond pure capital scale \[26\]. They view Matta as possessing a true moat: physical data generation and proprietary hardware-software integration on the factory floor \[26\].

**Operational Implication for Outreach**: Aligning proposed architectures with European data sovereignty will heavily resonate with the Giant Ventures mandate. Proposing edge compute architectures that can operate completely localized on the factory floor—ensuring GDPR compliance and preventing proprietary manufacturing IP from leaking to generic cloud providers—directly services Giant's geopolitical investment thesis.

### **Lakestar and the Digitalization of Legacy Assets**

Lakestar, the Seed Lead, is represented by Akis Bratsos, a partner heavily focused on automation, infrastructure software, and healthcare cross-pollination \[27, 28\]. Bratsos's thesis revolves around the rapid digitalization of deeply entrenched, physical legacy industries. His public commentary regarding Matta specifically praises the team's "transformative approach to rapidly training factory-ready AI with minimal data" and their "fast time to value that is rare in the sector" \[4, 5\].

Unlike consumer software, enterprise industrial sales cycles typically take 12 to 18 months. Bratsos has capitalized Matta specifically because they break this paradigm. The ability to achieve 99% defect detection with only 10 minutes of training data is the financial crux of Lakestar's bet \[15\].

**Operational Implication for Outreach**: Any vendor or architectural proposal targeting Matta must index heavily on speed-to-deployment and minimal friction. If a proposed database architecture or cloud integration adds weeks to Matta's deployment timeline, it violates Lakestar's core thesis. Conversely, technologies that support Matta's two-week factory go-live tempo and zero-calibration mandate will be viewed as mission-critical \[3, 15\].

### **1st Kind (The Peugeot Family Office) and Industrial Ruggedization**

The participation of 1st Kind, the investment vehicle of the Peugeot automotive family, injects deep, centuries-old industrial legacy into Matta's cap table \[29\]. Spearheaded by Sophia Martin and Ulysse Laroche, the fund explicitly focuses on the "Tech & Industry Alliance" spanning "atoms and bits" \[29\]. They leverage over 200 years of physical manufacturing expertise—from steel crinolines to mass-produced automobiles—to support founders building "durable, globally recognized products" \[29\].

The presence of 1st Kind ensures that Matta cannot pivot into a pure software-as-a-service play; they are structurally obligated to deliver highly robust physical solutions capable of surviving automotive and heavy industrial environments. 1st Kind provides Matta with direct gateway access to the European industrial network, but in exchange, they demand automotive-grade reliability \[29\].

**Operational Implication for Outreach**: Any proposed engineering stack or hardware component must demonstrate ruggedization and extreme fault tolerance suitable for tier-one automotive suppliers \[4\]. Theoretical uptime is irrelevant; the architecture must survive the thermal, electromagnetic, and vibrational realities of a stamping plant or an injection molding line.

| Investor Entity | Key Representative | Stated Thesis / Mandate | Implication for Matta's Technical Architecture |
| :---- | :---- | :---- | :---- |
| **Giant Ventures** | Madelene Larsson \[25\] | British Dynamism, European Tech Sovereignty, low-carbon manufacturing \[25\]. | Must prioritize localized data sovereignty, edge inference, and measurable reductions in physical waste (emissions) \[2\]. |
| **Lakestar** | Akis Bratsos \[27\] | Digitalization of legacy sectors, fast time to value \[5\]. | Must prioritize zero-calibration deployment, ultra-fast data labeling, and self-supervised models that go live in weeks \[3\]. |
| **1st Kind** | Sophia Martin, Ulysse Laroche \[29\] | Deeptech industrial applications, bridging atoms and bits, European craftsmanship \[29\]. | Must maintain automotive-grade hardware ruggedization and absolute reliability in hostile physical environments. |

## **Strategic Synthesis for Procurement and Outreach Posture**

The forensic profile of Matta reveals a highly asymmetric organization operating under intense scaling pressures. They possess the elite academic pedigree of Cambridge and MIT via Dr. Sebastian Pattinson and Douglas Brion \[1, 7\], the operational intensity of Balkan edge-engineering via Damjan Denic \[23\], and the heavy capitalization of top-tier European deep-tech venture capital \[28, 29, 30\].

Any successful technical proposal, vendor outreach, or architectural partnership must successfully navigate a rigorous, three-stage validation gauntlet, mapped directly to the psychological profiles of the leadership triad:

1. **The Brion Filter (Commercial & Physical Pragmatism)**: Does this technology accelerate deployment to two new factories a month? Does it natively handle evidential uncertainty? Does it solve a gritty, shop-floor reality, or is it just another dashboard? \[4, 17\].  
2. **The Pattinson Filter (Cyber-Physical Trust & First Principles)**: Is the underlying mathematics scientifically rigorous? Does the architecture respect the physical and material properties of the manufacturing environment (viscoelasticity, thermal dynamics)? Does it guarantee cyber-physical trust and prevent catastrophic failure states? \[1, 2\].  
3. **The Denic Gatekeeper (Execution & Idempotency)**: Is the data schema strictly typed via Pydantic? Is the network behavior perfectly idempotent? Can the system handle high-frequency WebRTC video data over unreliable, air-gapped edge networks without dropping state or crashing the event loop? \`\`.

Architectures that attempt to abstract away the physical reality of the factory floor, rely on black-box generative AI outputs without confidence intervals, or fail to account for intermittent network topologies will be systematically rejected across all three profiles. Success requires a hyper-specific, physical-first, idempotent engineering pitch that speaks directly to the reality of manufacturing the impossible.

#### **Works cited**

1. accessed December 31, 1969, [https://www.imveurope.com/interview/doug-brion-matta-vision-ai-manufacturing](https://www.imveurope.com/interview/doug-brion-matta-vision-ai-manufacturing)  
2. "Der schwierige Teil ist, es z... \- Startup Insider \- Apple Podcasts, accessed May 7, 2026, [https://podcasts.apple.com/bo/podcast/der-schwierige-teil-ist-es-zum-laufen-zu-bringen-14/id1511786820?i=1000742300113](https://podcasts.apple.com/bo/podcast/der-schwierige-teil-ist-es-zum-laufen-zu-bringen-14/id1511786820?i=1000742300113)

═══════════════════════════════════════════════════════════════
END FILE: Matta_Dossier.md
═══════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════
FILE: Brief_Audit.md
PURPOSE: Prior Gemini 1F-lite audit on the killed Brief architecture. Included for methodological self-calibration per the Anti-Rubber-Stamp Directive — this audit had three documented primary-source misses that the present audit must not replicate.
═══════════════════════════════════════════════════════════════

# **Brief\_Audit.md**

## **Architectural Baseline and Audit Scope**

The proposed transition of the Matta software architecture from the previously decommissioned 1F-red infrastructure to the newly conceptualized pre-deployment factory scoping application—internally designated as "The Brief"—represents a critical inflection point in the organization's commercial trajectory. Matta, a London-based industrial artificial intelligence enterprise, has recently emerged from stealth operations fortified by a $14 million seed funding round.1 This capital injection was led by Lakestar and Giant Ventures, with strategic participation from a consortium of high-profile investors including 1st Kind (the Peugeot family office), InMotion Ventures, RedSeed VC, Unruly Capital, and Boost VC.1 The core technological proposition of the organization revolves around the establishment of "factory sentience"—a paradigm designed to digitize the tacit knowledge of experienced human engineers and recover the estimated 20% of value typically lost within existing manufacturing processes.1

To achieve this, Matta deploys a suite of four distinct industrial agents: Sentry for unsupervised defect detection, Gauge for automated parts counting and kitting, Tally for micron-accurate dimensional measurement, and Trace for high-speed part traceability.1 These systems operate directly on the factory floor utilizing edge-compute hardware, unsupervised machine learning, and self-supervised computer vision.1 The rapid scaling of this deployment model—currently operating at a velocity of approximately two new factories per month with a pipeline exceeding 400 deployments—demands an extraordinarily efficient pre-sales and pre-deployment scoping mechanism.1 The Forward Deployed Engineers (FDEs) tasked with integrating this hardware and software into diverse, complex, and high-stakes industrial environments must possess deep, actionable intelligence regarding a prospect's legacy capital expenditure (CapEx), specific defect rates, and operational latency constraints prior to committing to an installation.1

The architectural premise of "The Brief" is that a stateless, pre-deployment factory scoping sidecar will accelerate this discovery phase and serve as a labor multiplier for the executive and engineering teams. However, allocating engineering resources to build this specific software architecture requires absolute certainty that its functional affordances align perfectly with the target organization's operational realities. A stateless sidecar is fundamentally optimized for immediate, ephemeral, low-latency interactions; it does not retain memory, construct longitudinal context, or support extended, multi-touch enterprise procurement cycles. If the foundational assumptions regarding how the Chief Executive Officer, Douglas Brion, and the FDEs interact with prospective clients are flawed, "The Brief" will introduce systemic operational friction rather than serving as the intended high-leverage utility.

This document presents an exhaustive forensic examination of the four load-bearing commercial and operational claims underpinning the proposed architecture of "The Brief." The analysis relies strictly on primary source materials, prioritizing the target organization's proprietary marketing copy, the founders' public statements, verbatim job descriptions (JDs), and relevant press coverage. The objective of this audit is to adjudicate the veracity of these claims, identify potential ontological or architectural vulnerabilities, and issue a definitive verdict on whether the engineering teams should proceed to the Phase 1 Specification, tighten the framing, or escalate the architecture back to 1F-red for comprehensive re-adjudication.

## **Claim 1 Adjudication: Lead Generation Context and the Trade-Show Hypothesis**

The first load-bearing claim dictates the primary contextual environment in which the software will be utilized. It posits that the trade-show context serves as the highest-leverage use case for an automated FDE discovery sidecar at Matta. This operational assumption is the foundational justification for a stateless architecture: if the primary lead generation engine relies on high-volume, fleeting interactions on a bustling exhibition floor, the application must be heavily optimized for mobile deployment, immediate response generation, and minimal manual data entry. To substantiate this hypothesis, an exhaustive forensic analysis was conducted against the Chief Executive Officer's public calendar, references to major industrial trade shows (specifically searching for industry staples such as MACH 2026 or Southern Manufacturing), and the comparative volume of inbound channels, specifically scrutinizing LinkedIn direct messages and organic waitlist volume.

An exhaustive review of the available primary materials yields a complete absence of empirical evidence supporting the trade-show hypothesis. A targeted search for "Southern Manufacturing," "MACH 2026," and generic trade show attendance records within the intelligence corpus returns negative results.1 There is no quantitative data or qualitative narrative indicating that physical booth presence functions as the anchor for lead acquisition. While Douglas Brion's professional history mentions networking at academic and industry symposia as an opportunity to "establish relationships for future collaborations" 1, this standard professional networking activity does not constitute the primary pipeline engine for a rapidly scaling enterprise that recently secured $14 million in seed capital.1

Conversely, the data overwhelmingly supports a massive, asynchronous digital inbound volume, heavily correlated with LinkedIn outreach, public professional networking, and organic digital network effects. The Chief Executive Officer's public statements explicitly quantify an overwhelming organic pipeline that renders aggressive outbound or trade-show lead generation functionally unnecessary at this stage of the organization's growth. In early 2026, a public announcement confirmed the sheer scale of this inbound momentum with the verbatim statement: "we have 100s of factories in the pipeline so don’t be shy. there are not a finite number of places".1 Furthermore, the organization's deployment capacity is currently vastly outpaced by its inbound demand. Public statements regarding the fulfillment rate provide the following verifiable metric: "we’re deploying to around two factories a month and have a multi-year waitlist at the moment".1

The existence of a confirmed "multi-year waitlist" fundamentally invalidates the mechanical requirements of a stateless, pre-deployment factory scoping sidecar built for trade shows. The architectural implications of this reality are profound and must be mapped meticulously to understand the failure of the initial claim.

### **Architectural Alignment Analysis: Trade Show vs. Digital Inbound**

| Operational Vector | Trade-Show Hypothesis (Claim 1\) | Verified Digital Inbound Reality | Architectural Implication for "The Brief" |
| :---- | :---- | :---- | :---- |
| **Pipeline Status** | High urgency to capture and qualify cold leads in real-time. | "we have 100s of factories in the pipeline" and a "multi-year waitlist".1 | Lead capture is not the bottleneck; pipeline prioritization and deep qualification are the true constraints. |
| **Interaction Medium** | Physical, ephemeral, face-to-face interaction (under 5 minutes). | Asynchronous digital communication (LinkedIn, website form-fills, direct inquiries).1 | Tool must support asynchronous ingestion of complex digital data (schematics, CapEx reports) rather than real-time conversational parsing. |
| **Data Persistence** | Stateless; interactions end when the prospect leaves the booth. | Stateful; prospects remain on a waitlist for months or years before deployment.1 | A stateless sidecar will fail to maintain longitudinal context across a multi-year enterprise sales cycle. |
| **Primary Inbound Channel** | Physical events, MACH 2026, Southern Manufacturing. | Founder network, Giant Ventures PR, LinkedIn announcements.1 | The "Magic Moment" occurs at a desktop during pre-call prep, not on a mobile device on an exhibition floor. |

When an enterprise operates with hundreds of qualified leads backlogged, the primary commercial bottleneck is resource allocation and deep technical qualification. A stateless, immediate-response mobile application is theoretically designed to lower the barrier to entry for cold leads and provide rapid talking points for a sales representative. However, Matta currently faces a surplus of demand.1 Therefore, the highest-leverage use case for "The Brief" is not rapid lead generation on a trade-show floor, but rather the rigorous, asynchronous deep-dive analysis of complex inbound requests.

If the primary inbound channel relies on LinkedIn direct messages, website form fills, and the digital broadcast strategy utilized by the founders—leveraging their prestigious academic pedigrees from the University of Cambridge and Imperial College London 1—the true Magic Moment for a Forward Deployed Engineer scoping tool occurs at a dedicated desktop environment. This environment allows the FDE to utilize the software to parse complex manufacturing schematics, evaluate legacy coordinate measuring machine (CMM) infrastructure, and conduct deep-web reconnaissance on prospective clients' existing defect rates.1 Architecting a stateless mobile sidecar strictly based on the trade-show hypothesis would result in a severely over-engineered solution for a non-existent bottleneck, while simultaneously failing to provide the deep analytical rigor required to effectively triage a multi-year waitlist.

Verdict: ❌ Fails. The trade-show context is definitively not the highest-leverage anchor. The organization is currently managing a multi-year waitlist generated via robust asynchronous digital inbound channels, rendering a stateless booth-scoping sidecar architecturally misaligned.

## **Claim 2 Adjudication: Temporal Dynamics and the "60-Seconds" Conflation**

The second load-bearing claim dictates the temporal interaction model of the software application, asserting that the "60-seconds-at-the-booth" use case is an operational reality rather than a "24-hours-after" asynchronous workflow. This claim suggests that the Chief Executive Officer, Douglas Brion, alongside the Forward Deployed Engineering team, executes rapid, in-the-moment discovery and requires instantaneous pre-sales context to capitalize on fleeting interactions. Validating this claim requires definitive evidence of the organization's internal pre-call preparation rituals, an understanding of the cognitive load inherent in their highly technical sales motion, and a precise examination of the FDE workflow as they interface with prospective manufacturing environments.

A rigorous forensic examination of the entire intelligence corpus reveals a critical semantic conflation embedded within the initial architectural premise: the speed of Matta's *industrial hardware and software products* has been incorrectly mapped onto the speed of their *enterprise sales and procurement motion*. The primary materials contain abundant references to extreme velocity, but these metrics exclusively describe the performance of the machine learning models and edge-compute hardware upon deployment.1

The product velocity metrics are unequivocally verified. The Sentry defect detection platform is verified to catch quality issues "the moment they happen" rather than waiting for end-of-line inspections.1 The Tally dimensional measurement tool achieves micron accuracy "in seconds".1 The Trace part traceability system allows highly complex audit questions to be answered "in seconds instead of hours".1 Furthermore, the unsupervised learning capabilities of the core foundation models are highly accelerated; the system "learns any production line within days," with the verbatim claim that "Their fastest learning was just 5 minutes".1 In a controlled, highly publicized demonstration involving a Halloween LEGO pumpkin, the fully unsupervised model trained itself for quality inspection in "less than 15 minutes".1

However, when isolating the human element of the sales and pre-deployment discovery process, a comprehensive search for the exact phrases "60 seconds," "at the booth," "pre-call prep," or "Magic Moment" in the context of human workflow yields zero corroborating evidence.1 There is no indication, within founder portfolios, LinkedIn posts, or corporate marketing collateral, that the Chief Executive Officer or the FDEs consume pre-sales context "in the moment" during physical interactions.1

To the contrary, the verified operational realities of the Forward Deployed Engineer role mandate deep, extensive, and highly technical preparation that inherently precludes a 60-second scoping framework. The verbatim description of the FDE responsibilities notes that an average week involves "visiting factories for plane wings/soup tins/electronics… you name it".1 The primary task upon arrival is to "help us install sensors, AI models, and our factory nervous system across UK, EU, and US factories in EVERY sector".1

### **Temporal Dynamics: Product Velocity vs. Human Procurement Velocity**

| Operational Domain | Stated Velocity Metric | Verbatim Evidence | Viability of "60-Second" Scoping |
| :---- | :---- | :---- | :---- |
| **Defect Detection (Sentry)** | Instantaneous | Catches issues "the moment they happen".1 | N/A (Machine operation) |
| **Model Training (Foundation)** | Minutes to Days | "Their fastest learning was just 5 minutes".1 | N/A (Machine operation) |
| **Audit Traceability (Trace)** | Seconds | Answers audit questions "in seconds instead of hours".1 | N/A (Machine operation) |
| **FDE Deployment Prep** | Highly Complex / Asynchronous | "visiting factories for plane wings... nuclear submarines".1 | **Impossible.** Procurement for highly regulated environments requires deep diligence. |
| **Founder Technical Philosophy** | Methodical / Risk-Averse | Insists AI models must "know when they are uncertain".1 | **Impossible.** "Uncertainty quantification" cannot be assessed in a 60-second booth interaction. |

The integration of a "factory nervous system" into environments as highly regulated, sensitive, and critical as those manufacturing nuclear submarines, aerospace components, or global electronics 1 represents a massive capital and operational risk for the prospective client. Procurement cycles in these sectors are notoriously complex, often spanning multiple quarters and requiring extensive cybersecurity audits, physical site inspections, and integration testing. Furthermore, Douglas Brion's documented leadership philosophy specifically emphasizes "uncertainty quantification" in AI, explicitly insisting that industrial models must know when they are uncertain to avoid damaging multi-million-dollar heavy equipment.1 Evaluating a prospect's operational capacity, network topology, lighting conditions, and legacy CapEx to safely integrate such models demands asynchronous, methodical analysis.

Therefore, the "60-seconds-at-the-booth" use case is highly aspirational and fundamentally disconnected from the immutable physics of enterprise industrial AI sales. A Forward Deployed Engineer, such as the currently employed Jake Moll 1, cannot accurately assess the nuanced requirements of a polymer extrusion plant or a casting line in a 60-second interaction. The true Magic Moment for "The Brief" will inevitably occur 24 to 48 hours prior to a factory visit or executive alignment call, when the software aggregates disparate data sources to provide a comprehensive, stateful, deep-vertical dossier on the target facility. Architecting for instantaneous consumption would artificially constrain the depth of the intelligence provided to the FDEs, neutering the sidecar's primary utility and increasing the risk of deployment failure.

Verdict: ❌ Fails. The "60-seconds-at-the-booth" use case is entirely unsupported by the evidence. The speed metrics cited in the organization's public footprint relate exclusively to the performance of their edge AI agents and unsupervised learning models, not the human pre-sales motion, which requires complex, asynchronous, and stateful diligence.

## **Claim 3 Adjudication: Ontological Integrity of the Six-Vertical Knowledge Graph**

The third load-bearing claim pertains to the foundational data architecture and the underlying ontology of "The Brief." It asserts that a strictly defined six-vertical knowledge graph—comprising polymer extrusion, metal casting, additive manufacturing, food and beverage (F\&B) bottling, electronics assembly, and aerospace composites—accurately covers Matta's named customer base and stated deployment patterns. The claim explicitly requires validation against specific customer mentions and facility terminologies extracted from cleaned intelligence, including the entities "Bowers & Wilkins," "Caracol AM," "Cummins," alongside references to "polymer plants," "casting lines," "bottling halls," and a "global drinks brand."

An exhaustive cross-reference of the specified verticals against the primary intelligence yields a highly fragmented validation landscape. While the macro-categories of the proposed knowledge graph map effectively to the organization's target markets, specific named entities and specialized terminologies exhibit critical coverage gaps and potential hallucination risks. The structural alignment between the proposed knowledge graph and the verified deployment reality is detailed in the comprehensive mapping below.

### **Knowledge Graph Coverage and Ontological Mapping Analysis**

| Proposed Vertical Node | Target Entity / Specific Term | Primary Source Verification Status | Verbatim Evidence & Contextual Reality |
| :---- | :---- | :---- | :---- |
| **Polymer Extrusion** | "polymer plants" | ✅ Verified | System is explicitly described as operational in "polymer plants".1 |
| **Metal Casting** | "casting lines" | ✅ Verified | Verbatim confirmation that the AI system is already running in "casting lines".1 |
| **Additive Manufacturing** | "Caracol AM" | ✅ Verified | Verbatim confirmation of active deployment with global client "Caracol AM".1 |
| **Electronics Assembly** | "Bowers & Wilkins" | ✅ Verified | Verbatim confirmation of active deployment with global client "Bowers & Wilkins".1 |
| **F\&B Bottling** | "bottling halls" | ✅ Verified | Verbatim confirmation that the system is running in "bottling halls".1 |
| **F\&B Bottling** | "global drinks brand" | ⚠️ Not Verified (Implicit) | The exact phrase is completely absent. Related environments explicitly mentioned include "soup tins" and "gourmet cheese".1 |
| **Aerospace Composites** | "aerospace composites" | ⚠️ Not Verified (Implicit) | The term "composites" is absent. General deployment in "aerospace" and "plane wings" is confirmed.1 |
| **(Unspecified Node)** | "Cummins" | ❌ Failed (Hallucination) | The entity "Cummins" is entirely absent from Matta's primary deployment footprint and marketing collateral.1 |

The forensic mapping indicates that four of the core terminologies perfectly align with the organization's verified public footprint. The industrial AI system is indisputably running in "polymer plants, casting lines, bottling halls and with global clients like Caracol AM and Bowers & Wilkins".1 The inclusion of the aerospace sector is broadly validated by active factory visits for "plane wings" and general deployments into the aerospace industry.1

However, the knowledge graph exhibits critical hallucinations and structural assumptions regarding specific proprietary entities. The name "Cummins" does not exist in any verified Matta marketing copy, founder statements, or public client rosters.1 A deeper investigation into the extraneous data reveals that while external academic literature indicates independent simulation research utilizing digital twins has occurred in proximity to Cummins Filtration (now Atmus Filtration Technologies) 2, and other research mentions Cummins in the context of additive manufacturing 3, there is zero demonstrable commercial or technical linkage to a Matta AI deployment. Hardcoding "Cummins" into a pre-deployment sidecar's evaluation matrix would introduce non-verifiable ghost data into the FDE scoping process, fundamentally poisoning the foundational context of the application.

Similarly, the specific phrase "global drinks brand" is entirely absent from the intelligence, despite the clear validation of the broader food and beverage sector through explicit references to "soup tins," "gourmet cheese," and "bottling halls".1 Relying on specific but unverified colloquialisms in the knowledge graph architecture creates rigid query limitations.

Furthermore, the aerospace vertical presents a semantic vulnerability: while "plane wings" are frequently constructed using advanced materials, the rigid specification of "aerospace composites" as the exclusive ontological node risks alienating adjacent aerospace manufacturing processes. The machining of titanium alloys or standard aeronautical metallurgy are equally viable targets for the Sentry defect detection and Tally metrology agents, especially given Douglas Brion's focus on deep learning enabled error detection.1

The architectural implication of these gaps is severe. A pre-deployment scoping sidecar reliant on a strictly defined six-vertical knowledge graph that hardcodes unverified entities will experience severe routing failures and context collapse during the extraction and synthesis phase. If the software is prompted by an FDE to retrieve historical deployment context for "Cummins" to aid in closing a similar heavy-machinery client, the system will either fail to retrieve data or hallucinate a deployment narrative based on scraped academic papers.2 The knowledge graph must be significantly broadened to reflect the actual verified sector diversity—which explicitly includes "nuclear submarines," "waterproof coats," and "gourmet cheese" 1—rather than artificially constraining the ontology to a rigid, partially inaccurate six-pillar model.

Verdict: ⚠️ Holds Partially. The macro-verticals (polymer, casting, additive, F\&B, electronics, aerospace) are fundamentally sound and heavily supported by the evidence. However, the specific inclusion of "Cummins," "global drinks brand," and "aerospace composites" as load-bearing anchors is unverified and introduces a severe hallucination risk that compromises the ontological integrity of the scoping tool.

## **Claim 4 Adjudication: Operational Utility and the "Special Projects" Multiplier**

The final load-bearing claim evaluates the organizational psychology, strategic hiring trajectory, and cognitive bottlenecks of the Matta executive team. It posits that the founders, Douglas Brion and Damjan Denic, would find a software sidecar profoundly useful for pre-sales discovery, specifically because they are actively hiring a human "Special Projects" role explicitly described as "helping close customer deals" and characterized as "probably our most important hire".1 The core tension to be resolved is whether "The Brief" acts as a redundant layer of software that competes with this new strategic human hire, or functions as a highly leveraged labor multiplier that perfectly aligns with the founders' operational philosophy. To adjudicate this, the verbatim job description for the "Special Projects" role must be meticulously analyzed against the proposed capabilities of the pre-deployment sidecar.

The primary intelligence confirms unequivocally that Matta is actively recruiting for a pivotal, high-visibility operational role titled "Special Projects." The verbatim job description explicitly defines the magnitude and strategic weight of the position: "This is probably our most important hire and you should be up for learning about and diving into anything".4 The responsibilities outlined are heavily weighted toward executive-level synthesis, commercial execution, and high-stakes problem solving, requiring the candidate to be at the heart of the organization by "steering long-term strategy, supporting fundraising efforts, and helping close customer deals".4

To determine if a stateless sidecar scoping tool augments or impedes this human role, one must examine the specific cognitive requirements and desired archetypes outlined by the founders. The job description mandates that the candidate possess the ability to "distil the team's often technical, complex, and sometimes chaotic/scatter-brain ideas into concise, polished points that resonate with diverse audiences".4 The ideal candidate is further characterized using a highly specific cultural archetype: "A Gandalf \- the kind of person who quietly works their magic behind the scenes, making sure everything runs seamlessly".4

This explicit desire for a commercially minded human operator capable of synthesizing "chaotic/scatter-brain ideas" into "concise, polished points" reveals a fundamental organizational pain point. The technical leadership at Matta—comprising individuals with advanced academic degrees and fellowships from the University of Cambridge, MIT, Microsoft, and Imperial College London 1—is generating highly complex, physics-based foundation models for manufacturing. The translation of this deep technical capability into commercial, pre-sales collateral that resonates with traditional manufacturing executives requires immense cognitive labor.

### **"Special Projects" Role Synthesis vs. Sidecar Capabilities**

| Required Skill/Attribute (Verbatim JD) | Human Operator Capacity | "The Brief" Software Capability (Proposed) | Assessment of Utility |
| :---- | :---- | :---- | :---- |
| "distil... chaotic/scatter-brain ideas" 4 | High, but time-consuming and cognitively taxing. | Instantly ingests and structures complex technical data into standardized formats. | **Multiplier.** Automates the low-level structuring, freeing human for high-level refinement. |
| "helping close customer deals" 4 | Strategic relationship building, negotiation. | Aggregates target company CapEx, defect histories, and factory schematics. | **Multiplier.** Provides the ammunition required for the human to execute the closing motion. |
| "managing the rhythm of the business" 4 | Requires deep, persistent contextual awareness over time. | Stateless by design; resets after every interaction. | **Conflict.** A stateless tool cannot support a role responsible for long-term business rhythm. |
| "A Gandalf... works magic behind the scenes" 4 | Anticipates needs, maintains long-term strategic vision. | Ephemeral data delivery. | **Conflict.** Magic requires preparation and memory. The tool must be stateful to be truly useful. |

If the "Special Projects" hire is forced to spend their time manually scraping target company reports, compiling factory CapEx histories from disparate databases, and manually aligning Matta's Sentry or Tally capabilities with a prospective client's legacy hardware, they are effectively acting as a data-entry clerk rather than a strategic "Gandalf".4 A pre-deployment scoping sidecar perfectly addresses this bottleneck. By automating the initial ingestion, categorization, and foundational synthesis of a prospect's manufacturing environment, "The Brief" serves as the ultimate labor multiplier. It elevates the human operator from the burden of primary data collation, allowing them to focus entirely on the high-leverage activities requested in the job description: "bounc\[ing\] ideas around and turn\[ing\] them into reality," and executing the strategic alignment necessary for "helping close customer deals".4

However, the claim only holds partially due to the severe limitations of a purely *stateless* architecture in this specific commercial context. The job description places immense value on relationship continuity, strategic thinking, and the ability to partner closely with the CEO over the long term.4 A stateless sidecar—which by definition retains no memory of previous interactions, client objections, or cumulative pipeline knowledge—is antithetical to the responsibilities of an executive tasked with "managing the rhythm of the business".4

To truly serve as a multiplier for this specific role, the scoping tool must possess stateful memory. It must allow the human operator to build persistent, evolving dossiers on prospective clients as they slowly move from the "multi-year waitlist" 1 through the complex deployment pipeline. Furthermore, the founders' technical philosophy emphasizes deep human intuition. The entire premise of Matta's mission to create "factory sentience" is to capture the "tacit knowledge" of experienced engineers—the human intuition of sensing when a machine is exhibiting a flaw before anyone else.1 Therefore, any software tool introduced into their internal workflow must respect the supremacy of human judgment. The sidecar must be positioned strictly as an augmentation layer that presents formatted intelligence, rather than an automated decision-engine that attempts to unilaterally qualify or disqualify leads based on rigid stateless parameters.

Verdict: ⚠️ Holds Partially. The fundamental premise that the executive team requires massive computational assistance in synthesizing complex pre-sales data is completely validated by the "Special Projects" job description. The tool is definitively a labor multiplier, not a redundant layer. However, the strict requirement for the tool to be a *stateless* sidecar contradicts the strategic, continuous, and highly persistent nature of the human role it is meant to support.

## **Final Adjudication and 1F-Red Escalation Directives**

The forensic audit of the four load-bearing claims supporting the development of "The Brief" sidecar architecture yields a highly critical assessment of the proposed pre-deployment scoping tool. The foundational assumptions regarding user behavior, sales velocity, ontological requirements, and statefulness are fundamentally misaligned with the verified operational realities of the target organization. The consolidated verdicts are as follows:

* **CLAIM 1:** ❌ Fails. The primary inbound channel is robust, asynchronous, and high-volume, successfully generating a multi-year waitlist via digital networks and founder pedigree. The trade-show anchor hypothesis is entirely unverified and architecturally misleading.  
* **CLAIM 2:** ❌ Fails. The "60-seconds-at-the-booth" scoping timeline incorrectly and dangerously conflates the micro-second performance speed of the deployed AI agents with the complex, methodical, and high-risk reality of enterprise industrial AI procurement and FDE deployment preparation.  
* **CLAIM 3:** ⚠️ Holds Partially. The macro-verticals designated in the knowledge graph are accurate and aligned with Matta's market strategy, but critical node dependencies (specifically "Cummins", "global drinks brand", and "aerospace composites") are non-existent in the verified data, posing severe hallucination and context-collapse risks.  
* **CLAIM 4:** ⚠️ Holds Partially. The software conceptually serves as a highly validated labor multiplier for the critical "Special Projects" role, but the proposed stateless architecture directly contradicts the strategic, continuous, and persistent nature of the required synthesis and pipeline management.

**Directive:** ❌ Escalate back to 1F-red for comprehensive re-adjudication.

The core premise of "The Brief" as a stateless, mobile-optimized, in-the-moment trade-show scoping tool must be abandoned. Matta is actively managing an overwhelming asynchronous pipeline, deploying highly complex physical AI infrastructure into strictly regulated environments, and hiring strategic human operators to manage long-term commercial relationships. Committing engineering resources to build a software architecture based on fleeting booth interactions, hallucinated knowledge graph nodes, and stateless memory will result in systemic failure and low user adoption. The functional specifications must be entirely re-framed, re-scoped, and re-architected around asynchronous, stateful, and deep-vertical pre-deployment research before advancing to Phase 1 Specification.

#### **Works cited**

1. Matta\_Dossier.md  
2. A Digital Twin Approach To Job Shop Scheduling: Simulation And Optimization In Anylogic \- ScholarWorks@UTEP, accessed May 10, 2026, [https://scholarworks.utep.edu/cgi/viewcontent.cgi?article=5352\&context=open\_etd](https://scholarworks.utep.edu/cgi/viewcontent.cgi?article=5352&context=open_etd)  
3. View/Download \- Intelligent Systems Center \- Missouri S\&T, accessed May 10, 2026, [https://isc.mst.edu/media/research/isc/researchinvestigators/2025documents/Liou%203-2025.docx](https://isc.mst.edu/media/research/isc/researchinvestigators/2025documents/Liou%203-2025.docx)  
4. Special Projects in London at MATTA | Apply now\! \- Talents by StudySmarter, accessed May 10, 2026, [https://talents.studysmarter.co.uk/companies/matta/london/special-projects-34977865/](https://talents.studysmarter.co.uk/companies/matta/london/special-projects-34977865/)

═══════════════════════════════════════════════════════════════
END FILE: Brief_Audit.md
═══════════════════════════════════════════════════════════════

