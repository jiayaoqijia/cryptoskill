---
name: freshness-and-rebuilds
domain: software-engineering/freshness-and-rebuilds
trigger: "Keeping a retrieval index current without rebuilding it constantly."
anti_trigger: "Not for embedding model migration, and not for database replication."
scope: "Incremental updates, tombstones, and the cost of a full re-embed."
status: seedling
---

# Freshness and rebuilds

## Standard

An index is a derived store, and it lags its source by however long the update path takes. That lag is a product decision rather than an implementation detail: a support search that returns yesterday's answer is acceptable, while a search over prices or inventory that returns yesterday's answer is not. Stating the freshness requirement first is what allows the update mechanism to be chosen rather than inherited.

Deletion is the part that is usually wrong. An embedding has no notion of removal, so a deleted document persists in the index until something removes it, and a naive update path that inserts new chunks without tombstoning the old ones produces duplicates and stale answers. The record should state how deletion propagates and how long the index can serve a deleted document.

Primary sources: <https://nlp.stanford.edu/IR-book/> and <https://www.nist.gov/>.

## Decision rules

- Record the freshness requirement as a stated maximum lag.
- Record the update mechanism: streaming, periodic batch, or on-demand.
- Record the deletion path and the maximum time a deleted document remains retrievable.
- Record the tombstone mechanism and how tombstones are compacted.
- Record the full re-embed cost and the conditions that force one.
- Record how lag is measured, since an unmeasured lag cannot be maintained.

## Procedure

1. Record the freshness requirement per use case.
2. Record the update mechanism and its measured lag.
3. Record the deletion propagation path.
4. Record the tombstone and compaction behaviour.
5. Estimate the full re-embed cost and its triggers.
6. Write the freshness contract with its measurement.

## Anti-patterns

- Assuming deletion removes the vector.
- Setting a freshness target without measuring the actual lag.
- Rebuilding the whole index for a small change.
- Leaving tombstones uncompacted until the index is mostly dead entries.
- Treating the index as the source of truth rather than a derived store.

## Done checklist

- [ ] Freshness requirement recorded.
- [ ] Update mechanism and lag recorded.
- [ ] Deletion path recorded.
- [ ] Tombstone behaviour recorded.
- [ ] Re-embed cost recorded.
- [ ] Lag measurement recorded.

The lag also differs by content type: a document added is visible as soon as its embedding lands, while a document edited may leave its old chunks retrievable until they are tombstoned, so the effective freshness of an update is worse than the freshness of an insert. Recording the two separately avoids a target that is met on inserts and missed on edits.


## Sources

- Information retrieval update strategies: <https://nlp.stanford.edu/IR-book/>
- Measurement guidance: <https://www.nist.gov/>
- Data pipeline context: <https://nlp.stanford.edu/IR-book/html/htmledition/contents-1.html>
