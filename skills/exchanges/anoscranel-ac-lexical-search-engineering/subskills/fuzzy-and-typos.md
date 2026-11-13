---
name: fuzzy-and-typos
domain: software-engineering/fuzzy-and-typos
trigger: "Matching what the user almost typed without paying for it everywhere."
anti_trigger: "Not for analyzer design, and not for scoring."
scope: "Edit distance matching, its indexing cost, and cheaper alternatives."
status: seedling
---

# Fuzzy and typos

## Standard

Fuzzy matching forgives typos by expanding a query term to every term within an edit-distance budget. The cost curve is brutal and worth knowing rather than discovering: at distance one the expansion is usually tolerable; at distance two, common short terms explode into thousands of candidates, and each candidate walks its postings list; at distance three on short alphabets, the query is effectively a scan of the term dictionary. The user experiences this as search that is simultaneously more generous and dramatically slower.

Because the cost is real, the engineering answer is to prefer cheaper approximations first: n-gram structures indexed at build time convert runtime expansion into a lookup; normalization fixes systematic errors like case, accent folding, digits and punctuation; and reserving true edit distance for the fields where typos are common — names and identifiers typed by humans — keeps the cost local. The distance itself is a budget the record states per field, because forgiving more and matching worse sit on one dial.

Primary sources: <https://elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html> and <https://nlp.stanford.edu/IR-book/>.

## Decision rules

- Fuzziness is enabled per field, not system-wide; typo-prone fields earn it.
- The edit-distance budget is stated per field, with two on short terms recognized as expensive.
- Normalization is layered before fuzziness: case, accents, punctuation — the cheap matches are never left to the expensive mechanism.
- Autocomplete contexts do not run fuzzy expansion on every keystroke; the prefix structure is the mechanism there.
- Fuzzy candidates are visually marked as such in results when the match differs from the query, so debugging needs no guessing.
- Per-field fuzziness decisions and their rationale live in the search record.

## Procedure

1. Measure the typed-error patterns first: which fields actually receive typos.
2. Apply normalization layers before enabling fuzziness anywhere.
3. Enable fuzziness on the typo-prone fields only, with a stated distance budget.
4. Test the latency of representative fuzzy queries against the budget.
5. Mark fuzzy-matched results in the response payload for debugging.
6. Record per-field decisions with measured latencies.

## Anti-patterns

- Fuzziness enabled globally because "users make typos" — the cost lands on every field including exact-match ones.
- Distance two on three-letter terms without measuring anything.
- Fuzzy queries inside type-ahead, re-expanding on every keystroke.
- Normalization absent, so the fallback mechanism fixes upper-case problems at premium cost.
- Fuzziness compensating for an analyzer mismatch; the fix belongs in the chain, not in distance.

## Done checklist

- [ ] Typo-prone fields identified by measurement.
- [ ] Normalization layered before fuzziness.
- [ ] Per-field distance budgets stated.
- [ ] Latency tested against the budget.
- [ ] Fuzzy matches marked in results.
- [ ] Decisions recorded with latencies.

## Sources

- Elasticsearch query DSL: <https://elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>
- Introduction to Information Retrieval: <https://nlp.stanford.edu/IR-book/>
- Lucene project: <https://lucene.apache.org/core/corenews.html>
