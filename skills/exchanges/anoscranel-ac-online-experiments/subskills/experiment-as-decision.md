---
name: experiment-as-decision
domain: software-engineering/experiment-as-decision
trigger: "Framing an experiment around the decision it will drive."
anti_trigger: "Not for deployment mechanics, and not for backtests."
scope: "Hypothesis, decision rule, and the metric that answers the question."
status: seedling
---

# Experiment as decision

## Standard

An experiment exists to change a decision: ship, do not ship, or investigate further. That decision determines everything upstream — the metric that will answer it, the direction that counts as success, the duration that makes the answer credible. An experiment without a stated decision defaults to "continue whatever we were already doing," which means the data collection effort purchased nothing and the result will be argued rather than acted on.

The pair that guides design is the hypothesis and the OEC — the overall evaluation criterion, the metric or weighted composite that the treatment is expected to move. The OEC must measure user value rather than the team's proxy comfort: clicks go up when you confuse people, session counts go up when you break something players need two pages for. The hypothesis names the direction, the OEC names the measure, and the decision rule states in advance what movement in what direction will trigger which action.

Primary sources: <https://experimentguide.com/> and <https://en.wikipedia.org/wiki/A/B_testing>.

## Decision rules

- State the decision the experiment serves before any design work.
- Name the hypothesis with its expected direction on the OEC.
- Define the OEC as the user-value metric, not the team's convenience metric.
- Write the decision rule before launch: which movement triggers ship, hold, or investigate.
- Trace the OEC to the decision: if the OEC moves as hypothesised, what exactly changes?
- Record all three in the experiment record before the first user is assigned.

## Procedure

1. Write the decision in one sentence: what will be different afterwards?
2. Draft the hypothesis: the treatment will move this metric in that direction because of this mechanism.
3. Choose the OEC and justify why it measures user value.
4. State the decision rule with thresholds and alternatives.
5. Identify secondary metrics and the segments that will be examined, in advance.
6. Freeze the design into the experiment record and register the analysis plan.

## Anti-patterns

- Running an experiment whose result cannot change any decision.
- An OEC that measures the thing that moved rather than the thing that mattered.
- Writing the decision rule after seeing the first week of data.
- Hypothesising a direction and then reading any movement as success.
- Changing the metric mid-experiment because the first one did not move.

## Done checklist

- [ ] Decision stated before design.
- [ ] Hypothesis with direction on the OEC.
- [ ] OEC justified as user value.
- [ ] Decision rule written with thresholds.
- [ ] Secondary metrics and segments pre-declared.
- [ ] Design frozen before assignment begins.

## Sources

- Kohavi, Tang, Xu book site: <https://experimentguide.com/>
- A/B testing overview: <https://en.wikipedia.org/wiki/A/B_testing>
- Sample size foundations: <https://en.wikipedia.org/wiki/Sample_size_determination>
