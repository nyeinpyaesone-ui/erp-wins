"""
ERP Platform — Test Configuration

Shared fixtures for all test suites.
"""

import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.config import Settings
from app.main import create_app


# Use a separate event loop for async tests
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Test settings with safe defaults."""
    import os
    os.environ.setdefault("APP_SECRET_KEY", "test-secret-key-for-testing-minimum-32-chars!!")
    os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://erp:test@localhost:5432/erp_test")
    os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
    os.environ.setdefault("CELERY_BROKER_URL", "redis://localhost:6379/1")
    os.environ.setdefault("CELERY_RESULT_BACKEND", "redis://localhost:6379/2")
    
    from app.config import get_settings
    # Clear cache to pick up test env
    get_settings.cache_clear()
    return get_settings()


@pytest_asyncio.fixture
async def app():
    """Create a test FastAPI application."""
    test_app = create_app()
    yield test_app


@pytest_asyncio.fixture
async def client(app) -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
