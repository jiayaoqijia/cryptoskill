---
name: skill-selection-guide
description: Help users and harnesses choose the smallest useful combination of router and direct skills for a task.
version: 1.0.0
tags: [core, routing, guidance, v1]
---

## Purpose

Provide a concise decision guide for choosing between the main router, a category router, or a direct specialist skill without loading unnecessary overlap.

## Use when

- A user or harness is unsure where to start.
- You want a quick rule set for loading only the necessary skills.
- The task may be simple enough for a direct skill or broad enough to need routing first.

## Required inputs

- The task objective.
- Whether the category is already known.
- Whether context is complete, partial, or missing.

## Safety/authority

- Prefer clarification over guessing when the category or context is unclear.
- Do not load extra skills just because they seem related.
- Keep any external action outputs draft-only unless explicitly approved.

## Workflow

1. Start with `agency-router` when the category is unclear, the task is cross-functional, or the harness has only a subset of skills enabled.
2. Start with a category router when the family is obvious but the exact specialist skill is not.
3. Start with a direct specialist skill only when the task, context, and required stage of work are already clear.
4. Use `context-loader` before downstream work when brand, client, or project context matters.
5. Keep the active stack to 1–3 skills and add an AI-creative quality layer only when it clearly improves the result.

## Output format

```
- Recommended entrypoint: agency-router | category router | direct specialist skill
- Why this entrypoint fits: ...
- Suggested skill stack size: 1 | 2 | 3
- Context prerequisite: ...
- Next step prompt: ...
```

## Quality checks

- The guide points to the smallest useful entrypoint.
- Context-sensitive work references `context-loader`.
- Category routing is used only when it adds clarity.
- The result stays simple and portable.

## Related skills

agency-router, context-loader, routing-confidence-check, router-first-use-guide
