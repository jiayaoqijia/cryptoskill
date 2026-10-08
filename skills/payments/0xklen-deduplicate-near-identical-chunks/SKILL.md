---
name: deduplicate-near-identical-chunks
description: Use when the index returns five copies of the same paragraph from boilerplate or mirrored docs. Detects near-duplicate chunks so one version is retrieved and the rest collapse.
---

# Deduplicate Near-Identical Chunks

Mirrored docs, license headers and repeat boilerplate fill a top-k with the same sentence five times, crowding out the one chunk that answers the question. Collapse near-duplicates before they consume the results.

## Procedure

1. Normalise for comparison only — lowercase, strip whitespace and punctuation — but keep the original text for the index.
2. Compute MinHash signatures with `datasketch`: `MinHash(num_perm=128)` over 5-gram shingles of the normalised text.
3. Build an LSH index (`MinHashLSH(threshold=0.9)`) and query each chunk to find its near-duplicates.
4. For each duplicate cluster, keep one representative (the longest, or the shortest source path) and mark the rest as aliases.
5. At retrieval, map every hit to its cluster representative and deduplicate the result list by representative id.
6. Record `alias_of` in metadata so a user clicking a representative can see the other copies.
7. Choose the threshold from the corpus: 0.9 catches verbatim mirrors; below 0.7 collapses paraphrases and distinct answers.
8. Do not deduplicate across tenants or permission groups — one user's copy is not another's.
9. Re-run clustering after a bulk ingest; mirrored documents usually arrive in batches.
10. Exclude intentional repetition (a repeated table header, a per-page footer) from the keep-one rule by length.

11. Keep the dedup map versioned with the chunk set so a re-ingest can reuse the same representatives.

## Pitfalls

- Deduplicating at index time by overwriting, so the deleted copy's provenance and ACL vanish.
- Threshold set so low that two genuinely different answers score as duplicates and one is discarded.
- Hashing the raw text with headers and timestamps, so real duplicates never match.
- Collapsing duplicates before the ACL filter, merging chunks a caller may not all be allowed to read.
- Treating near-duplicate detection as exact hashing; a one-word difference defeats it while remaining a duplicate.
- Leaving the cluster map stale so new duplicates are retrieved alongside their representative.

- A new ingest that re-inserts a copy previously collapsed, so the representative and the copy both return.
- Clustering with a shingle size tuned for prose and applying it to code, where 5-grams are rare.

## Verification

    python3 dedup.py --chunks chunks.jsonl --threshold 0.9
    jq -s 'map(.alias_of // empty) | length' chunks_dedup.jsonl   # alias count
    # passes when clustered duplicates share a representative and top-k returns each cluster at most once

Report to the user: clusters found, chunks collapsed, the threshold used, and the top-k reduction on a sample query.
