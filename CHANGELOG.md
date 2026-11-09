# Changelog

## 1.3.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.3.0 — work-in-progress checkpoint (2026-11-09)

### Added
- Storage assets module with CORS fix for Cloudflare __cf_bm cookie rejection (issue #37312)
- Storage endpoints: `/storage/v1/render/image/public/{path}` and `/storage/v1/object/public/{bucket}/{path}`
- CORS preflight (OPTIONS) and HEAD support for storage assets
- Security: Path traversal protection for asset serving
- Proper CORS headers: `Access-Control-Allow-Credentials: false`, `Vary: Origin`, no Set-Cookie
- Comprehensive test suite for storage assets (12 tests)

### Implementation Files
- `app/storage.py` - Storage assets module with CORS fix
- `app/main.py` - Updated to include storage router
- `tests/test_storage.py` - Storage assets tests (12 tests)

### Testing
- All tests pass (34/34)
- CORS headers prevent __cf_bm cookie rejection
- Asset serving works for images and generic objects
- Path traversal attempts blocked
- No Set-Cookie headers on asset responses

## 1.2.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.1.0 — work-in-progress checkpoint (2026-11-07)

### Added
- SMS OTP authentication with WebOTP API support (issue #6435)
- SMS template rendering with literal newline support for WebOTP compliance
- OTP generation, validation, and verification with expiry handling
- Phone number validation (E.164 format)
- Comprehensive test suite for SMS OTP functionality (20 tests)

### Implementation Files
- `app/auth.py` - SMS OTP service with WebOTP-compatible template rendering
- `tests/test_auth.py` - SMS OTP authentication tests (20 tests)

### Testing
- All tests pass (22/22)
- SMS template accepts literal newlines and multiline content
- Generated SMS contains newlines for WebOTP compatibility
- OTP generation, verification, and expiry work correctly

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-10-26

### Added
- FastAPI core skeleton with health endpoint (`/health`) and root endpoint (`/`)
- PostgreSQL connection pooling via asyncpg with configurable pool size
- Configuration management via Pydantic Settings with environment variable support
- Health check endpoint that verifies database connectivity
- Test suite with pytest and httpx for API endpoint testing
- Project structure following standard Python packaging conventions
- Requirements file with pinned dependencies
- Environment configuration example file (`.env.example`)

### Implementation Files
- `app/main.py` - FastAPI application with lifespan management
- `app/config.py` - Configuration using pydantic-settings
- `app/database.py` - Async PostgreSQL connection pool
- `tests/test_health.py` - Health and root endpoint tests
- `requirements.txt` - Python dependencies
- `.env.example` - Example environment configuration
- `feature-plan.json` - Feature tracking with JSON schema
- `PLAN.md` - Human-readable implementation plan
- `README.md` - Project documentation

### Testing
- All tests pass (2/2)
- Health endpoint returns proper structure with/without database
- Root endpoint returns application metadata

---

Alan Vo · [alanvo.net](https://alanvo.net) · [X: @alanvoasi](https://x.com/alanvoasi)
