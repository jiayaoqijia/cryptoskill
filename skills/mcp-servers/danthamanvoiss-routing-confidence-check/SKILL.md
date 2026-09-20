---
name: routing-confidence-check
description: Sanity-check whether the selected router path and skill stack are the clearest minimal fit for the task.
version: 1.0.0
tags: [core, routing, quality, v1]
---

## Purpose

Provide a lightweight final check that the chosen route is clear, minimal, and using the right fallback behavior before downstream work begins.

## Use when

- A router has selected a skill stack and you want to verify it.
- The task was initially ambiguous or cross-functional.
- A subset-enabled subagent had to use an alternate skill.

## Required inputs

- The user task.
- The selected router path and skills.
- Any missing inputs or fallback notes already identified.

## Safety/authority

- Prefer asking one clarifying question over forcing a low-confidence route.
- Do not approve alternate-skill substitution when the stage of work changes materially.
- Preserve draft-only boundaries.

## Workflow

1. Confirm the task category and stage of work are correctly identified.
2. Check whether any selected skill is redundant or outside the smallest useful stack.
3. Review whether a direct skill, category router, or main router would be simpler.
4. Confirm that any alternate-skill substitution is genuinely close and actually available.
5. Return a confidence verdict and the smallest adjustment needed, if any.

## Output format

```
- Route reviewed: ...
- Confidence: high | medium | low
- Stack too broad?: yes | no
- Alternate-skill substitution valid?: yes | no | not-used
- Recommended adjustment: ...
```

## Quality checks

- Confidence is tied to category fit and stack size.
- Clarification is recommended when confidence is low.
- Alternate-skill use is scrutinized, not assumed.
- The result is concise enough to use inline with routing.

## Related skills

agency-router, skill-selection-guide, skill-boundary-audit
