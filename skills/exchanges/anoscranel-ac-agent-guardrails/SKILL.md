---
name: ac-agent-guardrails
description: 'The runtime layer that watches a live agent and can interrupt it: deciding which actions need a gate before they run, the interception points where a check can actually stop something, output screening before a user or system receives it, the interrupt harness and how interruption itself fails, blast-radius bounds, incident response, and the written record. It explains how to build the enforcement layer around a running agent; it never declares an agent safe and never recommends a moderation vendor. Use when asking "agent guardrails", "agent safety layer", "action interception", "human in the loop gate", "output filtering for agents", "kill switch for agents", "agent incident", "irreversible action gate", "prompt firewall", "agent guardrail design". Not for tool permissioning at build time (ac-security-engineer), not for analyzing injection attacks as a vulnerability class (ac-prompt-engineer), not for content adjudication policy (ac-content-moderation), not for service-level error budgets (ac-reliability).'
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Agent guardrails

## Overview

A permissioned tool is a static decision made at build time; a guardrail is a runtime decision made while the agent runs. The runtime layer answers a different question: this agent is executing right now, it is about to call `delete_database`, its last output referenced a path it was never given — do we let the call through, rewrite it, hold it for a human, or kill the session? Static permissions cannot answer any of those because they were fixed before the run existed.

This skill builds that enforcement layer: the action gates, the interception points where a check can actually block something, the output screens, the interrupt mechanics, the blast bounds, and the incident record. It shares vocabulary with security engineering and content moderation but owns the runtime-seam problem neither does: hooking a running agent such that a decision is enforced, not merely logged.

Primary sources: <https://owasp.org/www-project-top-10-for-large-language-model-applications/> and <https://www.nist.gov/itl/ai-risk-management-framework>.

## When to use

- When an agent can take actions that are irreversible or hard to reverse.
- When agent output reaches a user, a shell, a database, or another agent.
- When designing the interception points so a check can actually enforce.
- When a guardrail has fired and the incident needs handling.

## When NOT to use

- For tool scopes and permission wiring at build time (use ac-security-engineer).
- For analyzing injection as a vulnerability class in your system (use ac-prompt-engineer).
- For content-adjudication policy and reviewer QC (use ac-content-moderation).
- For service-level error budgets and SLOs (use ac-reliability).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/action-classification.md` | `software-engineering/action-classification` | Which actions need a gate, and the test that decides. |
| `subskills/interception-points.md` | `software-engineering/interception-points` | Where a check can actually block a call, and where it only watches. |
| `subskills/output-screening.md` | `software-engineering/output-screening` | Checking agent emission before a user or a downstream system receives it. |
| `subskills/interrupt-harness.md` | `software-engineering/interrupt-harness` | Hold, kill, and divert — and how interruption itself fails. |
| `subskills/blast-radius-bounds.md` | `software-engineering/blast-radius-bounds` | Caps and walls that make the worst unchecked run survivable. |
| `subskills/guardrail-incidents.md` | `software-engineering/guardrail-incidents` | What firing a guardrail triggers: capture, review, and the fix loop. |
| `subskills/guardrail-record.md` | `software-engineering/guardrail-record` | The written record: gates, checks, firings, and their reviews. |

## Status and honest limits

A guardrail is a fence on a specific path, not a proof of safety; OWASP's LLM Top 10 and NIST's AI RMF both frame these as risk-management controls, never guarantees. Guardrails induce their own failure class: false interruption that breaks a correct run, and the operator who disables noisy checks until only silent ones remain — a guardrail nobody can hear is a guardrail that has quietly died. The record's job is to keep both problems visible: auditable firings with reviewed thresholds.
