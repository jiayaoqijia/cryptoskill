---
name: catalog-maintenance-guide
description: Keep catalog entries, paths, versions, categories, and counts aligned when the static skill library changes.
version: 1.0.0
tags: [core, catalog, maintenance, v1]
---

## Purpose

Document the lightweight maintenance rules that keep `catalog.json`, skill paths, and release validation aligned as the suite evolves.

## Use when

- Adding, removing, or renaming skills.
- Preparing a release version bump.
- Investigating catalog drift or validator failures.

## Required inputs

- The skill changes being made.
- The target release version.
- Current catalog and validator expectations.

## Safety/authority

- Keep the catalog as the source of truth for the published inventory.
- Do not bump counts or versions without updating the matching validation expectations.
- Avoid adding heavy validation rules unless they solve a real release problem.

## Workflow

1. Add or update the skill file first, then mirror the change in `catalog.json`.
2. Keep each entry aligned on name, module, category, scope, version, tags, and path.
3. Update release-level catalog metadata such as `version` and `total_skills`.
4. Adjust validator/test expected totals only when the release count genuinely changes.
5. Re-run the existing validation commands and fix drift before publishing.

## Output format

```
- Catalog action: add | update | remove | rename
- Skills affected: ...
- Release metadata changes: ...
- Validator alignment needed: ...
- Validation commands to run: ...
```

## Quality checks

- Catalog changes match the actual skill files.
- Versioned count expectations stay aligned.
- Category and scope discipline are preserved.
- The maintenance guidance stays dependency-free.

## Related skills

release-readiness-check, skill-boundary-audit, v1-launch-checklist
