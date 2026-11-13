---
name: ac-chaos-and-capacity-testing
description: "Breaking a system deliberately to find where it fails: failure injection and blast radius control, game days and their safety rails, the load model and whether it resembles reality, soak and spike tests, capacity headroom and the knee, dependency failure and partial degradation, and the written experiment record. Use when asking \"chaos engineering\", \"game day\", \"failure injection\", \"load test model\", \"soak test\", \"spike test\", \"capacity headroom\", \"what breaks under load\", \"blast radius\", \"should we test in production\". Not for latency profiling and optimisation (ac-performance), not for SLO definition and error budgets (ac-reliability), not for backup and disaster recovery targets (ac-reliability)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Chaos and capacity testing

## Overview

Two testing disciplines answer the same question from opposite directions. Capacity testing asks how much load the system handles before it degrades; chaos testing asks what happens when a component fails while it is handling that load. Both are experiments, and both are worthless without a hypothesis: a load test with no model proves the system can serve traffic nobody sends, and a chaos experiment with no expected behaviour proves only that something happened.

This skill covers the design of those experiments: how to build a load model that resembles production, where the knee is and why it matters more than the peak, how to inject failures with a blast radius you can stop, and what a soak test reveals that a short test cannot. Latency optimisation and reliability targets belong to other skills.

Primary sources: <https://principlesofchaos.org/> and <https://sre.google/>.

## When to use

- When planning a load, soak, or spike test.
- When designing a chaos experiment or a game day.
- When capacity headroom needs to be measured rather than assumed.
- When a dependency failure's effect on the system is unknown.

## When NOT to use

- For profiling, bundle size, and Core Web Vitals (use ac-performance).
- For SLOs, error budgets, and alerting (use ac-reliability).
- For backup, restore, and DR targets (use ac-reliability).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/failure-injection-and-blast-radius.md` | `software-engineering/failure-injection-and-blast-radius` | Injecting a fault with a stop button and a stated limit. |
| `subskills/game-days-and-hypotheses.md` | `software-engineering/game-days-and-hypotheses` | A stated expectation, a time box, and what counts as a finding. |
| `subskills/load-model-validity.md` | `software-engineering/load-model-validity` | Whether the synthetic traffic resembles the real traffic. |
| `subskills/soak-and-spike.md` | `software-engineering/soak-and-spike` | Long-duration leaks and sudden onsets, and what each reveals. |
| `subskills/capacity-headroom.md` | `software-engineering/capacity-headroom` | The knee, the plateau, and headroom measured rather than guessed. |
| `subskills/dependency-failure.md` | `software-engineering/dependency-failure` | Partial degradation when a dependency slows or stops. |
| `subskills/experiment-record.md` | `software-engineering/experiment-record` | The written record: hypothesis, method, result, and follow-up. |

## Status and honest limits

Testing in production is a real practice and a real risk, and the difference between the two is preparation rather than courage. Nothing here authorises an experiment on a live system: the blast radius control, the abort condition, and the people who must agree are prerequisites, not details. Capacity numbers also decay — the system changes and the measured ceiling moves — so a capacity result is a measurement with a date, not a property.
