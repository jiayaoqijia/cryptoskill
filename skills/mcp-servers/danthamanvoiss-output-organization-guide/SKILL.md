---
name: output-organization-guide
description: Guide where drafts and reusable outputs should conceptually live across agency, client, and exploratory work.
version: 0.1.0
tags: [core, organization, context, workflow]
---

## Purpose

Provide lightweight guidance on where generated drafts, reusable context, and one-off exploratory outputs conceptually belong so multi-client work stays organized.

## Use when

- A skill is producing reusable context, briefs, plans, or draft deliverables.
- The suite is being used across many clients, projects, or exploratory niches.
- You want outputs to stay consistent with the shared `context/clients/<client-slug>/` convention.

## Required inputs

- The target work type: agency-level, client/project-specific, or exploratory.
- The client slug or working label [if available].
- Whether the output is reusable context, a working draft, or a one-off experiment.

## Safety/authority

- Keep confidential client information in private, uncommitted context or working files.
- Do not overwrite approved shared context when the work is exploratory or client-specific.
- Recommend organization patterns only; do not imply that folders or files were actually created.

## Workflow

1. Determine whether the output belongs to the agency default context, a specific client/project, or an exploratory branch of work.
2. Place reusable agency-wide context at the root `context/` level only when it is meant to be a shared default.
3. Place client-specific reusable context under `context/clients/<client-slug>/`, including `BRAND-CONTEXT.md` and `CLIENT-CONTEXT.md` for that client/project.
4. Keep client deliverables, briefs, and work-in-progress grouped with that same client slug whenever the harness supports file organization.
5. Keep exploratory or test-brand work in its own slugged client-style folder so it does not overwrite approved agency or live-client defaults.
6. When handing work to another skill or harness, include the intended storage location in the handoff so outputs stay easy to find.

## Output format
```
- Work type: agency-default | client-project | exploratory
- Recommended location: ...
- Why this location fits: ...
- Reusable context files involved: ...
- Draft/output grouping notes: ...
```

## Quality checks

- Shared defaults, client work, and exploratory work stay separated.
- The `context/clients/<client-slug>/` convention is used consistently for client/project context.
- Recommendations stay lightweight and portable across harnesses.
- No claim is made that organization changes were executed automatically.

## Related skills

brand-client-context-onboarding, context-loader, skill-handoff-protocol, cross-harness-collaboration-notes
