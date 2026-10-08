---
name: detect-a-stale-knowledge-base
description: Use when a retrieval index may predate the documents it serves. Compares per-document source hashes against the index and flags drifted, deleted and new documents.
---

# Detect a Stale Knowledge Base

An index answers from the corpus as it was at build time, not as it is now. Staleness is invisible until an answer contradicts a document, so it must be measured on a schedule.

## Procedure

1. Store the source hash and mtime per document at ingest, e.g. `sha256sum` of the raw file in the index record.
2. On each check, recompute the source hashes: `find docs -type f -name '*.md' -exec sha256sum {} + | sort > /tmp/now.sha`.
3. Diff against the index's recorded hashes to classify each document as `unchanged`, `changed`, `deleted`, or `new`.
4. Treat `changed` and `deleted` as correctness bugs: the index still serves retired text as current.
5. Age the drift: if the newest index build is older than the freshness SLO (e.g. 24h for a live KB), alert regardless of diffs.
6. Report the ratio drifted/total; above a threshold (say 2%) the whole index needs a rebuild, not a patch.
7. Feed the `changed` set to the incremental refresh path; `deleted` must remove the chunk ids, not just orphan them.
8. Watch the answer side too: a chunk that cites a source revision that no longer exists is a stale citation.
9. Schedule the check where the drift cannot be silently skipped — a cron with an alert on non-zero drift.
10. Record every check to `kb/freshness.jsonl` so staleness has a history, not just a current value.

11. Alert on the age of the newest successful build, not only on a diff, so a stopped ingester is caught.

## Pitfalls

- Hashing normalised text instead of the raw file, so a formatting-only change looks unchanged while content moved.
- Rebuilding on mtime alone; a copied file gets a fresh mtime with stale contents.
- Removing a document from the index but leaving its chunk ids resolvable, so dead citations still click.
- Checking freshness only when someone complains, which is after the wrong answer shipped.
- Trusting a source's own "updated" field rather than the bytes you actually ingested.
- A rebuild that succeeds but writes to a new collection while serving still reads the old one.

- A freshness check that runs but whose exit code is ignored by the scheduler.
- Treating a document moved between directories as unchanged because the content hash matched.

## Verification

    python3 freshness.py --index index/ --docs docs/ --slo-hours 24
    # passes when drift ratio is 0 for unchanged sources and every changed/deleted doc is queued for refresh

Report to the user: documents scanned, drift ratio, the list of changed and deleted docs, and the age of the last build.
