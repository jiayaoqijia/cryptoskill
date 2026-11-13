---
name: ac-agent-run-observability
description: "Seeing what an agent did while it ran: the run record as a first-class stratum, step-level traces of tool calls and their inputs and outputs, span-level token and cost attribution per step, replay and diff for failed runs, failure classification by step type, sampling to keep tracing affordable, dashboards decisions actually use, and the written observability record. It builds the inspection layer for agent behaviour; it never recommends an observability vendor and never predicts agent performance. Use when asking \"agent tracing\", \"tool call logging\", \"why did the agent call this\", \"agent run replay\", \"LLM trace\", \"agent monitoring\", \"token cost per step\", \"agent run record\", \"observability for agents\". Not for service-level metrics and SLOs (ac-reliability), not for evaluating models or suites offline (ac-model-evaluation), not for spend ledgers alone (ac-token-cost-optimization), not for memory across sessions (ac-agent-memory-and-recall)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Agent run observability

## Overview

An agent run is invisible in a way a service request is not. A service logs its state; an agent generates a trajectory — a sequence of model calls, tool invocations, and intermediate outputs — and the failure mode most worth debugging is usually invisible in the final answer: the tool that returned unexpectedly and steered everything after it. Run observability is the discipline of capturing that trajectory at write time so the question "why did the agent do that?" is answered by reading a trace, not by rerunning with print statements.

This skill is the agent-specific layer above general instrumentation. A service-level skill owns SLI and SLO telemetry; this owns the trace structure of a run: per-step spans, call arguments captured at full fidelity, token and cost fields attached per step, and replay that reproduces a run from its stored trajectory. Adjacent skills own the cross-session memory, the offline evaluation suite, and the spend ledger; the splits between them are named in each's boundaries.

Primary sources: <https://opentelemetry.io/docs/specs/semconv/gen-ai/> and <https://langfuse.com/docs>.

## When to use

- When an agent behaved unexpectedly and the cause lives in its trajectory.
- When building the trace structure of a new agent from scratch.
- When attributing tokens and cost to steps within a run.
- When dashboards need to answer agent questions, not just service health.

## When NOT to use

- For SLI, SLO, and error-budget telemetry of services (use ac-reliability).
- For offline evaluation suites and model comparisons (use ac-model-evaluation).
- For the spend ledger across bills (use ac-token-cost-optimization).
- For what persists beyond the session (use ac-agent-memory-and-recall).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/run-record-structure.md` | `software-engineering/run-record-structure` | The whole run as an object: spans, inputs, outputs, timing, lineage. |
| `subskills/step-level-tracing.md` | `software-engineering/step-level-tracing` | One span per tool call and model call, captured at fidelity. |
| `subskills/token-and-cost-per-step.md` | `software-engineering/token-and-cost-per-step` | Token and price attached to each step, not just to the request. |
| `subskills/replay-and-diff.md` | `software-engineering/replay-and-diff` | Reproducing a run from its trace; diffing two runs. |
| `subskills/failure-classification.md` | `software-engineering/failure-classification` | Where it went wrong: classify by step, reason, and stage. |
| `subskills/trace-sampling.md` | `software-engineering/trace-sampling` | What to capture in full; what to record in outline. |
| `subskills/agent-dashboards.md` | `software-engineering/agent-dashboards` | Dashboards for answers to agent questions, not just graphs. |
| `subskills/run-observability-record.md` | `software-engineering/run-observability-record` | The written record: coverage, retention, tracing contract. |

## Status and honest limits

Capture at full fidelity logs what the tool returned, including any personal data the tool touched — the privacy boundary of heavy logging itself needs defining (which fields are retained, how long, for whom), and this skill defers the privacy design to privacy engineering and only personalises its scope to what a Trace must carry. Vendor conventions differ in detail; the OpenTelemetry GenAI semantic conventions are the developing standard but not universally adopted; the skill teaches the structure of the Trace in canonical terms rather than a vendor's schema.
