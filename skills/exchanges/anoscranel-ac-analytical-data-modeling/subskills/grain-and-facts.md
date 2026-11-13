---
name: grain-and-facts
domain: software-engineering/grain-and-facts
trigger: "Fixing what one row of a fact table means before anything else."
anti_trigger: "Not for operational table design, and not for recommending a store."
scope: "The one-row-per-what decision, and what belongs in a fact."
status: seedling
---

# Grain and facts

## Standard

The grain is the precise meaning of one row in a fact table: one row per order line, per transaction, per bank account at the close of each day, per device event. It is the first decision and the one that constrains everything after it, because an aggregation is only trustworthy over a stated grain — sum over "one row per order line" is revenue by product, while the same sum over "one row per order" is meaningless.

A fact row holds the keys to its dimensions and the measures. The measures come in three kinds: additive quantities that sum across every dimension, semi-additive balances that sum across everything but time, and non-additive facts like rates and ratios that must be aggregated by re-computing from components rather than by summing. Marking which kind each measure is, at modeling time, is what stops a dashboard from summing a balance across quarters.

Primary sources: <https://www.kimballgroup.com/> and <https://martinfowler.com/>.

## Decision rules

- State the grain as a sentence a non-specialist can repeat: "one row per X per Y".
- Record the additive class of every measure: additive, semi-additive, or non-additive.
- Record the degenerate dimensions kept as keys, such as an order number.
- Reject measures that belong at a different grain; route them to their own fact.
- Record the fact's source and the transformation applied, in one line.
- Record the retention and whether the grain is period-destructive when rebuilding.

## Procedure

1. Propose the grain sentence and test it against the questions to be answered.
2. List the measures and classify each as additive, semi-additive, or non-additive.
3. List the dimensions the fact references.
4. Move any measure at a different grain to its own fact table.
5. Record the lineage note for the fact.
6. Review the grain against every expected report before building.

## Anti-patterns

- A fact whose grain differs by source system, merged silently.
- Summing balances across time because the column is numeric.
- Rates averaged by summing and dividing by rows.
- A grain sentence nobody has written down, rediscovered during a dispute about a number.
- Mixed-grain facts patched at query time with a WHERE clause.

## Done checklist

- [ ] Grain stated as a sentence.
- [ ] Measures classified by additive behaviour.
- [ ] Dimension keys listed.
- [ ] Off-grain measures moved out.
- [ ] Lineage note recorded.
- [ ] Grain tested against every report.

## Sources

- Dimensional modeling techniques: <https://www.kimballgroup.com/>
- Analytical modeling patterns: <https://martinfowler.com/>
- Data warehousing references: <https://clickhouse.com/docs/>
