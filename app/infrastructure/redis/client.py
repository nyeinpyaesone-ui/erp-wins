"""
ERP Platform — Redis Client

Redis provides: Celery broker, cache, rate limiting, short-lived coordination.
Redis must NEVER be authoritative for business state.
"""

from redis.asyncio import Redis

from app.config import get_settings


_redis_client: Redis | None = None


async def init_redis() -> None:
    """Initialize Redis client."""
    global _redis_client

    settings = get_settings()
    _redis_client = Redis.from_url(
        str(settings.redis_url),
        decode_responses=True,
        socket_timeout=5,
        socket_connect_timeout=5,
        retry_on_timeout=True,
    )

    # Verify connection
    await _redis_client.ping()


async def close_redis() -> None:
    """Close Redis client."""
    global _redis_client

    if _redis_client is not None:
        await _redis_client.close()
        _redis_client = None


def get_redis() -> Redis:
    """Get the global Redis client."""
    if _redis_client is None:
        raise RuntimeError("Redis not initialized. Call init_redis() first.")
    return _redis_client
