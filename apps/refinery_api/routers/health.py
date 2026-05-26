from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text

from ..deps import RedisDep, SessionDep

router = APIRouter()


@router.get("/healthz")
@router.get("/health")
async def healthz() -> dict:
    """Liveness probe — the process is up. Used by Cloud Run / k8s.

    Stage E audit note: this endpoint returns {"status": "ok"}
    unconditionally and that is intentional. Liveness probes must NOT
    flap on transient downstream failures (DB blip, Redis blip), or
    k8s will kill an otherwise healthy process and restart it,
    making the outage worse. Dependency reachability is checked by
    /readyz, which is what readiness probes should hit.
    """
    return {"status": "ok"}


@router.get("/readyz")
async def readyz(redis: RedisDep, session: SessionDep) -> JSONResponse:
    """Readiness probe — the process can serve traffic.

    Pings Postgres + Redis. Returns 503 if either is unreachable.
    Cloud Run / k8s readiness probes should hit this endpoint.
    """
    checks: dict[str, str] = {}
    healthy = True

    try:
        await session.execute(text("SELECT 1"))
        checks["postgres"] = "ok"
    except Exception as e:
        checks["postgres"] = f"fail: {type(e).__name__}"
        healthy = False

    try:
        await redis.ping()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"fail: {type(e).__name__}"
        healthy = False

    # Vertex + KG validator are static configuration that's verified at
    # boot (validate_graph_or_die in lifespan); no runtime ping here —
    # readiness should reflect runtime traffic-serving capability.
    checks["vertex"] = "ok"
    checks["kg_validator"] = "ok"

    if healthy:
        return JSONResponse(
            status_code=200,
            content={"status": "ready", "checks": checks},
        )
    return JSONResponse(
        status_code=503,
        content={"status": "unhealthy", "checks": checks},
    )
