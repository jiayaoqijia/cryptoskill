# Connection & WebSocket Architecture

- **Cleanup has no owner for in-flight setup**: Register the owner before asynchronous initialization starts. Timeout, unmount and feature disable must retire that owner and prevent late activation. Cover pre-registration and post-ready paths separately; successful UI disposal must preserve an explicitly owned reuse/grace policy.

A single `PerpsAlwaysOnProvider` at the wallet root owns connect/disconnect; `PerpsConnectionProvider` only exposes connection state (`isEnabled`, `isFullScreen`, `suppressErrorView`) through the singleton connection manager.

- **A second lifecycle owner** — a provider, hook, or screen that calls connect/disconnect itself (or a `PerpsConnectionProvider` variant that tries to) creates reference-count bugs. Only `PerpsAlwaysOnProvider` manages the lifecycle.
- **Unthrottled WS → setState** — every WS tick triggers state update. Must use `useLivePrices` with appropriate `throttleMs` (100ms for charts, 2s for lists, 10s for order forms).
- **Per-component WS subscription** — creating a new WebSocket connection per component instead of using `PerpsStreamManager` shared subscriptions with reference counting.
- **WS subscription leak** — subscribing on mount without unsubscribing on unmount or market switch. `PerpsStreamManager` handles ref counting but custom subscriptions must clean up.
- **Stale data after async gap** — reading position/order state, awaiting something, then using the stale read. WS updates change state between awaits. Re-read after async boundaries.
- **Static WebView work coupled to live ticks** — a payload containing both `currentPrice` and static overlays can resend teardown/recreate work on every tick. Compare the static subset before mutating chart lines, do not force autoscale on a no-op update, and cover skip/clear behavior with executable helper tests rather than source-string assertions.
- **Missing cache invalidation** — after trade/withdrawal/position change, not calling `PerpsCacheInvalidator.invalidate()` for affected cache types (`positions`, `accountState`). Standalone queries on token detail pages show stale data.
