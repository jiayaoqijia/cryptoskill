# Legacy Module Audit

This audit summarizes whether legacy modules in the repository are suitable for public release as supported code.

## Summary

- Supported public surface: `openclaw-trading-suite/`
- Legacy/example-only: lightweight JS skill modules and `profit-forecaster/`
- Exclude or archive: `trading_bot/`, `trading_db/`

## Findings by module

### `market-data-aggregator/`

- Status: example-only
- Findings:
  - hardcoded provider assumptions
  - limited auth handling
  - no tests
  - not integrated with current adapter registry/security layer

### `technical-analysis-engine/`

- Status: example-only
- Findings:
  - minimal RSI-only decision logic
  - placeholder scoring
  - no integration with current strategy-gate or persistence layers

### `strategy-optimizer/`

- Status: example-only
- Findings:
  - uses random placeholder scoring
  - not safe to treat as production optimization logic

### `risk-position-manager/`

- Status: example-only
- Findings:
  - simplistic sizing and VaR approximation
  - insufficient for public supported risk engine claims

### `trade-signal-processor-executor/`

- Status: example-only
- Findings:
  - direct venue call assumptions
  - incomplete auth/header handling
  - no idempotency/retry/approval integration

### `performance-reporter-learner/`

- Status: example-only
- Findings:
  - basic PnL aggregation only
  - no model versioning or structured learning loop

### `profit-forecaster/`

- Status: keep as legacy/reference unless promoted
- Findings:
  - more structured than the JS placeholders
  - still isolated from the new orchestrator interfaces
  - can be migrated into the supported package later

### `trading_bot/`

- Status: exclude or archive
- Findings:
  - monolithic layout
  - direct provider coupling
  - older config patterns
  - no adapter/security/orchestration contract alignment

### `trading_db/`

- Status: exclude
- Findings:
  - runtime/sample data, not reusable source

## Recommendation

For a public repo:

1. present `openclaw-trading-suite/` as the maintained product
2. clearly label legacy directories as archived examples or move them to a separate archive branch/repo
3. only promote a legacy module after refactoring it onto the current adapter, autonomy, persistence, and security interfaces

