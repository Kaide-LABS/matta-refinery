# Matta Refinery

FDE-built sidecar that ranks trade-show leads against Matta's deployment
knowledge anchors, then composes pre-visit dossiers for the top-12 with
ensemble-agreement uncertainty gating.

Built by Kaide Labs. Phase 1.7 demo build for Matta.

## What this is

A stateless API sidecar + Celery worker on FastAPI + SQLAlchemy +
Postgres + Redis. Two stages:

**Stage 1: Vertical classification + fitness scoring**
- N=3 Gemini Flash temperature-varied ensemble for vertical
  classification (temps 0.1/0.5/0.9).
- Deterministic fitness scoring against calibrated per-vertical weights
  (`packages/scoring/fitness.py`).
- ~5 minutes for a 65-lead cohort.

**Stage 2: 5-section dossier composition**
- §1 Process Taxonomy — Gemini Pro 2.5.
- §2 Defect Hypothesis — Gemini Flash N=3 ensemble with
  **ensemble-agreement gating** (per-class threshold tuning,
  per-class agreement thresholds in
  `packages/uncertainty/calibration_table.json`).
- §3 Comparable Matta Deployment — Gemini Pro against a KG-anchored
  customer reference. Anchor selection is deterministic; the LLM only
  writes prose.
- §4 Integration Risk Register — Gemini Pro against KG-anchored risk
  pillars.
- §5 Suggested Approach — Gemini Pro filling a hardcoded phase
  template.

## What this isn't

- **Not split-conformal prediction.** The agreement-set gating is
  vote-share thresholding with per-class hand-tuned thresholds. There
  is no nonconformity score and no marginal coverage guarantee
  (Vovk/Shafer). See `packages/uncertainty/agreement.py` and the
  forthcoming `docs/CALIBRATION.md` for methodology and limitations.
- **Not a deep ensemble** in Brion et al.'s sense. Three calls to one
  Gemini Flash model at different temperatures is temperature-varied
  LLM sampling, not independently initialized networks.
- **Not a true knowledge graph.** `packages/knowledge_graph/graph.json`
  is a verified citation table — flat list of anchors with
  container-boot quote pinning against `Matta_Intel_cleaned.md`. No
  entities, relations, or traversal. The "Knowledge Graph" framing is
  kept in UI labels for architectural continuity with other
  substrate-pinned LLM output constraints, but the popover footer
  notes this explicitly.
- **Not production-hardened.** This is a Phase 1.7 demo build. Stage 2
  engagement deliverables include full test coverage, wired-up alembic
  migrations, multi-replica safety review, structured observability.

## Run locally

```bash
docker compose up -d
# Wait ~6 minutes for pre-bake to complete
curl http://localhost:8080/api/batch/prebaked   # poll until status=complete
open http://localhost:3000/sandbox?mode=quickdemo
```

Health endpoints:
- `GET /healthz` — liveness only, always 200 if the process is up.
- `GET /readyz` — readiness; pings Postgres + Redis, returns 503 if
  either is unreachable.

## Architecture principles

1. **Stateless sidecar** — no in-process state beyond connection
   pools. Postgres + Redis are the only persistence. Restart-safe.
2. **Anti-replication** — never duplicates what Matta's internal team
   is already building. Operates upstream (ingest) and downstream
   (briefing). The product is the workflow seam, not the inspection
   model.
3. **Native surfaces** — outputs land in Slack, HubSpot (mock for
   demo), and Drive (mock). The team never leaves their tools.
4. **Substrate-pinned citations** — every KG anchor's quote is
   verified at container boot against `docs/Matta_Intel_cleaned.md`
   line numbers (`packages/knowledge_graph/verify.py`,
   `validate_graph_or_die`). If any quote drifts, the container
   refuses to start.
5. **Magic Moment** — full ingest-to-briefing in ~85 seconds for the
   rank-1 prospect via `/sandbox?mode=quickdemo`.

## Methodology disclosure

This codebase uses statistical mechanisms but does not claim their
published formal guarantees:

- **Ensemble agreement gating** (`packages/uncertainty/agreement.py`):
  vote-share thresholding with per-class calibrated thresholds. Not
  split-conformal prediction.
- **Temperature-varied ensemble** (`apps/refinery_worker/tasks/
  dossier_section_defect.py`): N=3 Gemini Flash samples at
  temperatures 0.1 / 0.5 / 0.9. Not a deep ensemble in Brion et al.'s
  independent-initialization sense.
- **Verified citation table** (`packages/knowledge_graph/`): branded
  "Knowledge Graph" in UI for familiarity; structurally a flat anchor
  table with container-boot quote verification.

## Tech stack

- Python 3.12, FastAPI, SQLAlchemy (async), Celery, Pydantic v2
  (extra="forbid" at all 35 boundaries).
- Gemini 2.5 (Pro + Flash) via Vertex AI europe-west4.
- Postgres 16, Redis 7.
- Next.js 14 + TypeScript for the theater UI.
- Docker Compose for local; Cloud Run for production (Stage G).

## Migrations (deferred)

`alembic.ini` is present and `migrations/versions/*.py` files exist,
but `migrations/env.py` is not wired and the API still relies on
`Base.metadata.create_all` at lifespan startup. Wiring alembic
end-to-end is a Stage G deliverable — running `alembic upgrade head`
in the API entrypoint requires verifying autogenerate against the
live schema (custom ENUMs, `pgcrypto` extension), which can't be done
without a deploy-time Postgres pass.

## Background

See `docs/MATTA_MASTER_PRD_v2.md` for the architectural rationale,
`docs/Matta_Intel_cleaned.md` for the verified-quote substrate, and
the audit history in `docs/Brief_Audit.md` and
`docs/Matta_Architecture_Forensic_Audit.md`.

## License

Proprietary. © 2026 Kaide Labs.
