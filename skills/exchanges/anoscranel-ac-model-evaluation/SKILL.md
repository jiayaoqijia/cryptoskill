---
name: ac-model-evaluation
description: "Building evaluation suites that decide between models for a task: what the eval measures before any prompt is written, constructing cases from real failure modes and coding them from task-native artifacts, contamination and why held-out data no longer guarantees freshness, automatic scoring with exact-match and judge limits, pass-at-k and aggregate metrics read honestly, human comparison and preference data as a separate instrument, and the written evaluation record. It designs the measurement; it never certifies a model as good and never recommends a vendor. Use when asking \"model evaluation\", \"eval suite design\", \"build a benchmark\", \"contamination\", \"held-out set\", \"LLM as judge\", \"pass at k\", \"model comparison\", \"regression suite for model upgrades\", \"golden set\", \"cost of evaluation\". Not for improving a prompt against fixed cases (ac-prompt-engineer), not for running the harness code itself (ac-llm-api-integration), not for evaluating datasets as research evidence (ac-alternative-data)."
license: MIT
metadata:
  domain: prompt-engineering
status: seedling
---

# Model evaluation

## Overview

Choosing a model for a task is a measurement problem, and the measurement decides more than the choice of models does: an evaluation built from convenient examples measures convenience, one built from real failure modes measures the task, and the two rankings they produce are rarely the same. An eval suite is a small, task-shaped body of evidence — cases with known answers or graded criteria — that turns "model A feels better" into a number, and the number is only as good as its case design.

This skill covers building that instrument: deciding what the eval must measure, constructing cases from the task's real failure surface rather than from invented ease, the contamination problem that quietly erodes benchmarks built from public data, scoring tiers from deterministic checks through model judges to humans, reading aggregate metrics like pass-at-k without fooling yourself, and recording the whole thing so a later model choice can be re-decided on new evidence. Improving a prompt against a fixed set is a different skill; this one is about the set.

Primary sources: <https://docs.anthropic.com/en/docs/about-claude/evaluate> and <https://github.com/EleutherAI/lm-evaluation-harness>.

## When to use

- When choosing between models or model versions for a specific task.
- When building a regression suite to guard model upgrades.
- When a benchmark's public score is being mapped to your task.
- When deciding how much evaluation a decision deserves.

## When NOT to use

- For improving a prompt against fixed cases (use ac-prompt-engineer).
- For the harness and API mechanics of running evals (use ac-llm-api-integration).
- For evaluating datasets as research evidence (use ac-alternative-data).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/what-the-eval-measures.md` | `prompt-engineering/what-the-eval-measures` | Deciding the question and decision the eval serves. |
| `subskills/case-construction.md` | `prompt-engineering/case-construction` | Building cases from real failure modes, not ease. |
| `subskills/contamination.md` | `prompt-engineering/contamination` | Why held-out data no longer guarantees a fresh test. |
| `subskills/scoring-and-judges.md` | `prompt-engineering/scoring-and-judges` | Deterministic checks first, judges second, humans for the residue. |
| `subskills/metrics-and-reading.md` | `prompt-engineering/eval-metrics-and-reading` | Pass-at-k, aggregate scores, and honest reading. |
| `subskills/human-comparison.md` | `prompt-engineering/human-comparison` | Preference data and side-by-side as a separate instrument. |
| `subskills/eval-economics.md` | `prompt-engineering/eval-economics` | Cost, cadence, and how much eval a decision needs. |
| `subskills/evaluation-record.md` | `prompt-engineering/evaluation-record` | The written record: cases, scoring, results, and provenance. |

## Status and honest limits

An eval measures the cases it contains, and nothing else: a model can be excellent on your suite and poor on the population of requests you actually receive, if the suite is not drawn from that population. Public benchmarks add a second limit — the score on a contaminated benchmark measures recall of training data as much as capability. Treat every score as evidence about the cases measured, and re-decide when the task shifts. Nothing here certifies a model; it builds the instrument a decider can trust or rightly distrust.
