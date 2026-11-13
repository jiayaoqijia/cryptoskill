---
name: novelty-and-primacy
domain: software-engineering/novelty-and-primacy
trigger: "Reading effects that fade because the treatment is new or relearned."
anti_trigger: "Not for guardrail stopping, and not for logging analytics."
scope: "Effects that fade, and the cohort analysis that reveals them."
status: seedling
---

# Novelty and primacy

## Standard

A new interface is a change, and users respond to change itself before they respond to the thing. Novelty effects push a metric up for early adopters who explore anything new; primacy effects push it down while users relearn where things went. Both fade on a timescale of days to weeks, and both can present as a stable effect if the experiment happens to last exactly as long as the fade. An experiment that concludes during the novelty window has measured the reaction to change, not the value of the change.

The diagnostic that separates durable effect from fade is cohort-by-exposure-time analysis: group users by when they first experienced the treatment, and observe the effect for each cohort as their own exposure accumulates. A durable effect persists in every cohort's later days; a novelty effect lives only in each cohort's first days and dies thereafter. A single time series of the whole population averages both, and the average hides exactly the distinction the decision needs.

Primary sources: <https://experimentguide.com/> and <https://en.wikipedia.org/wiki/Novelty_effect>.

## Decision rules

- Ask in advance whether the treatment plausibly triggers a learnable reaction.
- Run long enough for the fading effect to hide: at least one full learning cycle, often two weeks.
- Analyze by exposure cohort, not only by calendar day.
- Distinguish novelty (a one-off excitement) from primacy (a start-up cost) by sign.
- Treat a metric that decays toward the control as a fade, not a weakening success.
- For changed placements, examine interaction-heavy user segments, where learning costs live.

## Procedure

1. Estimate the learning cycle for the affected interface and set experiment duration beyond it.
2. Log each unit's first-exposure date as part of the experiment record.
3. Compute the effect by cohort-week of exposure, not only the rolling population average.
4. Read the pattern: persistent effect repeats across cohorts; novelty fades within each.
5. If the effect fades, report the durable value as the post-fade baseline, and say so.
6. If the effect persists across cohorts, record durability as the basis for the ship decision.

## Anti-patterns

- Reporting only the population-average time series.
- Ending the experiment at novelty's peak.
- Treating a decay back toward control as "mixed evidence."
- Assuming the new treatment failed because early days dipped (primacy misread).
- Extending an experiment past fade to rescue a dying positive — the reverse fade is the same sin.

## Done checklist

- [ ] Learning cycle estimated pre-launch.
- [ ] First-exposure date logged per unit.
- [ ] Cohort analysis in the analysis plan.
- [ ] Novelty versus primacy distinguished by sign.
- [ ] Post-fade value identified.
- [ ] Durability finding recorded with the decision.

## Sources

- Novelty effects in experiments: <https://experimentguide.com/>
- Novelty effect concept: <https://en.wikipedia.org/wiki/Novelty_effect>
- Cohort design overview: <https://en.wikipedia.org/wiki/A/B_testing>
