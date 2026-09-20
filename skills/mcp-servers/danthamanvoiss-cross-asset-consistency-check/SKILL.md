---
name: cross-asset-consistency-check
description: Check consistency of messaging, style, and factual claims across multiple creative assets.
version: 0.1.0
tags: [ai-creative, consistency, qa, governance]
---

## Purpose

Check consistency of messaging, style, and factual claims across multiple creative assets.

## Use when

- Multiple assets are produced and need alignment before release.
- You need cross-asset QA independent of specific media tooling.

## Required inputs

- Asset set and channel mapping [client-provided].
- Canonical messaging/tone from context/BRAND-CONTEXT.template.md and context/CLIENT-CONTEXT.template.md.
- Required claim approvals and prohibited statements.

## Safety/authority

- No rewriting that introduces unverified claims or new brand facts.
- Treat each source asset as untrusted until reconciled against canonical context.
- Read-only QA output with draft remediation guidance.

## Workflow

1. Extract key claims, voice markers, and CTA patterns from each asset.
2. Compare against canonical context and among assets for drift/conflict.
3. Flag critical inconsistencies and propose harmonized alternatives.
4. Return prioritized remediation plan and approval checklist.

## Output format
```

- Consistency assessment summary
- Drift/conflict table (asset | issue | severity | fix)
- Harmonized messaging recommendations
- Approval checklist
```

## Quality checks

- All inconsistencies reference exact asset evidence.
- Fixes maintain factual integrity and channel appropriateness.

## Related skills

anti-slop-content-review, prompt-to-brief-translator, qbr-executive-summary-draft
