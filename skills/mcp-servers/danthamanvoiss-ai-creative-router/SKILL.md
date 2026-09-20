---
name: ai-creative-router
description: Route AI-creative quality, pipeline, prompt-translation, and cross-asset consistency work to the right support skill.
version: 1.0.0
tags: [core, routing, creative, ai, v1]
---

## Purpose

Choose the right AI-creative support layer so prompt cleanup, consistency review, pipeline design, and anti-slop quality control stay distinct and reusable across categories.

## Use when

- The main router has identified a cross-cutting AI-creative support need.
- Another category needs a quality or prompt-prep layer rather than a primary execution skill.
- The user is working on prompt quality, asset consistency, or AI-assisted content process design.

## Required inputs

- Asset type or workflow being supported.
- The main output category [if any].
- Whether the need is quality review, prompt translation, consistency, or pipeline planning.

## Safety/authority

- Treat AI-generated material as draft-only until reviewed in the destination workflow.
- Do not collapse category-specific requirements into generic prompt language without noting the loss of detail.
- Keep this router as a support layer unless the user explicitly wants AI-creative workflow design as the main task.

## Workflow

1. Clarify whether the need is quality control, prompt-to-brief translation, pipeline design, or consistency checking.
2. Route to:
   - `anti-slop-content-review` for output quality review
   - `prompt-to-brief-translator` for turning rough prompts into structured briefs
   - `ai-content-pipeline-builder` for reusable AI workflow design
   - `cross-asset-consistency-check` for multi-asset alignment
3. Pair with the main category skill only when the support layer adds clear value.
4. Keep the stack to 1–3 skills total including the primary category skill.
5. If the requested skill is unavailable, choose the closest support-layer alternative or ask for clarification.

## Output format

```
- Support need: ...
- Main category or asset: ...
- Selected skills (1-3): ...
- Missing inputs: ...
- Next step prompt: ...
```

## Quality checks

- This router acts as a support layer, not an unnecessary extra hop.
- The selected skill matches the actual AI-creative need.
- Pairing stays minimal.
- Draft-only status is preserved.

## Related skills

agency-router, anti-slop-content-review, prompt-to-brief-translator, ai-content-pipeline-builder, cross-asset-consistency-check
