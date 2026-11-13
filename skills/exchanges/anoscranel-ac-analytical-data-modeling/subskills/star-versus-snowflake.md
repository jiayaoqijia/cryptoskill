---
name: star-versus-snowflake
domain: software-engineering/star-versus-snowflake
trigger: "Choosing how normalised the descriptive context should be."
anti_trigger: "Not for normalisation theory in general, and not for a store choice."
scope: "Join depth versus update cost, and when normalising dimensions is worth it."
status: seedling
---

# Star versus snowflake

## Standard

A star puts every descriptive attribute in one flat dimension table: the fact joins once, and every attribute of context is one join away. A snowflake normalises those attributes into their own tables: the region becomes a table, the brand becomes a table, and queries traverse two or three joins to reach the label they want. The star buys query simplicity and optimizer-friendliness at the cost of a wide table that repeats values; the snowflake buys storage and single-point updates at the cost of join depth and more complex query authoring.

The default for analytical workloads is the star, because the workload is joins-plus-filters-plus-aggregation and every added join is a place for an optimizer mistake. Snowflaking earns its place in specific cases: a shared reference list maintained by another team, a genuinely enormous dimension where the storage saving is real, or a hierarchy that changes too often to rewrite a wide table for each change.

Primary sources: <https://www.kimballgroup.com/> and <https://martinfowler.com/>.

## Decision rules

- Record which shape each dimension uses, and the reason.
- Reserve snowflaking for attributes maintained elsewhere or changing independently.
- Record the join depth for the common queries; two is usually the ceiling.
- Record any bridge tables for many-to-many contexts, with their grain.
- Record the update story for repeated values in a star: a full rewrite or an accepted delay.
- Check the common reports against the shape by writing them before building.

## Procedure

1. List each dimension's attributes and their change frequency.
2. Choose flat or snowflaked per dimension, with reasons.
3. Write the five most common reports as queries against the chosen shape.
4. Identify many-to-many contexts and design their bridges.
5. Record the update path for flat tables.
6. Adjust the shape where the query writing found friction.

## Anti-patterns

- Snowflaking for storage alone on a dimension of modest size.
- A star so wide that its own maintainer cannot name its columns.
- Bridges without a stated grain, producing fan-out in counts.
- Join depth of four or five accepted silently because the diagram looked tidy.
- Different shapes for the same conformed dimension in two subject areas.

## Done checklist

- [ ] Shape chosen per dimension with reasons.
- [ ] Common reports written against the shape.
- [ ] Bridges designed with grain.
- [ ] Update path for flat tables recorded.
- [ ] Join depth checked.
- [ ] Conformed shapes consistent across subject areas.

## Sources

- Dimensional modeling techniques: <https://www.kimballgroup.com/>
- Analytical patterns: <https://martinfowler.com/>
- Data warehousing references: <https://clickhouse.com/docs/>
