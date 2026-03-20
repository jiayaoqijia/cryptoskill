# Security

## Guardrails

- Secrets are read from environment only.
- `API-Key`, `API-Sign`, and `KRAKEN_API_SECRET` are never written to stdout or stderr.
- Private REST requests are always POST and signed centrally.
- Base URLs are declared in config and validated before use.
- Trading commands require `--confirm` unless the operator explicitly disables `KRAKEN_REQUIRE_CONFIRM`.
- `jq` filters are local-only response formatting and are never applied to outbound request material.
- The endpoint registry is local and explicit. Unknown aliases are rejected rather than executed as arbitrary URLs.
- WebSocket transport is generic and agent-driven, but private feed auth still depends on explicit secrets or challenge material and is never logged back to stderr.

## Logging

- stdout contains API response bodies only.
- stderr contains sanitized operational messages.
- Shell tracing is disabled around signing and HTTP execution paths.

## Validation

- malformed base URLs are rejected
- unsupported path prefixes are rejected
- missing private credentials fail before request dispatch
