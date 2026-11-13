---
name: offline-and-sync
domain: software-engineering/offline-and-sync
trigger: "Reading and writing on the web without a network, and reconciling afterwards."
anti_trigger: "Not for mobile-device sync, and not for general caching strategy."
scope: "Reads and writes without a network, and the sync that follows."
status: seedling
---

# Offline and sync

## Standard

An offline-capable web app continues to serve reads from a cache and queues writes when the network is gone, then reconciles when it returns. The reads come from a service worker that intercepts requests and answers from storage; the writes come from a durable local queue that survives reload; the reconciliation is the honest part — a write made offline may fail on the server, and the queue must surface that failure to the user rather than silently drop it.

Offline is a promise with a budget, and the budget is stated, not discovered. Storage quotas are finite and evictable; a cache has a lifetime policy per resource class — the shell cached long, data cached short, some data never. The update flow is part of the design: when a new version of the app is deployed, the running instance is old until it reloads, and the user needs a path from "an old tab is running" to "the new version is live" without losing their work.

Primary sources: <https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API> and <https://developer.chrome.com/docs/workbox/>.

## Decision rules

- State what works offline — reads, writes, or both — and what the app shows when nothing is available.
- Choose a cache strategy per resource class: network-first, cache-first, stale-while-revalidate, or never-cache.
- Queue writes durably, with an identifier per queued write for later reconciliation.
- Surface sync outcomes: succeeded, failed, conflicted — silent drops are data loss with a UI.
- State the quota budget and what happens when the browser evicts the storage.
- Design the update flow: detect a new version, prompt the reload, never destroy in-progress work doing it.

## Procedure

1. Classify resources into cache strategy classes and write the policy.
2. Implement the service worker read path and the durable write queue.
3. Define reconciliation: identifier matching, retry policy, failure surfacing.
4. State the quota budget and eviction behaviour.
5. Implement the new-version detection and reload flow.
6. Test offline reads, offline writes, reconnect, eviction, and update-while-editing.

## Anti-patterns

- Promising offline with no statement of what data is cached and for how long.
- Queuing writes in memory that a reload silently discards.
- Treating all failed syncs as retryable — some are permanent failures the user must see.
- Caching API responses indefinitely because it makes the demo feel fast.
- Reloading into the new version without checking for unsaved work.

## Done checklist

- [ ] Offline surface stated.
- [ ] Cache policy per resource class.
- [ ] Durable write queue with identifiers.
- [ ] Reconciliation and failure surfacing.
- [ ] Quota and eviction stated.
- [ ] Update flow tested with work in progress.

## Sources

- Service worker API: <https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API>
- Workbox caching practice: <https://developer.chrome.com/docs/workbox/>
- PWA patterns: <https://web.dev/learn/pwa>
