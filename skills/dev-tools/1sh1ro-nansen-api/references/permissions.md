# Nansen Access Notes

Validated against public product/pricing pages (2026-02-23).

## Access model

- Nansen API access is paid-oriented (team/professional/enterprise style access).
- Do not assume public unauthenticated endpoints are available for production reporting.

## Integration guidance

- Required env vars:
  - `NANSEN_API_KEY`
  - `NANSEN_BASE_URL`
- Optional:
  - `NANSEN_API_KEY_HEADER` (default in script is `apikey`)

## Operational rule

- Treat 401/403/plan errors as hard capability blocks.
- Keep endpoint/plan notes in `data_gaps` for report traceability.
