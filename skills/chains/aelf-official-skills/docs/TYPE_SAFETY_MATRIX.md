# Type Safety Matrix

Last updated: 2026-03-04

## Scope
- Included repos (6): `eoa-agent-skills`, `portkey-agent-skills`, `awaken-agent-skills`, `eforest-agent-skills`, `tomorrowDAO-skill`, `aelf-node-skill`
- Excluded repo: `agent-skills-e2e`

## Unified Baseline
- `package.json` scripts:
  - `typecheck:src`
  - `typecheck:test`
  - `typecheck`
- TypeScript config layers:
  - `tsconfig.base.json`
  - `tsconfig.src.json`
  - `tsconfig.test.json`
- Type whitelist: `bun-types` + `node`
- Third-party declaration patch strategy:
  - `aelf-sdk` and `aelf-sdk/src/util/keyStore.js` declarations are explicitly provided

## CI Rollout Policy
- `test.yml` has a new `typecheck` step in **observe mode**:
  - `continue-on-error: true`
- Existing quality gates are unchanged:
  - `deps:check`
  - `build:openclaw:check`
  - `test:coverage:ci`

## Repo Status
| Repo | `typecheck:src` | `typecheck:test` | `typecheck` |
|---|---|---|---|
| eoa-agent-skills | Pass | Pass | Pass |
| portkey-agent-skills | Pass | Pass | Pass |
| awaken-agent-skills | Pass | Pass | Pass |
| eforest-agent-skills | Pass | Pass | Pass |
| tomorrowDAO-skill | Pass | Pass | Pass |
| aelf-node-skill | Pass | Pass | Pass |

## Debt Tracking
- Command: `bun run type-debt:report`
- Outputs:
  - `docs/type-safety/type-debt-latest.json`
  - `docs/type-safety/type-debt-history.json`
