# PHASE_1_5_DEBUG_SPEC.md

## §A SCOPE DISCIPLINE

This specification dictates exactly what Phase 1.5 IS and IS NOT. 

**In scope:**
- Driving `docker compose up` to a clean end-to-end run.
- Ensuring the pipeline flows end-to-end: CSV upload → Stage 1 prioritization → top-12 stubs → click → Stage 2 dossier → three surfaces, hitting `MATTA_COMPREHENSION.md` §8.5 milestones within ±5 seconds tolerance.
- Achieving three consecutive smoke-test passes as the exit condition.
- Lifting the STOP recommendation on demo recording.

**Out of scope (DEFERRED to Phase 1.6 or post-engagement):**
- Adding an Alembic migrations directory (current raw `text(...)` SQL DDL stays).
- Replacing 2-line integration test stubs with full E2E test trio.
- Refactoring the Stage 2 orchestrator from `send_task` chains to Celery `chord/group`.
- De-hardcoding `vertical = "metal_casting"` in `dossier_section_defect.py` (it is permitted as demo scaffolding for now).
- Implementing production conformal calibration (Phase 1 keeps the 30-event synthetic holdout).
- Writing real OAuth installs (Phase 1.5 stays on mock surfaces in `apps/mocks/`).
- Building a DLQ observability dashboard.
- Implementing multi-tenancy.

*If Gemini CLI is tempted to fix any out-of-scope item to clear a symptom, halt and surface — that's solving the wrong problem.*

## §B NIA-FIRST EXPLORATION DISCIPLINE

**NON-NEGOTIABLE:** NIA IS THE PRIMARY EXPLORATION TOOL.

When you execute this spec, you MUST use Nia MCP search and read to explore the existing codebase to anchor every diagnostic instruction to specific files. Direct repo read (grep, view, cat, ls) is permitted ONLY for:
- Running scripts.
- Verifying invariant counts (e.g., `extra="forbid"`, `cmms` residue, model strings).
- Viewing a specific file after Nia has surfaced it.

Defaulting to generic `grep` across the codebase drains session budget. You must honor this discipline.

## §C STAGE 1 — PRE-FLIGHT VERIFICATION (Gemini autonomous)

**Time-box:** 30 min target, 60 min hard cap.

Execute the following checks sequentially. If a check passes, log to `PHASE_1_5_LOG.md` and proceed. If it fails, attempt the named fix from the decision tree in §F. If the fix fails after 2 attempts, escalate per §G.

1. **Environment Variables:** Verify `.env` is present at the repo root and matches the Settings model in `apps/refinery_api/config.py`.
   - Command: `cat .env | grep -E "POSTGRES_URL|REDIS_URL|CELERY_BROKER|GCP_PROJECT|VERTEX_LOCATION|SLACK_SIGNING_SECRET|CRM_WEBHOOK_SECRET_HUBSPOT|CRM_WEBHOOK_SECRET_SALESFORCE|MOCK_SURFACES|KAIDE_LABS_PROJECT_ID"`
   - Expected: All fields must return a configured value.

2. **Docker Daemon:** Verify the Docker daemon is responsive.
   - Command: `docker info`
   - Expected: Exit code 0.

3. **Database & Cache Services:** Start and verify Postgres and Redis.
   - Command: `docker compose up postgres redis -d && sleep 5 && docker compose ps`
   - Expected: Both services show `Up` and `healthy`.
   - Command (Postgres): `psql -U postgres -h localhost -d refinery -c "\dt"`
   - Expected: Returns table list without connection error.
   - Command (Redis): `redis-cli -h localhost PING`
   - Expected: `PONG`

4. **Mock Surfaces:** Start and verify the mock API servers.
   - Command: `docker compose up mock_slack mock_crm mock_drive -d && sleep 5`
   - Command (Verify): `curl -s -o /dev/null -w "%{http_code}" http://localhost:8090/health` (repeat for 8091 and 8092 if endpoints exist, or verify via `docker compose ps`).
   - Expected: Services are up.

5. **Unit Tests:** Verify structurally sound code.
   - Command: `python -m pytest tests/unit/ -q`
   - Expected: `15 passed`

6. **Knowledge Graph Validation:** Check provenance.
   - Command: `python scripts/verify_knowledge_graph.py`
   - Expected: Exit code 0, outputs "Knowledge graph provenance check passed."

7. **Vertex AI Authentication:** Verify GCP connectivity.
   - Command: `gcloud auth list` (expect active account)
   - Command: `gcloud config get-value project` (expect matches `GCP_PROJECT`)
   - Command: `gcloud services list --enabled 2>/dev/null | grep aiplatform` (expect >= 1 line)
   - Command: `gcloud ai models list --region=europe-west4 --filter='displayName~"gemini-3"' 2>/dev/null`
   - Expected: Models are listed without permission/404 errors.

## §D STAGE 2 — SMOKE TEST EXECUTION (Gemini autonomous)

**Time-box:** 60 min target, 120 min hard cap.

Goal: Run the canonical happy path and catalog every milestone failure. Log timing and drift to `PHASE_1_5_LOG.md`.

1. **Start Stack:**
   - Command: `docker compose up -d`
2. **Await Lifespan:**
   - Poll: `docker compose logs refinery_api 2>&1 | grep -c "Knowledge graph provenance check passed"`
   - Wait until count ≥ 1 (max 60 seconds).
3. **Theater UI Render Check (Human Escalation Point 1):**
   - Command: `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000`
   - If 200, log: "Theater UI HTTP 200 — visual render verification deferred to human (see §G escalation 1)." Do NOT block the smoke test.
4. **Trigger Demo:**
   - Command: `[ -f scripts/run_demo.sh ] && ./scripts/run_demo.sh || (python scripts/seed_mock_data.py && curl -X POST http://localhost:8080/ingest/batch -F "file=@mocks/UK_Metals_Expo_2025_leads.csv")`
5. **Observe Milestones:** Check the signals below and measure drift from nominal timing (±5 seconds tolerance).

| Milestone | Verbatim signal Gemini can observe |
|---|---|
| T+0 CSV accepted | `curl` returned HTTP 200 with JSON containing `batch_id` |
| T+2 ADC decision | `docker compose logs refinery_worker 2>&1 \| grep "refinery.classify_action_domain"` returns ≥1 line |
| T+5 Stage 1 fan-out | `psql -U postgres -h localhost -d refinery -c "SELECT COUNT(*) FROM lead_prospects WHERE batch_id = '<batch_id>'"` returns 124 |
| T+8 Magic Moment 1 | THREE queries pass simultaneously: (a) `curl http://localhost:8090/api/canvases/list` returns ≥1 canvas, (b) `curl http://localhost:8091/api/contacts/list` returns ≥12 records with fitness_score field, (c) `curl http://localhost:8092/api/docs/list` returns ≥1 doc with title containing "Priority Index" |
| T+12 click trigger | `curl -X POST http://localhost:8080/slack/interactions -d '@mocks/williams_cook_click.json'` returns 200; then `docker compose logs refinery_worker 2>&1 \| grep "refinery.generate_dossier"` returns ≥1 line |
| T+25-78 Stage 2 cards | `docker compose logs refinery_worker 2>&1 \| grep -E "dossier_section_(taxonomy\|defect\|comparable\|risk\|approach)"` returns ≥5 lines |
| T+86 byte-density | `psql -U postgres -h localhost -d refinery -c "SELECT deterministic_section_ratio FROM dossier_artifacts ORDER BY generated_at DESC LIMIT 1"` returns value ≥0.60 |
| T+87 transactional outbox| `psql -U postgres -h localhost -d refinery -c "SELECT COUNT(*) FROM outbox WHERE dossier_id = '<dossier_id>'"` returns 3 |
| T+88 Magic Moment 2 | Same three curl checks as T+8 but with updated content (canvas count incremented, new CRM note, Drive doc with [Share] enabled) |
| T+89 cost ticker | Cost ticker is UI-rendered, no autonomous signal — defer to human verification per §G |

6. **End of Smoke Test:** Produce a structured failure list per §E.

## §E STAGE 3 — TRIAGE (Gemini autonomous)

Classify observed Stage 2 failures:

**(a) Blocking — smoke test cannot continue.**
Stop smoke test, attempt named fix from §F decision tree, re-run smoke test. Max 3 fix attempts per blocking failure before escalating per §G.

**(b) Non-blocking but milestone-affecting.**
Log to `PHASE_1_5_LOG.md`, attempt named fix from §F, continue smoke test, re-run full smoke test after the fix.

**(c) Cosmetic / log noise only.**
Log to `PHASE_1_5_LOG.md`, do NOT fix. Deferred to Phase 1.6.

Do NOT use LLM judgment to triage. Pattern-match against §F strictly.

## §F DECISION TREE — LIKELY FAILURE MODES + FIX PATTERNS

**1. Vertex AI Deprecation**
- **Signal:** Log shows `model not found: gemini-3-flash-preview` or `404`.
- **Cause Hypothesis:** HIGH. Preview model deprecated.
- **Nia Targets:** `packages/prompts/*.py`, `apps/refinery_worker/tasks/dossier_section_*.py`.
- **Fix:** Run `gcloud ai models list --region=europe-west4`. Replace the old model string with the current preview/GA equivalent strictly within the `gemini-3` family.
- **Re-test:** Re-run smoke test trigger (T+0).

**2. N=3 Vertical Disagreement**
- **Signal:** Worker log errors out in `classify_vertical.py` without returning a consensus.
- **Cause Hypothesis:** MEDIUM. Genuine three-way ensemble disagreement.
- **Nia Targets:** `packages/uncertainty/conformal.py`, `apps/refinery_worker/tasks/classify_vertical.py`.
- **Fix:** Mark `requires_human_review=True` rather than failing the task entirely.
- **Re-test:** Re-run smoke test (T+0).

**3. Byte-Density Gate Rejection**
- **Signal:** `compose_dossier` logs `ValidationError` on `deterministic_section_ratio`.
- **Cause Hypothesis:** HIGH. Stage 2 LLM output is too verbose.
- **Nia Targets:** `packages/prompts/*.py`.
- **Fix:** Tighten `max_output_tokens` in the prompt files.
- **Re-test:** T+12 click trigger.

**4. Slack Signature Verification Failure**
- **Signal:** `apps/refinery_api` returns 401/403 for Slack events.
- **Cause Hypothesis:** HIGH. Mock signing was lax vs real HMAC-SHA256 requirement.
- **Nia Targets:** `packages/adapters/slack/signature.py`.
- **Fix:** Align verification with Slack docs (`v0:{ts}:{raw_body}` 5-min window).
- **Re-test:** T+12 click trigger.

**5. Pydantic Webhook Extra Inputs**
- **Signal:** `ValidationError: extra inputs are not permitted` in API logs.
- **Cause Hypothesis:** HIGH. Mock surface added an unexpected field.
- **Nia Targets:** `packages/schemas/` (specifically the failing schema), `apps/mocks/`.
- **Fix:** Add the field with `Field(default=None)` or fix the mock emitter. Prefer fixing the mock.
- **Re-test:** T+12 click trigger or T+0 trigger depending on origin.

**6. WebSocket Disconnect**
- **Signal:** `docker compose logs refinery_api 2>&1 | grep -i websocket` shows disconnect before T+88.
- **Cause Hypothesis:** MEDIUM. Idle connection timeout or worker payload mismatch.
- **Nia Targets:** `apps/refinery_api/routers/websocket.py`.
- **Fix:** Escalate to human per §G #1/#6, as UI cannot be autonomously checked for the exact break. Add keepalives to the API if connection is explicitly timing out.
- **Re-test:** Re-run full test.

**7. Broken Mermaid Diagram**
- **Signal:** `ULTIMATE_PRD.md` renders broken.
- **Cause Hypothesis:** LOW. Subgraph edge syntax issue.
- **Fix:** Cosmetic/Documentation issue — log and defer (Category C triage).

**8. Missing Calibration Table**
- **Signal:** `FileNotFoundError` for `calibration_table.json` at boot.
- **Cause Hypothesis:** HIGH. Build script not run.
- **Nia Targets:** `scripts/build_calibration_table.py`, `packages/uncertainty/calibration_table.json`.
- **Fix:** Ensure `python scripts/build_calibration_table.py` executes before or during API boot.
- **Re-test:** Restart `docker compose`.

**9. Zero/Stuck Coverage Meter**
- **Signal:** PreVisitDossier output in DB/logs lacks the recomputed `deterministic_section_ratio`.
- **Cause Hypothesis:** HIGH. `compose_dossier.py` not serializing the dynamically recomputed value.
- **Nia Targets:** `apps/refinery_worker/tasks/compose_dossier.py`.
- **Fix:** Ensure `model_dump_json()` on the `PreVisitDossier` includes the overwritten value.
- **Re-test:** T+12 click trigger.

**10. Outbox DLQ Routing**
- **Signal:** `outbox_dispatcher` moves records to `outbox_dlq` after 6 retries.
- **Cause Hypothesis:** HIGH. Mock servers returning 5xx or offline.
- **Nia Targets:** `apps/mocks/mock_slack/server.py`, `apps/mocks/mock_crm/server.py`, `apps/mocks/mock_drive/server.py`.
- **Fix:** Ensure mock servers are bound to correct ports and accepting POSTs.
- **Re-test:** T+12 click trigger.

**11. Universal Human Review**
- **Signal:** All dossiers generate with `requires_human_review=True`.
- **Cause Hypothesis:** MEDIUM. `DSCP_SEVERE_SHIFT_THRESHOLD` is too tight.
- **Nia Targets:** `packages/uncertainty/dscp.py`.
- **Fix:** Loosen the threshold so standard demo verticals pass.
- **Re-test:** T+12 click trigger.

**12. Excess Vertex Cost**
- **Signal:** `docker compose logs refinery_worker` shows retry loops or elevated `thinking_level`.
- **Cause Hypothesis:** MEDIUM. Transient API failures or bad thinking config.
- **Nia Targets:** `packages/prompts/*.py`.
- **Fix:** Explicitly enforce `thinking_level="minimal"` and cap celery retries.
- **Re-test:** T+12 click trigger.

**13. Mock Surface 5xx on Payload Shape Mismatch**
- **Signal:** `refinery_worker` logs `httpx.HTTPStatusError: 500` from mock surfaces.
- **Cause Hypothesis:** HIGH. Field name mismatch between `compose_dossier.py` outbox payload and mock expected schema.
- **Nia Targets:** `apps/refinery_worker/tasks/compose_dossier.py`, `apps/mocks/`.
- **Fix:** Align field names. Prefer changing the mock surface over changing the production Pydantic schemas.
- **Re-test:** T+12 click trigger.

**14. Celery Worker Not Picking Up Tasks**
- **Signal:** Smoke test stalls past T+2; worker logs show startup but no `Task received`.
- **Cause Hypothesis:** HIGH. Queue routing misconfigured or broker connection fail.
- **Nia Targets:** `apps/refinery_worker/app.py`, `apps/refinery_api/config.py`.
- **Fix:** Verify `CELERY_BROKER` env var and queue names match between producer and consumer.
- **Re-test:** T+0 CSV trigger.

**15. Early WebSocket Disconnects (Theater UI)**
- **Signal:** Theater UI HTTP 200, but browser console (if viewed by human) or API logs show WS disconnect in first 30s.
- **Cause Hypothesis:** MEDIUM. Idle timeout or worker emitting rejected payload shape.
- **Nia Targets:** `apps/refinery_api/routers/websocket.py`.
- **Fix:** Cannot autonomously verify UI side — escalate per §G. Diagnostic command: `docker compose logs refinery_api 2>&1 | grep -i websocket`.
- **Re-test:** N/A.

## §G HUMAN-ESCALATION TRIGGERS

Escalate ONLY for these exact conditions by writing `HUMAN_INTERVENTION_REQUEST.md` at the repo root and pausing execution.

1. **Theater UI visual render verification.**
   After the smoke test passes all autonomous milestones, write the request asking Hafeedh to open `http://localhost:3000`, visually walk through the §8.5 sequence, and confirm.

2. **Cost ticker reading.**
   Ask for verification of the cost ticker UI rendering in the same request as #1.

3. **Vertex AI model family deprecation.**
   If both `gemini-3-flash-preview` AND `gemini-3.1-pro-preview` return 404, AND `gcloud` lists no `gemini-3-*` family for `europe-west4`, escalate. This is an architectural decision.

4. **Architectural deviation required to clear a symptom.**
   If the ONLY fix to a blocking symptom touches the 4 invariants (ADC purity, N=3, `extra="forbid"`, Vertex region) or 5 tightenings, HALT and write `QA_BLOCKER.md`.

5. **Smoke test cannot complete after 4 hours total elapsed.**
   Time-box blown. Escalate for a re-scope decision (proceed to hand-edited recording vs continue debugging vs kill demo).

6. **Failure mode not in §F AND not resolvable with standard debugging.**
   Sprint-specific failure unanticipated by the spec. Escalate with the symptom, diagnostic commands run, and the hypothesis space.

*Escalation Format:*
Timestamp | Smoke-test stage | Exact failing command | Full log output | Hypothesis space | Actions already tried | Explicit request for Hafeedh.

## §H STAGE 5 — VERIFICATION (Gemini autonomous, three consecutive passes)

Once all blocking and named non-blocking failures are cleared:

1. `docker compose down -v`
2. `docker compose up -d`
3. Run smoke test. Verify all §8.5 milestones within ±5s tolerance.
4. If PASS: Repeat step 1-3 for Run #2.
5. If PASS: Repeat step 1-3 for Run #3.
6. If three consecutive passes are achieved:
   - Replace `⚠️ PARTIAL` with `✅ INTEGRATION-VERIFIED` in `MATTA_RECONCILIATION.md` §4(b).
   - Lift the STOP recommendation.
   - Commit with message: `update: PHASE_1.5 integration verified, demo recording authorized`
   - Push.

*If 2 passes + 1 flake occurs, it is NOT done. Investigate via §F. If the flake is a non-deterministic timing race, escalate per §G #6.*

## §I EXIT AND HANDOFF

**On Success:**
- Ensure all commits use pattern `fix(phase-1.5): <symptom> <fix description>`.
- Ensure `PHASE_1_5_LOG.md` contains the full run history.
- Ensure `MATTA_RECONCILIATION.md` §4(b) is updated to `✅ INTEGRATION-VERIFIED`.
- Ensure NO `HUMAN_INTERVENTION_REQUEST.md` or `QA_BLOCKER.md` is outstanding.
- **Final Handoff String:** `"PHASE_1.5 integration verified at <SHA>, three consecutive smoke-test passes, STOP recommendation lifted, demo recording authorized."`

**On Escalation (§G triggered):**
- Smoke test is paused.
- **Handoff String:** `"PHASE_1.5 paused at <stage> awaiting human intervention per <filename>"`

**On Time-box Exceeded (§G #5):**
- **Handoff String:** `"PHASE_1.5 time-box exceeded, <N> failures cleared, <M> failures remaining, re-scope decision required."`
