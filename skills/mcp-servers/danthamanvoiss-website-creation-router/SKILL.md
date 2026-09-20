---
name: website-creation-router
description: Route website creation work to the right web brief, wireframe, audit, motion, or prompt-adapter skill.
version: 1.0.0
tags: [core, routing, website, creative, v1]
---

## Purpose

Separate website requirements, wireframing, design-system review, motion concepts, and prompt adaptation so web work stays clean and stage-specific.

## Use when

- The main router has identified a website or landing-page creation request.
- The user needs help picking the right web-creation skill.
- A request is clearly web-focused but still needs web-specific clarification.

## Required inputs

- Website objective and page or experience type.
- Brand/context status and any approved requirements [if known].
- Whether the user needs a brief, structure, audit, motion concept, or prompt specification.

## Safety/authority

- Do not invent requirements, UX evidence, or implementation commitments.
- Keep execution recommendations draft-only unless approved.
- Use the briefing step first when requirements are still unclear.

## Workflow

1. Clarify the page type, objective, and stage of work.
2. Route to:
   - requirements intake: `web-design-brief-builder`
   - structural page concept: `landing-page-wireframe-draft`
   - current-system review: `ui-design-system-audit`
   - motion or interaction concepts: `web-animation-microinteraction-concept`
   - prompt-spec adaptation from approved requirements: `superdesign-ui-prompt-adapter`
3. Keep the stack to 1–3 skills, usually one planning skill plus one optional support layer.
4. Optionally pair with `ai-creative-router` or `cross-asset-consistency-check` when the website work must align with broader asset systems.
5. If the exact skill is unavailable, use the closest same-stage website alternative or ask for clarification.

## Output format

```
- Website task stage: ...
- Selected skills (1-3): ...
- Missing inputs: ...
- Optional support layer: ...
- Next step prompt: ...
```

## Quality checks

- Briefing, wireframing, auditing, and prompt adaptation remain separate.
- The route stays stage-specific.
- Multi-asset alignment is optional, not default.
- Unknown requirements are made explicit.

## Related skills

agency-router, web-design-brief-builder, landing-page-wireframe-draft, ui-design-system-audit, web-animation-microinteraction-concept, superdesign-ui-prompt-adapter, ai-creative-router
