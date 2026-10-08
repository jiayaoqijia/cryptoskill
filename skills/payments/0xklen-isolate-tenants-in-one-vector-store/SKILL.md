---
name: isolate-tenants-in-one-vector-store
description: Use when one vector database serves multiple tenants and a query could cross the boundary. Uses namespaces or mandatory tenant filters with a boot-time assertion that isolation is active.
---

# Isolate Tenants in One Vector Store

Sharing a collection across tenants saves money until one tenant's query surfaces another's chunk. Isolation must be structural and asserted at startup, not remembered per call.

## Procedure

1. Pick the isolation model and write it down: separate collections (strongest), namespaces/partitions (strong), or a mandatory metadata filter (weakest).
2. If using a filter, make the tenant field non-nullable at ingest — a chunk with no tenant must fail to insert.
3. Wrap retrieval in a single function that requires a tenant argument, so no call site can forget it.
4. Add a boot-time self-test: insert a canary chunk per tenant, query as tenant A, assert tenant B's canary is absent.
5. Fail the process to start if the isolation self-test fails, rather than serving across tenants.
6. Keep tenant id in every chunk's metadata and in the embedding cache key, so ids never collide across tenants.
7. Size quotas per tenant (`enforce-per-tenant-storage-quotas`) so one tenant cannot exhaust shared capacity.
8. Re-derive tenant ids at query time from the authenticated principal, never from a request parameter the client controls.
9. On tenant deletion, remove all their chunks and cache entries in one transaction; orphaned vectors are a leak.
10. Monitor cross-tenant hit rate as a metric; any non-zero value is a P1, not a warning.

11. Snapshot the isolation self-test result with the deploy, so a config that drops the filter is caught in review.

## Pitfalls

- Adding the tenant filter in the search layer but not in the ingest cache, so one tenant's embeddings are reused for another.
- Relying on a filter that the SDK silently drops when the metadata field is missing.
- Sharing an ANN graph so that tenant A's traversal path passes through tenant B's neighbourhoods.
- Testing isolation with a human-readable query that happens to have no cross-tenant near-neighbour.
- Namespacing reads but not writes, so a stray write lands in the default namespace that every query scans.
- Forgetting the cache and object storage layers that back the index.

- A migration that re-creates the collection without the tenant field, silently disabling isolation.
- Assuming the vector store enforces the filter when only the client library adds it.

## Verification

    python3 isolation_test.py   # inserts canaries, queries each tenant, asserts no cross-hits
    # passes when every tenant's query returns zero of any other tenant's canaries, on every run

Report to the user: isolation model, tenants covered, the canary test result, and the residual leak surfaces checked.
