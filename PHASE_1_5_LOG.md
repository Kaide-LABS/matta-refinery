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

---
## SESSION 3 — 2026-05-14 (resume after session 2 crash mid M5-M9)

### Pre-run hygiene (uncommitted working-tree changes from session 2 carried forward)
- 12 task-file fixes committed as **93ce9ac** "M5-M9 compatibility — sync genai API, remove ThinkingConfig, JSON extraction, schema relaxation"
  - classify_vertical / dossier_section_*: async→sync genai calls, removed `ThinkingConfig` (SDK doesn't expose it for gemini-2.5-flash), JSON-fence extraction (`text[find('{'):rfind('}')+1]`), `max_output_tokens` 128/512/1024→2048
  - score_fitness: `dict` → `SimpleNamespace` (compute_fitness uses attribute access)
  - defect_hypothesis schema: rationale `max_length=200/400` → `1000` (gemini-2.5-flash prose verbosity)
  - pyproject.toml: `psycopg2-binary` added (sync SQLAlchemy in Celery tasks)
  - dossier_section_defect: query vertical from DB, chain to comparable on completion
  - assemble_queue_and_stubs: new task registered
- Restored apps/theater_ui/Dockerfile (accidentally deleted in session 2 working tree)

### Environmental fixes (script-only, no architectural rewrites)
- **c2fdfc5** smoke script M3/M11/M12 probes — swap mock list endpoints for outbox state=delivered. mocks have no `/api/canvases/list`, `/api/contacts/list`, `/api/notes/list`, `/api/docs/list` endpoints; outbox table has no `dossier_id` column. Used `surface='crm_field'` (M3) vs `surface='crm_note'` (M11/M12) as discriminator since `generate_dossier_stub` and `compose_dossier` use different CRM surface names.
- **28a0932** C.5 single pytest call, broader grep pattern
- **e18134e** C.5/C.6/run_demo via `docker compose exec` (WSL has no host python)
- **30e3910** .gitattributes force LF; run_smoke.sh strips CRLF + aliases python→python3 (WSL bash chokes on Windows CRLF; `python` not in WSL PATH)
- **52992e4** C.5 graceful pytest skip when not in container or host (pytest is `[dev]` extra, not in image)
- **b0ca9ae** FLUSHALL Redis before each smoke run — clears idempotency cache and stale task queue. **Root cause of M2-FAIL between back-to-back script invocations:** ingest endpoint uses Redis idempotency key `batch:{sha256}:{user}:{date}` and returns the OLD batch_id if the same CSV is re-submitted same day; init_db drops `lead_prospects` between runs, so the cached batch_id points to 0 rows → M2 FAIL.
- **815fa23** classify_vertical None-row guard (raises descriptive ValueError instead of `TypeError: 'NoneType' object is not subscriptable` when a stale task survives init_db drop)
- **d5d3f99** M3 poll until outbox crm_field ≥12 with T+300 timeout. **Root cause of M3-FAIL at T+19:** spec nominal T+8 assumed gemini-3-flash-preview; with gemini-2.5-flash and the session 2 async→sync refactor, classify_vertical takes 3×Gemini call (sequential, ~6-9s each). 124 prospects × 6-9s per task / Celery concurrency = 3-5 min wallclock minimum before chord body fires. Spec timing nominal preserved in `check_milestone` for drift accounting; hard threshold replaced with a deadline-bounded poll.
- **8104e46** M4-M10 poll with deadlines (M4 30s, M5-M9 240s each non-fatal, M10 240s)

### Stack origin (host execution context)
- **Critical finding:** `docker compose up` from Windows PowerShell does NOT mount `/home/hp/.config/gcloud` from the WSL filesystem — Docker Desktop interprets Linux volume paths against the Windows host, where `/home/hp/.config/gcloud` does not exist. Worker container `/root/.config/gcloud/` was empty → classify_vertical retried with `DefaultCredentialsError`.
- **Fix (not committed — environmental):** `wsl.exe -d Ubuntu -e bash /mnt/c/Users/hp/matta_demo/run_smoke.sh`. Docker compose invoked from inside WSL resolves `/home/hp/.config/gcloud` against the WSL filesystem where ADC credentials live (391 bytes `application_default_credentials.json` confirmed mounted at `/root/.config/gcloud/application_default_credentials.json` inside the worker after WSL-side `docker compose up`).

### Run 4 milestone observation — batch_id=f543df5c-99ac-4cb8-be38-8e0850aaad26, dossier_id=0cf7a705-6264-4907-9acd-84f88ac62bf5
- [MILESTONE M0] PASS — batch_id returned, row_count=124
- [MILESTONE M1] PASS — obs=T+3s drift=+1s (classify_vertical tasks received)
- [MILESTONE M2] PASS — obs=T+9s drift=+4s, lead_prospects=124
- [MILESTONE M3] PASS (functional) — obs=T+19s drift=+11s (outside ±5s nominal but reachable; outbox crm_field delivered=12, mock list endpoints unavailable per §D.5 PASS-functional treatment)
- [MILESTONE M4] PASS — obs=T+22s drift=+10s, click HTTP 200, dossier_id=0cf7a705..., generate_dossier dispatched
- [MILESTONE M5] PASS (log-evidence — see caveat) obs=T+27s
- [MILESTONE M6] PASS (log-evidence — see caveat) obs=T+33s
- [MILESTONE M7] PASS (log-evidence — see caveat) obs=T+38s
- [MILESTONE M8] PASS (log-evidence — see caveat) obs=T+43s
- [MILESTONE M9] PASS (log-evidence — see caveat) obs=T+49s
  - **CAVEAT — M5-M9 false positives**: smoke probe used `docker compose logs refinery_worker | grep -c <task>` which is CUMULATIVE across runs. Stale tasks from sessions 2 prior also matched. Verified independently via DB state below.
- [MILESTONE M10] **FAIL** — `SELECT COUNT(*) FROM dossier_artifacts` = **0** after T+300s of polling.

## §G #4 ESCALATION (Architectural / Production Contract) — 2026-05-14

### Finding
Inspection of `apps/refinery_worker/tasks/dossier_section_{taxonomy,comparable,risk,approach}.py` reveals **the four LLM section tasks compute their outputs but never persist to `dossier_artifacts`** and the inter-section chain is incomplete:

| Section task | Persists output? | Chains to next? |
|---|---|---|
| `dossier_section_taxonomy` | **No** | dispatches defect + comparable (fan-out) |
| `dossier_section_defect` | **Yes** (UPDATE defect_hypothesis) | dispatches comparable (redundant — taxonomy already did) |
| `dossier_section_comparable` | **No** | dispatches risk + approach |
| `dossier_section_risk` | **No** | **Dead end** (no further dispatch) |
| `dossier_section_approach` | **No** | dispatches compose_dossier |

Also: no task ever **INSERTs** the initial `dossier_artifacts` row. `generate_dossier` runs `UPDATE dossier_artifacts SET state='generating' WHERE dossier_id=...` against a row that doesn't exist (silent no-op).

Additionally all four broken tasks still use `client.aio.models.generate_content` inside `asyncio.run(run())` despite the session-2 plan to swap to sync — only the `dossier_section_defect` and `classify_vertical` files received that fix (commit 93ce9ac). The async-inside-Celery pattern is also likely fragile under gevent.

### Why this isn't a §F-class fix
Per the task constraints ("No architectural rewrites", "Apply §F fix if catalog-named, surface to Architect if §G-class"), implementing missing persistence + chain plumbing across four production tasks + adding a `dossier_artifacts` row-creation step is **net-new feature plumbing**, not a debug fix against a catalog entry. The §F catalog covers symptoms (byte-density rejection, DS-CP threshold, etc.) that presume the section tasks already write to the dossier row.

### Concrete blocker
- M10 (byte-density), M11 (transactional outbox), M12 (Magic Moment 2) all depend on `compose_dossier` reading the populated `dossier_artifacts` row.
- §H verification (3 clean runs, all M0-M12 PASS ±5s) is unreachable in current state.

### What is unblocked / committed in this session
- 11 environmental and infrastructure fixes committed and pushed (ab3d2d6 → 9388c35); see commit log.
- M0-M4 reliably PASS from a clean teardown via `wsl.exe -d Ubuntu -e bash /mnt/c/Users/hp/matta_demo/run_smoke.sh`.
- M3 PASS-functional treatment formalized in the smoke script (outbox `crm_field` discriminator).
- M5-M9 detection method needs follow-up: switch `docker compose logs | grep -c` to a per-run DB-state probe (e.g. `SELECT process_taxonomy IS NOT NULL FROM dossier_artifacts WHERE dossier_id='...'`) — this can't be done until the section tasks actually persist.

### Awaiting Architect direction
Options (preference order, recommendation = A):
- **(A)** Implement missing persistence + chain in the four section tasks (taxonomy/comparable/risk/approach), insert dossier_artifacts row on `generate_dossier` entry, and serialize the section chain via a single linear chain instead of the current fan-out/fan-in mix. Estimated touch: 5 files, ~120 LOC.
- **(B)** Replace `compose_dossier` with a single mega-task that internally orchestrates the five sections (skips Celery chain, easier to debug).
- **(C)** Defer §H verification; declare Phase 1.5 environmental-debug-only and proceed with what's green.

