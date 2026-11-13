---
name: chunking-strategy
domain: software-engineering/chunking-strategy
trigger: "Splitting documents for retrieval and choosing the boundaries."
anti_trigger: "Not for prompt construction, and not for database partitioning."
scope: "Boundaries, overlap, and the size that matches the question being asked."
status: seedling
---

# Chunking strategy

## Standard

A chunk is the unit that gets embedded and retrieved, so its boundaries decide what the system can find. Split at a fixed character count and a definition can be cut from the term it defines; split at a heading and a short section becomes a chunk too small to carry meaning. The right boundary follows the document's own structure and the size of the question the system is expected to answer.

Chunk size is a trade-off with two directions. Small chunks retrieve precisely but lose surrounding context, so the retrieved passage may answer a fragment of the question; large chunks carry context but dilute the embedding, so a passage about one topic can be retrieved for a query about another. Overlap between adjacent chunks softens the boundary but multiplies the index and can produce near-duplicate results.

Primary sources: <https://nlp.stanford.edu/IR-book/> and <https://www.nist.gov/>.

## Decision rules

- Record the boundary rule: structural (headings, sections), semantic, or fixed size.
- Record the chunk size in tokens and the overlap, with the reason for each.
- Record whether metadata is attached to each chunk, since filtering depends on it.
- Record the treatment of tables, code, and lists, which do not split like prose.
- Record the smallest and largest chunk produced, since a size distribution with outliers is a defect.
- Record how a chunk's source document is tracked, so a result can cite its origin.

## Procedure

1. Inspect the document structure and record its natural boundaries.
2. Choose a boundary rule and a target size, recording the reason.
3. Attach metadata: source, section, and any filterable field.
4. Handle tables, code, and lists with a rule of their own.
5. Measure the resulting size distribution and inspect outliers.
6. Write the chunking specification with its parameters.

## Anti-patterns

- Fixed-size splitting that cuts sentences and definitions.
- Overlap so large that the index doubles for little gain.
- Chunks without source metadata, which makes citation impossible.
- Splitting tables row by row and losing the header.
- Choosing a size without inspecting what the chunks actually contain.

## Done checklist

- [ ] Boundary rule recorded.
- [ ] Size and overlap recorded with reasons.
- [ ] Metadata recorded per chunk.
- [ ] Table and code handling recorded.
- [ ] Size distribution measured.
- [ ] Source tracking recorded.

## Sources

- Information retrieval foundations: <https://nlp.stanford.edu/IR-book/>
- Text retrieval evaluation guidance: <https://www.nist.gov/>
- Unicode text segmentation: <https://unicode.org/reports/tr29/>
