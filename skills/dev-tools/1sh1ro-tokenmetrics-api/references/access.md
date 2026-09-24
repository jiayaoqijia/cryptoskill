# Token Metrics Access Notes

## Access model

- Token Metrics API is key-authenticated and paid-plan oriented.
- Do not assume unauthenticated production endpoints.

## Env vars

- `TOKENMETRICS_API_KEY`
- Optional: `TOKENMETRICS_BASE_URL` (default in script)
- Optional: `TOKENMETRICS_API_KEY_HEADER` (default: `x-api-key`)
