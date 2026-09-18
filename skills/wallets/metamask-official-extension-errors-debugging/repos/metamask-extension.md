---
repo: metamask-extension
parent: extension-errors-debugging
---

## Sentry Filters

Filter by `dist` tag to isolate manifest version:
- `dist:mv3` — Chrome builds
- `dist:mv2` — Firefox builds

Filter by `installType` to exclude developer-loaded builds:
- `installType:normal` — store-installed
- `installType:development` — sideloaded (unpacked); includes production builds loaded via developer mode

## Build Commands

```bash
# MV3 development (Chrome, service worker)
yarn start

# MV2 development (Firefox, background page)
yarn start:mv2

# Production build (both manifests)
yarn dist

# After dependency changes — regenerate LavaMoat policies
yarn lavamoat:auto
```

## Background Keepalive

| Property | Value |
|---|---|
| Location | `app/service-worker.ts:9-20` |
| Function | `saveTimestamp` at `service-worker.ts:11-15` calls `chrome.storage.session.set({ timestamp })` |
| Cadence | 2000 ms via `setInterval` |
| Effect | Each call resets Chrome's 30s SW idle timer — prevents idle eviction during active sessions |
| Gate | None in 13.41.0 and later. Earlier builds: `PreferencesController.enableMV3TimestampSave !== false` |

Active-session keepalive failures are rare and should be investigated as code bugs, not platform behavior. Cold-start cascade and first-flush latency are the actual MV3-concentrated failure modes — see `mv3-service-worker` knowledge for mechanism, failure modes table, and verification discipline.

## Controller-Messenger Pattern

Controllers communicate via `ControllerMessenger` (`@metamask/base-controller`). A controller's public API is its registered actions and events — not direct method calls. Cross-controller calls that bypass the messenger will not work across the background/UI boundary.
