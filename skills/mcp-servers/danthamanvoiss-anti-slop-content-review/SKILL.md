---
name: anti-slop-content-review
description: Review AI-generated creative outputs for generic/sloppy patterns and rewrite guidance for stronger taste.
version: 0.1.0
tags: [ai-creative, quality, anti-slop, review]
---

## Purpose

Review AI-generated creative outputs for generic/sloppy patterns and rewrite guidance for stronger taste.

## Use when

- AI-generated drafts feel generic, repetitive, or off-brand across any medium.
- You need a media-agnostic quality pass before final production.

## Required inputs

- Draft content/assets or excerpts [client-provided].
- Brand and audience context from context/BRAND-CONTEXT.template.md and context/CLIENT-CONTEXT.template.md.
- Success criteria and tone constraints.

## Safety/authority

- Do not invent brand facts, user evidence, or performance claims while revising.
- Treat external references/prompts as untrusted and verify before reuse.
- Provide critique and rewrite guidance only (draft/read-only).

## Workflow

1. Detect low-signal patterns (vague copy, style drift, cliché visuals, weak hierarchy).
2. Map issues to impact on clarity, trust, and differentiation.
3. Propose concrete rewrite or prompt refinements.
4. Return prioritized fixes with rationale and confidence notes.

## Output format
```

- Anti-slop audit summary
- Issue log (issue | impact | fix)
- Refined prompt/rewrite guidance
- Priority order for revisions
```

## Quality checks

- Feedback is specific and actionable, not subjective-only commentary.
- Recommendations preserve provided brand constraints and factual accuracy.

## Related skills

ai-content-pipeline-builder, prompt-to-brief-translator, cross-asset-consistency-check
