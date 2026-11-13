---
name: autocomplete-and-suggest
domain: software-engineering/autocomplete-and-suggest
trigger: "Building type-ahead that answers before the user finishes typing."
anti_trigger: "Not for general query construction, and not for fuzzy matching policy."
scope: "Prefix structures, completion suggesters, and type-ahead latency budgets."
status: seedling
---

# Autocomplete and suggest

## Standard

Type-ahead is a latency contract first and a matching problem second. The user types a character and expects suggestions within a perceptible instant; the budget is tens of milliseconds, and every design decision — prefix structures, edge n-grams, completion dictionaries — exists to serve that budget. The two common designs have different physics: prefix structures (finite-state transducers, trie-like dictionaries) match completions of what was typed with memory-efficiency and speed; edge n-grams index every prefix at build time, making the query a simple term lookup at the cost of a larger index.

The second axis is what is suggested. Completion of strings the corpus contains is the simplest contract; query suggestions from a query log personalize and predict but carry their own failure — the log's tail is spam and one-offs unless filtered, and suggestions trained on past queries lag vocabulary the corpus has since gained. Both are legitimate; the record states which the system offers, because the honesty of the feature depends on the user knowing whether the box completes their text or predicts their intent.

Primary sources: <https://elastic.co/guide/en/elasticsearch/reference/current/analysis.html> and <https://lucene.apache.org/core/corenews.html>.

## Decision rules

- The latency budget is stated in milliseconds and measured at the p99, on the production device class.
- The suggestion source is recorded: corpus completions, query-log suggestions, or a blend; the blend's precedence is written down.
- Edge n-gram prefixes and prefix-structure choices are recorded with their index-size deltas.
- Keystroke handling debounces at a stated interval; the request in flight when a new keystroke lands is cancelled, not raced.
- Query-log suggestions are filtered by a minimum frequency and a blacklist; the raw tail never reaches the box.
- Suggestion ranking is stable enough that a user can retype and see the same list; ranking jitter is a bug.

## Procedure

1. State the latency budget and the device class it must hold on.
2. Choose the structure: prefix dictionary or edge n-grams; measure the index delta.
3. Choose the suggestion source; if a blend, write the precedence rule.
4. Implement debounced, cancellable keystroke handling.
5. Filter query-log candidates by frequency threshold and blacklist.
6. Measure p99 latency on the worst input class and record it.

## Anti-patterns

- Suggestions racing each other as the user types, so the final list matches an earlier prefix.
- The raw query log unfiltered, offering one-off mistakes and typos as the most recent completions.
- A latency budget expressed as "feels fast" with no number.
- Autocomplete silently becoming search-with-fuzzy-expansion on every keystroke.
- Ranking that shuffles between two identical keystrokes.

## Done checklist

- [ ] Latency budget stated and measured at p99.
- [ ] Structure chosen with index delta recorded.
- [ ] Suggestion source and precedence recorded.
- [ ] Debounce and cancellation implemented.
- [ ] Query-log filtering in place.
- [ ] Ranking stability verified.

## Sources

- Elasticsearch analysis reference: <https://elastic.co/guide/en/elasticsearch/reference/current/analysis.html>
- Lucene project: <https://lucene.apache.org/core/corenews.html>
- OpenSearch analyzers: <https://opensearch.org/docs/latest/analyzers/>
