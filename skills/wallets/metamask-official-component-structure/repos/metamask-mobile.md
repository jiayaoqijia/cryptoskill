---
repo: metamask-mobile
parent: component-structure
---

## MetaMask Mobile

### Folder convention (R1, R3)

Where a component goes, its file set and styling follow `mms-component-scaffold`. This skill adds two things to that layout: the screen hook `use<Name>.ts` returns `{ state, actions }` and has its own test, and a sub-component split out under R1 goes in `components/<Sub>/` next to the parent.

Many older screens live in `<Name>/index.tsx`. When restructuring one, move to `<Name>/<Name>.tsx` plus `index.ts` only if the change already touches the file's imports.

### React and React Compiler (R7)

- React 19. React Compiler covers all app code and is off under Jest, so tests do not exercise compiled output.
- ESLint: `react-compiler/react-compiler` is `warn`; `react-hooks/exhaustive-deps` is on (`error`) except in a few files listed in `.eslintrc.js`. Dependency lists on manual memoization are linted, so a memo added "just in case" also adds a list to maintain.
- Tests: the compiler is off under Jest and does not matter for `*.test.*` files, so R7 does not apply to them.
- Bailouts: confirm on current code by running the compiler with the `babel.config.js` options, `react-compiler/react-compiler`, or `react-compiler-marker` (setup in `mms-react-compiler-migration`). The local, append-only `react-compiler.log` may contain entries from older code or other branches; existing entries are hints, not proof. Without confirmation, mark the R7 finding as unconfirmed, name the suspected bailout and do not recommend removing existing memoization until checked.
- Possible bailout signs: a `react-hooks` eslint-disable inside the component, `try/finally`, or a `throw` inside `try/catch` (unsupported in `babel-plugin-react-compiler` 1.0). Signs alone do not confirm a bailout.
- Not compiled, so manual memoization stays and is not an R7 finding: a file with a `'use no memo'` directive (a module-scope one still logs `CompileSuccess`, so it never shows as a bailout in the log or the marker; grep for it), a class component, and a function the compiler reports as unsupported (`Todo` category). Do not rewrite working code to please the compiler.
- R7 exception: `useFocusEffect(useCallback(() => { ... }, [deps]))` from React Navigation needs a stable callback. Keep it. A focus effect responds to a navigation event, so it is not an R4 finding either.

### Copy

- `strings('key')` from `locales/i18n`. Call it at render or inside a function called at render.

### Navigation (R3)

- React Navigation: `useNavigation`, `useRoute`, `useFocusEffect`. Navigation decisions after an async flow belong in `use<Screen>`, which can call `useNavigation()` itself.

### Async (R4)

- `@tanstack/react-query` with the app's shared `QueryClient`. Use `useQuery` for async reads instead of an effect with a `cancelled` flag.
- Engine controller calls triggered by the user (`Engine.context.X.method()`) belong in handlers inside `use<Screen>`, not in effects.

### Subscriptions (R9)

- Live-data hooks: shared stream hooks (live prices, account, positions and similar) read from one shared subscription. Calling one per row, scoped to that row's symbol, is the intended pattern, not an R9 finding. Calling one at the top of a large view whose value feeds only a price or PnL region is.
- Controller state reaches Redux in batched flushes, so a rarely changing selector at the top of a screen is cheap. R9 targets values that change on most flushes: token rates and market data, balances, live prices.
- Rows: a list row that selects a whole market-data, currency-rate or asset-rate collection to price one asset is the R9 row case. Pass the price in, or read it with a selector that takes the asset's id and returns only the price.

### Testing extracted code

- Follow `mms-mobile-testing` for the layer: a component-view test for the screen, a unit test for a pure `use<Screen>` reducer or helper.
