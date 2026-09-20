---
name: print-design-router
description: Route print collateral and packaging work to the right brief or checklist skill with lightweight production clarification.
version: 1.0.0
tags: [core, routing, print, creative, v1]
---

## Purpose

Keep print work reliable by separating layout briefing, packaging design requirements, and production preflight review.

## Use when

- The main router has identified a print or packaging request.
- The user needs help choosing the correct print-design skill.
- The task should remain inside the print family.

## Required inputs

- Asset type, dimensions or format [if known], and business objective.
- Whether the work is a new brief or a preflight review.
- Any production, compliance, or vendor constraints [if known].

## Safety/authority

- Do not claim print-readiness, compliance approval, or vendor acceptance unless verified.
- Keep production-direction outputs draft-only until approved.
- Surface missing specifications instead of guessing them.

## Workflow

1. Clarify whether the work is collateral layout, packaging-specific design planning, or preflight review.
2. Route to:
   - print collateral layout planning: `print-layout-brief`
   - packaging-specific requirements: `packaging-design-brief`
   - final review checklist: `print-production-checklist`
3. Keep the route to 1–2 skills unless the user clearly wants both planning and preflight.
4. Optionally pair with `cross-asset-consistency-check` when print pieces must match other approved assets.
5. If the exact skill is unavailable, use the closest same-stage print alternative or ask for clarification.

## Output format

```
- Print task stage: ...
- Selected skills (1-3): ...
- Missing specs: ...
- Optional support layer: ...
- Next step prompt: ...
```

## Quality checks

- Layout, packaging, and preflight work are clearly separated.
- Missing specs are called out instead of invented.
- The route stays minimal.
- Cross-asset alignment is optional.

## Related skills

agency-router, print-layout-brief, packaging-design-brief, print-production-checklist, cross-asset-consistency-check
