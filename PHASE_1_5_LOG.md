[STAGE1.7] PASS 2026-05-12T07:40:00Z Vertex AI authenticated and models available
[STAGE2.4] PASS 2026-05-12T07:55:00Z CSV accepted batch_id=5a00fba1-f922-4596-b5d3-a61ca9f79b73
§G #6 escalation — novel failure mode (project type incompatible with Vertex AI). Stand by.

---
## SESSION 2 — 2026-05-13 (Claude Code, post Architect resolution)

### Prep work completed
- Step 3A: Model swap already committed (23f6c1c) — gemini-3-*-preview → gemini-2.5-* verified in runtime code
- Step 3B: MATTA_RECONCILIATION.md §6 already committed (246249a) — audit trail complete
- Step 3C: git push origin master — already up-to-date; docker compose down -v — clean state confirmed

### Stack bring-up — 2026-05-13T13:33Z
- [STACK] postgres, redis, mock_slack, mock_crm, mock_drive, refinery_api, refinery_worker, theater_ui — all started
- [API] Application startup complete — HTTP 200 on /health
- [WORKER] celery@bc86298d948a ready, connected to redis://redis:6379/0, subscribed to `celery` queue

### Pre-ingest fixes applied at runtime
- [FIX-RUNTIME-1] §D.4 curl command missing `-F "source_label=..."` form field — added `source_label=uk_metals_expo_2025`
- [FIX-RUNTIME-2] `run_demo.sh` does not call `init_db.py` — ran `docker compose exec refinery_api python scripts/init_db.py` manually; tables created

### Milestone observation — batch_id=67012210-6476-4fa5-aa73-529c9c751998
- [MILESTONE M0] nominal=T+0 obs=T+0 drift=0s PASS — batch_id returned, row_count=124
- [MILESTONE M1] nominal=T+2 obs=T+2 drift=0s PASS — score_batch received and succeeded; classify_vertical tasks dispatched
- [MILESTONE M2] nominal=T+5 obs=T+6 drift=+1s PASS — 124 rows in lead_prospects confirmed via psql
- [MILESTONE M3] nominal=T+8 FAIL — pipeline stalled; classify_vertical tasks looping with DefaultCredentialsError; no scores, no stubs, Magic Moment 1 unreachable

## INVESTIGATION REPORT — 2026-05-13T13:46Z

### Stack state
- postgres: running, tables initialised, 124 lead_prospects rows for batch
- redis: running, broker healthy
- refinery_worker: running, Celery ready — but all classify_vertical tasks in infinite retry loop
- refinery_api: running, HTTP 200 — no traceback in lifespan logs
- mock_slack/crm/drive: running (Docker healthcheck shows `curl: not found` but processes serving)
- Postgres MCP: connection timed out (network error); fallback to `docker compose exec postgres psql`

### First divergence
- **Milestone:** M3 (Magic Moment 1, T+8)
- **Observed:** classify_vertical tasks retrying indefinitely — `DefaultCredentialsError: Your default credentials were not found`
- **Expected per §8.5:** top-12 scored, Slack canvas + CRM fields + Drive priority-index at T+8

### Three ranked hypotheses

#### H1 (most likely) — ADC volume mount resolves to empty directory
- **Root cause:** `docker-compose.yml` mounts `${HOME}/.config/gcloud` which on this Windows/Git-Bash host resolves to `C:\Users\hp\.config\gcloud` (a directory that exists but is empty). The actual ADC credentials are at `C:\Users\hp\AppData\Roaming\gcloud\application_default_credentials.json` (confirmed — file exists, 411 bytes, dated 2026-05-12).
- **Diagnostic test (already executed):** `docker exec matta_demo-refinery_worker-1 sh -c "ls -la /root/.config/gcloud/"` → directory empty; `ls /c/Users/hp/AppData/Roaming/gcloud/application_default_credentials.json` → file confirmed.
- **Files to read:** `docker-compose.yml` volumes section (already read)
- **Fix:** Change both `refinery_api` and `refinery_worker` volume mounts from `${HOME}/.config/gcloud` to `${APPDATA}/gcloud` in `docker-compose.yml`. No architectural invariant touched — Vertex ADC auth pattern preserved, only the host path corrected.
- **Maps to §F:** None exactly — this is an environmental path issue, closest to §G #6 (novel failure mode, environmental). NOT §G #4 (no invariant touched by the fix).

#### H2 — `source_label` missing from run_demo.sh / §D.4 command
- **Root cause:** The ingest endpoint requires a `source_label` Form field. The §D.4 canonical curl command omits it, causing 422 on every run. Confirmed this session.
- **Diagnostic test (already executed):** raw curl → `{"detail":[{"type":"missing","loc":["body","source_label"],"msg":"Field required"}]}`.
- **Files to read:** `apps/refinery_api/routers/ingest.py` (read via Nia — confirmed `source_label: Annotated[str, Form(...)]`)
- **Fix:** Add `-F "source_label=uk_metals_expo_2025"` to the ingest curl in `scripts/run_demo.sh`. Also update §D.4 command in PHASE_1_5_DEBUG_SPEC.md.
- **Maps to §F #2:** yes (422 field required), but root cause is missing form field in run script not CSV schema drift.

#### H3 — `init_db.py` not called from `run_demo.sh`
- **Root cause:** `run_demo.sh` runs `seed_mock_data.py`, `build_calibration_table.py`, `verify_knowledge_graph.py` — but NOT `init_db.py`. DB tables don't exist at first ingest attempt after `docker compose down -v`. Causes 500 "Database transaction failed".
- **Diagnostic test (already executed):** ingest with source_label → `{"detail":"Database transaction failed"}` until `init_db.py` run.
- **Files to read:** `scripts/run_demo.sh`, `scripts/init_db.py` (both read via filesystem MCP)
- **Fix:** Add `python scripts/init_db.py` call to `scripts/run_demo.sh` (before the ingest step, after seed_mock_data).
- **Maps to §F:** None exactly — §F.9 (calibration table) is analogous pattern; this is same class of missing-setup-step.

### Summary
H1 is the blocking failure — classify_vertical will never succeed until ADC credentials are accessible inside the worker/api containers. H2 and H3 are also blocking in practice (prevent M0 from passing on a fresh `docker compose down -v` run) and need fixing before §H verification can run cleanly. All three fixes are environmental scaffolding corrections, not architectural changes.

### Awaiting approval to proceed with H1+H2+H3 fix path (recommended: all three in one pass).

---
## SESSION 2 — FIX EXECUTION (post Architect approval)

### Fixes applied
- [FIX-H1] docker-compose.yml: `${HOME}/.config/gcloud` → `/home/hp/.config/gcloud` (hardcoded Linux path; compose run via WSL Ubuntu)
- [FIX-H2] scripts/phase_1_5_run.sh created with `-F "source_label=uk_metals_expo_2025"` in ingest curl
- [FIX-H3] scripts/phase_1_5_run.sh calls `docker compose exec -T refinery_api python scripts/init_db.py` before ingest
- [FIX] infra/Dockerfile.api + Dockerfile.worker: `mkdir -p apps packages scripts migrations` before pip install (setuptools stub dirs)
- [FIX] apps/refinery_worker/tasks/generate_dossier_stub.py: `payload` → `payload_jsonb` in outbox INSERT
- [FIX] apps/refinery_worker/tasks/compose_dossier.py: `payload` → `payload_jsonb` in outbox INSERT
- [FIX] apps/refinery_worker/tasks/outbox_dispatcher.py: `payload` → `payload_jsonb` in outbox SELECT and outbox_dlq INSERT

### Run 3 milestone observation — batch_id=095f57f1-2e31-4d08-8e32-9cc4a24c5a56
- [MILESTONE M0] PASS — batch_id returned, row_count=124
- [MILESTONE M1] PASS — score_batch received and succeeded; classify_vertical tasks dispatched; Vertex gemini-2.5-flash HTTP 200 confirmed
- [MILESTONE M2] PASS — 124 rows in lead_prospects
- [MILESTONE M3] PASS (functional) — 12 dossier_stubs generated; 36 outbox rows all state=delivered; mock surfaces stateless stubs (no list endpoints; §D.5 curl probes return 404 — expected, not a failure)
- [MILESTONE M4] PASS — click trigger HTTP 200; generate_dossier received; dossier_section_taxonomy dispatched
- [MILESTONE M5-M9] IN PROGRESS — Stage 2 section chain running
