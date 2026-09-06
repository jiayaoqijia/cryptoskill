---
repo: metamask-mobile
parent: perps-review-pr
---

## File Paths

| Area | Path |
|---|---|
| Views | `app/components/UI/Perps/Views/` |
| Hooks | `app/components/UI/Perps/hooks/` |
| Utils | `app/components/UI/Perps/utils/` |
| TestIDs | `app/components/UI/Perps/Perps.testIds.ts` |
| Controller | `app/controllers/perps/` |
| Docs | `docs/perps/` |

## Review Focus Areas

**Formatting** — mobile is source of truth. `formatPerpsFiat` in `utils/formatUtils.ts` implements the correct sig-dig rules. PRs should use it, not introduce new formatters.

**Controller changes** — any modification to `app/controllers/perps/` syncs to Core via `validate-core-sync.sh`. Verify the sync script still passes. Changes here affect extension too.

**Hook granularity** — mobile uses fine-grained hooks (e.g., order form splits into 4 hooks). PRs adding new hooks should follow this pattern, not consolidate into monolithic hooks.

**Priority 1 candidates** — if a PR modifies a utility listed in shared-package-analysis Priority 1, flag the opportunity to move it to the controller instead of modifying it in the UI layer.

## Validation

1. `yarn lint` — no lint errors in affected files
2. `yarn test --testPathPattern=Perps` — run perps unit tests
3. `yarn build:ios` or `yarn build:android`
