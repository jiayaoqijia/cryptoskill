---
name: inverted-index
domain: software-engineering/inverted-index
trigger: "Understanding the structure that answers every term-based query."
anti_trigger: "Not for analysis choices, and not for database page layouts."
scope: "The structure: postings, skipping, compression, and what it costs."
status: seedling
---

# Inverted index

## Standard

The inverted index turns the question around: instead of asking each document which terms it contains, it lists, for every term, the documents that contain it. Each term points to a postings list of document identifiers, ordered, compressed, and — in the parts that need them — annotated with positions or offsets for phrase work. Query execution is then a set operation on those lists: intersect for AND, union for OR, skip through the ordered lists rather than scanning them.

The economics explain every design trade-off. The index costs disk and memory proportional to the corpus's unique terms and postings; compression keeps it tolerable because postings are sorted numbers. Query speed depends on touching few short lists: AND queries run fastest when the rarest term is evaluated first, because its postings list prunes everything downstream. Every feature added to the index — positions for phrases, norms for scoring, doc values for facets — is a separate cost decision, and knowing which structure serves which feature is the difference between designing and accumulating.

Primary sources: <https://lucene.apache.org/core/corenews.html> and <https://nlp.stanford.edu/IR-book/>.

## Decision rules

- Record what structure backs each feature: positions for phrase queries, norms for field-length scoring, doc values for aggregations.
- The rarest-term-first evaluation of AND queries is left to the engine; your job is not to defeat it with a prefilter that scans.
- Index bloat is measured: postings growth per field is a fact, not an accident.
- The terms vocabulary is inspected periodically; analyzer mistakes surface there as garbage terms.
- Field-level index decisions are explicit: not every field is both searchable and aggregatable by default.
- The physical size and the query-time memory cost are both recorded before a new field's structure is added.

## Procedure

1. State the query types the system must answer; derive the structures they need.
2. Choose per field: indexed or stored or both; positions or not; doc values or not.
3. Measure index size before and after a structural change; record the delta.
4. Inspect the term vocabulary for analyzer artifacts.
5. Exercise the slowest realistic query shape; confirm it walks lists rather than scanning.
6. Record the structure decisions in the mapping version.

## Anti-patterns

- Indexing everything with every structure on, then wondering why the index is five times the corpus.
- Phrase search on a field with no positions, failing over to full scans.
- Facets computed by scanning the corpus at query time because doc values were never added.
- A terms vocabulary nobody has looked at, full of tokenizer debris.
- Adding structures in production without measuring what they cost.

## Done checklist

- [ ] Query types stated and structures derived.
- [ ] Per-field structure decisions recorded.
- [ ] Size deltas measured per structural change.
- [ ] Term vocabulary inspected.
- [ ] Slowest query shape exercised.
- [ ] Mapping version updated.

## Sources

- Lucene project: <https://lucene.apache.org/core/corenews.html>
- Introduction to Information Retrieval: <https://nlp.stanford.edu/IR-book/>
- Elasticsearch analysis and structure: <https://elastic.co/guide/en/elasticsearch/reference/current/analysis.html>
