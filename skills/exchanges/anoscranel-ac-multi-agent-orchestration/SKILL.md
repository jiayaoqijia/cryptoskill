---
name: ac-multi-agent-orchestration
description: "The craft of running more than one agent on one job: deciding when to split at all, designing roles and scopes, budgeting context between agents, writing delegation prompts, verifying agent products independently, recovering failed agents, and keeping a ledger of what the loop costs. Seven leaves: when-to-split, role-and-scope, context-budget, delegation-prompts, verification-loops, failure-and-recovery, ledger-and-leverage. Use when asking 'orchestrate multiple agents', 'multi-agent workflow', 'split this work across agents', 'design an agent team', 'delegate to subagents', 'should I use more than one agent'. Not for handoff artifacts between people and sessions (ac-handoff), triaging one human's inbound queue (ac-inbound-triage), or prompting a single model (ac-prompt-engineer)."
license: MIT
metadata:
  domain: collaboration
---

# Multi-Agent Orchestration

## Overview

The skill governs the supervisor side of multi-agent work: deciding when a task warrants splitting across multiple agents, designing non-overlapping roles and scopes, budgeting context and constraints between models, writing delegation prompts with robust checkpoint contracts, verifying agent deliverables independently, recovering failed agents without restarting from scratch, and keeping a ledger of operational costs and leverage. The reader is an agent or supervisor orchestrating a team of agents on a complex task.

## When to use

- A task is too large or complex for a single agent context and requires parallel exploration or disjoint specialization.
- Producer-validator separation is required so that the agent generating an artifact does not grade its own work.
- Multiple independent sub-problems must be investigated concurrently to meet tight wall-clock timeframes.
- A multi-step autonomous workflow requires robust failure recovery, checkpointing, and cost tracking.

## When NOT to use

Managing handoff artifacts between people and sessions is outside; that is handled by ac-handoff. Triaging one human's inbound request queue is outside; that is handled by ac-inbound-triage. Prompting a single model or tuning instruction lines for an individual agent is outside; that is handled by ac-prompt-engineer.

## Subskill index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/when-to-split.md` | `collaboration/when-to-split` | Deciding when a multi-agent split is justified by independent contexts, parallel wall-clock need, or producer-validator separation |
| `subskills/role-and-scope.md` | `collaboration/role-and-scope` | Designing the split: one outcome per agent; non-overlapping scopes; producer-is-not-validator invariant; least-privilege assignment |
| `subskills/context-budget.md` | `collaboration/context-budget` | Minimal sufficient context, not the transcript; constraints passed verbatim; direction-dependent handoffs; file-based state |
| `subskills/delegation-prompts.md` | `collaboration/delegation-prompts` | Worker prompt structure: role preamble, mission in one line, verbatim constraints, output contract, file checkpointing, no questions |
| `subskills/verification-loops.md` | `collaboration/verification-loops` | Accepting agent work: verify file on disk; validator differs from producer; adversarial passes for load-bearing claims; cost trade-off |
| `subskills/failure-and-recovery.md` | `collaboration/failure-and-recovery` | Failure classes: transient vs latent/context faults; resumption from partial files with continuation brief; escalation paths |
| `subskills/ledger-and-leverage.md` | `collaboration/ledger-and-leverage` | Running the loop: per-task cost and retry records; irreversible acts stay human-gated; sequential heavy jobs; leverage ratio measurement |

## Status and honest limits

- Seedling: assembled from public research canon on agent workflows and internal operational playbooks.
- Multi-agent orchestration incurs inherent coordination overhead; unwarranted splits degrade performance rather than improving it.
- Supervisor judgment remains critical; rules and decision trees narrow choices but do not replace operational oversight.
- Cost and latency models are estimates based on standard multi-model handoffs and vary by provider infrastructure.

⚠️ Open question: no standardized benchmark universally quantifies the exact coordination threshold where multi-agent splits outperform single-agent execution across all domains.
