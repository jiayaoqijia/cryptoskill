---
repo: metamask-extension
parent: perps-review-pr
---

## File Paths

| Area | Path |
|---|---|
| Components | `ui/components/app/perps/` |
| Pages | `ui/pages/perps/` |
| Hooks | `ui/hooks/perps/` |
| Utils | `ui/components/app/perps/utils.ts` |
| Transforms | `ui/components/app/perps/utils/transactionTransforms.ts` |
| Stream bridge | `app/scripts/controllers/perps/perps-stream-bridge.ts` |
| Routes | `ui/helpers/constants/routes.ts` |

## Review Focus Areas

**Formatting hotspots** — these files have known incorrect formatting. PRs touching them should fix, not add more:

```
ui/components/app/perps/utils/transactionTransforms.ts    -- .toFixed(2) x7
ui/components/app/perps/order-entry/components/auto-close-section/  -- {min:2, max:2}
ui/components/app/perps/order-entry/components/limit-price-input/   -- {min:2, max:2}
ui/components/app/perps/edit-margin/edit-margin-modal-content.tsx    -- .toFixed(2)
ui/components/app/perps/reverse-position/reverse-position-modal.tsx  -- .toFixed(2)
ui/hooks/perps/usePerpsOrderForm.ts                                  -- formatCurrencyWithMinThreshold x6
```

**Hook consolidation** — extension merges several mobile hooks into one. When reviewing hook changes, check that the consolidated hook still covers all cases the separate mobile hooks handle.

**Component-view test fit** — Perps page tests under `ui/pages/perps/**/*.test.tsx` that render full pages or exercise UI behavior should be reviewed as component-view test candidates. Ask for conversion to the component-view test framework/skill while preserving coverage. Keep ordinary unit tests only for pure helpers, narrow rendering contracts, or cases the framework cannot cover yet; require that exception to be stated.

**Missing screens** — close-all, cancel-all, withdraw, order book, order details. Don't block PRs for these, but note if a PR introduces partial implementations that conflict with future full implementations.

## Validation

1. `yarn lint` — no lint errors in affected files
2. `yarn test:unit` — run tests for affected files
3. `yarn build` — TypeScript compiles
