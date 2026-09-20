---
name: prompt-to-brief-translator
description: Translate loose prompts into structured creative briefs with requirements, constraints, and acceptance criteria.
version: 0.1.0
tags: [ai-creative, briefing, prompting, requirements]
---

## Purpose

Translate loose prompts into structured creative briefs with requirements, constraints, and acceptance criteria.

## Use when

- Input arrives as messy prompt ideas and must become a reusable production brief.
- You need requirements clarity before any medium-specific creation starts.

## Required inputs

- Raw prompt/input request [client-provided].
- Brand/client context from context/BRAND-CONTEXT.template.md and context/CLIENT-CONTEXT.template.md.
- Known delivery channel constraints and review criteria.

## Safety/authority

- No invented constraints, personas, or performance outcomes.
- Mark unresolved requirements with placeholders like [confirm brand asset].
- Output brief draft only; no direct generation commitment.

## Workflow

1. Parse intent, audience, and desired outcomes from raw prompt.
2. Normalize into brief sections: goals, constraints, tone, deliverables, acceptance tests.
3. Identify ambiguities and ask clarifying questions.
4. Provide final structured brief plus optional prompt scaffold.

## Output format
```

- Normalized brief
- Assumptions/unknowns register
- Clarification questions
- Optional prompt scaffold
```

## Quality checks

- Brief resolves ambiguity while preserving original intent.
- Unknowns and assumptions are explicit before downstream use.

## Related skills

creative-brief-generator, ai-content-pipeline-builder, web-design-brief-builder
