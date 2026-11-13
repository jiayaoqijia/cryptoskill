---
name: query-construction
domain: software-engineering/query-construction
trigger: "Turning what the user typed into clauses the engine can evaluate."
anti_trigger: "Not for analyzer design, and not for scoring arithmetic."
scope: "Boolean clauses, phrase and span queries, and how analysis rewrites queries."
status: seedling
---

# Query construction

## Standard

A user's input becomes a tree of clauses: terms into match queries, quoted strings into phrase queries, operators into boolean structure. The construction step is where intention is encoded, and the standing failure is doing it twice — an application building boolean logic out of the user's operators, then handing the result to an engine whose query parser builds boolean logic again. The output is a query that means something other than what either layer intended, and the user experiences it as search that ignores half their words.

The discipline is one layer of construction. Either the application assembles structured clauses deliberately and passes them unambiguous — one place where AND, OR, filters, and phrase boundaries are decided — or it passes the user's string to a single declared parser and accepts its semantics. The query dialect's semantics — operator precedence, default operator, how an empty clause fails — are recorded once, so the person debugging a result set can read the tree that was actually built.

Primary sources: <https://elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html> and <https://lucene.apache.org/core/corenews.html>.

## Decision rules

- One layer constructs the boolean structure; double parsing is a defect to remove, not a feature.
- The semantics of precedence and the default operator are written down with the examples that exercise them.
- Quoted phrases become phrase clauses; filters (exact values, ranges, categories) become filter clauses excluded from scoring.
- The constructed tree is loggable at debug time; a result nobody can explain begins by reading the tree.
- Field-level search is explicit: which fields a bare query targets is a recorded decision.
- Failing gracefully on malformed input means a stated fallback query, never silent term dropping.

## Procedure

1. Define the input grammar: terms, quoted phrases, filters, operators you will honour.
2. Choose the construction layer; write the mapping from grammar to clause tree.
3. Record the semantics table: precedence, defaults, empty-input behaviour.
4. Implement filter versus scored clause separation.
5. Add a debug view of the final tree attached to a query id.
6. Test the semantics table's examples as fixtures, so a parser change that alters meaning fails a test.

## Anti-patterns

- Application-built boolean strings fed to a parser that also interprets operators.
- Every field searched by default; the scoring quietly becomes an average of noise.
- Malformed input silently truncated to the terms that parsed.
- Filters inside the scored clauses, forcing scoring over values that only ever needed matching.
- No debug tree, so relevance debugging happens by speculation.

## Done checklist

- [ ] Input grammar defined.
- [ ] One construction layer, named.
- [ ] Semantics table written and tested.
- [ ] Filters separated from scored clauses.
- [ ] Debug tree available per query.
- [ ] Fallback behaviour stated for malformed input.

## Sources

- Elasticsearch query DSL: <https://elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>
- Lucene project: <https://lucene.apache.org/core/corenews.html>
- Introduction to Information Retrieval: <https://nlp.stanford.edu/IR-book/>
