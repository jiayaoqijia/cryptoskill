# Runtime State Manipulation

Use `mm cdp` to read and write wallet state mid-session when fixtures and presets don't cover your scenario. All operations use `Runtime.evaluate` against the active extension page and work on every build type.

## Contents

- [CDP Basics](#cdp-basics)
- [Five Operations](#five-operations)
- [Verify State After Mutation](#verify-state-after-mutation)
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

CDP calls are **mutating** — run `mm describe-screen` afterward to re-sync the a11y ref map.

## Five Operations

| Operation            | API                                  | Scope                                                    |
| -------------------- | ------------------------------------ | -------------------------------------------------------- |
| Read Redux state     | `stateHooks.getCleanAppState()`      | In-memory UI state (what the user sees)                  |
| Read persisted state | `stateHooks.getPersistedState()`     | On-disk controller state (`chrome.storage.local`)        |
| Write Redux state    | Fiber dispatch via CDP               | Instant UI update, lost on reload                        |
| Write persisted state| `chrome.storage.local.set()` via CDP | Survives reload, eventually reflected in UI              |
| Inject in-memory data| Fiber walk + `pushData()` via CDP    | Reaches components that bypass Redux (streams, channels) |

To change what the user sees: write Redux state.
To make changes survive a reload: write persisted state too.
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

Locate the Redux store via the React fiber tree and dispatch `UPDATE_METAMASK_STATE`:

```bash
mm cdp Runtime.evaluate '{"expression":"(function(){var r=document.getElementById(\"app-content\");var k=Object.keys(r).find(function(k){return k.startsWith(\"__reactFiber$\")});var f=r[k];while(f){if(f.stateNode&&f.stateNode.store&&typeof f.stateNode.store.dispatch===\"function\"){var store=f.stateNode.store;var s=store.getState();var next=JSON.parse(JSON.stringify(s.metamask));next.preferences=Object.assign({},next.preferences,{privacyMode:true});store.dispatch({type:\"UPDATE_METAMASK_STATE\",value:next});return\"ok\"}f=f.return}return\"store not found\"})()","returnByValue":true}'
```

**To modify for other state changes**, change the line that modifies `next`:

```javascript
// Toggle privacy mode
next.preferences = Object.assign({}, next.preferences, {privacyMode: true});

// Change a nested controller value
next.PreferencesController = Object.assign({}, next.PreferencesController, {
  preferences: Object.assign({}, next.PreferencesController.preferences, {
    showTestNetworks: true
  })
});
```

Notes:
- The `__reactFiber$` key suffix is a random hash per build. The traversal pattern is stable.
- `UPDATE_METAMASK_STATE` does not persist. Change is lost on reload.
- If the fiber walk fails (e.g., LavaMoat scuttling), returns `"store not found"`.

### 4. Write Persisted State

Write directly to `chrome.storage.local`. The extension uses a split format where each controller is a separate key tracked by a `manifest` array.

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

### 5. Inject Into In-Memory Data Sources (React Fiber Walk)

Some components read from in-memory caches, stream managers, or data channels that are **not in Redux state**. Dispatching `UPDATE_METAMASK_STATE` updates Redux but these components won't re-render because they subscribe to a different data source.

**How to detect this:** After a Redux dispatch, if the component still shows stale data, it reads from an in-memory source — not Redux.

#### Step 1 — Identify the data source

Read the component source to find what hook it uses:
- `useSelector(...)` → reads from Redux → use Write Redux (operation 3)
- `useSomeChannel(...)` / `useSomeStream(...)` → reads from an in-memory provider → needs fiber injection
- `useContext(SomeContext)` → reads from React context → find the provider via fiber walk

#### Step 2 — Find the object via fiber walk

Walk the React fiber tree looking for the target object by its **shape** (the methods and properties it exposes). Shape-matching is more robust than looking for named exports because it works regardless of bundling, minification, or scoping.

```bash
mm cdp Runtime.evaluate '{"expression":"(function(){var r=document.getElementById(\"app-content\");var k=Object.keys(r).find(function(k){return k.startsWith(\"__reactFiber$\")});var f=r[k];var visited=0;function walk(node){if(!node||visited>500)return null;visited++;var s=node.memoizedState;while(s){if(s.queue&&s.queue.lastRenderedState){var obj=s.queue.lastRenderedState;if(obj&&typeof obj.pushData===\"function\"&&typeof obj.getCachedData===\"function\"){return obj}}s=s.next}if(node.memoizedProps){for(var pk in node.memoizedProps){var pv=node.memoizedProps[pk];if(pv&&typeof pv===\"object\"&&typeof pv.pushData===\"function\"){return pv}}}return walk(node.child)||walk(node.sibling)}var result=walk(f);return result?\"found at fiber \"+visited:\"not found after \"+visited+\" fibers\"})()","returnByValue":true}'
```

**Adapt the detection predicate** to match your target object's shape. Common predicates:

| Target type | Predicate |
|---|---|
| Data channel | `typeof obj.pushData === "function" && typeof obj.getCachedData === "function"` |
| Redux store | `typeof obj.dispatch === "function" && typeof obj.getState === "function"` |
| Stream manager | Check for named channel properties, e.g. `obj.account && typeof obj.account.pushData === "function"` |
| React context value | Match on the unique combination of properties the context provides |

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
mm cdp Runtime.evaluate '{"expression":"(function(){var r=document.getElementById(\"app-content\");var k=Object.keys(r).find(function(k){return k.startsWith(\"__reactFiber$\")});var f=r[k];var visited=0;function walk(n){if(!n||visited>500)return null;visited++;var s=n.memoizedState;while(s){if(s.queue&&s.queue.lastRenderedState){var obj=s.queue.lastRenderedState;if(obj&&typeof obj.pushData===\"function\"&&typeof obj.getCachedData===\"function\"){return obj}}s=s.next}var p=n.memoizedProps;if(p){for(var pk in p){var pv=p[pk];if(pv&&typeof pv===\"object\"){if(typeof pv.pushData===\"function\")return pv;for(var ck in pv){if(pv[ck]&&typeof pv[ck].pushData===\"function\")return pv[ck]}}}}return walk(n.child)||walk(n.sibling)}var ch=walk(f);if(!ch)return\"channel not found after \"+visited+\" fibers\";if(ch.unsubscribeFromSource){ch.unsubscribeFromSource();ch.unsubscribeFromSource=null}ch.isConnected=false;ch.pushData({totalBalance:\"10000.00\",unrealizedPnl:\"500.00\",marginUsed:\"2000.00\",spendableBalance:\"8000.00\",withdrawableBalance:\"8000.00\",returnOnEquity:\"0.05\"});return\"data pushed at fiber \"+visited})()","returnByValue":true}'
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

## When to Use CDP

| Need                                          | Suggested CDP method                                      |
| --------------------------------------------- | --------------------------------------------------------- |
| Read a JS value / `window` property           | `Runtime.evaluate` with `{ "expression": "..." }`        |
| Inspect / traverse DOM                        | `DOM.getDocument`, `DOM.querySelector`                    |
| Capture network traffic                       | `Network.enable`                                          |
| Inject cookies or storage                     | `Network.setCookie`, `Storage.setLocalStorage*`           |
| Low-level input beyond `mm click` / `mm type` | `Input.dispatchKeyEvent`, `Input.dispatchMouseEvent`      |
| Inject data into non-Redux in-memory sources   | Fiber walk + `pushData()` (see [operation 5](#5-inject-into-in-memory-data-sources-react-fiber-walk)) |
