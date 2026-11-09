"""Storage assets module with CORS fix for __cf_bm cookie issue (issue #37312)."""

from fastapi import APIRouter, Response, Header, Request
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional
import os
import mimetypes

router = APIRouter(prefix="/storage/v1", tags=["storage"])
mimetypes.init()

class StorageConfig:
    assets_root: str = "/var/lib/storage/assets"
    public_path: str = "public"
    cache_control: str = "public, max-age=31536000, immutable"

def get_cors_headers(origin: Optional[str] = None) -> dict:
    return {
        "Access-Control-Allow-Origin": origin or "*",
        "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, Range, Accept",
        "Access-Control-Expose-Headers": "Content-Length, Content-Range, Accept-Ranges",
        "Access-Control-Allow-Credentials": "false",
        "Access-Control-Max-Age": "86400",
        "Vary": "Origin",
        "Cache-Control": "public, max-age=31536000, immutable",
    }

@router.options("/{path:path}")
async def storage_options(path: str, origin: Optional[str] = Header(None)):
    return Response(status_code=204, headers=get_cors_headers(origin))

@router.head("/{path:path}")
async def storage_head(path: str, origin: Optional[str] = Header(None)):
    return Response(status_code=200, headers=get_cors_headers(origin))

@router.get("/render/image/public/{path:path}")
async def render_image_public(path: str, request: Request, origin: Optional[str] = Header(None)):
    headers = get_cors_headers(origin)
    file_path = os.path.normpath(os.path.join(StorageConfig.assets_root, StorageConfig.public_path, path))
    assets_root_norm = os.path.normpath(os.path.join(StorageConfig.assets_root, StorageConfig.public_path))
    if not file_path.startswith(assets_root_norm):
        return JSONResponse(status_code=403, content={"error": "Forbidden"}, headers=headers)
    if not os.path.isfile(file_path):
        return JSONResponse(status_code=404, content={"error": "Not found"}, headers=headers)
    content_type, _ = mimetypes.guess_type(file_path)
    if not content_type or not content_type.startswith("image/"):
        return JSONResponse(status_code=400, content={"error": "Not an image"}, headers=headers)
    headers["Content-Type"] = content_type
    headers["Accept-Ranges"] = "bytes"
    return FileResponse(path=file_path, headers=headers, media_type=content_type)

@router.get("/object/public/{bucket}/{path:path}")
async def object_public(bucket: str, path: str, request: Request, origin: Optional[str] = Header(None)):
    headers = get_cors_headers(origin)
    file_path = os.path.normpath(os.path.join(StorageConfig.assets_root, bucket, path))
    bucket_root_norm = os.path.normpath(os.path.join(StorageConfig.assets_root, bucket))
    if not file_path.startswith(bucket_root_norm):
        return JSONResponse(status_code=403, content={"error": "Forbidden"}, headers=headers)
    if not os.path.isfile(file_path):
        return JSONResponse(status_code=404, content={"error": "Not found"}, headers=headers)
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = "application/octet-stream"
    headers["Content-Type"] = content_type
    headers["Accept-Ranges"] = "bytes"
    return FileResponse(path=file_path, headers=headers, media_type=content_type)

def create_test_assets():
    import shutil, base64
    test_root = "/tmp/orbit-engine-test-assets"
    if os.path.exists(test_root):
        shutil.rmtree(test_root)
    public_dir = os.path.join(test_root, "public")
    os.makedirs(public_dir)
    with open(os.path.join(public_dir, "test.png"), "wb") as f:
        f.write(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="))
    with open(os.path.join(public_dir, "test.txt"), "w") as f:
        f.write("Test asset")
    return test_root

TEST_ASSETS_ROOT = create_test_assets()

class TestStorageConfig(StorageConfig):
    assets_root = TEST_ASSETS_ROOT

def get_test_router():
    from fastapi import APIRouter as _APIRouter
    test_router = _APIRouter(prefix="/storage/v1", tags=["storage"])
    @test_router.options("/{path:path}")
    async def test_storage_options(path: str, origin: Optional[str] = Header(None)):
        return Response(status_code=204, headers=get_cors_headers(origin))
    @test_router.head("/{path:path}")
    async def test_storage_head(path: str, origin: Optional[str] = Header(None)):
        return Response(status_code=200, headers=get_cors_headers(origin))
    @test_router.get("/render/image/public/{path:path}")
    async def test_render_image_public(path: str, request: Request, origin: Optional[str] = Header(None)):
        headers = get_cors_headers(origin)
        file_path = os.path.normpath(os.path.join(TestStorageConfig.assets_root, TestStorageConfig.public_path, path))
        assets_root_norm = os.path.normpath(os.path.join(TestStorageConfig.assets_root, TestStorageConfig.public_path))
        if not file_path.startswith(assets_root_norm):
            return JSONResponse(status_code=403, content={"error": "Forbidden"}, headers=headers)
        if not os.path.isfile(file_path):
            return JSONResponse(status_code=404, content={"error": "Not found"}, headers=headers)
        content_type, _ = mimetypes.guess_type(file_path)
        if not content_type or not content_type.startswith("image/"):
            return JSONResponse(status_code=400, content={"error": "Not an image"}, headers=headers)
        headers["Content-Type"] = content_type
        headers["Accept-Ranges"] = "bytes"
        return FileResponse(path=file_path, headers=headers, media_type=content_type)
    @test_router.get("/object/public/{bucket}/{path:path}")
    async def test_object_public(bucket: str, path: str, request: Request, origin: Optional[str] = Header(None)):
        headers = get_cors_headers(origin)
        file_path = os.path.normpath(os.path.join(TestStorageConfig.assets_root, bucket, path))
        bucket_root_norm = os.path.normpath(os.path.join(TestStorageConfig.assets_root, bucket))
        if not file_path.startswith(bucket_root_norm):
            return JSONResponse(status_code=403, content={"error": "Forbidden"}, headers=headers)
        if not os.path.isfile(file_path):
            return JSONResponse(status_code=404, content={"error": "Not found"}, headers=headers)
        content_type, _ = mimetypes.guess_type(file_path)
        if content_type is None:
            content_type = "application/octet-stream"
        headers["Content-Type"] = content_type
        headers["Accept-Ranges"] = "bytes"
        return FileResponse(path=file_path, headers=headers, media_type=content_type)
    return test_router
