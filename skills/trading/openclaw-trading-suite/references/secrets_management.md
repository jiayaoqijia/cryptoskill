# Secrets Management

Never hardcode credentials in code, configs, logs, or reports.

## Preferred order

1. Environment variables (runtime injected).
2. OpenClaw SecretRef values.
3. Development placeholders only.

## OpenClaw compatibility

Use SecretRef-shaped values compatible with OpenClaw Gateway secrets management.

- JSON form:
  - `{"source":"env","provider":"default","id":"ALPACA_API_KEY"}`
  - `{"source":"file","provider":"filemain","id":"/providers/alpaca/apiKey"}`
  - `{"source":"exec","provider":"vault","id":"providers/alpaca/apiKey"}`
- Shorthand env form supported by this codebase:
  - `openclaw:env:default:ALPACA_API_KEY`
  - `openclaw:file:filemain:/providers/alpaca/apiKey`
  - `openclaw:exec:vault:providers/alpaca/apiKey`

Validation rules aligned to OpenClaw docs:

- `source`: `env`, `file`, or `exec`
- `provider`: lower-case identifier such as `default`, `filemain`, `vault`
- `env.id`: uppercase env var name
- `file.id`: absolute JSON pointer path beginning with `/`
- `exec.id`: provider-specific identifier/path

Precedence:

- plaintext without ref: used as-is
- ref without plaintext: resolved at activation/runtime bootstrap
- plaintext and ref together: ref should win

## Logging safety

- Always pass dictionaries through `redact_structure(...)` before logging.
- Always pass strings through `redact_sensitive(...)` before logging.
- Do not log request headers or full URLs containing credentials.
