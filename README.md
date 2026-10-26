# Orbit Engine 147

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

## Project Structure

```
orbit-engine-147/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── config.py        # Configuration management
│   └── database.py      # Database connection pool
├── tests/
│   └── test_health.py   # Health endpoint tests
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

## Planned Features

- [ ] SMS OTP with newline support for WebOTP API (issue #6435)
- [ ] Fix __cf_bm cookie rejection on storage assets (issue #37312)
- [ ] Ensure pg_pgrst_no_exposed_schemas exists on project init (issue #40617)

Maintainer: Alan Vo <alanvo@gmail.com>
