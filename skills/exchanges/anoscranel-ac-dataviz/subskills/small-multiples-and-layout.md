---
name: small-multiples-and-layout
domain: writing/dataviz
trigger: "Many series on one panel; faceting versus overlaying; a chart wider than its trend; categories in alphabetical order; a dashboard grid that reads badly"
anti_trigger: "Which chart family answers the comparison (subskills/chart-selection.md); colouring across facets (subskills/colour-and-accessibility.md); one chart's own titles (subskills/annotation-and-labels.md)"
scope: "Faceting versus overlay; aspect ratio and banking to 45 degrees; ordering categories by the data; dashboard layout and preattentive cues"
status: seedling
---

# Small Multiples and Layout

## Standard

- **Wilke, "Multi-panel figures"**: shared scales are the point of a facet grid; independent scales destroy the comparison the grid exists for. <https://clauswilke.com/dataviz/multi-panel-figures.html>
- **Cleveland, McGill & McGill, "The Shape Parameter of a Two-Variable Graph", _JASA_ 83(402), 1988**: banking a line to about 45 degrees average slope makes direction and rate easiest to judge. <https://doi.org/10.1080/01621459.1988.10478598>
- **Few, "Tapping the Power of Visual Perception"**: preattentive attributes are seen before reading starts, so they carry the one value that matters. <https://www.perceptualedge.com/articles/ie/visual_perception.pdf>
- **Wilke, "Coordinate systems and axes"**: the frame is a design choice, and the default frame is rarely the best. <https://clauswilke.com/dataviz/coordinate-systems-axes.html>
- ⚠️ House convention: sort categories by the value being compared, never by alphabet, unless the reader is hunting a name.

## Decision rules

1. If more than four series share one measure, facet; do not add hues.
2. If panels are faceted, lock the axes and say so in the caption.
3. If panels use different units, separate them and label each axis.
4. If a line runs across a wide, short frame, re-bank it toward 45 degrees first.
5. If the comparison is a ranking, sort by value; keep alphabet only for lookup lists.
6. If time is on the x-axis, keep intervals equal; label unequal bins explicitly.
7. If one number decides the reader's action, cue it and mute the rest.

## Procedure

1. Count series and measures; two grouping dimensions means a facet grid, not a colour pile.
2. Order the facets by value, region, or the reader's model, never by default.
3. Set shared scales, then thin unreadable ticks in small panels.
4. Resize the panel until the average trend slope sits near 45 degrees. <https://doi.org/10.1080/01621459.1988.10478598>
5. Sort categories inside every facet to one shared order.
6. Align the grid: equal gaps, one baseline row, titles top-left of each panel.
7. Place a dashboard in reading order: most important tile top-left, then across and down.
8. Cue the action tile with one preattentive mark: weight, enclosure, or a single accent hue. <https://www.perceptualedge.com/articles/ie/visual_perception.pdf>
9. Read the figure at thumbnail size; if the structure vanishes, the layout is too busy.

## Anti-patterns

- **Overlay of eight series.** Lines tangle and the legend becomes the chart. Fix: small multiples with shared scales.
- **Independent y-scales in a facet grid.** Every panel looks alike and nothing compares. Fix: one scale, stated.
- **Alphabetical categories.** The ranking the reader wants is hidden. Fix: sort by value.
- **Aspect ratio set by the container.** The slope becomes an artefact of page width. Fix: bank to 45 degrees.

## Done checklist

- [ ] Facets share one scale, and the caption says so.
- [ ] Series count fits the form without a crowded legend.
- [ ] Trend slope sits near 45 degrees where a trend is judged.
- [ ] Categories are sorted by the plotted value.
- [ ] Dashboard tiles follow a stated reading order.

## Sources

- Wilke, "Multi-panel figures": <https://clauswilke.com/dataviz/multi-panel-figures.html>
- Cleveland, McGill & McGill 1988: <https://doi.org/10.1080/01621459.1988.10478598>
- Few, "Tapping the Power of Visual Perception": <https://www.perceptualedge.com/articles/ie/visual_perception.pdf>
- Wilke, "Coordinate systems and axes": <https://clauswilke.com/dataviz/coordinate-systems-axes.html>