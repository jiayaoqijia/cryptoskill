---
repo: metamask-mobile
parent: avoid-any
---

# `avoid-any` in metamask-mobile

## The rule is a re-enable, and the rules that would catch the absorbed case are off

`@typescript-eslint/no-explicit-any` is `'error'` at `.eslintrc.js:170`, inside the `files: ['*.{ts,tsx}']` override (`:155`) that extends `@metamask/eslint-config-typescript` (`:156`). That line **restores** a rule the shared config switches off. Mobile is on `^13.0.0` (`package.json:635`), whose `src/index.js` sets:

- `:44` — `@typescript-eslint/no-explicit-any: 'off'`
- `:67`–`:71` — `no-unsafe-argument`, `no-unsafe-assignment`, `no-unsafe-call`, `no-unsafe-member-access`, `no-unsafe-return`, all `'off'`

Those five are the rules typescript-eslint ships for the absorbed case, and nothing in `.eslintrc.js` turns any of them back on. So the parent skill's declared/absorbed split is this repo's literal configuration: **a written `any` fails CI, and an absorbed `any` is reported by nothing at all.**

One thing mobile gets right that extension does not: the block's `files` is a plain glob, `'*.{ts,tsx}'`. Extension derives its equivalent list from the tsconfig program, so a file excluded from typechecking there loses `no-explicit-any` with it. Here the two scopes are independent — excluding a file from `tsconfig.json` does not remove the rule from it.

## Three more rules off, and one that stays on

The comment at `.eslintrc.js:186` introduces the same ESLint-v9 reversion block extension carries (*"a temporary measure to get us to ESLint v9 compatible versions"*); the rules it governs run from `:191` to `:223`. Three of them bear on `any`:

- **`no-floating-promises: 'off'` (`:199`)** — with the `no-unsafe-*` rules also off, a call returning absorbed `any` and a call dropping a real promise are the same unreported line.
- **`no-unsafe-enum-comparison: 'off'` (`:206`)** — redundant with the shared config, which already disables it; the gap is not mobile-specific.
- **`restrict-template-expressions: 'off'` (`:221`)** — `` `${value}` `` with an `any` operand goes unremarked. Extension and core keep the rule on but leave `allowAny` at its default `true`, so the outcome is the same in all three; only the reason differs.

`no-unsafe-function-type` is **not** disabled here, unlike extension. It ships in typescript-eslint v8's `recommended` and mobile is on `@typescript-eslint/eslint-plugin@^8.1.0` (`package.json:692`), so `const f: Function` — an `any`-producing annotation with no `any` written — is caught in mobile and not in extension.

## The per-path override is the lever for tightening this

`.eslintrc.js:471` scopes `no-floating-promises: 'error'` (`:628`) back on for `app/**/*-method-action-types*.ts`, under the Perps Core-alignment comment at `:459`. Whatever its motivation, it is the worked example: a team wanting the five `no-unsafe-*` rules on in their own directory does it with an `overrides` entry on their glob, not a repo-wide flip.

## Where the absorbed `any` enters here

**`app/declarations/index.d.ts` is the largest bodyless-declaration surface of the three repos** — **14 of its 38 `declare module` lines are shorthand**, and a shorthand declaration types every import from that module as `any`, silently, under `strict` (verified by probe: `IsAny<T>` resolves `true`, `tsc` exits 0):

- `:2`–`:5` — four `react-native-safe-area-context/src/*` deep imports
- `:9` `*.mp4` · `:11` `@metamask/react-native-payments/lib/js/__mocks__` · `:13` `react-native-fade-in-image` · `:15` `react-native-fast-crypto` · `:17` `react-native-minimizer` · `:19` `xhr2`
- `:307` `@metamask/react-native-search-api` · `:439`–`:440` `@tommasini/react-native-scrollable-tab-view` and its `/DefaultTabBar` · `:442` `react-native-tcp-socket`

The same file also carries an **untyped ambient const** at `:302`–`:305` — `declare module '@metamask/react-native-actionsheet' { const ActionSheet; export default ActionSheet; }`. In an ambient context a missing annotation is `any` and `noImplicitAny` does not fire; the probe confirms it. This is the absorbed form wearing a declaration's clothes, and grepping for shorthand `declare module` will not find it.

**The `.js` boundary exists but is narrow.** `tsconfig.json:6` sets `allowJs: true` and `checkJs` is never set. Under `app/` there are **237 `.js`/`.jsx` files against 12,797 `.ts`/`.tsx`** (`main`, 2026-08-31) — proportionally about a seventh of extension's exposure. `app/core/InpageBridgeWeb3.js` is in `exclude` (`tsconfig.json:94`), so it is outside the program entirely.

**`lib: ["es2022"]` with no DOM (`tsconfig.json:5`) routes web-shaped code back into hand-written declarations.** A value with no ambient type either fails to compile or gets served by `app/declarations/`, which is where the shorthand list above lives. `index.d.ts:317` augmenting the global `Crypto` interface is this pressure showing up in the file.

**`paths` maps 20 specifiers to a chosen declaration file** (`tsconfig.json:15`), several of them deep into `node_modules/**/dist/**/*.d.cts`, and one (`tsconfig.json:18`) to a local `app/declarations/@keystonehq/ur-decoder.d.ts`. The type at every call site of those imports is decided by `tsconfig.json` rather than by the package — so re-reading the import statement tells you nothing about what was resolved.

## One setting that is not an `any` source

`noUncheckedIndexedAccess` is not set. That widens indexing results, not `any`; a replacement for a shorthand declaration typed `Record<string, X>` will read as total when it is not.

## Checking it

```bash
git grep -nE "^declare module '[^']+';$" -- '*.d.ts'   # shorthand = whole module is any
git grep -nE "^\s+(const|let|var) [A-Za-z_$][\w$]*;$" -- '*.d.ts'  # untyped ambient = also any
git grep -rn "eslint-disable.*no-explicit-any"          # the declared any, countable
```

None of these finds the absorbed form in ordinary source. Probe it at the call site with `IsAny<T>`; the probe, its controls, and the `declare module` composition that repairs one are in `tsc-blindspots`.

## Open questions

- Do any of the 20 `paths` targets resolve to `any` at their call sites? Settled by an `IsAny<T>` probe on one import from each mapped specifier, not by reading the mapping.
- Which of the 14 shorthand declarations still need to be shorthand? Settled by checking each package's `types`/`exports` field at the installed version.
- Whether mobile's resolved `@typescript-eslint` version treats `no-unsafe-function-type` as `recommended` — `^8.1.0` was read from `package.json`, not from `yarn.lock`. Settled by reading the lockfile entry.
