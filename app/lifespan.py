"""
ERP Platform — Application Lifespan

Manages startup and shutdown of infrastructure dependencies.
Startup ordering must not be confused with readiness.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.config import get_settings
from app.infrastructure.database.engine import close_database, init_database
from app.infrastructure.redis.client import close_redis, init_redis

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan context manager.
    
    Startup sequence:
    1. Validate configuration
    2. Initialize database
    3. Initialize Redis
    4. Mark startup as complete
    
    Shutdown sequence:
    1. Close Redis
    2. Close database
    """
    settings = get_settings()
    
    # -------------------------------------------------------------------------
    # Startup
    # -------------------------------------------------------------------------
    logger.info(f"Starting {settings.app_name} in {settings.app_env} mode")
    
    try:
        # Initialize database
        logger.info("Initializing database connection pool...")
        await init_database()
        logger.info("Database initialized successfully")
        
        # Initialize Redis
        logger.info("Initializing Redis connection...")
        await init_redis()
        logger.info("Redis initialized successfully")
        
        # Mark startup as complete
        app.state.startup_complete = True
        logger.info("Application startup complete")
        
        yield
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        # Cleanup on failure
        await _cleanup()
        raise
    
    # -------------------------------------------------------------------------
    # Shutdown
    # -------------------------------------------------------------------------
    logger.info("Shutting down application...")
    await _cleanup()
    logger.info("Shutdown complete")


async def _cleanup() -> None:
    """Cleanup infrastructure dependencies."""
    try:
        await close_redis()
    except Exception as e:
        logger.error(f"Error closing Redis: {e}")
    
    try:
        await close_database()
    except Exception as e:
        logger.error(f"Error closing database: {e}")
