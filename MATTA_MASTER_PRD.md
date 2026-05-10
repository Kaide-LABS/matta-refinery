# MATTA_MASTER_PRD.md

**Kaide Labs — Forward Deployed Engineering Strike Team**
**Target:** Matta (https://www.matta.ai/)
**Author:** Principal Staff Engineer red-team pass on Gemini Step 1A output
**Status:** Internal Kaide Labs document. Sections flagged for scrubbing if reused client-facing.
**Sprint window:** 48–72 hours, Hafeedh (architecture) + Isaac (demo production)

---

## 1. Red-Team Adjudication

This section is non-optional and precedes architecture selection per the SOP. Every Gemini proposal is interrogated against the source intelligence before any selection is made.

### 1.A. DMZ Vanguard (Enterprise IT/Security Questionnaire Automation) — DOWNGRADED

**Verdict:** Do not select as lead pitch.

**Reason 1 — Saturated commercial category.** Security questionnaire automation is not an underserved problem space. Vanta, Drata, SafeBase, Conveyor, Tribble, and Whistic all sell off-the-shelf SaaS in this exact slot, with vendor-pre-trained answer libraries, SOC 2 / ISO 27001 / CAIQ template support, and Slack-native question routing. The price point on these platforms is typically $1k–$5k/month at Matta's stage. Gemini did not articulate a defensible answer to "why Kaide at £10k/month versus Vanta at $2k/month, off-the-shelf." The only defensible answer would be "we customize for industrial AI verticals," but that's a thin moat — Vanta and Drata are already adding industrial-vertical answer libraries. The DMZ Vanguard pitch dies on Doug's first procurement pushback.

**Reason 2 — Wrong bottleneck for Doug's stated pain.** Doug Brion's repeatedly stated bottleneck is FDE deployment velocity: *"We're now deploying into two new factories every month – and we need to move faster"* [intel.md: Doug Brion LinkedIn 12 Feb 2026]. FDEs are not the people filling out IT security questionnaires — that work falls to GTM and SecOps functions, both of which Matta is hiring for separately ("Founding GTM" and "Special Projects" job listings). DMZ Vanguard accelerates SecOps, which is real value but is *not* aligned with the Brion Filter as Gemini claimed. It would land with the Founding GTM hire as a vendor evaluation, not with Doug as a strategic FDE force-multiplier.

**Reason 3 — The "vector similarity ≥95%" framing is pseudo-rigor.** Gemini claims DMZ Vanguard satisfies the Brion Filter on uncertainty quantification because it uses a 95% cosine-similarity threshold on retrieved Matta security ground-truth answers. This is mathematically dishonest. Doug Brion is the author of the PyTorch implementation of *Sensoy, Kaplan & Kandemir (2018), "Evidential Deep Learning to Quantify Classification Uncertainty"* — see his GitHub repo `dougbrion/pytorch-classification-uncertainty` and the companion `dougbrion/pytorch-deep-ensembles` (Lakshminarayanan et al. methodology). Evidential deep learning models *epistemic* uncertainty via Dirichlet priors over class probabilities, separating uncertainty due to lack of evidence from uncertainty due to genuine class ambiguity. Cosine similarity over text embeddings is not even in the same mathematical category — it's a distance metric over an embedding manifold, with no probabilistic interpretation and no separation of aleatoric versus epistemic components. Doug, having authored production PyTorch implementations of both methodologies, will identify this category error within the first ninety seconds of the demo. We are not pitching to a non-technical buyer; we are pitching to the person who literally wrote the uncertainty-quantification code. Gemini's framing as written would get Kaide blacklisted.

### 1.B. Taxonomy Engine (Legacy QC Document → SENTRY/TALLY Parameter Bootstrap) — KILLED

**Verdict:** Replication-adjacent. Disqualified under the Anti-Replication Principle.

**Structural flaw.** Gemini's architectural sketch states explicitly that the Taxonomy Engine "validates extracted tolerance parameters mathematically against the known physical limitations of the TALLY hardware specifications." This requires our sidecar to:
1. Hold a current internal model of TALLY's hardware capabilities, calibration envelopes, and acceptable parameter ranges.
2. Adjudicate whether a customer-derived tolerance can be ingested by TALLY before TALLY itself sees the data.

This is not adjacent to the TALLY parameterization layer — it *is* the TALLY parameterization layer, executed as an external service. Two compounding problems:

First, Damjan would block on the data contract. TALLY's internal parameter schema will change with every firmware revision (the dossier confirms Matta is shipping aggressively, with median employee tenure 0.8 years and continuous research integration via Sebastian's Cambridge CAM group). Every TALLY firmware push would require a coordinated change in our sidecar's validation rules, creating exactly the kind of tightly-coupled vendor relationship the FDE Strike Team model is designed to avoid. Per the Identity file: *"Zero Technical Debt: We hand the client's CTO a fully containerized API endpoint. They plug it in. If they don't like it, they unplug it."* The Taxonomy Engine is a containerized endpoint that Damjan cannot unplug without breaking deployments.

Second, Sebastian would interrogate the failure mode. He has stated publicly (ARIA SoTA Frontiers Night, March 2026) that cyber-physical trust requires deterministic guarantees against catastrophic failure. A sidecar that mis-parameterizes TALLY is a sidecar that can write physically impossible thresholds into a metrology agent that then drives downstream production decisions. The blast radius is "factory ships out-of-spec parts because Kaide's LLM mis-extracted a tolerance from a 1990s PDF schematic." This is the exact failure class Sebastian's "Security of Physical AI Systems" research theme is designed to prevent.

**Even ignoring the structural flaw, the bottleneck is overstated.** FDE onboarding does involve QC document review, but Matta's own marketing positions their few-shot foundation models as requiring "ten minutes of training data" to hit >99% defect detection accuracy [intel.md: Cambridge IfM funding announcement, 10 Dec 2025]. If the MFMs are genuinely few-shot, the legacy taxonomy bootstrap is not the dominant deployment friction Gemini frames it as. The bottleneck Gemini claims is not the bottleneck Matta actually has.

### 1.C. Supply Chain Ledger (External Compliance Generator) — VIABLE BUT NOT LEAD

**Verdict:** Structurally clean. Survives all four filters. Demoted to runner-up on commercial leverage grounds.

The Supply Chain Ledger is the cleanest of Gemini's three. It is purely downstream, webhook-subscribed, externally-facing (regulator audit packs and Tier-1 supplier certificates), and explicitly distinct from internal TRACE traceability. Anti-replication holds. Pattinson's deterministic governance mandate is satisfied because the rules engine adjudicates pass/fail and the LLM is restricted to narrative formatting inside fixed templates. Damjan's idempotency mandate is satisfiable with standard Celery + Redis patterns.

**However, two structural weaknesses Gemini missed:**

First, the Magic Moment is generic. A PDF audit pack materializing in SharePoint is administratively useful but visually undramatic. The demo video has to show 3–6 minutes of compelling theater per the SOP standard. A document materializing in a folder is hard to make exciting on screen. Compare to the Renlo "Voice-to-Deal" demo (a property card materializing in 15 seconds from a voice memo) or the Mundostra "Self-Healing Support" demo (a flight cancellation triaged and resolved in 34 seconds with live agent activity). Compliance PDF generation does not have the same kinetic appeal.

Second, the Supply Chain Ledger sells to a *quality* function inside Matta's customers, not to a *production* function. Matta's customers buy Matta to put cameras on production lines. The buyer of "external regulatory audit packs" is the customer's Quality Manager, not the Plant Manager who signed the Matta contract. The Bridge sidecar (selected below) sells to the Plant Manager and Maintenance Manager — exactly the same buying center that signed Matta. This is a tighter commercial fit.

The Supply Chain Ledger is preserved as a Phase 2 / verbal-only architecture in the demo video tail (per the Identity file's "Adjacent ideas are verbal only" outreach mechanic).

### 1.D. What Gemini Did Not Propose — Independent Evaluation

I evaluated four architectures Gemini did not consider. Three were killed; one was elevated to lead.

**D.1. Pre-Site Discovery / Sales Engineering Sidecar — KILLED.** Internal-facing tool that ingests publicly available factory information plus a customer questionnaire and produces a deployment readiness score with suggested camera count and integration list. Strong on Doug's deployment velocity bottleneck, weak on commercial fit: this scope conflicts directly with the Founding GTM hire's territory ("develop the playbook and scale it properly" per intel.md hiring post). Pitching this is pitching against an incoming hire's mandate, which creates an org-political headwind no matter how clean the architecture is. Killed.

**D.2. Operator Shift Briefing Generator — KILLED.** Auto-generates a "Day 1 Operator Briefing" PDF or Slack message at each shift change, summarizing the previous shift's defect events, root causes, and what to watch for in the incoming shift. Genuinely useful but suffers from the same Magic Moment problem as the Supply Chain Ledger — a briefing materializing in Slack is not visually dramatic, and the buyer (Plant Manager) is buying outcomes, not briefings. Killed for demo purposes; preserved as a verbal Phase 3 mention.

**D.3. Quality Management System (QMS) NCR Generator — RESERVED.** When SENTRY detects a defect crossing threshold, auto-generate a Non-Conformance Report in the customer's QMS (SAP QM, Sparta TrackWise, MasterControl). Strong play for regulated industries (aerospace, medical, automotive). Reserved as the Phase 2 generalization of the lead architecture — the same infrastructure that routes events to CMMS routes events to QMS with a different schema target. Demoed as the verbal expansion in the video tail.

**D.4. CMMS / ERP Work-Order Bridge — ELEVATED TO LEAD.** Subscribes to outbound webhook events from SENTRY and GAUGE; applies a deterministic Action Domain Classifier; generates structured work orders inside the customer's CMMS (SAP PM, IBM Maximo, Fiix, UpKeep) or ERP system. Magic Moment: defect detected on the line → work order materializes in the maintenance team's normal CMMS queue, with parts list, labor estimate, urgency tier, and a Slack/Teams notification with action buttons — total elapsed time under 60 seconds. Selected as the lead pitch. Full justification follows below.

**Patent distinction (US Patent Application 18/846,155).** Doug Brion and Sebastian Pattinson are co-inventors on a patent application titled *"Method, apparatus and system for closed-loop control of a manufacturing process"* (per dossier section on Doug's technical artifacts). This patent must be cleanly distinguished from the CMMS Bridge or the Bridge collapses on first review.

The patent claim — based on its title and on Doug's PhD thesis foundation in *"deep learning enabled error detection and correction for 3D printing"* — covers closed-loop control of *machine parameters* in real time: the system detects an error during fabrication and adjusts the manufacturing equipment's operating parameters (extrusion temperature, flow rate, head speed, etc.) directly, in the millisecond-to-second time scale, with the actuator being the machine itself.

The CMMS Bridge operates in a fundamentally different action space:

| Dimension | Patent Scope (closed-loop machine control) | CMMS Bridge Scope (closed-loop workflow routing) |
|---|---|---|
| Time scale | Milliseconds to seconds | Minutes to hours |
| Actuator | Machine PLC / firmware parameters | Maintenance technician acknowledging a Slack notification |
| Action space | Continuous numeric (temperature, speed, pressure) | Discrete categorical (work order type, urgency tier, technician assignment) |
| Failure mode | Out-of-spec part, in-line correction | Delayed maintenance response, manual escalation |
| Data flow | Closed inside Matta core | Outbound from Matta core to customer's enterprise systems |

These are mathematically and operationally distinct. The patent does not apply to enterprise workflow routing. This distinction is articulated in the FDE Thesis below and must be a verbal talking point in the pitch.

### 1.E. Citation Hygiene Audit

Gemini's Target Brief contains five citations with documented integrity issues. The PRD does not depend on any of them; alternative primary-source citations are used throughout.

**Citation 12/13 — "Controlled Agentic AI Systems: A Governance-Driven Architecture for Auditable and Reproducible Decision Pipelines" (preprints.org).** Gemini attributes this framework to Sebastian Pattinson and uses it to anchor the Pattinson Filter's central claim that *"governance is embedded directly into the decision pipeline as a deterministic operator."* The dossier did not surface this paper. Pattinson's verified Cambridge CAM group page lists three research themes: Learning Manufacturing Systems, Digitally Tailored Medical Devices, and Security of Physical AI Systems — none of which are "Controlled Agentic AI Systems." Pattinson's verified ICRA 2026 paper is *"IDfRA: Self-Verification for Iterative Design in Robotic Assembly"*, a different framework. Authorship of the cited preprint cannot be verified against Pattinson's Google Scholar profile or his Cambridge institutional page. **Verdict: very likely a semantic graft from an unrelated preprint with similar-sounding framework name. The Pattinson Filter as Gemini formulated it collapses.** This PRD rebuilds the Pattinson framework on Pattinson's verified ARIA SoTA Frontiers Night presentation on cyber-physical trust and his Cambridge CAM group's stated research theme on "Security of Physical AI Systems."

**Citation 18 / 22 — "Manually completing a security questionnaire takes 20 to 40 hours" / "Automating security questionnaires can reduce operational costs by up to 30%" (tribble.ai blog).** Tribble is a security questionnaire automation vendor — they directly profit from the perception that this pain is severe. Citing a vendor's marketing blog as the load-bearing statistic for the entire DMZ Vanguard recommendation is methodologically unsound. **Verdict: tainted source.** This contributed to the DMZ Vanguard downgrade above.

**Citation 20 — SMT Magazine, September 2015, cited as the source for 1st Kind's "automotive-ruggedization" investment thesis.** 1st Kind did not exist as a Matta investor in 2015 (Matta was founded in 2022, 1st Kind invested in the December 2025 seed round). A 2015 trade magazine cannot be the primary source for a 2025 venture capital thesis. **Verdict: temporally impossible. Likely fabricated attribution.** This PRD anchors the 1st Kind investor mandate on the verified intel.md content showing 1st Kind's connection to the Peugeot family office and Doug's reported Paris meeting with Sophia Martin and Ulysse Laroche.

**Citation 1 — douglasbrion.com/cv.pdf.** The dossier explicitly flagged Doug's personal site as non-operational. Gemini reintroduced this citation. **Verdict: dead link. Discard.**

**Citation 16 — Hacker News "Who is hiring? (November 2025)" cited as the source for Matta's tech stack.** intel.md captured Matta's actual job listings verbatim, including the FastAPI / Pydantic / Postgres / SQLAlchemy / Redis / Celery stack. Gemini routed through a Hacker News aggregator instead, where Matta-attributed content cannot be verified at the article level. **Verdict: aggregator with unverified authorship.** This PRD cites the verified intel.md job listings directly.

**Net effect on architecture selection:** The DMZ Vanguard's commercial case relied heavily on tainted citations 18 and 22. Removing them collapses the operational-pain framing. The Pattinson Filter framework relied entirely on the unverified citation 12/13. Removing it forces a rebuild on his actually-verified positions, which the CMMS Bridge satisfies more cleanly than the DMZ Vanguard ever could.

---

## 2. Architecture Selection

**The CMMS Bridge** — a stateless containerized sidecar that consumes Matta's outbound defect/anomaly webhook stream and produces structured work orders inside the customer's existing Computerized Maintenance Management System (SAP PM, IBM Maximo, Fiix, or UpKeep), surfaced to the maintenance technician through the customer's existing Slack or Microsoft Teams workspace.

**What it is:** A closed-loop *workflow* router. Matta detects defects on the line; the Bridge routes those detections into the customer's existing maintenance ticketing system as fully-formed work orders, with deterministic action-domain classification, schema-anchored Gemini generation, and ensemble-based uncertainty surfacing. The maintenance technician acknowledges or reassigns the work order from inside Slack, and the acknowledgment status flows back into Matta's event system as a "loop closed" signal.

**What it is not:** Closed-loop *machine-parameter* control. It does not adjust extrusion temperature, robot speed, or any physical machine setting. It does not actuate hardware. It does not touch SENTRY, TALLY, GAUGE, or TRACE internals. It does not replicate the Manufacturing OS dashboard. It operates strictly on the customer's outbound side of the Matta core, in the customer's existing enterprise systems, on a time scale of minutes-to-hours rather than the millisecond-to-second time scale of the patented machine-control loop.

---

## 3. The FDE Thesis

The CMMS Bridge passes all five SOP pillars and all four filters from the Step 1A target brief. Citations are verbatim from intel.md and the dossier; no fabricated sources are used.

### 3.1 Pillar 1 — Bottleneck Assassin

Doug Brion's verbatim hiring post: *"We're now deploying into two new factories every month – and we need to move faster"* [intel.md: Doug Brion LinkedIn, 12 Feb 2026]. The deployment velocity bottleneck is not the camera setup or the model training — Matta's own marketing claims hardware-to-live within hours and >99% defect detection accuracy with ten minutes of data [intel.md: Cambridge IfM news, 10 Dec 2025]. The bottleneck is the per-customer enterprise integration layer that turns Matta's defect signal into a maintenance action inside the customer's existing CMMS. Each factory has its own CMMS (SAP PM, Maximo, Fiix, UpKeep), each with bespoke API conventions and field mappings. Matta's FDEs absorb this integration work today as hand-written per-customer scripts. The Forward Deployed Engineer job description states the role is to "deploy hardware into factories and work side-by-side with customers to solve real manufacturing challenges" [intel.md: FDE job listing]. CMMS integration consumes that capacity. A pre-built, generalized CMMS Bridge eliminates this work, returning FDE hours to physical floor problems and accelerating the per-deployment timeline.

### 3.2 Pillar 2 — Anti-Replication

The CMMS Bridge does not touch any of Matta's four named agents (SENTRY, TALLY, GAUGE, TRACE), the Manufacturing Foundation Models, the Manufacturing OS UI, the edge device firmware, or the real-time camera streams. It consumes only Matta's outbound webhook contract — the same contract Matta exposes to any customer integration today. The patent distinction articulated in section 1.D above is the formal anti-replication argument: the closed-loop machine-control patent operates on machine-parameter actuation in real time; the Bridge operates on enterprise workflow routing in human time. The Ego Check is satisfied: Damjan's roadmap does not include per-customer CMMS connectors because they are by definition customer-specific integration work, not core product. Damjan would *welcome* a stateless containerized sidecar that absorbs this work.

### 3.3 Pillar 3 — Native Environment

The maintenance technician never sees a Kaide Labs UI and never sees a Matta UI. The work order materializes inside the customer's existing CMMS (Fiix, Maximo, SAP PM) — the same screen the technician already opens twenty times a day. The notification surfaces inside the customer's Slack or Microsoft Teams workspace — the same channel where maintenance escalations already happen. The acknowledgment action button is a Slack interactive message, the same UI pattern the technician already uses for incident response. Per the Identity file: *"Native Environment: Does the UI live where the users already work? It must feel like a native feature, not a bolted-on external tool."* The Bridge feels native because the work order *is* native — it sits in the same queue as every other work order the technician handles.

### 3.4 Pillar 4 — Magic Moment (under 60 seconds)

The demo video opens with a side-by-side screen: a mocked SENTRY feed on the left, a mocked Fiix CMMS view on the right, and a Slack mobile mock-up bottom-right.

T+0s: A defect event fires on the SENTRY feed (a polymer extrusion defect, urgency-tagged HIGH).
T+3s: The Bridge's intermediate "Theater" pane lights up with the inbound webhook, the deterministic Action Domain Classifier decision (`mechanical_wear → CMMS path`), and the launch of the three-shot Gemini Flash ensemble.
T+18s: The ensemble vote completes (3/3 agreement on root cause: "die head wear"). The narrative is generated. Pydantic validation passes.
T+21s: A fully-formed work order materializes in the Fiix queue: *"Replace die head on Press #3 — defect rate spiked from 0.2% to 8.4% over last 30 minutes — estimated labor 45 min — required parts: die head assembly P/N 7842."*
T+24s: A Slack notification fires to the on-shift maintenance technician's mobile phone with Acknowledge / Defer / Reassign buttons.
T+38s: Technician taps Acknowledge on mobile. Status flows back to the Bridge, into the Matta event log, marking the loop closed.

Total elapsed: 38 seconds. Buffer to 60s reserved for demo narration overlay.

### 3.5 Pillar 5 — System Resilience and Immunity

Three layers of deterministic safety, structured to address each filter explicitly.

*Idempotency layer:* Every inbound Matta webhook carries an `event_id`. The Bridge maintains a Redis-backed idempotency table; duplicate event_ids return the cached prior decision rather than re-running the pipeline. Webhook delivery semantics are exactly-once-effectively even under network retry storms. This addresses the Denic Gatekeeper's stated mandate against "brittle API contracts lacking Pydantic validation or failing to gracefully degrade during network loss."

*Deterministic Action Domain Classifier (ADC):* A hardcoded Python rules engine maps defect-type plus root-cause categorical fields to a target enterprise system (CMMS / QMS / Supplier). The LLM does not decide where the event goes. This addresses the Pattinson Filter — Sebastian's verified ARIA SoTA Frontiers Night talk on cyber-physical trust positions deterministic governance as the structural prerequisite for any AI system that interfaces with physical machinery. The ADC *is* the deterministic governance operator. The Pydantic schema for each output system enforces the admissible action space at the API boundary.

*Multi-sample consensus voting:* For the Gemini-generated narrative and root cause hypothesis, the Bridge runs Gemini 3 Flash three times in parallel with `thinking_level="minimal"` (to preserve sample diversity — Gemini 3's reasoning loop otherwise converges samples toward a single mode and collapses the ensemble signal) and temperature variance (0.1, 0.5, 0.9), then applies plurality voting on the categorical root-cause field. If the three samples disagree on root cause, the work order is generated with status `requires_human_review` and surfaces in a dedicated Slack channel for FDE/QE adjudication rather than being shipped directly to the maintenance queue. This is the structural analog of *Lakshminarayanan, Pritzel & Blundell (2017), "Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles"* — exactly the methodology Doug Brion implemented in his public repository `dougbrion/pytorch-deep-ensembles`. The pitch must be clear: we are not claiming to do Dirichlet-prior epistemic uncertainty on a foundation-model output (which is not mathematically definable); we are applying the deep ensembles methodology at the prompt-orchestration layer, which is structurally consistent with Doug's published work.

### 3.6 Filter Pass-Through Summary

| Filter | Anchor | How the Bridge satisfies |
|---|---|---|
| Brion (commercial pragmatism + uncertainty) | "We need to move faster" + `dougbrion/pytorch-deep-ensembles` | Eliminates per-customer CMMS integration work; surfaces uncertainty via N=3 ensemble voting structurally analogous to his published methodology. |
| Pattinson (cyber-physical trust + first principles) | ARIA SoTA Frontiers Night talk + Cambridge CAM "Security of Physical AI Systems" | Deterministic Action Domain Classifier as governance operator; admissible action space enforced by Pydantic schemas at every API boundary; no actuation of physical hardware. |
| Denic (execution maximalism + idempotency) | intel.md Backend Engineer JD: "FastAPI, Pydantic, Postgres, SQLAlchemy, Redis, Celery" | Bridge stack is exact match. Redis idempotency table. Celery task queue with exactly-once-effectively delivery semantics. Graceful degradation when CMMS API unavailable (queue + retry). |
| Investor mandate (Lakestar + Giant + 1st Kind) | Akis Bratsos quote on "fast time to value" + Giant European tech sovereignty + 1st Kind Peugeot industrial legacy | Bridge shortens deployment timeline (Lakestar). Runs in Google Cloud EU region, no proprietary data leaves customer region (Giant). Built for SAP PM and Maximo first — the exact CMMS systems automotive Tier-1 suppliers use (1st Kind). |

---

## 4. System Architecture and Agent Routing

All LLM inference is routed through Vertex AI on Google Cloud via the Google Gen AI SDK (`google-genai`), targeting `europe-west4` (Netherlands) for Giant Ventures' EU data-residency mandate. No Anthropic, OpenAI, or Bedrock dependencies anywhere in the deliverable. The legacy `vertexai.generative_models` module is deprecated and removed on 2026-06-24, so the Bridge ships against `google-genai` from day one.

### 4.1 Data Flow (Prose Diagram)

The Matta core (mocked in the demo) emits a webhook to the Bridge's FastAPI ingress endpoint. The webhook payload conforms to a Pydantic schema (`MattaDefectEvent`) with `event_id`, `agent` (`SENTRY` | `TALLY` | `GAUGE`), `defect_class`, `severity`, `timestamp`, `line_id`, `factory_id`, plus a 256-token raw context blob.

The ingress endpoint immediately checks the Redis idempotency table for the `event_id`. If present, it returns the cached prior response with HTTP 200 (idempotent replay). If absent, it writes a placeholder, validates the payload against `MattaDefectEvent`, and enqueues a Celery task `process_event(event_id)`.

The Celery worker fetches the event from Postgres, then executes a four-stage pipeline:

**Stage 1 — Action Domain Classification (deterministic, no LLM).** A hardcoded Python rules engine maps `(agent, defect_class, severity)` to one of three target domains: `CMMS` (mechanical wear, tool damage, calibration drift, scheduled maintenance trigger), `QMS` (batch quarantine, NCR-worthy escape, supplier traceability), `SUPPLIER` (incoming material defect with traced supplier ID). For the Phase 1 demo, only the CMMS path is wired through to a target system; QMS and SUPPLIER paths log "Phase 2 routing" to the Theater dashboard but do not produce live artifacts.

**Stage 2 — Root cause hypothesis (Gemini 3 Flash, N=3 ensemble).** Three parallel calls to Gemini 3 Flash via Vertex AI (model id `gemini-3-flash`) with `thinking_level="minimal"` and temperature variance (0.1, 0.5, 0.9), each receiving the event payload plus a constrained-generation prompt template (Section 6.4 below). Each call returns a JSON object conforming to `RootCauseHypothesis` Pydantic schema with categorical fields (root_cause, confidence_band) and a one-sentence natural language rationale. The Bridge applies plurality voting on `root_cause`; on disagreement, the work order is flagged `requires_human_review`.

**Stage 3 — Work order narrative generation (Gemini 3.1 Pro, N=1).** A single call to Gemini 3.1 Pro via Vertex AI (model id `gemini-3-1-pro`) with `thinking_level="medium"`, receiving the validated event plus the consensus root cause hypothesis. The prompt requests a structured `CMMSWorkOrder` Pydantic object with: `title`, `description`, `urgency_tier` (`P1`–`P4`), `estimated_labor_minutes`, `required_parts` (list of P/N strings), `assigned_team`. Vertex AI's structured-output mode is used to guarantee schema conformance; output is re-validated against the Pydantic schema as a defense-in-depth check.

**Stage 4 — Target system dispatch.** For the demo, a mock CMMS adapter writes the work order to a local Postgres `mock_cmms_workorders` table. In production, this stage is a polymorphic adapter pattern: `FiixAdapter`, `MaximoAdapter`, `SAPPlantMaintenanceAdapter`, `UpKeepAdapter`, each implementing a common `CMMSAdapter` interface with `create_work_order(payload: CMMSWorkOrder) -> WorkOrderID`. After the work order is written, a Slack notification is fired through the Slack Web API to the configured channel for the maintenance team, with Block Kit interactive buttons (Acknowledge, Defer, Reassign).

The Slack webhook for the Acknowledge button hits the Bridge's `/slack/interactions` endpoint, which updates the work order status, writes back to Matta's event log via a return webhook (in the demo this is a mocked endpoint), and updates the Theater dashboard in real time via WebSocket.

### 4.2 Gemini Model Routing Rationale

| Stage | Model | Reason |
|---|---|---|
| Root cause classification (Stage 2) | Gemini 3 Flash, N=3 (`thinking_level="minimal"`, temps 0.1 / 0.5 / 0.9) | Categorical classification under tight latency budget. Gemini 3 Flash is the current cost-optimized Vertex AI model with native structured-output, replacing the deprecated 2.5 Flash. `thinking_level="minimal"` is required to preserve ensemble diversity — Gemini 3's default reasoning trace otherwise collapses the three samples toward a single mode and destroys the deep-ensembles signal. Pricing: $0.50/M input, $3.00/M output. |
| Narrative generation (Stage 3) | Gemini 3.1 Pro, N=1 (`thinking_level="medium"`) | Higher-quality natural language for the customer-facing work order title and description. Gemini 3.1 Pro is the current flagship reasoning model on Vertex AI, replacing 2.5 Pro. Call frequency is one per consensus event so the unit cost is amortized. Pricing: $2.00/M input (≤200K context), $12.00/M output. |
| All inference | Vertex AI on Google Cloud, EU region | Investor mandate: Giant Ventures' European tech sovereignty thesis; GDPR data localization. |

### 4.3 Idempotency and Graceful Degradation

The Bridge guarantees exactly-once-effectively processing of each `event_id` through the Redis idempotency table with 24-hour TTL. Celery tasks are configured with `acks_late=True` and `reject_on_worker_lost=True` so a worker crash mid-pipeline retries cleanly without duplicate downstream effects (the Stage 4 CMMS adapter is itself idempotent on `event_id` written as the work order's external reference).

If the customer's CMMS is unreachable, the Stage 4 dispatch fails; the work order is queued in Postgres with status `pending_dispatch` and a Celery beat schedule retries every 60 seconds with exponential backoff, capped at six hours. The Slack notification still fires immediately with a "CMMS sync delayed — work order queued, ID xxx" badge, so the maintenance team has hands-on visibility even during CMMS outages. This addresses the Denic Gatekeeper requirement that the system "gracefully degrade across air-gapped or intermittently connected edge networks without state loss."

---

## 5. Native Environment UI Spec — The Theater

The demo video has three on-screen panes, recorded simultaneously and composed in post-production by Isaac.

### 5.1 Left Pane — Mocked Matta Dashboard (Vue-flavored, NOT Matta's actual UI)

A simplified mock of the kind of operations dashboard a Matta customer's plant manager would see. Built in plain HTML + Tailwind so it can be screen-recorded crisply. Shows a live SENTRY camera feed (a looped recorded video of an extrusion line), a defect detection overlay that highlights an anomaly when the demo trigger fires, and a defect-rate chart that visibly spikes. Branded with a generic "Factory Operations" header; never branded with the Matta wordmark or any Matta-flavored UI element. This pane represents *the customer's existing Matta deployment* — it is the source of the event, not the destination.

### 5.2 Center Pane — The Bridge Theater

A Next.js + Tailwind dashboard exposing the Bridge's internal state in real time via WebSocket. Modeled after the Mundostra "Self-Healing Support" dashboard from the SOP. Shows:

- **Inbound event card:** the raw `MattaDefectEvent` payload as JSON, animated in from the left.
- **Action Domain Classifier decision:** a small badge showing the deterministic rule that fired (e.g., `defect_class=mechanical_wear, severity=high → CMMS path`).
- **Ensemble voting visualization:** three parallel cards labeled "Gemini Flash Sample 1/2/3", each filling in with their `root_cause` classification as the parallel calls return. A consensus indicator lights up green when 3/3 agree, yellow on 2/3 (but still ships), red on full disagreement (requires_human_review).
- **Work order preview:** the generated `CMMSWorkOrder` Pydantic object, rendered as a faux-CMMS card.
- **Cost ticker:** live Vertex AI cost per event (sub-cent-level), to kill the "AI is expensive" objection per the Mundostra demo precedent.
- **JSON inspector:** click any pipeline stage to see the raw Pydantic-validated payloads, demonstrating end-to-end type safety. This is built specifically for Damjan to inspect during the demo review.

### 5.3 Right Pane — Mocked Customer CMMS (Fiix-flavored)

A simplified clone of the Fiix work-order queue UI, rendered in Tailwind. Sits empty at the demo's start. When the Bridge's Stage 4 dispatches, the new work order materializes at the top of the queue with the title, urgency badge, parts list, and a "New" indicator. This is the "Native Environment" proof: the CMMS sees the work order as a normal entry, indistinguishable from one a maintenance planner might have written by hand.

### 5.4 Bottom-Right Inset — Slack Mobile Mock-up

A phone-frame Slack mobile mock showing the on-shift maintenance technician's notification with the work order summary and three Block Kit action buttons. When the demo hits T+38s, the screen recording shows a finger tapping Acknowledge; the button confirms; the Theater pane reflects the status change.

### 5.5 Cold-Open and Voice-Over Treatment

Per the Identity file: cold-open with the Magic Moment in the first 10–15 seconds. The first 12 seconds of the video shows nothing but the three panes, the defect firing, and the work order materializing — no voiceover, just sound design. At T+13s Hafeedh's voiceover begins: *"What you just watched is a stateless sidecar that takes a defect event from a Matta production deployment and turns it into a maintenance work order in the customer's CMMS, with a Slack ack flow, in under forty seconds. Here's how it works."* The next 4 minutes is the technical walkthrough using the JSON inspector.

The final 30 seconds tease the verbal Phase 2: *"The same architecture handles QMS NCRs and supplier CARs — same Action Domain Classifier, different terminal schema. Happy to walk that through on a 15-minute call."* Per the Identity file: *"Adjacent ideas are verbal only. Tease 1-2 additional architectures at the end of the video to hook a second call. Never put the full architecture in writing."*

---

## 6. Phase 1 Execution Spec — 72-Hour Sprint

### 6.1 Repository Structure

```
matta-cmms-bridge/
├── README.md
├── docker-compose.yml
├── .env.example
├── infra/
│   ├── Dockerfile.api
│   ├── Dockerfile.worker
│   └── cloudrun.yaml
├── apps/
│   ├── bridge_api/                   # FastAPI ingress + Slack webhook
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── webhooks.py
│   │   │   └── slack_interactions.py
│   │   └── tests/
│   ├── bridge_worker/                # Celery workers
│   │   ├── tasks/
│   │   │   ├── process_event.py
│   │   │   ├── classify_action_domain.py
│   │   │   ├── ensemble_root_cause.py
│   │   │   ├── generate_work_order.py
│   │   │   └── dispatch_cmms.py
│   │   └── tests/
│   ├── theater_ui/                   # Next.js Theater dashboard
│   │   ├── pages/
│   │   ├── components/
│   │   └── hooks/useWebSocket.ts
│   └── mocks/
│       ├── matta_event_publisher.py  # Fires fake MattaDefectEvents
│       ├── mock_cmms_api/            # Fake Fiix-style API
│       └── mock_matta_dashboard/     # Left-pane Tailwind mock
├── packages/
│   ├── schemas/                      # Pydantic models (shared)
│   │   ├── matta_event.py
│   │   ├── root_cause.py
│   │   └── cmms_work_order.py
│   ├── adapters/
│   │   ├── base.py                   # CMMSAdapter ABC
│   │   ├── fiix_adapter.py
│   │   ├── maximo_adapter.py         # stubbed for demo
│   │   ├── sap_pm_adapter.py         # stubbed for demo
│   │   └── upkeep_adapter.py         # stubbed for demo
│   ├── adc/                          # Action Domain Classifier rules
│   │   └── rules.py
│   └── prompts/                      # Vertex AI prompt templates
│       ├── root_cause_flash.py
│       └── work_order_pro.py
└── scripts/
    ├── seed_mock_data.py
    └── run_demo.sh                   # Orchestrates the demo flow
```

### 6.2 Critical Pydantic Schemas

Pinned versions: `pydantic>=2.13,<3`, `fastapi>=0.136,<0.137`, `google-genai>=1.0`, `celery>=5.5`, `redis>=5.2`, `sqlalchemy>=2.0,<2.1`. All schemas use Pydantic v2 idioms (`Annotated[..., Field(...)]`, `field_validator`, `model_validate_json` / `model_dump_json`) — `parse_obj` and the v1 `@validator` decorator are not used anywhere in the codebase.

```python
# packages/schemas/matta_event.py
from datetime import datetime
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field

class MattaDefectEvent(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    event_id: Annotated[str, Field(min_length=1, max_length=64)]
    agent: Literal["SENTRY", "TALLY", "GAUGE"]
    defect_class: str
    severity: Literal["low", "medium", "high", "critical"]
    timestamp: datetime
    line_id: str
    factory_id: str
    raw_context: Annotated[str, Field(max_length=2048)]

# packages/schemas/root_cause.py
class RootCauseHypothesis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    root_cause: Literal[
        "mechanical_wear", "tool_damage", "calibration_drift",
        "material_defect", "process_drift", "operator_error", "unknown",
    ]
    confidence_band: Literal["high", "medium", "low"]
    rationale: Annotated[str, Field(max_length=400)]

# packages/schemas/cmms_work_order.py
class CMMSWorkOrder(BaseModel):
    model_config = ConfigDict(extra="forbid")

    external_event_id: str          # ties back to MattaDefectEvent.event_id
    title: Annotated[str, Field(max_length=120)]
    description: Annotated[str, Field(max_length=1000)]
    urgency_tier: Literal["P1", "P2", "P3", "P4"]
    estimated_labor_minutes: Annotated[int, Field(ge=5, le=480)]
    required_parts: Annotated[list[str], Field(default_factory=list, max_length=10)]
    assigned_team: str
    requires_human_review: bool = False
```

### 6.3 FastAPI Ingress Contract

```python
# apps/bridge_api/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
import redis.asyncio as aioredis
from celery import Celery

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = aioredis.from_url(
        settings.redis_url, decode_responses=True, max_connections=64,
    )
    app.state.celery = Celery("bridge", broker=settings.celery_broker)
    try:
        yield
    finally:
        await app.state.redis.aclose()

app = FastAPI(lifespan=lifespan, title="Matta CMMS Bridge")

# apps/bridge_api/routers/webhooks.py
from typing import Annotated
from fastapi import APIRouter, Depends, Request
from redis.asyncio import Redis

router = APIRouter()

async def get_redis(request: Request) -> Redis:
    return request.app.state.redis

async def get_celery(request: Request) -> Celery:
    return request.app.state.celery

RedisDep = Annotated[Redis, Depends(get_redis)]
CeleryDep = Annotated[Celery, Depends(get_celery)]

@router.post("/webhooks/matta-defect", response_model=IngressAck)
async def receive_matta_event(
    event: MattaDefectEvent,
    redis: RedisDep,
    celery: CeleryDep,
) -> IngressAck:
    # Idempotency guard
    cached = await redis.get(f"event:{event.event_id}")
    if cached:
        return IngressAck.model_validate_json(cached)

    # Reserve the event_id
    placeholder = IngressAck(event_id=event.event_id, status="processing")
    await redis.set(
        f"event:{event.event_id}",
        placeholder.model_dump_json(),
        ex=86400,  # 24h TTL
    )

    # Enqueue (Celery 5.5 — task name registered in bridge_worker)
    celery.send_task("bridge.process_event", args=[event.model_dump_json()])
    return placeholder
```

Notes on the modern stack used above:

- FastAPI ≥0.136 deprecates the `@app.on_event("startup"/"shutdown")` pattern in favour of the `lifespan` async context manager shown.
- Pydantic-v1 `parse_raw` is gone; the body is parsed by FastAPI itself, and cached payloads are revived with `model_validate_json`.
- `redis.asyncio` is the supported import path on `redis-py` ≥5.2 (the older `aioredis` package is archived). `Redis.close()` was renamed to `aclose()`.
- Dependencies are typed via `Annotated[T, Depends(...)]` (PEP 593), the FastAPI-recommended idiom since 0.95 and the only supported form once mutable defaults are removed.
- Celery workers are configured with `task_acks_late=True`, `task_reject_on_worker_lost=True`, `worker_prefetch_multiplier=1`, and `broker_transport_options={"visibility_timeout": 3600}` on the Redis broker — these are the current Celery 5.5 settings that combine with the Redis idempotency table to give exactly-once-effectively delivery.
- The Google Gen AI SDK call inside the worker uses `genai.Client(vertexai=True, project=..., location="europe-west4")`. The deprecated `vertexai.generative_models.GenerativeModel` API is not imported anywhere.

### 6.4 Vertex AI Prompt Templates

**Root cause classification (Gemini 3 Flash, N=3):**

```python
ROOT_CAUSE_PROMPT = """You are classifying a manufacturing defect event into one of seven root cause categories. Output strict JSON conforming to the provided schema. Do not invent categories outside the enum.

Event:
- Agent: {agent}
- Defect class: {defect_class}
- Severity: {severity}
- Line: {line_id}, Factory: {factory_id}
- Raw context: {raw_context}

Allowed root_cause values (choose exactly one):
- mechanical_wear: gradual degradation of tooling, dies, bearings
- tool_damage: acute damage to a specific tool or fixture
- calibration_drift: sensor or machine calibration outside tolerance
- material_defect: incoming material out of spec
- process_drift: parameter creep (temperature, speed, pressure) outside band
- operator_error: human procedural error
- unknown: insufficient information to classify

Allowed confidence_band values:
- high: signal is clear and unambiguous
- medium: signal is plausible but alternative explanations exist
- low: signal is weak; recommend human review

Output JSON only."""
```

Vertex AI structured-output mode is invoked through the Google Gen AI SDK (`google-genai`) using `client.models.generate_content` with `config=GenerateContentConfig(response_mime_type="application/json", response_schema=RootCauseHypothesis, thinking_config=ThinkingConfig(thinking_level="minimal"), temperature=t)`. Three parallel calls with `temperature` ∈ {0.1, 0.5, 0.9} and identical other parameters. Plurality vote on `root_cause`; if no plurality (3-way split), force `requires_human_review = True` on the downstream work order.

**Work order narrative (Gemini 3.1 Pro, N=1):** Receives the validated event plus consensus `RootCauseHypothesis` and outputs a `CMMSWorkOrder`. Prompt explicitly forbids the model from inventing parts numbers — the parts list is constrained to a small enum drawn from a hardcoded parts catalog for the demo (in production this would be the customer's actual SAP material master). Urgency tier is mapped from severity by deterministic rule, *then* the LLM is told the tier as a fixed input — the LLM does not choose urgency.

### 6.5 Mock Data Generation

`scripts/seed_mock_data.py` generates 50 synthetic `MattaDefectEvent` records spanning all three agents and all severity levels. The demo run uses event #23 (a polymer extrusion mechanical wear case) as the headline trigger because it produces the cleanest cross-pane visualization. Backup events #14 and #41 are pre-loaded in case the live demo run hits a Vertex AI rate limit during recording.

### 6.6 Demo Recording Flow (Isaac's Production Plan)

1. Hafeedh opens three browser windows tiled: mocked Matta dashboard (left), Theater UI (center), mocked Fiix CMMS + Slack mobile mock (right). Slack mobile mock is rendered in a phone-frame iframe.
2. Hafeedh runs `./scripts/run_demo.sh trigger=23`.
3. OBS Studio captures all three panes simultaneously at 1080p / 30fps. Audio is recorded separately to a Rode NT-USB; voiceover is added in post.
4. Total recording length target: 4–5 minutes. First take is the cold-open / Magic Moment (15 seconds, silent). Second take is the technical walkthrough (3 minutes, voiceover). Third take is the verbal Phase 2 tease (45 seconds, voiceover, no new visuals).
5. Post-production in DaVinci Resolve. Captions auto-generated in Descript and hand-edited.
6. Exported to MP4, uploaded to Vidyard. Timestamp marker placed at 0:00 (Magic Moment) per Identity file outreach mechanic.

### 6.7 Magic Moment Success Criteria

The demo recording succeeds if and only if all of the following are true:

1. From defect-event fire to Slack mobile notification, total elapsed wall time is under 45 seconds (giving us 15 seconds of buffer to the 60-second Pillar 4 ceiling).
2. The Theater pane visibly shows the deterministic Action Domain Classifier decision *separately* from the Gemini ensemble — proving to Sebastian that the routing is rule-based and to Damjan that the data contracts are typed.
3. The Theater pane visibly shows the N=3 ensemble votes converging — proving to Doug that the uncertainty layer mirrors his published methodology.
4. The work order in the mocked Fiix queue contains an `external_event_id` that exactly matches the inbound `event_id` — proving the idempotency chain.
5. The Slack Acknowledge button round-trips back to the Theater pane within 3 seconds.
6. Total Vertex AI cost displayed in the cost ticker is under $0.05 for the full event lifecycle. Worked estimate at May-2026 EU pricing: 3× Gemini 3 Flash at ~500 input + 200 output tokens each → 1,500 in × $0.50/M + 600 out × $3.00/M = $0.0026; 1× Gemini 3.1 Pro at ~1,000 input + 400 output tokens (`thinking_level="medium"` thinking tokens billed as output) → 1,000 × $2.00/M + 400 × $12.00/M = $0.0068. Per-event total ≈ **$0.0094**, leaving ~5× headroom against the $0.05 ceiling. Ceiling preserved.

---

## 7. Risk Register

The top three reasons this PRD could fail in front of Doug, Sebastian, or Damjan, with mitigation for each.

### 7.1 Risk: Doug interrogates the uncertainty quantification claim

**Failure mode:** Doug recognizes that ensemble voting on Gemini Flash classifications is *not* the same as Dirichlet-prior epistemic uncertainty estimation. He calls out the gap and accuses Kaide of marketing-speak rigor. The pitch dies.

**Mitigation:** Lead with the disclaimer ourselves. The voiceover script at T+1:30 should explicitly say: *"We can't do Dirichlet-prior evidential uncertainty on a foundation-model output — the model doesn't expose the right probability surface. What we can do, and what we've built, is the deep ensembles methodology applied at the orchestration layer. Three parallel Flash calls with mild temperature variance, plurality voting on the categorical output, with low-agreement events automatically routed to human review. It's the same idea you implemented in pytorch-deep-ensembles, lifted up a level of abstraction."* Naming the gap before Doug does converts a potential objection into a credibility marker. He authored the repo we're naming; he will respect the citation.

### 7.2 Risk: Sebastian challenges the patent boundary

**Failure mode:** Sebastian reviews the demo offline and challenges whether the CMMS Bridge encroaches on the closed-loop control patent. If he reads the patent claims expansively, he could argue that "any system that uses defect detection to drive an action" falls under the patent's scope.

**Mitigation:** The PRD's Section 1.D table making the time-scale / actuator / action-space distinction is the talking-point armor. The verbal pitch must include the line: *"The patent is on closed-loop control of machine parameters — millisecond-scale actuation of equipment settings. The Bridge is closed-loop control of enterprise workflow — minute-scale routing of work orders to humans. The actuator in the patent is the PLC; the actuator in the Bridge is a maintenance technician acknowledging a Slack notification. Different time scales, different action spaces, different failure modes."* Have the table from Section 1.D printed as a single slide ready to be pulled up if Sebastian raises the concern. A prepared answer signals that we anticipated the question, which signals respect for his domain.

### 7.3 Risk: Damjan rejects the Pydantic / idempotency story as too shallow

**Failure mode:** Damjan inspects the JSON inspector during the demo review and finds the data contracts are demo-grade rather than production-grade — missing fields, weak validation, naive idempotency keys. He concludes the architecture is theater rather than substance.

**Mitigation:** The 72-hour sprint produces a demo, but the schemas (Section 6.2) and the idempotency code (Section 6.3) must be production-quality even if the surrounding infrastructure is mocked. Specifically: the `MattaDefectEvent` schema must include all fields a real Matta event would carry (per the dossier's analysis of the WebSockets / WebRTC streaming architecture); the Redis idempotency table must use the exact pattern the Bridge would use in production with real TTL handling; the Celery `acks_late=True` configuration must be real, not faked. If Damjan inspects the codebase post-demo, every line he touches should be code we'd be willing to ship to production. The areas that *are* mocks (the CMMS adapters for SAP PM / Maximo / UpKeep, the Matta dashboard pane, the Slack mobile mock) must be clearly labeled as `# DEMO MOCK — Phase 2 production adapter` so there is no ambiguity about what is real versus what is theater.

---

## Appendix A — Sections Flagged for Vocabulary Scrubbing if Reused Client-Facing

Per the Identity file: *"this PRD is internal to Kaide Labs and may use Kaide vocabulary (Stateless Sidecar, Revenue Unblocking, DMZ, FDE Strike Team). Outreach materials drafted from this PRD must scrub all internal jargon."*

Sections requiring scrubbing before any client-facing reuse:
- Section 1 (Red-Team Adjudication) — entire section is internal posture, never share.
- Section 3 (FDE Thesis) — strip "FDE Thesis", "Bottleneck Assassin", "Magic Moment", "DMZ", "Stateless Sidecar", "Revenue Unblocking" before sharing as a "technical brief" if needed.
- Section 7 (Risk Register) — never share; reveals adversarial preparation.

Sections safe for client-facing reuse with light editing:
- Section 4 (System Architecture) — describes the technical deliverable in neutral terms.
- Section 5 (Native Environment UI Spec) — describes the demo theater in neutral terms.
- Section 6.2 / 6.3 / 6.4 (Schemas, contracts, prompts) — concrete technical artifacts that demonstrate competence.

---

## Appendix B — Modernization Audit Log

This appendix records the May-2026 modernization pass against the Pass A (frontier model upgrade) and Pass B (syntax & deprecation) checklists. Architecture, FDE strategy, deterministic math, and patent boundary are unchanged — only model strings, SDK surface, and Pythonic idiom were touched.

### B.1 Model string changes

| Location | Before | After | Justification |
|---|---|---|---|
| §3.5, §4.1 Stage 2, §4.2, §6.4 | Gemini 2.5 Flash, N=3 | **Gemini 3 Flash** (`gemini-3-flash`), N=3 | Gemini 2.5 Flash is no longer the cost-optimized production-recommended model on Vertex AI as of 2026. Gemini 3 Flash is the current generation, supports native structured-output, and matches the throughput/latency profile required for the N=3 ensemble. Pricing on Vertex AI: $0.50/M input, $3.00/M output. |
| §3.5, §4.1 Stage 2 | temperature variance (0.0, 0.2, 0.4) | temperature variance (0.1, 0.5, 0.9) with `thinking_level="minimal"` | Gemini 3 reasoning models converge samples toward a single mode by default, which collapses the deep-ensembles signal that the Brion Filter depends on. `thinking_level="minimal"` disables the reasoning trace for the Stage 2 ensemble; the wider temperature spread restores sample diversity equivalent to what 2.5 Flash gave at the narrower (0.0, 0.2, 0.4) spread. The Lakshminarayanan 2017 deep-ensembles methodology is unchanged in spirit; only the sampling configuration was retuned for the new model's variance characteristics. |
| §4.1 Stage 3, §4.2, §6.4 | Gemini 2.5 Pro, N=1 | **Gemini 3.1 Pro** (`gemini-3-1-pro`), N=1, `thinking_level="medium"` | Gemini 2.5 Pro has been superseded by the 3.1 Pro flagship for natural-language generation inside Pydantic-validated schemas. `thinking_level="medium"` is appropriate for narrative quality without runaway thinking-token cost. Pricing on Vertex AI: $2.00/M input (≤200K context), $12.00/M output. |
| §4 preamble | (no region pinned) | `europe-west4` (Netherlands) Vertex AI endpoint | Giant Ventures' EU data-residency mandate is now expressed concretely in the architecture, not just in the filter table. |

### B.2 Library / SDK changes

| Library | Before (implicit, January-2026) | After (May-2026) | Breaking change motivating the update |
|---|---|---|---|
| Google GenAI SDK | `vertexai.generative_models` (Vertex AI Python SDK) | `google-genai` (Google Gen AI SDK), `genai.Client(vertexai=True, location="europe-west4")` | `vertexai.generative_models`, `vertexai.language_models`, `vertexai.vision_models`, `vertexai.tuning`, `vertexai.caching` were deprecated 2025-06-24 and are removed 2026-06-24. Shipping against the deprecated module would brick within a month of the demo. |
| FastAPI | (unpinned, ~0.110-era patterns) | `fastapi>=0.136,<0.137` with `lifespan` async context manager and `Annotated[T, Depends(...)]` dependency injection | FastAPI 0.126 (Dec 2025) dropped Pydantic-v1 support entirely. `@app.on_event("startup"/"shutdown")` is deprecated in favor of `lifespan`. PEP 593 `Annotated` is now the recommended dependency form. |
| Pydantic | v1-style `Field(..., max_length=...)` directly on attributes, `parse_raw`, `@validator` | `pydantic>=2.13,<3` with `Annotated[..., Field(...)]`, `model_validate_json`, `model_dump_json`, `field_validator`, `ConfigDict(extra="forbid")` | Pydantic v2 rewrote the validation engine in Rust (`pydantic-core`). `parse_raw` and `parse_file` are gone; `@validator`/`@root_validator` are replaced by `@field_validator`/`@model_validator`. The list-length syntax `Field(max_length=...)` on `list[...]` only works in v2.5+. |
| Celery | `acks_late=True`, `reject_on_worker_lost=True` (correct, but unpinned) | `celery>=5.5` with the same flags plus `worker_prefetch_multiplier=1` and `broker_transport_options={"visibility_timeout": 3600}` on Redis broker | Celery 5.5 hardened the Redis broker visibility-timeout interaction with `acks_late`. Without the explicit visibility timeout, long-running Pro calls can be re-queued mid-flight and produce duplicate Stage 3 work orders. |
| Redis client | `aioredis` (separate package) | `redis.asyncio` from `redis>=5.2`; `Redis.aclose()` instead of `Redis.close()` | `aioredis` was archived; the async client is bundled into `redis-py`. `close()` is sync and deprecated for the async client. |
| SQLAlchemy | (unpinned) | `sqlalchemy>=2.0,<2.1` with the 2.0-style `select()` + `AsyncSession` API; ORM for the work-order table, Core for the idempotency cache | 2.0 deprecated the legacy `Query` API; mixing 1.x and 2.x styles produces silent behavioral drift in async sessions. |
| Slack Web API + Block Kit | Block Kit interactive messages with action buttons | Same Block Kit pattern, but signed via the modern Slack request-signature scheme (HMAC-SHA256 on `v0:{ts}:{raw_body}`) with a 5-minute timestamp window, verified before any Pydantic parsing of the interaction payload | Slack's older `verification_token` mechanism is deprecated; the `/slack/interactions` endpoint MUST verify `X-Slack-Signature` to satisfy the Pattinson Filter's "admissible action space at the boundary" requirement. |

### B.3 Cost estimate revisions

§6.7 success criterion #6 ("Vertex AI cost under $0.05 for the full event lifecycle") was recomputed against May-2026 Vertex AI EU pricing for Gemini 3 Flash and Gemini 3.1 Pro. Per-event estimate is **~$0.0094** (3× Flash ensemble ≈ $0.0026, 1× Pro narrative ≈ $0.0068), leaving roughly 5× headroom against the $0.05 ceiling. **The $0.05 ceiling is preserved** — no upward revision was required.

### B.4 Confirmations of unchanged sections

The following load-bearing sections were re-read after every pass and confirmed byte-for-byte unchanged from the pre-modernization PRD:

- **§1.D — Patent distinction table** (closed-loop machine control vs closed-loop workflow routing). Preserved verbatim. The time-scale / actuator / action-space / failure-mode / data-flow distinctions are the verbal armor against Sebastian's patent-encroachment challenge and must not drift.
- **§3.5 — Deep ensembles methodology framing.** The citation to *Lakshminarayanan, Pritzel & Blundell (2017)* and to Doug's `dougbrion/pytorch-deep-ensembles` repository is unchanged. Only the sampling-configuration sentence (model name, `thinking_level`, temperatures) was updated; the load-bearing rigor argument — that the Bridge applies the deep-ensembles methodology at the prompt-orchestration layer rather than claiming Dirichlet-prior epistemic uncertainty on a foundation-model output — is preserved word-for-word in the surrounding sentences.
- **§4.1 Stage 1 — Action Domain Classifier.** Hardcoded Python rules engine over `(agent, defect_class, severity) → {CMMS, QMS, SUPPLIER}`. No LLM. Unchanged.
- **§1.E — Citation Hygiene Audit.** Unchanged.
- **§3.1–§3.4, §3.6 — Pillar arguments and Filter Pass-Through table.** Unchanged.
- **Anti-replication boundary (§2, §3.2).** The Bridge still consumes only Matta's outbound webhook stream and writes to customer-side enterprise systems (CMMS, QMS, Supplier portals). It does not touch SENTRY, TALLY, GAUGE, TRACE, the Manufacturing Foundation Models, the Manufacturing OS UI, edge device firmware, or real-time camera streams. Verified after each pass.
- **No new vendor dependencies.** Anthropic, OpenAI, and AWS Bedrock are not imported anywhere. The deliverable remains Google-only (Vertex AI / Gemini via `google-genai`).

---

*End of MATTA_MASTER_PRD.md*
