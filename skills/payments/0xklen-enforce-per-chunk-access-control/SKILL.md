---
name: enforce-per-chunk-access-control
description: Use when a single index serves users who must not see each other's documents. Filters retrieval by the caller's permissions before ranking so no unauthorised chunk can reach the prompt.
---

# Enforce Per-Chunk Access Control

A vector index with no ACL is a search engine over everyone's data. Access must be applied at retrieval, not in the UI, because a filtered-out chunk that still ranks is a leak the moment the filter is forgotten.

## Procedure

1. Store an ACL on every chunk at ingest: the set of principals (users, groups, tenants) allowed to read it.
2. Filter at query time, inside the retrieval call, not after: pass `allowed: ["group:billing"]` into the vector search.
3. Prefer a pre-filter that the backend honours over post-filtering the top-k, since post-filtering silently shrinks results.
4. Model permissions as a closure: resolve the caller's groups to ids before the query, never at render time.
5. Default to deny: a chunk with an empty or absent ACL is not returned to anyone.
6. Re-derive the ACL from the source system on every re-ingest; a permission change upstream must propagate.
7. Test with a query that has a gold chunk the caller cannot read; it must be absent from the results, not merely unlinked.
8. Log every retrieval with the caller identity and the filter applied, so leaks are reconstructable.
9. Reject attempts to filter by client-supplied group ids; the server resolves the caller's groups itself.
10. Keep embeddings for restricted content in the same store only if the filter is enforced by the store; otherwise use separate collections per clearance.

11. Key any response cache by the resolved permission set, not just by the query string.

## Pitfalls

- Post-filtering the top-10 so a caller sees six results while the forbidden ones occupied ranks 1-3.
- Trusting a client to send its own permission list, which is trivially forged.
- Filtering on a tenant id that some chunks lack, so legitimate results vanish once the filter is on.
- Caching a result across callers without keying the cache by the permission set.
- An ACL update that changes the source document but not the stored chunk ACL.
- Leaking document existence through result counts even when the text is withheld.

- Caching a filtered result for one caller and serving it to a caller with broader permissions.
- A group rename upstream that leaves stored chunk ACLs pointing at a group that no longer exists.

## Verification

    python3 probe.py --as user:bob --query "acme invoices"
    # passes when every returned chunk lists user:bob or a group bob belongs to, and forbidden gold chunks are absent

Report to the user: chunks filtered vs returned for the probe, the ACL model used, and the pre- vs post-filter decision.
