"""Tests for storage assets module with CORS fix (issue #37312)."""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.storage import get_test_router, get_cors_headers


@pytest.mark.asyncio
async def test_cors_headers_no_credentials():
    """Test that CORS headers have Allow-Credentials: false to prevent __cf_bm cookie issue."""
    headers = get_cors_headers("https://example.com")
    assert headers["Access-Control-Allow-Credentials"] == "false"
    assert headers["Access-Control-Allow-Origin"] == "https://example.com"
    assert "Vary" in headers
    assert headers["Vary"] == "Origin"


@pytest.mark.asyncio
async def test_cors_headers_wildcard_origin():
    """Test CORS headers with wildcard origin."""
    headers = get_cors_headers(None)
    assert headers["Access-Control-Allow-Origin"] == "*"
    assert headers["Access-Control-Allow-Credentials"] == "false"


@pytest.mark.asyncio
async def test_storage_options_endpoint():
    """Test OPTIONS preflight request for storage assets."""
    test_router = get_test_router()
    from fastapi import FastAPI
    test_app = FastAPI()
    test_app.include_router(test_router)
    
    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as client:
        response = await client.options("/storage/v1/render/image/public/test.png")
        assert response.status_code == 204
        assert response.headers["access-control-allow-credentials"] == "false"
        assert response.headers["access-control-allow-origin"] == "*"


@pytest.mark.asyncio
async def test_storage_head_endpoint():
    """Test HEAD request for storage assets."""
    test_router = get_test_router()
    from fastapi import FastAPI
    test_app = FastAPI()
    test_app.include_router(test_router)
    
    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as client:
        response = await client.head("/storage/v1/render/image/public/test.png")
        assert response.status_code == 200
        assert response.headers["access-control-allow-credentials"] == "false"


@pytest.mark.asyncio
async def test_render_image_public_success():
    """Test successful image asset retrieval."""
    test_router = get_test_router()
    from fastapi import FastAPI
    test_app = FastAPI()
    test_app.include_router(test_router)
    
    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as client:
        response = await client.get("/storage/v1/render/image/public/test.png")
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        assert response.headers["access-control-allow-credentials"] == "false"
        assert response.headers["accept-ranges"] == "bytes"
        # Verify it's a valid PNG
        assert response.content.startswith(b"\x89PNG")


@pytest.mark.asyncio
async def test_render_image_public_not_found():
    """Test image asset not found."""
    test_router = get_test_router()
    from fastapi import FastAPI
    test_app = FastAPI()
    test_app.include_router(test_router)
    
    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as client:
        response = await client.get("/storage/v1/render/image/public/nonexistent.png")
        assert response.status_code == 404
        assert response.headers["access-control-allow-credentials"] == "false"


@pytest.mark.asyncio
async def test_render_image_public_non_image():
    """Test non-image file rejection on render/image endpoint."""
    test_router = get_test_router()
    from fastapi import FastAPI
    test_app = FastAPI()
    test_app.include_router(test_router)
    
    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as client:
        response = await client.get("/storage/v1/render/image/public/test.txt")
        assert response.status_code == 400
        assert response.headers["access-control-allow-credentials"] == "false"


@pytest.mark.asyncio
async def test_object_public_success():
    """Test public object retrieval."""
    test_router = get_test_router()
    from fastapi import FastAPI
    test_app = FastAPI()
    test_app.include_router(test_router)
    
    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as client:
        response = await client.get("/storage/v1/object/public/public/test.txt")
        assert response.status_code == 200
        assert response.headers["access-control-allow-credentials"] == "false"
        assert response.headers["accept-ranges"] == "bytes"
        assert response.text == "Test asset"


@pytest.mark.asyncio
async def test_object_public_not_found():
    """Test public object not found."""
    test_router = get_test_router()
    from fastapi import FastAPI
    test_app = FastAPI()
    test_app.include_router(test_router)
    
    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as client:
        response = await client.get("/storage/v1/object/public/public/nonexistent.txt")
        assert response.status_code == 404
        assert response.headers["access-control-allow-credentials"] == "false"


@pytest.mark.asyncio
async def test_storage_path_traversal_blocked():
    """Test that path traversal attempts are blocked via object endpoint."""
    test_router = get_test_router()
    from fastapi import FastAPI
    test_app = FastAPI()
    test_app.include_router(test_router)
    
    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as client:
        # Test path traversal via object endpoint with encoded dots
        response = await client.get("/storage/v1/object/public/public/%2e%2e/%2e%2e/etc/passwd")
        # Should be 403 (forbidden) or 404 (not found after normalization)
        assert response.status_code in (403, 404)
        assert response.headers["access-control-allow-credentials"] == "false"


@pytest.mark.asyncio
async def test_cors_headers_prevent_cf_bm_cookie():
    """Test that CORS configuration prevents Cloudflare __cf_bm cookie rejection.
    
    The fix for issue #37312 ensures:
    1. Access-Control-Allow-Credentials: false - prevents cookie handling
    2. Proper Vary: Origin header for caching
    3. No Set-Cookie headers on asset responses
    """
    test_router = get_test_router()
    from fastapi import FastAPI
    test_app = FastAPI()
    test_app.include_router(test_router)
    
    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as client:
        response = await client.get("/storage/v1/render/image/public/test.png")
        
        # Verify no Set-Cookie header (prevents __cf_bm cookie issue)
        assert "set-cookie" not in [h.lower() for h in response.headers.keys()]
        
        # Verify credentials disabled
        assert response.headers["access-control-allow-credentials"] == "false"
        
        # Verify proper CORS headers
        assert "access-control-allow-origin" in response.headers
        assert "vary" in response.headers
        assert response.headers["vary"] == "Origin"


@pytest.mark.asyncio
async def test_main_app_includes_storage_routes():
    """Test that main app includes storage routes."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # OPTIONS should work on storage endpoints
        response = await client.options("/storage/v1/render/image/public/test.png")
        assert response.status_code == 204
        assert response.headers["access-control-allow-credentials"] == "false"
