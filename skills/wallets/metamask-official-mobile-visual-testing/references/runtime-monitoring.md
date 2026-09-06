# Runtime Monitoring — Network & Console Capture

Inject interceptors into the Hermes runtime to capture `fetch` requests (including JSON-RPC method names and errors), and `console` output during visual testing. Read them back at any point to detect silent failures, slow API calls, RPC errors, or unexpected behavior that doesn't surface in the UI.

## Contents

- [Prerequisites](#prerequisites)
- [Install Interceptors](#install-interceptors)
- [Read Captured Data](#read-captured-data)
- [Check Interceptor Health](#check-interceptor-health)
- [Dismissing Dev Error Overlays](#dismissing-dev-error-overlays)
- [Anomaly Detection](#anomaly-detection)
- [Daemon & Metro Logs](#daemon--metro-logs)
- [Gotchas](#gotchas)

## Prerequisites

- Metro must be running (`MM_METRO_PORT` set at launch time)
- Same CDP requirements as [state-manipulation.md](state-manipulation.md) — Node 20 needs `--experimental-websocket`
- Interceptors operate in the JS thread only — native-layer network calls (e.g., iOS URLSession) are not captured

## Install Interceptors

Run once after launch. Installs both fetch and console interceptors in a single call. Idempotent — safe to re-run.

```bash
yarn mm cdp Runtime.evaluate '{"expression":"(function(){if(globalThis.__mmNet)return JSON.stringify(\"already installed\");var of=globalThis.fetch;globalThis.__mmNet=[];globalThis.fetch=function(){var u=arguments[0],o=arguments[1]||{},e={t:Date.now(),method:o.method||\"GET\",url:typeof u===\"string\"?u:(u&&u.url)||String(u)};if(o.body){try{var b=typeof o.body===\"string\"?JSON.parse(o.body):o.body;if(b&&b.method)e.rpcMethod=b.method}catch(x){}}globalThis.__mmNet.push(e);if(globalThis.__mmNet.length>2000)globalThis.__mmNet=globalThis.__mmNet.slice(-1000);return of.apply(globalThis,arguments).then(function(r){e.status=r.status;e.ms=Date.now()-e.t;if(e.rpcMethod){try{r.clone().text().then(function(t){try{var j=JSON.parse(t);if(j.error){e.rpcError=(j.error.message||JSON.stringify(j.error)).substring(0,200);e.rpcErrorCode=j.error.code}}catch(x){}}).catch(function(){})}catch(x){}}return r}).catch(function(err){e.err=String(err);e.ms=Date.now()-e.t;throw err})};globalThis.__mmCon=[];[\"log\",\"warn\",\"error\"].forEach(function(l){var orig=console[l];console[l]=function(){var a=Array.prototype.slice.call(arguments);globalThis.__mmCon.push({t:Date.now(),level:l,msg:a.map(function(x){try{return String(x)}catch(e){return\"[unstringifiable]\"}}).join(\" \")});if(globalThis.__mmCon.length>1000)globalThis.__mmCon=globalThis.__mmCon.slice(-500);return orig.apply(console,arguments)}});return JSON.stringify(\"interceptors installed\")})()","returnByValue":true}'
```

**Readable version** of the expression:

```javascript
(function() {
  if (globalThis.__mmNet) return JSON.stringify("already installed");

  // --- Fetch interceptor (with JSON-RPC capture) ---
  var origFetch = globalThis.fetch;
  globalThis.__mmNet = [];
  globalThis.fetch = function() {
    var url = arguments[0];
    var opts = arguments[1] || {};
    var entry = {
      t: Date.now(),
      method: opts.method || "GET",
      url: typeof url === "string" ? url : (url && url.url) || String(url),
    };
    // Extract JSON-RPC method from request body
    if (opts.body) {
      try {
        var b = typeof opts.body === "string" ? JSON.parse(opts.body) : opts.body;
        if (b && b.method) entry.rpcMethod = b.method;
      } catch(x) {}
    }
    globalThis.__mmNet.push(entry);
    // Auto-trim: keep last 1000 when buffer exceeds 2000
    if (globalThis.__mmNet.length > 2000) {
      globalThis.__mmNet = globalThis.__mmNet.slice(-1000);
    }
    return origFetch.apply(globalThis, arguments)
      .then(function(resp) {
        entry.status = resp.status;
        entry.ms = Date.now() - entry.t;
        // For RPC requests, clone response to extract JSON-RPC errors.
        // Without this, RPC errors are invisible — Infura returns HTTP 200
        // with {"error": {"message": "..."}} in the body.
        if (entry.rpcMethod) {
          try {
            resp.clone().text().then(function(body) {
              try {
                var j = JSON.parse(body);
                if (j.error) {
                  entry.rpcError = (j.error.message || JSON.stringify(j.error)).substring(0, 200);
                  entry.rpcErrorCode = j.error.code;
                }
              } catch(x) {}
            }).catch(function(){});
          } catch(x) {}
        }
        return resp;
      })
      .catch(function(err) {
        entry.err = String(err);
        entry.ms = Date.now() - entry.t;
        throw err;
      });
  };

  // --- Console interceptor ---
  globalThis.__mmCon = [];
  ["log", "warn", "error"].forEach(function(level) {
    var orig = console[level];
    console[level] = function() {
      var args = Array.prototype.slice.call(arguments);
      globalThis.__mmCon.push({
        t: Date.now(),
        level: level,
        msg: args.map(function(a) {
          try { return String(a); } catch(e) { return "[unstringifiable]"; }
        }).join(" "),
      });
      // Auto-trim: keep last 500 when buffer exceeds 1000
      if (globalThis.__mmCon.length > 1000) {
        globalThis.__mmCon = globalThis.__mmCon.slice(-500);
      }
      return orig.apply(console, arguments);
    };
  });

  return JSON.stringify("interceptors installed");
})()
```

## Read Captured Data

### Drain both buffers (read and clear)

Returns all captured data and resets the buffers. Use this between test steps or after a flow completes.

```bash
yarn mm cdp Runtime.evaluate '{"expression":"(function(){var r=JSON.stringify({net:globalThis.__mmNet||[],con:globalThis.__mmCon||[]});globalThis.__mmNet=[];globalThis.__mmCon=[];return r})()","returnByValue":true}'
```

### Read without clearing

Peek at the buffers without resetting. Useful when you want to keep accumulating across steps.

```bash
yarn mm cdp Runtime.evaluate '{"expression":"JSON.stringify({net:globalThis.__mmNet||[],con:globalThis.__mmCon||[]})","returnByValue":true}'
```

### Response shape

```json
{
  "net": [
    { "t": 1718000000000, "method": "GET", "url": "https://api.example.com/data", "status": 200, "ms": 142 },
    { "t": 1718000001000, "method": "POST", "url": "https://mainnet.infura.io/v3/KEY", "status": 200, "ms": 85, "rpcMethod": "eth_blockNumber" },
    { "t": 1718000002000, "method": "POST", "url": "https://mainnet.infura.io/v3/KEY", "status": 200, "ms": 3021, "rpcMethod": "eth_sendRawTransaction", "rpcError": "Signer had insufficient balance", "rpcErrorCode": -32000 },
    { "t": 1718000003000, "method": "GET", "url": "https://api.example.com/fail", "err": "TypeError: Network request failed", "ms": 15000 }
  ],
  "con": [
    { "t": 1718000000500, "level": "warn", "msg": "Deprecated API call: use v2 endpoint" },
    { "t": 1718000001200, "level": "error", "msg": "Unhandled promise rejection: RPC timeout" }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `t` | number | Unix timestamp (ms) |
| `method` | string | HTTP method |
| `url` | string | Request URL |
| `status` | number | HTTP response status (absent if request failed) |
| `ms` | number | Duration in milliseconds |
| `err` | string | Network-level error message (absent if fetch succeeded) |
| `rpcMethod` | string | JSON-RPC method from request body (absent for non-RPC requests) |
| `rpcError` | string | JSON-RPC error message from response body (absent if RPC succeeded) |
| `rpcErrorCode` | number | JSON-RPC error code (absent if RPC succeeded) |
| `level` | string | `log`, `warn`, or `error` |
| `msg` | string | Stringified console arguments |

## Check Interceptor Health

Verify interceptors are still installed. They are lost on app reload or Fast Refresh.

```bash
yarn mm cdp Runtime.evaluate '{"expression":"JSON.stringify({installed:!!globalThis.__mmNet,netCount:(globalThis.__mmNet||[]).length,conCount:(globalThis.__mmCon||[]).length})","returnByValue":true}'
```

If `installed` is `false`, re-run the install command.

## Dismissing Dev Error Overlays

The Engine module walk (`globalThis.__r(id)` loop from [state-manipulation.md](state-manipulation.md)) triggers **3–4 dev error overlays** in development builds. These are caused by modules that throw on import (e.g., `SegmentFetcher` TurboModule not found). The overlays are purely cosmetic — interceptors and cached references survive them — but they block UI interaction until dismissed.

**You must dismiss ALL overlays, not just the first one.** Each overlay is a separate error stacked on top of the previous.

### Dismiss loop pattern

```bash
for i in 1 2 3 4 5 6 7; do
  RESULT=$(yarn mm describe-screen 2>&1 | python3 -c "
import json, sys
a = json.load(sys.stdin).get('a11y', {}).get('nodes', [])
dismiss = [n for n in a if n.get('name', '').lower() == 'dismiss']
print(dismiss[0]['ref'] if dismiss else 'CLEAN')
" 2>&1)
  if [ "$RESULT" = "CLEAN" ]; then
    echo "All overlays dismissed after $((i-1)) dismissals"
    break
  fi
  yarn mm click "$RESULT" 2>&1 | grep -q clicked && echo "Dismissed overlay $i"
  sleep 0.5
done
```

### Recommended instrumentation sequence

1. Install fetch/console interceptors (safe, no overlays)
2. Run the Engine module walk (triggers overlays)
3. Run the dismiss loop above
4. Verify instrumentation survived: check `!!globalThis.__mmDebugNet` and `!!globalThis.__mmEngine`

### Notes

- Typically **3 overlays** appear, but the count can vary by build. The loop handles up to 7 as a safety margin.
- The overlays do **not** cause an app reload — interceptors and the cached Engine reference remain intact.
- If the app does reload (Fast Refresh, Metro reconnect), you must re-install everything from step 1.
- The "Dismiss" button's a11y ref changes between `describe-screen` calls, so the loop re-queries each iteration.

## Anomaly Detection

After draining the buffers, flag these patterns:

### Network anomalies

| Pattern | How to detect | Severity |
|---------|--------------|----------|
| Failed requests | `status >= 400` or `err` field present | High |
| **JSON-RPC errors** | **`rpcError` field present** (HTTP status will be 200) | **Critical** |
| Slow requests | `ms > 5000` | Medium |
| Network errors | `err` contains "Network request failed" or "aborted" | High |
| Repeated failures | Same `url` failing 3+ times | High |
| Unexpected RPC calls | `url` contains unfamiliar host (not infura, metamask, etc.) | Medium |
| Transaction failures | `rpcMethod` is `eth_sendRawTransaction` and `rpcError` present | Critical |

### Console anomalies

| Pattern | How to detect | Severity |
|---------|--------------|----------|
| Errors | `level === "error"` | High |
| Unhandled rejections | `msg` contains "Unhandled" or "rejection" | High |
| React render warnings | `msg` contains "Cannot update a component" or "Maximum update depth" | Medium |
| Deprecation warnings | `msg` contains "deprecated" or "Deprecated" | Low |

### When to drain

- **After each major flow step** (e.g., after completing a send transaction)
- **On unexpected UI state** (loading spinner stuck, missing data, blank screen)
- **On test failure** (before reporting — include anomalies in the failure context)
- **At session end** (final drain for the test report)

## Daemon & Metro Logs

Two additional log sources complement the JS interceptors:

### Daemon log

Records CLI events, session lifecycle, and tool execution timing.

```bash
# Read last 50 lines
tail -50 .mm-daemon.log

# Search for errors
grep -i "error\|fail\|crash" .mm-daemon.log | tail -20
```

### Metro output

Metro logs JS errors, warnings, and bundle events. When running Metro separately (`yarn watch:clean`), redirect output to a file:

```bash
yarn watch:clean 2>&1 | tee .mm-metro.log &
```

Then check for errors during testing:

```bash
grep -i "error\|warn\|exception" .mm-metro.log | tail -20
```

## Gotchas

- **JSON-RPC errors return HTTP 200.** Infura and relay services return `{"error": {"message": "..."}}` in the response body with a 200 status code. Without the `rpcError` field extraction (included in the default interceptor above), these errors are completely invisible — a failed `eth_sendRawTransaction` looks identical to a successful one at the HTTP level. Always check `rpcError`, not just `status`, when debugging transaction failures.
- **Many app errors never reach `console.error`.** Controllers like TransactionController catch RPC exceptions internally and update state (e.g., marking a transaction as "failed") without any console output. The console interceptor will not capture these. To detect on-chain failures, check the `rpcError` field in network entries or verify transaction status via the UI/activity list.
- **Response body cloning is async.** The `rpcError` field is populated asynchronously via `resp.clone().text().then(...)`. In rare cases, if you drain the buffer immediately after a request completes (< 1ms), the `rpcError` field may not yet be populated. A brief `sleep 1` before draining after a transaction submission avoids this.
- The Engine module walk triggers **multiple dev error overlays** (typically 3–4). You must dismiss all of them in a loop, not just the first one. See [Dismissing Dev Error Overlays](#dismissing-dev-error-overlays) for the pattern.
- Interceptors are **lost on Fast Refresh and app reload**. After any code change with Metro watch mode, re-run the install command. Use the health check to verify.
- The fetch interceptor captures **JS-level fetch only**. Native HTTP calls (iOS URLSession, image loading, WebSocket connections) are not captured.
- Buffer auto-trim is aggressive (1000-2000 entries) to prevent memory pressure. For long test sessions, drain periodically to avoid losing early entries.
- Console interceptor wraps `log`, `warn`, and `error`. It skips `debug` and `info` to reduce noise. If you need those, modify the `forEach` array in the install expression.
- The `url` field for `fetch(Request)` calls extracts `Request.url`. If the app uses a custom fetch wrapper that passes non-standard first arguments, the `url` may show `[object Object]`.
- `returnByValue: true` is required in the cdp params. Without it, you get a remote object reference instead of the actual JSON string.
- Interceptors add ~0.1ms overhead per fetch call (~0.2ms for RPC requests due to response cloning). No measurable impact on app performance during testing.
