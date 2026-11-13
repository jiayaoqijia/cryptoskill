---
name: guardrail-metrics
domain: software-engineering/guardrail-metrics
trigger: "Choosing the metrics that can stop an experiment early."
anti_trigger: "Not for the OEC choice, and not for incident response."
scope: "Metrics that stop a test early because the cost of waiting is real."
status: seedling
---

# Guardrail metrics

## Standard

Guardrails are metrics a treatment is not permitted to damage: latency, error rates, crash rates, page load success, privacy-regulated states. Unlike the OEC, which the experiment hopes to move, guardrails define what the experiment must not move, and their breach justifies stopping before the horizon when the cost of continuing is larger than the information still being purchased. The distinction is the legitimate exception to the no-early-stop rule: a stopping rule declared in advance, with a threshold and a reaction, is analysis discipline, while stopping on a whim at the OEC's crossing is not.

Guardrails must be objective, automatically collected, and agreed before launch — a guardrail discovered mid-experiment is an opinion wearing a metric's name. The best guardrails measure the user's experience of harm directly rather than the team's inference of it: a crash rate rather than a log-line count, a load-success rate rather than an average response time that latency-tolerant outliers flatter.

Primary sources: <https://experimentguide.com/> and <https://engineering.atspotify.com>.

## Decision rules

- Select guardrails for user-visible harm before launch, with thresholds and stop actions.
- Prefer directly observed guardrails over inferred proxies.
- Wire guardrails to alert during the ramp's first steps, when the population is smallest and harm is newest.
- Distinguish statistically significant guardrail breach from operationally catastrophic breach — the second stops on sight.
- Log and enforce each guardrail trigger through the pre-declared action.
- Record guardrails that were NOT triggered, as evidence the risks were monitored.

## Procedure

1. List the harms the treatment could plausibly cause users.
2. Choose one measurable guardrail per harm, directly observed where possible.
3. Set the alert threshold from historical variance and the stop action from the harm's severity.
4. Instrument the guardrails and verify alerting during the first ramp step.
5. On trigger, execute the stop action and investigate as an incident, not a result.
6. Record all guardrail states at experiment end.

## Anti-patterns

- Declaring guardrails after the experiment is underway.
- Guardrail metrics no dashboard or alert actually monitors.
- Stopping on the OEC's movement using a guardrail as the excuse.
- Averaging away the harmed segment in a composite guardrail.
- Treating a guardrail breach as a result rather than an incident.

## Done checklist

- [ ] Harm-by-harm guardrail list pre-declared.
- [ ] Directly observed metrics selected.
- [ ] Thresholds and stop actions written before launch.
- [ ] First-ramp verification done.
- [ ] Any trigger actioned per the pre-declared rule.
- [ ] All guardrail states recorded on completion.

## Sources

- Guardrail design in controlled experiments: <https://experimentguide.com/>
- Engineering culture with experiment guardrails: <https://engineering.atspotify.com>
- Overview: <https://en.wikipedia.org/wiki/A/B_testing>
