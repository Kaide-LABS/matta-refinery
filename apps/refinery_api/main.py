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
