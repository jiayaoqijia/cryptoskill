---
name: power-and-mde
domain: software-engineering/power-and-mde
trigger: "Sizing an experiment before launching it."
anti_trigger: "Not for running the test, and not for prompt evaluation sets."
scope: "Sample size, minimum detectable effect, and the pre-launch arithmetic."
status: seedling
---

# Power and MDE

## Standard

Statistical power is the probability that an experiment detects an effect of a given size if it exists; the minimum detectable effect is the smallest true effect the experiment can be expected to find at that power. The two are set before launch, because after launch they are no longer choices but facts about what the experiment can and cannot see. An underpowered experiment that returns "no significant difference" has not shown the treatment does nothing; it has shown nothing at all.

The arithmetic trades three quantities against a fourth: effect size, significance level, power, and sample size. Any three determine the fourth. The honest inputs come from the metric's own historical variance and from the world's plausible effect — most product changes move metrics by fractions of a percent, and a team that powers the experiment for a two percent effect will detect nothing real while confidently publishing a null.

Primary sources: <https://experimentguide.com/> and <https://en.wikipedia.org/wiki/Sample_size_determination>.

## Decision rules

- Compute required sample size before launch from historical variance of the OEC.
- Set the MDE from the smallest effect that would justify shipping, not from optimism.
- Power at the conventional 0.80 or state why a different level was chosen.
- Convert the sample size into a duration using realistic traffic, then commit to the duration.
- Record the MDE in the experiment record; a post-hoc power lament is a design failure.
- When traffic cannot support the MDE, say so before launch — a longer run, a bigger unit, or a denser metric is a design choice, not a hope.

## Procedure

1. Pull the OEC's historical variance from the metric pipeline.
2. State the shipping-worthy effect size as the MDE.
3. Compute sample size at the chosen significance level and power.
4. Convert to calendar duration at realistic traffic.
5. Check the duration against the experiment's business window; renegotiate if too long.
6. Record MDE, power, significance, and duration in the experiment record.

## Anti-patterns

- Launching first and computing power after the result disappoints.
- Powering for an effect the team privately knows is implausible.
- Treating a non-significant underpowered result as evidence of no effect.
- Sizing on averages rather than the metric's actual variance.
- Extending the run ad hoc until the number crosses a threshold.

## Done checklist

- [ ] Historical variance measured.
- [ ] MDE set from the shipping decision.
- [ ] Sample size and power computed pre-launch.
- [ ] Duration committed before launch.
- [ ] Unrealistic-design findings raised before launch.
- [ ] All numbers in the experiment record.

## Sources

- Power and MDE in controlled experiments: <https://experimentguide.com/>
- Sample size determination: <https://en.wikipedia.org/wiki/Sample_size_determination>
- Multiple comparisons context: <https://en.wikipedia.org/wiki/Multiple_comparisons_problem>
