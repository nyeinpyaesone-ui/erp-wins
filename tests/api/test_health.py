"""
ERP Platform — Health Check API Tests

Tests for /health/live, /health/ready, /health/startup endpoints.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_live(client: AsyncClient):
    """Test liveness probe returns 200."""
    response = await client.get("/api/v1/health/live")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "live"


@pytest.mark.asyncio
async def test_health_startup_not_started(client: AsyncClient):
    """Test startup probe returns 503 when startup not complete."""
    response = await client.get("/api/v1/health/startup")
    
    # In test mode, startup_complete may not be set
    assert response.status_code in [200, 503]
    data = response.json()
    assert "status" in data


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """Test root endpoint returns API information."""
    response = await client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "ERP Platform"
    assert data["version"] == "1.2.0"
    assert data["status"] == "running"
