---
repo: core
parent: avoid-any
---

# `avoid-any` in core

## The rule is a deliberate re-enable — and it does not travel with the code

`@typescript-eslint/no-explicit-any` is `'error'` at `eslint.config.mjs:152`, in the `files: ['**/*.ts', '**/*.mts']` block (`:135`) that extends the shared config (`:136`). The comment above it says so outright:

```
// Enable rules that are disabled in `@metamask/eslint-config-typescript`
```

`@metamask/eslint-config-typescript@^15.0.0` (`package.json:70`) sets `no-explicit-any: 'off'` at `src/index.mjs:46`. The same is true of the majors extension and mobile run (`14.1.1:50`, `13.0.0:44`) — **the org's shared TypeScript config permits explicit `any`, and each repo bans it separately.**

The consequence is for extraction, not for writing code here: **a package that leaves core and adopts `@metamask/eslint-config-typescript` without copying `eslint.config.mjs:152` silently permits explicit `any`.** Nothing warns at the split; the code lints clean in its new home and the rule is simply gone. Copy the line with the code.

The block's glob is `**/*.ts` and `**/*.mts`. There are currently no `.tsx`, `.cts` or `.mts` sources under `packages/` (`main`, 2026-08-31), so nothing falls outside it — a first `.tsx` file would.

## The absorbed case is unreported here too

`src/index.mjs:69`–`:73` sets `no-unsafe-argument`, `no-unsafe-assignment`, `no-unsafe-call`, `no-unsafe-member-access` and `no-unsafe-return` all `'off'`, under `// Recommended rules that require type information`. `eslint.config.mjs` does not turn any of them back on. Those five are exactly the rules typescript-eslint ships for the absorbed case, so the parent skill's declared/absorbed split is this repo's literal configuration: **a written `any` fails CI; an absorbed `any` is reported by nothing.**

Core is nonetheless the tightest of the three on the neighbouring rules. Unlike extension and mobile it carries **no ESLint-v9 reversion block**, so `no-floating-promises` and `no-unsafe-function-type` are both live from the shared config's `recommended` / `recommendedTypeChecked` (verified in `@typescript-eslint/eslint-plugin@8.54.0`, `dist/configs/flat/recommended.js`). Two gaps it shares with the others anyway:

- `no-unsafe-enum-comparison` — the shared config disables it at `src/index.mjs:78`.
- `restrict-template-expressions` — on, at `src/index.mjs:171`–`:177`, but neither there nor here does anything set `allowAny`, whose default is `true` (`@typescript-eslint/eslint-plugin`, `dist/rules/restrict-template-expressions.js`, `defaultOptions`). `` `${value}` `` with an `any` operand is permitted.

## Where the absorbed `any` enters here

**Not through `.js`.** `allowJs` and `checkJs` appear in no tsconfig in the repo (`git grep -l 'allowJs\|checkJs' -- '*.json'` returns nothing on `main`). `.js` files exist — `eslint.config.mjs:128` has a `files: ['**/*.{js,cjs}']` block for them — but they are outside every TypeScript program, so a `.ts` file cannot import one without a declaration. **The route that carries most of extension's exposure does not exist here. Do not go looking for it.**

**Through the root `types/` directory instead, and it reaches every package at once.** Ten shorthand `declare module` files live there, each typing its entire module as `any` with no `any` written and no diagnostic under `strict`:

`types/@metamask/contract-metadata.d.ts` · `types/@metamask/eth-json-rpc-filters.d.ts` (`/subscriptionManager`) · `types/@metamask/ethjs-provider-http.d.ts` · `types/@metamask/ethjs-unit.d.ts` · `types/@metamask/metamask-eth-abis.d.ts` · `types/eth-ens-namehash.d.ts` · `types/eth-json-rpc-infura/src/createProvider.d.ts` · `types/ethereum-ens-network-map.d.ts` · `types/ethjs-query.d.ts` · `types/single-call-balance-checker-abi.d.ts`

Package tsconfigs pull the directory in wholesale — `packages/network-controller/tsconfig.json` ends `"include": ["../../types", "../../tests", "./src", "./tests"]` — so all ten are in every package's program, not local to whichever package imports them. An ABI or a token-metadata blob entering a controller through one of these is `any` at the point of entry, and every precise signature downstream of it is absorbed.

**And an absorbed `any` crosses package boundaries as a published type.** `tsconfig.base.json:6` sets `composite: true`, and the root `tsconfig.json` wires the packages together with project references. A dependent package sees its dependency through the emitted `.d.ts`, not through source — so an absorbed `any` on an exported signature is not a local imprecision, it is the interface every consuming package compiles against, and the extension and mobile bundles beyond them.

## Two settings that are not `any` sources

`tsconfig.base.json:12` sets `strict: true`, and it is the only `"strict"` key in any tsconfig in the repo — no package weakens `noImplicitAny`. `noUncheckedIndexedAccess` is not set, which widens indexing results rather than producing `any`; a replacement for one of the shorthand declarations typed `Record<string, X>` will read as total when it is not.

## Checking it

```bash
git grep -nE "^declare module '[^']+';$" -- '*.d.ts'   # shorthand = whole module is any
git grep -rn "eslint-disable.*no-explicit-any"          # the declared any, countable
```

Neither finds the absorbed form. Probe it at the call site with `IsAny<T>` — the probe, its controls, and the `declare module` composition that turns one of these shorthand declarations into a real type are in `tsc-blindspots`.

## Open questions

- Which of the ten shorthand declarations are actually imported, and from which packages? Settled by resolving importers per specifier, not by the file list.
- Do any package `src` files re-export a value sourced from one of them, publishing the `any` through a `.d.ts`? Settled by an `IsAny<T>` probe against each package's built declaration output, not against its source.
- Whether every package tsconfig includes `../../types`, or only some. Checked here for `network-controller` only; settled by reading the `include` of each `packages/*/tsconfig.json`.
