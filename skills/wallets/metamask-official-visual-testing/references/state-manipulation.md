# Runtime State Manipulation

Use `mm cdp` to read and write wallet state mid-session when fixtures and presets don't cover your scenario. All operations use `Runtime.evaluate` against the active extension page. Reads and Redux writes work on every build type. LavaMoat builds block some globals, see [LavaMoat Scuttling](#lavamoat-scuttling).

## Contents

- [CDP Basics](#cdp-basics)
- [LavaMoat Scuttling](#lavamoat-scuttling)
- [Production Builds](#production-builds)
- [Five Operations](#five-operations)
- [Verify State After Mutation](#verify-state-after-mutation)
- [Troubleshooting](#troubleshooting)
- [When to Use CDP](#when-to-use-cdp)

## CDP Basics

`mm cdp` sends a raw [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) command against the active page. Use this **only when structured commands cannot express what you need**.

```bash
mm cdp Runtime.evaluate '{"expression":"document.title"}'
mm cdp Network.enable
mm cdp DOM.getDocument '{"depth":2}' --timeout 60000
```

| Argument        | Description                                                       |
| --------------- | ----------------------------------------------------------------- |
| `<method>`      | CDP method name (e.g., `Runtime.evaluate`, `DOM.getDocument`)     |
| `[params-json]` | Optional JSON object with method-specific parameters              |
| `--timeout`     | Per-command timeout in ms. Default: 30000. Min: 1000. Max: 30000  |

**Blocked methods** (returns `MM_CDP_BLOCKED`): `Browser.close`, `Target.closeTarget`, `Target.disposeBrowserContext`, `Browser.crashGpuProcess`.

An expression that throws does not make `mm cdp` fail. The command returns normally, and the error is in `result.exceptionDetails`. Check for it before you read `result.result.value`.

CDP calls are **mutating** — run `mm describe-screen` afterward to re-sync the a11y ref map.

## LavaMoat Scuttling

LavaMoat builds (`yarn build`, `yarn dist`, `yarn build:test`) scuttle `globalThis` on extension pages. A scuttled global throws when an expression reads it:

```
LavaMoat - property "chrome" of globalThis is inaccessible under scuttling mode.
```

- LavaMoat scuttles every configurable `window` global that is not on the exception list. The list is `getScuttleGlobalThisExceptions` in `development/webpack/utils/plugins/LavamoatPlugin/index.ts`. Check it before you use a global.
- Scuttled examples: `chrome`, `setInterval`, `clearInterval`, `requestAnimationFrame`, `MutationObserver`, `IntersectionObserver`, `localStorage`, `queueMicrotask`. `chrome.storage.local` calls fail (operation 4). `setInterval`, `MutationObserver`, `localStorage` and `requestAnimationFrame` errors were seen live on a production build.
- `typeof` does not show whether a global is scuttled. On a production build, `typeof window.chrome` returned `"object"` on `home.html`, and `chrome.tabs.query` threw on `sidepanel.html` (both seen live). Both pages get the same exception list. A possible cause: `scuttle.js` replaces a global that is writable but not configurable with a `Proxy`. The proxy throws only when you read one of its properties, and `typeof` does not. (Inferred from `lavamoat-core/src/scuttle.js`.) To test a global, read one of its properties, as the check below does.
- Test builds (`--test`) also allow `chrome`, `browser` and `indexedDB`. Everything else stays scuttled.
- Builds without LavaMoat (`yarn start`, `yarn build:dev`, `yarn start:test`, `yarn build:test:dev`) scuttle nothing.
- `document`, `location` and `window` stay usable. LavaMoat skips properties that are not configurable and not writable.
- `stateHooks`, `setTimeout`, `clearTimeout`, `Promise`, `JSON` and `Object` are on the exception list. The store lookup in operation 3 works on every build.
- Patching `window.setTimeout` from an expression did not change app timers on a production build.

To poll from an expression, use a recursive `setTimeout` instead of `setInterval`.

Run this check first. It shows whether `chrome` is usable and which `stateHooks` exist on this build:

```bash
mm cdp Runtime.evaluate '{"expression":"(function(){var c;try{c=typeof chrome.runtime===\"object\"}catch(e){c=false}return JSON.stringify({chrome:c,hooks:Object.keys(stateHooks)})})()","returnByValue":true}'
```

On a production build, the hooks are `getPersistedState`, `getBackupState`, `getSentryState`, `getSentryRemoteRates`, `reloadExtension`, `getCleanAppState`, `getSentryAppState`, `getLogs` (seen live). `chrome` should be `false` there, because `chrome.tabs.query` threw. This check itself has not run on a production build.

## Production Builds

A production build has LavaMoat and no `METAMASK_DEBUG`. It has no `stateHooks.store` and no `stateHooks.submitRequestToBackground` (seen live).

What works:
- Reads with `stateHooks.getCleanAppState()` and `stateHooks.getPersistedState()` (operations 1 and 2).
- Redux writes through the fiber store lookup, and the `store.subscribe` re-apply listener (operation 3 and [Troubleshooting](#troubleshooting)). Seen live.
- UI actions with `mm click`, for example a settings toggle. These change background state and persist it.
- Background calls through the UI messenger (operation 4). They reach background controllers and persist. Seen live.

What does not work:
- `chrome.storage.local` writes (operation 4). Reading a property of `chrome` throws.
- A direct line to the background service worker. `mm cdp` sends each command on a new CDP session for the active page. It has no service-worker target, and the background exposes only read hooks. Use the UI messenger instead.

If you need the debug hooks, use a different build:
- `yarn build:test:dev` (or `yarn start:test` to watch). No LavaMoat. `METAMASK_DEBUG` and `IN_TEST` are set, so `stateHooks.store` and `stateHooks.submitRequestToBackground` exist.
- `METAMASK_DEBUG=true yarn build:test`. Keeps LavaMoat but exposes the same hooks. Inferred: a variable in the environment overrides `builds.yml` (`development/webpack/utils/config.ts`). Not built and run.

## Five Operations

| Operation            | API                                  | Scope                                                    |
| -------------------- | ------------------------------------ | -------------------------------------------------------- |
| Read Redux state     | `stateHooks.getCleanAppState()`      | In-memory UI state (what the user sees)                  |
| Read persisted state | `stateHooks.getPersistedState()`     | On-disk controller state (`chrome.storage.local`)        |
| Write Redux state    | Fiber dispatch via CDP               | Instant UI update, lost on reload                        |
| Write persisted state| `chrome.storage.local.set()` via CDP | Read only when the background starts. Fails on production builds |
| Inject in-memory data| Fiber walk + `pushData()` via CDP    | Reaches components that bypass Redux (streams, channels) |

To change what the user sees: write Redux state.
To make changes persist: change the state in the background (see operation 4).
For most visual testing: writing Redux state alone is sufficient.
If a component doesn't respond to Redux changes: it reads from an in-memory source — use operation 5.

### 1. Read Redux State

```bash
# Full state keys
mm cdp Runtime.evaluate '{"expression":"stateHooks.getCleanAppState().then(s => JSON.stringify(Object.keys(s.metamask).sort()))", "awaitPromise":true, "returnByValue":true}'

# Specific values
mm cdp Runtime.evaluate '{"expression":"stateHooks.getCleanAppState().then(s => JSON.stringify({ privacyMode: s.metamask.preferences?.privacyMode, selectedNetwork: s.metamask.selectedNetworkClientId }))", "awaitPromise":true, "returnByValue":true}'
```

### 2. Read Persisted State

```bash
mm cdp Runtime.evaluate '{"expression":"stateHooks.getPersistedState().then(s => JSON.stringify(Object.keys(s.data)))", "awaitPromise":true, "returnByValue":true}'

# Specific controller
mm cdp Runtime.evaluate '{"expression":"stateHooks.getPersistedState().then(s => JSON.stringify(s.data.PreferencesController))", "awaitPromise":true, "returnByValue":true}'
```

### 3. Write Redux State

Locate the Redux store via the React fiber tree and dispatch `UPDATE_METAMASK_STATE`.

The UI renders with React 18 `createRoot`. `#app-content` is the root container. It carries a `__reactContainer$<hash>` key, not `__reactFiber$<hash>`. Start from its first child, which carries the `__reactFiber$` key. Walk up `.return` to the react-redux `<Provider>` and take `memoizedProps.store`:

```bash
mm cdp Runtime.evaluate '{"expression":"(function(){var r=document.getElementById(\"app-content\");r=r&&r.firstElementChild;if(!r)return \"app root not rendered\";var k=Object.keys(r).find(function(k){return k.startsWith(\"__reactFiber$\")});var f=r[k];var store=null;while(f){var st=f.memoizedProps&&f.memoizedProps.store;if(st&&typeof st.dispatch===\"function\"){store=st;break}f=f.return}if(!store)return\"store not found\";var next=JSON.parse(JSON.stringify(store.getState().metamask));next.preferences=Object.assign({},next.preferences,{privacyMode:true});store.dispatch({type:\"UPDATE_METAMASK_STATE\",value:next});return\"ok\"})()","returnByValue":true}'
```

**To modify for other state changes**, change the line that modifies `next`:

```javascript
// Toggle privacy mode
next.preferences = Object.assign({}, next.preferences, {privacyMode: true});

// Show test networks
next.preferences = Object.assign({}, next.preferences, {showTestNetworks: true});
```

`state.metamask` is flat. The background merges all controller states into one object (`getFlatState()` in `ComposableObservableStore.js`). There is no `next.PreferencesController` key. Persisted state is different: it is keyed by controller (operation 2).

Notes:
- The `__reactFiber$` key suffix is a random hash per build. The traversal pattern is stable.
- The store is a prop of the react-redux `<Provider>` (`ui/pages/index.js`), so read `memoizedProps.store`. The old `stateNode.store` check does not match it.
- `UPDATE_METAMASK_STATE` does not persist. Change is lost on reload.
- The next background state update can overwrite the change. See [Troubleshooting](#troubleshooting).
- If the walk returns `"store not found"`, check that you started from `#app-content.firstElementChild` and that the UI has rendered.
- On builds with `METAMASK_DEBUG`, `stateHooks.store` is the same store. You can skip the walk there.

### 4. Write Persisted State

Write directly to `chrome.storage.local`. The extension uses a split format where each controller is a separate key tracked by a `manifest` array.

Limits:
- On production builds, `chrome` is scuttled and these snippets throw (see [LavaMoat Scuttling](#lavamoat-scuttling)). Test builds and builds without LavaMoat allow `chrome`.
- The background reads storage only at startup. The running background keeps its own state, and its next persist of that controller can overwrite your write.
- Do not reload the extension to make the write show. `stateHooks.reloadExtension()` calls `browser.runtime.reload()`, which closes every extension page. The mm session keeps the closed page and cannot recover without `mm cleanup`. Cleanup deletes the temporary profile and your write. In an mm session, a restarted background also loads the fixture from the fixture server again and overwrites the write. (Inferred from source, not run.)

```bash
# Modify an existing controller
mm cdp Runtime.evaluate '{"expression":"chrome.storage.local.get([\"PreferencesController\"]).then(function(r){r.PreferencesController.preferences.privacyMode=true;return chrome.storage.local.set(r)})","awaitPromise":true}'

# Add a new controller (must update manifest)
mm cdp Runtime.evaluate '{"expression":"chrome.storage.local.get([\"manifest\"]).then(function(r){var m=r.manifest;if(m.indexOf(\"MyController\")<0)m.push(\"MyController\");return chrome.storage.local.set({manifest:m,MyController:{key:\"value\"}})})","awaitPromise":true}'
```

Storage schema:

```
chrome.storage.local = {
  manifest: ['PreferencesController', 'NetworkController', ...],
  PreferencesController: { preferences: { privacyMode: false, ... }, ... },
  meta: { version: 175, storageKind: 'split' }
}
```

Rules:
- Always read before write. Merge with existing state, never blind-write.
- Update `manifest` when adding new keys. Keys not in the manifest are invisible on next load.
- Do not delete or corrupt `manifest` or `meta`.

#### Change background state instead

Prefer a background call. The background changes the state, persists it, and sends the new state to the UI:
- Use the UI that already does it, for example a settings toggle with `mm click`. This works on every build.
- Call a background action through the UI messenger (below). This works on production builds and test builds.
- On builds with `METAMASK_DEBUG` (`yarn start`, `yarn build:dev`, `yarn start:test`, `yarn build:test:dev`), call `stateHooks.submitRequestToBackground`. It takes a messenger action name and an argument array, the same as in `ui/store/actions.ts`:

  ```bash
  mm cdp Runtime.evaluate '{"expression":"stateHooks.submitRequestToBackground(\"PreferencesController:setPreference\",[\"privacyMode\",true]).then(function(){return \"ok\"})","awaitPromise":true,"returnByValue":true}'
  ```

  `yarn build` and `yarn build:test` do not set `METAMASK_DEBUG`, so they do not expose this hook.

**Background call through the UI messenger.** The `UIMessengerProvider` above the app (`ui/pages/index.js`) holds a `UIMessenger`. Its `delegate()` registers a handler on the messenger you pass. The handler sends `messengerCall` to the background (`ui/messengers/ui-messenger.ts`). Walk up from the start fiber to the provider (its `memoizedProps.value`), delegate one action to a small stand-in messenger, and call the handler:

```bash
mm cdp Runtime.evaluate '{"expression":"(function(){var r=document.getElementById(\"app-content\");r=r&&r.firstElementChild;if(!r)return \"app root not rendered\";var k=Object.keys(r).find(function(k){return k.startsWith(\"__reactFiber$\")});var f=r[k];var ui=null;while(f){var v=f.memoizedProps&&f.memoizedProps.value;if(v&&typeof v.delegate===\"function\"&&typeof v.revoke===\"function\"){ui=v;break}f=f.return}if(!ui)return \"ui messenger not found\";var h=null;var m={_internalRegisterDelegatedActionHandler:function(t,fn){h=fn},_internalUnregisterDelegatedActionHandler:function(){},_internalPublishDelegated:function(){},captureException:function(){}};var a={actions:[\"PreferencesController:setPreference\"],messenger:m};return ui.delegate(a).then(function(){return h(\"privacyMode\",true)}).then(function(){return ui.revoke(a)}).then(function(){return \"ok\"})})()","awaitPromise":true,"returnByValue":true}'
```

To change the action or the arguments, do not edit the escaped one-liner. A shell substitution on it can fail to match because of the `\"` escaping, and then `mm cdp` silently runs the original call again. Write the expression as plain JavaScript and let `node` build the JSON parameters, as in [Troubleshooting](#keep-injected-redux-data-across-background-updates). Set `ACTION` and `ARGS` at the top:

```bash
EXPR=$(cat <<'EOF'
(function () {
  var ACTION = "PreferencesController:setPreference";
  var ARGS = ["privacyMode", true];
  var r = document.getElementById("app-content");
  r = r && r.firstElementChild;
  if (!r) return "app root not rendered";
  var k = Object.keys(r).find(function (k) { return k.startsWith("__reactFiber$"); });
  var f = r[k];
  var ui = null;
  while (f) {
    var v = f.memoizedProps && f.memoizedProps.value;
    if (v && typeof v.delegate === "function" && typeof v.revoke === "function") { ui = v; break; }
    f = f.return;
  }
  if (!ui) return "ui messenger not found";
  var h = null;
  var m = {
    _internalRegisterDelegatedActionHandler: function (t, fn) { h = fn; },
    _internalUnregisterDelegatedActionHandler: function () {},
    _internalPublishDelegated: function () {},
    captureException: function () {}
  };
  var a = { actions: [ACTION], messenger: m };
  return ui.delegate(a)
    .then(function () { return h.apply(null, ARGS); })
    .then(function () { return ui.revoke(a); })
    .then(function () { return "ok"; });
})()
EOF
)
PARAMS=$(node -e 'process.stdout.write(JSON.stringify({expression:process.argv[1],awaitPromise:true,returnByValue:true}))' "$EXPR")
mm cdp Runtime.evaluate "$PARAMS"
```

- Use the same action names and arguments as `submitRequestToBackground` calls in `ui/store/actions.ts`.
- The snippet returns `"ok"` and does not return the action's result. Read the state afterwards (see [Verify State After Mutation](#verify-state-after-mutation)). If the action throws, the error is in `result.exceptionDetails`.
- Each call uses a new stand-in messenger and revokes it at the end, so you can run it more than once.
- If it returns `"ui messenger not found"`, use `mm click` instead.
- Status: seen live on the CI production build of MetaMask Extension 13.57 and on an e2e test build. The preference changed in Redux and in persisted state, and the Home screen masked balances. An excluded action threw.

This route can call almost any action on the background messenger, including sensitive ones. The UI blocks only the actions listed in `EXCLUDED_CAPABILITIES` in `ui/messengers/configs/*.ts`. Today these are 8 `KeyringController` actions (such as `KeyringController:withKeyring`) and 7 `PasskeyController` actions. They throw `The action "<name>" has not been exposed to the UI.` (seen live for `KeyringController:withKeyring`). The background passes every other action to `controllerMessenger.call` (`messengerCall` in `app/scripts/metamask-controller.js`). For example, `KeyringController:exportAccount` is not excluded. It passed the UI check and reached the background (seen live). `ApprovalController:acceptRequest`, `TransactionController:addTransaction` and `NetworkController:setActiveNetwork` are registered on the messenger and not excluded, so they are probably reachable too (inferred from source). Use only the actions that your test needs.

Other routes that do not help:
- `store.dispatch(fn)` runs a thunk with `dispatch` and `getState` only. It does not get the background connection.
- Component callbacks such as `onToggle` on a settings toggle do reach the background, through the action they dispatch. Calling one is the same as `mm click` on that toggle, so click instead.

### 5. Inject Into In-Memory Data Sources (React Fiber Walk)

Some components read from in-memory caches, stream managers, or data channels that are **not in Redux state**. Dispatching `UPDATE_METAMASK_STATE` updates Redux but these components won't re-render because they subscribe to a different data source.

**How to detect this:** After a Redux dispatch, if the component still shows stale data, it reads from an in-memory source — not Redux.

#### Step 1 — Identify the data source

Read the component source to find what hook it uses:
- `useSelector(...)` → reads from Redux → use Write Redux (operation 3)
- `useSomeChannel(...)` / `useSomeStream(...)` → reads from an in-memory provider → needs fiber injection
- `useContext(SomeContext)` → reads from React context → find the provider via fiber walk

#### Step 2 — Find the object via fiber walk

Walk the React fiber tree looking for the target object by its **shape** (the methods and properties it exposes). Shape-matching is more robust than looking for named exports because it works regardless of bundling, minification, or scoping. Start from `#app-content.firstElementChild`, as in operation 3.

```bash
mm cdp Runtime.evaluate '{"expression":"(function(){var r=document.getElementById(\"app-content\");r=r&&r.firstElementChild;if(!r)return \"app root not rendered\";var k=Object.keys(r).find(function(k){return k.startsWith(\"__reactFiber$\")});var f=r[k];var visited=0;function walk(node){if(!node||visited>500)return null;visited++;var s=node.memoizedState;while(s){if(s.queue&&s.queue.lastRenderedState){var obj=s.queue.lastRenderedState;if(obj&&typeof obj.pushData===\"function\"&&typeof obj.getCachedData===\"function\"){return obj}}s=s.next}if(node.memoizedProps){for(var pk in node.memoizedProps){var pv=node.memoizedProps[pk];if(pv&&typeof pv===\"object\"&&typeof pv.pushData===\"function\"){return pv}}}return walk(node.child)||walk(node.sibling)}var result=walk(f);return result?\"found at fiber \"+visited:\"not found after \"+visited+\" fibers\"})()","returnByValue":true}'
```

**Adapt the detection predicate** to match your target object's shape. Common predicates:

| Target type | Predicate |
|---|---|
| Data channel | `typeof obj.pushData === "function" && typeof obj.getCachedData === "function"` |
| Redux store | `typeof obj.dispatch === "function" && typeof obj.getState === "function"` |
| Stream manager | Check for named channel properties, e.g. `obj.account && typeof obj.account.pushData === "function"` |
| React context value | Match on the unique combination of properties the context provides |

The walk goes down through `.child` and `.sibling`. Context providers rendered above the first DOM element are ancestors of the start fiber, so the walk does not reach them. To find a provider value, walk up `.return` and check `memoizedProps.value`, as in the UI messenger snippet in operation 4.

On builds with `METAMASK_DEBUG`, `stateHooks.getPerpsStreamManager()` returns the Perps stream manager directly.

#### Step 3 — Disconnect the live source

If the data source is fed by a live connection (WebSocket, polling, subscription), disconnect it first to prevent your injected data from being overwritten. TypeScript `private` fields compile to regular JS properties at runtime, so they are accessible:

```javascript
// Inside the Runtime.evaluate expression:
if (channel.unsubscribeFromSource) {
  channel.unsubscribeFromSource();
  channel.unsubscribeFromSource = null;
}
channel.isConnected = false;
```

#### Step 4 — Push data

Call the channel's update method with data matching the expected type:

```javascript
channel.pushData({
  // fields matching the component's expected data shape
});
```

`pushData` updates the internal cache AND notifies all subscribers — React components re-render immediately.

#### Complete example

Find a data channel by shape, disconnect its live source, and inject test data:

```bash
mm cdp Runtime.evaluate '{"expression":"(function(){var r=document.getElementById(\"app-content\");r=r&&r.firstElementChild;if(!r)return \"app root not rendered\";var k=Object.keys(r).find(function(k){return k.startsWith(\"__reactFiber$\")});var f=r[k];var visited=0;function walk(n){if(!n||visited>500)return null;visited++;var s=n.memoizedState;while(s){if(s.queue&&s.queue.lastRenderedState){var obj=s.queue.lastRenderedState;if(obj&&typeof obj.pushData===\"function\"&&typeof obj.getCachedData===\"function\"){return obj}}s=s.next}var p=n.memoizedProps;if(p){for(var pk in p){var pv=p[pk];if(pv&&typeof pv===\"object\"){if(typeof pv.pushData===\"function\")return pv;for(var ck in pv){if(pv[ck]&&typeof pv[ck].pushData===\"function\")return pv[ck]}}}}return walk(n.child)||walk(n.sibling)}var ch=walk(f);if(!ch)return\"channel not found after \"+visited+\" fibers\";if(ch.unsubscribeFromSource){ch.unsubscribeFromSource();ch.unsubscribeFromSource=null}ch.isConnected=false;ch.pushData({totalBalance:\"10000.00\",unrealizedPnl:\"500.00\",marginUsed:\"2000.00\",spendableBalance:\"8000.00\",withdrawableBalance:\"8000.00\",returnOnEquity:\"0.05\"});return\"data pushed at fiber \"+visited})()","returnByValue":true}'
```

Then `mm describe-screen` and `mm screenshot` to verify the component updated.

#### When to use this vs other operations

| Symptom | Cause | Solution |
|---------|-------|----------|
| Redux dispatch updated state but component shows stale data | Component reads from in-memory source, not Redux | Fiber injection (this section) |
| Feature needs live streaming data but no preset provides it | Data comes from external service via WebSocket/polling | Disconnect source + push mock data via fiber |
| Component shows loading skeleton despite state being set | The in-memory channel's `isInitialLoading` is still true | Push data via `pushData()` — it marks the channel as loaded |

## Verify State After Mutation

```bash
# Check Redux state
mm cdp Runtime.evaluate '{"expression":"stateHooks.getCleanAppState().then(function(s){return JSON.stringify({privacyMode:s.metamask.preferences.privacyMode})})","awaitPromise":true,"returnByValue":true}'

# Check persisted state
mm cdp Runtime.evaluate '{"expression":"stateHooks.getPersistedState().then(function(s){return JSON.stringify({privacyMode:s.data.PreferencesController.preferences.privacyMode})})","awaitPromise":true,"returnByValue":true}'
```

## Troubleshooting

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| Operation 3 returns `"store not found"` | The walk started at `#app-content`. With React 18 it has only `__reactContainer$`, no `__reactFiber$` | Start at `#app-content.firstElementChild` and read `memoizedProps.store` |
| `LavaMoat - property "X" of globalThis is inaccessible under scuttling mode` | The expression reads a scuttled global (for example `chrome`, `setInterval`, `MutationObserver`, `requestAnimationFrame`) | Use the replacements in [LavaMoat Scuttling](#lavamoat-scuttling) |
| Operation 3 returns `"app root not rendered"` | The page has no `#app-content` child yet | Wait for the UI to render, then run it again |
| Injected Redux data disappears after a few seconds or after an action | A background state update replaced the value you changed | Re-apply the data from a `store.subscribe` listener (below) |
| Injected data and listeners are gone after `mm navigate-home` or `mm navigate-settings`, or on another extension page | Each extension page (home, sidepanel, popup) has its own Redux store. `mm navigate-*` calls `page.goto`, a full page load that drops injected data and listeners | Route inside the page with `window.location.hash = "#/..."` from `Runtime.evaluate`. Or inject again after the navigation, on the page you will screenshot |

### Keep injected Redux data across background updates

The background sends state patches to the UI after each change. The UI applies them to its current Redux state. A patch that replaces a value you changed drops your data. Example: opening a notification calls `markMetamaskNotificationsAsRead`. The background replaces `metamaskNotificationsList`, and the injected notification is gone.

Re-apply the data from a `store.subscribe` listener. This example keeps one injected notification in `metamaskNotificationsList`. Long expressions are hard to escape by hand, so write the expression as plain JavaScript and let `node` build the JSON parameters:

```bash
EXPR=$(cat <<'EOF'
(function () {
  var r = document.getElementById("app-content");
  r = r && r.firstElementChild;
  if (!r) return "app root not rendered";
  var k = Object.keys(r).find(function (k) { return k.startsWith("__reactFiber$"); });
  var f = r[k];
  var store = null;
  while (f) {
    var st = f.memoizedProps && f.memoizedProps.store;
    if (st && typeof st.dispatch === "function") { store = st; break; }
    f = f.return;
  }
  if (!store) return "store not found";
  var n = {
    type: "features_announcement", id: "mm-test-feature", createdAt: new Date().toISOString(), isRead: true,
    data: {
      id: "mm-test-feature", category: "ANNOUNCEMENT", title: "Test announcement",
      shortDescription: "Short description", longDescription: "<p>Long description</p>",
      image: { title: "img", description: "", url: "" },
      extensionLink: { extensionLinkText: "Try now", extensionLinkRoute: "home.html" },
      externalLink: { externalLinkText: "Learn more", externalLinkUrl: "https://metamask.io" }
    }
  };
  if (window.__mmPinUnsub) { window.__mmPinUnsub(); window.__mmPinUnsub = null; }
  var busy = false;
  function ensure() {
    if (busy) return;
    var list = store.getState().metamask.metamaskNotificationsList || [];
    if (list.some(function (x) { return x.id === n.id; })) return;
    busy = true;
    try {
      var next = JSON.parse(JSON.stringify(store.getState().metamask));
      next.metamaskNotificationsList = list.concat([n]);
      store.dispatch({ type: "UPDATE_METAMASK_STATE", value: next });
    } finally {
      busy = false;
    }
  }
  ensure();
  window.__mmPinUnsub = store.subscribe(ensure);
  return "pinned";
})()
EOF
)
PARAMS=$(node -e 'process.stdout.write(JSON.stringify({expression:process.argv[1],returnByValue:true}))' "$EXPR")
mm cdp Runtime.evaluate "$PARAMS"
```

- The `busy` flag stops the listener from reacting to its own dispatch.
- Append injected items to arrays. Background patches can target array indexes (`app/scripts/lib/PatchStore.ts`), and prepending shifts them.
- Replace `n` with your own object. Keep a unique `id`, and use the same `id` in the cleanup command.

Clean up when the test is done. Unsubscribe, then remove the injected data:

```bash
mm cdp Runtime.evaluate '{"expression":"(function(){var r=document.getElementById(\"app-content\");r=r&&r.firstElementChild;if(!r)return \"app root not rendered\";var k=Object.keys(r).find(function(k){return k.startsWith(\"__reactFiber$\")});var f=r[k];var store=null;while(f){var st=f.memoizedProps&&f.memoizedProps.store;if(st&&typeof st.dispatch===\"function\"){store=st;break}f=f.return}if(!store)return \"store not found\";if(window.__mmPinUnsub){window.__mmPinUnsub();window.__mmPinUnsub=null}var next=JSON.parse(JSON.stringify(store.getState().metamask));next.metamaskNotificationsList=(next.metamaskNotificationsList||[]).filter(function(x){return x.id!==\"mm-test-feature\"});store.dispatch({type:\"UPDATE_METAMASK_STATE\",value:next});return \"unpinned\"})()","returnByValue":true}'
```

Then read the state again to confirm that no injected items remain.

## When to Use CDP

| Need                                          | Suggested CDP method                                      |
| --------------------------------------------- | --------------------------------------------------------- |
| Read a JS value / `window` property           | `Runtime.evaluate` with `{ "expression": "..." }`        |
| Inspect / traverse DOM                        | `DOM.getDocument`, `DOM.querySelector`                    |
| Capture network traffic                       | `Network.enable`                                          |
| Inject cookies or storage                     | `Network.setCookie`, `Storage.setLocalStorage*`           |
| Low-level input beyond `mm click` / `mm type` | `Input.dispatchKeyEvent`, `Input.dispatchMouseEvent`      |
| Inject data into non-Redux in-memory sources   | Fiber walk + `pushData()` (see [operation 5](#5-inject-into-in-memory-data-sources-react-fiber-walk)) |
