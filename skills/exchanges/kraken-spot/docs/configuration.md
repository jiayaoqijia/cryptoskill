# Configuration

The CLI reads configuration in this order:

1. Existing environment variables
2. `OPENCLAW_KRAKEN_CONFIG` if set
3. `config/kraken.env.example` when sourced manually by the operator

## Required non-secret settings

- `KRAKEN_API_BASE_URL`
- `KRAKEN_API_VERSION`

## Required secret settings for private endpoints

- `KRAKEN_API_KEY`
- `KRAKEN_API_SECRET`
- `KRAKEN_FUTURES_API_KEY`
- `KRAKEN_FUTURES_API_SECRET`

## Additional endpoints and transports

- `KRAKEN_FUTURES_API_BASE_URL`
- `KRAKEN_WS_SPOT_PUBLIC_URL`
- `KRAKEN_WS_SPOT_PRIVATE_URL`
- `KRAKEN_WS_FUTURES_URL`
- `KRAKEN_WS_TIMEOUT_MS`
- `KRAKEN_WS_MAX_MESSAGES`

## OpenClaw secrets pattern

Keep the Bash CLI environment-only. Let OpenClaw resolve the actual value from a secret ref. Valid refs use the shape:

```json
{"source":"env|file|exec","provider":"default","id":"..."}
```

See https://docs.openclaw.ai/gateway/secrets for provider validation and eager resolution behavior.
