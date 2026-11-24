"""
ERP Platform — SQLAlchemy Async Database Engine

PostgreSQL is the authoritative source of business state.
Connection pools are explicitly bounded.
"""

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_settings


def create_database_engine() -> AsyncEngine:
    """
    Create async SQLAlchemy engine with bounded connection pool.
    
    Rules:
    - Pool size configured according to actual workload
    - Pool timeout prevents indefinite waiting
    - Pool recycle prevents stale connections
    """
    settings = get_settings()

    engine = create_async_engine(
        str(settings.database_url),
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow,
        pool_timeout=settings.db_pool_timeout,
        pool_recycle=settings.db_pool_recycle,
        pool_pre_ping=True,  # Verify connections before use
        echo=settings.app_debug,  # SQL logging in debug mode
    )

    return engine


# Global engine instance (initialized in lifespan)
_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    """Get the global database engine."""
    if _engine is None:
        raise RuntimeError("Database engine not initialized. Call init_database() first.")
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Get the global session factory."""
    if _session_factory is None:
        raise RuntimeError("Session factory not initialized. Call init_database() first.")
    return _session_factory


async def init_database() -> None:
    """Initialize database engine and session factory."""
    global _engine, _session_factory

    _engine = create_database_engine()
    _session_factory = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def close_database() -> None:
    """Close database engine and release connections."""
    global _engine, _session_factory

    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _session_factory = None


async def get_db_session() -> AsyncSession:
    """
    Dependency: yield a database session for request scope.
    
    Rules:
    - Release connections promptly
    - Never hold connections while waiting on external services
    """
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
