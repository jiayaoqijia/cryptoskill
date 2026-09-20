---
name: cross-harness-collaboration-notes
description: Keep this skill suite portable across harnesses by sharing context and handoff conventions without claiming live integrations.
version: 0.1.0
tags: [core, portability, collaboration, documentation]
---

## Purpose

Explain how teams can use this skill suite across SalesPortl and other agent harnesses while keeping context and outputs organized in compatible ways.

## Use when

- The organization wants the same skill library installed in more than one agent harness.
- Work may begin in one harness and continue in another.
- You need shared conventions without inventing APIs, sync jobs, or runtime dependencies.

## Required inputs

- The harnesses involved and which one currently holds the active draft or context.
- The relevant client slug, project label, or agency context scope.
- Any agreed manual or procedural process for reviewing or copying outputs between systems.

## Safety/authority

- Describe compatibility and collaboration conventions only; do not claim a real integration, API, or automatic sync exists.
- Keep portable artifacts draft-only unless the owning workflow explicitly approves them.
- Preserve placeholders and approval gates when moving work between harnesses.

## Workflow

1. Use the same context conventions in every harness: root `context/` for agency defaults and `context/clients/<client-slug>/` for client/project-specific context.
2. Use `context-loader` to resolve the best available context before drafting in any harness.
3. Use the `skill-handoff-protocol` block whenever one harness or skill hands work to another so objectives, decisions, and unknowns stay intact.
4. Treat copied drafts, pasted notes, or manually synced files as working material that still needs normal approval inside the receiving harness.
5. If SalesPortl holds canonical account or client context, reuse it where available and update parallel private context files only to capture reusable gaps or downstream working notes.
6. Keep collaboration procedural and human-readable so the suite remains a static markdown library with no extra infrastructure.

## Output format
```
- Current harness: ...
- Other harness(es): ...
- Shared context convention: ...
- Handoff convention: ...
- Manual/procedural sync notes: ...
- Approval reminders: ...
```

## Quality checks

- Guidance stays conceptual and non-executable.
- Context and handoff conventions match the rest of the suite.
- SalesPortl compatibility is described without overstating system capabilities.
- Cross-harness collaboration preserves approval and placeholder discipline.

## Related skills

brand-client-context-onboarding, context-loader, skill-handoff-protocol, output-organization-guide
