---
name: ac-design-taste
description: "Judging and critiquing UI and visual-design quality: the judgment layer between building an interface and reviewing its code. Eight leaves: the critique protocol and perception order; typography scale and pairing; spacing grids and optical alignment; color and WCAG contrast math; Nielsen heuristic evaluation run as a protocol; AI-slop anti-patterns; a 0-10 scoring rubric; a taste-development practice loop. Use when asking \"critique this UI\", \"does this design look right\", \"score this mock\", \"is this contrast acceptable\", \"run a heuristic pass\", \"this UI looks like default AI slop\", \"sharpen my design taste\". Not for: building components (use ac-frontend-ui) or WCAG conformance checklists (use ac-frontend-ui)."
license: MIT
metadata:
  domain: software-engineering
---

# Design Taste

## Overview

The judgment layer between building and code review. Given a UI, mock, screenshot, or description, decide what works, what fails, and what to fix first. It never builds components and never grades code.

## When to use

- Critiquing a UI, mock, or screenshot description.
- Type, spacing, and palette decisions with contrast math.
- A Nielsen heuristic pass with evidence and severity.
- Diagnosing default-looking AI output and fixing it.
- Comparable 0-10 scores across rounds; a taste practice loop.

## When not to use

- Building components, tokens, or WCAG conformance work: pick `ac-frontend-ui`.
- Reviewing the code behind a UI: pick `ac-code-review`.

## Subskill index

| subskill file | when to load |
|---|---|
| `subskills/critique-protocol.md` | Perception order, the 10-minute checklist, hosting a crit |
| `subskills/typography.md` | Type scale, pairing, measure, hierarchy without color |
| `subskills/spacing.md` | The 4/8 point grid, optical alignment, density budgets |
| `subskills/color-contrast.md` | Palette shape, 4.5:1 and 3:1 ratios, colorblind safety |
| `subskills/heuristic-evaluation.md` | Nielsen's ten run as a protocol with severity and evidence |
| `subskills/ai-slop-anti-patterns.md` | Default-LLM visual tells, diagnosed and fixed |
| `subskills/rubric-scoring.md` | Anchored 0-10 scores, caps, and round deltas |
| `subskills/taste-development.md` | Practice reps: teardowns, constraint drills, canon, peer review |
