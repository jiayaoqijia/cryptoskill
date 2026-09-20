---
name: crm-workflow-blueprint
description: Draft CRM workflow blueprint documentation covering lifecycle stages, owners, fields, and governance.
version: 0.1.0
tags: [core, crm, workflow, blueprint]
---

## Purpose

Draft CRM workflow blueprint documentation covering lifecycle stages, owners, fields, and governance.

## Use when

- Documenting or redesigning CRM process architecture before implementation.
- You need a blueprint artifact for review, not direct system configuration.

## Required inputs

- Current lifecycle stages, teams, and operational constraints [client-provided].
- Field/property requirements and handoff expectations.
- Business context from context/BRAND-CONTEXT.template.md and context/CLIENT-CONTEXT.template.md.

## Safety/authority

- No direct CRM writes, automations, or integration actions.
- No fabricated lifecycle metrics or conversion assumptions.
- Clearly label proposed vs currently implemented workflow elements.

## Workflow

1. Map lifecycle stages, entry/exit criteria, and owners.
2. Define required fields, update triggers, and quality controls.
3. Outline automation opportunities as draft recommendations only.
4. Produce implementation-ready blueprint and validation checklist.

## Output format
```

- CRM workflow blueprint summary
- Stage/owner/criteria map
- Field governance matrix
- Implementation checklist and risks
```

## Quality checks

- Blueprint separates current-state facts from proposed changes.
- All recommendations are documentation-only with explicit approval gates.

## Related skills

pipeline-hygiene-review, salesportl-account-handoff, client-onboarding-plan
