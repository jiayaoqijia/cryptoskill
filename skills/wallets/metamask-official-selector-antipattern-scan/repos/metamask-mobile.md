---
repo: metamask-mobile
parent: selector-antipattern-scan
---

## Paths

- Selector definitions: [`app/selectors/`](https://github.com/MetaMask/metamask-mobile/tree/main/app/selectors)
- Redux store: [`app/store/`](https://github.com/MetaMask/metamask-mobile/tree/main/app/store)
- Engine / state shape: [`app/core/Engine/Engine.ts`](https://github.com/MetaMask/metamask-mobile/blob/main/app/core/Engine/Engine.ts)
- WDYR setup: [`wdyr.js`](https://github.com/MetaMask/metamask-mobile/blob/main/wdyr.js) at repo root
- Component consumption sites: anywhere under [`app/`](https://github.com/MetaMask/metamask-mobile/tree/main/app) that calls `useSelector`

## Commands

```bash
# Enable WDYR (env var gate, same as extension)
ENABLE_WHY_DID_YOU_RENDER=true yarn start

# Pre-merge grep checklist
grep -rE 'export function get' app/selectors/ --include="*.ts"
grep -rn createDeepEqualSelector app/ --include="*.ts"
grep -rnE 'useSelector\([^,]+,\s*(isEqual|shallowEqual)' app/ --include="*.ts" --include="*.tsx"
grep -rnE '\.find\(' app/selectors/
```

## WDYR

Mobile has `wdyr.js` at the repo root. It is gated on `__DEV__ && process.env.ENABLE_WHY_DID_YOU_RENDER === 'true'` and imported from the entry file. No manual setup required — flip the env var and restart Metro.

Current configuration (at time of authoring): `trackAllPureComponents: true`, `onlyLogs: true` (Metro/Hermes console doesn't group well).

## Differences from Extension

- React Compiler adoption and `"use no memo"` opt-outs are not extension-only: mobile has the compiler wired in `babel.config.js` too, via `scripts/react-compiler.js`.
