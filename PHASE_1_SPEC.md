# PHASE_1_SPEC.md

**Kaide Labs — Forward Deployed Engineering Strike Team**
**Target:** Matta (https://www.matta.ai/)
**Document:** Phase 1 technical blueprint for the Refinery Hybrid
**Architecture spec:** `ULTIMATE_PRD.md` (commit `40d6b92`, post-1F-red v3 tightenings)
**Authorizing verdict:** `validation_gate_1f_red_v3.md`
**Status:** BUILDING
**Sprint window:** 48–72h Phase 1 build. ~7.5h of that budget is the five 1F-red v3 tightenings (per validation gate's cost-accounting).

---

## §A. Scope Discipline and Anti-Sprawl Constraints

### A.1 — In Scope for Phase 1

| Stage / system | PRD anchor | Status |
|---|---|---|
| Stage 0 deterministic two-route Action Domain Classifier | `ULTIMATE_PRD.md` §3.2 | **BUILD** |
| Stage 1.1 deterministic enrichment (allowlist, no LLM) | §3.3 step 1.1 | **BUILD** |
| Stage 1.2 vertical classification (N=3 Flash ensemble) | §3.3 step 1.2 | **BUILD** |
| Stage 1.3 deterministic fitness scoring | §3.3 step 1.3 | **BUILD** |
| Stage 1.4 queue assembly + Slack canvas + CRM fields + Drive priority-index | §3.3 step 1.4 | **BUILD** |
| Stage 1.5 deterministic dossier stubs for top-12 (no LLM) | §3.3 step 1.5 (v1 contribution) | **BUILD** |
| Stage 2.1 process taxonomy (Pro N=1, `thinking_level="medium"`) | §3.4 step 2.1 | **BUILD** |
| Stage 2.2 defect-class hypothesis (Flash N=3 + conformal calibration) | §3.4 step 2.2 | **BUILD** |
| Stage 2.3a deterministic comparable selection from KG | §3.4 step 2.3a (v4 contribution) | **BUILD** |
| Stage 2.3b Pro prose for `dimension_of_comparability` ≤250 chars | §3.4 step 2.3b | **BUILD** |
| Stage 2.4 risk register (Pro N=1, fixed taxonomy) | §3.4 step 2.4 | **BUILD** |
| Stage 2.5 suggested approach (Pro N=1, fixed template library) | §3.4 step 2.5 | **BUILD** |
| Stage 2.6 `allowed_evidence[]` whitelist | §3.4 step 2.6 (v3 contribution) | **BUILD** |
| Slack canvas + slash command + interactions surface (mocked) | §3.1, §5.1 | **BUILD** |
| CRM note + structured fields surface (mocked) | §3.1, §5.4 | **BUILD** |
| Google Drive doc surface (mocked) | §3.1, §5.3 | **BUILD** |
| Theater UI (Next.js, three-pane + CRM inset) | §5.2, §6.1 | **BUILD** |
| Knowledge graph + container-boot citation-provenance validator | §6.5 | **BUILD** |
| Conformal calibration table (synthetic Phase 1 holdout) | §3.4 step 2.2, §6.6 | **BUILD** |
| **Tightening 1** — Transactional Outbox pattern, same-tx commit, DLQ after 6× retries | §3.6 | **BUILD** |
| **Tightening 2** — Redis distributed lock at Slack ingress, 60s TTL | §6.3 slack_events.py | **BUILD** |
| **Tightening 3** — byte-density `deterministic_section_ratio` validator | §6.2 PreVisitDossier `model_validator` | **BUILD** |
| **Tightening 4** — section-granular DS-CP for partial evidence | §3.6, §6.2 `unverified_sections` | **BUILD** |
| **Tightening 5** — deployment topology Mermaid diagram | §3.1.5 (already in PRD; build maps to it) | **DOCUMENTED** |

### A.2 — Out of Scope for Phase 1 (Reserved Phase 2/3)

- **Continuous-background refresh of dossier sections.** PRD §5.6 verbal Phase 2 tease. Phase 1 dossier is one-shot per (prospect_id, signal_hash, knowledge_graph_version).
- **CMMS work-order routing companion architecture.** PRD §5.6 verbal Phase 3 tease, vestigial from the killed CMMS Bridge architecture. Phase 1 builds **zero** CMMS code paths.
- **Live Slack / Hubspot / Salesforce / Drive credentials.** Phase 1 uses local mock servers (§6.1 `apps/mocks/`). Real OAuth installs are Phase 2.
- **Production-grade conformal calibration.** Phase 1 uses synthetic 30-event holdout (per `scripts/build_calibration_table.py`); daily re-calibration job is Phase 2.
- **DLQ observability dashboard.** Phase 1 surfaces DLQ rows in the Theater pane only. Cloud Monitoring / alerting stack is Phase 2.
- **Multi-tenancy.** Phase 1 is single-tenant. Workspace ID and CRM tenant ID are scoped to the demo tenant.
- **Real PII handling / GDPR DPA artifacts.** Phase 1 mocks are synthetic.

### A.3 — Architectural Invariants (Do Not Walk Back)

1. Deterministic two-route ADC. LLM never routes.
2. N=3 deep ensemble on every categorical Flash stage with `thinking_level="minimal"`, temperatures `(0.1, 0.5, 0.9)`.
3. Pydantic `ConfigDict(extra="forbid")` at every API boundary and every schema.
4. Vertex AI `europe-west4` pin via `google-genai`. Global endpoint forbidden. Model strings: `gemini-3-flash-preview`, `gemini-3.1-pro-preview` (with the dot in `3.1`, not a hyphen).

### A.4 — DMZ Rule (Absolute)

Phase 1 code MUST NOT import from, depend on, or reach into: SENTRY, TALLY, GAUGE, TRACE, Manufacturing Foundation Models, Manufacturing OS UI, edge device firmware, real-time camera streams, customer CMMS/QMS/MES, customer factory PLCs. Verified via §3.1.5 deployment topology — separate GCP project, separate VPC, separate Vertex AI client.

### A.5 — Vestigial Naming Correction

`ULTIMATE_PRD.md §3.6` and `§6.1` reference `cmms_outbox_dlq` as the DLQ table name. This is vestigial from the killed CMMS Bridge architecture (commit `752edae` and prior). **Phase 1 builds the table as `outbox_dlq`** — the `cmms_` prefix is dropped. Same applies to any code identifier (`cmms_outbox_dlq` → `outbox_dlq`). Documented again at §E.13 and §K.

---

## §B. File-by-File Manifest

Every file in `ULTIMATE_PRD.md §6.1` repository tree, with build-ready spec. Entries are ordered top-down through the tree.

### Root files

#### `pyproject.toml`
- **Purpose.** Project metadata, dependency pins (see §K), tool configuration (ruff, mypy, pytest).
- **Build content.** See §K verbatim.
- **PRD anchor.** §6.3 stack pin paragraph.

#### `docker-compose.yml`
- **Purpose.** Local dev compose stack: Postgres, Redis, mock-Slack, mock-CRM, mock-Drive, refinery_api (FastAPI), refinery_worker (Celery), theater_ui (Next.js).
- **Services.** `postgres:16`, `redis:7`, `mock_slack`, `mock_crm`, `mock_drive`, `refinery_api`, `refinery_worker`, `theater_ui`.
- **Networks.** Single network `refinery_dev`; mock services share it. No mapping to Matta-flavored network names.
- **Volumes.** `pg_data:/var/lib/postgresql/data` only; everything else is ephemeral.
- **Env vars (load from `.env`).** `POSTGRES_URL`, `REDIS_URL`, `CELERY_BROKER`, `GCP_PROJECT`, `VERTEX_LOCATION=europe-west4`, `SLACK_SIGNING_SECRET`, `CRM_WEBHOOK_SECRET_HUBSPOT`, `CRM_WEBHOOK_SECRET_SALESFORCE`, `MOCK_SURFACES=true`.
- **PRD anchor.** §6.1 root.

#### `.env.example`
- **Purpose.** Reference for local dev. Real secrets are NEVER committed.
- **Keys to declare** (with placeholder values): all env vars above plus `KAIDE_LABS_PROJECT_ID`, `KAIDE_LABS_REGION=europe-west4`.

#### `README.md`
- **Purpose.** One-page README pointing at `ULTIMATE_PRD.md` and this spec, with `docker compose up` quickstart and `make demo` invocation.
- **Out of scope.** Marketing copy.

### `infra/`

#### `infra/Dockerfile.api`
- **Purpose.** Multi-stage Python 3.12 image for `refinery_api`. Builder installs `pip install --no-cache-dir .` (uses pyproject); runtime layer uses `python:3.12-slim`.
- **Healthcheck.** `HEALTHCHECK CMD curl -f http://localhost:8080/healthz || exit 1`.
- **Entrypoint.** `uvicorn apps.refinery_api.main:app --host 0.0.0.0 --port 8080 --workers 2`.

#### `infra/Dockerfile.worker`
- **Purpose.** Celery worker image. Same base layer as API. Entrypoint runs the worker with concurrency 4 and beat scheduler off (Phase 1 has no scheduled tasks).
- **Entrypoint.** `celery -A apps.refinery_worker.app worker --loglevel=INFO --concurrency=4 --pool=gevent`.

#### `infra/cloudrun.yaml`
- **Purpose.** Cloud Run service descriptor for `refinery_api`. Region `europe-west4`. Min instances 0, max 10. Concurrency 80. Memory 1Gi. CPU 2.
- **Note.** Phase 1 demo runs via docker compose locally; this file exists for Phase 2 deploy.

#### `infra/cloudtasks.yaml`
- **Purpose.** Cloud Tasks queue descriptor for the outbox dispatcher (Tightening 1 message-relay). Location `europe-west4`. Max attempts 6. Min backoff 10s. Max backoff 3600s. Total max retry duration 21600s (6 hours).
- **Queue name.** `outbox-relay-eu`.

### `apps/refinery_api/`

#### `apps/refinery_api/main.py`
- **Purpose.** FastAPI app factory. Lifespan context manager wires Postgres engine, Redis client, Celery client, Vertex AI `genai.Client` into `app.state`.
- **Imports.** `from contextlib import asynccontextmanager`, `from fastapi import FastAPI`, `import redis.asyncio as aioredis`, `from celery import Celery`, `from google import genai`, `from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker`, `from .config import settings`.
- **Lifespan sets.** `app.state.redis`, `app.state.celery`, `app.state.engine`, `app.state.session_maker`, `app.state.vertex_client`.
- **Lifespan teardown.** `await app.state.redis.aclose()`, `await app.state.engine.dispose()`.
- **Includes routers.** `ingest`, `slack_events`, `slack_interactions`, `crm_webhooks`, `crm_actions`, `dossier`, `health`.
- **Startup KG check.** Calls `packages.knowledge_graph.verify.validate_graph_or_die()` inside the lifespan — failure aborts boot (per §6.5 contract).
- **PRD anchor.** §6.3 lifespan code block.

#### `apps/refinery_api/config.py`
- **Purpose.** Pydantic Settings (`pydantic-settings`) class.
- **Fields.** `postgres_url`, `redis_url`, `celery_broker`, `gcp_project`, `vertex_location: Literal["europe-west4"] = "europe-west4"`, `slack_signing_secret`, `crm_webhook_secret_hubspot`, `crm_webhook_secret_salesforce`, `mock_surfaces: bool = True`, `kaide_labs_project_id`.
- **Behavior.** Loaded from env at import time; raises on missing required fields.

#### `apps/refinery_api/deps.py`
- **Purpose.** FastAPI dependency-injection types.
- **Exports.**
  ```
  async def get_redis(request: Request) -> Redis: return request.app.state.redis
  async def get_celery(request: Request) -> Celery: return request.app.state.celery
  async def get_session(request: Request) -> AsyncSession: ...
  async def get_vertex(request: Request) -> genai.Client: return request.app.state.vertex_client
  async def get_current_user(...) -> User: stub for Phase 1; returns demo user
  RedisDep = Annotated[Redis, Depends(get_redis)]
  CeleryDep = Annotated[Celery, Depends(get_celery)]
  SessionDep = Annotated[AsyncSession, Depends(get_session)]
  VertexDep = Annotated[genai.Client, Depends(get_vertex)]
  UserDep = Annotated[User, Depends(get_current_user)]
  ```

#### `apps/refinery_api/routers/ingest.py`
- **Purpose.** `POST /ingest/batch` — Theater CSV upload entrypoint.
- **Idempotency.** `f"batch:{file_sha256}:{user.id}:{date.today().isoformat()}"` in Redis, 24h TTL.
- **Logic flow.** See §D.1.
- **Side effects.** Postgres `ingest_batches` row + `lead_prospects` upserts; Celery enqueues `refinery.score_batch`.
- **PRD anchor.** §6.3 ingest.py code block.

#### `apps/refinery_api/routers/slack_events.py`
- **Purpose.** `POST /slack/events` — Slack file_share + slash command + URL verification challenge.
- **Tightening 2 lock.** `SET NX EX` on `slack:lock:{event_id}` with `SLACK_LOCK_TTL_SECONDS=60`. Lock contention returns HTTP 202 `duplicate_in_flight`. Post-completion dedup at `slack:event:{event_id}` 24h TTL retained (set by Celery `on_success`).
- **Signature verify.** HMAC-SHA256 over `v0:{ts}:{raw_body}` with 5-min window before parsing body.
- **Logic flow.** See §D.2.
- **PRD anchor.** §6.3 slack_events.py code block; Tightening 2 spec.

#### `apps/refinery_api/routers/slack_interactions.py`
- **Purpose.** `POST /slack/interactions` — Slack button click (`Generate Full Dossier`).
- **Signature verify.** Same HMAC pattern as slack_events.
- **Idempotency.** Dossier-level key `f"dossier:{prospect_id}:{signal_hash}:{kg_version}"`.
- **Side effects.** Celery enqueues `refinery.generate_dossier`.

#### `apps/refinery_api/routers/crm_webhooks.py`
- **Purpose.** `POST /crm/webhook/{provider}` — Hubspot/Salesforce webhook ingest.
- **Path param.** `provider: Literal["hubspot", "salesforce"]`.
- **Signature verify.** Provider-specific HMAC (Hubspot v3 signature header; Salesforce JWT or named signature header).
- **Idempotency.** `f"crm:{provider}:{object_id}:{updated_at.isoformat()}:{changed_fields_hash}"`.
- **PRD anchor.** §6.3 crm_webhooks.py code block.

#### `apps/refinery_api/routers/crm_actions.py`
- **Purpose.** `POST /crm/actions/generate-dossier` — CRM UI button.
- **Body.** `CRMDossierActionRequest` with `provider`, `crm_object_id`.
- **Resolves to.** `prospect_id` via Postgres lookup, then enqueues `refinery.generate_dossier`.

#### `apps/refinery_api/routers/dossier.py`
- **Purpose.** `POST /dossier/generate` (Theater button) and `GET /dossier/{dossier_id}` (poll).
- **PRD anchor.** §6.3 dossier.py code block.

#### `apps/refinery_api/routers/health.py`
- **Purpose.** `GET /healthz` (liveness, 200 if process alive) and `GET /readyz` (readiness: KG validation passed at startup; Vertex client warm-pinged; Postgres ping; Redis ping).
- **Readyz behavior.** Returns 503 with `{"status": "unhealthy", "checks": {...}}` on any failed sub-check.

#### `apps/refinery_api/routers/websocket.py`
- **Purpose.** `WS /ws/theater/{batch_id}` for Theater pane real-time updates.
- **Message types broadcast.** `ingest.ack`, `adc.routed`, `stage1.enriched`, `stage1.vertical_voted`, `stage1.scored`, `stage1.complete`, `stage2.section_started`, `stage2.section_complete`, `stage2.complete`, `outbox.dispatched`, `outbox.dlq`, `cost.ticker`.

### `apps/refinery_worker/`

#### `apps/refinery_worker/app.py`
- **Purpose.** Celery app factory.
- **Config.** `task_acks_late=True`, `task_reject_on_worker_lost=True`, `worker_prefetch_multiplier=1`, `broker_transport_options={"visibility_timeout": 3600}`, `task_serializer="json"`, `result_backend=settings.redis_url`.
- **Task discovery.** `app.autodiscover_tasks(["apps.refinery_worker.tasks"])`.

#### `apps/refinery_worker/tasks/__init__.py`
- Imports all task modules so Celery autodiscovery sees them.

#### `apps/refinery_worker/tasks/classify_action_domain.py`
- **Task name.** `refinery.classify_action_domain`.
- **Purpose.** Stage 0 ADC entry. Receives request envelope; dispatches to PRIORITIZATION, DOSSIER_STUB, DOSSIER_FULL, or HUMAN_REVIEW.
- **No LLM. Hardcoded Python.**
- **Output.** Enqueues downstream task by name.

#### `apps/refinery_worker/tasks/score_batch.py`
- **Task name.** `refinery.score_batch`.
- **Purpose.** Stage 1 orchestration. Fans out per-prospect tasks.
- **Input.** `batch_id: str`.
- **Subtasks enqueued per prospect.** `refinery.enrich_prospect`, then `refinery.classify_vertical`, then `refinery.score_fitness`. Chained via Celery `chain()` or signature.
- **On batch completion.** Enqueues `refinery.generate_dossier_stub` for top-12 prospects by fitness score.
- **Idempotency.** `batch_id` key in `score_runs` table; replay returns existing run.

#### `apps/refinery_worker/tasks/enrich_prospect.py`
- **Task name.** `refinery.enrich_prospect`.
- **Stage 1.1.** Deterministic only. No LLM.
- **Sub-adapters called.** `enrichment.companies_house`, `enrichment.web_scraper`, `enrichment.linkedin_signal` (mocked).
- **Circuit breaker.** Each adapter wrapped; failures logged + `enrichment_status: partial`. Does not block.
- **Output.** Writes enrichment fields to `lead_prospects`; sets `enrichment_status` enum.

#### `apps/refinery_worker/tasks/classify_vertical.py`
- **Task name.** `refinery.classify_vertical`.
- **Stage 1.2.** N=3 Flash ensemble.
- **Model.** `gemini-3-flash-preview`, `thinking_level="minimal"`, temperatures `(0.1, 0.5, 0.9)`.
- **Response schema.** `VerticalClassification` (Pydantic, `Literal["polymer_extrusion", "metal_casting", "additive_manufacturing", "fnb_bottling", "electronics_assembly", "aerospace", "out_of_vertical"]`).
- **Voting.** `Counter([s.vertical for s in samples]).most_common(1)`; on 3-way split, set `vertical = "vertical_uncertain"` and `requires_human_review = True`.
- **Concurrency.** Three `client.aio.models.generate_content` calls via `asyncio.gather` inside the Celery task body (use `gevent` pool so async works).
- **Idempotency.** Key `f"vertical:{prospect_id}:{signal_hash}"`, 7d TTL.
- **Cost cap.** Per-call `max_output_tokens=64` (vertical enum + short rationale fit easily).

#### `apps/refinery_worker/tasks/score_fitness.py`
- **Task name.** `refinery.score_fitness`.
- **Stage 1.3.** Deterministic. No LLM.
- **Inputs.** Vertical, factory_size_band, trade_show_provenance flag, capacity_decay (slot-fill ratio from `prioritized_queues` table for current quarter).
- **Output.** `fitness_score: float ∈ [0.0, 1.0]` written to `lead_prospects.fitness_score`.
- **Scoring weights (Phase 1 demo).** `0.40 * vertical_match + 0.25 * size_band_match + 0.20 * trade_show_provenance + 0.15 * (1 - capacity_decay)`. All weights live in `packages/scoring/weights.py` as module constants for auditability.

#### `apps/refinery_worker/tasks/generate_dossier_stub.py`
- **Task name.** `refinery.generate_dossier_stub`.
- **Stage 1.5.** Deterministic only. **ZERO LLM calls.**
- **Enqueue trigger.** Auto for top-12 prospects on `score_batch` completion (Conflict D resolution per PRD §1.3).
- **Output.** Writes `DossierStub` rows: company facts (from enrichment), verified vertical, headline KG anchor lookup, `slot_readiness` ∈ {`ready_for_dossier`, `requires_human_review`, `low_signal`}.
- **Side effects.** Posts stub to Slack canvas, writes CRM stub fields, creates Drive priority-index entry.

#### `apps/refinery_worker/tasks/generate_dossier.py`
- **Task name.** `refinery.generate_dossier`.
- **Stage 2 orchestration.**
- **Subtasks enqueued in this order** (some parallelizable):
  1. `dossier_section_taxonomy` (Pro N=1, blocking — taxonomy informs downstream stages)
  2. `dossier_section_defect` (Flash N=3 + conformal, can run in parallel with comparable selection)
  3. `dossier_section_comparable` (deterministic select + Pro N=1 prose)
  4. `dossier_section_risk` (Pro N=1, depends on taxonomy)
  5. `dossier_section_approach` (Pro N=1, depends on taxonomy + defect + risk)
- **Compose.** Aggregates section outputs into `PreVisitDossier`, runs Pydantic validation (triggers Tightening 3 byte-density validator + Tightening 4 section-strip), writes to `dossier_artifacts` table + outbox (Tightening 1 same-tx).
- **Idempotency.** `f"dossier:{prospect_id}:{signal_hash}:{kg_version}"` Redis 7d TTL; Postgres unique constraint on `(prospect_id, signal_hash, knowledge_graph_version)`.

#### `apps/refinery_worker/tasks/dossier_section_taxonomy.py`
- **Task name.** `refinery.dossier_section_taxonomy`.
- **Stage 2.1.** `gemini-3.1-pro-preview`, `thinking_level="medium"`, N=1.
- **Response schema.** `ProcessTaxonomy`.
- **Cost cap.** `max_output_tokens=1024`.
- **Idempotency.** `f"section:taxonomy:{prospect_id}:{signal_hash}:{kg_version}"`.

#### `apps/refinery_worker/tasks/dossier_section_defect.py`
- **Task name.** `refinery.dossier_section_defect`.
- **Stage 2.2.** Flash N=3, `thinking_level="minimal"`, temps `(0.1, 0.5, 0.9)`. Apply conformal calibration table.
- **Response schema.** `LikelyDefectClassHypothesis`.
- **DS-CP check (Tightening 4).** Compute semantic distance between prospect's signal vector and calibration distribution centroid for the prospect's vertical sub-path; if distance > threshold OR `allowed_evidence[]` is empty, mark section `UNVERIFIED_INSUFFICIENT_DATA` and append `"defect_hypothesis"` to `unverified_sections`.
- **Conformal set computation.** Per §H.
- **Cost cap.** Per-call `max_output_tokens=512`.

#### `apps/refinery_worker/tasks/dossier_section_comparable.py`
- **Task name.** `refinery.dossier_section_comparable`.
- **Stage 2.3a (deterministic select).** `packages.knowledge_graph.select.select_comparable(vertical, process_taxonomy) -> matta_customer_anchor: str`. LLM never picks. Returns `"no_comparable_available"` if no KG match.
- **Stage 2.3b (Pro prose).** `gemini-3.1-pro-preview`, `thinking_level="low"`, N=1. Receives the pre-selected anchor + `permitted_dimensions_of_comparability` list from the KG. Writes 1–2 sentence `dimension_of_comparability` ≤250 chars. Cap enforced at Pydantic boundary (§C).
- **Response schema.** `ComparableDeployment`.

#### `apps/refinery_worker/tasks/dossier_section_risk.py`
- **Task name.** `refinery.dossier_section_risk`.
- **Stage 2.4.** `gemini-3.1-pro-preview`, `thinking_level="low"`, N=1.
- **Response schema.** `RiskRegister`. Fixed risk-taxonomy enum (see §C).

#### `apps/refinery_worker/tasks/dossier_section_approach.py`
- **Task name.** `refinery.dossier_section_approach`.
- **Stage 2.5.** `gemini-3.1-pro-preview`, `thinking_level="low"`, N=1.
- **Response schema.** `SuggestedApproach`. Fixed approach-template-library enum.

#### `apps/refinery_worker/tasks/outbox_dispatcher.py`
- **Task name.** `refinery.outbox_dispatcher`.
- **Tightening 1 message-relay.** Invoked by Cloud Tasks per outbox row.
- **Logic.** See §L.3.
- **DLQ.** After 6 failed attempts (delivery_attempts column), row is moved to `outbox_dlq` table (NOT `cmms_outbox_dlq` per §A.5).
- **Idempotency.** Outbox row `id` is the natural key; relay is idempotent on the external API (Slack canvas update, CRM note upsert, Drive doc create/update are all conditional on existence).

#### `apps/refinery_worker/tasks/release_slack_lock.py`
- **Task name.** `refinery.release_slack_lock` (also wired as `on_success`/`on_failure` callback on `refinery.parse_slack_ingress`).
- **Tightening 2 lock-release.**
- **Logic.** On task completion (success or failure), `redis.delete(f"slack:lock:{slack_event_id}")` and on success additionally `redis.set(f"slack:event:{slack_event_id}", "1", ex=86400)`.

### `apps/theater_ui/` (Next.js 14 + Tailwind)

#### `apps/theater_ui/pages/index.tsx`
- **Purpose.** Three-pane layout + CRM inset.
- **State.** Pulls `batch_id` from query string; opens WebSocket to `/ws/theater/{batch_id}`.
- **Tailwind grid.** `grid-cols-3` for main panes; CRM inset is `fixed bottom-4 right-4 w-80 h-48`.
- **Components.** `<SlackLeftPane />`, `<TheaterCenterPane />`, `<DriveDossierRightPane />`, `<CRMRecordInset />`.

#### `apps/theater_ui/components/SlackLeftPane.tsx` (§J.2)

#### `apps/theater_ui/components/TheaterCenterPane.tsx` (§J.3)

#### `apps/theater_ui/components/DriveDossierRightPane.tsx` (§J.4)

#### `apps/theater_ui/components/CRMRecordInset.tsx` (§J.5)

#### `apps/theater_ui/hooks/useWebSocket.ts` (§J.6)

### `apps/mocks/`

See §I for content specifications.

- `apps/mocks/lead_csv_generator.py`
- `apps/mocks/mock_slack/server.py`
- `apps/mocks/mock_crm/server.py`
- `apps/mocks/mock_drive/server.py`
- `apps/mocks/mock_matta_dashboard/` (Theater pane's CRM-style record inset — repurposed per §I)

### `packages/schemas/`

Each module declares one or more Pydantic models per §C.

- `packages/schemas/lead_intake.py` — `LeadIntakeRow`, `LeadIntakeBatch`, `IngestAck`
- `packages/schemas/lead_prospect.py` — `LeadProspect`, `PrioritizedQueue`
- `packages/schemas/dossier.py` — `ProcessTaxonomy`, `ComparableDeployment`, `RiskRegister`, `SuggestedApproach`, `PreVisitDossier`, `DossierAck`, `DossierRequest`, `DossierStub`
- `packages/schemas/defect_hypothesis.py` — `LikelyDefectClassHypothesis`, `VerticalClassification`
- `packages/schemas/slack_ingress.py` — `SlackEventPayload`, `SlackLeadBatchIngress`, `SlackDossierAction`, `SlackEventAck`
- `packages/schemas/crm.py` — `CRMLeadSignal`, `CRMWritebackEnvelope`, `CRMWebhookAck`, `CRMDossierActionRequest`
- `packages/schemas/drive.py` — `DossierDocManifest`
- `packages/schemas/outbox.py` — `OutboxEnvelope`, `OutboxDLQEntry` (Tightening 1)

### `packages/adc/`

- `packages/adc/rules.py` — `route_request(envelope) -> Route`. Pure function. No I/O. Returns `Literal["PRIORITIZATION", "DOSSIER_STUB", "DOSSIER_FULL", "HUMAN_REVIEW"]`.

### `packages/scoring/`

- `packages/scoring/weights.py` — module-level constants (vertical-match weight 0.40, size-band weight 0.25, trade-show 0.20, capacity-decay 0.15).
- `packages/scoring/fitness.py` — `compute_fitness(prospect: LeadProspect, queue_state: QueueState) -> float`. Pure function.

### `packages/enrichment/`

- `packages/enrichment/base.py` — `EnrichmentAdapter` ABC with circuit breaker. `async def fetch(prospect: LeadProspect) -> EnrichmentResult`.
- `packages/enrichment/companies_house.py` — UK Companies House adapter (mocked).
- `packages/enrichment/web_scraper.py` — Bounded, allowlist-only scraper.
- `packages/enrichment/linkedin_signal.py` — Mocked.

### `packages/knowledge_graph/`

- `packages/knowledge_graph/graph.json` — KG data per §G.
- `packages/knowledge_graph/loader.py` — `load_graph() -> KnowledgeGraph` Pydantic-validated.
- `packages/knowledge_graph/verify.py` — `validate_graph_or_die() -> None` startup validator; CLI mode for CI.
- `packages/knowledge_graph/select.py` — `select_comparable(vertical, taxonomy) -> matta_customer_anchor` deterministic rules (Stage 2.3a).
- `packages/knowledge_graph/evidence.py` — `compute_allowed_evidence(vertical, section_type, prospect_signals) -> list[int]` (citation lines whitelist).

### `packages/uncertainty/`

- `packages/uncertainty/conformal.py` — Split-conformal computation per §H.
- `packages/uncertainty/dscp.py` — Section-granular DS-CP semantic-distance computation (Tightening 4).
- `packages/uncertainty/calibration_table.json` — Built by `scripts/build_calibration_table.py`.

### `packages/outbox/`

- `packages/outbox/models.py` — SQLAlchemy ORM for `outbox`, `outbox_dlq`. Note: **`outbox_dlq` not `cmms_outbox_dlq`** (§A.5).
- `packages/outbox/dispatcher.py` — Reads outbox rows, dispatches to surface adapters, retries on failure, moves to DLQ after 6 attempts.
- `packages/outbox/enqueue.py` — `async def enqueue_in_tx(session: AsyncSession, envelope: OutboxEnvelope) -> None`. Tightening 1 same-tx commit helper.

### `packages/adapters/`

#### `packages/adapters/slack/`
- `client.py` — Slack Web API client (calls mock server in Phase 1).
- `signature.py` — HMAC-SHA256 `v0:{ts}:{raw_body}` verification, 5-min window.
- `renderer.py` — Pydantic schema → Slack blocks/canvas blocks.

#### `packages/adapters/crm/`
- `base.py` — `CRMAdapter` Protocol; `provider: Literal["hubspot", "salesforce"]`; `create_or_update_record_fields()`, `append_record_note()`.
- `hubspot.py` — Implements protocol against mock server.
- `salesforce.py` — Implements protocol against mock server.

#### `packages/adapters/drive/`
- `client.py` — Google Drive API v3 client (mock).
- `renderer.py` — Schema → Google Doc structured paragraphs + tables.

### `packages/prompts/` (per §F)

- `packages/prompts/vertical_flash.py`
- `packages/prompts/taxonomy_pro.py`
- `packages/prompts/defect_flash.py`
- `packages/prompts/comparable_pro.py`
- `packages/prompts/risk_pro.py`
- `packages/prompts/approach_pro.py`

### `scripts/`

- `scripts/seed_mock_data.py` — Per §I.
- `scripts/build_calibration_table.py` — Per §H.
- `scripts/verify_knowledge_graph.py` — CLI wrapper around `packages.knowledge_graph.verify.validate_graph_or_die`.
- `scripts/run_demo.sh` — Orchestrates the demo (compose up, seeds data, opens browser tabs).

### `migrations/` (Alembic)

- `migrations/versions/0001_initial.py` — All tables:
  - `ingest_batches` (idempotency on `(file_sha256, user_id, day)`)
  - `lead_prospects` (upsert on `(source_system, external_lead_id)`; columns include `signal_hash`, `enrichment_status`, `fitness_score`, `vertical`, `vertical_uncertain`, etc.)
  - `prioritized_queues` (per-batch ranked list)
  - `dossier_artifacts` (unique on `(prospect_id, signal_hash, knowledge_graph_version)`)
  - `dossier_stubs` (top-12 stubs from Stage 1.5)
  - `outbox` (Tightening 1 — columns: `id`, `surface` enum, `payload_jsonb`, `delivery_attempts`, `last_attempt_at`, `next_attempt_at`, `state` enum)
  - `outbox_dlq` (Tightening 1 DLQ — same shape plus `failed_at`, `final_error`)
  - `event_idempotency` (Redis-overflow audit; not strictly required but useful for forensics)
- **Indexes.** All idempotency lookup columns indexed; outbox `state` partial index for active rows.

### `tests/`

- `tests/unit/test_schemas_pydantic.py`
- `tests/unit/test_byte_density_validator.py` (success criterion #12)
- `tests/unit/test_slack_distributed_lock.py` (success criterion #13)
- `tests/unit/test_knowledge_graph_validator.py` (success criterion #14)
- `tests/unit/test_dscp_section_strip.py` (success criterion #15)
- `tests/unit/test_adc_routing.py`
- `tests/unit/test_conformal_calibration.py`
- `tests/integration/test_csv_to_stub_pipeline.py` (Magic Moment 1 path)
- `tests/integration/test_slack_click_to_dossier_pipeline.py` (Magic Moment 2 path)
- `tests/integration/test_outbox_relay_and_dlq.py` (Tightening 1)
- `conftest.py` (Postgres fixture, Redis fixture, mock surface fixtures, deterministic seed)

---

## §C. Pydantic Schema Definitions (Exact)

Common imports for every schema module:

```python
from datetime import datetime
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
```

### C.1 — `packages/schemas/lead_intake.py`

```python
class LeadIntakeRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    external_lead_id: Annotated[str, Field(min_length=1, max_length=128)]
    company_name: Annotated[str, Field(min_length=1, max_length=256)]
    contact_name: Annotated[str | None, Field(max_length=128)] = None
    contact_email: Annotated[str | None, Field(max_length=256)] = None
    sector_hint: Annotated[str | None, Field(max_length=128)] = None
    factory_size_band: Literal["small", "medium", "large", "unknown"] | None = None
    raw_notes: Annotated[str | None, Field(max_length=2048)] = None


class LeadIntakeBatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    batch_id: str
    source_label: Annotated[str, Field(max_length=128)]
    source_surface: Literal["theater_csv", "slack_upload", "crm_webhook", "email_forward"]
    ingest_user: str
    ingest_timestamp: datetime
    rows: Annotated[list[LeadIntakeRow], Field(min_length=1, max_length=2000)]


class IngestAck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    batch_id: str
    status: Literal["scoring", "duplicate", "rejected"]
    row_count: Annotated[int, Field(ge=0)]
    rejection_reason: str | None = None
```

### C.2 — `packages/schemas/lead_prospect.py`

```python
VERTICAL_ENUM = Literal[
    "polymer_extrusion", "metal_casting", "additive_manufacturing",
    "fnb_bottling", "electronics_assembly", "aerospace",
    "out_of_vertical", "vertical_uncertain",
]

class LeadProspect(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    external_lead_id: str
    source_system: Literal["hubspot", "salesforce", "csv_upload", "slack_upload"]
    company_name: Annotated[str, Field(max_length=256)]
    vertical: VERTICAL_ENUM
    factory_size_band: Literal["small", "medium", "large", "unknown"]
    trade_show_provenance: bool
    fitness_score: Annotated[float, Field(ge=0.0, le=1.0)]
    enrichment_status: Literal["complete", "partial", "failed"]
    signal_hash: str
    last_scored_at: datetime
    requires_human_review: bool = False


class PrioritizedQueueEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prospect_id: str
    rank: Annotated[int, Field(ge=1)]
    fitness_score: Annotated[float, Field(ge=0.0, le=1.0)]
    vertical: VERTICAL_ENUM
    slot_readiness: Literal["ready_for_dossier", "requires_human_review", "low_signal"]


class PrioritizedQueue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    batch_id: str
    generated_at: datetime
    entries: Annotated[list[PrioritizedQueueEntry], Field(min_length=0, max_length=2000)]
```

### C.3 — `packages/schemas/defect_hypothesis.py`

```python
DEFECT_CLASS_ENUM = Literal[
    "porosity", "dimensional_drift", "surface_inclusions", "tool_wear",
    "calibration_drift", "material_defect", "process_drift", "unknown",
]

class VerticalClassification(BaseModel):
    """Per-sample output for the N=3 Stage 1.2 ensemble."""
    model_config = ConfigDict(extra="forbid")

    vertical: VERTICAL_ENUM
    rationale: Annotated[str, Field(max_length=200)]


class LikelyDefectClassHypothesis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    conformal_set: Annotated[list[DEFECT_CLASS_ENUM], Field(min_length=0, max_length=8)]
    coverage: Annotated[float, Field(ge=0.0, le=1.0)]
    calibration_version: str
    requires_human_review: bool = False
    rationale: Annotated[str, Field(max_length=400)]

    @model_validator(mode="after")
    def _flag_review_on_degenerate_set(self) -> "LikelyDefectClassHypothesis":
        # Empty set or all-class set → uncertainty is total → flag review.
        if len(self.conformal_set) == 0 or len(self.conformal_set) == 8:
            object.__setattr__(self, "requires_human_review", True)
        return self
```

### C.4 — `packages/schemas/dossier.py`

```python
MATTA_CUSTOMER_ANCHOR_ENUM = Literal[
    "bowers_and_wilkins", "caracol_am", "polymer_unnamed",
    "metal_casting_unnamed", "global_drinks_brand",
    "no_comparable_available",
]

RISK_CATEGORY_ENUM = Literal[
    "legacy_cmm_infrastructure", "lighting_variance",
    "emf_environment", "network_topology",
    "ot_it_segmentation", "regulatory_audit_burden",
    "operator_training_overhead", "calibration_baseline_unknown",
]

APPROACH_TEMPLATE_ENUM = Literal[
    "two_camera_pilot", "four_camera_pilot",
    "full_line_deployment", "caracol_am_oem_partnership",
]


class ProcessTaxonomy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    primary_process: Annotated[str, Field(max_length=200)]
    sub_processes: Annotated[list[str], Field(max_length=10)]
    line_level_steps: Annotated[list[str], Field(max_length=20)]
    rationale: Annotated[str, Field(max_length=600)]


class ComparableDeployment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    matta_customer_anchor: MATTA_CUSTOMER_ANCHOR_ENUM
    citation_substrate_line: Annotated[int, Field(ge=1, le=100000)]
    dimension_of_comparability: Annotated[str, Field(max_length=250)]  # Pro prose, ≤250 chars (v4 hardening)
    selection_method: Literal["deterministic_rules", "no_comparable_available"]


class RiskFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: RISK_CATEGORY_ENUM
    severity: Literal["identified", "unknown", "not_applicable"]
    note: Annotated[str, Field(max_length=300)]


class RiskRegister(BaseModel):
    model_config = ConfigDict(extra="forbid")

    findings: Annotated[list[RiskFinding], Field(min_length=1, max_length=10)]


class SuggestedApproach(BaseModel):
    model_config = ConfigDict(extra="forbid")

    template: APPROACH_TEMPLATE_ENUM
    rationale: Annotated[str, Field(max_length=600)]
    day_one_risks: Annotated[list[str], Field(max_length=8)]


DETERMINISTIC_BYTE_THRESHOLD = 0.60

DETERMINISTIC_SECTION_KEYS = frozenset({
    "company_facts",
    "verified_kg_anchors",
    "fitness_score_rationale",
    "risk_checklist_baseline",
    "approach_template_baseline",
})

LLM_SECTION_KEYS = frozenset({
    "process_taxonomy",
    "defect_hypothesis",
    "comparable_dimension_of_comparability_prose",
    "risk_register_narrative",
    "suggested_approach_narrative",
})


class PreVisitDossier(BaseModel):
    """The full Stage 2 artifact. Tightening 3 byte-density validator and Tightening 4 unverified_sections live here."""
    model_config = ConfigDict(extra="forbid")

    dossier_id: str
    prospect_id: str
    signal_hash: str
    knowledge_graph_version: str
    calibration_version: str

    process_taxonomy: ProcessTaxonomy
    defect_hypothesis: LikelyDefectClassHypothesis
    comparable_deployment: ComparableDeployment
    risk_register: RiskRegister
    suggested_approach: SuggestedApproach

    rendered_sections: dict[str, str]  # section_key -> rendered utf-8 bytes; source of truth for the recomputation

    deterministic_section_ratio: Annotated[
        float,
        Field(
            ge=0.0, le=1.0,
            description=(
                "Byte-density ratio: bytes(deterministic_content) / bytes(total_content). "
                "Recomputed inside _recompute_and_enforce_deterministic_byte_ratio model_validator "
                "from rendered_sections at validation time; caller-provided values are overwritten. "
                "Rejects payloads below DETERMINISTIC_BYTE_THRESHOLD."
            ),
        ),
    ]

    unverified_sections: Annotated[
        list[str],
        Field(
            default_factory=list,
            description=(
                "Section keys stripped from the dossier under section-granular DS-CP "
                "(Tightening 4; arXiv 2510.05566 per ULTIMATE_PRD.md §4.2). "
                "Renderers show explicit 'N sections marked unverified' note rather than silent omission."
            ),
        ),
    ]

    requires_human_review_sections: Annotated[list[str], Field(default_factory=list)]
    generated_at: datetime

    @model_validator(mode="after")
    def _recompute_and_enforce_deterministic_byte_ratio(self) -> "PreVisitDossier":
        det_bytes = sum(
            len(self.rendered_sections[k].encode("utf-8"))
            for k in DETERMINISTIC_SECTION_KEYS
            if k in self.rendered_sections
        )
        llm_bytes = sum(
            len(self.rendered_sections[k].encode("utf-8"))
            for k in LLM_SECTION_KEYS
            if k in self.rendered_sections
        )
        total = det_bytes + llm_bytes
        if total == 0:
            raise ValueError("PreVisitDossier.rendered_sections is empty")
        recomputed = det_bytes / total
        # NEVER trust the caller-provided value. Overwrite it.
        object.__setattr__(self, "deterministic_section_ratio", recomputed)
        if recomputed < DETERMINISTIC_BYTE_THRESHOLD:
            raise ValueError(
                f"deterministic_section_ratio={recomputed:.3f} is below threshold "
                f"{DETERMINISTIC_BYTE_THRESHOLD}; LLM byte volume exceeded the audit budget. "
                f"Payload rejected (Tightening 3 byte-density gate)."
            )
        return self


class DossierStub(BaseModel):
    """Stage 1.5 deterministic-only top-12 stub. Zero LLM calls in producing this."""
    model_config = ConfigDict(extra="forbid")

    stub_id: str
    prospect_id: str
    company_facts: dict[str, str]
    verified_vertical: VERTICAL_ENUM
    headline_kg_anchor: MATTA_CUSTOMER_ANCHOR_ENUM
    slot_readiness: Literal["ready_for_dossier", "requires_human_review", "low_signal"]
    generated_at: datetime


class DossierRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prospect_id: str
    force_regenerate: bool = False
    requested_surface: Literal["slack", "crm", "drive", "all"] = "all"


class DossierAck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dossier_id: str
    status: Literal["generating", "cached", "queued", "rejected"]
```

### C.5 — `packages/schemas/slack_ingress.py`

```python
class SlackEventPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str
    team_id: str
    api_app_id: str
    event: dict  # untyped passthrough; the handler narrows on event.type
    type: Literal["event_callback", "url_verification"]
    challenge: str | None = None  # for url_verification handshake


class SlackLeadBatchIngress(BaseModel):
    model_config = ConfigDict(extra="forbid")

    slack_event_id: str
    workspace_id: str
    channel_id: str
    user_id: str
    source_label: Annotated[str, Field(max_length=128)]
    file_sha256: str | None = None
    raw_text: Annotated[str | None, Field(max_length=4000)] = None


class SlackDossierAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action_id: Literal["generate_full_dossier"]
    prospect_id: str
    signal_hash: str
    slack_response_url: str  # ephemeral response URL Slack provides


class SlackEventAck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["accepted", "duplicate", "duplicate_in_flight"]
    event_id: str
```

### C.6 — `packages/schemas/crm.py`

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
    fit_score: Annotated[float, Field(ge=0.0, le=1.0)]
    vertical: VERTICAL_ENUM
    slot_readiness: Literal["ready_for_dossier", "requires_human_review", "low_signal"]
    dossier_url: str | None = None
    requires_human_review: bool


class CRMWebhookAck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["accepted", "duplicate"]


class CRMDossierActionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: Literal["hubspot", "salesforce"]
    crm_object_id: str
```

### C.7 — `packages/schemas/drive.py`

```python
class DossierDocManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    drive_folder_id: str
    drive_doc_id: str
    share_link: str
    last_verified_at: datetime
    knowledge_graph_version: str
```

### C.8 — `packages/schemas/outbox.py`

```python
SurfaceEnum = Literal["slack_canvas", "crm_note", "crm_field", "drive_doc"]

class OutboxEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    surface: SurfaceEnum
    payload: dict
    delivery_attempts: Annotated[int, Field(ge=0, le=6)]
    state: Literal["pending", "in_flight", "delivered", "dlq"]
    next_attempt_at: datetime
    last_error: str | None = None


class OutboxDLQEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    original_outbox_id: str
    surface: SurfaceEnum
    payload: dict
    delivery_attempts: int
    final_error: str
    failed_at: datetime
```

---

## §D. API Route Signatures (FastAPI)

### D.1 — `POST /ingest/batch`

```python
@router.post("/ingest/batch", response_model=IngestAck, status_code=200)
async def receive_batch(
    file: Annotated[UploadFile, File(...)],
    source_label: Annotated[str, Form(...)],
    redis: RedisDep,
    celery: CeleryDep,
    session: SessionDep,
    user: UserDep,
) -> IngestAck:
```

**Logic flow.**
1. Read raw bytes: `file_bytes = await file.read()`. Reject if `len(file_bytes) > 10 * 1024 * 1024` (10MB) with HTTP 413.
2. Compute `file_sha256 = hashlib.sha256(file_bytes).hexdigest()`.
3. `idempotency_key = f"batch:{file_sha256}:{user.id}:{date.today().isoformat()}"`.
4. `cached = await redis.get(idempotency_key)` — if present, return `IngestAck.model_validate_json(cached)` with status `"duplicate"`.
5. Parse CSV to `LeadIntakeBatch` via `packages.ingest.csv_parser.parse_csv_to_batch(file_bytes, source_label, user)`. Reject on Pydantic validation failure with HTTP 422 + error detail.
6. Inside a single Postgres transaction (Tightening 1 transactional posture): insert `ingest_batches` row, upsert per-row `lead_prospects` rows.
7. Build `IngestAck(batch_id=..., status="scoring", row_count=len(batch.rows))`.
8. `await redis.set(idempotency_key, ack.model_dump_json(), ex=86400)`.
9. `celery.send_task("refinery.score_batch", args=[batch.batch_id])`.
10. Return ack with HTTP 200.

**Failure modes.**
- 413 if file too large.
- 422 if CSV doesn't validate against `LeadIntakeRow` (e.g., missing `external_lead_id`, unknown columns triggering `extra="forbid"`).
- 500 if Postgres transaction fails.

### D.2 — `POST /slack/events` (Tightening 2)

```python
SLACK_LOCK_TTL_SECONDS = 60

@router.post("/slack/events", response_model=SlackEventAck)
async def receive_slack_event(
    request: Request,
    redis: RedisDep,
    celery: CeleryDep,
) -> SlackEventAck | JSONResponse:
```

**Logic flow.**
1. `raw_body = await request.body()`.
2. `slack_adapter.signature.verify(headers=request.headers, body=raw_body, signing_secret=settings.slack_signing_secret, window_seconds=300)` — raises HTTP 401 on mismatch or stale timestamp.
3. Parse to `SlackEventPayload`. Reject on validation failure with HTTP 422.
4. **URL verification handshake.** If `payload.type == "url_verification"`, return `{"challenge": payload.challenge}` with HTTP 200 (special path; no idempotency).
5. **Tightening 2 lock acquire.**
   ```
   lock_acquired = await redis.set(
       f"slack:lock:{payload.event_id}", "1",
       ex=SLACK_LOCK_TTL_SECONDS, nx=True,
   )
   ```
6. If not `lock_acquired`: return `JSONResponse(status_code=202, content={"status": "duplicate_in_flight", "event_id": payload.event_id})`. Slack does not retry on 202.
7. **Post-completion dedup check.** If `await redis.get(f"slack:event:{payload.event_id}")`: release lock (`await redis.delete(f"slack:lock:{payload.event_id}")`) and return `SlackEventAck(status="duplicate", event_id=...)`.
8. Branch on `payload.event["type"]`:
   - `"file_shared"`: enqueue `refinery.parse_slack_ingress` with kwargs `{"slack_event_id": payload.event_id}` (kwargs needed for lock-release callback to find the key).
   - other types: log + ack accepted without enqueue (Phase 1 only handles file_shared).
9. Return `SlackEventAck(status="accepted", event_id=payload.event_id)` with HTTP 200.

The Celery task `refinery.parse_slack_ingress` is configured with `on_success=release_slack_lock_and_mark_complete`, `on_failure=release_slack_lock`. On success, the callback sets `slack:event:{event_id}` = "1" with 24h TTL AND deletes `slack:lock:{event_id}`. On failure, only the lock is released (no post-completion key set — a later legitimate retry can re-attempt).

### D.3 — `POST /slack/interactions`

```python
@router.post("/slack/interactions", response_model=DossierAck)
async def receive_slack_interaction(
    request: Request,
    redis: RedisDep,
    celery: CeleryDep,
    session: SessionDep,
) -> DossierAck:
```

**Logic flow.**
1. HMAC signature verification (same as `/slack/events`).
2. Slack sends interaction payload as form-encoded `payload=<json>`; parse to `SlackDossierAction` via `model_validate_json`.
3. Compute idempotency key: `f"dossier:{action.prospect_id}:{action.signal_hash}:{current_kg_version()}"`.
4. If cached dossier_id exists in Redis: return `DossierAck(dossier_id=cached, status="cached")`.
5. Else: new uuid; `await redis.set(key, new_id, ex=86400*7)`; `celery.send_task("refinery.generate_dossier", args=[action.prospect_id, new_id])`; return `DossierAck(dossier_id=new_id, status="generating")`.

### D.4 — `POST /crm/webhook/{provider}`

```python
@router.post("/crm/webhook/{provider}", response_model=CRMWebhookAck)
async def crm_webhook(
    provider: Literal["hubspot", "salesforce"],
    request: Request,
    redis: RedisDep,
    celery: CeleryDep,
) -> CRMWebhookAck:
```

**Logic flow.**
1. Read raw body.
2. Provider-specific signature verification: Hubspot via `X-HubSpot-Signature-v3` header; Salesforce via configured signature header (Phase 1 mocks both with `X-Mock-Signature`).
3. Parse to `CRMLeadSignal`.
4. `idempotency_key = f"crm:{provider}:{signal.object_id}:{signal.updated_at.isoformat()}:{compute_changed_fields_hash(signal.changed_fields)}"`.
5. If cached: return `CRMWebhookAck(status="duplicate")`.
6. Else: set Redis key 24h; enqueue `refinery.normalize_crm_event`; return `CRMWebhookAck(status="accepted")`.

### D.5 — `POST /crm/actions/generate-dossier`

```python
@router.post("/crm/actions/generate-dossier", response_model=DossierAck)
async def crm_generate_dossier(
    payload: CRMDossierActionRequest,
    redis: RedisDep, celery: CeleryDep, session: SessionDep,
) -> DossierAck:
```

**Logic flow.**
1. Resolve `prospect_id` from `(provider, crm_object_id)` via `lead_prospects` join.
2. If not found: HTTP 404.
3. Same idempotency + enqueue pattern as D.3.

### D.6 — `POST /dossier/generate`

```python
@router.post("/dossier/generate", response_model=DossierAck)
async def generate_dossier(
    payload: DossierRequest,
    redis: RedisDep, celery: CeleryDep, session: SessionDep,
) -> DossierAck:
```

**Logic flow** mirrors PRD §6.3 dossier.py:
1. Fetch `LeadProspect` by `payload.prospect_id`. HTTP 404 if missing.
2. HTTP 409 if `prospect.enrichment_status == "failed"`.
3. Compute idempotency key.
4. If cached AND not `payload.force_regenerate`: return cached `DossierAck(dossier_id=..., status="cached")`.
5. Else enqueue + ack.

### D.7 — `GET /dossier/{dossier_id}`

```python
@router.get("/dossier/{dossier_id}")
async def fetch_dossier(dossier_id: str, session: SessionDep) -> PreVisitDossier | DossierAck:
```

**Logic flow.**
1. Query `dossier_artifacts` by `dossier_id`.
2. If state is `complete`: return `PreVisitDossier`.
3. If state is `generating`: return `DossierAck(dossier_id=..., status="generating")` with HTTP 202.
4. If not found: HTTP 404.

### D.8 — `GET /healthz`

```python
@router.get("/healthz")
async def healthz() -> dict:
    return {"status": "ok"}
```

### D.9 — `GET /readyz`

```python
@router.get("/readyz")
async def readyz(redis: RedisDep, session: SessionDep, vertex: VertexDep) -> JSONResponse:
```

**Logic.**
- Ping Postgres (`SELECT 1`), Redis (`PING`), Vertex client (cached warm result; check on lifespan startup).
- Confirm KG validator ran cleanly at startup (read a flag set by lifespan).
- Return 200 on all healthy, 503 with details on any failure.

### D.10 — `WS /ws/theater/{batch_id}`

WebSocket endpoint. Receives connection, joins a Redis pub/sub channel keyed on `batch_id`, broadcasts pipeline events to client. Closes on client disconnect or batch completion.

---

## §E. Celery Task Specifications

Common decorator pattern:

```python
@app.task(
    name="refinery.<task_name>",
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=3,
)
def <task_name>(self, ...):
```

For the LLM-calling tasks, max_retries is 3 to avoid cost runaway on persistent Vertex AI errors.

### E.1 — `refinery.classify_action_domain` (Stage 0)
- **Input.** `envelope_json: str` deserializing to a discriminated union of `LeadIntakeBatch | SlackEventPayload | CRMLeadSignal | DossierRequest`.
- **Side effects.** Calls `packages.adc.rules.route_request(envelope)` (pure function) and enqueues the result task. No DB writes.
- **Idempotency.** N/A (pure routing; downstream tasks idempotent).
- **Cancellation.** Worker-loss safe; replays cleanly.

### E.2 — `refinery.score_batch` (Stage 1 orchestration)
- **Input.** `batch_id: str`.
- **Logic.**
  1. Load `LeadIntakeBatch` from Postgres.
  2. For each prospect, build a Celery chain: `enrich_prospect.s(prospect_id) | classify_vertical.s() | score_fitness.s()`.
  3. Group all chains; on `chord` callback, run `assemble_queue_and_stubs.s(batch_id)`.
- **Output.** Writes `prioritized_queues` row + `dossier_stubs` rows for top-12.
- **Idempotency.** `batch_id` PK in `score_runs` table. Replay returns existing run.

### E.3 — `refinery.enrich_prospect` (Stage 1.1)
- **Input.** `prospect_id: str`.
- **Logic.** Calls each enrichment adapter (Companies House, web scraper, LinkedIn signal). Aggregates into prospect record. Sets `enrichment_status`.
- **Adapter failures.** Circuit-breaker per adapter. Failures logged. Does not raise; final `enrichment_status` reflects partial state.

### E.4 — `refinery.classify_vertical` (Stage 1.2)
- **Input.** `prospect_id: str`.
- **LLM config.** `gemini-3-flash-preview`, `thinking_level="minimal"`, temps `(0.1, 0.5, 0.9)`, `max_output_tokens=128`, `response_schema=VerticalClassification`.
- **Fan-out.** Three `client.aio.models.generate_content` calls via `asyncio.gather(*[call(t) for t in temps])`.
- **Voting.** Plurality on `.vertical` field. 3-way tie → `vertical = "vertical_uncertain"`, `requires_human_review = True`.
- **Output.** Updates `lead_prospects.vertical`, `.requires_human_review`.

### E.5 — `refinery.score_fitness` (Stage 1.3)
- **Input.** `prospect_id: str`.
- **Logic.** Pure Python — `packages.scoring.fitness.compute_fitness(prospect, queue_state)`.
- **Output.** Updates `lead_prospects.fitness_score`.

### E.6 — `refinery.generate_dossier_stub` (Stage 1.5)
- **Input.** `prospect_id: str`.
- **LLM calls.** **ZERO.** Pure deterministic composition.
- **Logic.**
  1. Load prospect record.
  2. Look up headline KG anchor via `packages.knowledge_graph.select.select_comparable(vertical, basic_taxonomy_proxy=None)`.
  3. Compute `slot_readiness` from `(fitness_score, enrichment_status, requires_human_review)`.
  4. Write `DossierStub` row.
  5. Enqueue outbox writes to Slack canvas + CRM fields + Drive priority-index entry (Tightening 1 transactional outbox — same Postgres tx as the DossierStub insert).

### E.7 — `refinery.generate_dossier` (Stage 2 orchestration)
- **Input.** `prospect_id: str`, `dossier_id: str`.
- **Logic.**
  1. Mark `dossier_artifacts` row as `state="generating"`.
  2. Run section tasks (`refinery.dossier_section_taxonomy` first since others depend on taxonomy; then defect + comparable in parallel; then risk + approach).
  3. On all-section completion, run `refinery.compose_dossier` which:
     - Renders each section to bytes
     - Constructs `PreVisitDossier(...)` — triggers Pydantic validators (Tightening 3 byte-density + Tightening 4 unverified_sections handling)
     - Opens a Postgres transaction; writes `dossier_artifacts` row + three `outbox` rows (Slack/CRM/Drive); commits.

### E.8 — `refinery.dossier_section_taxonomy` (Stage 2.1)
- **Input.** `prospect_id`, `dossier_id`.
- **LLM config.** `gemini-3.1-pro-preview`, `thinking_level="medium"`, N=1, `max_output_tokens=1024`, `response_schema=ProcessTaxonomy`.
- **Prompt template.** `packages.prompts.taxonomy_pro.TAXONOMY_PROMPT` (see §F.2).
- **Output.** Persists `ProcessTaxonomy` to `dossier_artifacts.process_taxonomy`.

### E.9 — `refinery.dossier_section_defect` (Stage 2.2)
- **Input.** `prospect_id`, `dossier_id`.
- **LLM config.** `gemini-3-flash-preview`, `thinking_level="minimal"`, temps `(0.1, 0.5, 0.9)`, `max_output_tokens=512`, `response_schema=LikelyDefectClassHypothesis`.
- **DS-CP check (Tightening 4).** Before LLM call:
  1. Compute `allowed_evidence = packages.knowledge_graph.evidence.compute_allowed_evidence(vertical, "defect_hypothesis", prospect_signals)`.
  2. If `allowed_evidence == []`: skip LLM call, mark section `UNVERIFIED_INSUFFICIENT_DATA`, append `"defect_hypothesis"` to `unverified_sections`, persist a stub `LikelyDefectClassHypothesis(conformal_set=[], coverage=0.0, calibration_version=current, requires_human_review=True, rationale="DS-CP severe shift / no anchor data")`.
  3. Else: compute DS-CP distance via `packages.uncertainty.dscp.semantic_distance(prospect_signals, calibration_centroid_for(vertical))`. If distance > configured threshold: same skip behavior.
- **Else.** Run N=3 fan-out, apply conformal calibration (§H), produce `LikelyDefectClassHypothesis`.

### E.10 — `refinery.dossier_section_comparable` (Stage 2.3a + 2.3b)
- **Input.** `prospect_id`, `dossier_id`.
- **Stage 2.3a — deterministic.**
  ```
  anchor = packages.knowledge_graph.select.select_comparable(vertical, process_taxonomy)
  # returns one of MATTA_CUSTOMER_ANCHOR_ENUM or "no_comparable_available"
  ```
- If anchor is `"no_comparable_available"`: persist `ComparableDeployment(matta_customer_anchor="no_comparable_available", citation_substrate_line=0, dimension_of_comparability="No verified Matta deployment in this vertical sub-path.", selection_method="no_comparable_available")`. Skip 2.3b.
- **Stage 2.3b — Pro prose.** `gemini-3.1-pro-preview`, `thinking_level="low"`, N=1, `max_output_tokens=256`, `response_schema=DimensionOfComparabilityProse` (a wrapper schema with a single `prose: Annotated[str, Field(max_length=250)]` field). The prompt PASSES IN the selected anchor + permitted dimensions and INSTRUCTS the model: "Do NOT propose a different anchor. Do NOT exceed 250 characters."
- Pydantic boundary on `ComparableDeployment.dimension_of_comparability` enforces ≤250 cap.

### E.11 — `refinery.dossier_section_risk` (Stage 2.4)
- **LLM config.** `gemini-3.1-pro-preview`, `thinking_level="low"`, N=1, `max_output_tokens=768`, `response_schema=RiskRegister`.
- **Constraint.** Prompt explicitly lists the `RISK_CATEGORY_ENUM`; LLM cannot invent categories (Pydantic boundary enforces).

### E.12 — `refinery.dossier_section_approach` (Stage 2.5)
- **LLM config.** `gemini-3.1-pro-preview`, `thinking_level="low"`, N=1, `max_output_tokens=768`, `response_schema=SuggestedApproach`.
- **Constraint.** Prompt lists `APPROACH_TEMPLATE_ENUM`; cannot invent.

### E.13 — `refinery.outbox_dispatcher` (Tightening 1 message-relay)
- **Trigger.** Cloud Tasks invocation, payload contains `outbox_id`.
- **Logic.** See §L.3.
- **DLQ.** After 6 failed attempts, row moved to **`outbox_dlq`** table (NOT `cmms_outbox_dlq` — vestigial naming corrected per §A.5).
- **Side effects.** Calls the appropriate surface adapter (Slack/CRM/Drive). Updates `outbox.delivery_attempts`, `outbox.state`, `outbox.last_error`. WebSocket emits `outbox.dispatched` or `outbox.dlq`.

### E.14 — `refinery.release_slack_lock` (Tightening 2 callback)
- **Trigger.** Wired as `on_success` and `on_failure` callbacks on `refinery.parse_slack_ingress`.
- **On success.** `redis.set(f"slack:event:{slack_event_id}", "1", ex=86400)`; then `redis.delete(f"slack:lock:{slack_event_id}")`.
- **On failure.** `redis.delete(f"slack:lock:{slack_event_id}")` only — no post-completion key set.

### E.15 — `refinery.parse_slack_ingress`
- **Input.** `payload_json: str` (the SlackEventPayload).
- **Logic.** Fetches the shared file via Slack Web API (mock), parses CSV via `parse_csv_to_batch`, persists batch + prospects, enqueues `refinery.score_batch`.
- **Callbacks.** `on_success=release_slack_lock_and_mark_complete`, `on_failure=release_slack_lock` per §E.14.

### E.16 — `refinery.normalize_crm_event`
- **Input.** `signal_json: str` (CRMLeadSignal).
- **Logic.** Translates provider-specific field names to canonical names; upserts `lead_prospects` row; sets/refreshes `signal_hash`; enqueues `refinery.classify_vertical` if vertical missing or stale.

### E.17 — `refinery.compose_dossier`
- **Input.** `dossier_id: str`.
- **Logic.**
  1. Begin Postgres transaction.
  2. Load all five section outputs from intermediate storage.
  3. Render each section to bytes (`rendered_sections` dict).
  4. Construct `PreVisitDossier(...)` — triggers `model_validator`. If Tightening 3 rejects (ratio < 0.60), abort transaction; emit `dossier.rejected` WebSocket event; do NOT persist; mark `dossier_artifacts` row `state="rejected_byte_ratio"`.
  5. Else: write `dossier_artifacts` row + three `outbox` envelopes (Slack/CRM/Drive) inside same tx.
  6. Commit.
  7. Cloud Tasks schedule outbox dispatch.

---

## §F. Vertex AI Prompt Templates (Per-Stage)

Common SDK call pattern (verified per PRD §6.4):

```python
from google import genai
from google.genai.types import GenerateContentConfig, ThinkingConfig

# at module init
client = genai.Client(vertexai=True, project=settings.gcp_project, location="europe-west4")

# at call site
response = await client.aio.models.generate_content(
    model=MODEL_STRING,
    contents=[PROMPT.format(**payload)],
    config=GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=SCHEMA,
        thinking_config=ThinkingConfig(thinking_level=THINKING_LEVEL),
        temperature=TEMP,
        max_output_tokens=MAX_OUT,
    ),
)
parsed = SCHEMA.model_validate_json(response.text)
```

### F.1 — `packages/prompts/vertical_flash.py`

```
MODEL = "gemini-3-flash-preview"
THINKING_LEVEL = "minimal"
TEMPS = (0.1, 0.5, 0.9)
MAX_OUT = 128
RESPONSE_SCHEMA = VerticalClassification

VERTICAL_PROMPT = """You are classifying a UK or EU manufacturing prospect into a vertical
from a fixed enum. Output strict JSON conforming to the schema. Choose `out_of_vertical` if the
prospect is clearly outside the manufacturing surface listed below; do not stretch.

Prospect:
- Company name: {company_name}
- Sector hint (from raw data, may be empty or noisy): {sector_hint}
- Public enrichment summary: {enrichment_summary}
- Raw notes from the trade-show or CRM: {raw_notes}

Allowed vertical values (choose exactly one):
- polymer_extrusion: continuous polymer extrusion, polymer molding, polymer line work
- metal_casting: ductile iron casting, sand casting, investment casting, die casting
- additive_manufacturing: large-format AM, industrial 3D printing, AM cells (OEM partner context: Caracol)
- fnb_bottling: high-speed bottling, F&B packaging, beverage line inspection
- electronics_assembly: precision component assembly, speaker/electronics QC, small-form-factor metrology
- aerospace: aerospace components, plane wings, titanium alloys, aerospace metallurgy
- out_of_vertical: prospect is clearly outside the above set

Output JSON only."""
```

### F.2 — `packages/prompts/taxonomy_pro.py`

```
MODEL = "gemini-3.1-pro-preview"
THINKING_LEVEL = "medium"
TEMP = 0.2
MAX_OUT = 1024
RESPONSE_SCHEMA = ProcessTaxonomy

TAXONOMY_PROMPT = """You are synthesizing a process taxonomy for a manufacturing prospect.
Output strict JSON conforming to ProcessTaxonomy.

Prospect:
- Company name: {company_name}
- Vertical (already classified by Stage 1.2): {vertical}
- Public enrichment payload: {enrichment_payload}
- Allowed evidence whitelist (lines from substrate, cite only from this list when you reference
  factual claims; do NOT invent claims that require evidence outside this list): {allowed_evidence}

Produce:
- primary_process: the dominant production process at line-level granularity (≤200 chars)
- sub_processes: up to 10 sub-process names (each ≤80 chars)
- line_level_steps: up to 20 step names in the production order (each ≤80 chars)
- rationale: 1-3 sentence explanation tied to vertical + enrichment (≤600 chars)

Output JSON only."""
```

### F.3 — `packages/prompts/defect_flash.py`

```
MODEL = "gemini-3-flash-preview"
THINKING_LEVEL = "minimal"
TEMPS = (0.1, 0.5, 0.9)
MAX_OUT = 512
RESPONSE_SCHEMA = LikelyDefectClassHypothesis

DEFECT_PROMPT = """Classify the likely defect classes for this manufacturing process. Output
strict JSON conforming to LikelyDefectClassHypothesis. Do NOT invent defect categories outside
the enum. Do NOT claim high coverage when your evidence is thin.

Process context:
- Vertical: {vertical}
- Process taxonomy: {process_taxonomy_json}
- Allowed evidence whitelist: {allowed_evidence}

Allowed defect classes (your conformal_set field is a subset of these):
- porosity, dimensional_drift, surface_inclusions, tool_wear, calibration_drift,
- material_defect, process_drift, unknown

Decision rules:
- If the process is well-understood and you have specific evidence, include the 1-3 most likely
  defect classes in conformal_set and set coverage to your honest estimate (0.0-1.0).
- If evidence is weak or the process is out-of-vertical, return an empty conformal_set or
  include only "unknown"; the system will mark for human review.
- The calibration_version field will be overwritten by the system; populate as best-effort.

Output JSON only."""
```

The N=3 plurality vote runs over the `conformal_set` field; the conformal calibration table (see §H) adjusts inclusion thresholds at the post-LLM step.

### F.4 — `packages/prompts/comparable_pro.py`

```
MODEL = "gemini-3.1-pro-preview"
THINKING_LEVEL = "low"
TEMP = 0.3
MAX_OUT = 256
RESPONSE_SCHEMA = DimensionOfComparabilityProse  # wrapper: { prose: str }

COMPARABLE_PROMPT = """A deterministic rules engine has PRE-SELECTED the comparable Matta
deployment anchor for this prospect. Your job is to write a 1-2 sentence `dimension_of_comparability`
explaining the AXIS on which the comparison holds.

PRE-SELECTED anchor (do NOT propose a different anchor): {matta_customer_anchor}
Anchor citation substrate line: {citation_substrate_line}
Permitted dimensions of comparability for this anchor (choose ONE or compose from this set ONLY):
{permitted_dimensions_of_comparability}

Prospect:
- Company name: {company_name}
- Vertical: {vertical}
- Process taxonomy: {process_taxonomy_json}

Strict constraints:
- Do NOT propose a different anchor. Do NOT cite a different Matta deployment.
- Do NOT exceed 250 characters in your prose.
- Name the dimension explicitly (e.g., 'surface-finish QC stage similarity'); name what does
  NOT carry over (e.g., 'NOT process category, NOT production volume') if relevant in your 250 chars.

Output JSON with a single field `prose` containing the ≤250-char string."""
```

The Pydantic boundary on `ComparableDeployment.dimension_of_comparability` enforces the 250-char cap as defense-in-depth.

### F.5 — `packages/prompts/risk_pro.py`

```
MODEL = "gemini-3.1-pro-preview"
THINKING_LEVEL = "low"
TEMP = 0.2
MAX_OUT = 768
RESPONSE_SCHEMA = RiskRegister

RISK_PROMPT = """Produce a risk register for this prospect's likely Matta deployment. Output
strict JSON conforming to RiskRegister. Use ONLY the fixed risk categories below; do NOT invent
new categories.

Prospect:
- Company name: {company_name}
- Vertical: {vertical}
- Process taxonomy: {process_taxonomy_json}
- Public enrichment payload: {enrichment_payload}

Fixed risk categories (your findings list uses these enum values):
- legacy_cmm_infrastructure, lighting_variance, emf_environment, network_topology,
- ot_it_segmentation, regulatory_audit_burden, operator_training_overhead,
- calibration_baseline_unknown

For each finding, set severity = identified | unknown | not_applicable. Provide a 1-2 sentence
note (≤300 chars) anchored to the prospect's vertical and process taxonomy.

Output JSON only."""
```

### F.6 — `packages/prompts/approach_pro.py`

```
MODEL = "gemini-3.1-pro-preview"
THINKING_LEVEL = "low"
TEMP = 0.2
MAX_OUT = 768
RESPONSE_SCHEMA = SuggestedApproach

APPROACH_PROMPT = """Produce a suggested-approach recommendation. Output strict JSON conforming
to SuggestedApproach. Use ONLY the fixed template enum; do NOT invent new templates.

Prospect:
- Company name: {company_name}
- Vertical: {vertical}
- Process taxonomy: {process_taxonomy_json}
- Defect-class hypothesis conformal set: {conformal_set}
- Identified risks: {risk_findings}

Fixed approach templates:
- two_camera_pilot, four_camera_pilot, full_line_deployment, caracol_am_oem_partnership

Compose:
- template: one of the enum above.
- rationale: 1-3 sentence explanation tied to vertical + defect + risk (≤600 chars).
- day_one_risks: up to 8 short strings (each ≤120 chars) naming risks the FDE should expect on
  day 1 of deployment (e.g., 'lighting calibration', 'PLC OPC-UA gateway access').

Output JSON only."""
```

---

## §G. Knowledge Graph Specification

### G.1 — `packages/knowledge_graph/graph.json` structure

```json
{
  "version": "phase1-v1",
  "built_at": "2026-05-11T00:00:00Z",
  "anchors": [
    {
      "anchor_id": "matta_deployment_bowers_and_wilkins",
      "vertical": "electronics_assembly",
      "deployment_type": "precision_speaker_components",
      "citation_substrate_lines": [83, 540, 600],
      "citation_verbatim_excerpt": "working with Bowers & Wilkins, where Matta",
      "permitted_dimensions_of_comparability": [
        "surface_finish_qc",
        "precision_machining_inspection",
        "small_form_factor_metrology"
      ]
    },
    {
      "anchor_id": "matta_deployment_caracol_am",
      "vertical": "additive_manufacturing",
      "deployment_type": "oem_closed_loop_partnership",
      "citation_substrate_lines": [83, 271, 542, 602],
      "citation_verbatim_excerpt": "OEMs, Caracol",
      "permitted_dimensions_of_comparability": [
        "additive_manufacturing_inspection",
        "oem_closed_loop_partnership",
        "large_format_robot_am_cell"
      ]
    },
    {
      "anchor_id": "matta_deployment_global_drinks_brand",
      "vertical": "fnb_bottling",
      "deployment_type": "high_speed_bottling_qc",
      "citation_substrate_lines": [540, 600],
      "citation_verbatim_excerpt": "high-speed bottling for defects with a global drinks brand",
      "permitted_dimensions_of_comparability": [
        "high_speed_line_qc",
        "fnb_packaging_inspection",
        "bottling_throughput_anomaly_detection"
      ]
    },
    {
      "anchor_id": "matta_deployment_polymer_unnamed",
      "vertical": "polymer_extrusion",
      "deployment_type": "polymer_line_defect_detection",
      "citation_substrate_lines": [540, 600],
      "citation_verbatim_excerpt": "polymer manufacturing deployment, Matta achieved over 99% defect-detection",
      "permitted_dimensions_of_comparability": [
        "polymer_extrusion_defect_detection",
        "continuous_line_inspection",
        "few_shot_calibration_minutes_not_hours"
      ]
    },
    {
      "anchor_id": "matta_deployment_metal_casting_unnamed",
      "vertical": "metal_casting",
      "deployment_type": "casting_line_qc",
      "citation_substrate_lines": [271, 421],
      "citation_verbatim_excerpt": "polymer manufacturing and metal casting to bottling and consumer electronics",
      "permitted_dimensions_of_comparability": [
        "casting_surface_finish_qc",
        "metallurgical_inspection",
        "ductile_iron_inspection_baseline"
      ]
    }
  ]
}
```

Phase 1 seeds these 5 anchors. Phase 2 expansion fills out the ~360-anchor target (6 verticals × 5 defect classes × ~12 anchors).

**Cummins exclusion enforced.** No anchor with `anchor_id` containing `cummins` is permitted in `graph.json`. The graph loader raises if it finds one. The Cummins exclusion is a load-bearing audit-trail invariant from `MATTA_MASTER_PRD_v2.md §1.F`.

### G.2 — `packages/knowledge_graph/loader.py`

```python
class KnowledgeGraphAnchor(BaseModel):
    model_config = ConfigDict(extra="forbid")
    anchor_id: str
    vertical: VERTICAL_ENUM
    deployment_type: str
    citation_substrate_lines: list[Annotated[int, Field(ge=1, le=100000)]]
    citation_verbatim_excerpt: Annotated[str, Field(min_length=10, max_length=500)]
    permitted_dimensions_of_comparability: list[Annotated[str, Field(max_length=80)]]

class KnowledgeGraph(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str
    built_at: datetime
    anchors: list[KnowledgeGraphAnchor]

def load_graph(path: Path = Path("packages/knowledge_graph/graph.json")) -> KnowledgeGraph:
    raw = path.read_text(encoding="utf-8")
    return KnowledgeGraph.model_validate_json(raw)
```

### G.3 — `packages/knowledge_graph/verify.py`

```python
class KnowledgeGraphProvenanceError(RuntimeError):
    pass

SUBSTRATE_PATH = Path("Matta_Intel_cleaned.md")

def validate_graph_or_die() -> None:
    graph = load_graph()
    substrate_lines = SUBSTRATE_PATH.read_text(encoding="utf-8").splitlines()
    for anchor in graph.anchors:
        if "cummins" in anchor.anchor_id.lower():
            raise KnowledgeGraphProvenanceError(
                f"Cummins is excluded as a deployment anchor (MATTA_MASTER_PRD_v2.md §1.F). "
                f"Found: {anchor.anchor_id}"
            )
        for line_no in anchor.citation_substrate_lines:
            if line_no < 1 or line_no > len(substrate_lines):
                raise KnowledgeGraphProvenanceError(
                    f"Anchor {anchor.anchor_id} cites substrate line {line_no} which is out of range "
                    f"(substrate has {len(substrate_lines)} lines)."
                )
            line_text = substrate_lines[line_no - 1]
            if anchor.citation_verbatim_excerpt not in line_text:
                raise KnowledgeGraphProvenanceError(
                    f"Anchor {anchor.anchor_id} citation_verbatim_excerpt "
                    f"'{anchor.citation_verbatim_excerpt}' not found in substrate line {line_no}."
                )
```

CLI mode in `scripts/verify_knowledge_graph.py`:

```python
if __name__ == "__main__":
    try:
        validate_graph_or_die()
        print("Knowledge graph provenance check passed.")
        sys.exit(0)
    except KnowledgeGraphProvenanceError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        sys.exit(1)
```

### G.4 — `packages/knowledge_graph/select.py`

```python
def select_comparable(
    vertical: str,
    process_taxonomy: ProcessTaxonomy | None,
) -> tuple[MATTA_CUSTOMER_ANCHOR_ENUM, int, list[str]]:
    """Deterministic comparable selection (v4 Stage 2.3a contribution).

    Returns (anchor_id, citation_substrate_line, permitted_dimensions_of_comparability).
    Returns ('no_comparable_available', 0, []) if no anchor matches.
    """
    # Phase 1 rules: 1-to-1 vertical → anchor mapping, demoted to multi-key when verticals expand.
    vertical_to_anchor = {
        "electronics_assembly": "matta_deployment_bowers_and_wilkins",
        "additive_manufacturing": "matta_deployment_caracol_am",
        "fnb_bottling": "matta_deployment_global_drinks_brand",
        "polymer_extrusion": "matta_deployment_polymer_unnamed",
        "metal_casting": "matta_deployment_metal_casting_unnamed",
        # aerospace, out_of_vertical, vertical_uncertain → no_comparable_available
    }
    anchor_id = vertical_to_anchor.get(vertical)
    if anchor_id is None:
        return ("no_comparable_available", 0, [])
    anchor = _find_anchor_by_id(anchor_id)  # from loaded graph cache
    return (
        _enum_for_anchor_id(anchor_id),  # maps to MATTA_CUSTOMER_ANCHOR_ENUM
        anchor.citation_substrate_lines[0],  # primary citation line
        anchor.permitted_dimensions_of_comparability,
    )
```

### G.5 — `packages/knowledge_graph/evidence.py`

```python
def compute_allowed_evidence(
    vertical: str,
    section_type: Literal["taxonomy", "defect_hypothesis", "comparable", "risk", "approach"],
    prospect_signals: dict,
) -> list[int]:
    """Compute the citation-substrate-line whitelist for a given section + prospect.

    Returns the union of substrate lines from KG anchors whose vertical matches AND whose
    deployment_type relevance to the section_type is non-zero. Empty list signals 'no anchor data'
    and triggers section-granular DS-CP (Tightening 4) to mark the section UNVERIFIED_INSUFFICIENT_DATA.
    """
    graph = load_graph()
    matching_anchors = [a for a in graph.anchors if a.vertical == vertical]
    if not matching_anchors:
        return []  # Triggers DS-CP strip
    all_lines = set()
    for a in matching_anchors:
        all_lines.update(a.citation_substrate_lines)
    return sorted(all_lines)
```

---

## §H. Conformal Calibration Specification

### H.1 — `packages/uncertainty/conformal.py`

Split-conformal calibration applied to the N=3 Gemini Flash defect-class ensemble (Stage 2.2 per `ULTIMATE_PRD.md §3.4 step 2.2`). Methodology: Vovk-style coverage guarantee at α=0.1 (90% set coverage target). Doug Brion's `dougbrion/pytorch-deep-ensembles` repo is the structural anchor; arXiv 2510.05566 (Lin et al. 2025) is the distribution-shift extension.

```python
class CalibrationTable(BaseModel):
    model_config = ConfigDict(extra="forbid")
    calibration_version: str
    alpha: Annotated[float, Field(ge=0.0, le=1.0)]
    coverage_target: Annotated[float, Field(ge=0.0, le=1.0)]
    nonconformity_thresholds_by_class: dict[str, float]
    built_at: datetime
    holdout_size: int
    seed: int

def compute_conformal_set(
    ensemble_outputs: list[LikelyDefectClassHypothesis],
    calibration: CalibrationTable,
) -> tuple[list[str], float]:
    """Given N=3 ensemble outputs and the calibrated table, return (conformal_set, coverage).

    Algorithm:
    1. Aggregate the three sample outputs into per-class vote shares: share = votes / N.
    2. For each class, compare share against its nonconformity_thresholds_by_class[class].
    3. Class is in the conformal_set iff share >= 1 - threshold.
    4. coverage = calibration.coverage_target if set is non-empty and not all-class; else 0.0.
    5. Empty or all-class set → degenerate; the Pydantic model_validator on LikelyDefectClassHypothesis
       flags requires_human_review = True (per §C.3).
    """
```

### H.2 — `scripts/build_calibration_table.py`

```python
def main():
    """Phase 1 calibration table build.

    Reads 30 hand-labeled mock events from mocks/calibration_holdout.json.
    Runs the production prompt template against each with N=3 Flash sampling.
    Computes nonconformity scores at α=0.1 (target 90% set coverage).
    Outputs packages/uncertainty/calibration_table.json with deterministic seed=42.
    """
    holdout = load_holdout("mocks/calibration_holdout.json")
    assert len(holdout) == 30, f"Expected 30 holdout events, got {len(holdout)}"

    rng = random.Random(42)
    ensemble_outputs_by_class = defaultdict(list)
    for event in holdout:
        samples = run_n3_flash_ensemble(event, prompt=DEFECT_PROMPT)
        true_class = event["true_defect_class"]
        # Record vote share for the true class on this event.
        true_share = sum(1 for s in samples if true_class in s.conformal_set) / len(samples)
        ensemble_outputs_by_class[true_class].append(true_share)

    # Compute α=0.1 quantile of (1 - true_share) per class — the nonconformity score threshold.
    thresholds = {}
    for cls, shares in ensemble_outputs_by_class.items():
        nonconformity_scores = [1.0 - s for s in shares]
        nonconformity_scores.sort()
        # quantile index at α=0.1 with finite-sample correction (Vovk)
        n = len(nonconformity_scores)
        quantile_idx = math.ceil((n + 1) * (1 - 0.1)) - 1
        quantile_idx = min(quantile_idx, n - 1)
        thresholds[cls] = nonconformity_scores[quantile_idx]

    table = CalibrationTable(
        calibration_version="phase1-demo-v1",
        alpha=0.1,
        coverage_target=0.9,
        nonconformity_thresholds_by_class=thresholds,
        built_at=datetime.utcnow(),
        holdout_size=30,
        seed=42,
    )
    Path("packages/uncertainty/calibration_table.json").write_text(table.model_dump_json(indent=2))
```

Deterministic seed = 42; Damjan must be able to re-run and get identical thresholds.

### H.3 — `packages/uncertainty/dscp.py` (Tightening 4)

Section-granular Domain-Shift-Aware Conformal Prediction. Per `ULTIMATE_PRD.md §3.6` (Tightening 4) and the Lin et al. 2025 methodology reference (arXiv 2510.05566).

```python
def semantic_distance(
    prospect_signals: dict,
    calibration_centroid_for_vertical: dict,
) -> float:
    """Compute a semantic-distance proxy between the prospect signal vector and the calibration
    distribution centroid for the prospect's vertical. Phase 1 implementation: hash-based
    feature overlap proxy (cosine of sparse feature vectors). Phase 2 upgrade: embed signals via
    Vertex AI text-embedding model and cosine in embedding space.
    """

DSCP_SEVERE_SHIFT_THRESHOLD = 0.55  # Phase 1 calibrated against the 30-event holdout; tune in Phase 2.

def section_passes_dscp_gate(
    section_type: str,
    vertical: str,
    prospect_signals: dict,
    allowed_evidence: list[int],
) -> bool:
    """Returns False if the section should be stripped per DS-CP. True if section can proceed."""
    if not allowed_evidence:
        return False  # No anchor data for this vertical sub-path
    distance = semantic_distance(prospect_signals, _centroid_for(vertical))
    return distance <= DSCP_SEVERE_SHIFT_THRESHOLD
```

---

## §I. Mock Data Specifications

### I.1 — `scripts/seed_mock_data.py`

Produces all Phase 1 mock data deterministically. Single invocation: `python scripts/seed_mock_data.py`.

**Outputs.**
- `mocks/UK_Metals_Expo_2025_leads.csv` — 124 rows. 30% real attendees, 70% synthetic.
- `mocks/calibration_holdout.json` — 30 hand-labeled defect-class events.
- `mocks/mock_slack/seed_workspace.json` — Slack workspace state.
- `mocks/mock_crm/seed_contacts.json` — Hubspot/Salesforce contacts.
- `mocks/mock_drive/seed_folders.json` — Drive folder structure.

### I.2 — `UK_Metals_Expo_2025_leads.csv` specification

```
external_lead_id,company_name,contact_name,contact_email,sector_hint,factory_size_band,raw_notes
W001,William Cook Sheffield,(generated),(generated)@wcook-sheffield.example,ductile iron casting,medium,booth-conversation:porosity-spike-on-pour-A
T002,Tata Steel UK,(generated),...,steel,large,...
E003,Ernest Wright,...,blade-grinding,small,...
C004,Centriblast,...,abrasive blasting,medium,...
S005,Safran Seats GB,...,aerospace seat assembly,large,...
... (119 more synthetic rows mixing across the 6 verticals)
```

The first 5 rows are real UK Metals Expo attendees verified at `Matta_Intel_cleaned.md` line 294. William Cook Sheffield MUST be the highest-fitness-score prospect post-Stage-1 (verified vertical: `metal_casting`; comparable: `matta_deployment_metal_casting_unnamed` via line 271 citation; trade-show provenance: true; size band: medium; fitness ≈ 0.84 expected from the scoring weights in §B/`packages/scoring/weights.py`).

Backup prospects #2 and #3 (next-highest fitness) pre-seeded for Vertex AI rate-limit insurance during the live demo.

### I.3 — `mocks/calibration_holdout.json` specification

30 hand-labeled entries. Distribution: 4 events per major class (porosity, dimensional_drift, surface_inclusions, tool_wear, calibration_drift, material_defect, process_drift) plus 2 events labeled `unknown`. Each entry:

```json
{
  "event_id": "calib_001",
  "vertical": "metal_casting",
  "process_taxonomy_summary": "ductile iron pour into molds; ladle pour at ~1450C",
  "true_defect_class": "porosity",
  "raw_context": "Operator notes increased porosity defects on Pour A line after ladle refurb."
}
```

Labels are hand-set; the calibration script does NOT call an LLM to label.

### I.4 — `mocks/mock_slack/` server

FastAPI sidecar on port 8090. Endpoints:
- `POST /api/auth.test` — returns demo workspace metadata.
- `POST /api/files.info` — returns mock file metadata for a given `file_id`.
- `POST /api/files.share` — accepts a file post (test setup).
- `POST /api/canvases.edit` — accepts a canvas update.
- `POST /api/chat.postMessage` — accepts a message post.

Signature secret: from env `SLACK_SIGNING_SECRET=mock-signing-secret-phase1`. The mock server validates inbound HMAC the same way the real Slack would.

### I.5 — `mocks/mock_crm/` server

FastAPI sidecar on port 8091. Implements both Hubspot-flavored and Salesforce-flavored endpoints:
- `POST /hubspot/webhook` — emits a `CRMLeadSignal` to the refinery_api.
- `PATCH /hubspot/contacts/{id}` — accepts field writeback.
- `POST /hubspot/contacts/{id}/notes` — accepts note writeback.
- `POST /salesforce/webhook` — similar.
- `PATCH /salesforce/contacts/{id}` — similar.

### I.6 — `mocks/mock_drive/` server

FastAPI sidecar on port 8092. Endpoints:
- `POST /drive/files` — create a Google Doc; returns `{file_id, web_view_link}`.
- `PATCH /drive/files/{file_id}` — update content.
- `POST /drive/files/{file_id}/permissions` — generate share link.

### I.7 — `mocks/mock_matta_dashboard/`

This is **NOT** a Matta product surface. Per `ULTIMATE_PRD.md §5.4`, the Theater UI's CRM record inset is a Hubspot-style mocked panel; the directory name `mock_matta_dashboard` is vestigial from the v0 Refinery PRD and is reused here for the Hubspot CRM record inset rendering. Build accordingly — Tailwind, no Matta wordmark, no Matta UI elements; CRM-flavored only.

---

## §J. Theater UI Component Tree

Stack: Next.js 14 (app dir or pages dir — Phase 1 uses pages dir for simplicity), Tailwind, no UI component library imports. All Tailwind utility classes inline.

### J.1 — `apps/theater_ui/pages/index.tsx`

```typescript
interface IndexPageProps {
  batchId: string  // from query string
}

const IndexPage: NextPage<IndexPageProps> = ({ batchId }) => {
  const { events, connected } = useWebSocket(`/ws/theater/${batchId}`)
  return (
    <div className="grid grid-cols-3 h-screen relative">
      <SlackLeftPane events={events} />
      <TheaterCenterPane events={events} />
      <DriveDossierRightPane events={events} />
      <CRMRecordInset events={events} />  {/* fixed positioning, bottom-right */}
    </div>
  )
}
```

### J.2 — `components/SlackLeftPane.tsx`

**Props.** `events: TheaterEvent[]`.
**State.** `csvFile?: { name: string; rows: number }`, `canvasContent?: SlackCanvasPayload`.
**WebSocket message types consumed.** `ingest.ack`, `stage1.complete`, `stage2.complete`.
**Visual hierarchy.**
- Header: `#fde-lead-refinery` channel name + Slack-style chrome.
- Message thread: forwarded email → CSV attachment tile → canvas materializes inline.
- "Generate Full Dossier" button on top prospect (William Cook Sheffield) triggers `POST /slack/interactions` (mocked through the mock_slack server).

### J.3 — `components/TheaterCenterPane.tsx`

**Props.** `events: TheaterEvent[]`.
**Visual hierarchy** (top to bottom):
- **Inbound event card.** Raw event JSON with signature-verification badge.
- **ADC decision badge.** Pill showing the deterministic route (e.g., `PRIORITIZATION` or `DOSSIER_FULL`).
- **Idempotency keys panel.** Three keys: batch + prospect + dossier.
- **Stage 1 progress.** Per-prospect cards with vertical-vote ensemble + fitness score.
- **Stage 2 progress.** Five horizontal cards (taxonomy / defect / comparable / risk / approach), each fills as section completes.
- **Defect-class ensemble visualization.** Three Flash-sample cards filling in with categorical distributions; conformal calibration shown as a fourth card aggregating the three; the conformal coverage statement renders live.
- **Comparable card highlight.** When Stage 2.3a runs, the card visibly highlights "Deterministic selection from KG (LLM did NOT pick this anchor)" — this is the v4-contribution audit surface.
- **Deterministic-vs-LLM byte-density coverage meter.** Live bar showing `det_bytes / total_bytes`; green when ≥0.60, red when below. Tightening 3 audit surface.
- **Cost ticker.** Running Vertex AI cost; target under $0.10 per dossier.
- **Citation panel.** Expandable side-panel; click any KG anchor to see the verbatim line excerpt from `Matta_Intel_cleaned.md`.
- **JSON inspector.** Click any pipeline stage to see Pydantic-validated payload; `extra="forbid"` badge always visible.
- **Outbox inspector.** Bottom panel showing per-surface outbox state (`pending` / `in_flight` / `delivered` / `dlq`) with row count and DLQ visibility.

### J.4 — `components/DriveDossierRightPane.tsx`

**Props.** `events: TheaterEvent[]`.
**Render.** Mocked Google Doc with title "Matta Pre-Visit Dossier — {company_name} — {date}". Sections fill in as `stage2.section_complete` events arrive:
- Header: `last_verified_at`, `knowledge_graph_version`, `calibration_version`.
- §1 Process taxonomy.
- §2 Defect-class hypothesis (with coverage statement: "With X% coverage, dominant defect classes are in: {...}").
- §3 Comparable Matta deployment (anchor name + dimension_of_comparability + clickable substrate line citation).
- §4 Integration risk register (table).
- §5 Suggested approach.
- §6 Evidence appendix (all KG anchors used).
- Footer: `[Share]` button (mock; copies share-link to clipboard).
- **Unverified sections note.** If `unverified_sections.length > 0`, render: `"⚠ N sections marked unverified — see Theater for DS-CP details"` near top.

### J.5 — `components/CRMRecordInset.tsx`

**Props.** `events: TheaterEvent[]`.
**Render.** Bottom-right `w-80 h-48` fixed-position panel. Hubspot-style contact record for William Cook Sheffield. Fields update live:
- `refinery_fit_score: 0.84` at T+8.
- `vertical: metal_casting` at T+8.
- `slot_readiness: ready_for_dossier` at T+8.
- `requires_human_review: false` at T+8.
- Notes section appends: "Pre-Visit Dossier generated 2026-05-11, link: drive.google.com/…" at T+88.

### J.6 — `hooks/useWebSocket.ts`

```typescript
interface UseWebSocketReturn {
  events: TheaterEvent[]
  connected: boolean
  lastEvent: TheaterEvent | null
}

interface TheaterEvent {
  type: 'ingest.ack' | 'adc.routed' | 'stage1.enriched' | 'stage1.vertical_voted'
      | 'stage1.scored' | 'stage1.complete' | 'stage2.section_started'
      | 'stage2.section_complete' | 'stage2.complete' | 'outbox.dispatched'
      | 'outbox.dlq' | 'cost.ticker'
  timestamp: string
  payload: Record<string, unknown>
}

export function useWebSocket(url: string): UseWebSocketReturn { ... }
```

State managed via `useReducer`; reconnect on disconnect with exponential backoff (max 5 attempts then stop).

---

## §K. Required Dependencies (Exact Pins)

### K.1 — `pyproject.toml`

```toml
[project]
name = "matta-refinery"
version = "0.1.0"
requires-python = ">=3.12,<3.13"
dependencies = [
  "fastapi>=0.136,<0.137",
  "pydantic>=2.13,<3",
  "pydantic-settings>=2.6",
  "google-genai>=1.0",
  "celery>=5.5,<5.6",
  "redis>=5.2,<6",
  "sqlalchemy>=2.0,<2.1",
  "alembic>=1.13",
  "asyncpg>=0.30",
  "slack-sdk>=3.27",                # signature verification; Phase 1 uses against mock server
  "hubspot-api-client>=11.0",       # adapter; Phase 1 uses against mock server
  "simple-salesforce>=1.13",        # adapter; Phase 1 uses against mock server
  "google-api-python-client>=2.150",# Drive; Phase 1 uses against mock server
  "google-cloud-tasks>=2.16",
  "google-cloud-secret-manager>=2.20",
  "python-multipart>=0.0.9",
  "httpx>=0.27",
  "structlog>=24",
  "uvicorn[standard]>=0.32",
  "gevent>=24",                     # Celery worker pool
]

[project.optional-dependencies]
dev = [
  "pytest>=8.0",
  "pytest-asyncio>=0.24",
  "pytest-postgresql>=6.0",
  "ruff>=0.7",
  "mypy>=1.13",
  "freezegun>=1.5",
]
```

### K.2 — `apps/theater_ui/package.json`

```json
{
  "name": "theater_ui",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev -p 3000",
    "build": "next build",
    "start": "next start -p 3000",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^14.2.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "tailwindcss": "^3.4.0"
  },
  "devDependencies": {
    "typescript": "^5.5.0",
    "@types/node": "^22",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "autoprefixer": "^10.4",
    "postcss": "^8.4"
  }
}
```

### K.3 — Vestigial naming reminder

DLQ table in Alembic migration is **`outbox_dlq`**, NOT `cmms_outbox_dlq`. SQLAlchemy ORM class `OutboxDLQ`, NOT `CMMSOutboxDLQ`. Documented at §A.5, §B (`packages/outbox/models.py`), §E.13.

---

## §L. Backend Engine Logic Flows

### L.1 — Flow: CSV ingest → Stage 1 → top-12 dossier stubs (Magic Moment 1)

```
1. User uploads UK_Metals_Expo_2025_leads.csv via Theater (or Slack /matta-refinery triage).
2. Theater: POST /ingest/batch  OR  Slack: POST /slack/events (file_shared event).
3. Refinery_api validates signature (Slack only), computes file_sha256, checks Redis idempotency.
4. Parses CSV → LeadIntakeBatch (Pydantic). Rejects if extra="forbid" fails.
5. Inside one Postgres tx:
   a. Insert ingest_batches row.
   b. Upsert 124 lead_prospects rows (PK: (source_system, external_lead_id)).
   c. (Tightening 1 transactional posture in effect throughout.)
6. Set Redis idempotency cache for batch.
7. Enqueue Celery task refinery.classify_action_domain(envelope=LeadIntakeBatch).
8. ADC routes: PRIORITIZATION → enqueue refinery.score_batch(batch_id).
9. score_batch fans out per-prospect chain:
     enrich_prospect → classify_vertical → score_fitness
   124 chains in parallel (Celery group).
10. enrich_prospect: deterministic adapters (Companies House, web scraper, LinkedIn signal).
    Each adapter has circuit breaker; failures → enrichment_status: partial.
11. classify_vertical: N=3 Flash ensemble (temps 0.1/0.5/0.9, thinking=minimal).
    Plurality vote on .vertical. 3-way split → vertical_uncertain.
12. score_fitness: deterministic Python (weights in packages/scoring/weights.py).
13. On all 124 chains complete (chord callback), refinery.assemble_queue_and_stubs:
    a. Sort prospects by fitness_score desc.
    b. Top 12 → enqueue refinery.generate_dossier_stub per prospect.
14. generate_dossier_stub (ZERO LLM calls):
    a. Look up headline KG anchor via packages.knowledge_graph.select.
    b. Compose DossierStub (company facts + verified vertical + headline anchor + slot_readiness).
    c. Begin Postgres tx:
       - Insert dossier_stubs row.
       - Insert 3 outbox envelopes (Slack canvas, CRM fields, Drive priority-index entry).
       (Tightening 1 same-tx commit.)
    d. Commit tx.
    e. Cloud Tasks schedule outbox dispatch (refinery.outbox_dispatcher per envelope).
15. WebSocket emits stage1.complete to Theater.
16. T+8s wall: ranked Slack canvas + CRM fields + Drive priority-index visible. MAGIC MOMENT 1.
```

### L.2 — Flow: Slack button click → Stage 2 → multi-surface dossier render (Magic Moment 2)

```
1. FDE clicks [Generate Full Dossier] on William Cook Sheffield in the Slack canvas.
2. Slack POST /slack/interactions to refinery_api with SlackDossierAction payload.
3. Signature verified; idempotency key computed (dossier:{prospect_id}:{signal_hash}:{kg_version}).
4. If cached: return DossierAck(status=cached).
5. Else: new dossier_id; Redis set with 7d TTL; enqueue refinery.generate_dossier.
6. ADC routes: DOSSIER_FULL.
7. generate_dossier orchestration:
    a. Mark dossier_artifacts row state=generating.
    b. Enqueue dossier_section_taxonomy first (others depend on taxonomy).
    c. On taxonomy complete, parallel:
       - dossier_section_defect (Tightening 4 DS-CP check; if empty allowed_evidence OR
         severe shift → strip; else N=3 Flash + conformal).
       - dossier_section_comparable (Stage 2.3a deterministic select; then 2.3b Pro prose).
    d. On both complete, parallel:
       - dossier_section_risk (Pro N=1, fixed risk taxonomy).
       - dossier_section_approach (Pro N=1, fixed approach templates).
    e. On all sections complete, refinery.compose_dossier:
       i.    Render each section to bytes (rendered_sections dict).
       ii.   Construct PreVisitDossier(...).
       iii.  Pydantic model_validator runs:
             - Tightening 3 byte-density recompute (overwrites caller value); reject < 0.60.
             - Tightening 4 unverified_sections retains any DS-CP-stripped section keys.
       iv.   If validation rejects → state=rejected_byte_ratio; emit dossier.rejected WS event;
             do NOT persist; do NOT write outbox.
       v.    Else inside one Postgres tx:
             - Insert dossier_artifacts row.
             - Insert 3 outbox envelopes (Slack canvas update, CRM note, Drive doc create).
             - Commit.
       vi.   Cloud Tasks schedule outbox dispatch.
       vii.  WebSocket emit stage2.complete.
8. outbox_dispatcher (per envelope, in parallel):
    a. Mark outbox row state=in_flight.
    b. Call surface adapter (slack/canvas.edit, crm/notes.create, drive/files.update).
    c. On success: state=delivered; WS emit outbox.dispatched.
    d. On failure: delivery_attempts++; retry per Cloud Tasks backoff (10s, 30s, 90s, 4m, 20m, 1h).
       After 6 attempts: move to outbox_dlq; WS emit outbox.dlq.
9. T+88s wall: Drive doc visible + CRM note visible + Slack canvas updated. MAGIC MOMENT 2.
```

### L.3 — Flow: Transactional Outbox commit + relay + retry + DLQ (Tightening 1)

```
1. Producer (compose_dossier or generate_dossier_stub) opens Postgres tx.
2. Producer INSERTs the canonical artifact row (dossier_artifacts or dossier_stubs).
3. Producer INSERTs N outbox rows (one per surface) with state=pending, delivery_attempts=0,
   next_attempt_at=now().
4. Producer COMMITs tx atomically. Artifact and outbox rows land together or not at all.
5. Producer schedules Cloud Tasks invocations per outbox row.
6. refinery.outbox_dispatcher (per row) runs:
    a. SELECT FOR UPDATE the outbox row; abort if state != pending OR next_attempt_at > now().
    b. UPDATE state=in_flight.
    c. Call surface adapter with payload.
    d. On success: UPDATE state=delivered, delivered_at=now(). COMMIT.
    e. On failure:
       i.   delivery_attempts++.
       ii.  If delivery_attempts >= 6:
            - Begin tx; INSERT outbox_dlq row with final_error; DELETE outbox row; COMMIT.
            - Emit outbox.dlq WebSocket event.
       iii. Else:
            - UPDATE next_attempt_at = now() + backoff[delivery_attempts],
              last_error=str(err), state=pending. COMMIT.
            - Cloud Tasks reschedules.
7. Backoff schedule (exponential, jittered, capped 6h total per cloudtasks.yaml):
   attempt 1: 10s, 2: 30s, 3: 90s, 4: 4m, 5: 20m, 6: 1h.
```

### L.4 — Flow: Slack distributed lock acquire + release (Tightening 2)

```
1. Slack POST /slack/events arrives at refinery_api.
2. Signature verified (HMAC v0:{ts}:{body}, 5-min window).
3. lock_acquired = redis.SET slack:lock:{event_id} 1 NX EX 60.
4. If not lock_acquired:
   - Return HTTP 202 {"status": "duplicate_in_flight", "event_id": ...}.
   - Slack does NOT retry on 202. END.
5. Check post-completion key: redis.GET slack:event:{event_id}.
   If present:
   - redis.DEL slack:lock:{event_id}  (release immediately; work was already done)
   - Return SlackEventAck(status=duplicate).
6. Enqueue Celery task with on_success=release_slack_lock_and_mark_complete,
   on_failure=release_slack_lock.
7. Return SlackEventAck(status=accepted).
8. Celery task runs (parse_slack_ingress → score_batch chain).
9. On task success:
   - redis.SET slack:event:{event_id} 1 EX 86400  (24h post-completion dedup).
   - redis.DEL slack:lock:{event_id}  (release lock).
10. On task failure:
    - redis.DEL slack:lock:{event_id}  (release lock; no post-completion key set, allowing later
      legitimate retry).
11. If lock TTL (60s) expires before callback fires (worker death or partition):
    - Lock auto-expires. A later Slack retry will acquire the lock and re-run the task.
    - Task-level idempotency (batch_id Postgres unique constraint) prevents duplicate work.
```

### L.5 — Flow: Section-granular DS-CP partial enrichment path (Tightening 4)

```
1. Stage 2.2 dossier_section_defect task starts for prospect P, vertical V.
2. Compute allowed_evidence = packages.knowledge_graph.evidence.compute_allowed_evidence(
     vertical=V, section_type="defect_hypothesis", prospect_signals=P.signals
   ).
3. If allowed_evidence == []:
   - Log: "DS-CP strip: no anchor data for {V}/{defect_hypothesis}".
   - Persist stub LikelyDefectClassHypothesis(conformal_set=[], coverage=0.0,
     calibration_version=current, requires_human_review=True, rationale="No anchor data").
   - Append "defect_hypothesis" to PreVisitDossier.unverified_sections.
   - Return without LLM call.
4. Else: compute DS-CP distance.
   distance = packages.uncertainty.dscp.semantic_distance(P.signals, centroid_for(V)).
5. If distance > DSCP_SEVERE_SHIFT_THRESHOLD:
   - Same strip behavior as step 3.
6. Else: run N=3 Flash ensemble (Stage 2.2 happy path).
7. Apply conformal calibration table → conformal_set + coverage.
8. Persist LikelyDefectClassHypothesis (model_validator on the schema flags
   requires_human_review if set is empty or all-class).
9. Same pattern applies to Stage 2.3 comparable (if allowed_evidence is empty),
   Stage 2.4 risk, Stage 2.5 approach — each section is independently stripped if its
   allowed_evidence whitelist is empty for the prospect's vertical sub-path.
10. compose_dossier proceeds with remaining verified sections; PreVisitDossier renders
    "⚠ N sections marked unverified" note via the renderer when unverified_sections is non-empty.
```

---

## §M. Demo Recording Cut List

Per `ULTIMATE_PRD.md §5.5` timing budget. Recording total: 90 seconds for the silent take + ~75 seconds voiceover overdub. OBS captures 1080p/30fps. Pane focus changes are post-production crops.

```
T+0       COLD-OPEN. Silent. Slack channel #fde-lead-refinery receives a forwarded email
          with UK_Metals_Expo_2025_leads.csv attachment + a Doug-flavored note: "UK Metals Expo
          batch — Stew can you triage?"
T+1       Theater pane (center) shows inbound Slack event JSON appearing.
T+2       Signature OK badge appears. ADC routes to PRIORITIZATION pill.
T+3       Theater: idempotency keys panel shows batch key just computed.
T+5       Stage 1 enrichment fan-out visible as 124 small per-prospect cards lighting up
          (Companies House + web scraper + LinkedIn signal).
T+6       N=3 Flash vertical-classification cards filling in across prospects (parallel
          ensemble visible).
T+7       Deterministic fitness scoring writes back per prospect.
T+8       MAGIC MOMENT 1. Three things land simultaneously:
          - Slack canvas materializes with ranked shortlist (William Cook Sheffield top).
          - CRM record inset (bottom-right) populates William Cook's refinery_fit_score,
            vertical, slot_readiness fields.
          - Drive priority-index doc tile appears in the right pane's Drive folder mock.
T+9       Cursor moves to the [Generate Full Dossier] button on William Cook in the Slack canvas.
T+11      Brief pause for emphasis — Theater pane shows the deterministic Stage 1 was rule-based
          (Damjan-readiness signal: "No LLM in routing").
T+12      Cursor clicks [Generate Full Dossier].
T+13      Theater: new ADC route badge appears (DOSSIER_FULL). New idempotency key visible.
T+14      Stage 2.1 process taxonomy card lights up (Pro N=1 thinking=medium).
T+25      Stage 2.1 complete. Process taxonomy section appears in Drive doc right pane.
T+27      Stage 2.2 defect-class card lights up. THREE Flash sample cards fill in
          (temps 0.1, 0.5, 0.9 visible).
T+38      Fourth card aggregates: conformal calibration step. Coverage statement renders.
T+40      Defect-class section in Drive doc shows conformal set + coverage statement.
T+42      Stage 2.3a comparable: Theater HIGHLIGHTS "Deterministic selection from KG
          (LLM did NOT pick this anchor)" — v4 audit surface. Brief pause for emphasis.
T+45      Stage 2.3b Pro prose generates dimension_of_comparability (≤250 chars).
T+60      Comparable Matta deployment section in Drive doc shows anchor + 250-char prose +
          clickable line citation. Citation panel expands on hover.
T+65      Stage 2.4 risk register card lights up. Cards fill in with fixed risk taxonomy.
T+75      Risk register section in Drive doc.
T+78      Stage 2.5 suggested approach card lights up.
T+85      Suggested approach section in Drive doc.
T+86      Theater: deterministic-vs-LLM byte-density coverage meter visible at >0.60 green.
          Pydantic validator passes; no rejection.
T+87      Compose_dossier writes PreVisitDossier + 3 outbox envelopes inside one Postgres tx.
T+88      MAGIC MOMENT 2. Three things land simultaneously:
          - Slack canvas updates with the full dossier section anchors.
          - CRM record inset (bottom-right) appends note: "Pre-Visit Dossier generated
            2026-05-11, link: drive.google.com/...".
          - Drive doc footer shows [Share] button live.
T+89      Cost ticker shows total Vertex AI cost: ~$0.037. Well under $0.10.
T+90      RECORDING CAP. Hard cut.
```

Voiceover overdub (separate take, ~75 seconds) starts at T+12 (the click) and runs to T+88. The verbal Phase 2 / Phase 3 tease is a third take (~15 seconds) added in post.

---

## §N. Phase 1 Success Criteria (Verification Gate)

Restated from `ULTIMATE_PRD.md §6.8` (10 Magic Moment criteria) + 5 Phase-1-specific gates from this spec.

| # | Criterion | PASS condition |
|---|---|---|
| 1 | Two Magic Moments visible | T+8 Slack canvas + CRM fields + Drive index. T+88 full dossier across all three surfaces. Total elapsed < 90s. |
| 2 | Theater pane shows ADC decision separately from any LLM call | A dedicated UI element renders the ADC route pill BEFORE any Flash/Pro card lights up. |
| 3 | Defect-class section shows N=3 ensemble votes + conformal calibration step | Three sample cards + a fourth aggregating card visible during Stage 2.2; coverage statement renders. |
| 4 | Comparable card highlights "deterministic selection from KG" | UI element visible at T+42 in the Theater pane. |
| 5 | `deterministic_section_ratio ≥ 0.60` visible | Byte-density coverage meter green at T+86. |
| 6 | Citation panel shows verbatim line numbers into `Matta_Intel_cleaned.md` | Click-to-expand citation works for every KG anchor used. |
| 7 | Dossier referenceable via permanent Drive URL | `[Share]` button copies real (mock) Drive share-link. |
| 8 | CRM record inset shows fields populated at T+8 and note at T+88 | Bottom-right inset visibly updates twice. |
| 9 | Vertex AI cost < $0.10 per dossier | Cost ticker shows ~$0.037 (within envelope per `ULTIMATE_PRD.md §3.5`). |
| 10 | `verify_knowledge_graph.py` passes at container boot | Lifespan logs "Knowledge graph provenance check passed"; readyz returns 200. |
| **11** | DLQ table is **`outbox_dlq`**, NOT `cmms_outbox_dlq` | `psql -c "\dt"` confirms `outbox_dlq` table exists; `cmms_outbox_dlq` does NOT exist. |
| **12** | Pydantic `PreVisitDossier.model_validator` Goodhart-resistance test | Unit test `tests/unit/test_byte_density_validator.py` constructs payload with `deterministic_section_ratio=0.95` and `rendered_sections` whose actual byte ratio is 0.30; assertion: `pytest.raises(ValidationError, match="byte-density gate")`. |
| **13** | Slack distributed lock test | Unit test fires two concurrent `POST /slack/events` requests with same `event_id`; first returns 200 `accepted`, second returns 202 `duplicate_in_flight`; Celery task ran exactly once. |
| **14** | Knowledge graph startup validator test | Unit test seeds `graph.json` with a citation line that does not resolve; `scripts/verify_knowledge_graph.py` returns exit code 1; container fails to boot. |
| **15** | Section-granular DS-CP test | Unit test sets `allowed_evidence=[]` for defect-section; assertion: `PreVisitDossier.unverified_sections == ["defect_hypothesis"]` and remaining sections still render. |

Additional engineering gates beyond the spec's required 15:

- 16. Cummins not in KG. `grep -i "cummins" packages/knowledge_graph/graph.json` returns 0 matches.
- 17. No `cmms_*` identifiers in code or migrations. `grep -ri "cmms" packages/ apps/ migrations/` returns 0 hits.
- 18. Model strings exact match. `grep "gemini-3-flash-preview\|gemini-3.1-pro-preview" packages/prompts/` shows the exact strings (with `3.1.` dot, not `3-1-` hyphen).
- 19. `extra="forbid"` on every schema. `grep -c "extra=\"forbid\"" packages/schemas/*.py` matches the number of BaseModel classes.
- 20. ADC is pure function. No Celery task imports `genai.Client` in `packages/adc/rules.py` or `apps/refinery_worker/tasks/classify_action_domain.py`.

---

## Appendix — Build Order (Suggested 72h Sequencing)

| Hour | Work |
|---|---|
| 0–4 | Repo scaffold; pyproject.toml + Dockerfiles + docker-compose. Pydantic schemas (§C). |
| 4–8 | Alembic migrations (outbox + outbox_dlq + all canonical tables). KG loader + validator (§G) with the 5 seed anchors. |
| 8–14 | FastAPI app skeleton + lifespan + all routers (§D), including Tightening 2 distributed lock in slack_events.py. |
| 14–20 | Celery worker skeleton + all tasks (§E) with mock surface adapters. Tightening 1 transactional outbox helper (`packages/outbox/enqueue.py`). |
| 20–28 | Prompt templates (§F), Vertex AI integration, N=3 ensemble fan-out, conformal calibration build (§H). |
| 28–36 | Mock surface servers (Slack/CRM/Drive per §I). Seed data scripts. |
| 36–44 | Theater UI three-pane + CRM inset + WebSocket (§J). |
| 44–52 | Tightening 3 byte-density validator + Tightening 4 DS-CP section-strip tests. |
| 52–60 | Integration tests (§N #11–#20). End-to-end demo dry-runs. |
| 60–68 | Demo recording per §M cut list. OBS setup. Voiceover takes. |
| 68–72 | Vidyard upload. Post-production captions. Cold-email draft pointing at 0:08 / 0:88 markers. |

---

*End of PHASE_1_SPEC.md. Architectural spec is `ULTIMATE_PRD.md` (commit `40d6b92`). Authorizing verdict is `validation_gate_1f_red_v3.md`. Build proceeds from this blueprint without further re-reading the PRD.*
