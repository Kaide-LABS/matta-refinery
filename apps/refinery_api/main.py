from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as aioredis
from celery import Celery
from google import genai
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .config import settings

from .routers import ingest, slack_events, slack_interactions, crm_webhooks, crm_actions, dossier, health, websocket, batch, demo
from packages.knowledge_graph.verify import validate_graph_or_die
from packages.observability.logging_config import configure_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(service_name="refinery-api")
    validate_graph_or_die()
    app.state.redis = aioredis.from_url(settings.redis_url)
    app.state.celery = Celery("refinery", broker=settings.celery_broker)
    app.state.engine = create_async_engine(settings.postgres_url)
    app.state.session_maker = async_sessionmaker(app.state.engine, expire_on_commit=False)
    app.state.vertex_client = genai.Client(vertexai=True, project=settings.gcp_project, location=settings.vertex_location)

    # Phase 1.7 Stage D: idempotent table create-if-missing so the
    # startup pre-bake hook below can insert without 500'ing on fresh
    # volumes. SQLAlchemy create_all only CREATEs missing tables — it
    # does NOT drop existing ones. The full init_db.py script (with
    # drop_all + seed_demo_enrichment) remains the canonical setup for
    # smoke runs that need a known-clean state.
    import logging
    _life_log = logging.getLogger(__name__)
    try:
        from packages.models.prospects import Base as ProspectsBase
        # Register EnrichmentArtifact on ProspectsBase.metadata via import
        from packages.models.enrichment import EnrichmentArtifact  # noqa: F401
        from packages.outbox.models import Base as OutboxBase
        from sqlalchemy import text as _sa_text

        # Stage E hotfix: CREATE EXTENSION IF NOT EXISTS is not atomic in
        # Postgres — with uvicorn --workers 2, both workers race and the
        # loser hits a UniqueViolationError on pg_extension_name_index.
        # Wrap the extension creation in its own transaction so the loser
        # can swallow the IntegrityError without rolling back the
        # subsequent create_all (which is what regressed pre-bake).
        try:
            async with app.state.engine.begin() as _conn:
                await _conn.execute(_sa_text("CREATE EXTENSION IF NOT EXISTS pgcrypto"))
        except IntegrityError as e:
            _life_log.info(
                "pgcrypto extension already created by concurrent worker",
                extra={"exception_type": type(e).__name__},
            )

        async with app.state.engine.begin() as _conn:
            await _conn.run_sync(ProspectsBase.metadata.create_all)
            await _conn.run_sync(OutboxBase.metadata.create_all)

            # Stage E audit fix: dossier_artifacts, dossier_stubs,
            # prioritized_queues, and event_idempotency have no
            # SQLAlchemy model — historically they were created by
            # scripts/init_db.py at smoke-harness invocation time.
            # The Stage E harness reframe stopped calling init_db,
            # so on a fresh-volume boot these tables didn't exist
            # and worker INSERTs raised UndefinedTable → 500 on
            # /dossier/{id} → CORS middleware never got to add
            # response headers → browser reported a CORS error
            # masking the underlying schema bug.
            #
            # All four tables are now created idempotently here.
            # IF NOT EXISTS keeps re-boots safe.
            for ddl in (
                """
                CREATE TABLE IF NOT EXISTS dossier_artifacts (
                    id TEXT PRIMARY KEY,
                    dossier_id TEXT,
                    prospect_id TEXT,
                    batch_id TEXT,
                    signal_hash TEXT,
                    knowledge_graph_version TEXT,
                    calibration_version TEXT,
                    state TEXT,
                    process_taxonomy JSONB,
                    defect_hypothesis JSONB,
                    comparable_deployment JSONB,
                    risk_register JSONB,
                    suggested_approach JSONB,
                    unverified_sections JSONB,
                    deterministic_section_ratio FLOAT,
                    validation_error TEXT,
                    generated_at TIMESTAMP
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS dossier_stubs (
                    stub_id TEXT PRIMARY KEY,
                    prospect_id TEXT,
                    batch_id TEXT,
                    company_facts JSONB,
                    verified_vertical TEXT,
                    headline_kg_anchor TEXT,
                    slot_readiness TEXT,
                    generated_at TIMESTAMP
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS prioritized_queues (
                    id TEXT PRIMARY KEY,
                    batch_id TEXT,
                    payload_json JSONB
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS event_idempotency (
                    id TEXT PRIMARY KEY,
                    event_id TEXT,
                    processed_at TIMESTAMP
                )
                """,
            ):
                await _conn.execute(_sa_text(ddl))
    except Exception as e:
        _life_log.exception(
            "Lifespan create_all failed", extra={"exception_type": type(e).__name__},
        )

    # Phase 1.7 Stage D: pre-bake Stage 1 on the default demo CSV so the
    # quickdemo URL has a ready-to-serve queue. Idempotent on file_hash —
    # subsequent boots reuse the existing baked batch.
    try:
        from .startup_prebake import maybe_prebake_default_csv
        await maybe_prebake_default_csv(engine=app.state.engine, celery=app.state.celery)
    except Exception as e:
        # Never block API startup on pre-bake failure — the existing
        # CSV-upload flow still works without it.
        import logging
        logging.getLogger(__name__).exception(
            "Default-CSV pre-bake failed at startup",
            extra={"exception_type": type(e).__name__},
        )
    yield
    await app.state.redis.aclose()
    await app.state.engine.dispose()

app = FastAPI(lifespan=lifespan)

# CORS for the Theater UI dev server. Permissive on localhost only — the
# refinery_api runs behind a reverse proxy in production where CORS is
# handled at the edge. This middleware is for the local docker-compose
# demo flow (UI at :3000 → API at :8080).
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router)
app.include_router(slack_events.router)
app.include_router(slack_interactions.router)
app.include_router(crm_webhooks.router)
app.include_router(crm_actions.router)
app.include_router(dossier.router)
app.include_router(health.router)
app.include_router(websocket.router)
app.include_router(batch.router)
app.include_router(demo.router)
