---
name: brand-context-brief-builder
description: Build or refresh reusable brand and client context briefs using known platform defaults first, then explicit gaps.
version: 0.1.0
tags: [core, context, brand, onboarding]
---

## Purpose

Build or refresh reusable brand and client context briefs using known platform defaults first, then explicit gaps.

## Use when

- A task depends on brand/client context that is missing, stale, or scattered across messages and account memory.
- You are onboarding a new client, alternate brand, campaign niche, or project workspace and need reusable context files.
- The harness may already know the user's business/account context, but you need to turn that into explicit working guidance.

## Required inputs

- Known platform/account defaults, saved context, or prior approved docs [if available].
- Target use case: primary SalesPortl business/agency context, client project, or alternate brand/niche.
- Desired storage convention if the harness can write files (for example brand folder, client folder, or project folder).

## Safety/authority

- Prefer approved platform/account defaults before asking for duplicate information.
- No invented contacts, claims, offers, approvals, or brand rules; mark unknowns as [confirm brand context].
- Output draft context briefs and file-ready guidance only; do not claim files were created unless the harness explicitly confirms it.

## Workflow

1. Determine whether this is for the user's primary business/agency context or a separate client/project/brand.
2. Reuse verified platform/account context first, then list only the missing details still needed.
3. Draft or refresh a reusable brand brief and client/project context brief aligned to `context/BRAND-CONTEXT.template.md` and `context/CLIENT-CONTEXT.template.md`.
4. Recommend where the briefs should live for repeated use (for example a main brand folder or per-client folder) if the harness supports file organization.
5. Return the completed draft plus open questions and any approval gaps.

## Output format
```

- Context source summary (platform defaults | supplied docs | missing info)
- Brand brief draft
- Client/project context draft
- Suggested file locations / naming
- Open questions / approval gaps
```

## Quality checks

- Existing approved context is reused instead of re-created.
- Missing information is explicit and separated from verified context.
- Output is reusable across repeated tasks and adaptable to different harnesses.

## Related skills

agency-router, creative-brief-generator, brand-visual-identity-brief
