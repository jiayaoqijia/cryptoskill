---
name: salesportl-sales-marketing-quality-review-orchestrator
description: Run recursive quality checks across sales and marketing operations outputs, scoring logic, consistency, thoroughness, and completeness.
version: 2.0.0
tags: [salesportl, sales-marketing, niche-suite, context-loop, qa-recursive, tool-node-aware]
---

## Purpose
Run recursive quality checks across sales and marketing operations outputs, scoring logic, consistency, thoroughness, and completeness.

## Use when
- You are operating inside `SalesPortl-Sales-Marketing-Skills-Suite`.
- You need sales and marketing operations execution quality for sales teams, growth teams, and full-funnel agencies.
- You want repeatable, improving workflows that learn from each run via context + memory updates.

## Industry fit: micro-niche variants
- outbound-led growth
- inbound funnel optimization
- account-based campaigns

## Standard operating patterns (SOP)
- lead qualification standards
- campaign to pipeline attribution
- handoff between SDR/AE/CS functions

## SalesPortl platform tooling focus (if available in workspace)
- campaign builders with stage-based triggers
- pipeline automation and SLA alerts
- calendar-driven follow-up sequences

## Required inputs
- Business objective and requested deliverable
- Current context quality (none/partial/verified)
- Business model, offer mix, and target customer profile
- Authority boundary for external actions (draft-only unless approved)
- Available SalesPortl platform features in this workspace

## Workflow
1. Score outputs across logic, consistency, thoroughness, completeness, and platform execution readiness.
2. Reject any output below threshold and send targeted revision requests to source skill(s).
3. Run recursive loops until confidence threshold is achieved or blocking unknowns are surfaced.
4. Finalize only when output is actionable, niche-accurate, and tool-node implementable.

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
- Scorecard by criterion: ...
- Defects and required corrections: ...
- Loop count and current confidence: ...
- Final go/no-go decision: ...
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

## Recursive loop control
1. Evaluate current output against the scoring rubric.
2. If target score is not met, route revision to the most relevant source skill.
3. Re-run checks after revision and update confidence score.
4. Continue until target score is reached or blocking unknowns require user input.
