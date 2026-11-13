---
name: server-versus-ui-state
domain: software-engineering/server-versus-ui-state
trigger: "Separating the server copy from local UI state and invalidating the copy."
anti_trigger: "Not for component structure basics, and not for offline storage."
scope: "The two kinds of client state, the data layer, and invalidation."
status: seedling
---

# Server versus UI state

## Standard

Server state is a cache. The server owns the truth, the client holds a copy with a fetch time, and the copy's validity decays. UI state — selections, open panels, half-typed input, hover — is owned by the client and dies with the session. These two kinds of state have opposite rules: server copies want refetching, caching, and invalidation; UI state wants to be left alone by anything except the component that owns it. The pathologies come from crossing the wires — a background refetch resetting a form, a UI toggle cached as if it were data, a server copy mutated locally as if the client were its owner.

The fix is a data layer. Queries read from the server copy, mutations write to the server and invalidate affected queries, and the layer owns keys, deduplication, and staleness. Components keep UI state in their own scope and read server data through the layer. The question "where does this state live" then has a structural answer: if the server owns it, the layer; if the session owns it, the component; if the URL owns it, the URL.

Primary sources: <https://tanstack.com/query/latest/docs/framework/react/overview> and <https://web.dev/learn/performance>.

## Decision rules

- Classify every piece of state: server copy, UI state, or URL state — mistyped state is the root bug.
- Server copies live in the data layer keyed by what they represent, never in component state that a refresh could clobber.
- Mutations invalidate the affected queries; components never hand-patch server copies except as explicit optimistic writes.
- Refetch triggers are policy: mount, interval, window focus, or reconnect — chosen and stated, not defaulted silently.
- Derivable values are derived, not stored; storing a computed copy creates a second source of truth.
- Stale-while-revalidate is the default read posture; blocking the UI on refetch is a decision, not a habit.

## Procedure

1. List the application's state and type each as server copy, UI, or URL.
2. Give each server copy a key and a staleness policy in the data layer.
3. Move UI state to the owning component; remove it from any global store.
4. Wire each mutation to the queries it invalidates.
5. State the refetch triggers per query in the record.
6. Test the crossover cases: background refetch during editing, reconnect after sleep, two views of one key.

## Anti-patterns

- Copying server data into local state "just to render it" and never updating again.
- One global store holding server copies and UI booleans together.
- Mutating the local copy as if the client were the owner of the truth.
- Refetch-on-focus for expensive queries with no statement of cost.
- Deriving nothing — storing every computed value.

## Done checklist

- [ ] Every state item classified.
- [ ] Server copies keyed and staleness-stated in the layer.
- [ ] Mutations invalidate the queries they affect.
- [ ] UI state scoped to its owner.
- [ ] Refetch triggers stated per query.
- [ ] Crossover cases tested.

## Sources

- Data-layer patterns, server state: <https://tanstack.com/query/latest/docs/framework/react/overview>
- Frontend data fetching performance: <https://web.dev/learn/performance>
- Storage on the web: <https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API>
