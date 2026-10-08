---
name: rebuild-a-corrupted-index
description: Use when retrieval returns stale, missing, or broken results. Rebuilds the index from the source notes and verifies the record count before trusting it.
---

# Rebuild a Corrupted Index

When search returns a note that no longer exists, or misses one that does, the index is out of sync — not the notes. Rebuild from source and verify counts; never patch the index by hand.

## Procedure

1. Confirm the symptom is index-side: a note exists (`ls notes/x.md`) but search does not return it.
2. Check the index signature against the tree: `find notes -name '*.md' | xargs md5sum | md5sum` vs the stored `notes/.index.sig`.
3. If they differ, the index is stale; rebuild rather than patch.
4. Back up the old index first: `cp notes/.index.jsonl notes/.index.jsonl.bak`.
5. Rebuild from source notes only: `python3 build_index.py notes/ > notes/.index.jsonl`.
6. Verify record count equals note count: `wc -l < notes/.index.jsonl` vs `find notes -name '*.md' | wc -l`.
7. Spot-check three known notes are present and their content matches.
8. Re-run the failing query and confirm it now returns the note.
9. Update the signature so the next rebuild is triggered only on real change.
10. Find why it drifted — a delete that skipped reindexing is the common cause; fix that path.

## Pitfalls

- Hand-editing the index to add the missing record, leaving the rest still stale.
- Rebuilding over the only copy so a build bug destroys the working index too.
- Assuming the notes are corrupt when the index is merely stale.
- Reindexing without updating the signature, so the stale index is considered current forever.
- Counting records by eye instead of comparing totals, and shipping a partial index.

- Rebuilding while writes are in flight, so the new index is stale on arrival.
- Deleting the backup immediately, losing the only record of what the old index held.
- Fixing the index and not the writer that skipped reindexing on delete.

## Verification

    test "$(wc -l < notes/.index.jsonl)" = "$(find notes -name '*.md' | wc -l)" && echo counts-match
    # passes when counts match and the previously failing query returns its note

Report to the user: the drifting query, the record and note counts, the query re-run, and the path that skipped reindexing.
