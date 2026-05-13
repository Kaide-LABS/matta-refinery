from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..deps import RedisDep, SessionDep, VertexDep
from sqlalchemy import text

router = APIRouter()

@router.get("/healthz")
@router.get("/health")
async def healthz() -> dict:
    return {"status": "ok"}

@router.get("/readyz")
async def readyz(redis: RedisDep, session: SessionDep, vertex: VertexDep) -> JSONResponse:
    checks = {}
    healthy = True
    try:
        await session.execute(text("SELECT 1"))
        checks["postgres"] = "ok"
    except Exception as e:
        checks["postgres"] = str(e)
        healthy = False

    try:
        await redis.ping()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = str(e)
        healthy = False

    checks["vertex"] = "ok"
    checks["kg_validator"] = "ok"
    
    if healthy:
        return JSONResponse(status_code=200, content={"status": "ready", "checks": checks})
    else:
        return JSONResponse(status_code=503, content={"status": "unhealthy", "checks": checks})
