---
name: churn-risk-early-warning
description: Assess churn risk signals from supplied account data and produce early-warning mitigation drafts.
version: 0.1.0
tags: [client-success, churn, risk, read-only]
---

## Purpose

Assess churn risk signals from supplied account data and produce early-warning mitigation drafts.

## Use when

- Account health appears unstable and early intervention planning is needed.
- You must assess risk from provided evidence without inventing engagement data.

## Required inputs

- Supplied account data: delivery status, comms notes, KPI trend snapshots [client-provided].
- Contract/expectation context from context/BRAND-CONTEXT.template.md and context/CLIENT-CONTEXT.template.md.
- Known incidents, blockers, and stakeholder feedback.

## Safety/authority

- Use only supplied data; do not infer unprovided usage or sentiment metrics.
- No fabricated root-cause claims; mark uncertain hypotheses clearly.
- Output is read-only assessment and draft mitigation plan.

## Workflow

1. Compile available risk signals by category (performance, delivery, communication, trust).
2. Score confidence and severity based on evidence quality.
3. Draft near-term mitigation actions and owner suggestions.
4. List missing data required before escalation decisions.

## Output format
```

- Risk snapshot
- Signal table (signal | evidence | severity | confidence)
- Mitigation draft plan
- Missing data and escalation triggers
```

## Quality checks

- Every risk statement references supplied evidence.
- Mitigation recommendations include confidence and dependency notes.

## Related skills

monthly-client-review, retention-and-upsell-review, qbr-executive-summary-draft
