---
name: attach-stable-citation-ids
description: Use when answers cite sources that cannot be found again. Assigns each chunk a stable id derived from content and version so every claim links back to a retrievable span.
---

# Attach Stable Citation IDs

A citation is useless if the reader cannot resolve it, and a citation that changes on every re-ingest is not a link. Give every chunk an id that survives re-indexing as long as its content and source version do.

## Procedure

1. Derive the chunk id from stable inputs, not from insertion order: `id = sha1(source_uri + version + char_start + char_end)[:12]`.
2. Store the id alongside the text, the `source_uri`, the `version` (commit or doc revision), and the offsets.
3. Emit answers with inline markers referencing those ids: `Refunds are processed in 5 days [doc:sha1abc123]`.
4. Resolve a marker for the user by rendering `source_uri#L{start}-L{end}` as a clickable link.
5. Re-ingesting unchanged content must reproduce the same id — verify by re-running the loader and diffing ids.
6. When content changes, the id changes; keep the old id in a `supersedes` field so stale citations resolve to history.
7. Never cite a generated summary as the source; cite the chunk the summary was drawn from.
8. Reject an answer whose citations do not resolve to ids present in the current index.
9. Include the retrieval timestamp with each citation, because a source can change after the answer.
10. Preserve ids through re-chunking where possible; a full re-chunk is a new version and should be labelled as one.

11. Validate the id format with a regex before it enters an answer, so a malformed id cannot masquerade as a citation.

## Pitfalls

- Using a list index as the id, so adding one document shifts every citation downstream.
- Citing the document title when the claim came from one paragraph, leaving the reader to re-search it.
- Hashing the chunk text alone, so two identical boilerplate chunks collide into one id.
- Broken links after ingest because offsets were recomputed on normalised text, not the original.
- Letting the model invent citation markers: validate every marker against the retrieved set before shipping.
- Quoting a source that was later edited, without recording the version that was actually read.

- Truncating the hash so two different spans collide on the same short id.
- Reusing a document version label across an edited file, so the citation points at text that never existed.

## Verification

    python3 ingest.py --check-ids  # re-run loader, ids must be byte-identical for unchanged docs
    grep -oE '\[doc:[0-9a-f]{12}\]' answer.md | while read m; do
      id=${m:5:12}; grep -q "$id" index/ids.txt || echo "unresolved $id"; done
    # passes when every citation resolves to a current index id

Report to the user: citation count, how many resolved, and any unresolved markers with the claim they backed.
