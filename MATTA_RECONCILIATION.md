# MATTA_RECONCILIATION.md

**Kaide Labs — Forward Deployed Engineering Strike Team**
**Reconciliation date:** 2026-05-11

---

## §1 Summary

Sprint: **Matta Refinery Hybrid (Form C)** — synthesis from `MATTA_MASTER_PRD_v2.md` augmented with features carried from `LATERAL_PRD_v1..v4.md`, post-1F-red v3 tightenings per `validation_gate_1f_red_v3.md`. Final build commit `93482e2` (QA-fixed); status finalization at `2b9774f`. **One phase ran**: PHASE_1 covered the full 72-hour sprint as a single phase per its own §A scope discipline; 3B closed Branch A "loop complete." **Does what shipped solve the bottleneck the demo was specced to solve?** Structurally yes — the Stage 1 / Stage 2 / three-surface architecture from `ULTIMATE_PRD.md` §3.3–§3.4 is present in the shipped tree — but **end-to-end integration verification has not been run**, so the answer is conditional pending a Phase 1.5 integration debug pass before recording.

## §2 Spec-vs-Ship Reconciliation

| Specced item (PRD ref) | What shipped (path) | Status |
|---|---|---|
| Stage 0 deterministic two-route ADC (§3.2) | `packages/adc/rules.py` | ✅ EXACT |
| Stage 1.0 ADC dispatch task | `apps/refinery_worker/tasks/classify_action_domain.py` | ✅ EXACT |
| Stage 1 orchestration (§3.3) | `apps/refinery_worker/tasks/score_batch.py` | ✅ EXACT |
| Stage 1.1 enrichment (§3.3) | `apps/refinery_worker/tasks/enrich_prospect.py` + `packages/enrichment/{base,companies_house,linkedin_signal,web_scraper}.py` | ✅ EXACT |
| Stage 1.2 vertical classification N=3 (§3.3) | `apps/refinery_worker/tasks/classify_vertical.py` + `packages/prompts/vertical_flash.py` | ✅ EXACT |
| Stage 1.3 fitness scoring (§3.3) | `apps/refinery_worker/tasks/score_fitness.py` + `packages/scoring/{weights,fitness}.py` | ✅ EXACT |
| Stage 1.5 deterministic stub for top-12 (§3.3 v1 contribution) | `apps/refinery_worker/tasks/generate_dossier_stub.py` | ✅ EXACT |
| Stage 2 orchestrator (§3.4) | `apps/refinery_worker/tasks/generate_dossier.py` | ⚠️ PARTIAL — scaffolds taxonomy→defect→comparable→risk→approach via `send_task` chains rather than Celery `chord/group`; structurally correct, ordering simplified |
| Stage 2.1 taxonomy (§3.4) | `apps/refinery_worker/tasks/dossier_section_taxonomy.py` + `packages/prompts/taxonomy_pro.py` | ✅ EXACT |
| Stage 2.2 defect-class N=3 + conformal (§3.4) | `apps/refinery_worker/tasks/dossier_section_defect.py` + `packages/prompts/defect_flash.py` + `packages/uncertainty/conformal.py` | ⚠️ PARTIAL — DS-CP gate present but `vertical` and `signals` hardcoded as demo stubs at task entry; production pulls from `lead_prospects` row |
| Stage 2.3a deterministic comparable + 2.3b prose (§3.4 v4 contribution) | `apps/refinery_worker/tasks/dossier_section_comparable.py` + `packages/knowledge_graph/select.py` + `packages/prompts/comparable_pro.py` | ✅ EXACT |
| Stage 2.4 risk register (§3.4) | `apps/refinery_worker/tasks/dossier_section_risk.py` + `packages/prompts/risk_pro.py` | ✅ EXACT |
| Stage 2.5 approach (§3.4) | `apps/refinery_worker/tasks/dossier_section_approach.py` + `packages/prompts/approach_pro.py` | ✅ EXACT |
| Stage 2 final composition (§E.17) | `apps/refinery_worker/tasks/compose_dossier.py` | 🆕 ADDED in `93482e2` (was ❌ DEFERRED in initial build `266a3961`; QA caught the missing task referenced by `dossier_section_approach.py:46`) |
| Pydantic schemas with `extra="forbid"` (§6.2) | `packages/schemas/{lead_intake,lead_prospect,defect_hypothesis,dossier,slack_ingress,crm,drive,outbox}.py` — 28 BaseModel / 28 `extra="forbid"` | ✅ EXACT |
| FastAPI routers (§6.3) | `apps/refinery_api/routers/{ingest,slack_events,slack_interactions,crm_webhooks,crm_actions,dossier,health,websocket}.py` | ✅ EXACT |
| Knowledge Graph data + loader + selector (§6.5) | `packages/knowledge_graph/{graph.json,loader.py,select.py,evidence.py}` | ✅ EXACT (after `93482e2` citation fix — see §3(j)) |
| KG container-boot citation-provenance validator (§6.5) | `packages/knowledge_graph/verify.py` + `scripts/verify_knowledge_graph.py` CLI | ✅ EXACT |
| Mock surfaces (§6.6) | `apps/mocks/{mock_slack,mock_crm,mock_drive}/server.py` + `lead_csv_generator.py` | ✅ EXACT |
| Theater UI (§5/§6.1) | `apps/theater_ui/pages/index.tsx` + `components/{SlackLeftPane,TheaterCenterPane,DriveDossierRightPane,CRMRecordInset}.tsx` + `hooks/useWebSocket.ts` | ✅ EXACT |
| **Tightening 1** Transactional Outbox | `packages/outbox/{enqueue,dispatcher,models}.py` + same-tx writes in `compose_dossier.py` | ✅ EXACT |
| **Tightening 2** Slack distributed lock | `apps/refinery_api/routers/slack_events.py` SET NX EX 60s + `apps/refinery_worker/tasks/release_slack_lock.py` | ✅ EXACT |
| **Tightening 3** byte-density validator | `packages/schemas/dossier.py` `PreVisitDossier._recompute_and_enforce_deterministic_byte_ratio` with `object.__setattr__` overwrite | ✅ EXACT |
| **Tightening 4** section-granular DS-CP | `packages/uncertainty/dscp.py` + `PreVisitDossier.unverified_sections` + DS-CP gate in `dossier_section_defect.py` | ✅ EXACT |
| **Tightening 5** deployment topology diagram | `ULTIMATE_PRD.md §3.1.5` Mermaid | ✅ EXACT (doc-only by design) |
| Conformal calibration build script (§3.4 / §H) | `packages/uncertainty/{conformal,dscp}.py` + `packages/uncertainty/calibration_table.json` + `scripts/build_calibration_table.py` | ✅ EXACT |
| Tests criterion 12/13/14/15 (§N) | `tests/unit/{test_byte_density_validator,test_slack_distributed_lock,test_knowledge_graph_validator,test_dscp_section_strip}.py` | 🆕 REWRITTEN in `93482e2` (initial build shipped trivially-passing stubs that didn't exercise the validators) |
| Test infrastructure | `tests/conftest.py` | 🆕 ADDED in `93482e2` (env-var seed for Pydantic Settings load) |
| Integration tests (§N) | `tests/integration/{test_csv_to_stub_pipeline,test_slack_click_to_dossier_pipeline,test_outbox_relay_and_dlq}.py` | ❌ DEFERRED — 2-line stubs only; full end-to-end coverage is Phase 1.5 |
| Alembic migrations | `migrations/versions/0001_initial.py` (referenced in `PHASE_1_SPEC §B`) | ❌ DEFERRED — no migrations directory in shipped tree; SQL DDL is inlined in task code via `text(...)` raw SQL |

## §3 Architectural Drift

| Invariant | PRD requirement | Implementation | Verdict |
|---|---|---|---|
| (a) ADC purity | Zero LLM calls in `packages/adc/` | `grep -rn 'genai\|gemini' packages/adc/` → 0 hits | ✅ intact |
| (b) DMZ rule | No SENTRY/TALLY/GAUGE/TRACE/MFM/MOS/edge-firmware references | grep across `packages/` + `apps/` → 0 hits | ✅ intact |
| (c) Anti-replication | No real camera streams / MFM inference / closed-loop control | No imports of vision libs; LLM calls bounded to schema-constrained prose | ✅ intact |
| (d) Model routing | Vertex AI europe-west4 + `gemini-3-flash-preview` / `gemini-3.1-pro-preview` exclusively | All 12 model-string references match; `genai.Client(vertexai=True, location=settings.vertex_location)`; no Anthropic/OpenAI/Bedrock in `pyproject.toml` | ✅ intact |
| (e) `extra="forbid"` boundaries | All BaseModel classes lock | 28/28 match | ✅ intact |
| (f) N=3 ensemble pattern | `thinking_level="minimal"`, temps `(0.1, 0.5, 0.9)` | `vertical_flash.py` + `defect_flash.py` declare `TEMPS = (0.1, 0.5, 0.9)`; `classify_vertical.py` and `dossier_section_defect.py` use them | ✅ intact |
| (g) Tightening 3 Goodhart-resistance | `object.__setattr__` to overwrite caller-provided ratio | `packages/schemas/dossier.py:149`: `object.__setattr__(self, "deterministic_section_ratio", recomputed)` — recompute-from-bytes pattern present, NOT a caller-trusted check | ✅ intact |
| (h) Tightening 1 same-tx outbox | Dossier write + outbox row writes in ONE Postgres tx | `compose_dossier.py` wraps both `UPDATE dossier_artifacts` and 3× `INSERT INTO outbox` inside one `with engine.begin() as conn:` block | ✅ intact |
| (i) Vestigial naming purge (`cmms_outbox_dlq` → `outbox_dlq`) | 0 `cmms_*` identifiers anywhere | `grep -ri cmms packages/ apps/ migrations/ scripts/ tests/` → 0 hits | ✅ intact |
| (j) Cummins KG exclusion | Not present as deployment anchor | `grep -i cummins packages/knowledge_graph/graph.json` → 0 hits | ✅ intact |

**No load-bearing drift.** The two ⚠️ PARTIAL items in §2 (Stage 2 orchestrator simplification + `dossier_section_defect.py` hardcoded demo signals) are engineering-only; they do not violate any invariant. The real production gap is end-to-end integration: structurally complete, not yet integration-tested.

## §4 Bottleneck Thesis Check

**(a) Are the two Magic Moments still present?** PRD §6.8 specs Magic Moment 1 (T+8 Stage 1 batch scoring across 124 prospects → Slack canvas + CRM fields + Drive priority-index materializing simultaneously) and Magic Moment 2 (T+88 full dossier across the same three surfaces). **Structural answer: yes.** The 16 Celery tasks in `apps/refinery_worker/tasks/`, the three mock surface adapters in `apps/mocks/`, and the four Theater UI components in `apps/theater_ui/components/` are all in the shipped tree. **Honest gap: end-to-end timing under `docker compose up` has not been executed against the full pipeline.** T+8 / T+88 are structurally feasible per `PHASE_1_SPEC.md §M` but not yet verified. ⚠️ partial.

**(b) Is the load-bearing thesis intact?** Thesis (from `ULTIMATE_PRD.md §2`): *"The Refinery absorbs the slice of FDE / Doug / Special Projects load that lives between the trade-show floor and the factory visit, with calibrated uncertainty surfacing where Doug's published methodology expects it and structurally bounded LLM action elsewhere."* **Verdict: ⚠️ PARTIAL.** Every structural element required to support the thesis is present in the shipped tree (the §3 invariants check confirms 10/10 intact). The thesis is not fully demonstrable in a recording until Phase 1.5 integration debug confirms the Magic Moment timings hold under `docker compose up trigger=william_cook_sheffield`.

**(c) What evidence the build solves the bottleneck would survive Doug or Damjan's scrutiny?** Named artifacts:
1. **28/28 `extra="forbid"` declarations in `packages/schemas/`.** Damjan-readiness anchor; verifiable by `grep -c`.
2. **`apps/refinery_worker/tasks/compose_dossier.py` (added `93482e2`).** The single integration point where all three tightenings cross: constructs `PreVisitDossier` (Tightening 3 byte-density validator fires), retains `unverified_sections` (Tightening 4), writes 1 dossier row + 3 outbox envelopes in one Postgres transaction (Tightening 1).
3. **`packages/knowledge_graph/verify.py` + the `93482e2` citation fix.** Production container boot fails on any citation-provenance mismatch — the fact that 3B QA caught a real `bowers_and_wilkins`/`caracol_am` data bug at build time before deployment is itself the Damjan-readiness signal: the spec's validator catches what the spec's prose didn't.

## §5 Handoff to Post-Reconciliation Actions

- **❌ DEFERRED — Alembic migrations.** Flag in `MATTA_DEMO_BRIEFING.md §8` as a known gap; not blocking the demo because the docker-compose Postgres can boot with the inline `text(...)` DDL bootstrap path. Address in Phase 1.5.
- **❌ DEFERRED — Integration tests (3 stub files in `tests/integration/`).** Replace with real end-to-end coverage during Phase 1.5 integration debug. Not blocking the recording, but covering them strengthens the cold-email-time Damjan-readiness signal.
- **⚠️ PARTIAL — Stage 2 orchestrator uses `send_task` chains rather than Celery `chord/group`.** Engineering-only; does not need amendment in `MATTA_DEMO_BRIEFING.md §4` architecture explanation.
- **⚠️ PARTIAL — `dossier_section_defect.py` hardcodes demo `vertical` and `signals`.** Engineering-only; flag in §8 of the briefing as a Phase 1.5 fix.
- **🆕 ADDED — `compose_dossier.py` and the four real tests.** Worth one sentence in `MATTA_DEMO_BRIEFING.md §4` describing the same-tx commit pattern and the Goodhart-resistance validator — these are the strongest Damjan-readiness signals in the build.
- **§4(b) verdict ⚠️ PARTIAL → STOP recommendation:** **Do NOT proceed to demo recording until a Phase 1.5 end-to-end dry-run against `docker compose up` confirms Magic Moment 1 (T+8) and Magic Moment 2 (T+88) timings hold.** The demo cannot demonstrate a thesis that the integration timing hasn't verified.

---

*End of MATTA_RECONCILIATION.md.*

## §6 Model-String Adjustment (Phase 1.5)

**Adjustment date:** 2026-05-12

### §6.1 Decision

The locked invariant in `ULTIMATE_PRD.md §0` originally pinned model strings to `gemini-3-flash-preview` (Flash tier, N=3 ensemble) and `gemini-3.1-pro-preview` (Pro tier, single call) on Vertex AI europe-west4. During Phase 1.5 integration debug, Vertex AI access to the `gemini-3-*` family was confirmed unavailable to the project `kaide-ai-84019` at any region. Inference calls return HTTP 404 NOT_FOUND for `gemini-3-flash-preview` in both `europe-west4` and `us-central1`, and for `gemini-3.1-flash-lite-preview` in `europe-west4`. The model-family appears to be behind a project enrollment gate that Kaide Labs is not currently on.

The Architect authorized a lateral step within the Gemini family from `gemini-3-*` (preview) to `gemini-2.5-*` (GA) for Phase 1.5. Effective swap:
- Flash tier (N=3 ensemble): `gemini-3-flash-preview` → `gemini-2.5-flash`
- Pro tier (single call): `gemini-3.1-pro-preview` → `gemini-2.5-pro`

### §6.2 What Did NOT Change

Every other architectural invariant remains intact:
- Vertex AI fabric pin (NOT Generative Language API at `generativelanguage.googleapis.com`)
- europe-west4 region pin
- ADC-based authentication (NOT API key)
- N=3 deep ensemble pattern with `thinking_level="minimal"` and temperatures (0.1, 0.5, 0.9)
- Pydantic `extra="forbid"` on all 28 BaseModel boundaries
- Deterministic two-route ADC with zero LLM imports in any router
- All 5 1F-red v3 tightenings (transactional outbox, Slack distributed lock, byte-density validator ≥0.60, section-granular DS-CP, deployment topology diagram)

### §6.3 Methodology Anchoring Unchanged

The Doug Brion methodology lineage (deep ensembles per `pytorch-deep-ensembles`, conformal coverage, confidence-informed self-consistency) is generation-agnostic — it depends on the ensemble + uncertainty pattern, not on a specific Gemini generation. The Damjan-absorbable stack story is unchanged. The Pattinson Filter (EU data residency, deterministic governance, structured output bounds) holds — `gemini-2.5-*` on Vertex europe-west4 satisfies all three.

### §6.4 What Audit-Trail Docs Show vs Runtime Code

By design, the following audit-trail documents retain the *original* `gemini-3-*` pin as the historically-locked architectural decision:
- `ULTIMATE_PRD.md §0` (original pin)
- `PHASE_1_SPEC.md` (build-time spec)
- `validation_gate_1f_red_v3.md` (1F-red counter-verdict)
- `MATTA_COMPREHENSION.md §4` (architectural lineage)

The runtime code under `packages/` and `apps/` now references `gemini-2.5-*`. This is the standard pattern: architecture-of-record documents the locked decision at the time it was made; reconciliation §6 documents the runtime adjustment; the two together form the complete audit trail.

### §6.5 Damjan- or Doug-Facing Justification (Reusable)

If asked by Doug, Damjan, or any technical reviewer why the build runs Gemini 2.5 rather than Gemini 3:

> "We pinned to Gemini 3 in the architectural spec. During Phase 1.5 integration debug we discovered the Gemini 3 family is currently gated behind a Google preview-access program we're not enrolled in. Rather than block the demo on an indefinite allowlist wait, we stepped laterally to Gemini 2.5 — same Vertex europe-west4 fabric, same ensemble pattern, same conformal calibration, same deterministic safety rails. The architecture is generation-agnostic. When the Gemini 3 family becomes available to the production project, the swap is a single sed across `packages/` and `apps/` (see MATTA_RECONCILIATION.md §6 for the exact pattern)."

### §6.6 Re-verification

After the swap, smoke-test verification per `PHASE_1_5_DEBUG_SPEC.md §H` must run three consecutive passes against the `gemini-2.5-*` runtime. If it passes, §4(b) verdict (currently ⚠️ PARTIAL pending Phase 1.5) advances to ✅ INTEGRATION-VERIFIED with the §6 adjustment recorded.
