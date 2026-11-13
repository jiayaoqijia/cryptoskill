---
name: facets-and-aggregations
domain: software-engineering/facets-and-aggregations
trigger: "Counting the result set by category without scanning the corpus."
anti_trigger: "Not for scoring, and not for the index structure itself."
scope: "Structured counts without corpus scans, and doc values as the design."
status: seedling
---

# Facets and aggregations

## Standard

A facet answers "within these results, how many are of each category" — and the naive implementation, iterating every matching document at query time, dies the day the corpus grows. The engineered answer is columnar: doc values store each document's field value in a column-oriented structure built at index time, so aggregation over a result set reads ordered values rather than reconstructing documents. That structure is what makes facet counts tractable, and deciding which fields carry it is a design decision with a memory cost.

The deeper design split is filter-then-count versus count-then-filter. A user clicks one brand facet; the counts shown for the remaining facets must reflect that choice — counts computed inside the filtered set — or the user sees options that lead nowhere. Facet state is therefore part of the query, and each visible facet is computed against the filtered result set except for itself, so all items of a selection remain visible rather than vanishing on their own click.

Primary sources: <https://elastic.co/guide/en/elasticsearch/reference/current/analysis.html> and <https://lucene.apache.org/core/corenews.html>.

## Decision rules

- Every aggregatable field carries doc values or an equivalent columnar structure; the decision is recorded per field.
- Filter-then-count is the default: facets are computed inside the active filter set, with the facet's own filter excluded from its count.
- Facet cardinality is budgeted: a category field with a million distinct values is not a facet; high-cardinality fields get limited or a different interaction.
- Facet latency is measured on the largest realistic filtered set, not on the whole corpus.
- Facet counts are approximate where the engine says so, and the user-facing accuracy is stated.
- Facet definitions live in the mapping record next to the analyzer decisions.

## Procedure

1. Choose facet fields by product need and measured cardinality.
2. Enable doc values on those fields at mapping time; record the memory delta.
3. Assemble the test: the largest filter set users can construct, with every facet visible.
4. Measure counts and latencies; record budgets.
5. Verify the filter-then-count behaviour matches what the UI displays.
6. Store facet definitions and their costs in the search record.

## Anti-patterns

- Aggregating a field with no doc values, falling back to a per-query scan.
- Facet counts computed outside the active filters, offering zero-result options.
- A high-cardinality user-id field sitting in the facet bar.
- Unmeasured facet latency until a customer with a large catalogue complains.
- Approximate counts presented as exact because nobody read the engine's documentation.

## Done checklist

- [ ] Facet fields chosen with cardinality measured.
- [ ] Doc values enabled and memory delta recorded.
- [ ] Filter-then-count verified in the UI.
- [ ] Worst-case facet latency measured.
- [ ] Approximation disclosed where used.
- [ ] Definitions in the mapping record.

## Sources

- Elasticsearch analysis and structures: <https://elastic.co/guide/en/elasticsearch/reference/current/analysis.html>
- Lucene project: <https://lucene.apache.org/core/corenews.html>
- OpenSearch analyzers and structures: <https://opensearch.org/docs/latest/analyzers/>
