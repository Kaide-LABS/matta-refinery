from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as aioredis
from celery import Celery
from google import genai
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .config import settings

from .routers import ingest, slack_events, slack_interactions, crm_webhooks, crm_actions, dossier, health, websocket, batch
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
