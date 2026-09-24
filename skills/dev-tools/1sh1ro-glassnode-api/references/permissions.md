# Glassnode Access Notes

Validated against official docs/pricing pages (2026-02-23).

## Auth

- API key required for API access.
- Typical integration uses `api_key` query parameter; header mode can be used if account/docs specify.

## Access model

- Free-tier access exists but metric coverage and historical granularity are limited.
- Advanced metrics and production-level historical coverage are paid-tier features.

## Integration guidance

- Env var: `GLASSNODE_API_KEY`
- Base URL: `https://api.glassnode.com`
- Treat 401/403/plan errors as capability blocks, not transient failures.
