---
name: query-record
domain: software-engineering/query-record
trigger: "Writing the record of an index or query decision."
anti_trigger: "Not for recommending a database, and not for schema migration planning."
scope: "The written record: the query, its plan, the indexes, and the cost model."
status: seedling
---

# Query record

## Standard

The record states the query, the plan it produced, the indexes that plan used, and the write cost those indexes impose. It exists so that a later slowdown can be diagnosed against a known baseline rather than reconstructed, and so that an index added for one query is visible as a cost to every other write on the table.

Its second function is to capture the data volume the plan was measured at. A plan that is optimal at ten thousand rows can be wrong at ten million, and a record without a row count cannot distinguish a planner regression from a table that grew past the threshold where the access path changes.

Primary sources: <https://www.postgresql.org/docs/> and <https://osf.io/prereg/>.

## Decision rules

- The record states the query text and its parameter values.
- The plan is recorded with estimates and actual rows.
- The table's row count and the index sizes are recorded at the time of measurement.
- The indexes present on the table are listed with their write cost.
- Review triggers are dated: row count crossing a threshold, plan change, new slow-query report.
- The record is append-only; plan changes are dated amendments.

## Procedure

1. Record the query and its parameters.
2. Record the plan with estimates and actuals.
3. Record row counts and index sizes.
4. List the table's indexes with their maintenance cost.
5. Set the review triggers.
6. Amend when the measurement is repeated.

## Anti-patterns

- Recording the plan without the data volume.
- Omitting the parameter values that produced the plan.
- Listing the indexes used without the ones that only cost.
- No trigger, so the plan is never re-measured.
- Editing the record instead of amending it.

## Done checklist

- [ ] Query and parameters recorded.
- [ ] Plan with estimates and actuals recorded.
- [ ] Row counts and index sizes recorded.
- [ ] Index list with costs recorded.
- [ ] Triggers dated.
- [ ] Amendments dated.

The record should also note the product and version that produced the plan, because optimizer behaviour changes between releases and a comparison across versions is otherwise uninterpretable. A plan recorded without its version is an observation, not a baseline.


The record's final field is the decision it supported: which index was added, removed, or left alone, and what measurement justified it. Without that, the file becomes a log of plans rather than a history of choices.

## Sources

- Query planner documentation: <https://www.postgresql.org/docs/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Index design guidance: <https://use-the-index-luke.com/>
