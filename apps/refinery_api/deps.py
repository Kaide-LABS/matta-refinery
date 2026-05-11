from typing import Annotated
from fastapi import Depends, Request
from redis.asyncio import Redis
from celery import Celery
from sqlalchemy.ext.asyncio import AsyncSession
from google import genai

async def get_redis(request: Request) -> Redis:
    return request.app.state.redis

async def get_celery(request: Request) -> Celery:
    return request.app.state.celery

async def get_session(request: Request) -> AsyncSession:
    async with request.app.state.session_maker() as session:
        yield session

async def get_vertex(request: Request) -> genai.Client:
    return request.app.state.vertex_client

class User:
    id: str = "demo_user"

async def get_current_user(request: Request) -> User:
    return User()

RedisDep = Annotated[Redis, Depends(get_redis)]
CeleryDep = Annotated[Celery, Depends(get_celery)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]
VertexDep = Annotated[genai.Client, Depends(get_vertex)]
UserDep = Annotated[User, Depends(get_current_user)]
