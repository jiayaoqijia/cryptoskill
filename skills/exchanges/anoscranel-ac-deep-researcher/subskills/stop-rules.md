---
name: stop-rules
domain: research-operations/stop-rules
trigger: "\"are we done yet\", \"should I keep researching\", \"when do I stop searching\", \"close the study\"."
anti_trigger: "The adversarial counter-search itself (subskills/adversarial-pass.md); writing the stop reason into the final report (subskills/write-report.md)."
scope: "Deciding a study is done against declared criteria, and always writing the stop reason into the record"
status: "seedling"
---

# Stop rules

## Standard

- A research task never stops silently. The record names which criterion
 fired, or why more research adds no value.
- Four stop criteria. Coverage: every planned
 sub-question carries an answered or explicitly blocked cell. Saturation:
 new queries return restatements of what is already covered, and the log
 shows it. Error budget: verification has settled every load-bearing claim
 or named its wall. Diminishing leverage: the next round would re-derive
 existing rows.
- Saturation is recorded, never implied. A recorded honest failure is the
 model: a saturation criterion that "never fired" because the log was not kept,
 written up as such rather than implied to have held.
- Retrieval sufficiency has a measurable shape. A strategy that finds k of k
 known relevant items bounds the miss rate; 59 of 59 gives more than 95%
 confidence that recall exceeds 95% (known-item method, Sampson & McGowan
 2011; check the binomial bound yourself).

## Decision rules

- Stopping early with the reason stated is a success mode, not a failure.
- A structural wall (paywalled half of the literature, an unpublished
 standard, no deployment telemetry anywhere) is a legitimate stop. Name the
 wall as a finding.
- When new information stops changing conclusions, stop. The report records
 that judgment.

## Procedure

1. At plan time, pre-register the stop criteria in the plan file.
2. During retrieval, log repeat or already-covered queries as they happen.
3. At close, mark each criterion: met, not met, or not applicable.
4. Write the stop reason in one sentence naming the criterion that fired.
5. If none fired, write why stopping is still correct.

## Anti-patterns

- Stopping because the session feels long, with no criterion named.
- Declaring saturation without a log of covered queries.
- Extending forever because no criteria were pre-registered.
- Hiding an unmet criterion inside a confident report.

## Done checklist

- The plan file names the criteria.
- The saturation log exists, even if short.
- The record names the fired criterion or the named wall.
- The final report repeats the stop reason verbatim.

The rule should also say what happens when a criterion fires early with conclusions that feel unfinished, because the temptation is to continue until the report reads well rather than until the evidence stops moving. A stop that is honoured only when convenient is not a stop rule.

## Sources

- <https://osf.io/prereg/>
- <https://arxiv.org>
