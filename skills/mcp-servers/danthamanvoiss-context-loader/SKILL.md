---
name: context-loader
description: Resolve the best available harness, agency, or client context before running downstream skills.
version: 0.1.0
tags: [core, context, routing, portability]
---

## Purpose

Define the standard context-resolution procedure other skills should follow before they begin drafting, reviewing, or planning work.

## Use when

- A downstream skill depends on brand, client, project, or account context.
- It is unclear whether the harness already knows the needed context.
- You want a consistent, lightweight way to decide whether to proceed, ask clarifying questions, or trigger onboarding first.

## Required inputs

- The current task objective and whether it is agency-level, client/project-specific, or exploratory.
- Any harness-native account, brand, client, or project context already available.
- Any known client slug, workspace name, or folder hint [if available].

## Safety/authority

- Treat harness-native context and existing files as preferred evidence, not as permission to invent missing details.
- If context remains ambiguous, say so explicitly and keep outputs draft-only.
- Do not claim files were loaded, created, or updated unless the harness explicitly confirms that capability.

## Workflow

1. Identify the target context scope: agency default, specific client/project, or exploratory brand style.
2. Check harness-native context first (account memory, known business profile, client/workspace metadata, or other built-in awareness).
3. If the task is agency-level, look next for `context/BRAND-CONTEXT.md` and `context/CLIENT-CONTEXT.md` as the default reusable pair.
4. If the task is for a specific client/project, check `context/clients/<client-slug>/BRAND-CONTEXT.md` and `context/clients/<client-slug>/CLIENT-CONTEXT.md` before falling back to the root defaults.
5. If the task is exploratory, check `context/clients/<client-slug>/BRAND-CONTEXT.md` and `context/clients/<client-slug>/CLIENT-CONTEXT.md` for an existing exploratory slug before falling back to the root defaults.
6. Prefer the most specific verified context available and note any conflicts between harness-native context, root files, and client-folder files.
7. If no sufficient context is found, invite the user to run `brand-client-context-onboarding` before continuing, or proceed only with explicitly generic placeholders if the user wants exploratory output.
8. Pass downstream skills a short summary of which context source was used, which facts were confirmed, and which fields remain unknown.

## Output format
```
- Task scope: agency-default | client-project | exploratory
- Context source selected: harness-native | root context files | client folder | none
- Confirmed context available: ...
- Conflicts or ambiguities: ...
- Missing context still needed: ...
- Recommended next step: proceed | ask clarifying question | run brand-client-context-onboarding
```

## Quality checks

- Harness-native context is checked before file-based fallbacks.
- Client-specific context is preferred over shared defaults when the task is client-specific.
- Unknowns and conflicts are explicit so downstream skills do not over-assume.
- The recommendation stays lightweight and procedural rather than pretending to perform file I/O.

## Related skills

agency-router, brand-client-context-onboarding, brand-context-brief-builder, skill-handoff-protocol
