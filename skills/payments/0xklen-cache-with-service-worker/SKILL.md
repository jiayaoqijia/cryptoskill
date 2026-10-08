---
name: cache-with-service-worker
description: Use when repeat visits should be offline-capable and instant. Precaches app shell assets with Workbox and serves data with stale-while-revalidate.
---

# Cache with a Service Worker

A service worker is the only way to make a repeat visit paint from disk in under 100 ms. It also gives you a cache you can corrupt, so versioning discipline is the whole job.

## Procedure

1. Generate the precache manifest at build time so every hashed asset is listed, not hand-typed:

       npx workbox-cli generateSW workbox-config.js

2. Set the strategy per route: precache the app shell, `stale-while-revalidate` for GET API data, `network-first` for volatile config, `cache-first` for immutable static hashes.
3. Cap cache growth so a long-lived user does not fill the disk quota:

       workbox.routing.registerRoute(({request}) => request.destination === 'image',
         new workbox.strategies.CacheFirst({cacheName: 'imgs',
           plugins: [new workbox.expiration.ExpirationPlugin({maxEntries: 80, maxAgeSeconds: 30*24*3600})]}));

4. Beat the 24-hour cache update rule: ship a small `sw.js` that changes each deploy (a build hash in a comment) so the browser byte-compares and updates.
5. Handle the `activate` lifecycle by deleting caches whose name is not in the current list; otherwise old shells accumulate.
6. Guard `skipWaiting`/`clients.claim` behind an explicit reload prompt so users are not swapped mid-session.

## Pitfalls

- Precaching before hashing is applied, so the manifest lists stale filenames and every fetch misses.
- Deleting all caches in `activate` without excluding the newly created one, blanking the offline page.
- A cache-first strategy on `/api/` returning yesterday's prices forever.
- Forgetting that the SW intercepts navigation, so a bad deploy serves a cached 200 for a route that now 404s.
- No cache size cap, letting a chatty image route quietly exhaust the origin quota and evict everything.

## Verification

    # DevTools -> Application -> Service Workers: reload twice offline
    curl -sI https://shop.example.com/sw.js | grep -i 'cache-control'

`sw.js` must be served `no-cache` so the browser can byte-check it. Report the precache entry count and a cold-reload repeat-visit timing from the Network panel.
