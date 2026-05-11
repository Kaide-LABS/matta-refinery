from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import redis.asyncio as aioredis
from ..config import settings
import asyncio

router = APIRouter()

@router.websocket("/ws/theater/{batch_id}")
async def websocket_endpoint(websocket: WebSocket, batch_id: str):
    await websocket.accept()
    redis = aioredis.from_url(settings.redis_url)
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"theater:{batch_id}")
    
    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message:
                await websocket.send_text(message["data"].decode("utf-8"))
            else:
                await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        await pubsub.unsubscribe(f"theater:{batch_id}")
        await redis.aclose()
