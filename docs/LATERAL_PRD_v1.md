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
