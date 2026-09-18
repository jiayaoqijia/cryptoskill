---
repo: metamask-extension
parent: selector-antipattern-scan
---

## Paths

- Selector definitions: [`ui/selectors/`](https://github.com/MetaMask/metamask-extension/tree/main/ui/selectors)
- Selector creators: [`shared/lib/selectors/selector-creators.ts`](https://github.com/MetaMask/metamask-extension/blob/main/shared/lib/selectors/selector-creators.ts) — source of truth for `createSelector`, `createDeepEqualSelector`, `createResultEqualSelector`, `createShallowResultSelector`
- Controller state shape: [`app/scripts/metamask-controller.js`](https://github.com/MetaMask/metamask-extension/blob/main/app/scripts/metamask-controller.js)
- Component consumption sites: anywhere under [`ui/`](https://github.com/MetaMask/metamask-extension/tree/main/ui) that calls `useSelector`

## Commands

```bash
# Enable WDYR for post-merge diagnosis
ENABLE_WHY_DID_YOU_RENDER=true yarn start

# Pre-merge grep checklist
grep -rE 'export function get' ui/selectors/ --include="*.ts"
grep -rn createDeepEqualSelector ui/ --include="*.ts"
grep -rnE 'useSelector\([^,]+,\s*(isEqual|shallowEqual)' ui/ --include="*.ts" --include="*.tsx"
grep -rnE '\.find\(' ui/selectors/
```

## Selector Creators

`shared/lib/selectors/selector-creators.ts`

| Creator | Use Case |
|---------|----------|
| `createSelector` | Standard memoization (default) |
| `createDeepEqualSelector` | Genuinely unstable inputs (rare — see [narrow exception](../skill.md#overuse-of-createdeepequalselector)) |
| `createResultEqualSelector` | Unstable outputs requiring deep comparison |
| `createShallowResultSelector` | Unstable outputs, shallow comparison sufficient |

## Example Fix Methodology

[PR #37147](https://github.com/MetaMask/metamask-extension/pull/37147) fixed `getInternalAccounts` as the canonical example. Before: `createSelector(selectInternalAccounts, (accounts) => accounts)` (identity function, defeats memoization). After: `createSelector(getInternalAccountsObject, (accounts) => Object.values(accounts))`. Impact: 50+ component re-renders eliminated per state update.

## Reference

- [Frontend Performance Optimization Guidelines](https://github.com/MetaMask/contributor-docs/pull/159) (contributor-docs PR #159)
