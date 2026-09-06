# Eternl dApp Browser — iframe wallet connection (postMessage bridge)

How to connect a dApp to a wallet that loads it inside an **iframe / webview**
instead of injecting `window.cardano` — primarily Eternl's `eternl.io`
"dApp browser" tab and its iOS/Android in-app browser. Companion to Step 5 of
`SKILL.md`.

## Why normal CIP-30 discovery fails here

Browser extensions inject `window.cardano.<wallet>` into every page. A wallet's
**dApp browser** doesn't run an extension in your page's context — it loads your
site cross-origin in an iframe (web) or a webview (mobile) and the wallet lives
in the **parent** frame. It therefore cannot synchronously inject into your
page's `window.cardano`. Instead it exposes the CIP-30 API over `postMessage`.

A dApp that only enumerates `window.cardano.*` (the standard discovery in Step 3)
finds nothing inside the dApp browser → empty picker, dead connect button — even
though the exact same build works in the desktop extension.

## The bridge

- **npm:** `@eternl/cardano-dapp-connector-bridge` — single export
  `initCardanoDAppConnectorBridge(onBridgeCreated?: (api) => void): void`. CJS +
  TypeScript types, SSR-guarded (`typeof window === 'undefined'` → returns).
- **Source:** https://github.com/Tastenkunst/cardano-dapp-connector-bridge
  (author = Tastenkunst GmbH, the Eternl developer). Bridge file:
  `src/bridge/cardano-dapp-connector-bridge.js` (+ `.min.js`); dApp-side init
  examples under `src/dapp/`; integration notes in `EternlDAppBrowser.md`.
- **Official docs:** https://wiki.eternl.io/en/5_for-developers/dapp-integration

## Handshake protocol (what actually happens)

1. The wallet (parent window) loads your dApp into the iframe and `postMessage`s a
   `connect` with `{ walletNamespace /* e.g. "eternl" */, initialApi: { isBridge:
   true, apiVersion, name, icon, experimental } }`, plus the event's `origin` and
   `source` (a reference to the parent window).
2. The bridge in your page validates the message, then `initBridge(...)`:
   - ensures `window.cardano = {}`, then sets
     `window.cardano[walletNamespace]` to an object exposing `isBridge: true`,
     `enable()`, `isEnabled()`, `apiVersion`, `name`, `icon`, and `experimental`
     (which includes `feeAddress`);
   - records the parent `source` + `origin` to address replies to.
   - If `window.cardano[walletNamespace]` **already exists** (desktop extension
     in the same browser), it logs a warning and **skips** — which is why calling
     `initCardanoDAppConnectorBridge` unconditionally is safe everywhere.
3. The bridge replies `handshake`; on success it invokes
   `onBridgeCreated(window.cardano[walletNamespace])`.
4. Thereafter every method call becomes a `createRequest(method, ...args)` that
   `source.postMessage(payload, origin)`s with a UID; the wallet replies
   `{ uid, response | error }`, resolving/rejecting the matching promise. The
   `enable()` response is itself a map of method-name strings, which the bridge
   reconstructs into the full CIP-30 api object dynamically. There is no fixed
   client-side method list beyond `connect` / `handshake` / `enable` /
   `isEnabled` — the rest are declared by the wallet at runtime.

Net effect: after `onBridgeCreated` fires, `window.cardano.eternl` behaves like a
normal CIP-30 provider and the rest of your code is unchanged.

## Auto-connect across all three Eternl surfaces

| Surface | Mechanism | Behaviour |
|---|---|---|
| Desktop **extension** | direct `window.cardano.eternl` injection | normal discovery + persisted reconnect; first-time connect requires a user gesture (extensions reject a cold `enable()`) |
| `eternl.io` **dApp browser** (web) | postMessage bridge | `onBridgeCreated` fires → auto-connect |
| Eternl **mobile app** dApp browser | postMessage bridge | `onBridgeCreated` fires → auto-connect |

The bridge callback fires **only** inside a dApp browser (after a real handshake),
so auto-connecting in it is safe and never triggers on a plain desktop page. Use a
single guard so the bridge path and the stored-reconnect path can't double-`enable()`:

```tsx
useEffect(() => {
  let cancelled = false;
  const connected = { current: false };
  const autoConnect = (id: string) => {
    if (cancelled || connected.current) return;
    connected.current = true;
    void doConnect(id); // your existing window.cardano[id].enable() flow
  };

  // dApp browser (web + mobile): wallet arrives over the bridge.
  initCardanoDAppConnectorBridge(() => { refreshInstalled(); autoConnect("eternl"); });

  // Extensions: poll window.cardano ~4s and reconnect the stored wallet.
  // ... (unchanged) ...

  return () => { cancelled = true; };
}, [doConnect, refreshInstalled]);
```

## Framing / CSP requirements

The page must be embeddable in an iframe by the wallet's origins:
- Do **not** send `X-Frame-Options: DENY` or `SAMEORIGIN`.
- If you set a CSP, `frame-ancestors` must include the wallet origins, e.g.
  `Content-Security-Policy: frame-ancestors 'self' https://*.eternl.io https://eternl.io`.
  A bare `frame-ancestors 'self'` blocks framing.
- **`Unrecognized origin: 'self'`** in the wallet-app console is the signature of
  this framing/origin mismatch. (If your page visibly loads and renders inside the
  dApp browser, framing is already fine and the bug is simply the missing bridge.)

## Console noise that is NOT your bug

Lines originating in `contentscript.js` —
`MaxListenersExceededWarning: Possible EventEmitter memory leak`,
`ObjectMultiplex - orphaned data for stream "…-liveness"`,
`ObjectMultiplex - malformed chunk without name` — come from a MetaMask-style
extension's content script present in the environment, unrelated to the dApp or
the wallet bridge. Ignore them when triaging.

## Listing vs functioning

Eternl's **comfort/convenience fee** (0.1% or 1 ADA, whichever is higher, on
buy/swap orders ≥ 100 ADA) is a requirement to be **listed** in Eternl's curated
dApp browser — it is **not** required for the bridge to work. You can make the
connection work first and handle listing separately.

## Sources

- https://github.com/Tastenkunst/cardano-dapp-connector-bridge — `EternlDAppBrowser.md`, `src/bridge/`, `src/dapp/`
- npm `@eternl/cardano-dapp-connector-bridge`
- https://wiki.eternl.io/en/5_for-developers/dapp-integration
