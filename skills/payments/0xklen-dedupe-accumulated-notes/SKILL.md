---
name: dedupe-accumulated-notes
description: Use when the same fact has been written many times across notes. Normalizes and merges duplicates into one canonical entry with the strongest content.
---

# Dedupe Accumulated Notes

Repeated facts are not redundancy, they are drift: the copies disagree, and a reader gets whichever greps first. Deduping means merging to one entry that keeps the best content.

## Procedure

1. Normalise before comparing: lowercase, strip punctuation and timestamps into a scratch copy.
2. Find near-duplicates by shared key: `grep -rhoE '^[a-z][a-z0-9_-]+ *[:=]' notes/ | sort | uniq -c | sort -rn | head -20`.
3. For long prose, cluster by a shingle hash rather than exact match, so paraphrases group too.
4. For each cluster, pick the canonical entry: the one with a date, a source, and the most complete statement.
5. Merge the useful bits from the others into the canonical entry; do not concatenate, edit.
6. Delete the losers only after the merge is written and re-read.
7. Keep a tombstone line if the key is commonly searched: `deprecated: see notes/facts/prod-db.md`.
8. Re-run the duplicate finder to confirm the cluster is down to one.
9. Fix the source that keeps re-creating the duplicate, or the cluster returns next week.
10. Log the merge: key, count before, count after.

## Pitfalls

- Exact-match dedupe that misses three paraphrases of the same fact.
- Merging by concatenating both texts, so the entry now says two different things.
- Deleting the loser before writing the canonical version, losing the only dated copy.
- Deduping on raw text including dates, so a fact re-confirmed each month looks unique each time.
- Cleaning the output while the input process keeps emitting duplicates, so the pile regrows.

- Deduping notes but not the index built from them, so search still returns the loser.
- Merging entries from different scopes (prod vs staging) because their text is identical.
- Rewriting duplicates to one file but leaving originals a reader still opens from git history.

## Verification

    grep -rhoE '^[a-z][a-z0-9_-]+ *[:=]' notes/ | sort | uniq -d | wc -l
    # passes when the duplicate-key count is 0

Report to the user: the keys deduped, the before/after counts, and the source fixed to stop the regrowth.
