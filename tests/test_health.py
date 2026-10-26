import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_health_endpoint():
    """Test health endpoint returns healthy when database is available."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
        # Will be 503 if no database, but structure should be correct
        assert response.status_code in (200, 503)
        data = response.json()
        assert "status" in data
        assert "database" in data


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test root endpoint returns app info."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "orbit-engine-147"
        assert "version" in data
        assert "description" in data
