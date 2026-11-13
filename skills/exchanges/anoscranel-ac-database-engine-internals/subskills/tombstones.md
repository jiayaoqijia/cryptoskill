---
name: tombstones
domain: software-engineering/tombstones
trigger: "Understanding deletion in structures that do not overwrite."
anti_trigger: "Not for application cache invalidation (ac-caching-and-invalidation)."
scope: "Deletion as a write, the reclamation it defers, and the read cost it adds."
status: seedling
---

# Tombstones

## Standard

In an append-only structure there is no place at which to erase a key, so deletion writes a record that says the key is gone. The tombstone does not remove anything; it masks older copies of the key from queries until a merge folds it together with the copies it masks and physically discards both.

Until that merge, a deleted key still occupies space, and a read of that key still encounters the tombstone before concluding absence. Deletion is therefore a write, and reclamation is a later merge scheduling question. A workload that deletes heavily and reads by key will pay storage for the dead pairs and read cost for the mask, and the visible symptom — space not reclaimed, deletes not making reads faster — is the design working as intended rather than a fault.

Primary sources: <https://github.com/facebook/rocksdb/wiki/Compaction> and <https://github.com/google/leveldb/blob/main/doc/impl.md>.

## Decision rules

- Record deletion as a write in cost accounting.
- Record the presence of tombstones in space accounting until reclamation.
- Record the read path of a deleted key and where its absence is concluded.
- Record the migration of the deleted key's identifier from one masking to another.
- Record the merge that reclaims the dead pairs and when it is scheduled.
- Record dropped tombstones — those that follow a merge that physically discarded nothing but the expired mask.

## Procedure

1. Insert, then delete, a key in the structure.
2. Record the storage still occupied by key, tombstone, or both.
3. Record the read path length for the deleted key before reclaim.
4. Wait for or run the merge that merges the tombstone with the key's older copies.
5. Record the space reclaimed and the read path after.
6. Write the record with deletion's full cost: one write now, storage until the merge, and a read-path mask.

## Anti-patterns

- Expecting disk space to shrink on delete.
- Treating deletion as free because no copy is physically discarded.
- Shortening a key's read path by adding an unsorted mask.
- Compacting only when the read path degrades, without recording the space already held.
- Dropping expired masks early without discarding the copies they mask.

## Done checklist

- [ ] Deletion recorded as a write.
- [ ] Space held until reclamation recorded.
- [ ] Read path of the deleted key recorded pre-merge.
- [ ] Merge reclaim recorded post-merge.
- [ ] Read path after reclaim recorded.
- [ ] Full deletion cost written as three lines.

## Sources

- RocksDB deletion and compaction behaviour: <https://github.com/facebook/rocksdb/wiki/Compaction>
- LevelDB deletion markers and compaction: <https://github.com/google/leveldb/blob/main/doc/impl.md>
- Log-structured merge trees and deletion cost: <https://en.wikipedia.org/wiki/Log-structured_merge-tree>
