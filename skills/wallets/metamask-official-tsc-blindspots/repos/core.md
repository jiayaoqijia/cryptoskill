---
repo: core
parent: tsc-blindspots
---

# Blind spots — core

What `MetaMask/core`'s configuration does **not** check. One of the parent skill's
classes does not exist here and two exist only here, so do not carry the extension
or mobile playbook across unchanged.

Every line number and count below was read from `origin/main`
(`git show origin/main:<path>`), not from a working tree. This matters more here
than in the other two: a local branch a few hundred commits behind reports a
different package count and different reference lists.

## The JS boundary does not exist here — say so, do not omit it

`tsconfig.base.json` does not set `allowJs`, and it is absent from the resolved
options for a package (`npx tsc -p packages/assets-controllers/tsconfig.json
--showConfig`). Independently, `packages/*/src` contains **0** `.js` files against
**2,052** `.ts`.

So the parent skill's central premise — *"across a JavaScript boundary (`checkJs`
off) it checks nothing at all"* — has no instance in core. A review that reports
"the callers are still `.js`, so this type is validated against nothing" is wrong
here, and a `checkJs` finding copied from an extension review does not transfer.

State this explicitly in a core review rather than leaving it out.

## The repo-wide typecheck covers 14 of 98 packages

The largest blind spot here, and it is not a compiler setting — it is which files
the compiler is pointed at.

`lint` begins with `lint:tsc`, which is `tsc --build tsconfig.lint.json`, and CI
runs it as a matrix entry in `.github/workflows/lint-build-test.yml:91`. But
`tsconfig.lint.json` declares its own `references` — **14 entries** — and that is
the whole graph: `references` is not inherited through `extends`, so extending
`tsconfig.json` (99 entries, 98 unique) does not widen it. Checked with a two-config
fixture and `--showConfig`: a child declaring one reference over a base declaring
two resolves to **one**, and a child declaring none resolves to **no `references`
key at all** — overridden, never merged. Independently, exactly **14** of the **98**
packages have a `tsconfig.lint.json` for it to point at. The config says so itself: *"This configuration
incrementally enables repository-wide type checking."*

The 14: `announcement-controller`, `app-metadata-controller`, `base-controller`,
`build-utils`, `client-controller`, `foundryup`, `local-node-utils`, `messenger`,
`messenger-cli`, `platform-api-docs`, `preferences-controller`,
`rate-limit-controller`, `stellar-quickstart-up`, `storage-service`.

The other 84 are typechecked by the **Build** job instead
(`lint-build-test.yml:194-231`), which runs `ts-bridge` over a tsconfig generated
from the changed packages (`scripts/generate-partial-build-tsconfig.mts`), falling
back to `yarn build` over all 98. Different entry point, different config chain,
different scope per PR.

**So "core is green" is a claim about one of two graphs, and neither is the whole
repo on every run.** Name the command you ran. Before reporting that a probe was
silent, confirm the package you probed is in the graph you invoked — a probe in one
of the 84 is not covered by `lint:tsc` at all.

## Unchecked indexing — and it is not uniform across packages

`tsconfig.base.json` does not set `noUncheckedIndexedAccess`, so `record[key]` and
`arr[i]` yield `T`, never `T | undefined`. But three configs opt in:

| Config | Line |
|---|---|
| `packages/json-rpc-engine/tsconfig.json` | :9 |
| `packages/eth-json-rpc-provider/tsconfig.json` | :9 |
| `tsconfig.scripts.json` | :19 |

That is **2 of the 98 package tsconfigs**, plus the scripts config. Read the
package's own file before concluding an index expression is unchecked — the answer
differs by directory, which no other MetaMask repo here requires you to check.

The same expression appears both guarded and unguarded in two files of one package,
`packages/assets-controllers`:

```ts
// packages/assets-controllers/src/TokenBalancesController.ts:590-592  (also :606-608)
const networkConfig = networkConfigurationsByChainId[chainId];
const { networkClientId } =
  networkConfig.rpcEndpoints[networkConfig.defaultRpcEndpointIndex];

// packages/assets-controllers/src/AccountTrackerController.ts:629-636
return popularEvmChainIds
  .map((hexChainId) => {
    const networkConfig = networkConfigurationsByChainId[hexChainId];
    return networkConfig?.rpcEndpoints[
      networkConfig.defaultRpcEndpointIndex
    ]?.networkClientId;
  })
  .filter((id): id is NetworkClientId => id !== undefined);
```

Two index operations each, both typed non-nullable under `strict: true`. The second
site guards both with `?.` and then needs the type-predicate `.filter` to remove
the `undefined` it introduced by doing so; the first guards neither and destructures
straight through. `tsc` has no opinion about either, so consistency on this axis is
a review property in core, not a checked one.

### A package's source is checked under stricter settings than its emitted types

`packages/json-rpc-engine/tsconfig.json` sets `noUncheckedIndexedAccess` and
`exactOptionalPropertyTypes`; its `tsconfig.build.json` sets neither — it extends
`tsconfig.packages.build.json`, which does not. **0 of the build configs set
either.** So a package's source is checked under stricter settings than the `.d.ts`
consumers read is emitted under.

**Open question:** whether that asymmetry changes any emitted signature — an
inferred return type of a function returning `arr[i]` is the candidate. I did not
test it. Settle it by building the package and diffing the emitted `dist/*.d.ts`
against one emitted with the flags added to `tsconfig.build.json`.

## Bodiless ambient shims — verified `any` at live call sites

Ten files under `types/` are a single line of the form `declare module 'x';` with no
body, which types the entire module `any`. Every package includes them —
`"include": ["../../types", "./src", "../../tests"]`.

Two cases, needing different remedies:

**1. The shim overrides a package that ships its own types.**
`@metamask/metamask-eth-abis` has `"types": "dist/index.d.ts"` in its
`package.json`, and `types/@metamask/metamask-eth-abis.d.ts` shadows it. Verified
with the parent skill's substitution method, replicating a package's arrangement
(`strict`, `module`/`moduleResolution` `Node16`, `target ES2020`,
`lib ES2020 + DOM`, core's `node_modules`):

```ts
import { abiERC20 } from '@metamask/metamask-eth-abis';
import contractMap from '@metamask/contract-metadata';
type IsAny<T> = 0 extends 1 & T ? true : false;
const abiIsAny: IsAny<typeof abiERC20> = true;
const mapIsAny: IsAny<typeof contractMap> = true;
```

- With `types/**/*.d.ts` in `include`: **clean**, and flipping either to `false`
  errors `TS2322` — so both are `any`.
- With `types/` removed from `include`: `abiIsAny` errors (`Type 'true' is not
  assignable to type 'false'`) — the shipped declarations resolve and `abiERC20` is
  **not** `any`.

The probe ran against an older checkout, but both inputs match `main`: the shim file
is byte-identical, and `main` declares `@metamask/metamask-eth-abis@^3.1.1` against
the probed 3.1.1 with `types: dist/index.d.ts`.

The shim is what makes it `any`, at these importers under
`packages/assets-controllers/src/` — `Standards/ERC20Standard.ts:6`,
`TokensController.ts:31`, `Standards/NftStandards/ERC1155/ERC1155Standard.ts:11`,
`Standards/NftStandards/ERC721/ERC721Standard.ts:11` — and outside that package at
`packages/bridge-controller/src/bridge-controller.ts:8` and
`packages/bridge-controller/src/utils/balance.ts:5`. This is parent §7 false
precision with a source you can delete: remove the shim.

**2. The shim stands in for a package with no types.**
`@metamask/contract-metadata` has no `types`/`typings` field; with `types/` removed
the import is `TS7016`. Hand-writing is the parent's Step 2 case 7 — correct in
principle. The defect is that the shim asserts `any` rather than a shape, so
`contractMap` is `any` at `packages/assets-controllers/src/TokensController.ts:16`,
`.../TokenDetectionController.ts:10` and
`packages/client-utils/src/mappers/helpers/token-metadata.ts:1`.
`single-call-balance-checker-abi` is the same case, at
`.../AssetsContractController.ts:19`.

Two gates that cannot see either case. `@typescript-eslint/no-explicit-any` is
`'error'` in `eslint.config.mjs`, under the comment *"Enable rules that are disabled
in `@metamask/eslint-config-typescript`"* — and no `any` is written anywhere, so it
has nothing to match. (That re-enable is not distinctive: extension and mobile do
the same, over the same shared default.) And `skipLibCheck` does not help either
way — a bodiless `declare module` is well-formed, so checking declarations finds
nothing wrong with it.

## Project references — two entry points that resolve differently

`composite: true` in `tsconfig.base.json`. Every package tsconfig lists its
dependencies under `references`, and every `tsconfig.build.json` references the
other packages' `tsconfig.build.json`. This is a class the other two repos do not
have, and the first thing to get right is which config you ran.

**The `paths` mapping is not inherited by every entry point.**
`tsconfig.packages.json` sets `"@metamask/*": ["../*/src"]`, commented *"we ensure
that TypeScript resolves `@metamask/*` imports to the uncompiled source code."*

| Config | Extends | Carries the `src` mapping |
|---|---|---|
| `packages/*/tsconfig.json` | `tsconfig.packages.json` | yes |
| `packages/*/tsconfig.build.json` | `tsconfig.packages.build.json` → `tsconfig.packages.json` | yes |
| `tsconfig.json` (root, `noEmit`) | `tsconfig.base.json` **directly** | **no** |

So the root config is the one whose cross-package imports fall through to normal
`Node16` resolution and the package's `types` field, and the per-package configs —
lint *and* build alike — are the ones pointed at source.

**Open question:** which file each entry point actually loads for a cross-package
import, since project references also redirect to declaration output. I did not
test it. Settle it before citing any typecheck as evidence about a cross-package
type:

```bash
npx tsc -p packages/<pkg>/tsconfig.json --explainFiles | grep -i '<dep-pkg>'
npx tsc --build tsconfig.lint.json --verbose --traceResolution 2>&1 | grep -i '<dep-pkg>'
```

**Open question:** whether `tsc --build` here can report clean over an out-of-date
`dist/*.d.ts`. Both `build:types` and `lint:tsc` use `--build`, and `build:types`
already passes `--verbose`, which prints the up-to-date decision per project — read
that log rather than the exit code.

What holds regardless of the resolution question: **consumers outside the repo read
`dist/*.d.ts`**, and no check inside core exercises that path from a consumer's
position. Mobile goes further and hardcodes paths *into* that `dist/` in its own
`tsconfig.json` (see the mobile overlay). A type correct against `src` and stale in
`dist` is invisible here and lands there.

**Every typecheck that actually runs sets `skipLibCheck`.** Both
`tsconfig.packages.lint.json` and `tsconfig.packages.build.json` set it `true`, as
does the root `tsconfig.lint.json`. The per-package `tsconfig.json` — the one an
editor picks up for a file under `packages/*/src` — does not. So declarations are
checked in the editor and skipped by both CI paths, which is the wrong way round
for catching a bad `.d.ts`.

## Probe note

`lib` is `["ES2020", "DOM"]`, so a DOM-typed probe compiles here. It does not in
mobile. `module` and `moduleResolution` are `Node16`, matching extension and not
mobile — a probe is portable between core and extension, and is not portable to
mobile without rewriting its imports.

Put the probe in a package that is in the graph you are running. In one of the 84
packages outside `tsconfig.lint.json`, `yarn lint:tsc` will not read it.
