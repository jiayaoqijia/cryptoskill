---
name: seo-geo-router
description: Route SEO and GEO requests to the right audit or content-review skill with lightweight visibility-specific clarification.
version: 1.0.0
tags: [core, routing, seo, geo, v1]
---

## Purpose

Direct search visibility work to the right SEO/GEO skill so audits, citability review, and local visibility checks stay distinct and easy to run.

## Use when

- The main router has identified an SEO, GEO, discoverability, or local visibility request.
- The user needs either a diagnostic audit or a content-focused review but has not specified which.
- The task is narrow enough to stay inside the SEO/GEO family.

## Required inputs

- Target site, business, page set, or content set.
- Desired focus: opportunity audit, AI citability, or local visibility [if known].
- Location, service area, or priority topics [if relevant].

## Safety/authority

- Do not promise rankings, traffic, or citation outcomes.
- Keep audits evidence-based and note missing site or market inputs.
- Treat competitive claims and local assertions as draft-only unless verified.

## Workflow

1. Clarify whether the user needs a broad opportunity audit, a content citability review, or a local presence review.
2. Select the closest fit:
   - site/opportunity diagnosis: `seo-geo-opportunity-audit`
   - AI answer-engine readiness or citation quality: `ai-citability-content-review`
   - local business presence and local search visibility: `local-visibility-review`
3. Select at most 1–2 skills unless the user explicitly wants a sequenced audit plus remediation input.
4. Optionally pair with `anti-slop-content-review` when copy quality is part of the review.
5. If the exact skill is unavailable, pick the nearest visibility-review alternative or ask for clarification.

## Output format

```
- Visibility focus: ...
- Target property or content: ...
- Selected skills (1-3): ...
- Missing inputs: ...
- Optional quality layer: ...
- Next step prompt: ...
```

## Quality checks

- The route distinguishes technical/opportunity review from content citability and local presence review.
- The stack stays lean.
- No ranking promises are made.
- Missing site or location context is surfaced.

## Related skills

agency-router, seo-geo-opportunity-audit, ai-citability-content-review, local-visibility-review, anti-slop-content-review
