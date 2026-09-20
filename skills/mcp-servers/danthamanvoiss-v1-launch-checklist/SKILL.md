---
name: v1-launch-checklist
description: Provide a concise go-live checklist for publishing the suite as a stable v1.0.0 release.
version: 1.0.0
tags: [core, release, checklist, v1]
---

## Purpose

Capture the minimum final checks needed to publish this suite as a stable v1 release without turning launch prep into a heavyweight process.

## Use when

- Finalizing the v1.0.0 release.
- Running a last-pass go-live review.
- Coordinating docs, routing, and catalog completion before publish.

## Required inputs

- Current release version and catalog state.
- Validation status.
- Any known open issues or review comments.

## Safety/authority

- Do not mark launch-ready while blockers remain unresolved.
- Keep the checklist factual and release-focused.
- Separate blocking issues from nice-to-have polish.

## Workflow

1. Confirm router hierarchy, docs, catalog, and validation are all aligned to the target release.
2. Check that context-first workflow guidance and handoff conventions are documented.
3. Verify there are no unresolved critical overlap or routing-confidence concerns.
4. Confirm the published inventory count and version are correct.
5. Return a short launch-ready checklist with only the necessary next actions.

## Output format

```
- Release version: ...
- Launch-ready items complete: ...
- Remaining blockers: ...
- Remaining polish: ...
- Final go-live recommendation: ...
```

## Quality checks

- The checklist is short and actionable.
- Routing, context, docs, and catalog are all represented.
- Blocking issues are explicit.
- The result is suitable for a final publish pass.

## Related skills

release-readiness-check, catalog-maintenance-guide, routing-confidence-check
