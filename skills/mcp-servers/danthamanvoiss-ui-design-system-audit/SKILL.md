---
name: ui-design-system-audit
description: Audit existing UI design system consistency across tokens, components, accessibility, and interaction patterns.
version: 0.1.0
tags: [website, design-system, audit, read-only]
---

## Purpose

Audit existing UI design system consistency across tokens, components, accessibility, and interaction patterns.

## Use when

- An existing web UI needs consistency and governance review before redesign/scale.
- You need read-only findings rather than new system creation.

## Required inputs

- Current UI references, component inventory, or screenshots [client-provided].
- Brand constraints from context/BRAND-CONTEXT.template.md and context/CLIENT-CONTEXT.template.md.
- Accessibility and platform standards in scope.

## Safety/authority

- No implementation changes; audit findings only.
- No invented component usage metrics or accessibility pass claims.
- Flag uncertain findings as needing verification.

## Workflow

1. Review tokens (type, color, spacing, elevation, motion) for consistency.
2. Audit component patterns and state coverage.
3. Identify accessibility and hierarchy risks.
4. Prioritize remediation backlog by impact and effort.

## Output format
```

- Design system audit summary
- Findings table (area | issue | impact | recommendation)
- Priority remediation backlog
- Verification needs
```

## Quality checks

- Findings are evidence-backed and categorized by severity.
- Recommendations respect provided constraints and context.

## Related skills

web-design-brief-builder, superdesign-ui-prompt-adapter, cross-asset-consistency-check
