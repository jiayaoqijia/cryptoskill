---
name: modeling-record
domain: software-engineering/modeling-record
trigger: "Writing down the model's grain, change policy, and metric ownership."
anti_trigger: "Not for recommending a store, and not for a data dictionary dump."
scope: "The written record: grain, dimensions, change policy, and metric ownership."
status: seedling
---

# Modeling record

## Standard

The modeling record is the design's own documentation: the grain sentence of every fact, the change policy per dimension attribute, the derivation per aggregate and metric, and the owner of each definition. It exists because analytical models outlive their builders, and the only alternative to a written record is archaeology through pipelines at a moment when a number is disputed.

Its most valuable section is the divergences: the attributes where two facts keep different definitions, the metrics that share a name and differ deliberately, the aggregates that serve overlapping-but-different grains. A record that documents these reads as a set of conscious decisions; a record without them is a claim that no divergence exists, which is never true.

Primary sources: <https://www.kimballgroup.com/> and <https://osf.io/prereg/>.

## Decision rules

- The record holds the grain sentence of every fact.
- Every dimension attribute carries its change policy and the reason.
- Every metric carries its definition, owner, and version history.
- Every aggregate carries its derivation and refresh window.
- Divergences are documented as decisions, with the reason for each.
- The record is updated with every modeling change, with dates.

## Procedure

1. Record each fact's grain sentence.
2. Record each attribute's change policy.
3. Record each metric's definition, owner, and version.
4. Record each aggregate's derivation and refresh.
5. Write the divergences with their reasons.
6. Date every amendment, and never silently edit.

## Anti-patterns

- A record of table shapes with no grains or policies.
- Divergences absent, implying a consistency that was never checked.
- Definitions edited without dates, so no one can say when the number changed.
- An owner column filled with a team name, so no one answers.
- A record written once and never updated as the model grows.

## Done checklist

- [ ] Grain sentences recorded.
- [ ] Change policies recorded with reasons.
- [ ] Metrics, owners, and versions recorded.
- [ ] Aggregate derivations and refreshes recorded.
- [ ] Divergences written as decisions.
- [ ] Amendments dated.

The record earns its keep at the moment a number is challenged, which is rarely a calm moment: a reviewer who can open one file and find the grain, the change policy, and the definition version settles the dispute in minutes, while the same dispute without the record is a half-day of pipeline archaeology and often ends in a re-run of everything.

## Sources

- Dimensional modeling documentation: <https://www.kimballgroup.com/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Data modeling references: <https://clickhouse.com/docs/>
