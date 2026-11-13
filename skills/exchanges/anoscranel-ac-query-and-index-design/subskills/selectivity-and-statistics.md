---
name: selectivity-and-statistics
domain: software-engineering/selectivity-and-statistics
trigger: "Diagnosing a plan that chose the wrong path because of bad statistics."
anti_trigger: "Not for tuning statistics parameters, and not for schema design."
scope: "Cardinality, histograms, staleness, and the planner's mistakes."
status: seedling
---

# Selectivity and statistics

## Standard

The planner estimates how many rows a predicate will match, and it estimates from statistics the database collects about the data: distinct value counts, histograms of distribution, and correlation between columns. When those statistics are stale, or when the predicate's shape hides the data, the estimate is wrong and the chosen path is wrong with it.

Three failure patterns recur. A column with a skewed distribution, where one value covers most rows and the rest are rare, defeats a simple distinct-count statistic unless a histogram captures the skew. A correlated pair of columns, where a predicate on both is far more selective than the product of the two individually, is underestimated unless the database knows the correlation. And a function applied to a column hides the column from the statistics entirely.

Primary sources: <https://www.postgresql.org/docs/> and <https://use-the-index-luke.com/>.

## Decision rules

- Record the estimated and actual rows at each node where they diverge.
- Record the column's distinct count and whether its distribution is skewed.
- Record whether the predicate wraps the column in a function or a cast.
- Record whether the columns are correlated and whether the database knows it.
- Record when statistics were last collected.
- Record the estimate error as a ratio, since an order of magnitude is the signal.

## Procedure

1. Capture the plan with estimates and actuals.
2. Compute the estimate-to-actual ratio per node.
3. Identify the node with the largest ratio.
4. Record the predicate shape at that node.
5. Check the statistics for the columns involved.
6. Write the diagnosis with the correction named.

## Anti-patterns

- Applying a function to an indexed column and expecting the index to be used.
- Assuming statistics are current after a bulk load.
- Treating a single bad plan as a systemic problem.
- Ignoring correlation between columns in a multi-column predicate.
- Correcting the query before confirming the estimate was the cause.

## Done checklist

- [ ] Estimates and actuals recorded.
- [ ] Error ratios computed.
- [ ] Worst node identified.
- [ ] Predicate shape recorded.
- [ ] Statistics checked.
- [ ] Diagnosis and correction recorded.

The correction to record is usually not a query rewrite but a change in what the database knows: extended statistics for correlated columns, an expression index for a function predicate, or a statistics target raised on a skewed column. Naming which of the three applies is what makes the diagnosis reusable when the same shape appears on another table.


## Sources

- Statistics and planner documentation: <https://www.postgresql.org/docs/>
- Index and selectivity guidance: <https://use-the-index-luke.com/>
- SQLite planner notes: <https://sqlite.org/optoverview.html>
