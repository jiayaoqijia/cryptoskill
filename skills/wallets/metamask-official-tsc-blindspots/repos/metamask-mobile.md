---
repo: metamask-mobile
parent: tsc-blindspots
---

# Blind spots — metamask-mobile

**Scope of this file.** `tsconfig.json`, `.eslintrc.js` and `package.json` were read
from `main` via `gh api repos/MetaMask/metamask-mobile/contents/<path>`, so every
config claim below is verified. The repo is **not checked out**, so there are **no
verified call sites** — statements about actual code are open questions with the
command that settles them. Add examples on the first real review; the extension and
core overlays show the form.

## Strictness is local — the extension's audit trap does not apply

`strict: true` is set in `tsconfig.json` itself, not inherited. A reader auditing
that file sees it, which is the opposite of extension, where `strict` arrives
through `@tsconfig/node22` and is invisible locally.

Two flags that matter here are still not part of `strict`:

- **`noUncheckedIndexedAccess` is not set.** Next section.
- **`skipLibCheck: true` is set**, so no `.d.ts` is checked — the same posture as
  extension, and the same as every typecheck core actually runs.

## Unchecked indexing

`record[key]` and `arr[i]` yield `T`, never `T | undefined`. Under `strict: true`
this is the one nullability hole left open, and it is the one that reaches runtime —
as a property access on `undefined`, not as a type error.

The source roots are `app/`, `tests/` and `scripts/` (from `include`; `app/**/*` is
the bulk). Find an index expression dereferenced immediately, and a hand-written
runtime guard on an index expression sitting beside one that has none:

```bash
grep -rnE '\]\.[a-zA-Z]' app --include=*.ts --include=*.tsx | grep -v '\.test\.'
grep -rnE '\?\.\[|\]\?\.' app --include=*.ts --include=*.tsx | grep -v '\.test\.'
```

A guard the compiler did not ask for is evidence the author knew the lookup could
miss; the sibling index without one is the finding. Both core and extension carry
that exact pair on `networkConfigurationsByChainId[chainId]` followed by
`rpcEndpoints[defaultRpcEndpointIndex]`. **Open question:** whether it appears here.
Settle with `grep -rn "rpcEndpoints\[" app --include=*.ts`.

## Hand-written `paths` into dependency `dist/` — a class the other two lack

`tsconfig.json` maps roughly twenty subpath imports directly at declaration files
inside `node_modules`, with the reason stated: *"TODO: Remove these once we use
`Node16` module resolution."* `moduleResolution` is `node`, which cannot follow the
`exports` subpaths these packages publish, so the paths are written out by hand:

```jsonc
"@metamask/json-rpc-engine/v2": ["node_modules/@metamask/json-rpc-engine/dist/v2/index.d.cts"],
"@metamask/keyring-api/v2":     ["node_modules/@metamask/keyring-api/dist/v2/index.d.cts"],
"@metamask/perps-controller/types": ["node_modules/@metamask/perps-controller/dist/types/index.d.cts"],
```

Each is a hand-written claim about another package's build output — the same class
the parent skill is built around, one level up from a type to a file path. Two ways
it fails silently:

1. **The path stops resolving.** A dependency reorganises `dist/`, and the mapping
   points at nothing. Whether that surfaces as an error or as a fallback to normal
   resolution is worth knowing before you trust a green run.
2. **The path resolves to a stale or wrong declaration.** These reach *into* core's
   emitted `dist/`, which core's own checks do not exercise from a consumer's
   position (see the core overlay). A type correct against core's `src` and stale in
   its `dist` is invisible in core and lands here.

**For review:** a PR touching one of these packages' subpath exports should be
checked against this list. **Open question:** whether any mapped path is currently
dead — settle with a loop over the `paths` values testing each file exists, then
`npx tsc -p tsconfig.json --traceResolution` for one of them.

## No DOM lib — this changes how probes are written, not just what compiles

`lib: ["es2022"]`, with `jsx: react-native`. Nothing from `lib.dom.d.ts` is in
scope from `lib`, so a probe borrowing a DOM type fails for a reason that has
nothing to do with the claim under test — the parent skill's Step 5 failure, and
here it is the default outcome of copying a probe from an extension review.

`typeRoots` is unset, so every `@types/*` package is auto-included, and
`@types/node@^24` is a devDependency. Node-declared globals therefore have a
source; DOM-only ones (`document`, `window`, `HTMLElement`, `Event`) do not.
**Open question:** which specific globals resolve. Settle each in one line — a
scratch file inside the `include` paths, then run `tsc`:

```ts
type _Probe = HTMLElement;   // TS2304 if absent
type _Probe2 = typeof fetch; // TS2304 if absent
```

Do the same before using any DOM type in a real probe. Do not infer it from the
other two overlays; core has `DOM` in `lib` and extension has `DOM` plus `es2023`.

## The JS boundary is live

`allowJs: true` and **`checkJs` is not set**, so `.js` files are in the program and
checked against nothing — the same posture as extension. A hand-written type for a
function whose callers are all `.js` can drift indefinitely.

`app/core/InpageBridgeWeb3.js` and `scripts/inpage-bridge/dist` are explicitly
excluded, so they are not even in the program.

Size the boundary before weighting a finding, the way the extension overlay does:

```bash
find app -name '*.js' | wc -l
find app \( -name '*.ts' -o -name '*.tsx' \) | wc -l
grep -rl '@ts-check' app --include=*.js | wc -l
```

## The lint layer

`lint:tsc` is `tsc --project ./tsconfig.json` with a 12 GB heap — one whole-program
typecheck, unlike core, where the equivalent script covers a fraction of the repo.
`lint` runs `eslint '**/*.{js,ts,tsx}'` **by glob**, not by tsconfig program, so
mobile does not have extension's excluded-files-lose-the-rule problem.

`.eslintrc.js:170` sets `@typescript-eslint/no-explicit-any` to `'error'` in the
`*.{ts,tsx}` block at `:155`. **That is a re-enable, not a repo quirk** — the shared
`@metamask/eslint-config-typescript` sets it `'off'`, and all three repos turn it
back on. Consequence: you cannot find an absorbed `any` by grepping for `any`. Use
`IsAny` at the call sites (parent §7), and read escape-hatch clusters as the index.

The same shared config sets all five `no-unsafe-*` rules (`-argument`,
`-assignment`, `-call`, `-member-access`, `-return`) to `'off'` at major 13.0.0,
which mobile resolves. Those are the rules that report an `any` *flowing into* a
typed position — so writing `any` is an error here and letting one arrive and spread
is unreported.

The `*.{ts,tsx}` block disables three rules that matter to this skill:

| Rule | Line |
|---|---|
| `no-floating-promises` | :199 |
| `no-unsafe-enum-comparison` | :206 |
| `restrict-template-expressions` | :221 |

`no-unsafe-enum-comparison` is the lint counterpart of the parent's divergence
shape 1 — a field widened from an enum to `string` and compared against an enum
member is green in **both** `tsc` and lint. Lint silence is not a clearance there.

Two of the three are re-enabled in a narrow override: `.eslintrc.js:471` scopes
`files: ['app/**/*-method-action-types*.ts']`, and that block sets
`no-floating-promises` and `restrict-template-expressions` to `'error'` at
`:628-629`. That is generated-file territory, not a repo-wide restoration — do not
read it as either rule being on.

## Probe note

`module: commonjs` and `moduleResolution: node`, against `Node16` in both extension
and core; `jsx: react-native` against `react`. A probe is **not** portable from
those repos without rewriting its imports. `isolatedModules: true` additionally
requires `import type` / `export type` for type-only positions — a probe that
re-exports a type without `type` errors for the wrong reason, the parent's Step 5
again.

## Open questions, collected

| Question | Settles it |
|---|---|
| Does the `record[k]` then `arr[i]` pair appear? | `grep -rn "rpcEndpoints\[" app --include=*.ts` |
| How big is the `.js` surface? | `find app -name '*.js' \| wc -l` |
| Which DOM-named globals resolve? | one-line `type _P = X;` probe per global |
| Is any `paths` mapping into `node_modules/**/dist` dead? | test each mapped file exists, then `--traceResolution` |
| Are there per-directory tsconfigs overriding the root? | `find . -name 'tsconfig*.json' -not -path '*/node_modules/*'` |
