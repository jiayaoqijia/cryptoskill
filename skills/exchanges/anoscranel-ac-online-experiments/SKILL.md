---
name: ac-online-experiments
description: "Running trustworthy online controlled experiments: the experiment as a decision with a hypothesis and a success metric, statistical power and minimum detectable effect before launch, randomisation units and stable bucketing, ramping percentages and the peeking problem, guardrail metrics that stop an experiment early, novelty and primacy effects that fade, multiple comparisons across a fleet, and the written experiment record. It explains how to design, run, and read a controlled experiment; it never certifies that a variant won. Use when asking \"A/B test\", \"controlled experiment\", \"treatment arm\", \"randomisation unit\", \"minimum detectable effect\", \"statistical power\", \"peeking\", \"sequential testing\", \"novelty effect\", \"guardrail metric\", \"experiment ramp\", \"hash bucketing\", \"why did our A/B test flip sign\". Not for trading strategy backtests (ac-backtest-integrity), not for prompt and model evaluation sets (ac-prompt-engineer), not for feature deployment mechanics like canary and rollback (ac-ci-and-release)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Online experiments

## Overview

An online controlled experiment assigns some users to a treatment and others to a control, measures the difference, and decides. The arithmetic is one line; the trustworthiness is the whole craft. Most results are wrong not because the statistics were miscomputed but because the experiment was misdesigned: the metric answered a different question than the decision, the randomisation leaked, the sample was too small to detect anything realistic, or the analyst peeked at a moving average until it crossed a threshold.

This skill covers the design and reading of experiments: the decision framed first, power computed before launch rather than lamented after, assignment made stable and hashable, ramps that separate safety from measurement, guardrails that stop real harm, novelty effects that fade and mislead, and the multiplicity that a fleet of simultaneous tests introduces. The deployment mechanics of rolling out a feature belong elsewhere; the trading backtest and the prompt evaluation set are separate instruments with the same honesty problems and different machinery.

Primary sources: <https://experimentguide.com/> and <https://en.wikipedia.org/wiki/A/B_testing>.

## When to use

- When designing or sizing an online controlled experiment.
- When a result will decide whether a feature ships.
- When ramping, peeking, or multiple simultaneous tests threaten the reading.
- When an experiment result looks too good, too bad, or too unstable to be true.

## When NOT to use

- For trading strategy backtests (use ac-backtest-integrity).
- For evaluating prompts and models on held-out sets (use ac-prompt-engineer).
- For feature deployment mechanics like canary rollout and rollback (use ac-ci-and-release).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/experiment-as-decision.md` | `software-engineering/experiment-as-decision` | Hypothesis, decision rule, and the metric that answers the question. |
| `subskills/power-and-mde.md` | `software-engineering/power-and-mde` | Sample size, minimum detectable effect, and the pre-launch arithmetic. |
| `subskills/randomisation-and-bucketing.md` | `software-engineering/randomisation-and-bucketing` | Units, hash assignment, and the leakage that breaks an experiment. |
| `subskills/ramping-and-peeking.md` | `software-engineering/ramping-and-peeking` | Ramps for safety, fixed horizons for measurement, and sequential honesty. |
| `subskills/guardrail-metrics.md` | `software-engineering/guardrail-metrics` | Metrics that stop a test early because the cost of waiting is real. |
| `subskills/novelty-and-primacy.md` | `software-engineering/novelty-and-primacy` | Effects that fade, and the cohort analysis that reveals them. |
| `subskills/multiplicity-across-tests.md` | `software-engineering/multiplicity-across-tests` | Many tests, many metrics, and the corrections that keep a fleet honest. |
| `subskills/experiment-record.md` | `software-engineering/experiment-record` | The written record: design, analysis plan, result, and the decision it drove. |

## Status and honest limits

Experiments measure averages over populations during a window; they do not certify that every segment benefited, that the effect will persist, or that the metric movement had the cause the team believes. Sample ratio mismatch and instrumentation bugs can silently ruin results that look statistically sound. Nothing here recommends shipping a variant — it states what the evidence supports and what it cannot, and a negative result honestly recorded is worth more than a positive one peeked into existence.
