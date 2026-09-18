---
repo: metamask-extension
parent: derive-types
---

# Deriving in `metamask-extension`

Most authoritative types this repo uses are **not in this repo**. `package.json` carries 134
`@metamask/*` dependencies at caret ranges, resolving through `node_modules` to built declarations
(`dist/index.d.cts`). There is no `paths` mapping to sibling source.

Paths, line numbers and counts below are verified against `origin/main` (2026-08-31), not a working
tree — a local checkout can sit far enough behind that every line number in this file is wrong.

That is what makes deriving non-optional here. Upstream shapes change on a lockfile bump the
extension *performs* but does not *author*. A derived type fails the build at that bump, where you
can see it. A hand-written copy keeps compiling and is now wrong.

## Where to look, in order

1. `node_modules/@metamask/<pkg>` — the published state, action and event types from `core`.
2. `app/scripts/controllers/` — 40 extension-local controllers, including 15 generated
   `*-method-action-types.ts` files that derive `handler: Controller['method']`.
3. `shared/types/background.ts` and `ui/store/types.ts` — the already-derived spine below.

## The spine is already derived — join it, don't re-derive it

**Background state.** `shared/types/background.ts` builds the redux `metamask` slice type twice and
asserts the two agree:

- `ControllerStatePropertiesEnumerated` — one indexed access per property into an upstream state
  type (`transactions: TransactionControllerState['transactions']`, 255 rows in all).
- `ControllerStateTypesMerged` — the intersection of those same `*State` types.
- `FlattenedBackgroundStateProxy` — `IsEquivalent<Enumerated, Merged> extends true ? … : never`.

That last line is a drift alarm, not decoration. When an upstream package adds or removes a state
property, the two sides disagree and the whole redux slice type collapses to `never`, which fails
loudly across the UI. `IsEquivalent` lives in `shared/types/type-level-utils.ts`.

**Redux state.** `ui/store/types.ts` derives the root from the store rather than declaring it:

```typescript
type Store = ReturnType<typeof configureStore>;
export type MetaMaskReduxState = ReturnType<Store['getState']>;
export type MetaMaskReduxDispatch = Store['dispatch'];
```

So UI types derive from `MetaMaskReduxState['metamask'][…]`, never from a fresh import of the
controller state — that path already carries the `IsEquivalent` guard. `ui/store/actions.ts` uses
`MetaMaskReduxState['metamask']` as the background-call return type in several places.
`configureStore`'s input type uses `Omit<RootReducerReturnType, …>` to override the slices redux
infers as `never`, which is derive-then-override rather than restate.

**Messenger clients.** `app/scripts/messenger-client-init/controller-list.ts` declares the
`MessengerClient` union over imported controller classes, then
`MessengerClientFlatState = AccountOrderController['state'] & AccountsController['state'] & …`.
`types.ts` derives the rest from the union — `MessengerClientName = MessengerClient['name']`,
`MessengerClientByName` as a mapped type, `MessengerClientPersistedState` from that.

**Root messenger.** `app/scripts/lib/messenger.ts` derives the root action and event unions from
the factory table:

```typescript
type ChildMessengers = ReturnType<
  (typeof MESSENGER_FACTORIES)[keyof typeof MESSENGER_FACTORIES]['getMessenger']
>;
export type RootMessengerActions = MessengerActions<ChildMessengers> | DefaultActions;
```

Registering a factory in `MESSENGER_FACTORIES`
(`app/scripts/messenger-client-init/messengers/index.ts`) widens the root union with no hand edit.
`messenger-client-init/utils.ts` derives each init function's messenger parameters the same way,
via `ReturnType<(typeof MESSENGER_FACTORIES)[Name]['getMessenger']>`.

## Config that bears on derivation

- Extends `@tsconfig/node22`, which supplies `strict`, `skipLibCheck` and `module`/
  `moduleResolution: node16`. Strictness is inherited, not set locally — do not read its absence
  from `tsconfig.json` as it being off. Node16 means subpath exports resolve, so
  `@metamask/profile-sync-controller/auth` is a legal place to find an authoritative type
  (`app/scripts/lib/state-utils.ts:1`).
- `noUncheckedIndexedAccess` is **not** set. Deriving an element type out of a `Record` gives the
  value type, not `value | undefined`.
- `isolatedModules: true` — re-export derived types with `export type { … }`.
- `lib: ["DOM", "es2023"]`, `jsx: react`, `allowJs: true`. `allowJs` means a `typeof` derivation can
  land on an untyped JS module and silently widen; check what the source file actually is.
- `import-x/no-restricted-paths` is `error` (`.eslintrc.js:838`, architectural zones per ADR 0021
  `modularize-routes`). Deriving across a zone boundary needs `import type` plus the documented
  disable — `shared/types/background.ts` opens with exactly that, on the grounds that type imports
  are stripped at runtime.
- `@typescript-eslint/no-explicit-any` is `error` (`.eslintrc.js:162`). `Record<string, unknown>`
  passes that rule and is the shape the parent skill's `getMetaMaskState` example was rejected for;
  a clean lint run is not evidence a type was derived.

## The generated action types are enforced here too

The 15 `app/scripts/controllers/*-method-action-types.ts` files derive `handler: Controller['method']`
exactly as `core`'s do, and they run the same tool: `@metamask/messenger-cli` (published from
`core`'s `packages/messenger-cli`) supplies the `messenger-action-types` binary, and
`yarn messenger-action-types:check` is the last step of this repo's `lint` script. Regenerate with
`yarn messenger-action-types:generate`; never hand-edit an action's handler signature. Tooling also
knows these files are generated (`.eslintrc.js:872`, `oxfmt.config.mts:13`).

That the extension and `core` share one generator is the practical form of this skill's cross-repo
point: the action types on both sides of the package boundary are produced from the same class
methods by the same binary, so the only way they can disagree is if someone writes one by hand.
