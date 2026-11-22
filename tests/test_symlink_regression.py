"""Regression: storage endpoints must not serve files outside the assets root via symlinks."""
import os
import base64
import pytest
from httpx import AsyncClient, ASGITransport
from app.storage import get_test_router, TEST_ASSETS_ROOT


def _make_outside_secret(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    secret = outside / "secret.txt"
    secret.write_text("TOP SECRET - outside assets root")
    return secret


@pytest.fixture
def storage_app(tmp_path):
    from fastapi import FastAPI
    secret = _make_outside_secret(tmp_path)
    public_dir = os.path.join(TEST_ASSETS_ROOT, "public")
    link_path = os.path.join(public_dir, "escape.txt")
    if os.path.lexists(link_path):
        os.remove(link_path)
    os.symlink(str(secret), link_path)
    app = FastAPI()
    app.include_router(get_test_router())
    return app


@pytest.mark.asyncio
async def test_object_public_blocks_symlink_escape(storage_app, tmp_path):
    """A symlink inside the public bucket must not leak a file outside the assets root."""
    async with AsyncClient(transport=ASGITransport(app=storage_app), base_url="http://test") as client:
        response = await client.get("/storage/v1/object/public/public/escape.txt")
    assert response.status_code in (403, 404)
    assert "TOP SECRET" not in response.text


@pytest.mark.asyncio
async def test_render_image_blocks_symlink_escape(storage_app, tmp_path):
    """A symlink inside render/image/public must not leak a file outside the assets root."""
    async with AsyncClient(transport=ASGITransport(app=storage_app), base_url="http://test") as client:
        response = await client.get("/storage/v1/render/image/public/escape.txt")
    assert response.status_code in (403, 404)
    assert "TOP SECRET" not in response.text
