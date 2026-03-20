# OpenClaw Trading Suite

Public, publish-safe scaffold for running OpenClaw agents in a trading-bot role.

## Includes

- adapter contracts and skill-aware routing
- autonomy policy modes
- strategy builder and paper-to-live promotion gates
- SQLite-backed retention for hypotheses, orders, fills, metrics, and lessons
- overnight research and user-facing reporting
- log redaction and OpenClaw-compatible secret reference handling

## Quick start

1. Review [SKILL.md](./SKILL.md)
2. Configure secrets using environment variables or OpenClaw SecretRefs
3. Start in paper mode
4. Use strategy-specific promotion gates before enabling live trading

## Secrets

This repo supports:

- regular environment variables
- OpenClaw SecretRef JSON objects
- OpenClaw-style shorthand refs for local development

See:

- [references/secrets_management.md](./references/secrets_management.md)
- OpenClaw docs: https://docs.openclaw.ai/gateway/secrets#secrets-management

## Public scope

This repository is the supported public surface. Historical modules have been archived separately.

See:

- [references/public_release_scope.md](./references/public_release_scope.md)
- [references/legacy_module_audit.md](./references/legacy_module_audit.md)

## Safety note

This repository is for research, paper trading, and controlled automation scaffolding. Live trading should remain user-governed and strategy-gated.

