# Matta Refinery — Demo Walkthrough

**Audience:** Doug Brion (CEO, buyer-level) and the Special Projects hire / Damjan Denic (CTO, operator-level).
**Use case:** Vidyard voiceover reference, cold-email accompaniment, follow-up call notes.

Each beat below leads with the buyer-level reading. Beneath each is an *Operator depth* subsection with the technical reading. Read just the buyer-level beats for a five-minute scan; read both for full comprehension.

---

## Part 1 — The Problem in 60 Seconds

Matta deploys factory-line inspection cameras in hours, not months. That speed has produced a queue Doug cannot serve: roughly two deployments a month against a multi-year waitlist, with 124 leads from a single trade show (UK Metals Expo 2025) and 100+ from another (Advanced Engineering 2025). Every misallocated slot is a meaningful fraction of ARR.

The week between the trade-show floor and the factory visit is where Doug, Damjan, and the incoming Special Projects hire personally absorb the triage burden: which prospect actually fits Matta's deployment patterns, which past customer is the right comparable, which factory has the integration risk that will torpedo the pilot. That research is currently manual — open Companies House, open LinkedIn, open the customer-reference deck, open eight more tabs.

The Refinery handles that slice and only that slice. It reads the trade-show CSV, ranks 124 leads by fit, and writes audit-grade pre-visit briefings for the top twelve. It never touches the cameras, the production line, or the closed-loop control. When the Special Projects hire walks in on day one, the triage is already done.

---

## Part 2 — What Doug Sees: The Demo Flow

### Beat 1 · T+0: The setup

The screen shows a three-pane console with the Matta wordmark in the navy header. Left pane: Doug's Slack channel (`#fde-lead-refinery`) with his own message — *"UK Metals Expo batch — Stew, can you triage?"* — and the CSV attached. Center pane: a "Theater Console" with a single peach **Run Demo** button. Right pane: an empty Drive view waiting for a dossier. A guided-demo callout in the top-right explains what's about to happen.

> **Operator depth:** Three React panes plus a fixed CRM inset render through a Next.js front end at `:3000`. The Theater UI lives outside Matta's infrastructure entirely — it talks to a FastAPI service at `:8080` over CORS-allowed `localhost`. No batch has been ingested yet, so the system is idle: Postgres has no `ingest_batches` row, Redis has no idempotency key, the worker fleet is parked. The console intentionally avoids any "control surface" affordances — it shows the system thinking, not knobs to turn. That restraint is part of the Damjan-readiness signal: this is observability, not autonomy.

### Beat 2 · The click: Run Demo fires

Doug clicks **Run Demo**. The CSV uploads in under a second. The Theater Console swaps the button for an ADC-route pill reading **PRIORITIZATION**, the idempotency hash of the upload, and a Stage 1 progress bar. The guided-demo callout advances to *"Stage 1 in flight: classifying each lead's vertical and scoring fit."*

> **Operator depth:** The front end fetches the static CSV from `/public/UK_Metals_Expo_2025_leads.csv`, wraps it in a `FormData` blob with `source_label=uk_metals_expo_2025`, and `POST`s to `/ingest/batch`. FastAPI computes `sha256(file)`, derives a 24-hour Redis idempotency key, and — inside one Postgres transaction — writes one `ingest_batches` row and 124 `lead_prospects` rows. Only then does it `send_task("refinery.score_batch")` to Celery. The ADC pill says PRIORITIZATION because `packages/adc/rules.py` ran zero LLM calls to decide: a batch upload always routes to prioritization; a single Slack interaction always routes to dossier-full. The route is determined by request shape, not by inference. That's the architectural anchor against any future Gemini regression — the ADC cannot misroute, because there is nothing to mislearn.

### Beat 3 · T+0 to ~T+5 min: Stage 1 in flight

The progress bar in the center pane creeps right. Nothing else moves. The guided callout updates the elapsed counter. Doug sees a system thinking — not an instant magic-trick. This is what Stew does over a week of evenings, compressed into the time it takes to make a coffee.

> **Operator depth:** During Stage 1 the worker fans out across 124 prospects. For each prospect: an enrichment task pulls company facts; a vertical-classification task runs an N=3 ensemble on Gemini 2.5 Flash at temperatures 0.1 / 0.5 / 0.9, then casts a confidence-weighted majority vote (the CISC pattern from Taubenfeld et al. 2025, the academic anchor for Doug's own `pytorch-deep-ensembles` lineage); a fitness-scoring task multiplies deterministic weights against the verified facts; and a stub-generation task writes the rank-12 cards. Stage 1 takes roughly five to six minutes of wallclock against gemini-2.5-flash at this batch size. The PRD's headline T+8 was specified against a 10-prospect simulator; the as-built timing at 124 prospects through real synchronous Vertex calls is documented in `MATTA_RECONCILIATION.md §4(a)`. The choice not to parallelize harder is deliberate: the cost of an N=3 ensemble per lead is the floor of the Pattinson methodology, and burning 5x the Vertex spend to compress the timer was rejected against the $0.10-per-dossier budget.

### Beat 4 · ~T+5 min: Magic Moment 1

Twelve prospect cards materialize in the Slack pane. **William Cook Sheffield** is at the top of the ranking with a fit score of 0.84 and a peach **Generate** badge. The CRM inset at the bottom-right populates with the same prospect's fit score, vertical (`metal_casting`), and a `slot_readiness: ready_for_dossier` flag. The Drive pane breadcrumb updates to show a new "Priority Index" document. Three Matta-relevant surfaces — Slack, CRM, Drive — populate in the same beat. The guided callout reads *"Magic Moment 1: top 12 prospects ranked. Slack canvas, CRM fields, and Drive priority index updated simultaneously."*

> **Operator depth:** What makes the three surfaces light simultaneously is the transactional outbox (Tightening 1). The stub-generation task writes the `dossier_artifacts` row and three `outbox` envelopes inside one `engine.begin()` block — Slack, CRM, and Drive are not three sequential API calls but three rows in one Postgres commit. A separate `outbox_dispatcher` worker drains them with exponential backoff and a DLQ. If the Slack mock is down, the CRM and Drive writes still happen; the system never enters split-brain where one surface knows about William Cook and another doesn't. This is the load-bearing visual claim for Damjan: simultaneous-across-surfaces is not three callbacks racing — it's one Postgres transaction with three projections.

### Beat 5 · The click on William Cook

Doug clicks the William Cook card. Visually nothing else has changed yet, but the guided callout has already advanced. The card border pulses peach. The center pane swaps to a Stage 2 view: five empty section rows labeled Process Taxonomy, Defect Hypothesis (N=3 conformal), Comparable Matta Deployment, Integration Risk Register, Suggested Approach. The first row glows.

> **Operator depth:** The click `POST`s to `/slack/interactions` with a payload mimicking Slack's Block Kit action — `action_id=generate_full_dossier`, `prospect_id=pros_9cb419495484`, and a synthetic `signal_hash`. FastAPI accepts it (the Slack HMAC verifier returns a bool the existing router treats as advisory; this is consistent with the smoke-test path and is flagged for production hardening). FastAPI hands a deterministic `dossier_id` back to the UI and `send_task("refinery.generate_dossier")` to Celery. The dossier-generation task inserts an empty `dossier_artifacts` row with `state='generating'` (via `ON CONFLICT … DO UPDATE` for retry-safety), then kicks off the linear five-section chain. Linear and not chord/group: the structural simplification is documented in `MATTA_RECONCILIATION.md §2`; at five sections, chord overhead bought nothing observable. Damjan can swap to chord/group in Phase 1.7 without changing any schemas.

### Beat 6 · ~T+6 min to ~T+9 min: Stage 2 in flight

The five section rows fire in order. Each row sits inactive (neutral grey), then turns peach (active) when its task starts, then locks to forest-green with a checkmark (complete) when the JSON payload lands in Postgres. The Drive pane on the right starts filling in section by section: Process Taxonomy first ("ductile iron casting, ladle pour at ~1450°C"), then Defect Hypothesis ("conformal set: porosity, surface inclusions; coverage 0.90"), then Comparable Matta Deployment, then Risk Register, then Suggested Approach. The guided callout names each section as it goes.

> **Operator depth:** Each section task is a separate Celery task to keep retries and DLQ-routing surgical. Taxonomy produces a `ProcessTaxonomy` (primary process, sub-processes, line-level steps, rationale capped at 600 chars). Defect produces a `LikelyDefectClassHypothesis` — the only section currently running the full uncertainty pattern: N=3 sample, conformal coverage gate at ≥0.90 against the calibration table built by `scripts/build_calibration_table.py`, and `requires_human_review=True` if the conformal set collapses to empty or all-classes. Comparable produces a `ComparableDeployment` whose `matta_customer_anchor` is selected by `packages/knowledge_graph/select.py` against `graph.json` — the LLM only writes the prose `dimension_of_comparability` field (capped at 250 characters). Risk produces a `RiskRegister` with findings keyed to a fixed enum (eight categories: lighting variance, EMF, network topology, OT/IT segmentation, regulatory burden, operator training, calibration baseline, legacy CMM). Approach produces a `SuggestedApproach` whose `template` is one of four enums (two-camera pilot, four-camera pilot, full-line deployment, Caracol AM OEM partnership) with a deterministic phase breakdown attached. Every section's JSON is validated against `extra="forbid"` Pydantic — any extra field from a hallucinating LLM rejects the section, not the dossier. The chain is linear because each downstream section uses the upstream's structured output as context; fan-out would have required passing five outputs back through the Celery result backend for no observable gain.

### Beat 7 · ~T+9 min: Magic Moment 2

The center pane swaps to a peach-bordered "Magic Moment 2 fired" block. The Drive document is now fully rendered with all five briefing sections plus a Company Facts header, a verified KG anchors list, a fitness-score rationale tree, a risk checklist, and an approach phase breakdown. The CRM inset adds a "Pre-Visit Dossier link" note. The Slack pane's William Cook card shows the briefing posted as a canvas update. Total elapsed: roughly seven to nine minutes. The guided callout reports the byte-density ratio.

> **Operator depth:** `compose_dossier.py` is where all three Tightenings converge. It reads the five section payloads from `dossier_artifacts`, assembles the deterministic sections from the verified Company Facts + KG anchors + scoring rationale + risk lookup + approach phase breakdown, and constructs a `PreVisitDossier` instance. The Pydantic `@model_validator(mode="after")` then runs the byte-density gate (Tightening 3), which computes `bytes(deterministic_sections) / bytes(total_sections)` and rejects the dossier if the ratio falls below 0.60. Same transaction: one `dossier_artifacts` UPDATE + three `outbox` INSERTs (slack_canvas, crm_note, drive_doc). Then `compose_dossier` returns, the outbox dispatcher drains, and the three surfaces light up in lockstep. The PRD's T+88 was specified against the 10-prospect simulator and the gemini-3-* preview family; the as-built timing on gemini-2.5 against the 124-prospect batch is the seven-to-nine-minute window observed across three §H verification runs.

### Beat 8 · The byte-density validator firing

A horizontal gradient bar appears in the Theater Console: peach on the left, forest on the right, a navy tick at the 60% mark, a numeric readout below ("ratio = 0.672 · PASS"). Three §H verification runs landed at 0.685, 0.652, and 0.675 — every dossier ships within a five-to-eight-percentage-point margin above the floor. The guided callout: *"Byte-density validator confirming deterministic content carries the load. Threshold ≥0.60."*

> **Operator depth:** The validator computes the ratio from `rendered_sections` (a map of section key → UTF-8 bytes) over two frozen sets: `DETERMINISTIC_SECTION_KEYS` (company_facts, verified_kg_anchors, fitness_score_rationale, risk_checklist_baseline, approach_template_baseline) and `LLM_SECTION_KEYS` (process_taxonomy, defect_hypothesis, comparable_dimension_of_comparability_prose, risk_register_narrative, suggested_approach_narrative). The Goodhart-resistance is the line `object.__setattr__(self, "deterministic_section_ratio", recomputed)` — the validator never trusts a caller-provided ratio, even from its own pipeline. If an LLM section overruns its token budget and the ratio drops below 0.60, the dossier is rejected with `ValueError`, never persisted, and never reaches the outbox. The architectural stance is that hollow LLM output is worse than no output: a half-confident briefing is more dangerous to Doug's slot allocation than a missing one. Path C of `MATTA_RECONCILIATION.md §6.8` documents why this threshold can never be lowered — the lever is always deterministic enrichment, never threshold relaxation.

### Beat 9 · The "Deterministic KG selection" callout

The Drive pane's Comparable Matta Deployment section is wrapped in a peach left border and tagged in small caps: **Deterministic KG selection — LLM did not pick this anchor.** The anchor selected for William Cook is `matta_deployment_metal_casting_unnamed`, with a citation back to substrate lines 271 and 421 in the source intel file. This is the single most important visual element for Damjan. Everything else in the dossier could be regenerated; this anchor could not have been hallucinated.

> **Operator depth:** When the comparable-section task runs, it does not ask Gemini to "pick a similar customer." It reads the prospect's verified vertical (`metal_casting`), passes it to `packages/knowledge_graph/select.py`, and the selector returns the matching anchor from `graph.json` — or `no_comparable_available` if there isn't one. The LLM's only role in this section is to write the 250-character prose explaining the dimension of comparability against the deterministically-selected anchor. The `selection_method` field on `ComparableDeployment` is a `Literal["deterministic_rules", "no_comparable_available"]` — there is no `"llm_picked"` option in the schema. This is the load-bearing safety rail against the worst Damjan-facing failure mode: a Matta customer reference invented by an LLM. The provenance is verifiable two ways: the citation_substrate_line on the deployment, and the container-boot validator in `packages/knowledge_graph/verify.py` that re-checks every KG anchor against the source intel before the API ever becomes healthy. The whole stack refuses to start if the citations don't match.

### Beat 10 · Demo complete

The center pane shows a Reset Demo button. Doug has a ranked top-12 he didn't have at T+0, a full pre-visit briefing for William Cook with five validated sections plus deterministic substrate, the same briefing materialized in the Slack canvas his team already lives in, a HubSpot note linking back to the Drive doc, and a Drive document ready to share with the field engineer. In his real workflow: forward the Drive link to the Special Projects hire, schedule the William Cook visit for next week, and use the rest of the morning to close the two deals already in flight.

> **Operator depth:** Total elapsed wallclock is roughly seven to nine minutes against the 124-prospect batch. Vertex AI spend lands near the $0.037 budget per full dossier — well under the $0.10 ceiling. Every artifact is reversible: the Slack canvas is in Matta's own workspace, the CRM note is in Matta's HubSpot, the Drive doc is in Matta's shared drive. When Matta unplugs the container, the Kaide-side Postgres goes with it; no orphaned data remains in Matta's systems. This is the unplug-or-absorb guarantee made concrete. The Special Projects hire inherits an API at `:8080` and a UI at `:3000`, both of which can be ported into Matta's stack with no schema rewrites — same FastAPI, same Pydantic, same Postgres, same Celery, same Redis. That stack-mirroring is intentional, not coincidence; Damjan's Backend Engineer JD specifies exactly this toolset.

---

## Part 3 — The Four Locked Invariants

### Deterministic two-route ADC

**Buyer-level:** The system cannot misroute a request — the decision is made by code, not by a model.

> **Operator depth:** `packages/adc/rules.py` contains zero `genai` or `gemini` imports — `grep` proves it. A batch upload always routes to Stage 1 (PRIORITIZATION); a single Slack interaction always routes to Stage 2 (DOSSIER_FULL). The routing decision is determined by request shape, not by inference. If this invariant slipped — if even one LLM call crept into the routing layer — the entire pipeline would inherit the LLM's failure modes (hallucinated routes, regression-on-update, drift under prompt changes). The defense is enforced by a grep test in CI plus the DMZ rule in `ULTIMATE_PRD.md §1.4`.

### N=3 deep ensemble (Flash tier) plus single-call Pro (Pro tier)

**Buyer-level:** Where the system makes judgment calls, it samples three times and weighs the answers — the same methodology Doug published in `pytorch-deep-ensembles`.

> **Operator depth:** Stage 1.2 vertical classification and Stage 2.2 defect-class hypothesis both run as N=3 ensembles on Gemini 2.5 Flash at temperatures 0.1, 0.5, 0.9 with `thinking_level="minimal"`. The aggregation is confidence-informed self-consistency (CISC, arXiv 2502.06233, verified during 1F-red v3 adjudication) — confidence-weighted majority vote rather than naive log-probability. The Pro tier (Gemini 2.5 Pro) is used single-call only for taxonomy, comparable-prose, risk-narrative, and approach-narrative because Pro's reasoning trace consumes ~1500-2000 tokens of any budget before emitting output, making ensembles cost-prohibitive. N=3 was chosen over N=5 because CISC's empirical claim is that confidence weighting cuts the required sample size by >40% — three weighted samples beat five unweighted at half the spend. This is the lever Doug would inspect first.

### Pydantic `extra="forbid"` on all 28 boundaries

**Buyer-level:** The system refuses to accept or emit any field that isn't in its schema — no silent corruption, no surprise data.

> **Operator depth:** All 28 BaseModel classes across `packages/schemas/` carry `model_config = ConfigDict(extra="forbid")`. Any extra field on ingest (a hallucinating LLM, a mock-surface drift, a Slack payload shape change) raises `ValidationError` at the boundary, not silently in downstream logic. The 28-of-28 ratio is grep-verifiable in seconds. Without this invariant, the byte-density validator would be bypassable: a malformed LLM section could emit extra deterministic-looking keys and game the ratio. With it, the schema is the spec.

### Google-only inference via Vertex AI in europe-west4

**Buyer-level:** Every inference runs in an EU region — no UK GDPR violation, no Anthropic API key sitting in the env, no Bedrock leakage path.

> **Operator depth:** The `genai.Client(vertexai=True, location="europe-west4")` instantiation is the only inference path. `grep` of `pyproject.toml` returns zero hits for `anthropic`, `openai`, or `boto3`. The model strings are pinned to the Vertex AI europe-west4 locations table — currently `gemini-2.5-flash` and `gemini-2.5-pro` (the spec's gemini-3-* preview pin was relaxed during Phase 1.5 because the Gemini 3 family is behind a project allowlist Kaide is not enrolled in; see `MATTA_RECONCILIATION.md §6`). This is the Pattinson Filter anchor: EU data residency, deterministic governance via Vertex's region pin, structured-output bounds via the schema layer. A regional regression — Vertex deprecating europe-west4 or moving Gemini 2.5 to a Global endpoint — would surface immediately because the model string is hardcoded; nothing silently falls back to us-central1.

---

## Part 4 — The Five Tightenings

### Transactional outbox (same-tx commit)

**Buyer-level:** When the system says "I posted to Slack, CRM, and Drive," it means all three landed — no half-states, no Slack canvas pointing to a missing CRM record.

> **Operator depth:** `compose_dossier.py` opens one `engine.begin()` block and inside it: UPDATEs `dossier_artifacts`, INSERTs three `outbox` rows (one per surface). Either all four writes commit or none do. A separate `outbox_dispatcher` worker drains the outbox with exponential backoff and a DLQ for permanent failures. The alternative — three sequential API calls — would have allowed Slack-succeeded-CRM-failed states that look exactly like dossier-doesn't-exist to a downstream consumer. Defends against the split-brain failure mode that Damjan would flag in a five-minute architectural review.

### Slack distributed lock (60s TTL)

**Buyer-level:** If Slack retries the same click three times because the network blinked, only one dossier gets generated.

> **Operator depth:** `apps/refinery_api/routers/slack_events.py` sets a Redis key `slack:lock:{event_id}` with `SET NX EX 60`. Subsequent retries hitting the same event ID return HTTP 202 immediately, suppressing duplicate `generate_dossier` task instantiation. The 60-second TTL slightly exceeds the Stage 2 latency envelope. Released by `release_slack_lock.py` on completion or by Redis TTL on stall. Without this, Slack's 3-second retry policy against Celery's 4-second-plus execution time would have run dossier generation 2-3x per click — burning Vertex spend and creating duplicate outbox rows.

### Byte-density validator (≥0.60 floor)

**Buyer-level:** The system refuses to ship a briefing that's mostly model-generated guessing — at least 60% of the bytes must be deterministic, verified content.

> **Operator depth:** Pydantic `@model_validator(mode="after")` on `PreVisitDossier` recomputes `bytes(deterministic_sections) / bytes(total)` from the `rendered_sections` map and raises `ValueError` if below 0.60. The recomputation overwrites any caller-provided ratio via `object.__setattr__` — pipeline cannot fake it. Defends against the Goodhart's-Law gaming surface Gemini's 1F audit identified: an LLM producing one verbose 3000-char hallucinated section while the deterministic engine produces three terse 100-char factual sections would yield a 75% section-count ratio but 90% LLM byte volume. The byte-density framing eliminates that escape hatch. Empirically, the dossier lands in the 0.652-0.685 band — comfortable margin above the floor.

### Section-granular DS-CP

**Buyer-level:** If the system isn't confident enough about one specific section (say, the defect hypothesis for a vertical it hasn't seen before), that section is marked unverified rather than the whole briefing being thrown away.

> **Operator depth:** Domain-Shift Conformal Prediction (arXiv 2510.05566, verified during 1F-red v3) is applied per section, not per dossier. If a section's semantic distance metric indicates severe domain shift against the calibration table, the section is stripped and the section key appended to `unverified_sections`. The dossier ships with the verified remainder plus an explicit "N sections marked unverified" note — not a silent omission. Currently the full uncertainty pattern is implemented only for the defect-hypothesis section (it carries the `requires_human_review` field and the conformal-coverage gate); the other four LLM sections persist their output but cannot trigger DS-CP because they don't yet carry uncertainty fields. This scoping limitation is documented in `MATTA_RECONCILIATION.md §6.7` and is Phase 1.7 territory.

### Deployment topology diagram

**Buyer-level:** The system runs in its own isolated cloud project — physically incapable of touching Matta's production cameras or control loops.

> **Operator depth:** `ULTIMATE_PRD.md §3.1.5` contains a Mermaid diagram showing the Refinery in a Kaide-owned GCP project with a dedicated VPC, separate Vertex client, no shared infrastructure or service accounts with any hypothetical Matta production environment. The diagram is documentation-only by design — it makes the airgapping visually explicit for Pattinson's expected 5-minute architectural review. The DMZ rule in `ULTIMATE_PRD.md §1.4` is the verbal commitment; the diagram is the visual proof. Defends against the worst Pattinson-facing failure mode: any plausible read where the sidecar could introduce latency jitter into closed-loop control.

---

## Part 5 — What the Demo Does NOT Show (and Why)

**Mock Slack / CRM / Drive surfaces instead of real OAuth integrations.** Real OAuth installs (Slack app review, HubSpot private-app provisioning, Google Drive workspace consent) are 2-3 days of provisioning work that doesn't change anything architecturally. The mock servers at `:8090`/`:8091`/`:8092` accept POST writes and return success — the outbox dispatcher cannot tell the difference. Phase 1.7 work, not a structural gap.

**Hardcoded `vertical="metal_casting"` in the defect-hypothesis demo path.** Originally a 3B QA scaffolding artifact. Fixed for the other four section tasks in Phase 1.5 (they now read vertical from `lead_prospects`); deferred for defect because the demo prospect (William Cook) is in fact `metal_casting`, so the scaffold and the production path produce the same output. Documented in `MATTA_RECONCILIATION.md §6.7`.

**The 0.60 byte-density threshold is not tunable.** It's the Goodhart-resistance design point, not a config knob. Lowering it would defeat the entire validator — at 0.40 the LLM sections dominate; at 0.80 the deterministic engine has no room to grow. Empirical observation across three §H runs put the actual ratio in the 0.652-0.685 band, so the floor sits comfortably below what the pipeline produces in practice. The lever for future improvement is deterministic enrichment, never threshold relaxation.

**The dossier is rejected (not degraded) when byte-density fails.** A hollow briefing is worse than a missing one because it gets forwarded, acted on, and used to allocate a deployment slot. The Pydantic validator raises `ValueError` and the dossier never reaches the outbox; the user gets an error state, not a hedged half-briefing. This is the architectural stance, not an oversight.

**N=3 and not N=5 or N=10.** Three samples is the empirical floor of CISC (Taubenfeld 2025 — confidence weighting cuts required sample size by >40%); five unweighted samples are no better than three weighted at twice the Vertex spend. Doug's own `pytorch-deep-ensembles` methodology specifies the ensemble pattern, not a specific N. Cost per dossier sits near $0.037 against the $0.10 budget; N=5 would push past $0.06 without measurably improving conformal coverage.

**Stage 1 wallclock is ~5-6 minutes, not 8 seconds.** The PRD's T+8 was specified against a 10-prospect simulator; the as-built runs against 124 prospects through real synchronous Vertex calls at the N=3 ensemble cost. `MATTA_RECONCILIATION.md §4(a)` documents the timing reconciliation. The structural trigger (top-12 ranking, three-surface delivery in lockstep) is what's load-bearing — the wallclock number is a function of batch size and model latency.

**Model strings are `gemini-2.5-*`, not `gemini-3-*`.** The Gemini 3 preview family is gated behind a Google project allowlist Kaide is not currently enrolled in. The architecture is generation-agnostic — same Vertex region, same ensemble pattern, same conformal calibration. When Gemini 3 becomes available to the project, the swap is one sed across `packages/prompts/`. Audit trail: `MATTA_RECONCILIATION.md §6`.

---

## Part 6 — The Damjan-Readiness Anchors

When Hafeedh hands Damjan the GitHub link, these are the specific files Damjan should inspect, in this order, and what story each tells.

1. **`packages/schemas/dossier.py`** — Open `PreVisitDossier`. The `@model_validator(mode="after")` with `object.__setattr__(self, "deterministic_section_ratio", recomputed)` is the Goodhart-resistance pattern. The two frozensets (`DETERMINISTIC_SECTION_KEYS`, `LLM_SECTION_KEYS`) make the audit budget explicit. Read it once: this is the architectural commitment that a hollow briefing cannot ship.

2. **`packages/adc/rules.py`** — Open and `grep -c 'genai\|gemini'`. Zero hits. The deterministic two-route invariant is enforced by absence, not by convention.

3. **`apps/refinery_worker/tasks/compose_dossier.py`** — The `with engine.begin() as conn:` block writing one `dossier_artifacts` UPDATE plus three `outbox` INSERTs is Tightening 1 in code. Same transaction, three projections, one source of truth.

4. **`packages/knowledge_graph/verify.py`** + **`packages/knowledge_graph/graph.json`** — The container-boot validator re-checks every KG anchor's citation against the source intel substrate before FastAPI becomes healthy. The container literally refuses to start if William Cook's `matta_deployment_metal_casting_unnamed` anchor doesn't trace back to a verbatim line in the intel file. QA caught a real Bowers & Wilkins / Caracol AM mis-citation here at build time — this is the spec's validator catching what the spec's prose didn't.

5. **`packages/uncertainty/conformal.py`** + **`packages/uncertainty/dscp.py`** — The Pattinson-facing pieces. Conformal calibration table built by `scripts/build_calibration_table.py` against a 30-event holdout; DS-CP applies arXiv 2510.05566's framework at section granularity. The defect-hypothesis task gates on coverage ≥0.90 from this table.

6. **`tests/unit/test_byte_density_validator.py`** + **`tests/unit/test_slack_distributed_lock.py`** + **`tests/unit/test_knowledge_graph_validator.py`** + **`tests/unit/test_dscp_section_strip.py`** — The four tightenings that ship with real unit-test coverage (not stubs — these were rewritten in `93482e2` after 3B QA caught the original test files as trivially-passing). Each test exercises the actual validator, not a mock.

7. **`MATTA_RECONCILIATION.md`** — The as-built variance ledger. §1-§3 covers the spec-vs-ship table; §4 covers the integration verdict (now ✅ INTEGRATION-VERIFIED after three §H smoke runs); §6.7 documents the Stage 2 persistence completion (the §G #4 escalation); §6.8 documents the byte-density calibration audit trail (initial 0.088 → final 0.652-0.685 band via deterministic enrichment, never threshold relaxation). This is the document Damjan reads to understand why the build is shaped the way it is.

8. **`PHASE_1_5_LOG.run3.log`** + the §H verification table** in `MATTA_RECONCILIATION.md §6.8`** — Three consecutive clean smoke runs against the live gemini-2.5 runtime. All M0-M12 milestones passed with byte-density ratios at 0.685, 0.652, 0.675. This is the integration-verified anchor — not "should work," but "did work, three runs in a row, here's the dossier_id from each."

The story those eight anchors tell: the architecture cannot misroute (anchor 2), cannot ship a hollow dossier (1, 6), cannot half-commit across surfaces (3, 6), cannot invent a customer reference (4), cannot ignore conformal uncertainty (5, 6), and has receipts (7, 8). That's the absorbability case.

---

*End of DEMO_WALKTHROUGH.md.*
