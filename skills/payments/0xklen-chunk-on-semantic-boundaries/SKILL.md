---
name: chunk-on-semantic-boundaries
description: Use when splitting documents whose chunks start mid-sentence or mid-table. Splits on headings, paragraphs, list items and table rows before applying any size cap, so every chunk is a self-contained unit.
---

# Chunk on Semantic Boundaries

A chunk is the retrieval unit, so a chunk that begins mid-sentence retrieves badly and cites worse. Split where the document already splits — headings, paragraphs, list items, table rows — and only fall back to a size cap for sections that are still too large.

## Procedure

1. Parse structure before text. For HTML use `trafilatura` or `selectolax` to get block elements; for Markdown split on `^#{1,6} `; for PDF take per-page blocks with `pdftotext -layout`.
2. Emit one chunk per leaf section: a heading plus the paragraphs beneath it, up to the next heading of equal or higher level.
3. Keep tables whole. If a table must be split, split at row boundaries and repeat the header row in every piece.
4. Keep fenced code blocks whole; a function cut across two chunks is unsearchable from either side.
5. Attach the heading path to each chunk as metadata: `{"h1": "Billing", "h2": "Refunds"}` so the topic travels into the prompt with the text.
6. Only after structural splitting, apply a token cap (~1000-1500 tokens) to any oversized section, splitting at paragraph boundaries.
7. Never split at a fixed character offset: "the limit is 5" / "00 requests" is worse than one long chunk.
8. Prefix the embedded text with its heading path so the embedding sees the topic, not just the body prose.
9. Record `char_start` and `char_end` offsets so a citation can later highlight the exact span.
10. Re-chunk the whole corpus after changing the splitter; mixed chunkers produce incomparable retrievals.

11. Emit chunks in source order and keep a `prev_id`/`next_id` link so a multi-section answer can pull a neighbour.

## Pitfalls

- Splitting on a blanket 512-token window and calling the lost context "acceptable", then blaming the retriever.
- Dropping tables and lists because a naive text extractor ignores them — the numbers are usually the answer.
- Splitting a single FAQ entry into question and answer chunks, so neither retrieves the pair.
- Losing the document title because the parser starts at the first `<p>`, leaving orphan chunks with no provenance.
- Chunking a 200-page PDF by bytes and shipping page 1's heading into page 40's chunk.

- Applying an HTML stripper that silently drops `<pre>` and `<table>` and then wondering why code answers score zero.
- Emitting a chunk for every heading even when the section is empty, filling the index with titles that match everything.

## Verification

    python3 chunk.py --in docs/ --out chunks.jsonl
    jq -r '.text' chunks.jsonl | awk '{ if ($0 ~ /^[a-z]/) print NR": starts lowercase" }'
    # passes when no chunk starts mid-sentence and every chunk carries h1/h2 metadata

Report to the user: chunk count, mean and max tokens per chunk, and the number of chunks that failed the structure check.
