---
name: snapshot-and-version-a-knowledge-base
description: Use when a wrong answer may trace to a specific corpus state that has since changed. Snapshots the chunk set, embeddings and index config as one versioned unit so any answer is reproducible.
---

# Snapshot and Version a Knowledge Base

When an answer was wrong last week, you need the exact chunks, vectors and splitter that produced it — not the current corpus. A knowledge base version is the whole pipeline state, addressable and reproducible.

## Procedure

1. Define a version as the tuple: chunker id, embedding model id, chunk set hash, and index build id — all four.
2. On every build, write `kb/versions/<version>.json` with those fields plus a UTC timestamp and the source manifest hash.
3. Store the chunk set durably (`chunks-<version>.jsonl`), not just its hash, so a past retrieval can be rebuilt exactly.
4. Tag the serving index with its version, and log the version on every query and answer.
5. Never mutate a built version in place; a change creates a new version and a new tag.
6. Keep the previous version servable for a rollback window; switching is a pointer change, not a rebuild.
7. Tie every evaluation run to a version id so a metric is always attached to a corpus state.
8. On answering a "why did it say X" question, pull the chunk set for the logged version and reconstruct.
9. Retain versions by policy: keep the last N and any that served during an incident.
10. Document the diff between two versions (documents added/removed/changed) so drift is explainable.

11. Record the serving version in every eval result so a metric and a corpus state are never separated.

## Pitfalls

- Versioning the code but not the corpus, so the same commit produces different answers a week apart.
- Rebuilding over the same version tag, destroying the state a past answer depended on.
- Storing only the chunk hash, so the text can never be recovered for a reconstruction.
- Logging the version on the index but not on the query, so answers cannot be tied to a state.
- Keeping so many snapshots that storage cost forces deleting the one an incident needs.
- Tagging the model id but not the chunker version, so a splitter change is invisible.

- A snapshot that stores the index but not the chunker config, so it cannot be rebuilt.
- Versioning the corpus but not the query rewriter, so two runs of one version differ.

## Verification

    jq -r '.version,.chunker,.model,.chunks_sha,.built_at' kb/versions/*.json | tail -5
    python3 rebuild.py --version kb-2026-10-08.3 --out /tmp/rebuilt.jsonl  # must match stored chunk set hash
    # passes when any logged answer's version rebuilds byte-identically

Report to the user: current version id, its four fields, the retention policy, and confirmation that a past version reconstructs.
