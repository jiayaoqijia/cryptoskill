---
name: collect-subagent-results-into-a-report
description: Use when a fan-out has finished and many child outputs must become one parent report. Aggregates by iterating the roster so totals are exact and per-row provenance survives.
---

# Collect Subagent Results into a Report

The parent's report is a reduction over children, and the reduction must be mechanical. Iterate the roster in code, never assemble the summary from what you remember seeing.

## Procedure

1. Load the roster from `notes/roster.json` and treat it as the authoritative list of expected results.
2. For every roster entry, append the child's verified artifact to `out/report/rows.jsonl`, in roster order.
3. Assert coverage before summarising: `jq length notes/roster.json` equals the row count; a shortfall is a missing child, not an empty one.
4. Aggregate with code: `jq -s 'group_by(.area) | map({area:.[0].area, n:length})' out/report/rows.jsonl`.
5. Include only values you verified yourself (per `notes/metrics.tsv`), not the child's raw claims.
6. State totals as counts you can reproduce, and attach the command behind each: "20/20 valid (validate.py)".
7. Preserve provenance per row as `{slug, child_id, artifact_path, verdict}` so any line traces to its child.
8. List failures explicitly with their blocking reason; do not bury them under the success summary.
9. Keep the report in a fixed order the requester asked for; if none was asked, use roster order and say so.
10. Re-read the final report against the roster once, as a last check, before delivering it.

## Pitfalls

- Writing the summary from memory of the children's messages instead of iterating the roster file.
- Reporting the children's claimed totals rather than recomputed ones, propagating inflated numbers.
- Dropping a failed or missing child so the report reads cleaner than reality.
- Sorting or grouping by eye and miscounting, when `jq` or `sort | uniq -c` gives the exact figure.
- Losing provenance, so a wrong row in the report cannot be traced back to the child that produced it.

## Verification

```bash
jq length notes/roster.json; wc -l < out/report/rows.jsonl
# passes when the two numbers match and every failure has an explicit reason line
```

Report to the user: the roster size, the reproduced aggregate, and any child that failed with its reason.
