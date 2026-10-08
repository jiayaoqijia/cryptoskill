---
name: refresh-an-index-incrementally
description: Use when re-embedding the whole corpus for a few changed documents wastes hours. Updates, upserts and deletes only the chunks whose source hash changed since the last build.
---

# Refresh an Index Incrementally

Full rebuilds are correct but expensive; incremental refresh is the same result for the diff. The danger is orphans — chunks that belong to a document that changed or vanished but were never removed.

## Procedure

1. Compare source hashes to the index (`detect-a-stale-knowledge-base`) to get the `changed`, `deleted` and `new` sets.
2. For each changed document, delete all existing chunk ids with that `source_uri` before inserting the new chunks.
3. Upsert by the stable chunk id (`attach-stable-citation-ids`) so an unchanged chunk is overwritten, not duplicated.
4. Embed only the new chunk texts; reuse cached embeddings for identical content (`cache-embeddings-by-content-hash`).
5. Apply deletes first, then inserts, in one batch per document so a crash cannot leave both old and new versions live.
6. Commit the index and the source-hash manifest together; if the manifest advances but the index does not, the next run will skip the change.
7. Rebuild only on schema changes — chunker, embedding model, or metadata shape — not on ordinary edits.
8. Verify post-refresh that the index holds no chunk whose `source_uri` no longer resolves to a file.
9. Run the retrieval eval after a refresh; a broken delete shows up as duplicate or stale hits.
10. Keep a rebuild path that works from scratch, so a corrupted index can be discarded, not repaired.

11. Record the refresh as a transaction id per document so a partially applied batch can be retried exactly.

## Pitfalls

- Inserting new chunks without deleting the old ones, so the index quietly doubles and returns both versions.
- Advancing the hash manifest before the index commit, so a crash loses the change permanently.
- Re-embedding every chunk because the loader cannot tell which text changed.
- Deleting by source path while the path was renamed, leaving the old path's chunks alive forever.
- Running the refresh in the same collection without a version tag, so a partial failure is undetectable.
- Assuming upsert is delete-then-insert when the backend only inserts, creating hidden duplicates.

- Retrying a refresh that failed after the deletes but before the inserts, losing content until the retry lands.
- Advancing the source manifest when the embedding call fails, so the changed document is marked done.

## Verification

    python3 refresh.py --index index/ --manifest kb/hashes.json
    ls index/orphans.txt 2>/dev/null && echo "ORPHANS PRESENT" || echo "no orphans"
    # passes when orphan count is 0 and eval recall is unchanged from the pre-refresh baseline

Report to the user: documents changed, chunks deleted and inserted, embeddings computed vs reused, and the eval delta.
