# Coinglass Access Notes

Validated against official docs/pricing pages (2026-02-23).

## Auth

- API key required.
- Header in docs: `CG-API-KEY`.

## Access model

- Open API uses plans/quotas; practical usage is paid-tier based for sustained reporting workloads.
- Treat missing key / insufficient plan as capability block.

## Integration guidance

- Env var: `COINGLASS_API_KEY`
- Optional base URL override: `COINGLASS_BASE_URL`
- Keep endpoint-level error messages in report `data_gaps`.
