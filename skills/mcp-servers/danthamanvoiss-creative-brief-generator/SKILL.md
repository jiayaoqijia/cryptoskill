---
name: creative-brief-generator
description: Generate cross-functional creative requirements briefs for downstream execution teams and tools.
version: 0.1.0
tags: [marketing, creative-brief, requirements, draft-only]
---

## Purpose

Generate cross-functional creative requirements briefs for downstream execution teams and tools.

## Use when

- A campaign needs a clear requirements brief before design or production begins.
- You are defining what must be created, not generating final media assets.

## Required inputs

- Objective, target audience, key message, and CTA [client-provided].
- Brand/client context from context/BRAND-CONTEXT.template.md and context/CLIENT-CONTEXT.template.md, or drafts created with brand-context-brief-builder.
- Channel list, asset types, constraints, and approval requirements.

## Safety/authority

- No invented brand rules, personas, timelines, or performance promises.
- Treat missing creative constraints as [confirm brand asset] / [client-provided].
- Output brief only; execution belongs to media-specific skills.

## Workflow

1. Capture business objective and audience outcomes.
2. Define deliverable requirements, mandatory elements, and exclusions.
3. Document acceptance criteria, review flow, and handoff package.
4. Flag open questions before production kickoff.

## Output format
```

- Creative brief summary
- Deliverables matrix (asset | purpose | specs | owner)
- Acceptance criteria and review plan
- Open questions / dependency list
```

## Quality checks

- Brief is specific enough for execution teams without making assumptions.
- Boundaries between requirements brief and execution skills are explicit.

## Related skills

This skill defines requirements only. Use brand-context-brief-builder first if reusable context is missing. Execution belongs to website-creation-skills/web-design-brief-builder, graphic-design-creation-skills/social-graphic-concept, and print-design-skills/print-layout-brief.
