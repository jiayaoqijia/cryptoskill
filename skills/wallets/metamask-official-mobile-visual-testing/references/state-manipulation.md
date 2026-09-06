# Runtime State Manipulation (Mobile)

Use `mm cdp` only for advanced runtime inspection or manipulation of the current installed app during a Metro-attached session. On mobile, `mm cdp` connects to the Hermes JavaScript runtime through Metro's inspector proxy. These operations use `Runtime.evaluate` and require Metro to be running (`MM_METRO_PORT`).

## Contents

- [CDP Basics (Mobile)](#cdp-basics-mobile)
- [Fiber Entry Point (React Native)](#fiber-entry-point-react-native)
- [Operations](#operations)
- [Finding the Engine Singleton](#finding-the-engine-singleton)
- [Verify State After Mutation](#verify-state-after-mutation)
- [When to Use CDP](#when-to-use-cdp)

## CDP Basics (Mobile)

`mm cdp` sends a Chrome DevTools Protocol command. On mobile, it connects to the Hermes runtime via Metro's inspector proxy, targeting the **React Native JS thread** (on the extension it targets the browser page instead).

```bash
yarn mm cdp Runtime.evaluate '{"expression":"JSON.stringify(1+1)"}'
yarn mm cdp Runtime.evaluate '{"expression":"JSON.stringify(globalThis.__DEV__)"}'
```

**Requirements:**
- Metro must be running (`MM_METRO_PORT` set at launch time)
- Node 20 requires `--experimental-websocket` flag at daemon launch
- Node 22+ works natively

CDP calls are **mutating**, so run `mm describe-screen` afterward to re-sync the a11y ref map.

## Fiber Entry Point (React Native)

The extension walks fibers from a DOM node (`document.getElementById("app-content").__reactFiber$...`). React Native has no DOM. Instead, use `__REACT_DEVTOOLS_GLOBAL_HOOK__`:

```javascript
var hook = globalThis.__REACT_DEVTOOLS_GLOBAL_HOOK__;
var rid = hook.renderers.keys().next().value;
var root = hook.getFiberRoots(rid).values().next().value;
var fiber = root.current; // root fiber, start walking from here
```

From `fiber`, traverse the tree with `.child`, `.sibling`, and `.return` exactly like the extension pattern. The fiber shape (`memoizedState`, `memoizedProps`, `stateNode`) is identical.

## Operations

| Operation | Method | Scope |
|---|---|---|
| Read Redux state | Fiber walk, store, `getState()` | In-memory UI state |
| Write Redux state | Fiber walk, store, `dispatch()` | Instant UI update, lost on restart |
| Call controller methods | Fiber walk, Engine singleton, `context.SomeController.method()` | Triggers real controller logic and state propagation |

**Preferred order:** Call controller methods (operation 3) first. This is the most correct approach because the controller manages its own state and propagates to Redux. Fall back to Redux dispatch (operation 2) only when you need to fake state that no controller API provides.

### 1. Read Redux State

Find the Redux store on the `<Provider>` component's fiber props:

```bash
yarn mm cdp Runtime.evaluate '{"expression":"(function(){var hook=globalThis.__REACT_DEVTOOLS_GLOBAL_HOOK__;var rid=hook.renderers.keys().next().value;var root=hook.getFiberRoots(rid).values().next().value;function find(f){if(!f)return null;if(f.memoizedProps&&f.memoizedProps.store&&typeof f.memoizedProps.store.getState===\"function\")return f.memoizedProps.store;return find(f.child)||find(f.sibling)}var store=find(root.current);if(!store)return JSON.stringify(\"store not found\");var s=store.getState();return JSON.stringify({userRegion:s.engine.backgroundState.RampsController.userRegion,moneyEnabled:!!s.engine.backgroundState.RemoteFeatureFlagController})})()","returnByValue":true}'
```

**Readable version** of the expression:

```javascript
(function() {
  var hook = globalThis.__REACT_DEVTOOLS_GLOBAL_HOOK__;
  var rid = hook.renderers.keys().next().value;
  var root = hook.getFiberRoots(rid).values().next().value;

  function find(f) {
    if (!f) return null;
    if (f.memoizedProps && f.memoizedProps.store
        && typeof f.memoizedProps.store.getState === "function")
      return f.memoizedProps.store;
    return find(f.child) || find(f.sibling);
  }

  var store = find(root.current);
  if (!store) return JSON.stringify("store not found");
  var s = store.getState();
  return JSON.stringify({
    userRegion: s.engine.backgroundState.RampsController.userRegion,
  });
})()
```

### 2. Write Redux State

Dispatch an action to update the backgroundState slice. The UI re-renders immediately.

```javascript
(function() {
  // ... same fiber walk to find store ...
  var s = store.getState();
  var bg = s.engine.backgroundState;

  // Patch the target controller state
  var ramps = Object.assign({}, bg.RampsController, {
    userRegion: {
      regionCode: "BR",
      country: { isoCode: "BR", name: "Brazil", supported: { buy: false } },
      state: null
    }
  });

  // Dispatch backgroundState update
  store.dispatch({
    type: "UPDATE_BG_STATE",
    key: "RampsController",
    payload: ramps
  });
  return "ok";
})()
```

> **Note:** The exact action type for backgroundState updates may differ. If `UPDATE_BG_STATE` doesn't work, inspect the Redux reducer to find the correct action type. Redux dispatch only updates what the UI reads via selectors, but it does NOT modify the live controller instance.

### 3. Find Engine Singleton and Call Controller Methods (Preferred)

The Engine singleton holds every controller at `Engine.context`. Components that use controllers (e.g., `useRampsProviders`, `useMoneyAccountDeposit`) import Engine as a module dependency. Walk the fiber tree looking for an object with the controller context shape: an object that has `RampsController`, `TransactionController`, and `NetworkController` as properties.

**Strategy A: Shape-match Engine.context on fiber props/state:**

```javascript
(function() {
  var hook = globalThis.__REACT_DEVTOOLS_GLOBAL_HOOK__;
  var rid = hook.renderers.keys().next().value;
  var root = hook.getFiberRoots(rid).values().next().value;
  var visited = 0;

  function isEngineContext(obj) {
    return obj
      && typeof obj.RampsController !== "undefined"
      && typeof obj.TransactionController !== "undefined"
      && typeof obj.NetworkController !== "undefined";
  }

  function searchObj(obj, depth) {
    if (!obj || depth > 3 || typeof obj !== "object") return null;
    if (isEngineContext(obj)) return obj;
    for (var k in obj) {
      try {
        var v = obj[k];
        if (v && typeof v === "object") {
          var found = searchObj(v, depth + 1);
          if (found) return found;
        }
      } catch(e) {}
    }
    return null;
  }

  function walk(f) {
    if (!f || visited > 2000) return null;
    visited++;

    // Check memoizedProps
    var ctx = searchObj(f.memoizedProps, 0);
    if (ctx) return ctx;

    // Check stateNode
    if (f.stateNode && typeof f.stateNode === "object") {
      ctx = searchObj(f.stateNode, 0);
      if (ctx) return ctx;
    }

    // Check hook state chain (memoizedState linked list)
    var hookState = f.memoizedState;
    while (hookState) {
      if (hookState.memoizedState && typeof hookState.memoizedState === "object") {
        ctx = searchObj(hookState.memoizedState, 0);
        if (ctx) return ctx;
      }
      // useRef stores value in .current
      if (hookState.memoizedState && hookState.memoizedState.current) {
        ctx = searchObj(hookState.memoizedState.current, 0);
        if (ctx) return ctx;
      }
      hookState = hookState.next;
    }

    return walk(f.child) || walk(f.sibling);
  }

  var ctx = walk(root.current);
  if (!ctx) return JSON.stringify("Engine.context not found after " + visited + " fibers");

  // Now call the controller method
  ctx.RampsController.setUserRegion("BR");
  return JSON.stringify("setUserRegion called, visited " + visited + " fibers");
})()
```

**Strategy B: Metro module registry (fallback):**

In dev builds with Metro, `globalThis.__r` is Metro's module require function. Scan for the Engine module by checking exports:

```javascript
(function() {
  if (typeof globalThis.__r !== "function") return JSON.stringify("__r not available");

  for (var id = 0; id < 80000; id++) {
    try {
      var m = globalThis.__r(id);
      if (m && m.default && m.default.context
          && m.default.context.RampsController
          && m.default.context.NetworkController) {
        // Found Engine default export
        m.default.context.RampsController.setUserRegion("BR");
        return JSON.stringify("Engine found at module " + id);
      }
    } catch(e) {}
  }
  return JSON.stringify("Engine module not found");
})()
```

> **Note:** Strategy B brute-forces module IDs. It works but is slow (~5-15s). Cache the module ID within a session once found. Strategy A (fiber walk) is faster and preferred.

### Example: Simulate Unsupported Region for Fiat Deposits

```bash
# 1. Set region to Brazil (unsupported for buy)
yarn mm cdp Runtime.evaluate '{"expression":"(function(){var hook=globalThis.__REACT_DEVTOOLS_GLOBAL_HOOK__;var rid=hook.renderers.keys().next().value;var root=hook.getFiberRoots(rid).values().next().value;var visited=0;function isCtx(o){return o&&typeof o.RampsController!==\"undefined\"&&typeof o.NetworkController!==\"undefined\"}function search(o,d){if(!o||d>3||typeof o!==\"object\")return null;if(isCtx(o))return o;for(var k in o){try{var v=o[k];if(v&&typeof v===\"object\"){var f=search(v,d+1);if(f)return f}}catch(e){}}return null}function walk(f){if(!f||visited>2000)return null;visited++;var c=search(f.memoizedProps,0)||search(f.stateNode,0);if(c)return c;var h=f.memoizedState;while(h){if(h.memoizedState&&typeof h.memoizedState===\"object\"){c=search(h.memoizedState,0);if(c)return c}h=h.next}return walk(f.child)||walk(f.sibling)}var ctx=walk(root.current);if(!ctx)return JSON.stringify(\"not found\");ctx.RampsController.setUserRegion(\"BR\");return JSON.stringify(\"region set to BR\")})()","returnByValue":true}'

# 2. Wait for provider re-resolution
sleep 3

# 3. Navigate to Money, then Add Money sheet
yarn mm describe-screen
yarn mm click --testid money-action-button-row-add
yarn mm wait-for --testid money-add-money-sheet --timeout 10000
yarn mm describe-screen
yarn mm screenshot --name "unsupported-region-no-deposit-funds"

# 4. Verify: "Deposit Funds" option should be missing or disabled

# 5. Restore to US
yarn mm cdp Runtime.evaluate '{"expression":"(function(){/* same walk */ctx.RampsController.setUserRegion(\"US\");return JSON.stringify(\"region restored\")})()","returnByValue":true}'
```

## Verify State After Mutation

```bash
# Read current region from Redux
yarn mm cdp Runtime.evaluate '{"expression":"(function(){var hook=globalThis.__REACT_DEVTOOLS_GLOBAL_HOOK__;var rid=hook.renderers.keys().next().value;var root=hook.getFiberRoots(rid).values().next().value;function find(f){if(!f)return null;if(f.memoizedProps&&f.memoizedProps.store&&typeof f.memoizedProps.store.getState===\"function\")return f.memoizedProps.store;return find(f.child)||find(f.sibling)}var store=find(root.current);if(!store)return JSON.stringify(\"no store\");var r=store.getState().engine.backgroundState.RampsController;return JSON.stringify({regionCode:r.userRegion&&r.userRegion.regionCode,country:r.userRegion&&r.userRegion.country})})()","returnByValue":true}'
```

## When to Use CDP

| Need | Approach |
|---|---|
| Read any Redux state value | Fiber walk, store, `getState()` |
| Change what the UI displays (fast, non-persistent) | Fiber walk, store, `dispatch()` |
| Trigger real controller logic (region change, provider refresh) | Fiber walk, Engine.context, controller method |
| Verify a JS global or Hermes flag | `Runtime.evaluate` with simple expression |
| Execute JS against the React Native runtime | `Runtime.evaluate` |

| Symptom | Cause | Solution |
|---|---|---|
| Redux dispatch updated state but UI didn't change | Component reads from controller state, not Redux selector | Use Engine.context controller method instead |
| Fiber walk returns "not found" | DevTools hook not available (release build) or tree too deep | Try Metro `__r` fallback (Strategy B) |
| `setUserRegion` called but UI unchanged | Provider re-fetch is async; UI hasn't re-rendered yet | Wait 3-5 seconds, then `describe-screen` |
