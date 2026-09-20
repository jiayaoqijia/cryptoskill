---
name: release-readiness-check
description: Confirm a skill, router change, or catalog update is clear, complete, and ready to ship in the static suite.
version: 1.0.0
tags: [core, release, quality, v1]
---

## Purpose

Provide a short release-hardening review so new or changed skills are ready for a stable static-library release without adding heavy process.

## Use when

- Preparing a versioned release of the suite.
- Reviewing new or changed skills before publishing.
- Checking whether docs, routing, and catalog updates are aligned.

## Required inputs

- The changed skills or docs under review.
- The intended release version.
- Any known open questions or follow-up items.

## Safety/authority

- Flag missing clarity or overlap instead of assuming it is acceptable.
- Do not claim release readiness if validation or catalog alignment is still unresolved.
- Keep recommendations procedural and lightweight.

## Workflow

1. Check that the changed skills have clear purpose, use-when boundaries, and related-skill links.
2. Confirm router guidance still prefers minimal skill stacks and clear fallback behavior.
3. Verify docs, catalog entries, and release version references are aligned.
4. Confirm the validation commands and any release-count expectations are up to date.
5. Return a short ready/not-ready summary with only the blocking gaps that still matter.

## Output format

```
- Release target: ...
- Areas reviewed: ...
- Ready status: ready | needs-fixes
- Blocking gaps: ...
- Non-blocking notes: ...
- Recommended next step: ...
```

## Quality checks

- The review focuses on ship-readiness rather than stylistic noise.
- Router, docs, and catalog alignment are all checked.
- Blocking gaps are clearly separated from optional polish.
- The result stays concise.

## Related skills

catalog-maintenance-guide, routing-confidence-check, skill-boundary-audit, v1-launch-checklist
