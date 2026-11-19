---
name: ac-agent-eval-harness
description: 'Testing an assembled agent — loop, tools, guardrails, the whole system — before you ship a change: golden scenarios from real traces, assertion layers from final answers down to individual tool calls, the mock-and-stub decision for each tool, replay as regression testing, flaky-agent triage, environment simulation that stays honest, and the written harness record. It builds the pre-release test layer for agent systems; it never predicts agent performance and never certifies an agent as safe. Use when asking "test an agent", "agent eval harness", "golden scenarios", "tool call assertions", "agent regression suite", "mock tool", "agent test flakiness", "pre-ship agent test", "LLM agent CI", "assertions on trajectory". Not for model selection suites (ac-model-evaluation), not for live-run inspection and dashboards (ac-agent-run-observability), not for the runtime interrupt layer (ac-agent-guardrails), not for unit-testing software in general (ac-testing).'
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Agent eval harness

## Overview

An agent is a system with moving parts that do not fail independently: a model that varies by temperature and provider update, a tool loop whose next call depends on the last, guardrails that can interrupt mid-stream. Testing the assembled system before a release is different work from testing any component — the unit is the *run*, the assertion target is often a tool call rather than a return value, and the same harness must catch both regressions (it worked, now it doesn't) and silent drift (it still "works" while doing something worse).

This skill owns the pre-release harness. Its neighbours carve the rest: ac-model-evaluation tests models offline for selection; ac-agent-run-observability inspects live runs; ac-agent-guardrails enforces at runtime; ac-testing is software test craft. The harness sits between: the assembled agent under controlled conditions, exercised by scenarios that represent real work, with assertions precise enough to catch a change and loose enough not to rewrite the agent.

Primary sources: <https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html> and <https://arxiv.org/abs/2308.03688>.

## When to use

- Before shipping an agent change — model swap, tool edit, prompt change, guardrail update.
- When an agent needs a standing regression suite.
- When tools must be replaced with test doubles for repeatable runs.
- When agent runs flake and the suite needs triage discipline.

## When NOT to use

- For model selection suites and offline benchmarks (use ac-model-evaluation).
- For live-run tracing and dashboards (use ac-agent-run-observability).
- For the runtime interrupt and gating layer (use ac-agent-guardrails).
- For software unit/integration testing in general (use ac-testing).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/golden-scenarios.md` | `software-engineering/golden-scenarios` | Building the scenario set from real traces, not invention. |
| `subskills/assertion-layers.md` | `software-engineering/assertion-layers` | What to assert at each depth, from answer to tool call. |
| `subskills/tool-doubles.md` | `software-engineering/tool-doubles` | Deciding mock, stub, or real for each tool. |
| `subskills/replay-regression.md` | `software-engineering/replay-regression` | Recorded trajectories as regression baselines. |
| `subskills/flaky-agent-triage.md` | `software-engineering/flaky-agent-triage` | Dividing nondeterminism from real defects. |
| `subskills/environment-simulation.md` | `software-engineering/environment-simulation` | Simulated worlds that stay honest about what they omit. |
| `subskills/harness-record.md` | `software-engineering/harness-record` | The written record: coverage, results, and the ship/no-ship decision. |

## Status and honest limits

A harness is a sample of an agent's behaviour space, never a proof of correctness; passing scenarios say what was tested worked, not that the agent is safe. Scenario sets drift stale as real usage diverges from the traces they were built from, and the record must carry that risk honestly. Nondeterministic components can be reined in, not eliminated — a harness built on exact-match assertions against a live model will fail its authors, not the agent. Nothing here certifies safety; the guardrail layer and its incident record own that question in production.
