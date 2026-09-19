---
name: salesportl-account-handoff
description: Produce structured SalesPortl handoff notes as draft CRM-ready content.
version: 0.1.0
tags: [sales, crm, handoff, draft-only]
---

## Purpose
Turn sales-stage context into a structured implementation handoff draft for account teams.

## Use when
- Deal is moving from sales to delivery/client success.
- Need consistent account notes for CRM entry.

## Required inputs
- Client context, scope summary, and stakeholders.
- Known risks, commitments, and timeline targets.
- Workspace reference placeholder: [SalesPortl workspace/link].

## Safety/authority
- Draft-only output; this skill never writes to SalesPortl or third-party systems.
- No invented commitments or undocumented promises.
- Minimize personal data and include only operationally necessary details.

## Workflow
1. Summarize deal context and goals.
2. Map stakeholders, approvals, and communication cadence.
3. List delivery dependencies, open questions, and risks.
4. Format as CRM/account handoff note.

## Output format
```
- Account summary
- Stakeholders
- Scope snapshot
- Risks/open questions
- First 30-day priorities
```

## Quality checks
- All commitments trace to supplied evidence.
- Action owners and due windows are clear.
- No direct system-write instruction present.

## Related skills
proposal-scope-draft, client-onboarding-plan, monthly-client-review
