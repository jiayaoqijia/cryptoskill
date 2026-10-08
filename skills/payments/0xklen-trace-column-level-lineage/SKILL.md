---
name: trace-column-level-lineage
description: Use when you need to know which source columns and jobs produced a downstream value. Builds column-level lineage from parsed transforms so impact analysis and debugging are answerable.
---

# Trace Column-Level Lineage

Table-level lineage (a dashboard reads orders) cannot answer which metrics break when `orders.currency` is wrong. Column-level lineage maps each output column back to its inputs and the job that wrote it.

## Procedure

1. Start from the DAG you already have: orchestration metadata (`dbt manifest.json`, an Airflow DAG, a Dagster asset graph) gives job-to-job edges.
2. Parse each model's SQL for column edges with `sqlglot`:
   `sqlglot.lineage.lineage("amount", expression, schema=schema)` and `sqlglot.parse_one(sql).find_all(exp.Column)`.
   For dbt, `dbt docs generate` writes `manifest.json` with `parent_map`/`child_map` and compiled SQL to parse.
3. For non-SQL transforms, annotate the code with the columns read and written (a decorator or a manifest). A transform you cannot parse must declare its lineage.
4. Store edges as tuples: `(source_table, source_col, target_table, target_col, job)`.
5. Query in both directions: upstream of a column (what feeds it) and downstream (what it feeds).
6. Use it operationally: before changing a source column, list downstream columns and their owning jobs; during an incident, show which job last wrote a bad value.
7. Refresh lineage on every deploy so it does not rot. An unmaintained lineage graph is worse than none because it is trusted.
8. Store the edge graph in a queryable store (SQLite/Postgres), not a static image, so it can be joined against alerts and ownership.
9. Resolve ambiguity by qualifying columns with their table alias during parsing, so a stored edge names the right source.
10. Fail the build if a model cannot be parsed for lineage, so a wildcard or an odd syntax is flagged rather than silently unlinked.

## Pitfalls

- Wildcard `SELECT *` hides edges; expand columns at parse time or the graph is empty for that model.
- Renaming a column in a transform without updating lineage silently detaches the edge.
- Views and CTEs that alias columns break naive name matching; parse, do not regex.
- Lineage derived once and never refreshed points at deleted tables.
- Columns with the same name across a join are ambiguous and need qualified resolution.
- Treating lineage as documentation only, with no queryable store, means it is never used during an incident.
- Parsing only the final model misses intermediate CTEs that rename a column on the way through.
- An unparseable transform that is skipped makes the graph look complete when it has a hole.

## Verification

```sh
python -c "import sqlglot; print(sqlglot.lineage.lineage('revenue', sql, schema=s))"
sqlite3 lineage.db "SELECT * FROM edges WHERE target_col='revenue'"
```

A known source column resolves to the expected target through named jobs; an intentionally broken column returns no path, proving detection works. Report the edge count and the downstream columns of the changed source.