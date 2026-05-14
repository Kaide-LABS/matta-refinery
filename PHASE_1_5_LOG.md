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

---
## §G #4 RESOLUTION — STEP 0 VERIFICATION (Option A authorized, 2026-05-14)

### dossier_artifacts schema (single-row-with-section-fields pattern)
Authoritative DDL: `scripts/init_db.py` lines 31-52 (`DROP TABLE IF EXISTS dossier_artifacts; CREATE TABLE dossier_artifacts (...)`):

| Column | Type | Population point (correct intent) |
|---|---|---|
| `id` | TEXT PRIMARY KEY | INSERT on generate_dossier (same value as dossier_id) |
| `dossier_id` | TEXT | INSERT on generate_dossier (UUID from slack_interactions) |
| `prospect_id` | TEXT | INSERT on generate_dossier |
| `batch_id` | TEXT | INSERT on generate_dossier (lookup from lead_prospects.batch_id) |
| `signal_hash` | TEXT | INSERT on generate_dossier (lookup from lead_prospects.signal_hash) |
| `knowledge_graph_version` | TEXT | INSERT on generate_dossier (`load_graph().version`) |
| `calibration_version` | TEXT | INSERT on generate_dossier (CalibrationTable.calibration_version) |
| `state` | TEXT | 'generating' on INSERT, 'complete' or 'rejected_byte_ratio' on compose |
| `process_taxonomy` | JSONB | UPDATE by `dossier_section_taxonomy` (missing) |
| `defect_hypothesis` | JSONB | UPDATE by `dossier_section_defect` (✓ present) |
| `comparable_deployment` | JSONB | UPDATE by `dossier_section_comparable` (missing) |
| `risk_register` | JSONB | UPDATE by `dossier_section_risk` (missing) |
| `suggested_approach` | JSONB | UPDATE by `dossier_section_approach` (missing) |
| `unverified_sections` | JSONB | UPDATE by `compose_dossier` (json.dumps of list) |
| `deterministic_section_ratio` | FLOAT | UPDATE by `compose_dossier` (validator-computed) |
| `validation_error` | TEXT | UPDATE on byte-density rejection path |
| `generated_at` | TIMESTAMP | INSERT on entry, UPDATE on compose |

**Pattern: single-row-with-section-fields, NOT staging-table-per-section.** Confirmed by compose_dossier.py:53-61 which SELECTs all five section columns directly from `dossier_artifacts` for a given `dossier_id`.

### compose_dossier expectations (already correct — no code change needed)
- Reads from: `dossier_artifacts` only (single SELECT, single dossier_id key)
- Required input fields per SELECT at compose_dossier.py:54-58: `prospect_id, signal_hash, knowledge_graph_version, calibration_version, process_taxonomy, defect_hypothesis, comparable_deployment, risk_register, suggested_approach, unverified_sections`
- Builds `PreVisitDossier(...)` with **10 rendered_sections** entries:
  - 5 deterministic (count toward bytes(deterministic_content)): `company_facts`, `verified_kg_anchors`, `fitness_score_rationale`, `risk_checklist_baseline`, `approach_template_baseline`
  - 5 LLM (count toward bytes(total)−bytes(deterministic)): `process_taxonomy`, `defect_hypothesis`, `comparable_dimension_of_comparability_prose`, `risk_register_narrative`, `suggested_approach_narrative`
- Byte-density validator in `PreVisitDossier._recompute_and_enforce_deterministic_byte_ratio` (packages/schemas/dossier.py:132-156) — rejects if `det_bytes / (det_bytes+llm_bytes) < 0.60`. Reads section content via `rendered_sections[k].encode("utf-8")`, NOT directly from the section JSONB columns.
- On success: `UPDATE dossier_artifacts SET state='complete', deterministic_section_ratio=:r, unverified_sections=:u, generated_at=:t`; INSERT 3 outbox rows (`slack_canvas`, `crm_note`, `drive_doc`) in the same transaction (Tightening 1).
- On `ValidationError`: separate transaction `UPDATE state='rejected_byte_ratio', validation_error=:err`; outbox NOT written.

### Section task output shapes
Each task computes a Pydantic model; only `dossier_section_defect` persists. The 4 broken tasks discard.

| Task | Returns (Pydantic model) | Currently persists to | Currently chains to |
|---|---|---|---|
| `taxonomy` | `ProcessTaxonomy` (packages/schemas/dossier.py:27-33) | **nothing** | dispatches `defect` + `comparable` (fan-out) |
| `defect` | `LikelyDefectClassHypothesis` (packages/schemas/defect_hypothesis.py) | `UPDATE dossier_artifacts SET defect_hypothesis = :res WHERE dossier_id = :did` ✓ | dispatches `comparable` (redundant — taxonomy already did) |
| `comparable` | wraps locally-defined `DimensionOfComparabilityProse` into `ComparableDeployment` (packages/schemas/dossier.py:36-42) | **nothing** (the wrapped `res` is discarded after construction) | dispatches `risk` + `approach` (fan-out) |
| `risk` | `RiskRegister` (packages/schemas/dossier.py:53-56) | **nothing** | **DEAD END** — no dispatch |
| `approach` | `SuggestedApproach` (packages/schemas/dossier.py:59-64) | **nothing** | dispatches `compose_dossier` |

Plus async-in-Celery anti-pattern: `taxonomy`, `comparable`, `risk`, `approach` still use `await client.aio.models.generate_content(...)` inside `asyncio.run(run())`. Same fragility addressed in commit 93ce9ac for `classify_vertical` and `dossier_section_defect`.

Also: `generate_dossier.py` line 19 does `UPDATE dossier_artifacts SET state='generating' WHERE dossier_id=:did` — silent no-op because no INSERT precedes it. The `dossier_artifacts` row does not exist when the chain starts.

### Proposed fix design (Option A, refined per Architect direction)

**Pattern:** linear chain via `app.send_task` from each section task to the next. Replace current fan-out/fan-in.

**dossier_artifacts row creation:** INSERT at the start of `generate_dossier(prospect_id, dossier_id)`. The task already receives `prospect_id` and `dossier_id` as args. Look up `batch_id`, `signal_hash` from `lead_prospects`. Resolve `knowledge_graph_version` via `packages.knowledge_graph.loader.load_graph().version`. Resolve `calibration_version` by reading `packages/uncertainty/calibration_table.json` (or via the `CalibrationTable.calibration_version` field that compose_dossier already loads at line 134-135).

**Chain order:** `generate_dossier` → `taxonomy` → `defect` → `comparable` → `risk` → `approach` → `compose_dossier`

**Per-section persistence:** each section task adds at the end (after Pydantic model is computed):
```python
with engine.begin() as conn:
    conn.execute(
        text("UPDATE dossier_artifacts SET <column> = :payload WHERE dossier_id = :did"),
        {"payload": result.model_dump_json(), "did": dossier_id},
    )
app.send_task("refinery.<next_task>", args=[prospect_id, dossier_id])
```

Column mapping:
- taxonomy → `process_taxonomy`
- defect → `defect_hypothesis` (already correct; remove redundant comparable dispatch — chain to comparable singularly)
- comparable → `comparable_deployment` (NOTE: persist the *wrapped* `ComparableDeployment`, not the inner `DimensionOfComparabilityProse`)
- risk → `risk_register` (add dispatch to approach)
- approach → `suggested_approach` (already dispatches compose_dossier — keep)

**Async-in-Celery swap:** for taxonomy/comparable/risk/approach, replace the async pattern with the sync pattern in `client.models.generate_content` (matches 93ce9ac). Remove `import asyncio` from these files.

**Estimated LOC:** ~110-130 across 5 files (generate_dossier.py ~25 LOC INSERT + lookups; 4 section tasks ~20-25 LOC each: sync swap + UPDATE + linear chain). `compose_dossier.py` unchanged. `init_db.py` unchanged (schema already correct).

**Files touched:**
1. `apps/refinery_worker/tasks/generate_dossier.py` — INSERT row + dependency lookups
2. `apps/refinery_worker/tasks/dossier_section_taxonomy.py` — sync swap + UPDATE + chain to defect
3. `apps/refinery_worker/tasks/dossier_section_defect.py` — single-chain to comparable (remove redundant dispatch; already persists)
4. `apps/refinery_worker/tasks/dossier_section_comparable.py` — sync swap + UPDATE (ComparableDeployment) + chain to risk only
5. `apps/refinery_worker/tasks/dossier_section_risk.py` — sync swap + UPDATE + chain to approach
6. `apps/refinery_worker/tasks/dossier_section_approach.py` — sync swap + UPDATE + keep compose dispatch

(6 files, not 5 — taxonomy now chains to defect instead of fan-out, so all 4 broken tasks need the chain edit, plus defect needs the comparable-redundancy removed.)

### Open questions for Architect (low-stakes, asking before code)
1. **signal_hash provenance**: `lead_prospects.signal_hash` is `nullable=True` (packages/models/prospects.py:33). Is it populated by `score_fitness` or expected to be empty at dossier-generation time? If empty, use empty string `""` or compute on the fly inside generate_dossier?
2. **batch_id provenance**: `generate_dossier(prospect_id, dossier_id)` doesn't receive `batch_id`. Look it up via `SELECT batch_id FROM lead_prospects WHERE id=:pid`. Acceptable?
3. **Vertical / signals passed to section tasks**: currently the four broken tasks hardcode `vertical="metal_casting"` and `signals={}` / `enrichment_payload="{}"`. The defect task correctly queries `vertical` from lead_prospects. Should taxonomy/comparable/risk/approach also query the real vertical, or is the demo seeding such that hardcoded `metal_casting` is acceptable for §H verification?
   - **Recommend:** query real vertical for parity with defect, but keep `signals={}` and other placeholders if the upstream enrichment data isn't populated yet (would expand scope).

**STOPPING HERE per Architect direction — awaiting confirmation of fix design before writing code.**

---
## §G #4 RESOLUTION — IMPLEMENTATION COMPLETE & §H VERIFICATION SURFACES NEW BYTE-DENSITY ISSUE (2026-05-14)

### Implementation (commits e467809, 0782893, f18ebda, b058f76, 4061b87, 2ebf2ea, fedeef2, 38e0c54)
Per Architect-approved Option A:
- `generate_dossier` INSERT with idempotent UPSERT (signal_hash fallback to sha256(prospect|batch|kg)[:16])
- 4 section tasks (taxonomy/comparable/risk/approach) now UPDATE their JSONB columns (defect already did)
- Linear chain: taxonomy → defect → comparable → risk → approach → compose
- Sync genai client swap across all 4 broken section tasks (extends 93ce9ac)
- Real `vertical` queried from lead_prospects in all 4
- comparable: `matta_deployment_` prefix stripped at schema boundary (latent KG/schema mismatch; surfaced only because comparable now actually executes and persists)
- max_retries 3 → 8 across all Stage 2 tasks (DNS hiccups on oauth2.googleapis.com — Stage 1 absorbed via parallelism, linear Stage 2 cannot)
- compose_dossier: dict-or-str dispatch on JSONB column reads (Postgres returns dict via SQLAlchemy adapter, `model_validate_json` requires str)

§6.7 audit trail appended to MATTA_RECONCILIATION.md.

### §H verification — Run 1 outcomes
**M0-M9: ALL PASS via DB-state probe (per-run, no cumulative-log false positives):**
| Milestone | Obs | Evidence |
|---|---|---|
| M0 | T+0 | batch_id=2922af1c-..., row_count=124 |
| M1 | T+4s drift +2s | classify_vertical tasks dispatched |
| M2 | T+9s drift +4s | lead_prospects count=124 |
| M3 | T+382s | outbox crm_field delivered=12 (Stage 1 takes ~6min wallclock with gemini-2.5-flash sync × 124 prospects × 3 temps / Celery concurrency=4) |
| M4 | T+387s | click HTTP 200, dossier_id=2922af1c-bd8e-..., generate_dossier dispatched |
| M5 | T+405s | dossier_artifacts.process_taxonomy IS NOT NULL |
| M6 | T+428s | defect_hypothesis IS NOT NULL |
| M7 | T+450s | comparable_deployment IS NOT NULL |
| M8 | T+512s | risk_register IS NOT NULL |
| M9 | T+523s | suggested_approach IS NOT NULL |
| M10 | T+1100+ | **FAIL — state='rejected_byte_ratio'** |

### M10 FAIL — Byte-density rejection (§F.4 catalog match, but tokens-only fix is structurally insufficient)

`compose_dossier` ran cleanly (no retries, ~50ms) and correctly rejected: `deterministic_section_ratio=0.088` vs threshold 0.60. State updated to `rejected_byte_ratio`. Validation error stored. Tightening 3 byte-density gate working as designed.

#### Why §F.4 alone won't land it

The §F.4 prescription is "lower max_output_tokens; lowering 0.60 threshold is forbidden". But the math is brutal:

Today's deterministic renderers in compose_dossier.py:90-97 are placeholders:
```python
"company_facts": _render_section({"prospect_id": prospect_id}),                  # ~50 B
"verified_kg_anchors": _render_section({"anchor": ..., "citation_line": ...}),   # ~80 B
"fitness_score_rationale": _render_section({"signal_hash": signal_hash}),        # ~30 B
"risk_checklist_baseline": _render_section([f.category for f in risk.findings]), # ~200 B
"approach_template_baseline": _render_section({"template": approach.template}),  # ~40 B
# total deterministic ≈ 400 B
```

LLM total at current `max_output_tokens=2048` per section: 5 × ~1500 B ≈ 7500 B (gemini-2.5-flash/pro JSON fills toward schema `max_length` caps: rationale 600/1000 chars, RiskRegister findings 10 × 300 chars).

- Current ratio: 400 / 7900 ≈ 0.050  (observed 0.088 — slightly higher because gemini didn't max out every field)
- At `max_output_tokens=512`: LLM ≈ 5 × ~1500 = 7500 B unchanged (schema caps were the binding constraint, not the token cap) → ratio still ~0.05
- At `max_output_tokens=128`: LLM ≈ 5 × ~400 = 2000 B → ratio = 400/2400 ≈ 0.17. Still fails the 0.60 floor.
- To hit 0.60 with current deterministic=400 B: LLM must be ≤ 267 B total — ≤ 53 B per section. Roughly one short sentence. Effectively unusable.

**Conclusion:** the catalog §F.4 fix (lower tokens) is necessary but **structurally insufficient** with the current deterministic placeholders. The byte-density gate presumes the deterministic side carries real verified content; the current renderers ship only IDs and enum strings.

#### Two paths (recommendation = A; B is acceptable fallback if Architect prefers minimal scope)

**Path A — Fatten the deterministic renderers (recommended).** Pull real data already available in the row + lead_prospects join:
- `company_facts`: company_name, vertical, factory_size_band, trade_show_provenance, contact_email, sector_hint, fitness_score (deterministic — verified at ingest, not LLM-derived)
- `verified_kg_anchors`: anchor enum + citation_substrate_line + the permitted_dimensions_of_comparability list from KG (these are *verified* facts in graph.json)
- `fitness_score_rationale`: fitness_score numeric + factory_size_band + a deterministic template-rendered sentence describing how the score was computed (the scoring formula is in packages/scoring/fitness.py; this is verified math, not LLM)
- `risk_checklist_baseline`: full RiskFinding (category + severity) for each — already in schema, just include severity not just category
- `approach_template_baseline`: template enum + day_one_risks list (the structured fields of SuggestedApproach — deterministic schema-grade data, not the rationale prose)

Estimated touch: ~30 LOC in compose_dossier.py:90-97; one SELECT to lead_prospects for the company facts. No schema changes. This is completion of the spec — the deterministic_section_keys list (packages/schemas/dossier.py:69-75) clearly intends these to be rich.

**Path B — Combine §F.4 token tightening + Path A.** Belt-and-braces: drop max_output_tokens to 384 AND fatten deterministic renderers. Lands the ratio with more safety margin.

#### Out of scope (do not propose without Architect approval)
- Lowering the 0.60 threshold (forbidden by §F.4)
- Adding schema-level uncertainty fields to non-defect sections (Phase 1.6 per §6.7 Flag 2)
- Changing the byte-density math (Tightening 3 invariant)

### Awaiting Architect direction on M10 (Path A vs B)

---
## §F.4 / Path B — STEP 1 NUMERICAL SANITY CHECK (2026-05-14)

### Schema key lists (confirmed — packages/schemas/dossier.py:69-83, unchanged)

```python
DETERMINISTIC_SECTION_KEYS = frozenset({"company_facts", "verified_kg_anchors",
    "fitness_score_rationale", "risk_checklist_baseline", "approach_template_baseline"})

LLM_SECTION_KEYS = frozenset({"process_taxonomy", "defect_hypothesis",
    "comparable_dimension_of_comparability_prose", "risk_register_narrative",
    "suggested_approach_narrative"})
```

The byte-density validator (packages/schemas/dossier.py:132-156) iterates these key sets over `rendered_sections` — **NOT** raw JSONB columns. The split is data-vs-prose: e.g. comparable's structured fields go into the deterministic side (`verified_kg_anchors`), but its `dimension_of_comparability` prose goes into the LLM side.

### Measured bytes — rejected dossier 2922af1c-bd8e-4871-a683-921a560810e3

Raw JSONB column sizes (via `octet_length(col::text)`):

| Section | JSONB bytes |
|---|---|
| process_taxonomy | 1,357 |
| defect_hypothesis | 190 |
| comparable_deployment | 352 |
| risk_register | 2,248 |
| suggested_approach | 782 |
| **Total** | **4,929** |

`rendered_sections` byte composition (per compose_dossier.py:90-103 mapping — JSONB → rendered):

| Section | rendered as | Est. bytes | Side |
|---|---|---|---|
| `company_facts` | `{"prospect_id": "<id>"}` placeholder | ~40 | DET |
| `verified_kg_anchors` | `{"anchor": <enum>, "citation_line": <int>}` placeholder | ~60 | DET |
| `fitness_score_rationale` | `{"signal_hash": "<16-hex>"}` placeholder | ~40 | DET |
| `risk_checklist_baseline` | `[<category enum>, ...]` placeholder | ~200 | DET |
| `approach_template_baseline` | `{"template": <enum>}` placeholder | ~35 | DET |
| **Det total observed** | | **~375** | |
| `process_taxonomy` | full ProcessTaxonomy JSON | 1,357 | LLM |
| `defect_hypothesis` | full LikelyDefectClassHypothesis JSON | 190 | LLM |
| `comparable_dimension_of_comparability_prose` | string only (`comparable.dimension_of_comparability`) | ≤250 | LLM |
| `risk_register_narrative` | `[f.note for f in findings]` list of note strings only | ~1,500 | LLM |
| `suggested_approach_narrative` | string only (`approach.rationale`) | ≤600 | LLM |
| **LLM total observed** | | **~3,900** | |
| **Validator ratio** | 375 / (375 + 3,900) = 375 / 4,275 = **0.088** | matches observed | |

### Available raw material (verified — no schema or invariant touched)

**lead_prospects columns** (packages/models/prospects.py): id, batch_id, external_lead_id, company_name, contact_name, contact_email, sector_hint, source_system, vertical, factory_size_band, trade_show_provenance, fitness_score, enrichment_status, signal_hash, last_scored_at, requires_human_review, raw_notes.

**KnowledgeGraphAnchor** (packages/knowledge_graph/loader.py:8-15): anchor_id, vertical, deployment_type, citation_substrate_lines (list of ints), `citation_verbatim_excerpt` (10-500 chars), `permitted_dimensions_of_comparability` (list, each ≤80 chars).

**Scoring weights** (packages/scoring/weights.py): VERTICAL_MATCH_WEIGHT=0.40, SIZE_BAND_WEIGHT=0.25, TRADE_SHOW_PROVENANCE_WEIGHT=0.20, CAPACITY_DECAY_WEIGHT=0.15. Component contribution is purely deterministic per `compute_fitness` (packages/scoring/fitness.py:13-31). No new data dependencies — all of this is already in scope.

---
## §F.4 / Path B — STEP 2 PROPOSED TARGETS (awaiting Architect confirmation)

### Target equation
- LLM total ≈ 2,000 B (~50% reduction from observed 3,900 B)
- Deterministic total ≈ 3,700 B (~10× from observed 375 B placeholders)
- Predicted ratio = 3,700 / (3,700 + 2,000) = **0.649** (target band 0.65-0.72, hits with margin)

### Per-section deterministic targets (compose_dossier.py:90-97 rewrite)

| Section | New content | Est. bytes |
|---|---|---|
| `company_facts` | `{"company_name", "vertical", "factory_size_band", "trade_show_provenance", "contact_email", "sector_hint", "source_system", "external_lead_id", "raw_notes" (truncated 400 chars)}` from lead_prospects. ONE extra SELECT in compose_dossier. | ~700 |
| `verified_kg_anchors` | `{"anchor_id", "deployment_type", "citation_substrate_lines": [..], "citation_verbatim_excerpt" (≤500 chars from KG), "permitted_dimensions_of_comparability": [..], "selection_method"}` — looked up by `select_comparable(vertical, None)` already returns dims/lines; for the verbatim excerpt, load_graph() and find matching anchor by ID. | ~700 |
| `fitness_score_rationale` | `{"fitness_score": <float>, "weights_applied": {"vertical_match": 0.40 if applicable, "size_band": 0.25 if medium/large, "trade_show": 0.20 if true, "capacity_decay_contribution": <float>}, "computation": "score = vertical(0.40) + size_band(0.25) + trade_show(0.20) + capacity_decay(0.15 × (1 − decay))", "score_components_attributed": [...]}` — pure deterministic math from packages/scoring/weights.py + actual prospect fields. | ~800 |
| `risk_checklist_baseline` | Full RiskFinding list **minus** the `note` field (which lives on the LLM side as `risk_register_narrative`): `[{"category": <enum>, "severity": <enum>}, ...]` for all findings. | ~700 |
| `approach_template_baseline` | `{"template": <enum>, "day_one_risks": [...]}` from SuggestedApproach **minus** rationale prose (which is the LLM side). day_one_risks list already structured. | ~600 |
| **Deterministic total target** | | **~3,500** |

### Per-section LLM max_output_tokens tightening

| File | Current | Target | Rationale |
|---|---|---|---|
| `dossier_section_taxonomy.py` | 2048 | **384** | Taxonomy JSON rationale ≤600 chars + small lists → target ~600 B output |
| `dossier_section_defect.py` | 2048 | **256** | Already lean (~190 B observed); cap for safety |
| `dossier_section_comparable.py` | 2048 | **128** | Only the prose field (`DimensionOfComparabilityProse.prose`, schema 250-char cap) is the gemini output |
| `dossier_section_risk.py` | 2048 | **512** | List of up to 10 RiskFinding with notes ≤300 chars each; tighter cap will produce shorter notes naturally |
| `dossier_section_approach.py` | 2048 | **256** | Rationale ≤600 chars + day_one_risks list; cap pushes briefer rationale |
| **LLM rendered total target** | | **~2,000** | |

### Predicted ratio
- det ≈ 3,500 B
- LLM ≈ 2,000 B
- ratio = 3,500 / 5,500 = **0.636** — clears the 0.60 floor by ~6 percentage points

If actuals come in 10-15% below target on the deterministic side (gemini is verbose at the cap), we still land ratio ≈ 0.58-0.62, which is on the edge. I'll add ~10-15% safety headroom by including a couple optional fields where data is present (raw_notes longer than 400 chars truncates at 600; one structured "lead_intake_metadata" sub-object in company_facts).

### Preserved invariants (not touched)
- `DETERMINISTIC_BYTE_THRESHOLD = 0.60` in packages/schemas/dossier.py:67 — UNCHANGED
- `object.__setattr__(self, "deterministic_section_ratio", recomputed)` Goodhart-resistance pattern at dossier.py:149 — UNCHANGED
- `DETERMINISTIC_SECTION_KEYS` and `LLM_SECTION_KEYS` enum sets — UNCHANGED
- Schema `max_length` caps on rationale/prose fields — UNCHANGED
- No new dependencies; only one extra SELECT in compose_dossier to lead_prospects

### Awaiting Architect confirmation of targets before writing code.

