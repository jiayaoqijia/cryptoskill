---
repo: metamask-extension
parent: tsc-blindspots
---

# Blind spots — metamask-extension

What this repo's configuration does **not** check, and what that means for the
parent skill's five divergence shapes. How to *run* the two-arm proof here — heap,
probe location, the authoritative-source table, the `chrome.*` caveat — is
[references/metamask-extension.md](../references/metamask-extension.md).

Every line number and count below was read from `origin/main`
(`git show origin/main:<path>`), not from a working tree.

## `tsconfig.json` does not show you the strictness

The local file names exactly one strictness flag, `useUnknownInCatchVariables`.
Everything else arrives through `"extends": "@tsconfig/node22/tsconfig.json"`.
Resolve it before concluding anything is off:

```bash
npx tsc -p tsconfig.json --showConfig
```

That prints `strict`, `strictNullChecks`, `strictFunctionTypes`, `noImplicitAny`,
`alwaysStrict`, `strictBindCallApply`, `strictPropertyInitialization` and
`strictBuiltinIteratorReturn` all `true`, plus `target: es2022` and
`skipLibCheck: true` — none of which appear in `tsconfig.json`.

**The failure this causes is under-reporting.** An auditor greps the local file for
`strict`, finds nothing, and downgrades a real nullability divergence to "tsc
wouldn't have caught it anyway." It would: `strictNullChecks` is on, so a dropped
`| undefined` (parent shape 2) *does* surface in a probe here.

`noUncheckedIndexedAccess` is genuinely absent — the repo has three tsconfigs
(`tsconfig.json`, `development/webpack/tsconfig.webpack.json`,
`test/e2e/playwright/llm-workflow/tsconfig.json`) and none sets it.

## 300 Storybook files are outside `tsc` *and* outside the lint rule

The strongest blind spot in this repo, because it removes both checks at once and
neither absence is visible from the file you are reviewing.

`tsconfig.json` excludes them, with the reason stated:

```jsonc
"exclude": [
  // don't typecheck stories, as they don't yet pass the type checker.
  "**/*.stories.tsx",
  "**/*.stories.ts"
],
```

**300** `.stories.ts`/`.stories.tsx` files on `main`, all under `include` paths.

The lint half follows from how the config is built. `.eslintrc.js:26-28` parses the
tsconfig with the TypeScript API —

```js
const tsconfigPath = ts.findConfigFile('./', ts.sys.fileExists);
const { config } = ts.readConfigFile(tsconfigPath, ts.sys.readFile);
const tsconfig = ts.parseJsonConfigFileContent(config, ts.sys, './');
```

— and `.eslintrc.js:148` scopes the block carrying `no-explicit-any` to
`files: tsconfig.fileNames.filter((f) => /\.tsx?$/u.test(f))`. **The rule's scope
is the tsconfig program.** A file excluded from the tsconfig is excluded from the
rule by construction.

The repo documents the consequence at `.eslintrc.js:687-688`, in the comment above
the `**/*.stories.js` override: *"This block is for overriding settings from the
base config. It's JavaScript-only because the Storybook TypeScript files don't have
the base config applied."* The one block that does match `.stories.ts(x)`
(`.eslintrc.js:674-683`) sets only `color-no-hex` and `storybook/no-redundant-story-name`
— it does not restore anything.

So in a `.stories.tsx` file: no `tsc`, no `no-explicit-any`, and no
`no-unsafe-*` (those are off repo-wide anyway, below). A hand-written type there is
unfalsifiable in the parent skill's Step 1 sense, and an `any` there is invisible to
every gate. Note the asymmetry — the 156 `.stories.js` files **do** get the base
config; only the TypeScript ones lost it.

**For review:** a migration PR that adds or edits a `.stories.tsx` has had none of
its types checked. Say so rather than treating a green CI as coverage.

## The JS boundary, sized

`allowJs: true` and `checkJs` unset. The parent reference explains why
`app/scripts/background.js` matters; the number is the part worth knowing. Counts
under `include` (`app`, `development`, `shared`, `test`, `types`, `ui`) on `main`:

| | Count |
|---|---|
| `.js` | 1,182 |
| `.ts` / `.tsx` | 7,374 (of which **300** are `.stories.ts(x)`, excluded above) |
| `.js` carrying `@ts-check` | **1** (`development/lib/build-type.js`) |

Roughly one included file in seven asserts nothing and is checked against nothing.
A type hand-written for a function whose callers are all in that seventh is
unfalsifiable — probe it, but expect Arm B to stay silent, and report that as
*unconstrained* rather than as *cleared*.

## Unchecked indexing, in one function

`noUncheckedIndexedAccess` is off, so `record[key]` and `arr[i]` both yield `T`,
never `T | undefined`. `shared/lib/network.utils.ts:238-256` shows the whole class
in nineteen lines:

```ts
const enabledEip155Networks =
  enabledNetworkMap[KnownCaipNamespace.Eip155] ?? {};   // :243  guard the author wrote

const chainIds = Object.entries(enabledEip155Networks)
  .filter(([_chainId, isEnabled]) => isEnabled)
  .map(([chainId, _isEnabled]) => chainId) as Hex[];    // :247  escape hatch on the key type

return chainIds
  .map((chainId) => networkConfigurationsByChainId[chainId])
  .filter((config) => config !== undefined)             // :251  guard the author wrote
  .map(
    (config) =>
      config.rpcEndpoints[config.defaultRpcEndpointIndex].networkClientId,  // :254  no guard
  );
```

The record lookup at `:250` is typed `NetworkConfiguration`, so the `!== undefined`
filter at `:251` is guarding against something the compiler says cannot happen — the
author supplied it from knowledge of the data. Two lines later the array index at
`:254` is dereferenced immediately with no equivalent guard, and the compiler asked
for neither. If `defaultRpcEndpointIndex` is ever out of range the throw is at
runtime and `tsc` is green.

**For review:** a hand-written guard on an index expression is evidence the author
knew the lookup could miss. Ask why the sibling index in the same expression has
none. `shared/lib/selectors/networks.ts:88` is the same shape with the cast form —
`networkConfigurationsByChainId[chainId as Hex]` on a parameter declared `string`.

## `skipLibCheck: true` — declarations are not checked

Inherited from the base. Every `.d.ts` is exempt: the eleven files in `types/` and
every dependency's declarations.

`types/lavamoat__lavadome-core.d.ts` is a bodiless `declare module
'@lavamoat/lavadome-core';`, which types the entire module `any`. The package ships
no types (no `types`/`typings` field, no `.d.ts` in the package), so hand-writing is
the parent's Step 2 case 7 — correct in principle. The defect is that the shim
asserts `any` where it could assert a shape. I found no `.ts`/`.tsx` importer under
`app`, `shared` or `ui`; a `.js` importer would be invisible to `tsc` regardless.

## The lint layer changes what you can grep for

`.eslintrc.js:162` sets `@typescript-eslint/no-explicit-any` to `'error'`, in the
override at `.eslintrc.js:148` scoped to the tsconfig program.

**That is a re-enable, not a repo quirk.** The shared config
`@metamask/eslint-config-typescript` sets `no-explicit-any` to `'off'`, and all
three repos here turn it back on locally — extension at `.eslintrc.js:162`, mobile
at `.eslintrc.js:170`, core in `eslint.config.mjs` under the comment *"Enable rules
that are disabled in `@metamask/eslint-config-typescript`"*. Do not build a contrast
out of it.

**Consequence for parent §7 (false precision):** you cannot find an absorbed `any`
by grepping for `any`, because writing one is a lint error. The rule pushes authors
to `as` instead, which is why the parent's "escape hatches are the tell" section is
the productive search here. Use `IsAny` at the call sites, not a grep.

### The five `no-unsafe-*` rules are off in all three repos

The shared config also sets `no-unsafe-argument`, `no-unsafe-assignment`,
`no-unsafe-call`, `no-unsafe-member-access` and `no-unsafe-return` to `'off'`,
across the majors each repo resolves (13.0.0 mobile, 14.1.1 extension, 15.0.0 core).

Those are precisely the rules that report an `any` *flowing into* a typed position —
the thing `no-explicit-any` cannot see because no `any` was written. So the
repo-wide posture is: writing `any` is an error, and letting one arrive and spread
is unreported. That is the parent skill's §7 in configuration form, and it is why
this skill has work to do in all three repos.

### Locally disabled rules

`.eslintrc.js:278-296` disables a block, commented *"removing changes to our shared
ESLint config made after version v9 … TODO: Remove these modifications after the
ESLint v9 update"* — temporary, so a finding these would have caught is not a
decision to accept risk.

| Rule | Line | Note |
|---|---|---|
| `no-floating-promises` | :284 | also off in mobile (`.eslintrc.js:199`) — shared posture, not local |
| `no-unsafe-enum-comparison` | :289 | **redundant** — the shared config already disables it in every resolved major |
| `no-unsafe-function-type` | :291 | the genuinely local disable |

`no-unsafe-enum-comparison` being off — whether locally or via the shared config —
is what matters for this skill: it is the lint counterpart of the parent's first
divergence shape, so a migration that widens an enum-valued field to `string` and
compares it to an enum member is green in **both** `tsc` and lint. Lint silence is
not a clearance for that shape.

## Probe note

`incremental: true` with `tsBuildInfoFile:
node_modules/.cache/typescript/tsconfig.tsbuildinfo` means a cache persists between
Arm A and Arm B. **Open question:** whether that cache can mask a probe diagnostic
under `--noEmit`. I did not test it. If the two arms disagree in a way that does not
track the probe, delete that file and re-run before reporting anything.

A probe file must be inside `include` **and** not match `**/*.stories.ts(x)`, or it
is silently outside the program.
