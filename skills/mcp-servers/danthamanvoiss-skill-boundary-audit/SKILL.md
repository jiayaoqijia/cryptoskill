---
name: skill-boundary-audit
description: Check nearby skills for overlap, ambiguity, or confused ownership so the suite stays easy to route.
version: 1.0.0
tags: [core, routing, audit, v1]
---

## Purpose

Audit neighboring skills or routers for overlap so each skill keeps a clear job and the router can make deterministic choices.

## Use when

- Adding, renaming, or revising a skill.
- Two skills seem too similar or are being selected interchangeably.
- You want to tighten category boundaries before release.

## Required inputs

- The skills or routers being compared.
- Their stated purposes and use cases.
- Any observed routing confusion or overlap.

## Safety/authority

- Prefer narrowing boundaries over inventing extra complexity.
- Do not merge skill responsibilities unless the overlap is real and material.
- Keep the review descriptive; do not imply file changes happened automatically.

## Workflow

1. Compare each skill's purpose, use-when section, and output type.
2. Identify whether the overlap is stage-based, category-based, or only wording-based.
3. Decide whether the best fix is clearer wording, a stronger router note, or a handoff between skills.
4. Confirm the revised boundary still supports minimal 1–3 skill stacks.
5. Return the cleanest boundary statement for each compared skill.

## Output format

```
- Skills compared: ...
- Overlap type: ...
- Clear owner for each use case: ...
- Router note needed: yes | no
- Recommended change: ...
```

## Quality checks

- The audit identifies real overlap, not cosmetic similarity.
- Each skill ends with a clear ownership statement.
- Recommendations reduce routing ambiguity.
- The result stays lightweight and static.

## Related skills

agency-router, skill-selection-guide, routing-confidence-check, catalog-maintenance-guide
