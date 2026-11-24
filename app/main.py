"""
ERP Platform — FastAPI Application

Main application factory with middleware, CORS, and routing.
"""

import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.api.websocket import router as websocket_router
from app.config import get_settings
from app.lifespan import lifespan

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Configuration is validated once during startup.
    """
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        version="1.2.0",
        description="Production-oriented modular business platform",
        docs_url="/docs" if settings.app_debug else None,
        redoc_url="/redoc" if settings.app_debug else None,
        lifespan=lifespan,
    )
    
    # -------------------------------------------------------------------------
    # Middleware
    # -------------------------------------------------------------------------
    
    # CORS
    if settings.api_cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.api_cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    # -------------------------------------------------------------------------
    # Routers
    # -------------------------------------------------------------------------
    app.include_router(api_router, prefix="/api/v1")
    app.include_router(websocket_router)
    
    # -------------------------------------------------------------------------
    # Root endpoint
    # -------------------------------------------------------------------------
    @app.get("/", tags=["root"])
    async def root() -> dict[str, str]:
        """Root endpoint — API information."""
        return {
            "name": settings.app_name,
            "version": "1.2.0",
            "status": "running",
            "docs": "/docs" if settings.app_debug else "disabled",
        }
    
    logger.info(f"FastAPI application created: {settings.app_name}")
    
    return app


# Application instance
app = create_app()
