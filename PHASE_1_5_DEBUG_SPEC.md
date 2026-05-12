# PHASE_1_5_DEBUG_SPEC.md

**Author:** Claude Code (Principal Architect, Kaide Labs FDE Strike Team)
**Executor:** Gemini CLI (autonomous)
**Anchor commit:** HEAD (post `9b38522`)
**Canonical success criterion:** `MATTA_COMPREHENSION.md` §8.5 milestones, ±5 s tolerance, three consecutive passes.
**Exit handoff string (success):** `"PHASE_1.5 integration verified at <SHA>, three consecutive smoke-test passes, STOP recommendation lifted, demo recording authorized."`

---

## §A SCOPE DISCIPLINE

Phase 1.5 is the **integration-debug** sprint between structural completeness (HEAD `9b38522`) and demo recording. It is bounded.

### A.1 In scope

- Driving `docker compose up` to a clean end-to-end run.
- One canonical happy path: CSV upload → ADC route `PRIORITIZATION` → Stage 1 fan-out across 124 leads → top-12 ranking surfaces (Slack canvas + CRM + Drive doc) → click on William Cook Sheffield → ADC route `DOSSIER_FULL` → Stage 2 dossier (taxonomy, defect, comparable, risk, approach) → byte-density gate ≥0.60 → transactional outbox → three surface updates.
- Hitting every `MATTA_COMPREHENSION.md` §8.5 milestone within ±5 s tolerance.
- **Three consecutive end-to-end passes** with `docker compose down -v` between runs.
- Lifting the STOP recommendation in `MATTA_RECONCILIATION.md` §4(b).

### A.2 Out of scope — DEFERRED to Phase 1.6 or post-engagement

If Gemini is tempted to touch any item below to clear a symptom, **halt and escalate per §G #4** — that is solving the wrong problem.

1. Alembic migrations directory. Current raw `text(...)` SQL DDL inlined in tasks stays.
2. Replacing the 2-line integration test stubs with full E2E test trio.
3. Refactoring Stage 2 orchestrator from `send_task` chains to Celery `chord` / `group`.
4. De-hardcoding `vertical = "metal_casting"` in `apps/refinery_worker/tasks/dossier_section_defect.py`. The hardcode is permitted demo scaffolding.
5. Production conformal calibration. Phase 1 keeps the 30-event synthetic holdout.
6. Real OAuth installs for Slack, HubSpot, Drive. Phase 1.5 stays on the mock surfaces under `apps/mocks/`.
7. DLQ observability dashboard.
8. Multi-tenancy.

### A.3 Locked invariants (architectural — DO NOT touch)

If clearing a blocking symptom would require modifying any of the following, **halt and write `QA_BLOCKER.md` per §G #4**:

- Deterministic two-route ADC with **zero LLM imports** in `apps/refinery_api/routers/slack_events.py` / `slack_interactions.py` and any router file.
- N=3 ensemble with `thinking_level="minimal"` and temperatures `0.1 / 0.5 / 0.9`.
- `extra="forbid"` on **all 28 of 28** Pydantic BaseModel boundaries.
- Vertex AI pinned to `europe-west4`.
- The five 1F-red v3 tightenings: transactional outbox, Slack distributed lock, byte-density validator (≥0.60), section-granular DS-CP, deployment topology diagram.
- Pinned model strings: `gemini-3-flash-preview` (Flash, N=3 ensemble) and `gemini-3.1-pro-preview` (Pro, single call). Only autonomous replacement permitted is to a currently available preview/GA of the same family per §F #1.

### A.4 Known spec-vs-ship reconciliation notes (read once before Stage 1)

`MATTA_COMPREHENSION.md` §8 / §8.5 uses approximate port numbers that **do not match** the actual `docker-compose.yml`. Canonical values are the compose file:

| Resource | Comprehension says | Compose says (canonical) |
|---|---|---|
| FastAPI | `http://localhost:8000` | **`http://localhost:8080`** |
| Mock Slack | `9001` | **`8090`** |
| Mock CRM | `9002` | **`8091`** |
| Mock Drive | `9003` | **`8092`** |
| Theater UI | `3000` | `3000` (matches) |
| Postgres | `5432` | **not host-exposed** — use `docker compose exec postgres psql ...` |
| Redis | `6379` | **not host-exposed** — use `docker compose exec redis redis-cli ...` |

All commands in this spec use the compose-canonical values. Do not "fix" the comprehension doc — it is a frozen audit artifact.

---

## §B NIA-FIRST EXPLORATION DISCIPLINE

**Non-negotiable.** Nia MCP search and read are the primary exploration tools for this sprint. Default to `mcp__nia__search` and `mcp__nia__nia_read` against the indexed repo (`Kaide-LABS/matta-refinery:master`).

Direct repository read (`grep -r`, `cat`, `view`, `ls -R`) is permitted **only** for:

1. Running scripts and tests (`python -m pytest ...`, `python scripts/...`, `bash scripts/run_demo.sh`).
2. Verifying verbatim invariant counts (`grep -rn 'extra="forbid"' packages/ apps/ | wc -l` must return 28; `grep -rn 'cmms' packages/ apps/ migrations/ scripts/ tests/ | wc -l` must return 0; `grep -rn 'gemini-3-flash-preview\|gemini-3.1-pro-preview' packages/ apps/` must return ≥12 hits).
3. Viewing a specific file **after** Nia has surfaced its path.
4. `docker compose` / `docker compose logs` / `docker compose exec` invocations.

Defaulting to wide grep across the codebase drains session budget. The same way it would drain Claude's. **Honor this discipline.**

When the spec references a file path, Gemini reads it via Nia first. Example pattern:

```
# Step: Read the compose_dossier task to verify the transactional outbox pattern.
# Use Nia:
mcp__nia__nia_read --repo Kaide-LABS/matta-refinery --path apps/refinery_worker/tasks/compose_dossier.py
# Only fall through to direct cat if Nia returns truncated or stale content.
```

---

## §C STAGE 1 — PRE-FLIGHT VERIFICATION (Gemini autonomous)

**Time-box:** 30 min target, **60 min hard cap**. On hard-cap blown, escalate per §G #5.

Execute the 7 checks below sequentially. For each: on PASS, append a single line to `PHASE_1_5_LOG.md` in the form `[STAGE1.<N>] PASS <UTC timestamp> <one-line evidence>` and proceed. On FAIL, jump to the matching §F entry, attempt the fix, then re-run the check. Max **2 fix attempts** per check before escalating per §G #6.

### C.1 `.env` matches Settings model

```bash
test -f .env || { echo "MISSING_ENV_FILE"; exit 1; }
for k in POSTGRES_URL REDIS_URL CELERY_BROKER GCP_PROJECT VERTEX_LOCATION SLACK_SIGNING_SECRET CRM_WEBHOOK_SECRET_HUBSPOT CRM_WEBHOOK_SECRET_SALESFORCE MOCK_SURFACES KAIDE_LABS_PROJECT_ID; do
  grep -qE "^${k}=" .env || echo "MISSING ${k}"
done
```

**PASS signal:** no `MISSING ...` line printed.
**FAIL signal:** any `MISSING ...` line. → §F #16.

### C.2 Docker daemon up

```bash
docker info > /dev/null 2>&1; echo "exit=$?"
```

**PASS:** `exit=0`. **FAIL:** non-zero. → §F #17.

### C.3 Postgres and Redis healthy

```bash
docker compose up -d postgres redis
sleep 8
docker compose ps --format json | grep -E '"Service":"(postgres|redis)"'
docker compose exec -T postgres psql -U postgres -d refinery -c '\dt' > /dev/null 2>&1; echo "pg_exit=$?"
docker compose exec -T redis redis-cli PING
```

**PASS:** `pg_exit=0` AND redis prints `PONG`.
**FAIL:** either non-zero/missing. → §F #18.

### C.4 Mock surfaces up and healthy

```bash
docker compose up -d mock_slack mock_crm mock_drive
sleep 5
for port in 8090 8091 8092; do
  code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:${port}/health)
  echo "mock_${port}=${code}"
done
```

**PASS:** all three lines read `=200`.
**FAIL:** any non-200. → §F #19.

### C.5 Unit tests pass (15/15)

```bash
python -m pytest tests/unit/ -q 2>&1 | tail -3
```

**PASS:** final line matches `^15 passed` (or `^15 passed in ...s$`).
**FAIL:** any other count, any failures, any errors. → §F #20.

### C.6 Knowledge graph validates

```bash
python scripts/verify_knowledge_graph.py; echo "kg_exit=$?"
```

**PASS:** `kg_exit=0`. **FAIL:** non-zero. → §F #21.

### C.7 Vertex AI authentication & model availability

```bash
gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -1
gcloud config get-value project
proj_env=$(grep '^GCP_PROJECT=' .env | cut -d= -f2)
proj_gcloud=$(gcloud config get-value project 2>/dev/null)
[ "${proj_env}" = "${proj_gcloud}" ] && echo "proj=match" || echo "proj=mismatch env=${proj_env} gcloud=${proj_gcloud}"
gcloud services list --enabled --filter="config.name:aiplatform.googleapis.com" --format="value(config.name)" | head -1
# Model availability: try gcloud first, then curl fallback
gcloud ai models list --region=europe-west4 --filter='displayName~"gemini-3"' --format="value(name)" 2>/dev/null | head -5
if [ $? -ne 0 ] || [ -z "$(gcloud ai models list --region=europe-west4 --filter='displayName~\"gemini-3\"' --format='value(name)' 2>/dev/null)" ]; then
  token=$(gcloud auth print-access-token)
  curl -s -H "Authorization: Bearer ${token}" \
    "https://europe-west4-aiplatform.googleapis.com/v1/projects/${proj_env}/locations/europe-west4/publishers/google/models" | grep -E "gemini-3" | head -5
fi
```

**PASS:** active account printed, `proj=match`, `aiplatform.googleapis.com` printed, ≥1 line containing `gemini-3-flash-preview` AND ≥1 line containing `gemini-3.1-pro-preview` surface.
**FAIL — either model missing:** → §F #1 (preview deprecation autonomous fix path).
**FAIL — entire `gemini-3-*` family missing for europe-west4:** → §G #3 escalation.

---

## §D STAGE 2 — SMOKE TEST EXECUTION (Gemini autonomous)

**Time-box:** 60 min target, **120 min hard cap**. Hard cap blown → §G #5.

### D.1 Bring up the full stack

```bash
docker compose up -d
# Tail logs to file for the duration of the smoke test
docker compose logs -f > PHASE_1_5_LOG.smoke.$(date -u +%Y%m%dT%H%M%SZ).log 2>&1 &
LOG_PID=$!
echo "log_pid=${LOG_PID}"
```

### D.2 Wait for FastAPI lifespan completion

The lifespan in `apps/refinery_api/main.py` calls `validate_graph_or_die()` first. Poll for evidence that lifespan finished and the app is serving:

```bash
for i in $(seq 1 30); do
  code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health)
  if [ "${code}" = "200" ]; then echo "api_ready_at=${i}s"; break; fi
  sleep 2
done
docker compose logs refinery_api 2>&1 | grep -E "validate_graph_or_die|provenance|Application startup complete" | tail -5
```

**PASS:** `api_ready_at` printed within 60 s AND no `Traceback` in `refinery_api` logs.
**FAIL — timeout:** → §F #22.
**FAIL — traceback in logs:** read the traceback. If it names a §F entry, apply that fix. Otherwise → §G #6.

### D.3 Theater UI HTTP probe (visual deferred)

```bash
code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
echo "theater_http=${code}"
```

**PASS — HTTP 200:** log `"Theater UI HTTP 200 — visual render verification deferred to human (see §G #1)."` and continue. **Do not** block smoke test on visual render.
**FAIL — non-200 or connection refused:** → §F #23.

### D.4 Execute the canonical happy path

Two-step pattern: prep (`run_demo.sh`) then trigger ingest.

```bash
if [ -x scripts/run_demo.sh ]; then
  bash scripts/run_demo.sh 2>&1 | tee -a PHASE_1_5_LOG.md
fi
# Ingest the seeded CSV. The mock seeding lives in scripts/seed_mock_data.py; the CSV path is canonical.
CSV_PATH=$(find . -name "UK_Metals_Expo_2025_leads*.csv" -not -path "./.git/*" | head -1)
[ -z "${CSV_PATH}" ] && { echo "MISSING_CSV"; exit 1; }
INGEST_RESP=$(curl -s -X POST http://localhost:8080/ingest/batch -F "file=@${CSV_PATH}")
echo "${INGEST_RESP}" | tee -a PHASE_1_5_LOG.md
BATCH_ID=$(echo "${INGEST_RESP}" | python -c 'import sys,json; print(json.load(sys.stdin).get("batch_id",""))')
echo "batch_id=${BATCH_ID}"
SMOKE_T0=$(date +%s)
```

**PASS:** non-empty `batch_id`, HTTP body contains `"batch_id"`.
**FAIL — HTTP 422:** → §F #2 (CSV schema drift).
**FAIL — `MISSING_CSV`:** → §F #24.
**FAIL — connection refused / 5xx:** check `docker compose logs refinery_api` for traceback. → §F entry matching, or §G #6.

### D.5 Milestone observation table (verbatim signals)

For each milestone below, Gemini runs the verbatim command(s) at the named offset from `SMOKE_T0`, records observed timestamp `obs_t`, computes drift `obs_t - SMOKE_T0 - nominal`, and logs the line:

```
[MILESTONE <name>] nominal=<T+N>s obs=<obs>s drift=<±X>s PASS|FAIL <evidence>
```

| Milestone | Nominal | Verbatim autonomous signal |
|---|---|---|
| **M0** CSV accepted | T+0 | `D.4` returned HTTP 200 with non-empty `batch_id`. |
| **M1** ADC PRIORITIZATION | T+2 | `docker compose logs refinery_worker 2>&1 \| grep -c "refinery.classify_action_domain"` ≥ 1 |
| **M2** Stage 1 fan-out | T+5 | `docker compose exec -T postgres psql -U postgres -d refinery -tAc "SELECT COUNT(*) FROM lead_prospects WHERE batch_id='${BATCH_ID}'"` returns `124` |
| **M3** Magic Moment 1 | T+8 | **ALL THREE pass simultaneously:** (a) `curl -s http://localhost:8090/api/canvases/list \| python -c 'import sys,json;print(len(json.load(sys.stdin)))'` ≥ 1; (b) `curl -s http://localhost:8091/api/contacts/list \| python -c 'import sys,json;d=json.load(sys.stdin);print(sum(1 for r in d if "fitness_score" in r))'` ≥ 12; (c) `curl -s http://localhost:8092/api/docs/list \| python -c 'import sys,json;print(any("Priority Index" in r.get("title","") for r in json.load(sys.stdin)))'` prints `True` |
| **M4** Click trigger | T+12 | `curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8080/slack/interactions -H "Content-Type: application/json" --data-binary "@apps/mocks/fixtures/williams_cook_click.json"` returns `200`; then `docker compose logs refinery_worker 2>&1 \| grep -c "refinery.generate_dossier"` ≥ 1 |
| **M5** Stage 2.1 taxonomy | T+25–30 | `docker compose logs refinery_worker 2>&1 \| grep -c "dossier_section_taxonomy"` ≥ 1 |
| **M6** Stage 2.2 defect | T+45 | `grep -c "dossier_section_defect"` ≥ 1 AND `psql ... -tAc "SELECT defect_hypothesis IS NOT NULL FROM dossier_artifacts WHERE batch_id='${BATCH_ID}' ORDER BY generated_at DESC LIMIT 1"` returns `t` |
| **M7** Stage 2.3 comparable | T+55 | `grep -c "dossier_section_comparable"` ≥ 1 |
| **M8** Stage 2.4 risk | T+70 | `grep -c "dossier_section_risk"` ≥ 1 |
| **M9** Stage 2.5 approach | T+78 | `grep -c "dossier_section_approach"` ≥ 1 |
| **M10** Byte-density | T+85–86 | `psql ... -tAc "SELECT deterministic_section_ratio FROM dossier_artifacts WHERE batch_id='${BATCH_ID}' ORDER BY generated_at DESC LIMIT 1"` returns numeric ≥ `0.60` |
| **M11** Transactional outbox | T+87 | `psql ... -tAc "SELECT COUNT(*) FROM outbox WHERE dossier_id=(SELECT id FROM dossier_artifacts WHERE batch_id='${BATCH_ID}' ORDER BY generated_at DESC LIMIT 1)"` returns `3` |
| **M12** Magic Moment 2 | T+88 | **ALL THREE:** (a) canvas count from M3.a query is now `+1`; (b) CRM has a new note record with `note_type='dossier_link'` (`curl -s http://localhost:8091/api/notes/list \| python -c '...'` ≥ 1); (c) Drive has a new doc with `share_enabled=true` |
| **M13** Cost ticker | T+89 | **UI-only signal — autonomous defer.** Log `"M13 deferred to §G #2 human verification."` |

Acceptance per milestone: PASS if drift ≤ ±5 s AND signal evaluates true. FAIL otherwise.

### D.6 End of smoke test

Stop the log tail (`kill ${LOG_PID}`). Compile the failure list and proceed to §E.

---

## §E STAGE 3 — TRIAGE (Gemini autonomous, deterministic decision tree)

Gemini does **not** use LLM judgment to triage. It pattern-matches each observed failure into exactly one of three buckets based on the rules below.

### E.1 Bucket (a) — BLOCKING

A failure is blocking if and only if **any** of the following hold:
- The smoke test cannot continue past the current step (e.g., API never serves health 200).
- A milestone M0–M4 fails (these are stage-gates; later milestones cannot be evaluated without them).
- An `extra="forbid"` `ValidationError` was raised AND it touches a production schema (not a mock surface).
- Postgres or Redis exited / unhealthy mid-run.

**Action:** stop smoke test → apply §F fix for the matching symptom → re-run the **full** smoke test from §D.1. Max **3 fix attempts** per blocking failure before escalating per §G #6.

### E.2 Bucket (b) — NON-BLOCKING BUT MILESTONE-AFFECTING

A failure is in bucket (b) if the smoke test completed but **one or more** of M5–M12 failed or drifted >±5 s. Specifically:
- Milestone drifted >±5 s but landed.
- Milestone failed but later milestones still landed (rare but possible if a section task swallowed an exception).
- `outbox` count is 2 of 3 (one surface dispatch missing).

**Action:** log to `PHASE_1_5_LOG.md`, apply §F fix, re-run full smoke test from §D.1.

### E.3 Bucket (c) — COSMETIC / LOG NOISE

A failure is cosmetic if and only if **all** of the following hold:
- No milestone failed.
- No `ValidationError`, no `Traceback`, no HTTP 5xx in any log file.
- The artifact is purely a log warning, a deprecation notice, or a non-load-bearing stderr line.

**Action:** log to `PHASE_1_5_LOG.md` under `## Deferred to Phase 1.6 (cosmetic)`. **Do not fix.**

---

## §F DECISION TREE — LIKELY FAILURE MODES + FIX PATTERNS

Each entry: **failing signal** → **root cause** (confidence) → **files to read via Nia** → **fix pattern** → **re-test command**.

### F.1 Vertex AI preview model deprecated *(from comprehension #1)*

- **Signal:** `refinery_worker` logs `google.api_core.exceptions.NotFound: 404 ... model not found: gemini-3-flash-preview` (or `gemini-3.1-pro-preview`).
- **Root cause (HIGH):** preview model rolled forward after build.
- **Files via Nia:** `packages/prompts/*.py`, `apps/refinery_worker/tasks/dossier_section_*.py`, `apps/refinery_worker/tasks/classify_vertical.py`, `apps/refinery_worker/tasks/score_fitness.py`.
- **Autonomous fix:** query Vertex for currently-available family members:
  ```bash
  token=$(gcloud auth print-access-token)
  curl -s -H "Authorization: Bearer ${token}" \
    "https://europe-west4-aiplatform.googleapis.com/v1/projects/$(gcloud config get-value project)/locations/europe-west4/publishers/google/models" \
    | grep -E "gemini-3" | sort -u
  ```
  Replace only with another `gemini-3-*-preview` or `gemini-3-*` GA of the same Flash/Pro tier. Update via `sed -i 's/gemini-3-flash-preview/<new_flash>/g' packages/prompts/*.py apps/refinery_worker/tasks/*.py` (and analogous for Pro). Commit `fix(phase-1.5): pin Vertex model strings to <new>` on master.
- **Forbidden:** swapping to a non-`gemini-3-*` family (e.g., 2.5). That escalates per §G #3.
- **Re-test:** §C.7 then §D.

### F.2 CSV upload returns HTTP 422 *(from comprehension #5 + ingest)*

- **Signal:** `D.4` returns 422 with body containing `extra inputs are not permitted` or `field required`.
- **Root cause (HIGH):** `LeadIntakeRow` schema in `packages/schemas/lead_intake.py` diverged from CSV column headers, OR the CSV in `mocks/` has been replaced.
- **Files via Nia:** `packages/schemas/lead_intake.py`, `apps/refinery_api/routers/ingest.py`, the CSV at `mocks/UK_Metals_Expo_2025_leads.csv`.
- **Fix:** prefer aligning the CSV (test scaffolding) to the schema (production contract). If a column header was renamed in source data, rename in CSV. If the schema accidentally lost a column that exists in the canonical CSV, **escalate per §G #4** — that touches a production boundary.
- **Re-test:** §D.4.

### F.3 N=3 Flash ensemble disagreement *(from comprehension #2)*

- **Signal:** `classify_vertical` task log line `plurality_vote: no_majority` AND `requires_human_review=True` on the dossier output.
- **Root cause (MEDIUM):** genuine three-way disagreement on a borderline prospect. Often William Cook himself is fine; check non-anchor prospects.
- **Files via Nia:** `apps/refinery_worker/tasks/classify_vertical.py`, `packages/uncertainty/conformal.py`.
- **Fix:** if disagreement is on William Cook → real bug; verify prompt fidelity (no token drift, temps locked 0.1/0.5/0.9). If on a non-anchor prospect → expected behavior, surface in Theater pane; do not "fix" by changing the threshold.
- **Re-test:** §D milestone M3 / M4.

### F.4 Byte-density `ValidationError` *(from comprehension #3)*

- **Signal:** `compose_dossier` raises `ValidationError: deterministic_section_ratio < 0.60` OR M10 returns < 0.60.
- **Root cause (HIGH):** LLM section prose too verbose.
- **Files via Nia:** `packages/prompts/dossier_*.py`, `apps/refinery_worker/tasks/compose_dossier.py`.
- **Fix:** lower `max_output_tokens` in the offending prompt. **Forbidden:** lowering the 0.60 threshold (it is a tightening). If multiple prompts are above their cap, lower all proportionally.
- **Re-test:** §D milestones M10, M11.

### F.5 Slack signature verification fails *(from comprehension #4)*

- **Signal:** `apps/refinery_api/routers/slack_*.py` logs `signature_verification_failed`.
- **Root cause (HIGH):** mock fixture body was modified after the HMAC was computed, OR `SLACK_SIGNING_SECRET` in `.env` differs from the mock's signing key.
- **Files via Nia:** `packages/adapters/slack/signature.py`, `apps/mocks/fixtures/williams_cook_click.json`, `apps/mocks/mock_slack/server.py`.
- **Fix:** regenerate the fixture HMAC using the current `SLACK_SIGNING_SECRET` and the `v0:{ts}:{raw_body}` window. If the body must change, recompute the signature; do not weaken signature verification.
- **Re-test:** §D milestone M4.

### F.6 `extra="forbid"` `ValidationError` on a mock surface payload *(from comprehension #5)*

- **Signal:** worker logs `pydantic_core._pydantic_core.ValidationError: ... extra_forbidden` where the producer of the bad payload is one of `apps/mocks/*`.
- **Root cause (HIGH):** mock emits a field not in the schema.
- **Files via Nia:** schema file named in traceback; the mock surface emitter (`apps/mocks/mock_*/server.py`).
- **Fix:** **prefer changing the mock** (test scaffolding) to changing the schema (production boundary). Remove the spurious field from the mock emitter. Adding `Field(default=None)` to a production schema is permitted **only** if the field is genuinely optional in the real Slack/HubSpot/Drive API contract — verify against the adapter doc before doing so; otherwise escalate per §G #4.
- **Re-test:** §D milestone where it failed.

### F.7 WebSocket disconnects before T+88 *(from comprehension #6, expanded to F.15 below)*

See §F.15 — this is one of the three additions and is partially-autonomous-fixable. Diagnostic only at this entry; the autonomous diagnostic command is in §F.15.

### F.8 Mermaid diagram broken *(from comprehension #7)*

- **Bucket:** (c) cosmetic. Do not fix.

### F.9 Calibration table missing at boot *(from comprehension #8)*

- **Signal:** `refinery_api` lifespan traceback `FileNotFoundError: packages/uncertainty/calibration_table.json`.
- **Root cause (HIGH):** `scripts/build_calibration_table.py` not run before `docker compose up`.
- **Files via Nia:** `scripts/build_calibration_table.py`, `packages/uncertainty/calibration.py`.
- **Fix:** `python scripts/build_calibration_table.py`. Then restart only the API: `docker compose restart refinery_api`. Note: `scripts/run_demo.sh` already calls this; if it's still missing, `run_demo.sh` didn't execute — investigate that next.
- **Re-test:** §D.2.

### F.10 Coverage meter stuck at 0 *(from comprehension #9)*

- **Signal:** M10 returns `0.0` or `NULL`.
- **Root cause (MEDIUM):** `compose_dossier.py` not recomputing `deterministic_section_ratio` before `model_dump_json()`.
- **Files via Nia:** `apps/refinery_worker/tasks/compose_dossier.py`, `packages/schemas/pre_visit_dossier.py`.
- **Fix:** ensure `dossier.deterministic_section_ratio = compute_ratio(dossier)` runs **before** the `model_dump_json()` and **before** the `with engine.begin()` block.
- **Re-test:** §D milestone M10.

### F.11 Outbox DLQ moves *(from comprehension #10)*

- **Signal:** `outbox_dispatcher` log line `moved_to_dlq` OR `outbox` rows stuck in `state='pending'` past M12.
- **Root cause (HIGH):** mock surface returning 5xx, OR mock not bound to expected port.
- **Files via Nia:** `apps/refinery_worker/tasks/outbox_dispatcher.py`, `apps/mocks/mock_*/server.py`, `docker-compose.yml`.
- **Fix:** first verify port binding via `docker compose ps`. If a mock is unhealthy, restart it: `docker compose restart mock_<name>`. If the mock is returning 5xx, see §F.13.
- **Re-test:** §D milestone M12.

### F.12 `requires_human_review=True` on every dossier *(from comprehension #11)*

- **Signal:** every dossier in `dossier_artifacts` has `requires_human_review=true`.
- **Root cause (MEDIUM):** DS-CP threshold mis-tuned.
- **Files via Nia:** `packages/uncertainty/dscp.py`.
- **Fix:** **read** `DSCP_SEVERE_SHIFT_THRESHOLD` and the 30-event holdout coverage. If `metal_casting` is failing the gate at the demo seed, the threshold is too tight — relax to the **lowest** value that admits the seed `metal_casting` prospects but still rejects an obvious out-of-distribution synthetic. Do **not** disable the gate.
- **Re-test:** §D milestones M6–M12 + verify that `requires_human_review=False` for William Cook specifically.

### F.13 Cost ticker > $0.037 *(from comprehension #12)*

- **Signal:** M13 (when verified by human per §G #2) reads >$0.10 ceiling.
- **Root cause (HIGH):** retry loop OR `thinking_level` accidentally elevated.
- **Files via Nia:** `apps/refinery_worker/app.py` (Celery retry config), `packages/prompts/*.py`.
- **Fix:** verify `thinking_level="minimal"` for all Flash calls and `thinking_level="medium"` for the single Pro call. Cap `max_retries=2` on dossier-section tasks. Verify no exponential-retry storm by `grep "Retry"` count in worker logs (expected ≤6 across the run).
- **Re-test:** full §D run + human verification per §G #2.

### F.14 Mock surface 5xx on payload shape mismatch *(NEW — added by spec author)*

- **Signal:** `refinery_worker` logs `httpx.HTTPStatusError: Server error '500 Internal Server Error' for url 'http://mock_slack:8090/...'` (or analog for mock_crm:8091 / mock_drive:8092). Mock surface log shows a Python `KeyError` or `ValidationError` on incoming payload.
- **Root cause (HIGH):** field name mismatch between what `compose_dossier.py` (or upstream task) emits and what the mock surface's request handler expects.
- **Files via Nia:** the task emitting the call, the mock surface route handler. Read both side-by-side.
- **Fix:** **prefer changing the mock** to changing the production contract. Align the mock's expected field name to the task's emitted name. If the task is emitting against a real Slack/HubSpot/Drive contract published spec and the mock drifted from that spec, change the mock to match the spec. If the task emits a non-spec field, that's a production bug — escalate per §G #4.
- **Re-test:** §D milestone M3 or M12 (whichever is failing).

### F.15 Celery worker not picking up tasks *(NEW)*

- **Signal:** smoke test stalls past T+2; `docker compose logs refinery_worker` shows `celery@... ready.` but no task execution lines. Or M1 stays at 0 past 10 s.
- **Root cause (HIGH for queue routing, MEDIUM for prefetch, LOW for broker):**
  1. Queue routing mismatch — `app.send_task("refinery.classify_action_domain", queue="ingest")` but the worker subscribed only to `default`.
  2. `worker_prefetch_multiplier=0` or pathological config.
  3. Broker URL mismatch — `CELERY_BROKER` in `.env` not equal to the redis service URL from inside the compose network.
- **Files via Nia:** `apps/refinery_worker/app.py`, `apps/refinery_api/routers/ingest.py`, `apps/refinery_api/routers/slack_interactions.py`, `.env` (`CELERY_BROKER`).
- **Diagnostic commands:**
  ```bash
  docker compose exec -T redis redis-cli LLEN ingest
  docker compose exec -T redis redis-cli LLEN dossier
  docker compose exec -T redis redis-cli LLEN default
  docker compose logs refinery_worker 2>&1 | grep -E "queue|Connected to|Registered tasks" | head -20
  ```
  If `LLEN` > 0 on a queue the worker doesn't consume → routing mismatch (root cause 1). Add queue to `worker.app.conf.task_queues` or change producer's `queue=` kwarg to match. If `LLEN` is 0 everywhere and producer logs no errors → broker URL mismatch (root cause 3). Compare `CELERY_BROKER` to `redis://redis:6379/0`.
- **Re-test:** §D milestone M1.

### F.16 WebSocket disconnects before T+88 *(NEW — partial-autonomous + escalation)*

- **Signal — autonomous side:** `docker compose logs refinery_api 2>&1 | grep -iE "websocket|ws disconnect|connection closed"` shows disconnect events within first 30 s after `docker compose up`.
- **Signal — UI side:** browser console shows `WebSocket connection to 'ws://localhost:8080/ws' closed`. **Gemini cannot observe this autonomously.**
- **Diagnostic commands (autonomous):**
  ```bash
  docker compose logs refinery_api 2>&1 | grep -iE "websocket" | head -30
  docker compose exec -T redis redis-cli --scan --pattern 'ws:*' | head
  ```
- **Root causes:** (HIGH) worker emits payload Theater UI rejects (validation in `useWebSocket.ts`); (MEDIUM) idle timeout no ping/pong; (LOW) reverse-proxy buffering (n/a — direct compose).
- **Autonomous fix attempt (one only):** if API logs show outgoing payload with a shape that does not match `apps/theater_ui/hooks/useWebSocket.ts` event schema (read both via Nia), align the worker's emitted shape to the UI's expected shape. If the only signal is a clean disconnect with no payload mismatch → likely idle timeout; **escalate per §G #1** (needs UI observation to confirm).
- **Re-test:** §D milestone M3 (the first surface where WS payloads matter) and human visual check.

### F.17 Pre-flight: missing env var

- **Signal:** §C.1 prints `MISSING <NAME>`.
- **Fix:** Gemini regenerates `.env` from `.env.example` if present, then fills the missing variable from sensible defaults (compose service URLs for `POSTGRES_URL`, `REDIS_URL`, `CELERY_BROKER`; `europe-west4` for `VERTEX_LOCATION`; `true` for `MOCK_SURFACES`). For **secret values** (`SLACK_SIGNING_SECRET`, `CRM_WEBHOOK_SECRET_*`, `GCP_PROJECT`, `KAIDE_LABS_PROJECT_ID`) — if no value is recoverable from `.env.example` or `infra/.env.template`, **escalate per §G #6**.
- **Re-test:** §C.1.

### F.18 Pre-flight: docker daemon down

- **Signal:** §C.2 `exit≠0`.
- **Fix:** on Windows host, attempt `wsl --status` and report. Gemini cannot autonomously start Docker Desktop. → §G #6.

### F.19 Pre-flight: postgres or redis unhealthy

- **Signal:** §C.3 fails.
- **Fix:** `docker compose down -v && docker compose up -d postgres redis && sleep 10` then retry. If still failing, `docker compose logs postgres` / `redis` and read the error. Port conflict → free the port. Image pull failure → retry. After 2 attempts: §G #6.
- **Re-test:** §C.3.

### F.20 Pre-flight: mock surface non-200

- **Signal:** §C.4 prints non-200 for any mock.
- **Fix:** `docker compose logs mock_<name>` — if `ImportError` or `ModuleNotFoundError`, the image build is stale, run `docker compose build mock_<name> && docker compose up -d mock_<name>`. If `Address already in use`, free the port and retry.
- **Re-test:** §C.4.

### F.21 Pre-flight: unit tests failing

- **Signal:** §C.5 not 15 passed.
- **Triage:** if failure count > 0 in a test introduced by the build (commit `93482e2` rewrote 4 stubs into real validators for criteria 12/13/14/15) → the validator caught a real regression. **Read the failing test via Nia**, locate the production code it exercises, fix the production code (not the test). If the count itself drifted (16 tests passing, or 14 instead of 15) → a test was added/removed since `9b38522`; verify via `git log -- tests/unit/`. Adjust the expected count in this spec by committing a fix to PHASE_1_5_DEBUG_SPEC.md only if the new count is the deliberate new floor.
- **Re-test:** §C.5.

### F.22 Pre-flight: knowledge graph validation fails

- **Signal:** §C.6 `kg_exit≠0`.
- **Diagnostic:** read stderr — it will name the offending anchor and the cited line. Recall `93482e2` fixed B&W and Caracol citation-line drift. If a new anchor drifted, read `Matta_Intel_cleaned.md` at the cited line and `packages/knowledge_graph/graph.json`, correct the citation line.
- **Re-test:** §C.6.

### F.23 Stage 2: API never serves health 200

- **Signal:** §D.2 `api_ready_at` never printed within 60 s.
- **Diagnostic:** `docker compose logs refinery_api 2>&1 | tail -100`. Traceback in lifespan → match against §F.1 (Vertex auth), §F.9 (calibration table), §F.22 (KG validate). No traceback but no `Application startup complete` → likely blocked on Vertex client init (network/credentials) → §F.1.
- **Re-test:** §D.2.

### F.24 Stage 2: Theater UI HTTP non-200

- **Signal:** §D.3 returns non-200.
- **Diagnostic:** `docker compose logs theater_ui 2>&1 | tail -50`. Next.js build error → fix per error message. Container not started → `docker compose up -d theater_ui`. Connection refused → port collision (3000 already in use).
- **Re-test:** §D.3.

### F.25 Smoke: missing seed CSV

- **Signal:** §D.4 prints `MISSING_CSV`.
- **Diagnostic:** check `scripts/seed_mock_data.py` — does it create the CSV at runtime, or expect it to exist? Read via Nia.
- **Fix:** if seed script creates it, ensure `bash scripts/run_demo.sh` ran first. If file is checked into `mocks/`, verify path. → if neither, §G #6.

---

## §G HUMAN-ESCALATION TRIGGERS

Gemini escalates ONLY for these six exact conditions. No LLM-judgment escalations.

### G.1 Theater UI visual render verification

**Fires when:** all autonomous milestones M0–M12 pass AND M13 is deferred. Required to lift STOP recommendation per §A.1.
**Action:** write `HUMAN_INTERVENTION_REQUEST.md` (see G.7 format) asking Hafeedh to open `http://localhost:3000`, walk through §8.5 timing visually, and confirm or report deviations on Slack/Theater/Drive panes.

### G.2 Cost ticker reading

**Fires when:** M13 is reached and smoke test otherwise passing. UI-only signal.
**Action:** included in the same `HUMAN_INTERVENTION_REQUEST.md` as G.1.

### G.3 Vertex AI `gemini-3-*` family deprecation

**Fires when:** §C.7 OR §F.1 finds **both** `gemini-3-flash-preview` AND `gemini-3.1-pro-preview` missing AND `gcloud ai models list --region=europe-west4 --filter='displayName~"gemini-3"'` returns zero rows.
**Action:** write `QA_BLOCKER.md` documenting the gcloud query, the model list returned, and the proposed replacement family options. **Do not** swap to `gemini-2.5-*` autonomously — that's an architectural decision touching the Doug-Brion methodology lineage anchor.

### G.4 Architectural deviation required to clear a symptom

**Fires when:** the only fix to a blocking symptom would touch one of the §A.3 locked invariants or §A.2 out-of-scope deferred items.
**Examples that trigger:**
- A symptom that would be cleared by removing `extra="forbid"` from a Pydantic schema.
- A symptom that would be cleared by adding an LLM call inside `apps/refinery_api/routers/slack_events.py` (would break deterministic ADC).
- A symptom that would be cleared by lowering the 0.60 byte-density threshold.
- A symptom that would be cleared by writing Alembic migrations (out of scope; raw `text(...)` DDL stays).
- A symptom that would be cleared by refactoring `send_task` chains to `chord/group`.
**Action:** write `QA_BLOCKER.md`. Do not implement.

### G.5 4-hour total time-box exceeded

**Fires when:** `(now - PHASE_1_5_START_TIME) > 4h`.
**Action:** halt smoke test, commit all WIP, write `HUMAN_INTERVENTION_REQUEST.md` framing re-scope decision: (1) proceed to hand-edited Vidyard recording from current partial state, (2) continue debugging with extended time-box, or (3) kill demo.

### G.6 Failure mode not in §F catalog AND not resolvable with general Python/Docker debugging

**Fires when:** observed symptom does not pattern-match any of §F.1–§F.25, AND a reasonable Python traceback / Docker `logs` inspection does not yield a fix in 2 attempts.
**Action:** write `HUMAN_INTERVENTION_REQUEST.md` with: timestamp, smoke-test stage, exact failing command + output, all diagnostic commands run, hypothesis space, all attempted fixes, what specifically Hafeedh needs to do.

### G.7 Escalation file format

Write `HUMAN_INTERVENTION_REQUEST.md` (or `QA_BLOCKER.md`) at repo root with these fields, in order:

```markdown
# <HUMAN_INTERVENTION_REQUEST | QA_BLOCKER> — <short symptom>

- **Trigger:** §G #<n>
- **Timestamp (UTC):** <iso8601>
- **Smoke-test stage:** <§C.<n> | §D.<n> | §H.run<n>>
- **Failing command:** `<verbatim>`
- **Observed output:** <verbatim, fenced>
- **Hypothesis space:** <enumerated list>
- **Attempts already made:** <enumerated list, each with verbatim command and outcome>
- **Specific human action required:** <one-paragraph>
- **Blocking?:** <yes/no — does this block §H verification>
```

Commit with message `escalate: <one-line>`. Push.

---

## §H STAGE 5 — VERIFICATION (Gemini autonomous, three consecutive passes)

Triggered only after all bucket (a) and bucket (b) failures from §E are cleared.

```bash
for RUN in 1 2 3; do
  echo "=== VERIFICATION RUN ${RUN} ==="
  docker compose down -v
  sleep 5
  # Execute Stage 1 (§C) and Stage 2 (§D) afresh
  # Implemented as a wrapper script for determinism:
  bash scripts/phase_1_5_run.sh ${RUN} 2>&1 | tee -a PHASE_1_5_LOG.md
  if [ $? -ne 0 ]; then
    echo "RUN ${RUN} FAILED — investigate via §F, do NOT proceed to RUN $((RUN+1))"
    exit 1
  fi
done
echo "=== THREE CONSECUTIVE PASSES ACHIEVED ==="
```

(If `scripts/phase_1_5_run.sh` does not exist at execution time, Gemini writes it as a thin wrapper that executes §C.1–§C.7 then §D.1–§D.6, exiting non-zero on any milestone failure.)

### H.1 Acceptance

- Three runs complete.
- All §D.5 milestones M0–M12 PASS with drift ≤ ±5 s on **all three** runs.
- M13 has been verified once by human (G.2) and is consistent across runs (`grep "cost_total" PHASE_1_5_LOG.md` shows the same value pattern).
- No new escalation files created during verification.

### H.2 Flake handling

Two passes + one flake = **not done**.
- Investigate the flake via §F decision tree.
- If flake source is non-deterministic (timing race in event ordering, etc.) and matches §F.15 root-cause patterns, fix and reset run counter to 0.
- If flake source is non-deterministic and does **not** match any §F entry → §G #6.

### H.3 On success — sign-off commit

```bash
# Update MATTA_RECONCILIATION.md §4(b)
# Atomic replacement:
python -c "
import re
p='MATTA_RECONCILIATION.md'
s=open(p,encoding='utf-8').read()
s=re.sub(r'(§4\(b\)[^\n]*?Verdict[^\n]*?)⚠️\s*PARTIAL', r'\1✅ INTEGRATION-VERIFIED', s)
s=re.sub(r'(STOP recommendation[^\n]*?)(in force|active|standing)', r'\1LIFTED', s, flags=re.I)
open(p,'w',encoding='utf-8').write(s)
"
git add MATTA_RECONCILIATION.md PHASE_1_5_LOG.md PHASE_1_5_DEBUG_SPEC.md scripts/phase_1_5_run.sh 2>/dev/null
git commit -m "update: PHASE_1.5 integration verified, demo recording authorized"
git push origin master
```

---

## §I EXIT AND HANDOFF

### I.1 On success

- All commits pushed with message pattern `fix(phase-1.5): <symptom> <fix description>`.
- `PHASE_1_5_LOG.md` contains the full run history: every command, every output, every milestone timing, every fix applied.
- `MATTA_RECONCILIATION.md` §4(b) updated to **✅ INTEGRATION-VERIFIED**, STOP recommendation **LIFTED**.
- No `HUMAN_INTERVENTION_REQUEST.md` outstanding (resolved ones may stay in git history).
- No `QA_BLOCKER.md` outstanding.
- **Final handoff string:**
  `"PHASE_1.5 integration verified at <SHA>, three consecutive smoke-test passes, STOP recommendation lifted, demo recording authorized."`

### I.2 On escalation

- `HUMAN_INTERVENTION_REQUEST.md` or `QA_BLOCKER.md` written and committed.
- Smoke test paused at current stage; no destructive teardown.
- **Handoff string:** `"PHASE_1.5 paused at <§D.<n> | §H.run<n>> awaiting human intervention per <filename>."`

### I.3 On time-box exceeded (§G #5)

- All work-in-progress committed (even partial fixes — better to surface than to lose).
- `PHASE_1_5_LOG.md` complete through last attempted command.
- **Handoff string:** `"PHASE_1.5 time-box exceeded, <N> failures cleared, <M> failures remaining, re-scope decision required."`

---

## §J APPENDIX — invariant verification one-liners (for spot-checks)

```bash
# 28 of 28 extra="forbid" boundaries
grep -rn 'extra="forbid"' packages/ apps/ | wc -l   # expect 28

# 0 cmms residue across production paths
grep -rni 'cmms' packages/ apps/ migrations/ scripts/ tests/ 2>/dev/null | wc -l   # expect 0

# 0 cummins (excluded company)
grep -rni 'cummins' packages/ apps/ 2>/dev/null | wc -l   # expect 0

# Pinned model strings present (≥12 hits combined)
grep -rn 'gemini-3-flash-preview\|gemini-3\.1-pro-preview' packages/ apps/ | wc -l   # expect ≥12

# No LLM imports in routers (deterministic ADC invariant)
grep -rnE 'from google import genai|import genai|vertexai' apps/refinery_api/routers/ | wc -l   # expect 0

# Vertex region pin
grep -rn 'europe-west4' packages/ apps/ | wc -l   # expect ≥3
```

Run these at the start of §C and again before §H.3 sign-off. Any deviation → §G #4.

---

**END OF SPEC.** Gemini CLI executes top-to-bottom. Spec author (Claude) does not re-enter unless §G #6 fires.
