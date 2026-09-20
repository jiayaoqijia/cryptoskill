---
name: client-success-router
description: Route onboarding, review, retention, and expansion work to the right client-success skill with concise lifecycle clarification.
version: 1.0.0
tags: [core, routing, client-success, v1]
---

## Purpose

Separate onboarding, recurring review, churn prevention, executive reporting, and expansion planning so client-success work stays stage-aware and actionable.

## Use when

- The main router has identified a post-sale or account-management request.
- The user needs help choosing the right client-success stage.
- A request could be onboarding, review, risk, or growth work and needs a tighter route.

## Required inputs

- Client-success objective and account stage.
- Known account history, risks, goals, or renewal timing [if known].
- Deliverable type requested by the user.

## Safety/authority

- Do not claim client outcomes, risks, or approvals that are not evidenced.
- Keep renewal, pricing, and expansion recommendations draft-only unless explicitly approved.
- Separate diagnostic review from upsell planning when the evidence is thin.

## Workflow

1. Clarify whether the work is onboarding, recurring review, churn prevention, executive summary, or expansion planning.
2. Select the nearest skill:
   - onboarding setup: `client-onboarding-plan`
   - routine account review: `monthly-client-review`
   - churn/risk diagnosis: `churn-risk-early-warning`
   - leadership-facing recap: `qbr-executive-summary-draft`
   - retention and growth assessment: `retention-and-upsell-review`
   - packaged expansion ideas: `service-expansion-planner`
3. Keep the route to 1–3 skills and only chain review into expansion when the user actually wants both.
4. Optionally pair with `cross-asset-consistency-check` when the deliverable includes multi-touch client messaging or decks.
5. If the exact skill is unavailable, choose the closest same-stage client-success alternative or ask for clarification.

## Output format

```
- Client-success stage: ...
- Selected skills (1-3): ...
- Missing inputs: ...
- Optional quality layer: ...
- Risk or approval notes: ...
- Next step prompt: ...
```

## Quality checks

- The route matches the account lifecycle stage.
- Review, risk, and expansion work are not merged by default.
- The selected stack is minimal.
- Unknown account evidence is stated clearly.

## Related skills

agency-router, client-onboarding-plan, monthly-client-review, churn-risk-early-warning, qbr-executive-summary-draft, retention-and-upsell-review, service-expansion-planner
