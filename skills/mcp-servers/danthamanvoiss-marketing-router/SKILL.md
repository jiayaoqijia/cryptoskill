---
name: marketing-router
description: Route marketing work to the right planning, positioning, audit, or campaign skill with concise channel-specific clarification.
version: 1.0.0
tags: [core, routing, marketing, v1]
---

## Purpose

Keep marketing work tight by separating audits, positioning, campaign planning, content planning, ad briefs, and creative requirements before downstream execution begins.

## Use when

- The main router has identified a marketing-led request.
- The user needs help choosing between strategy, planning, audit, or creative-brief marketing skills.
- A request touches channel planning but is not yet specific enough for a direct skill.

## Required inputs

- Marketing objective and target audience.
- Primary channel or campaign type [if known].
- Offer, funnel stage, and success metric [if known].

## Safety/authority

- Keep claims and performance expectations grounded in approved context.
- Do not treat planning drafts as approved launch instructions.
- Separate briefing work from execution work when the request is still early-stage.

## Workflow

1. Clarify the objective, audience, and primary channel or asset.
2. Route by need:
   - audit or funnel review: `website-marketing-audit` or `landing-page-cro-review`
   - positioning: `offer-positioning`
   - multi-channel planning: `campaign-plan`
   - publishing cadence: `content-calendar` or `social-content-ops-plan`
   - ad planning: `paid-ads-brief-draft`
   - requirements for downstream creative/media work: `creative-brief-generator`
3. Select 1–3 skills maximum and avoid mixing planning, execution, and review unless the user explicitly needs a chain.
4. Optionally pair with `anti-slop-content-review` when messaging quality is part of the deliverable.
5. If the requested skill is unavailable, use the closest same-purpose marketing alternative or ask for clarification.

## Output format

```
- Marketing objective: ...
- Channel or asset focus: ...
- Selected skills (1-3): ...
- Missing inputs: ...
- Optional quality layer: ...
- Next step prompt: ...
```

## Quality checks

- The route distinguishes planning from review from briefing.
- Only the smallest useful marketing stack is selected.
- Cross-category creative work is handed off cleanly instead of being guessed inside the marketing route.
- Unknowns are explicit.

## Related skills

agency-router, website-marketing-audit, offer-positioning, campaign-plan, content-calendar, landing-page-cro-review, paid-ads-brief-draft, social-content-ops-plan, creative-brief-generator
