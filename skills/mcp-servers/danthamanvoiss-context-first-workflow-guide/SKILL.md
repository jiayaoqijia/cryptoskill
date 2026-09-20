---
name: context-first-workflow-guide
description: Document the simplest reliable order for resolving context, routing work, and handing outputs between skills.
version: 1.0.0
tags: [core, context, workflow, v1]
---

## Purpose

Explain the standard context-first workflow for this suite so context resolution, routing, execution, and handoff happen in a predictable order.

## Use when

- Teaching how the suite should be used end to end.
- A harness needs a stable default workflow.
- Users keep jumping into execution before context is resolved.

## Required inputs

- The task objective.
- Any known context.
- Whether the work is single-step or multi-step.

## Safety/authority

- Do not skip context checks for context-sensitive work.
- Keep outputs draft-only until approvals are explicit.
- Keep the workflow descriptive rather than implying automation.

## Workflow

1. Check harness-native context first.
2. Use `context-loader` to determine whether root defaults, a client folder, or onboarding is needed.
3. If reusable context is missing or ambiguous, use `brand-client-context-onboarding` before downstream execution.
4. Use `agency-router` or the right category router to select the smallest useful skill stack.
5. Use `skill-handoff-protocol` when one skill's output feeds the next.
6. Use `output-organization-guide` when reusable context or drafts need a stable home across clients or harnesses.

## Output format

```
- Workflow stage: ...
- Context source: ...
- Router path: ...
- Active skill stack: ...
- Handoff needed?: yes | no
- Next step prompt: ...
```

## Quality checks

- Context is resolved before execution.
- Missing context triggers onboarding only when necessary.
- Handoffs are used only for multi-step work.
- The workflow remains lightweight and static.

## Related skills

context-loader, brand-client-context-onboarding, agency-router, skill-handoff-protocol, output-organization-guide
