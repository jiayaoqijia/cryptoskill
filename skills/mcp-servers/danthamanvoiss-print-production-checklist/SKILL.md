---
name: print-production-checklist
description: Provide read-only print production QA checklist for prepress readiness and handoff verification.
version: 0.1.0
tags: [print, production, checklist, read-only]
---

## Purpose

Provide read-only print production QA checklist for prepress readiness and handoff verification.

## Use when

- A print file package needs preflight verification before sending to production.
- You need quality/control checklist guidance, not print execution.

## Required inputs

- Print file specs and handoff package details [client-provided].
- Project context from context/BRAND-CONTEXT.template.md and context/CLIENT-CONTEXT.template.md.
- Printer requirements for bleed, CMYK, DPI, trim/safe zones, and finishing.

## Safety/authority

- Read-only checklist only; no direct print ordering or file transmission actions.
- No assumption that files pass unless evidence is supplied.
- Flag unknown specs as required confirmations before release.

## Workflow

1. Verify technical prepress criteria (bleed, trim, safe area, CMYK, DPI, embedding, overprint).
2. Check finishing/production metadata (stock, coating, folds, dieline alignment).
3. Validate content/legal elements and approval signatures.
4. Return pass/hold findings with remediation steps.

## Output format
```

- Preflight summary (pass/hold)
- Checklist table (item | status | evidence | action)
- Critical blockers
- Final handoff confirmation prompts
```

## Quality checks

- Checklist covers bleed/CMYK/DPI/finishing requirements explicitly.
- Statuses are evidence-based and unresolved items remain hold state.

## Related skills

print-layout-brief, packaging-design-brief, cross-asset-consistency-check
