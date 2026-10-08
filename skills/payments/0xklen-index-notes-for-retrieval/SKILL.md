---
name: index-notes-for-retrieval
description: Use when a growing note store is slow to search or misses obvious hits. Builds a keyword or embedding index and queries it instead of scanning every file.
---

# Index Notes for Retrieval

Scanning every file per query works at 50 notes and fails at 5,000. An index turns a linear scan into a lookup, but only if it is rebuilt whenever the notes change.

## Procedure

1. Decide the index type by the query shape: keyword (BM25 / grep-derived) for exact terms, embeddings for paraphrase.
2. Build the keyword index with a real tool, not ad-hoc grep: `python3 -m whoosh` or `rg --json > notes/.index.jsonl`.
3. Store one record per note: path, title, tags, and token counts; keep it beside the notes at `notes/.index.jsonl`.
4. For embeddings, chunk notes to ~500 tokens with overlap so a hit does not fall on a chunk boundary.
5. Query the index, not the tree: read `notes/.index.jsonl`, score, take the top-k.
6. Stamp the index with the note tree's hash so you can tell it is current: `find notes -name '*.md' | xargs md5 | md5sum > notes/.index.sig`.
7. Rebuild the index whenever the signature changes; a stale index returns moved or deleted notes.
8. Keep the index out of the durable memory store — it is a derived artefact, regenerable at will.
9. Measure the result with `score-retrieval-quality`; an index that does not move recall is not worth maintaining.
10. Cap top-k at what you will actually read (10-20), not everything that matches.

## Pitfalls

- Building an index once and never rebuilding, so hits point at deleted or renamed notes.
- Indexing the raw text including dates and ids, so every version of a note is a separate hit.
- Chunking on fixed byte offsets and splitting a key sentence across two chunks.
- Returning 200 matches and pasting them all into the window instead of the top 10.
- Treating the index as a source of truth and editing it, when the notes are the truth.

- Indexing a symlinked or generated directory, so the index churns with artefacts.
- Serving from the index after a bulk rename and returning paths that no longer resolve.
- Rebuilding on every query instead of on signature change, which is slower than scanning.

## Verification

    wc -l notes/.index.jsonl; find notes -name '*.md' | wc -l
    # passes when index records == note count and the signature matches the current tree

Report to the user: the index type, the note and record counts, the signature match, and the recall from `score-retrieval-quality`.
