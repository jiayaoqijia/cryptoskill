---
name: ac-dataviz
description: "Chart judgment for a general agent. Eight leaves: claim-first-design (the sentence a chart must support; headline as conclusion), chart-selection (decision tree by comparison type), perceptual-accuracy (Cleveland-McGill ranking; why pie and bubble charts lose), colour-and-accessibility (palette types; colour-blind-safe defaults; WCAG 2.2 1.4.11; redundant encoding), annotation-and-labels (direct labels; source discipline; data-ink; baselines), small-multiples-and-layout (facet vs overlay; banking to 45 degrees; ordering; dashboards), misleading-patterns (truncated axes, dual y-axes, 3D, cherry-picked windows), chart-review (the five-test audit). Use when asking 'which chart should I use', 'is this chart misleading', 'fix this truncated axis', 'make this chart colour-blind safe', 'review this dashboard', 'why does this pie chart feel wrong'. Not for: deck layouts (use ac-slide-decks) or document typesetting (use ac-technical-writing)."
license: MIT
metadata:
  domain: writing
---

# Data Visualisation

## Overview

The judgment layer for charts: which chart answers which claim, what the eye decodes, colour that survives colour blindness, annotation discipline, dashboards, and the patterns that mislead. The reader is an agent choosing or reviewing a chart, not a plotting library.

## When to use

- Choosing a chart for a claim you must support.
- Reviewing a figure or dashboard before it ships; the chart feels wrong and the fault needs a name.

## When NOT to use

Slide layouts and speaker notes are outside; ac-slide-decks covers those. Document typesetting is outside; ac-technical-writing covers those. Drawing code for a library is outside by design: this skill decides what the chart must do.

## Subskill index

| subskill file | when to load |
|---|---|
| `subskills/claim-first-design.md` | the claim is vague or the headline is a topic |
| `subskills/chart-selection.md` | the comparison type is named but the chart is not |
| `subskills/perceptual-accuracy.md` | a pie, donut, bubble, or area chart is proposed |
| `subskills/colour-and-accessibility.md` | picking a palette or fixing contrast |
| `subskills/annotation-and-labels.md` | titles, legends, units, source lines, chart junk |
| `subskills/small-multiples-and-layout.md` | faceting, aspect ratio, category order, dashboards |
| `subskills/misleading-patterns.md` | the chart may distort what the data says |
| `subskills/chart-review.md` | a finished chart needs a pass-or-fix verdict |