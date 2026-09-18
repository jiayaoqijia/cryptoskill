---
repo: metamask-extension
parent: avoid-any
---

# `avoid-any` in metamask-extension

## The rule is a re-enable, and the rules that would catch the absorbed case are off

`@typescript-eslint/no-explicit-any` is `'error'` at `.eslintrc.js:162`. That line **restores** a rule the shared config switches off. Extension is on `@metamask/eslint-config-typescript@^14.1.1` (`package.json:620`), whose `src/index.mjs` sets:

- `:50` — `@typescript-eslint/no-explicit-any: 'off'`
- `:73`–`:77` — `no-unsafe-argument`, `no-unsafe-assignment`, `no-unsafe-call`, `no-unsafe-member-access`, `no-unsafe-return`, all `'off'`, under the comment `// Recommended rules that require type information`

Those five are the rules typescript-eslint ships for the absorbed case. Nothing in `.eslintrc.js` turns any of them back on. So the parent skill's declared/absorbed split is this repo's literal configuration: **a written `any` fails CI, and an absorbed `any` is reported by nothing at all.**

## Three further rules off — extension's distinguishing gap

The comment at `.eslintrc.js:272`–`:276` introduces a block of reversions — *"removing changes to our shared ESLint config made after version v9 … a temporary measure to get us to ESLint v9 compatible versions, at which point we can restore the intended rules"* — and the rules it governs run from `:277` to `:306`. Three of them bear on `any`:

- **`no-floating-promises: 'off'` (`:284`)** — with the `no-unsafe-*` rules also off, a call whose return is absorbed `any` and a call that drops a real promise are the same unreported line. This rule is the last one that would have noticed the value was thenable.
- **`no-unsafe-enum-comparison: 'off'` (`:289`)** — comparing an enum member against a value that is `any` typechecks. Note this one is **not** extension-specific: the shared config already disables it at `src/index.mjs:82` (`// Recommended rules that we do not want to use`), so `:289` is redundant and the gap exists in mobile and core too.
- **`no-unsafe-function-type: 'off'` (`:291`)** — **this one is extension-only.** `Function` accepts any argument list and returns `any`, so `const f: Function` is an `any`-producing annotation with no `any` written. Mobile and core do not disable it, and it ships in typescript-eslint v8's `recommended` (verified in `@typescript-eslint/eslint-plugin@8.54.0`, `dist/configs/flat/recommended.js`).

A fourth rule looks tightened and is not. `restrict-template-expressions` gets a local config at `:262` (`allowBoolean`, `allowNumber`) — the same option object the shared config already passes at `src/index.mjs:171`–`:177`. Neither sets `allowAny`, whose default is `true` (`@typescript-eslint/eslint-plugin`, `dist/rules/restrict-template-expressions.js`, `defaultOptions`). So `` `${value}` `` with an `any` operand is permitted. Same conclusion in core, by the same default; in mobile the rule is `'off'` outright.

## Where the absorbed `any` enters here

**The `.js` boundary is the largest of the three repos.** `tsconfig.json` sets `allowJs: true` and never sets `checkJs`. Inside its `include` (`app`, `development`, `shared`, `test`, `types`, `ui`) there are **1,182 `.js`/`.jsx` files against 7,373 `.ts`/`.tsx`** (`origin/main`, 2026-08-31). An untyped JS export's parameters and return are `any` at every TS call site, with zero diagnostics — verified by probe under `--strict` (`IsAny<Parameters<typeof f>[0]>` resolves `true`, `tsc` exits 0).

**Two bodyless ambient module declarations**, of 16 `declare module` lines in the repo:

- `shared/lib/declare-modules.d.ts:1` — `declare module 'human-standard-token-abi';`
- `types/lavamoat__lavadome-core.d.ts:1` — `declare module '@lavamoat/lavadome-core';`

A shorthand declaration types **every** import from that module as `any`, silently, under `strict` (verified by the same probe). Both files are inside `include`.

**The 300 story files get neither `tsc` nor the rule, and the two exclusions compound.** `.eslintrc.js:26`–`:28` builds a `tsconfig` object from `tsconfig.json` with the TypeScript API — `ts.findConfigFile`, `ts.readConfigFile`, `ts.parseJsonConfigFileContent` — and `:148` uses `tsconfig.fileNames` as the `files` list for the block that carries `no-explicit-any`. So the rule's scope *is* the tsconfig program. `tsconfig.json` excludes `**/*.stories.ts` and `**/*.stories.tsx` (`:31`–`:32`) — **300 files on `origin/main`** — which puts them outside `fileNames` and therefore outside the rule as well. The repo says so itself, in the docblock at `.eslintrc.js:684`–`:691`: *"Storybook (JavaScript only) … This block is for overriding settings from the base config. It's JavaScript-only because the Storybook TypeScript files don't have the base config applied."* In those 300 files an explicit `any` is not an error and an absorbed `any` is not even typechecked.

The same mechanism generalises: any `.ts`/`.tsx` file outside `tsconfig.json`'s `include` list is outside `no-explicit-any` too, silently, with no entry in `.eslintrc.js` naming it. Beyond the stories that is currently 3 files, all under `.devcontainer/` (7,379 `.ts`/`.tsx` on `origin/main`; 7,373 in the `include` dirs, 3 at repo root matching `*.ts`). The hole is real and small — it is the stories that carry it.

The parent skill's own absorbed example (`shared/lib/token-util.ts`, ethers dynamic-method results) is extension code; it is the shape to expect wherever a precise signature sits downstream of ethers, a `.js` module, or one of the two shorthand declarations above.

## Two settings that are not `any` sources, so they don't belong in this hunt

- `useUnknownInCatchVariables: true` is set explicitly in `tsconfig.json` (already implied by the inherited `strict`). Catch bindings are `unknown`, so no `catch (e: any)` is needed.
- `noUncheckedIndexedAccess` is not set. That widens indexing results, not `any` — a replacement for a bodyless declaration typed `Record<string, X>` will read as total when it is not.

`strict` is inherited from `@tsconfig/node22` (`node_modules/@tsconfig/node22/tsconfig.json`), not declared locally — a local `tsconfig.json` edit that changed `extends` would drop `noImplicitAny` with nothing in the file mentioning it.

## Checking it

```bash
git grep -nE "^declare module '[^']+';$" -- '*.d.ts'      # shorthand = whole module is any
git grep -rn "eslint-disable.*no-explicit-any"            # the declared any, countable
```

The absorbed form is invisible to both. Probe it at the call site with `IsAny<T>` — the probe, its controls, and the `declare module` composition that repairs one are in `tsc-blindspots`.

## Open questions

- How many of the 1,182 in-program `.js` files are actually imported from `.ts`? Settled by resolving each `.js` file's importers, not by the file count above.
- Do the two shorthand declarations still need to be shorthand, or do the packages now ship types? Settled by checking each package's `types`/`exports` field at the installed version.
