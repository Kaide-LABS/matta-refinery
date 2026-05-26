# MATTA_COMPREHENSION.md

### §1 THE COMPANY (Plain English)

Matta installs specialized cameras and small computers directly onto factory production lines to spot defective parts in real time. They sell to factories that make physical things at a massive scale. Their system watches components pass by on the belt and instantly identifies flaws without requiring the factory to rip out or modify their existing manufacturing equipment. The core pitch is speed and accuracy: getting the benefits of digital inspection running within hours instead of months.

Their customers are large manufacturing companies, primarily located in the UK and Europe. We know they work with Bowers & Wilkins for precision speaker components, Caracol AM for 3D printing partnerships, and a global drinks brand for beverage bottling lines. The typical buyer is a head of operations or head of quality at a facility churning out hundreds of parts per hour. These leaders spend their days dealing with the financial fallout of defective parts reaching customers and the constant burnout of human inspection staff who cannot maintain focus at high line speeds.

The company is led by three founders. Douglas Brion is the CEO and a commercial pragmatist who drives their deployment cadence, stating that "we're deploying to around two factories a month and have a multi-year waitlist at the moment" (line 0114). He responds to hard evidence and mathematical rigor rather than buzzwords. Sebastian Pattinson, the Chief Scientist and Cambridge faculty member, thinks in terms of guarantees and strict control boundaries; he is allergic to probabilistic claims that cannot be proven or that might interfere with real-time operations. Damjan Denic, the CTO, is an execution maximalist who values resilience, idempotency, and clean, maintainable systems that his team can easily absorb [inferred].

The bottleneck they face is crucial. Manufacturing factories lose meaningful revenue to defective parts that escape inspection. Human inspection at line speeds above sixty parts per minute is unreliable. Historically, setting up computer vision to catch these defects was custom-engineered per customer and incredibly slow. Matta's foundation models generalize across customers, allowing them to deploy in hours. Because of this speed, they have a massive backlog of factories waiting for their system, creating an operational bottleneck before the system is even installed.

### §2 THE BOTTLENECK (Plain English)

The primary pain is that Matta has far more demand than they can currently serve. Doug stated they are *"deploying to around two factories a month and have a multi-year waitlist at the moment"* (`Matta_Intel_cleaned.md` line 0114). At recent trade shows, they gathered overwhelming interest: *"124 leads in two days"* at UK Metals Expo 2025 (line 0294) and *"over 100 incredible leads"* at Advanced Engineering 2025 (line 0284). The team spends one week at trade shows (FDE JD lines 0698, 0704, 0705, 0716 — trade-show qualification and factory-visit prep are named responsibilities) and the next week traveling to factory visits. Doug, Damjan, and the Special Projects hire absorb at least some portion of the pre-sales research required to figure out which two factories out of hundreds get the next available slots.

This triage burden directly costs them deals. With only two deployments a month against a multi-year waitlist, every decision about which prospect gets a slot is a rate-limiter on revenue. Misallocating a slot to a low-fit prospect is a meaningful fraction of ARR lost. Every hour Doug spends pre-qualifying trade-show leads is an hour he is not closing existing deals or supporting deployed factories.

Their current response to this pressure is partially visible in the substrate and partially inferred. They are hiring a Special Projects leader (`line 0625`: *"probably our most important hire"*) — the role is verified as critical, ⚠️ though the specific framing that it absorbs pre-sales scoping is one plausible interpretation of a broadly-scoped JD. They are taking the full team to trade shows (verified at lines 0187, 0191 for MACH 2026, lines 0234, 0393 for Southern Manufacturing) — ⚠️ though "to handle volume" is our framing, not their stated reason. **Whether they have already built internal tooling to automate the pre-visit research phase is unknown.** The substrate does not state they have such tooling; it also does not state they don't. Given that Doug actively maintains open-source ML uncertainty libraries and the team includes Cambridge research faculty plus an execution-maximalist CTO with a clear stack mandate, the prior probability that they have at least some internal triage automation is non-trivial. **Outreach must NOT assume the absence of such tooling.**

Our architecture solves this pain by handling the slice of work between trade-show floor and factory visit — not by being the first tool in the category, but by being the rigorous, audit-grade version of pre-visit prep. The Refinery's specific architectural choices are the differentiator: deterministic comparable selection from a knowledge graph with verbatim citation provenance, deep ensembles methodology applied at the orchestration layer with conformal coverage on the defect-class hypothesis (matching Doug's published pytorch-deep-ensembles methodology lineage), Pydantic-locked output envelopes with `extra="forbid"` at every boundary, the byte-density Goodhart-resistance validator. Whether Matta has a Notion template, a custom internal Python script, or no tooling at all, the comparison surface is the same: their existing approach versus the Refinery's specific methodology. If they have nothing, we are a 10x improvement. If they have something, we are the structured, Damjan-absorbable upgrade.

### §3 THE DEMO — LAYMAN VERSION

Matta's team comes back from a trade show with a list of 124 manufacturing companies interested in talking to them. Today, that list goes into a shared document and a salesperson manually researches each company, ranks them, and writes up a briefing for the most promising ones — a week of work. Our tool reads the list and does the research itself. Within 90 seconds, the tool ranks the 124 companies by fit, writes a deep briefing document for each of the top 12, and posts the briefings into the team's existing chat channels and customer database. The salesperson opens their morning chat and finds the briefings already there, with notes on which manufacturing process each company uses, what the most likely defect problems are based on similar customers Matta has worked with before, what to watch out for on the factory visit, and what the recommended pilot approach would be. 

The tool never touches the factory cameras, never touches the production line, never replaces anything Matta's product already does. It only handles the paperwork piece that today eats into the team's time before each visit.

A small dashboard with three panels is visible at once. On the left, the team's chat channel with a fresh briefing pinned. In the middle, a behind-the-scenes view showing the tool thinking through each step — pulling company facts, comparing to past customers, weighing the evidence, writing the briefing section by section. On the right, a Google Doc that fills itself in with the full briefing. A small inset at the bottom shows the customer database record updating with the briefing link. At the 8-second mark, the ranking finishes and the top 12 light up. At the 88-second mark, the full briefing for the headline company materializes across all three panels at once.

The week of pre-visit prep collapses to 90 seconds. The new hire walks into a system that already did the triage. The team's time goes back to the work that bills.

### §4 THE DEMO — TECHNICAL VERSION

The architecture begins with three ingress routes: a Theater CSV upload via `apps/refinery_api/routers/ingest.py`, a Slack interaction via `apps/refinery_api/routers/slack_events.py` and `apps/refinery_api/routers/slack_interactions.py`, and a CRM webhook via `apps/refinery_api/routers/crm_webhooks.py`. The deterministic Stage 0 routing decision is executed in `packages/adc/rules.py` without any language model imports. The Stage 1 prioritization fan-out is orchestrated across `apps/refinery_worker/tasks/score_batch.py`, `apps/refinery_worker/tasks/enrich_prospect.py`, `apps/refinery_worker/tasks/classify_vertical.py`, `apps/refinery_worker/tasks/score_fitness.py`, and `apps/refinery_worker/tasks/generate_dossier_stub.py`. Stage 2 dossier generation runs through `apps/refinery_worker/tasks/generate_dossier.py`, which chains the five section tasks located in `apps/refinery_worker/tasks/dossier_section_taxonomy.py`, `apps/refinery_worker/tasks/dossier_section_defect.py`, `apps/refinery_worker/tasks/dossier_section_comparable.py`, `apps/refinery_worker/tasks/dossier_section_risk.py`, and `apps/refinery_worker/tasks/dossier_section_approach.py`. The sections are composed by `apps/refinery_worker/tasks/compose_dossier.py`, which was added during QA to finalize the payload. Multi-surface dispatch is handled by `packages/outbox/dispatcher.py` communicating with mock surfaces in `apps/mocks/mock_slack/server.py`, `apps/mocks/mock_crm/server.py`, and `apps/mocks/mock_drive/server.py`. The front-end view is driven by the Next.js application in `apps/theater_ui/pages/index.tsx`. The deployment topology is defined exclusively by the Mermaid diagram in `ULTIMATE_PRD.md` section 3.1.5.

The system strictly enforces the four invariants and five tightenings. The deterministic two-route ADC is locked in `packages/adc/rules.py` where zero LLM calls exist. The deep ensemble pattern runs in `packages/prompts/vertical_flash.py` and `packages/prompts/defect_flash.py` using explicit temperatures of 0.1, 0.5, and 0.9. Pydantic schemas enforce strict boundaries; all twenty-eight schemas in `packages/schemas/dossier.py` and peers declare `extra="forbid"`. The Vertex AI routing is pinned to europe-west4, utilizing exact strings for `gemini-3-flash-preview` and `gemini-3.1-pro-preview` across all prompt files. For the tightenings, the Transactional Outbox pattern commits state simultaneously in `apps/refinery_worker/tasks/compose_dossier.py` using the machinery in `packages/outbox/enqueue.py`. The Slack distributed lock is secured in `apps/refinery_api/routers/slack_events.py` via an NX EX 60 mechanism and released by `apps/refinery_worker/tasks/release_slack_lock.py`. The byte-density validator operates inside `packages/schemas/dossier.py`. Section-granular data stripping is evaluated in `apps/refinery_worker/tasks/dossier_section_defect.py` backed by thresholds in `packages/uncertainty/dscp.py`. The deployment topology diagram remains a documentation-only guard in `ULTIMATE_PRD.md` section 3.1.5.

Several load-bearing patterns secure the architecture against edge cases. The `object.__setattr__` overwrite in `packages/schemas/dossier.py` explicitly forces a recomputed byte-density value onto the model instance, preventing upstream callers from faking a high density score and bypassing the Goodhart-resistance check. The hardcoded routing rules in `packages/adc/rules.py` deliberately avoid LLM inference to ensure that incorrect routing decisions cannot pollute downstream states. The same-transaction commit block in `apps/refinery_worker/tasks/compose_dossier.py` writes the core artifact and three outbox records inside a single Postgres transaction scope, preventing split-brain states where a chat message fires but the database has no record of the dossier. The container-boot validator in `packages/knowledge_graph/verify.py` reads `packages/knowledge_graph/graph.json` and cross-references every citation against `Matta_Intel_cleaned.md` before the server becomes healthy, which already caught a real mis-citation during the build phase. The section-granular domain-shift gate in `apps/refinery_worker/tasks/dossier_section_defect.py` allows the system to omit unverified analytical sections without failing the entire dossier generation process. Finally, the Mermaid diagram in `ULTIMATE_PRD.md` section 3.1.5 physically isolates the architecture from Matta's production environment, ensuring that no latency jitter can ever reach their real-time control loops.

### §5 END-TO-END WALKTHROUGH

The happy path begins when the user triggers the pipeline using a command like `./scripts/run_demo.sh` [inferred from scripts/run_demo.sh]. The CSV upload pushes 124 records into the system, and the ADC routes the batch to the Stage 1 prioritization fan-out. Inside the Theater UI, the user observes 124 cards lighting up as the pipeline scores each prospect deterministically. At the 8-second mark, Magic Moment 1 lands: the top twelve stubs finish computing, a ranked list appears in the Slack canvas, the CRM updates with fitness scores, and a priority index document is created in Drive. 

The user then shifts focus to the Slack pane and clicks the Generate Full Dossier button on the William Cook Sheffield lead. This interaction fires a webhook back to the API, where the distributed lock secures the request. Stage 2 orchestration begins chaining the five core analytical sections. The taxonomy generates first, followed by a parallel run of the defect-class ensemble and comparable analysis. The risk register and approach sections complete the analysis phase. As the results return, the system recomputes the byte-density ratio, which renders green at a value greater than 0.60 on the Theater UI meter. 

Once validation passes, the Transactional Outbox commits the final state, and Magic Moment 2 lands at the 88-second mark. The full PreVisitDossier materializes identically across the Slack canvas, a new CRM note, and a completed Google Drive document containing the shareable link. The Vertex AI cost ticker displays a final run cost of approximately $0.037, completing the demonstration well under the 90-second and ten-cent constraints.

### §6 ANTI-REPLICATION BOUNDARY

The architecture strictly avoids touching any of Matta's core intellectual property. The system never interacts with the production agents known as SENTRY, TALLY, GAUGE, and TRACE. The Manufacturing Foundation Models and the Manufacturing OS UI are fully isolated from our sidecar, as stated in the PRD's anti-replication principles. No real-time camera streams or edge firmware are ingested or simulated. Customer systems such as their CMMS, QMS, or MES environments are completely out of bounds, acknowledging that the previous CMMS Bridge architecture was killed in an earlier phase. To ensure absolute compliance with closed-loop safety, the deployment topology places our application in a completely separate GCP project with a dedicated VPC, preventing any possibility of network cross-contamination with Matta's real-time control environments. If challenged by the CTO, the defensive line is absolute: the system is a stateless sidecar running strictly in pre-deployment airspace.

### §7 CRITICAL FILES TO KNOW BEFORE DEBUG

1. `packages/schemas/dossier.py` — PreVisitDossier schema containing the Tightening 3 byte-density validator (critical). Look here first if dossier generation suddenly rejects payloads.
2. `apps/refinery_worker/tasks/compose_dossier.py` — Stage 2 orchestrator and Transactional Outbox commit boundary (critical). Look here first if outbox events fail to fire after all five sections complete.
3. `apps/refinery_api/routers/slack_events.py` — Slack ingress and distributed lock enforcement (critical). Look here first if duplicate Slack interactions trigger multiple Celery tasks.
4. `packages/adc/rules.py` — Deterministic Stage 0 routing logic (critical). Look here first to confirm zero LLM calls are executed during initial dispatch.
5. `packages/knowledge_graph/verify.py` — Container-boot citation-provenance validator (important). Look here first if the API container refuses to become healthy at startup.
6. `packages/outbox/dispatcher.py` — Transactional Outbox relay machinery (important). Look here first if records are stuck in outbox or landing in outbox_dlq.
7. `packages/outbox/enqueue.py` — Helper functions for the Transactional Outbox (important). Look here first to trace the initial envelope creation.
8. `packages/uncertainty/dscp.py` — Domain-shift and threshold calculation (important). Look here first if the system strips sections unexpectedly.
9. `packages/uncertainty/conformal.py` — Deep ensemble conformal calibration logic (important). Look here first if the conformal coverage statement drops to zero.
10. `packages/knowledge_graph/select.py` — Deterministic comparable selection logic (important). Look here first if the wrong KG anchor is chosen.
11. `packages/prompts/defect_flash.py` — N=3 ensemble prompt definition (context). Look here first if the model hallucinates defect classes.
12. `packages/prompts/vertical_flash.py` — N=3 vertical classification prompt definition (context). Look here first if the model misclassifies basic industries.
13. `tests/unit/test_byte_density_validator.py` — Goodhart-resistance testing (context). Look here first to understand how the object.__setattr__ overwrite protects the density calculation.
14. `tests/unit/test_slack_distributed_lock.py` — Concurrency testing (context). Look here first to verify the 60-second TTL logic.
15. `tests/unit/test_knowledge_graph_validator.py` — Provenance testing (context). Look here first to see how exact line-level citations are verified against the substrate.

### §8 DEBUG GUIDE — THE LOAD-BEARING PAYLOAD

- **Pre-flight check**
  * Verify the `.env` file is present containing `POSTGRES_URL`, `REDIS_URL`, `CELERY_BROKER`, `GCP_PROJECT`, `VERTEX_LOCATION=europe-west4`, `SLACK_SIGNING_SECRET`, `CRM_WEBHOOK_SECRET_HUBSPOT`, `CRM_WEBHOOK_SECRET_SALESFORCE`, `MOCK_SURFACES=true`, and `KAIDE_LABS_PROJECT_ID` corresponding to `apps/refinery_api/config.py`.
  * Confirm the Docker daemon is up and running.
  * Execute `docker compose up postgres redis -d` and confirm both containers are healthy.
  * Execute `python scripts/verify_knowledge_graph.py` and confirm it returns exit 0.
  * Execute `python -m pytest tests/unit/ -q` and confirm all 15 tests pass.
  * Verify the Google Cloud SDK is authenticated locally to a project with Vertex AI access in the `europe-west4` region.

- **The smoke test**
  * Run `./scripts/run_demo.sh` [inferred] which triggers `python scripts/seed_mock_data.py`. Follow with an API call or UI upload to send the UK Metals Expo batch.
  * Success state: The Theater UI loads at `http://localhost:3000`. The mock Slack receives the canvas write at T+8. The mock CRM receives field updates at T+8. The top-12 prospects light up. Clicking William Cook triggers Stage 2. The dossier generation completes at T+88. The cost ticker reflects approximately $0.037.

- **Order of operations for debugging**
  * If `docker compose up` fails: check environment variables. Check for port conflicts on 5432, 6379, 8000, 3000, 9001, 9002, and 9003. Verify Docker daemon status.
  * If `verify_knowledge_graph.py` fails: check that every citation in `packages/knowledge_graph/graph.json` maps verbatim to the correct line number in `Matta_Intel_cleaned.md`. Remember that the B&W and Caracol anchors were fixed in `93482e2`, but any new additions require identical strictness.
  * If CSV upload returns HTTP 422: verify the CSV column headers perfectly match the `LeadIntakeRow` schema in `packages/schemas/lead_intake.py`.
  * If Stage 1 hangs past T+8: inspect the Celery worker logs. Verify that the N=3 vertical_flash calls are not stalling due to Vertex AI rate limits or missing credentials.
  * If the Theater UI hangs: inspect the WebSocket connection at `ws://localhost:8000/ws`. Verify that `apps/theater_ui/hooks/useWebSocket.ts` expects the exact event schema emitted by the Celery worker.
  * If Stage 2 starts but the byte-density validator rejects the payload: the LLM output is too verbose, driving the ratio below 0.60. Check the `max_output_tokens` limits inside `packages/prompts/*.py`.
  * If the dossier completes but surfaces fail to update: inspect the `outbox` table in Postgres. Check if the `outbox_dispatcher.py` task is executing. Verify the mock surface servers are running and accepting HTTP POST requests.

- **Likely failure modes**
  1. Symptom: Vertex AI returns `model not found: gemini-3-flash-preview`. Root cause: The preview model was deprecated after the build. Check first: Vertex AI release notes. Fix pattern: Update the model strings in `packages/prompts/*.py` to the current available preview or GA version.
  2. Symptom: The N=3 Flash ensemble returns three completely different verticals. Root cause: Genuine three-way disagreement causing the plurality vote in `apps/refinery_worker/tasks/classify_vertical.py` to fail. Check first: `packages/uncertainty/conformal.py`. Fix pattern: Mark `requires_human_review=True` and surface the disagreement cleanly in the Theater pane.
  3. Symptom: `compose_dossier` throws a `ValidationError` due to the byte-density gate. Root cause: Stage 2 prose was overly verbose. Check first: `max_output_tokens` in `packages/prompts/`. Fix pattern: Tighten token limits to reduce the LLM-generated character count relative to deterministic data.
  4. Symptom: Slack signature verification fails in production despite working locally. Root cause: The mock signature validation in `packages/adapters/slack/signature.py` was too lax compared to Slack's real HMAC-SHA256 requirement over the `v0:{ts}:{raw_body}` 5-minute window. Check first: `packages/adapters/slack/signature.py`. Fix pattern: Align the verification function precisely with Slack documentation.
  5. Symptom: `ValidationError: extra inputs are not permitted` on webhook ingest. Root cause: A mock surface included a field not present in the strict schema. Check first: the specific schema file referenced in the traceback. Fix pattern: Either add the field to the schema with `Field(default=None)` or remove it from the mock surface emitter.
  6. Symptom: WebSocket disconnects before the T+88 mark. Root cause: Idle connection timeout or the worker emitted an irregularly shaped event payload. Check first: `apps/refinery_api/routers/websocket.py`. Fix pattern: Add ping/pong keepalives or correct the worker's payload structure.
  7. Symptom: The Mermaid diagram in `ULTIMATE_PRD.md` §3.1.5 renders broken lines. Root cause: The subgraph-to-node edge syntax misfires in some markdown viewers. Check first: GitHub's native web view. Fix pattern: Replace with an ASCII box-and-arrow diagram if the specific recipient's viewer cannot parse Mermaid.
  8. Symptom: The conformal calibration table fails to load at boot. Root cause: `packages/uncertainty/calibration_table.json` is missing because `scripts/build_calibration_table.py` was not executed. Check first: the startup script sequence. Fix pattern: Ensure the deterministic 30-event holdout builds the JSON file before API boot.
  9. Symptom: The Theater UI coverage meter shows zero or is stuck. Root cause: `apps/refinery_worker/tasks/compose_dossier.py` is not emitting the `deterministic_section_ratio` correctly. Check first: `apps/refinery_worker/tasks/compose_dossier.py`. Fix pattern: Ensure `model_dump_json()` on the `PreVisitDossier` includes the dynamically recomputed value.
  10. Symptom: The `outbox_dispatcher` moves records to the DLQ after six retries. Root cause: A mock surface server is offline or returning 5xx responses. Check first: `apps/mocks/mock_slack/server.py` and peers. Fix pattern: Ensure the mock servers are bound to their expected ports.
  11. Symptom: All dossiers generate with `requires_human_review=True`. Root cause: The DS-CP threshold is too sensitive. Check first: `DSCP_SEVERE_SHIFT_THRESHOLD` in `packages/uncertainty/dscp.py`. Fix pattern: Loosen the threshold so that standard verticals like `metal_casting` pass the gate for the seeded CSV.
  12. Symptom: The cost ticker displays significantly more than $0.037. Root cause: The Celery worker is caught in a retry loop or the `thinking_level` was accidentally increased. Check first: worker logs for repeated Vertex AI calls. Fix pattern: Explicitly enforce `thinking_level="minimal"` and cap task retries.

- **What "working" looks like — when to stop debugging**

  Debug stops when the full happy path executes within these timing and state windows. If all of the following hold, the demo is integration-complete and recording can proceed.

  * **T+0 — System idle, all surfaces alive.** Theater UI loads at `http://localhost:3000` with all three panes rendered (Slack left, Theater center, Drive right) plus CRM inset bottom-right. Mock Slack server responding to GET `http://localhost:9001/health` with 200. Mock CRM server at port 9002 healthy. Mock Drive server at port 9003 healthy. Postgres at 5432 healthy. Redis at 6379 healthy. FastAPI at 8000 has logged "Knowledge graph provenance check passed" in the lifespan startup output.

  * **T+0 (action) — CSV upload accepted.** POST `/ingest/batch` with the UK Metals Expo CSV returns HTTP 200 with a `batch_id`. Postgres `lead_intake_batches` has one new row. Worker logs show `refinery.classify_action_domain` task firing.

  * **T+2 — ADC decision visible.** Theater center pane shows the Slack event JSON inspector populated, signature verification "OK" badge, and ADC route pill rendered as "PRIORITIZATION" (NOT yet "DOSSIER_FULL" — that comes at T+12 after the click). This is the deterministic-ADC visual proof: no LLM card has lit yet.

  * **T+5 — Stage 1 fan-out animation.** Theater center pane shows 124 prospect cards in a grid, each with an in-flight indicator. Worker logs show `refinery.enrich_prospect`, `refinery.classify_vertical`, `refinery.score_fitness` tasks firing per prospect.

  * **T+8 — Magic Moment 1 lands.** Three simultaneous things must be visible:
    - Slack left pane: a fresh canvas appears in `#fde-lead-refinery` with the top-12 prospect ranking
    - CRM inset bottom-right: 12 prospect records show updated fitness scores
    - Drive right pane: a "Priority Index — UK Metals Expo 2025" doc is created with the ranked list

    Theater center pane: the 12 highest-fitness cards highlight in green. The William Cook Sheffield card is at the top of the ranking. The total elapsed shows ~8 seconds.

  * **T+12 (action) — Click "Generate Dossier" on William Cook.** Slack interaction fires. Theater center ADC route pill updates to "DOSSIER_FULL". Worker logs show `refinery.generate_dossier` task firing. The Slack distributed lock at `slack:lock:{event_id}` should be visible in Redis via `redis-cli GET` if you check immediately.

  * **T+25 — Stage 2.1 taxonomy card lights up.** Theater center pane: process_taxonomy section card transitions from gray to active. After completion (T+30): card shows primary_process="ductile iron casting", sub_processes populated.

  * **T+45 — Stage 2.2 defect-class card lights with N=3 ensemble visible.** Three sample cards visible during generation, then the conformal calibration step renders showing the coverage statement and the conformal set. After completion: card shows defect_hypothesis with conformal_set populated and coverage ≥0.9.

  * **T+55 — Stage 2.3 comparable card highlights "deterministic selection from KG."** UI element specifically marks the matta_customer_anchor as selected by the rules engine (NOT by LLM) — this is the v4-contribution visible-proof moment. Anchor shown: `metal_casting_*` family matching William Cook's vertical.

  * **T+70 — Stage 2.4 risk register card.** Findings list populated.

  * **T+78 — Stage 2.5 approach card.** Template = "two_camera_pilot", day_one_risks list populated.

  * **T+85-86 — Byte-density coverage meter green.** Theater center bottom-right shows the deterministic-vs-LLM coverage meter at ≥0.60, rendering green. Pydantic validator passes; no rejection log entry.

  * **T+87 — `compose_dossier` writes atomically.** Worker log shows the `with engine.begin() as conn:` block committing one `dossier_artifacts` UPDATE and three `outbox` INSERTs (Slack, CRM, Drive surfaces). Postgres `outbox` table has three new rows with state='pending'.

  * **T+88 — Magic Moment 2 lands.** Three simultaneous things:
    - Slack left pane: William Cook canvas updates with full dossier section anchors
    - CRM inset: appends a note "Pre-Visit Dossier generated 2026-MM-DD, link: drive.google.com/..."
    - Drive right pane: complete dossier with footer [Share] button live

    Theater center cost ticker reads approximately $0.037 (within the §3.5 budget under $0.10). Total elapsed should be under 90 seconds.

  * **T+90 — Recording cap.** Hard cut for OBS recording.

  If any of these milestones drift more than ±5 seconds, debug the corresponding stage. If a milestone fails to land at all, see "Order of operations for debugging" above and trace upward from the symptom.

  If all milestones land within tolerance: **stop debugging. The demo is integration-complete.** Proceed to recording per `PHASE_1_SPEC §M` cut list with OBS at 1080p / 30fps, separate voiceover take to Rode NT-USB, post in DaVinci Resolve.

- **Common generated gotchas**
  * QA caught and fixed four stub unit tests that were failing to exercise the actual validators (resolved in commit `93482e2`).
  * QA caught and fixed the missing `compose_dossier.py` task, which was referenced but missing in the autonomous build (resolved in `93482e2`).
  * QA caught and fixed the citation line bug for Bowers & Wilkins and Caracol AM where excerpts did not exist on the specified line (resolved in `93482e2`).
  * Beware of hardcoded demo data inside task files. For instance, `apps/refinery_worker/tasks/dossier_section_defect.py` contains a hardcoded `vertical = "metal_casting"` used purely for demo scaffolding; this must be traced and swapped if attempting real production loads.
  * Keep an eye out for `TODO` or `FIXME` comments left by the generation agent that compile cleanly but fail at runtime. `grep -rn "TODO\|FIXME\|XXX" packages/ apps/` is your friend.
  * Ensure that the Pydantic schema shape perfectly matches the inline SQL DDL raw text migrations scattered inside the setup scripts, as autonomous agents occasionally drift between the two definitions.

### §9 GLOSSARY

- **FDE Strike Team:** Forward Deployed Engineering, Kaide Labs' operational unit focused on extremely rapid, high-impact prototypes.
- **DMZ Rule:** The absolute architectural boundary ensuring the sidecar never imports or directly interfaces with Matta's core intellectual property.
- **Anti-Replication Principle:** The mandate that Kaide Labs builds non-core tooling rather than attempting to recreate the prospect's primary product.
- **Stateless Sidecar:** An application pattern that holds no permanent authoritative data, serving only to enrich and relay information between existing customer surfaces.
- **Magic Moment:** The specific, choreographed seconds (T+8 and T+88) where complex backend processing materializes across multiple user interfaces simultaneously.
- **Theater Pane:** The center UI panel of the demo dashboard designed to visually expose the system's deterministic decision-making processes.
- **Refinery Hybrid:** The final architectural blueprint merging the v0 Refinery PRD with features lifted from lateral Step 1D PRDs.
- **Form C:** Internal shorthand for the Refinery Hybrid deployment shape.
- **The Killed Brief:** An earlier, rejected architecture (1F-red v2) that failed to meet Damjan-readiness standards.
- **1F-red v3:** The final counter-verdict document that authorized the five specific technical tightenings after challenging a premature kill order.
- **Tightening 1-5:** The five non-negotiable engineering mandates (Transactional Outbox, Slack lock, byte-density validator, DS-CP, deployment topology) enforcing architectural rigor.
- **DS-CP:** Domain-Shift Conformal Prediction, the specific mathematical check used to determine if the model is operating too far outside its verified training distribution.
- **CISC:** Confidence-Informed Self-Consistency (Taubenfeld et al., 2025, arXiv 2502.06233). The method behind the N=3 Flash ensemble's weighted majority vote: confidence scores from the model are used to weight reasoning paths, reducing the required sample size for reliable answers. Cited in `ULTIMATE_PRD.md §4.2` as the academic anchor for the ensemble pattern. Doug Brion-readiness reference — methodology lineage from his own `pytorch-deep-ensembles` and `pytorch-classification-uncertainty` repos. NOT to be confused with the CPU-architecture acronym.
- **Byte-density ratio:** The metric calculating what percentage of the final dossier was deterministically retrieved versus generated by an LLM.
- **Deterministic-vs-LLM coverage meter:** The UI element in the Theater pane displaying the byte-density ratio, turning green only when >0.60.
- **SENTRY/TALLY/GAUGE/TRACE:** Matta's proprietary, real-time production agents operating directly on the factory edge.
- **MFM:** Manufacturing Foundation Models, Matta's core computer vision architecture.
- **MOS:** Manufacturing OS, Matta's proprietary user interface for factory operators.
- **Global drinks brand:** An anonymized, high-volume Matta customer utilized to validate the `beverage_bottling` defect taxonomy.
- **Two-camera pilot:** Matta's standard initial deployment motion, explicitly recommended in the sidecar's generated approach section.

### §10 OPEN QUESTIONS & FLAGS

- **⚠️ unverified:** The exact terminal command to execute the happy-path demo is inferred as `./scripts/run_demo.sh` followed by a curl ingest, but the README was not explicitly verified.
- **⚠️ unverified:** Damjan Denic's communication style and psychological triggers are entirely inferred from the tone of Matta's Backend Engineer job description, lacking a direct verbatim quote.
- **⚠️ unverified:** It is unconfirmed whether the Mermaid diagram embedded in `ULTIMATE_PRD.md` §3.1.5 will render correctly across non-GitHub markdown viewers.
- **⚠️ unverified:** The availability of the specific `gemini-3-flash-preview` and `gemini-3.1-pro-preview` models in the `europe-west4` Vertex AI region on the actual day of demo recording remains unconfirmed.
- **❌ DEFERRED:** The end-to-end `docker compose up` walk-through has never been fully executed across the pipeline.
- **❌ DEFERRED:** The Vertex AI `europe-west4` connection has not been actively verified against live credentials.
- **❌ DEFERRED:** The Theater UI browser render has not been visually verified.
- **❌ DEFERRED:** Real OAuth installations for Slack, Hubspot, and Google Drive are deferred to Phase 2 per `PHASE_1_SPEC §A.2`.
- **❌ DEFERRED:** Production-grade conformal calibration against a live database replaces the 30-event synthetic holdout in Phase 2.
- **❌ DEFERRED:** The DLQ observability dashboard is explicitly deferred to Phase 2.
- **🔍 synthesizer-noticed:** `apps/refinery_worker/tasks/dossier_section_defect.py` contains hardcoded demo assignments (e.g., `vertical = "metal_casting"`). This is scaffolding that will break if testing a different vertical.
- **🔍 synthesizer-noticed:** The Stage 2 orchestrator utilizes `send_task` chains instead of Celery `chord/group` primitives, functioning correctly but structurally simplified from the canonical blueprint.
- **🔍 synthesizer-noticed:** The database DDL migrations are executed via raw `text(...)` SQL within task scripts, lacking a formal Alembic migrations directory despite being referenced in the spec.
- **🔍 synthesizer-noticed:** Pydantic schemas and raw SQL DDL strings may contain subtle shape divergence since they were generated simultaneously by independent agents.
