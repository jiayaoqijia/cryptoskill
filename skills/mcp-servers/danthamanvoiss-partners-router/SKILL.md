---
name: partners-router
description: Route partner, affiliate, and referral-program work to the right enablement skill with simple program-stage clarification.
version: 1.0.0
tags: [core, routing, partners, v1]
---

## Purpose

Keep partner work simple by separating affiliate enablement from referral-program activation so the suite picks the right partner workflow quickly.

## Use when

- The main router has identified a partners or channel-growth request.
- The user wants help with affiliates, partners, or referrals but has not named the exact skill.
- The task should stay inside the partner family.

## Required inputs

- Partner-program objective.
- Whether the work is affiliate-facing or referral-program-facing.
- Audience, offer, and any launch constraints [if known].

## Safety/authority

- Do not promise payouts, terms, or partnership approvals that are not verified.
- Treat outreach or launch assets as draft-only until approved.
- Keep the route narrow; do not pull sales or marketing skills unless the user explicitly wants a mixed workflow.

## Workflow

1. Clarify whether the goal is affiliate enablement or referral-program activation.
2. Route to:
   - `affiliate-enablement` for recruiting, briefing, and enabling affiliates
   - `referral-program-activation` for standing up or refreshing a referral motion
3. Select only one partner skill unless the user clearly needs both in sequence.
4. Optionally pair with `anti-slop-content-review` when partner-facing copy quality is part of the deliverable.
5. If the requested skill is unavailable, use the closest partner alternative or ask for clarification.

## Output format

```
- Partner motion: ...
- Selected skills (1-3): ...
- Missing inputs: ...
- Optional quality layer: ...
- Next step prompt: ...
```

## Quality checks

- Affiliate and referral work are kept distinct.
- The stack stays minimal.
- Unverified program terms are not invented.
- Cross-category pairing is only added when clearly requested.

## Related skills

agency-router, affiliate-enablement, referral-program-activation, anti-slop-content-review
