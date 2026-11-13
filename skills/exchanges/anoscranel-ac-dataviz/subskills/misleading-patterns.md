---
name: misleading-patterns
domain: writing/dataviz
trigger: "An axis that does not start at zero; two y-axes on one chart; 3D effects; a time window chosen after the result was known"
anti_trigger: "Judging encoding accuracy in the abstract (subskills/perceptual-accuracy.md); ordinary label hygiene (subskills/annotation-and-labels.md); the five-test audit with a fix order (subskills/chart-review.md)"
scope: "Detecting and fixing distorting charts: truncated axes / dual y-axes / 3D / area exaggeration / cherry-picked windows / spurious precision"
status: seedling
---

# Misleading Patterns

## Standard

- **Cairo, _How Charts Lie_ (2019)**: most chart deception is a mismatch between the visual and the number, not a fabricated one. <https://wwnorton.com/books/9781324001997>
- **Wilke, "Don't go 3D"**: perspective adds a depth cue that carries no data and distorts the comparison. <https://clauswilke.com/dataviz/no-3d.html>
- **Wilke, "Visualizing amounts"**: bar length is the reader's scale; a cut baseline turns a ratio into a picture of one. <https://clauswilke.com/dataviz/visualizing-amounts.html>
- **Wilke, "Proportional ink"**: ink that grows with the square or cube of the value overstates the difference. <https://clauswilke.com/dataviz/proportional-ink.html>
- **FT Visual Vocabulary**: each form carries its known failure modes. <https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary>
- ⚠️ House convention: a truncated axis on a line chart is allowed only when the break is marked and the caption says why.

## Decision rules

1. If a bar axis misses zero, the length lies; restart at zero or switch to a line with a marked range.
2. If two y-axes share a frame, ask what the shared shape implies; if it is "a relationship", split the panels.
3. If the chart has depth, remove it; every 3D bar hides part of another.
4. If a circle grows with the value, check the scaling: area tracks value, never radius.
5. If the window starts where the trend looks good, widen it to a full cycle.
6. If the figure carries more decimals than the measurement supports, round to the source's precision.
7. If a line joins two points, it claims a trend from a straightedge; use a dot pair instead.

## Procedure

1. Read the axis: start, top, unit, and whether the scale is linear.
2. Compare the visual ratio with the numeric ratio; a gap is the fault.
3. List every channel that grows with the value: length, area, radius, depth.
4. Check each channel's scaling law against the value. <https://clauswilke.com/dataviz/proportional-ink.html>
5. Check the window against the data's natural cycle.
6. Check aggregation: unequal bins, totals mixed with rates, survivors only.
7. Check precision and any secondary axis for a chosen crossing point or reversed direction.
8. Apply the smallest fix that removes the distortion, then re-read the claim.
9. Where the distortion came from a source, keep its number and note the correction.

## Anti-patterns

- **Truncated bar baseline.** A 2% difference looks like a doubling. Fix: zero baseline, or a marked break.
- **Dual y-axes.** Any two series can be made to cross. Fix: stacked panels sharing an x-axis.
- **3D and perspective.** Back bars shrink, front bars grow. Fix: flat, one plane.
- **Radius scaled to value.** Perceived area grows as the square. Fix: scale area, or use bars.
- **Cherry-picked window.** The start date is the finding. Fix: the full series or a cycle-justified window.

## Done checklist

- [ ] Bar and area baselines start at zero.
- [ ] No dual y-axis survives without a stated reason.
- [ ] Area and radius encodings scale by area.
- [ ] The time window covers a full cycle or the series.

## Sources

- Cairo, _How Charts Lie_: <https://wwnorton.com/books/9781324001997>
- Wilke, "Don't go 3D": <https://clauswilke.com/dataviz/no-3d.html>
- Wilke, "Proportional ink": <https://clauswilke.com/dataviz/proportional-ink.html>
- Wilke, "Visualizing amounts": <https://clauswilke.com/dataviz/visualizing-amounts.html>