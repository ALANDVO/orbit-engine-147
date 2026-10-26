# Changelog

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
