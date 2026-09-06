---
repo: metamask-extension
parent: controller-integration
---

# Controller Integration into the Extension Background

The integration surface is `app/scripts/messenger-client-init/` (the pattern is called "messenger client" init; types are `MessengerClientInitFunction`/`MessengerClientInitRequest`/`MessengerClientInitResult`). The root `AGENTS.md` "Workflow: Creating a Controller" predates this pattern — follow the steps below instead.

## 1. Path decision

| Path | When | Resolve via |
|---|---|---|
| Modular init (default) | New stateful controller or service | `MESSENGER_FACTORIES` + `*-init.ts`, `this.messengerClientsByName.<Name>` |
| Stateless service | No persisted state (e.g. an API service) | Same as modular, minus state steps |
| Wallet-managed | Name is one of: AccountsController, ApprovalController, ConnectivityController, KeyringController, NetworkController, RemoteFeatureFlagController, StorageService | `this.wallet.getInstance('<Name>')` — construction happens inside `@metamask/wallet` |

Independently of the path above, the controller class itself comes from one of two sources — the `messenger-client-init/` wiring in §3 is identical either way, only step 1 (and where types are imported from) differs:

| Source | When | Where the class lives |
|---|---|---|
| npm package | Controller is owned/shared outside the extension (most new controllers) | `@metamask/<name>-controller`, imported as a dependency |
| Repo-local | Controller is extension-only | `app/scripts/controllers/<name>/` (class + a `<name>-controller.types.ts` exporting the messenger type) — e.g. `app/scripts/controllers/rewards/rewards-controller.ts` |

## 2. Canonical examples (read, don't guess)

| Controller | Copy for |
|---|---|
| `app/scripts/messenger-client-init/geolocation-controller-init.ts` + `messengers/geolocation-controller-messenger.ts` (+ both `.test.ts`) | Default pattern (npm-package controller): init fn, default-state hydration, `api` methods, minimal messenger, tests |
| `app/scripts/messenger-client-init/transaction-pay-controller-init.ts` + `messengers/transaction-pay-controller-messenger.ts` | Separate init messenger used inside constructor callbacks, heavy cross-controller delegation |
| `app/scripts/controllers/rewards/rewards-controller.ts` (+ `rewards-controller.types.ts` exporting `RewardsControllerMessenger`) + `app/scripts/messenger-client-init/rewards-controller-init.ts` + `messengers/rewards-controller-messenger.ts` | Repo-local controller pattern, plus remote-feature-flag gating via init messenger. The init/messenger files are indistinguishable in shape from the npm-package case — only the class import path differs |
| `PerpsController` entries in `app/scripts/metamask-controller.js` + `shared/lib/environment.ts` | Build-flag gating (conditional init-map spread) |
| `app/scripts/messenger-client-init/data-deletion-service-init.ts` | Stateless service |

## 3. Ordered steps

| # | File | Action |
|---|---|---|
| 1 | `package.json`, or `app/scripts/controllers/<name>/` | **npm package**: `yarn add @metamask/<name>-controller`, then `yarn lint:lockfile:dedupe:fix && yarn allow-scripts auto && yarn lavamoat:auto && yarn attributions:generate`. **Repo-local**: create the folder with the controller class and a `<name>-controller.types.ts` exporting the messenger type — mirror `app/scripts/controllers/rewards/` — no dependency commands needed |
| 2 | `app/scripts/messenger-client-init/messengers/<name>-controller-messenger.ts` | Create `getXControllerMessenger` (skeleton below). Add `getXControllerInitMessenger` (namespace `'XControllerInit'`) only if the init fn itself needs actions/events beyond the controller's messenger type |
| 3 | `app/scripts/messenger-client-init/messengers/<name>-controller-messenger.test.ts` | `expect(messenger).toBeInstanceOf(Messenger)`; optionally assert delegation via a `delegate` spy |
| 4 | `app/scripts/messenger-client-init/messengers/index.ts` | Export the factory fns; add to `MESSENGER_FACTORIES`: `{ getMessenger, getInitMessenger: noop }` (lodash `noop`) or the real init-messenger fn |
| 5 | `app/scripts/messenger-client-init/controller-list.ts` | Add the class to the `MessengerClient` union; add `XController['state'] &` to `MessengerClientFlatState` |
| 6 | `app/scripts/messenger-client-init/utils.ts` | Add `'XController'` to `MessengerClientsToInitialize` for typed messenger inference in the init fn |
| 7 | `app/scripts/messenger-client-init/<name>-controller-init.ts` | Create the init fn (skeleton below). UI-facing methods go in the returned `api` — `getApi()` in `metamask-controller.js` is closed for new additions |
| 8 | `app/scripts/messenger-client-init/<name>-controller-init.test.ts` | Use `buildControllerInitRequestMock()` from `./test/utils` (path is `test/utils.ts`) |
| 9 | `app/scripts/metamask-controller.js` | Import the init fn; add `XController: XControllerInit` to `messengerClientInitFunctions` **after every controller it calls during construction** — map insertion order is init order. ⚠️ This file is un-type-checked JS: a typo'd key fails only at runtime |
| 10 | `shared/types/background.ts` | Add each top-level state property to `ControllerStatePropertiesEnumerated` **and** the state type to `ControllerStateTypesMerged` |
| 11 | `app/scripts/lib/state-utils.ts` | ⚠️ Add sensitive top-level property names to `REMOVE_KEYS`/`REMOVE_PATHS` — this is the only filter before UI patches; `persist`/`anonymous` metadata leaves them through |
| 12 | `app/scripts/constants/sentry-state.ts` | Add a `SENTRY_BACKGROUND_STATE.XController` mask only for properties safe to send to Sentry; unlisted state is reduced to its `typeof` automatically |
| 13 | `test/e2e/tests/metrics/state-snapshots/*.json` | Refresh via the e2e run in §7 — any new mem-state key changes these enforced snapshots |
| 14 | `ui/selectors/<domain>.ts` (+ test) | State is **flattened** into `state.metamask` (top-level properties, un-nested); read with `??` fallbacks; derive with `createSelector` |
| 15 | `test/e2e/fixtures/default-fixture.json` + `withXController` in `test/e2e/fixtures/fixture-builder-v2.ts`; `test/data/mock-state.json` | Optional — only when e2e / UI unit tests need seeded state |
| 16 | `.github/CODEOWNERS` | Add `app/scripts/messenger-client-init/<sub>  @MetaMask/<team>` if a team owns a new subfolder |

Persistence and UI state need zero store wiring: the `...controllerPersistedState` / `...controllerMemState` spreads in `metamask-controller.js` pick the controller up under its default keys. A brand-new controller also never needs a migration — init hydrates with `persistedState.X ?? default`.

### Messenger skeleton (step 2)

```ts
import { Messenger, MessengerActions, MessengerEvents } from '@metamask/messenger';
import { RootMessenger } from '../../lib/messenger';

export function getXControllerMessenger(
  messenger: RootMessenger<
    MessengerActions<XControllerMessenger>,
    MessengerEvents<XControllerMessenger>
  >,
): XControllerMessenger {
  const controllerMessenger: XControllerMessenger = new Messenger({
    namespace: 'XController',
    parent: messenger,
  });
  messenger.delegate({
    messenger: controllerMessenger,
    actions: ['OtherController:getState'],
    events: ['OtherController:stateChange'],
  });
  return controllerMessenger;
}
```

`delegate()` is the runtime authorization — the type union alone does not allow `messenger.call(...)`.

### Init function skeleton (step 7)

```ts
export const XControllerInit: MessengerClientInitFunction<
  XController,
  XControllerMessenger
> = ({ controllerMessenger, persistedState }) => {
  const messengerClient = new XController({
    messenger: controllerMessenger,
    state: persistedState.XController ?? getDefaultXControllerState(),
  });
  return {
    messengerClient,
    api: { getThing: messengerClient.getThing.bind(messengerClient) },
  };
};
```

## 4. Deltas

**Stateless service** — skip steps 10-15; in step 5 add to the `MessengerClient` union only; in step 7 return `{ messengerClient, persistedStateKey: null, memStateKey: null }`.

**Wallet-managed** — skip all steps above. Edit the builder in `app/scripts/wallet-init/instance-options/<name>.ts` and, if needed, `app/scripts/wallet-init/initialization.ts`; instances come from `this.wallet.getInstance('<Name>')`.

**Legacy store keys** — `CurrencyController` and `AccountTracker` persist under historical keys via explicit entries in the `metamask-controller.js` store maps; keep those entries intact, persisted user state lives under them.

## 5. Feature gating

| Idiom | Where | Reference |
|---|---|---|
| Init-messenger flag read (lazy, per call) | Constructor callbacks call `initMessenger.call('RemoteFeatureFlagController:getState')` | `rewards-controller-init.ts` |
| Runtime flag subscription | Delegate `'RemoteFeatureFlagController:stateChange'` on the controller messenger; the package reacts itself | `messengers/perps-controller-messenger.ts` |
| Selector gating | `createSelector` over `getRemoteFeatureFlags` | `ui/selectors/config-registry/config-registry.ts` |
| Build flag | `process.env` helper in `shared/lib/environment.ts` + conditional spread in `messengerClientInitFunctions`; guard consumers with `?.` (the extension idiom — mobile-style `ONLY_INCLUDE_IF` fences don't gate controllers here) | `getIsPerpsIncludedInBuild` + the `PerpsController` spread in `metamask-controller.js` |

## 6. Silent failures (no type error — verify manually)

| Mistake | Symptom |
|---|---|
| Init map entry placed before a dependency | Throw `Messenger client requested before it was initialized: <Name>` — move the entry later |
| Typo'd key in `messengerClientInitFunctions` | Fails at runtime in the factory lookup — the JSDoc `@type {InitFunctions}` is advisory only |
| Calling a non-delegated action/event | Runtime rejection from `@metamask/messenger` at call/subscribe time |
| UI methods defined outside the init result `api` | Methods never reach the UI — the connection API is `{...getApi(), ...messengerClientApi}` only |
| `persistedStateKey: null` on a controller that needs persistence | State silently resets every restart; `persistedState.X` hydrates as `undefined` |
| Sensitive top-level key without a `REMOVE_KEYS`/`REMOVE_PATHS` entry | Secrets stream to the UI in state patches |
| Relying on `anonymous` metadata for Sentry | Sentry masking is the manual `SENTRY_BACKGROUND_STATE` object; an over-permissive `true` entry leaks the value |
| State property lacking `persist` metadata | Patch filter counts it as persisted but `deriveStateFromMetadata` drops it from disk writes |

## 7. Verify

```bash
yarn test:unit app/scripts/messenger-client-init/<name>-controller-init.test.ts
yarn lint:tsc
yarn test:e2e:single test/e2e/tests/metrics/errors.spec.ts --update-snapshot  # refreshes enforced Sentry state snapshots
```

## 8. Writing the controller itself

This skill covers *integration* — wiring an existing controller into the background.
For the internals of authoring one (BaseController patterns, state metadata,
messenger action/event typing), read the sibling `controller-guidelines` skill:

```
domains/coding/skills/controller-guidelines/skill.md
```

Both are base skills, and the split is deliberate: `controller-guidelines` answers
"how do I write this controller", this one answers "how do I wire it in". Reach for
that one when the question is about state metadata, the options bag, or whether
BaseController is the right base class at all.
