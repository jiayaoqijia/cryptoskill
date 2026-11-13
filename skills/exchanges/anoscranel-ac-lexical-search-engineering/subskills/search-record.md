---
name: search-record
domain: software-engineering/search-record
trigger: "Recording the search system's decisions so tuning stays explainable."
anti_trigger: "Not for the index itself, and not for query logs in general."
scope: "The record: analyzers, schemas, query rewrites, and tuned mappings."
status: seedling
---

# Search record

## Standard

The search record gathers every decision that a future debugging session will need: the analyzer per field, the structural decisions (positions, doc values, index-vs-store), the query-construction semantics table, the scoring parameters with their tuning baselines, the fuzziness budgets, the facet definitions with cardinalities, the autocomplete structure and latency budget, and the frozen query sets used for evaluation. Search behaviour is cumulative — an analyzer chosen in month one shapes every relevance complaint in month twelve — and the record is the only thing that makes the cumulative system inspectable.

The record's second function is change safety. Analyzer changes require reindexing; scoring changes alter every result's ordering; structure changes have memory costs. Each of these is a versioned event in the record, tied to the mapping version that shipped it and to the evaluation numbers that justified it. A search system without this history degrades into folklore: the tuning is real but unexplainable, and the next engineer either re-derives everything or reverts something that was load-bearing.

Primary sources: <https://elastic.co/guide/en/elasticsearch/reference/current/analysis.html> and <https://nlp.stanford.edu/IR-book/>.

## Decision rules

- The record contains the analyzer table, structure decisions, query semantics, scoring parameters with baselines, fuzziness budgets, facet definitions, and the autocomplete contract.
- Every mapping version is listed with the changes it carried and the reason for each.
- Frozen query sets are stored with their versions; evaluation runs reference the set they used.
- Tuning entries carry their one-knob-at-a-time log with the before and after numbers.
- Engine upgrades are recorded as events with a re-tuning pass, not as silent behaviour continuations.
- The record lives beside the mapping definitions and version-histories with them.

## Procedure

1. Create the record at design time from each leaf's decision points.
2. Bind the mapping version history to the record's entries.
3. Store the frozen query sets and their versions.
4. Log every tuning change with its single knob, numbers, and rationale.
5. Record engine upgrades with their re-tuning outcome.
6. Review the record at each search-quality retrospective; drift is a finding.

## Anti-patterns

- Mapping changes shipped without a record entry, so the analyzer history becomes untraceable.
- Tuning parameters in the record without the baseline they beat.
- Query semantics documented in a wiki that no parser change ever updated.
- Upgrades assumed score-neutral, discovered otherwise in a user complaint.
- The record written once at launch and never amended, quietly outpaced by the system.

## Done checklist

- [ ] All decision points recorded per leaf.
- [ ] Mapping version history bound to the record.
- [ ] Frozen query sets stored with versions.
- [ ] Tuning log with baselines and single-knob entries.
- [ ] Upgrades recorded with re-tuning outcomes.
- [ ] Retrospective reviews the record for drift.

## Sources

- Elasticsearch analysis reference: <https://elastic.co/guide/en/elasticsearch/reference/current/analysis.html>
- Introduction to Information Retrieval: <https://nlp.stanford.edu/IR-book/>
- Lucene project: <https://lucene.apache.org/core/corenews.html>
