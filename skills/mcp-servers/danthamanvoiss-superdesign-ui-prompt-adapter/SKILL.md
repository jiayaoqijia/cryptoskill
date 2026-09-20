---
name: superdesign-ui-prompt-adapter
description: Convert approved web requirements into reusable UI prompt scaffolds inspired by superdesign prompt patterns.
version: 0.1.0
tags: [website, prompting, ui-spec, superdesign-inspired]
---

## Purpose

Convert approved web requirements into reusable UI prompt scaffolds inspired by superdesign prompt patterns.

## Use when

- Requirements are already defined and you need high-fidelity UI prompt specifications for generation/iteration.
- You are generating prompt-specs, not collecting baseline requirements.

## Required inputs

- Approved web requirements brief (often from web-design-brief-builder).
- Brand/client context from context/BRAND-CONTEXT.template.md and context/CLIENT-CONTEXT.template.md.
- Design references and constraints [client-provided].

## Safety/authority

- Do not copy upstream prompt text verbatim; generate original proprietary scaffolds.
- No invented brand traits, product claims, or inaccessible style directives.
- Output prompt-spec drafts only, with verification placeholders as needed.

## Workflow

1. Extract non-negotiable requirements and style constraints from approved brief.
2. Compose modular prompt scaffold blocks (layout, typography, spacing, interactions, QA criteria).
3. Add anti-slop/taste checks and fallback instructions for missing assets.
4. Return reusable prompt variants for iteration contexts.

## Output format
```

- Prompt adapter summary
- Reusable UI prompt scaffold(s)
- Constraint and fallback map
- QA checklist for generated outputs
```

## Quality checks

- Prompt specs remain traceable to approved requirements and context templates.
- Use-when boundary stays distinct from requirements gathering skill.

## Related skills

web-design-brief-builder, anti-slop-content-review, landing-page-wireframe-draft
