---
name: analysis-chain
domain: software-engineering/analysis-chain
trigger: "Deciding what counts as a term before anything is indexed."
anti_trigger: "Not for scoring, and not for the index structure."
scope: "Tokenizers, normalization, stemming, and the analyzer per field."
status: seedling
---

# Analysis chain

## Standard

Before anything can be searched, text passes through an analysis chain: tokenization splits it into units, normalization folds case and strips punctuation, and optionally stemming or lemmatization reduces variants to one term. That chain runs once at index time and again at query time, and the single rule that governs everything is that both sides must agree: a query analyzed differently from its documents produces terms that meet nothing, and the failure is silent because the system returns empty rather than error.

The chain is a per-field decision. Titles deserve different treatment from bodies — a title's tokens are few and heavily weighted, so aggressive stemming wastes signal; a body benefits from light stemming; identifiers and SKUs often want no analysis at all, matched exactly. Recording the analyzer per field is what makes the system's behaviour explainable later, when someone asks why a search for one form of a word missed another.

Primary sources: <https://elastic.co/guide/en/elasticsearch/reference/current/analysis.html> and <https://opensearch.org/docs/latest/analyzers/>.

## Decision rules

- Name the analyzer per field, in the mapping record; no field is indexed on a silent default.
- Queries pass through the analyzer of the field they target, or a search_analyzer is stated explicitly when it differs.
- Stemming choice is recorded with its consequence: aggressive stems collapse variants aggressively and merge distinct meanings with them.
- Identifiers, codes, and tags are indexed with the no-op analyzer and matched exactly.
- Reindexing is the price of changing an analyzer; the analyzer is part of the schema's version history.
- A few representative texts are analyzed by hand and their term output inspected before the mapping ships.

## Procedure

1. List the fields and their text classes: titles, bodies, names, identifiers.
2. Choose an analyzer per field; write the reason for each.
3. Run representative documents and queries through each analyzer; list the resulting terms.
4. Verify query analysis matches index analysis for every searchable field.
5. Record the mapping version with its analyzer decisions.
6. Plan the reindex path for any future analyzer change at the start, not when the first one is needed.

## Anti-patterns

- One global analyzer for every field because the default was invisible.
- Stemming that produces unrecognizable terms nobody can debug at query time.
- Exact-match fields run through the standard analyzer, so AB1234 becomes two lowercase tokens.
- Changing an analyzer and expecting the old index to answer with the new behaviour.
- Never once printing the analyzed form of a real query.

## Done checklist

- [ ] Analyzer per field recorded with reason.
- [ ] Query and index analysis verified to agree.
- [ ] Representative terms inspected in each class.
- [ ] No-op analysis on exact-match fields.
- [ ] Mapping versioned with the analyzer decisions.
- [ ] Reindex path planned.

## Sources

- Elasticsearch analysis reference: <https://elastic.co/guide/en/elasticsearch/reference/current/analysis.html>
- OpenSearch analyzers: <https://opensearch.org/docs/latest/analyzers/>
- Lucene project: <https://lucene.apache.org/core/corenews.html>
