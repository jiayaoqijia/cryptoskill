---
name: brand-client-context-onboarding
description: Detect existing harness or file-based brand/client context, then fill only the missing gaps with reusable onboarding drafts.
version: 0.1.0
tags: [core, context, onboarding, portability]
---

## Purpose

Detect existing harness or file-based brand/client context, then fill only the missing gaps with reusable onboarding drafts aligned to the committed context templates.

## Use when

- A task depends on reusable brand or client context and it is unclear whether that context already exists.
- You are onboarding the agency's own brand, a specific client/project, or a test niche/alternate brand style.
- The harness may already know account or business context, but you need a repeatable context set other skills can rely on.

## Required inputs

- Target context scope: agency brand, specific client/project, or exploratory brand/niche.
- Any harness-native account, brand, client, or project context already available.
- Any existing context files, folders, approved docs, or prior briefs [if available].

## Safety/authority

- Prefer verified harness-native context and existing files before asking the user to repeat information.
- No fabricated brand claims, offers, positioning, proof, contacts, or approvals; keep placeholders such as [confirm current offer] when facts are missing.
- Output draft-only onboarding notes, file-ready drafts, and recommended locations; do not claim files were created or synced unless the harness explicitly confirms it.

## Workflow

1. Determine the target: (a) the agency's own brand, (b) a named client/project, or (c) an exploratory niche/brand style.
2. Check harness-native account/brand awareness first, then follow the most specific file path available for the target:
   - Agency-default work: `context/BRAND-CONTEXT.md`, then `context/CLIENT-CONTEXT.md`.
   - Client/project work: `context/clients/<client-slug>/BRAND-CONTEXT.md` and `context/clients/<client-slug>/CLIENT-CONTEXT.md` before falling back to shared root defaults.
   - Exploratory brand-style work: use the matching exploratory slugged folder first so test context stays separate from approved defaults.
3. Reuse any verified context already present and list only the missing gaps that still need confirmation.
4. If context is missing or incomplete, run a guided onboarding conversation using `context/BRAND-CONTEXT.template.md` and `context/CLIENT-CONTEXT.template.md`, asking the minimum necessary follow-up questions.
5. Draft reusable context outputs using this convention:
   - Agency-level context: `context/BRAND-CONTEXT.md` and `context/CLIENT-CONTEXT.md` when the agency wants one shared default set.
   - Client/project context: `context/clients/<client-slug>/BRAND-CONTEXT.md` and `context/clients/<client-slug>/CLIENT-CONTEXT.md`.
   - Exploratory niche or alternate brand style: use a distinct slugged folder under `context/clients/<client-slug>/` so it does not overwrite approved defaults.
6. If the skills are being used in another harness outside SalesPortl, keep the same context file structure so drafts can still be referenced, reviewed, or manually/procedurally updated alongside SalesPortl workflows without claiming a real integration.
7. Return the completed drafts, unresolved placeholders, and the recommended next skill(s) that should consume the context.

## Output format
```
- Target context type: agency-brand | client-project | exploratory-brand-style
- Context sources found: harness-native | root context files | client folder | none
- Reused verified context: ...
- Missing fields still needed: ...
- Recommended file locations: ...
- Brand context draft: ...
- Client context draft: ...
- Suggested next skills: ...
```

## Quality checks

- Existing harness/account context is reused before new questions are asked.
- Agency, client, and exploratory contexts are kept distinct and do not overwrite each other.
- Drafts follow the committed templates and preserve placeholders for unverified facts.
- Cross-harness guidance stays conceptual only and does not imply a live API or automation.

## Related skills

agency-router, context-loader, brand-context-brief-builder, output-organization-guide, cross-harness-collaboration-notes
