---
name: cost-record
domain: prompt-engineering/cost-record
trigger: "Writing the record of a cost-optimization decision and its outcome."
anti_trigger: "Not for the invoice, and not for recommending providers."
scope: "The written record: baselines, changes, and per-task dollars."
status: seedling
---

# Cost record

## Standard

The cost record states the baseline, the change, the measured effect, and the trade the change made. Its purpose is to keep savings honest: a technique that saved nothing, or that saved dollars by degrading outcomes, is recorded as what it is. Every optimization in this skill's leaves trades something — latency, quality risk, restructuring effort — and the record names the trade beside the number.

Its second purpose is durability of assumptions. Rates change, tiers change, models change; a saving measured against a dated baseline survives as evidence, while a saving asserted against an unrecorded one dissolves into folklore. The record carries the dated rate table, the benchmark task set, the before-and-after dollars per task, and the re-measure trigger for each optimization.

Primary sources: <https://osf.io/prereg/> and <https://docs.anthropic.com/en/docs/about-claude/pricing>.

## Decision rules

- Baseline recorded before any change: per-task dollars at dated rates, with a benchmark task set.
- One change at a time; the effect is attributed to the change that is measured.
- The trade is named beside the saving: latency, quality-risk, or effort.
- Quality checked at the same time as cost; a saving with degraded outcomes is a loss.
- Re-measure triggers recorded: rate changes, tier updates, prompt restructures.
- The record is append-only; new measurements are amendments with dates.

## Procedure

1. Record the baseline task set, rates, and dollars per task, dated.
2. Make one change; keep everything else fixed.
3. Measure dollars per task and outcome quality on the same benchmark set.
4. Record saving, trade, and quality delta together.
5. Set the re-measure trigger tied to the assumption the change rests on.
6. Amend, never overwrite, when later measurements arrive.

## Anti-patterns

- Recording savings without the baseline they were measured against.
- Many changes at once; the number is unattributable.
- Reporting dollars saved without the quality check beside it.
- Treating a one-month rate as permanent in the arithmetic.
- Updating the record in place so the history of claims disappears.

## Done checklist

- [ ] Baseline: task set, rates, dollars, dated.
- [ ] One change measured in isolation.
- [ ] Saving, trade, and quality delta recorded together.
- [ ] Re-measure trigger tied to the assumption.
- [ ] New measurements as dated amendments.

The record also earns its keep when a saving is challenged: the dated baseline, the benchmark set, and the quality check beside every number mean the dispute is settled by re-running the measurement, not by argument. An optimization without a record is a belief; with one, it is a finding that survives staff changes and provider rate updates.

## Sources

- Pre-registration practice for baselines: <https://osf.io/prereg/>
- Dated rate basis: <https://docs.anthropic.com/en/docs/about-claude/pricing>
- Batch trade-off context: <https://docs.anthropic.com/en/docs/build-with-claude/batch-processing>
