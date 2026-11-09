# Orbit Engine 147 — Alan Vo

> Work in progress. This checkpoint may be incomplete or fail tests. See PLAN.md and STATUS.md before use.


The Postgres development platform. Supabase gives you a dedicated Postgres database to build your web, mobile, and AI applications.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment config
cp .env.example .env
# Edit .env with your database URL

# Run the server
python -m app.main
```

The API will be available at `http://localhost:8000`.

## API Endpoints

- `GET /` - Application info
- `GET /health` - Health check with database connectivity
- `GET /storage/v1/render/image/public/{path}` - Serve public image assets (issue #37312)
- `GET /storage/v1/object/public/{bucket}/{path}` - Serve public objects from bucket
- `OPTIONS /storage/v1/{path}` - CORS preflight for storage assets
- `HEAD /storage/v1/{path}` - HEAD requests for storage assets

## Project Structure

```
orbit-engine-147/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── config.py        # Configuration management
│   ├── database.py      # Database connection pool
│   ├── auth.py          # SMS OTP authentication
│   └── storage.py       # Storage assets with CORS fix
├── tests/
│   ├── test_health.py   # Health endpoint tests
│   ├── test_auth.py     # SMS OTP authentication tests
│   └── test_storage.py  # Storage assets tests (issue #37312)
├── requirements.txt
├── .env.example
├── feature-plan.json
└── PLAN.md
```

## Features Implemented

- [x] Core API skeleton with FastAPI
- [x] Health check endpoint with database connectivity
- [x] PostgreSQL connection pooling
- [x] Configuration via environment variables
- [x] SMS OTP with newline support for WebOTP API (issue #6435)
- [x] Storage assets with CORS fix for __cf_bm cookie rejection (issue #37312)

## Planned Features

- [ ] Ensure pg_pgrst_no_exposed_schemas exists on project init (issue #40617)

Maintainer: Alan Vo <alanvo@gmail.com>

---

Alan Vo · [alanvo.net](https://alanvo.net) · [X: @alanvoasi](https://x.com/alanvoasi)
