from contextlib import asynccontextmanager
from fastapi import FastAPI
import redis.asyncio as aioredis
from celery import Celery
from google import genai
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .config import settings

from .routers import ingest, slack_events, slack_interactions, crm_webhooks, crm_actions, dossier, health, websocket
from packages.knowledge_graph.verify import validate_graph_or_die

@asynccontextmanager
async def lifespan(app: FastAPI):
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

app.include_router(ingest.router)
app.include_router(slack_events.router)
app.include_router(slack_interactions.router)
app.include_router(crm_webhooks.router)
app.include_router(crm_actions.router)
app.include_router(dossier.router)
app.include_router(health.router)
app.include_router(websocket.router)
