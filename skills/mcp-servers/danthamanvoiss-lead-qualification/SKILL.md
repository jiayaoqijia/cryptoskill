---
name: lead-qualification
description: Run BANT/MEDDIC-inspired qualification with evidence vs unknown separation.
version: 0.1.0
tags: [sales, qualification, bant, meddic]
---

## Purpose
Assess lead quality using evidence-backed qualification criteria and recommend next action.

## Use when
- A new lead or referral needs prioritization.
- Pipeline review requires clear fit/confidence scoring.

## Required inputs
- Lead/account details supplied by user.
- Current offer scope from brand context.
- Any known timeline, budget, or decision process notes.

## Safety/authority
- No fabricated prospect facts.
- No legal, financial, or guaranteed-outcome claims.
- If data is missing, mark unknown instead of guessing.

## Workflow
1. Map evidence to BANT/MEDDIC-style dimensions.
2. Separate known evidence from assumptions and unknowns.
3. Identify blockers, risks, and required discovery questions.
4. Recommend qualification status and next step.

## Output format
```
- Qualification summary
- Evidence table (criterion | evidence | confidence)
- Unknowns to validate
- Recommendation: pursue | nurture | disqualify
- Next questions
```

## Quality checks
- Every claim has supporting input or is marked unknown.
- Recommendation aligns with evidence quality.

## Related skills
discovery-call-prep, proposal-scope-draft, salesportl-account-handoff
