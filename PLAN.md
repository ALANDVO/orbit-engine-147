# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

core-api-skeleton

## Roadmap

### core-api-skeleton — FastAPI core skeleton with health endpoint and Postgres connection

Status: done

Acceptance:
- FastAPI app starts and serves /health endpoint
- Postgres connection pool configured via environment
- Basic project structure with requirements.txt

Implementation: `app/main.py`, `app/config.py`, `app/database.py`, `requirements.txt`

Tests: `tests/test_health.py`

### auth-otp-sms — SMS OTP with newline support for WebOTP API (issue #6435)

Status: planned

Acceptance:
- SMS template accepts literal newlines
- Generated SMS contains newline for WebOTP compatibility

### storage-cors-fix — Fix __cf_bm cookie rejection on storage assets (issue #37312)

Status: planned

Acceptance:
- Storage asset responses don't trigger invalid domain cookie errors

### postgrest-schema-init — Ensure pg_pgrst_no_exposed_schemas exists on project init (issue #40617)

Status: planned

Acceptance:
- Fresh project initializes without schema missing errors

