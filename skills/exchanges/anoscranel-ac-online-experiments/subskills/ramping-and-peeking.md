---
name: ramping-and-peeking
domain: software-engineering/ramping-and-peeking
trigger: "Ramping for safety without peeking the result into significance."
anti_trigger: "Not for rollout mechanics alone, and not for guardrail design."
scope: "Ramps for safety, fixed horizons for measurement, and sequential honesty."
status: seedling
---

# Ramping and peeking

## Standard

Ramping — starting at a small percentage and increasing — serves safety and performance: a bug that ships to one percent of users harms one percent. But each percentage change restarts measurement. A ramped experiment's early percentages are sabotage data: curious power users, instant rollback triggers, and arms whose membership changed as the ramp moved. The measured phase begins when the percentage stabilises, and the effective sample starts accruing then.

Peeking is the twin sin. Checking a moving result against a fixed significance threshold and stopping when it crosses inflates false positives enormously: twenty independent looks at noise produce a crossing almost by certainty. The honest alternatives are a fixed horizon declared in advance, or a sequential design whose thresholds adjust for the number of looks. Anything else is optional stopping, and optional stopping finds whatever the analyst was hoping for.

Primary sources: <https://experimentguide.com/> and <https://en.wikipedia.org/wiki/A/B_testing>.

## Decision rules

- Ramp for safety; measure at a stable percentage; keep the two phases separate in the record.
- Declare the analysis horizon at launch and hold it.
- If early looks are operationally necessary, use sequential thresholds; never a fixed-threshold repeat.
- Treat a mid-experiment metric dip during ramp as a safety investigation, not a result.
- Never stop on a crossing found by repeated looks at a fixed threshold.
- Record every look that occurred, even the ones that did not influence the stop decision.

## Procedure

1. Choose the ramp schedule from performance and safety needs.
2. Hold each ramp step until monitoring shows stability.
3. Fix the measured percentage and the analysis horizon before measurement.
4. If interim looks are needed, apply sequential-analysis thresholds.
5. Complete the horizon and run the planned analysis once.
6. Record the ramp history and every look with timestamps.

## Anti-patterns

- Ending the experiment the first morning the number looks good.
- Treating the ramp percentage's own data as the experiment.
- Quietly extending a "failed" experiment until it passes.
- Ten dashboard checks a day as the stop rule.
- Restarting the clock after each look without adjusting thresholds.

## Done checklist

- [ ] Ramp schedule pre-declared.
- [ ] Measurement phase separated from ramp.
- [ ] Horizon declared at launch.
- [ ] Sequential thresholds where looks are needed.
- [ ] Single final analysis at the horizon.
- [ ] All looks logged.

## Sources

- Peeking and validity: <https://experimentguide.com/>
- Sequential vs fixed horizons: <https://en.wikipedia.org/wiki/A/B_testing>
- Multiple comparisons: <https://en.wikipedia.org/wiki/Multiple_comparisons_problem>
