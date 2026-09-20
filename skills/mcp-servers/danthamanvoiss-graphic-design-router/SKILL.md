---
name: graphic-design-router
description: Route graphic-design requests to the right identity, social-graphic, or icon/illustration skill with simple asset clarification.
version: 1.0.0
tags: [core, routing, graphic-design, creative, v1]
---

## Purpose

Keep graphic-design work concise by separating identity-system work, social-graphic concepts, and icon or illustration briefs.

## Use when

- The main router has identified a graphic-design request.
- The user needs a design concept but has not specified the exact design family skill.
- The request is visual but not specifically web, video, or print production.

## Required inputs

- Asset type and business objective.
- Audience, brand direction, and channel [if known].
- Whether the work is identity, campaign/social, or icon/illustration focused.

## Safety/authority

- Do not claim brand approvals, final artwork, or production readiness unless explicitly confirmed.
- Keep concept outputs draft-only.
- Separate broad identity direction from one-off campaign asset concepts.

## Workflow

1. Clarify the asset type and whether the request is identity, social, or illustration focused.
2. Route to:
   - brand system direction: `brand-visual-identity-brief`
   - campaign/social concepting: `social-graphic-concept`
   - icons or illustration briefing: `icon-illustration-brief`
3. Keep the route to 1–2 skills unless the user explicitly wants an identity-to-campaign chain.
4. Optionally pair with `cross-asset-consistency-check` when the design output must align with other asset families.
5. If the exact skill is unavailable, use the closest same-purpose design alternative or ask for clarification.

## Output format

```
- Graphic-design focus: ...
- Selected skills (1-3): ...
- Missing inputs: ...
- Optional support layer: ...
- Next step prompt: ...
```

## Quality checks

- Identity, campaign graphic, and illustration requests stay distinct.
- The route remains minimal.
- Alignment layers are optional.
- Missing brand direction is surfaced clearly.

## Related skills

agency-router, brand-visual-identity-brief, social-graphic-concept, icon-illustration-brief, cross-asset-consistency-check
