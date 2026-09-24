# Santiment Access Notes

Validated against official docs/product pages (2026-02-23).

## Access model

- Santiment API usage is key-based and practical production usage is paid-plan oriented.
- Free/public access, if any, is limited and should not be assumed for full report pipelines.

## Integration guidance

- Env vars:
  - `SANTIMENT_API_KEY`
  - `SANTIMENT_API_URL` (default script value: `https://api.santiment.net/graphql`)
- Default auth format in script:
  - `Authorization: Apikey <key>`

## Operational rule

- Treat GraphQL error blocks and 401/403 as capability blocks.
- Keep query + error summary in `data_gaps`.
