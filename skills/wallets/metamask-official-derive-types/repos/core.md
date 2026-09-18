---
repo: core
parent: derive-types
---

# Deriving in `core`

Paths, line numbers and counts below are verified against `origin/main` (2026-08-31), not a working
tree — a local checkout can sit far enough behind that every line number in this file is wrong.

`core` is where the authoritative types are *written*. Everything in this repo is a source that
`metamask-extension` and `metamask-mobile` derive from, so a loose or unexported type here becomes
a hand-written copy in two consumers.

## Where the authoritative source lives

Package granularity. `packages/<name>/src/index.ts` is the contract — read it before defining
anything.

| Source | Where |
| --- | --- |
| Controller state, action union, event union, messenger | `packages/<name>/src/<Name>Controller.ts`, re-exported from `src/index.ts` |
| Per-method action types | `packages/<name>/src/<Name>Controller-method-action-types.ts` (generated, 88 files) |
| Get-state action and state-change event builders | `@metamask/base-controller` — `ControllerGetStateAction`, `ControllerStateChangeEvent` |
| Action/event extraction utilities | `@metamask/messenger` — `ExtractActionResponse`, `ExtractActionParameters`, `ExtractEventPayload`, `ActionHandler`, `MessengerActions`, `MessengerEvents` |
| Schema-backed types | `Infer<typeof Schema>` from `@metamask/superstruct` |

## The generated action types are the source, not a convenience

A controller lists its exposed methods in `MESSENGER_EXPOSED_METHODS` (94 files under `packages/`
do). The generator turns each into an action whose handler is an indexed access on the class:

```typescript
// packages/accounts-controller/src/AccountsController-method-action-types.ts (generated)
export type AccountsControllerGetAccountAction = {
  type: `AccountsController:getAccount`;
  handler: AccountsController['getAccount'];
};
```

`yarn messenger-action-types:check` runs inside the root `lint` script, so a hand-written
handler signature that disagrees with the method is a lint failure, not a silent drift. Add the
method name to `MESSENGER_EXPOSED_METHODS` and regenerate; never write the action type by hand.

The state action and change event are derived the same way, from `base-controller` generics
rather than restated:

```typescript
// packages/accounts-controller/src/AccountsController.ts
export type AccountsControllerGetStateAction = ControllerGetStateAction<
  typeof controllerName,
  AccountsControllerState
>;
```

## Prefer the messenger's own extractors

`@metamask/messenger` exports `ExtractActionResponse<Action>` and `ExtractActionParameters<Action>`,
which do what the parent skill's `ReturnType<Action['handler']>` / `Parameters<...>` do but are
matched to the action shape. Reach for them first inside `core`.

Measured caveat, so you know what you are adopting: outside `packages/messenger` these are almost
unused — `ExtractEventPayload` has one non-test call site (`AccountsController.ts:933`) and
`ExtractActionResponse` has none. They are exported and correct; they are not yet the prevailing
idiom, and `ReturnType` is what you will find in review.

## Deriving across a package boundary

`tsconfig.base.json` sets `composite: true`, and `tsconfig.packages.json` maps
`"@metamask/*": ["../*/src"]`. So a cross-package type import typechecks against the sibling's
**uncompiled source** — no build step stands between you and the authoritative type, and there is
no reason to copy a shape because "the other package isn't built."

One edit makes a new cross-package derivation legal, and the rest is generated: add the package to
`dependencies` (or `devDependencies`) in `packages/<yours>/package.json`, then run
`yarn lint:tsconfigs:fix`. `scripts/lint-tsconfigs/lint-package-tsconfigs.mts` derives the expected
`references` in both `tsconfig.json` and `tsconfig.build.json` from the manifest's dependencies and
writes them; `yarn lint:tsconfigs:all` enforces the result inside the root `lint` script. Do not
hand-maintain the `references` arrays.

Those entries do not affect resolution — `paths` already did that. They order `tsc --build`.

`packages/bridge-controller/src/types.ts` is the worked example: it derives against types imported
by package name from eleven sibling `@metamask/*` packages, and derives 13 more with
`Infer<typeof …Schema>`.

## Config that bears on derivation

- `module` / `moduleResolution` are `Node16`, so package `exports` subpaths resolve natively.
- `strict: true`; `noUncheckedIndexedAccess` is **not** set. `State['someRecord'][key]` is the
  value type, not `value | undefined` — a type derived out of a `Record` will claim more than the
  runtime guarantees.
- `isolatedModules: true` — re-export derived types with `export type { … }`.
- `@typescript-eslint/no-explicit-any` is `error` (`eslint.config.mjs:152`). The legal escape from
  that rule is a too-wide hand-written type, which the parent skill's cast-tax argument covers;
  passing the lint rule is not evidence the type was derived.

## Open

- Whether `ExtractActionResponse` / `ExtractActionParameters` are intended to become the house
  idiom or stay internal to `packages/messenger`. Settled by asking the messenger package owners,
  or by a decision record in `MetaMask/decisions`.
