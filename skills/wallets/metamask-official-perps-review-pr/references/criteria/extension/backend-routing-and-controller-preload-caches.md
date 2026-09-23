# Backend Routing and Controller Preload Caches

A backend route or provider endpoint change updates the preload and cache-prime paths (`cachedMarketDataByProvider`, `PerpsStreamBridge`'s `startMarketDataPreload`) and the reconnect fallback, not only the explicit UI fetch, or warm restarts keep serving the stale route.

- **Preload cache not updated alongside explicit fetch path** — whenever a backend route or provider endpoint changes, grep for all preload and cache-prime call sites (`cachedMarketDataByProvider`, `PerpsStreamBridge`'s `startMarketDataPreload`) and verify they resolve through the same updated path.
- **Reconnect fallback bypasses cache invalidation** — reconnect handlers that re-init from cache without invalidating first will restore the old route after a network interruption.
- **Cache TTL assumes a route that no longer exists** — if the TTL or stale-while-revalidate window is longer than the rollout window for a backend routing change, the cache will serve the old route to users who reconnected within that window.
