---
name: ac-agent-coding-governance
description: "Governing AI-written code and the agent's repo instructions: merge gates, review packets, provenance logs, licence scanning, liability and authorship for generated code, plus AGENTS.md rules files, context budgets and compaction. Use when asking \"review AI-generated code\", \"the agent wrote this patch\", \"who is liable for generated code\", \"set up an AGENTS.md\", \"the agent ignores the repo rules\", \"compact the rules file\". Not for judging a human colleague's diff, designing the test portfolio, or CI pipeline wiring; those sit outside this skill."
license: MIT
metadata:
  domain: software-engineering
---

# Agent Coding Governance

## Overview

Two leaves govern agent-assisted development. One sets the gates a machine-written change must pass before merge: the review packet, provenance, licence scan and liability frame. The other covers the repo's instruction file for agents: what goes in it, how long it may run, and when to compact it.

## When to use

- Reviewing or accepting agent-written patches; assembling the review packet.
- Provenance, licence-hygiene, liability and authorship questions over generated code.
- Setting up, restructuring or slimming an AGENTS.md or rules file; the agent ignoring repo rules; context-budget problems.

## When not to use

- Reviewing a colleague's diff on its merits — outside this skill.
- Designing the tests or the CI gates that enforce the rules — outside this skill.
- Writing human-facing docs, docstrings or API reference — outside this skill.

## Precedence

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Task | Trigger |
|---|---|---|
| `subskills/ai-assisted-coding.md` | Gates, provenance, liability for generated code | "review AI-generated code" |
| `subskills/agent-context.md` | Repo instruction files for agents | "set up an AGENTS.md" |

## See also

- `subskills/ai-assisted-coding.md` — gate the output.
- `subskills/agent-context.md` — steer the agent.
