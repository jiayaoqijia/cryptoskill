# Public Release Scope

This file defines what should be considered public-facing and supported in this repository.

## Publish as supported

- `openclaw-trading-suite/`

Reason:
- actively organized package layout
- tests and runtime scaffolding
- secret handling and log redaction
- adapter routing and strategy-gate framework

## Keep only as legacy/reference unless promoted later

- `market-data-aggregator/`
- `performance-reporter-learner/`
- `risk-position-manager/`
- `strategy-optimizer/`
- `technical-analysis-engine/`
- `trade-signal-processor-executor/`
- `profit-forecaster/`

Reason:
- useful component ideas
- lightweight or placeholder implementations
- not yet aligned to the orchestrator package/runtime contracts

## Exclude from public release or archive separately

- `trading_bot/`
- `trading_db/`
- any generated runtime artifacts
- any machine-local scripts, symlinks, temp folders, nested repos

Reason:
- older monolithic prototype patterns
- runtime/output data rather than source
- higher maintenance burden and weaker contract boundaries

## Promotion rule for legacy modules

Promote a legacy module into the supported public surface only after:

1. it uses the current adapter/security/autonomy interfaces
2. it has tests
3. it avoids direct secret handling in source
4. it has a clear role that is not duplicated by the orchestrator package

