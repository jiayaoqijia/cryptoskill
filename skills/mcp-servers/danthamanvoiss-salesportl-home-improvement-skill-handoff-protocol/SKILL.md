---
name: salesportl-home-improvement-skill-handoff-protocol
description: Standardize inter-skill handoffs for home improvement services work with clear assumptions, approvals, and next-node instructions.
version: 2.0.0
tags: [salesportl, home-improvement, niche-suite, context-loop, qa-recursive, tool-node-aware]
---

## Purpose
Standardize inter-skill handoffs for home improvement services work with clear assumptions, approvals, and next-node instructions.

## Use when
- You are operating inside `SalesPortl-Home-Improvement-Skills-Suite`.
- You need home improvement services execution quality for home improvement contractors and remodeling businesses.
- You want repeatable, improving workflows that learn from each run via context + memory updates.

## Industry fit: micro-niche variants
- kitchen/bath remodelers
- general renovation contractors
- specialty install providers

## Standard operating patterns (SOP)
- design/estimate approval process
- project milestone communication
- change-order and upsell handling

## SalesPortl platform tooling focus (if available in workspace)
- campaign setup for project showcases
- click tracking for consultation funnels
- pipeline workflows for estimate→project kickoff

## Required inputs
- Business objective and requested deliverable
- Current context quality (none/partial/verified)
- Business model, offer mix, and target customer profile
- Authority boundary for external actions (draft-only unless approved)
- Available SalesPortl platform features in this workspace

## Workflow
1. Package source objective, context source, assumptions, approvals, and constraints.
2. Include logic checks performed, confidence score, and unresolved risks.
3. Specify downstream skill and exact output format expected.
4. Prevent rework by summarizing completed workflow nodes and generated assets.

## Platform execution checklist
- Campaign orchestration nodes
- Click-tracking and attribution configuration
- Workflow/automation nodes
- Custom agent launch and role-specialized sub-agents
- CRM pipeline and lead stage automation
- Calendar, booking, and follow-up automations
- Website/page/app builder flows (where available)

## Output format
```text
- Handoff packet: ...
- Logic/consistency checks completed: ...
- Risks/open questions: ...
- Exact downstream instructions: ...
```

## Confidence scoring rubric (0-5 each)
- Logic integrity
- Consistency with context and previous decisions
- Thoroughness of analysis
- Completeness for implementation
- Platform/tooling readiness
- Niche-specific relevance
- **Target**: average >= 4.2 before final handoff

## Quality checks
- Output explicitly reflects this industry plus at least one micro-niche variant.
- Recommendations map to practical SalesPortl feature usage when requested.
- Ambiguities are handled by questions, not assumptions.
- Logic is coherent end-to-end across routing, execution, and QA.
- Completeness is verified before finalization; partial output is labeled as partial.
