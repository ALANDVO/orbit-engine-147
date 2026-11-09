# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

storage-cors-fix

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

Status: done

Acceptance:
- SMS template accepts literal newlines
- Generated SMS contains newline for WebOTP compatibility

Implementation: `app/auth.py`, `tests/test_auth.py`

Tests: `tests/test_auth.py`

### storage-cors-fix — Fix __cf_bm cookie rejection on storage assets (issue #37312)

Status: done

Acceptance:
- Storage asset responses don't trigger invalid domain cookie errors
- CORS headers include Access-Control-Allow-Credentials: false
- No Set-Cookie headers on asset responses
- Proper Vary: Origin header for caching

Implementation: `app/storage.py`, `app/main.py`

Tests: `tests/test_storage.py`

### postgrest-schema-init — Ensure pg_pgrst_no_exposed_schemas exists on project init (issue #40617)

Status: planned

Acceptance:
- Fresh project initializes without schema missing errors

---

Alan Vo · [alanvo.net](https://alanvo.net) · [X: @alanvoasi](https://x.com/alanvoasi)
