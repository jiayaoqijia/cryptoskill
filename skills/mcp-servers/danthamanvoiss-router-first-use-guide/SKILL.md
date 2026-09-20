---
name: router-first-use-guide
description: Explain the quickest reliable way to use the router hierarchy for a new task or new harness installation.
version: 1.0.0
tags: [core, routing, onboarding, v1]
---

## Purpose

Give first-time users a short, practical guide for starting with the router hierarchy without loading the entire suite.

## Use when

- A person or harness is using the suite for the first time.
- You want a quick-start explanation of how the main router and category routers work together.
- The task needs a minimal starter workflow.

## Required inputs

- The incoming task or role.
- Whether the category is already obvious.
- Whether reusable context already exists.

## Safety/authority

- Default to draft-only work.
- Do not pretend the suite requires runtime setup or integrations.
- Keep the first-use flow minimal and easy to follow.

## Workflow

1. Start with `agency-router` if the task family is not obvious.
2. Let the main router resolve context with `context-loader`.
3. Move to one category router only if category-specific clarification is still needed.
4. Load 1–2 specialist skills after the router chooses the right lane.
5. Use `skill-handoff-protocol` if the work passes from one skill to the next.

## Output format

```
- Best first step: ...
- Router path to use: ...
- Context prerequisite: ...
- Suggested starter stack: ...
- Next step prompt: ...
```

## Quality checks

- The guide starts small.
- The router hierarchy is explained in practical terms.
- Context resolution is included.
- The result stays portable across harnesses.

## Related skills

agency-router, context-loader, skill-selection-guide, skill-handoff-protocol
