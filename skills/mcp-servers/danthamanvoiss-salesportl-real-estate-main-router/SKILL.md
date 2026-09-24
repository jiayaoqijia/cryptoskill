---
name: salesportl-real-estate-main-router
description: Route real estate services tasks to the smallest reliable skill stack with context-first logic, tool-node awareness, and confidence-gated recursion.
version: 2.0.0
tags: [salesportl, real-estate, niche-suite, context-loop, qa-recursive, tool-node-aware]
---

## Purpose
Route real estate services tasks to the smallest reliable skill stack with context-first logic, tool-node awareness, and confidence-gated recursion.

## Use when
- You are operating inside `SalesPortl-Real-Estate-Skills-Suite`.
- You need real estate services execution quality for real estate teams, brokerages, and property operators.
- You want repeatable, improving workflows that learn from each run via context + memory updates.

## Industry fit: micro-niche variants
- buyer-side teams
- listing-heavy teams
- investor/property management operators

## Standard operating patterns (SOP)
- lead routing by intent/timeline
- listing launch cadence
- showing/offer follow-up workflows

## SalesPortl platform tooling focus (if available in workspace)
- listing campaign node orchestration
- click tracking by listing CTA
- pipeline and calendar automations for showing-to-close

## Required inputs
- Business objective and requested deliverable
- Current context quality (none/partial/verified)
- Business model, offer mix, and target customer profile
- Authority boundary for external actions (draft-only unless approved)
- Available SalesPortl platform features in this workspace

## Workflow
1. Run `brand-bootstrap-memory-loop` when context is missing, stale, or inconsistent.
2. Run `context-intake` to normalize business model, micro-niche, offer mix, and operating constraints.
3. Classify request into sales, marketing, delivery/operations, client success, or multi-function strategy.
4. Ask minimum clarifying questions when objective, authority, or context is ambiguous.
5. Route to 1-3 skills only; include `quality-review-orchestrator` for all substantive deliverables.
6. If platform-enabled execution is requested, map the plan to explicit SalesPortl workflow nodes and tool actions.
7. Launch sub-agents by function for parallel research/execution when complexity is high; merge results through `skill-handoff-protocol`.
8. Return selected chain, unresolved unknowns, and confidence score.

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
- Router chain (skills + order): ...
- Request class and micro-niche fit: ...
- Required SalesPortl features/tool actions: ...
- Missing inputs and clarifying questions: ...
- Sub-agent parallelization plan (if needed): ...
- Confidence score (0-100) and next-step prompt: ...
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

## Related skills in this collection
- salesportl-real-estate-brand-bootstrap-memory-loop
- salesportl-real-estate-context-intake
- salesportl-real-estate-offer-service-mapper
- salesportl-real-estate-sales-conversion-playbook
- salesportl-real-estate-marketing-growth-planner
- salesportl-real-estate-delivery-operations-planner
- salesportl-real-estate-client-success-expansion
- salesportl-real-estate-skill-handoff-protocol
- salesportl-real-estate-quality-review-orchestrator
