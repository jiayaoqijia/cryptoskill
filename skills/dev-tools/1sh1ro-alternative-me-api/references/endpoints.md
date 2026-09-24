# Alternative.me API Notes

Validated against official Fear & Greed API docs page (2026-02-23).

## Access model

- Public API for Fear & Greed index is available without API key.

## Common endpoint

- `GET /fng/`
  - Example params: `limit`, `format`, `date_format`

## Integration guidance

- Treat service outage as soft failure and preserve other report sections.
