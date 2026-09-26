"""
ERP Platform — Health Check Endpoints

Implements:
- GET /health/live — process is functioning
- GET /health/ready — required runtime dependencies are available
- GET /health/startup — initialization has completed successfully

Health responses must not expose secrets or sensitive infrastructure information.
"""

from fastapi import APIRouter, FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.infrastructure.database.engine import get_engine
from app.infrastructure.redis.client import get_redis

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live", summary="Liveness probe")
async def health_live() -> dict[str, str]:
    """
    Liveness probe: process is functioning.
    
    Returns 200 if the process is alive and responding.
    Does not check external dependencies.
    """
    return {"status": "live"}


@router.get("/ready", summary="Readiness probe")
async def health_ready() -> JSONResponse:
    """
    Readiness probe: required runtime dependencies are available.
    
    Checks:
    - Database connectivity
    - Redis connectivity
    
    Returns 200 if all dependencies are available, 503 otherwise.
    """
    checks = {}
    all_healthy = True
    
    # Check database
    try:
        engine = get_engine()
        async with engine.connect() as conn:
            await conn.execute(
                __import__("sqlalchemy").text("SELECT 1")
            )
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"
        all_healthy = False
    
    # Check Redis
    try:
        redis = get_redis()
        await redis.ping()
        checks["redis"] = "healthy"
    except Exception as e:
        checks["redis"] = f"unhealthy: {str(e)}"
        all_healthy = False
    
    status_code = status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "ready" if all_healthy else "not_ready",
            "checks": checks,
        },
    )


@router.get("/startup", summary="Startup probe")
async def health_startup(request: Request) -> JSONResponse:
    """
    Startup probe: initialization has completed successfully.
    
    Returns 200 if startup is complete, 503 otherwise.
    """
    startup_complete = getattr(request.app.state, "startup_complete", False)
    
    status_code = status.HTTP_200_OK if startup_complete else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "started" if startup_complete else "starting",
        },
    )
