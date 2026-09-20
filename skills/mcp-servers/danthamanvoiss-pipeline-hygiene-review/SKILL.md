---
name: pipeline-hygiene-review
description: Review pipeline records for stage accuracy, stale deals, missing fields, and next-action clarity.
version: 0.1.0
tags: [sales, pipeline, crm, read-only]
---

## Purpose

Review pipeline records for stage accuracy, stale deals, missing fields, and next-action clarity.

## Use when

- Pipeline visibility is unclear and stages/next steps may be outdated.
- You need a read-only cleanup plan before any CRM updates are made by humans.

## Required inputs

- Current pipeline export or summary [client-provided].
- Stage definitions and SLA expectations from context/BRAND-CONTEXT.template.md and context/CLIENT-CONTEXT.template.md.
- Any required CRM fields and owner assignments.

## Safety/authority

- No direct CRM edits; produce draft recommendations only.
- No invented deal activity, revenue, or probability values.
- Flag missing/ambiguous data explicitly.

## Workflow

1. Check each opportunity against stage criteria and recency thresholds.
2. Identify missing required fields, ambiguous owners, and stalled records.
3. Recommend disposition actions (advance, hold, nurture, close-lost pending validation).
4. Prioritize cleanup tasks by impact and urgency.

## Output format
```

- Pipeline hygiene summary
- Issue table (record | issue | evidence | suggested action)
- Prioritized cleanup queue
- Data gaps to resolve
```

## Quality checks

- All flags trace to supplied pipeline evidence.
- Recommended actions map to defined stage/SLA rules.

## Related skills

crm-workflow-blueprint, lead-qualification, salesportl-account-handoff
