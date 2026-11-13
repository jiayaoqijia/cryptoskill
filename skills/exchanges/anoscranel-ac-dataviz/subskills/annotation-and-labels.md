---
name: annotation-and-labels
domain: writing/dataviz
trigger: "Legends instead of labels; titles that repeat the axis; missing units or source lines; decoration crowding the data"
anti_trigger: "Which chart form answers the claim (subskills/chart-selection.md); palette and contrast (subskills/colour-and-accessibility.md); axis truncation that distorts (subskills/misleading-patterns.md)"
scope: "Direct labelling; title and source discipline; units and baselines; removing non-data ink"
status: seedling
---

# Annotation and Labels

## Standard

- **Tufte, _The Visual Display of Quantitative Information_**: the data-ink ratio, and chart junk as ink that serves decoration rather than data. <https://www.edwardtufte.com/book/the-visual-display-of-quantitative-information/>
- **Wilke, "Figure titles and captions"**: title, subtitle, and caption each carry a different job and must not duplicate each other. <https://clauswilke.com/dataviz/figure-titles-captions.html>
- **Wilke, "Balance the data and the context"**: a figure without source, unit, and period invites a wrong reading. <https://clauswilke.com/dataviz/balance-data-context.html>
- **Wilke, "Small axis labels"**: axis text is read, so it must be legible at final size, not screen size. <https://clauswilke.com/dataviz/small-axis-labels.html>
- **FT Visual Vocabulary**: annotation is part of the chart's argument, not an afterthought. <https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary>
- ⚠️ House convention: four series or fewer get direct labels; five or more get a legend sorted to match the data.

## Decision rules

1. If a series can hold its own label, label it there and delete the legend.
2. If the legend stays, order it by value and place it near the first point it explains.
3. If the title restates the axis ("Sales by month"), rewrite it as the finding.
4. If there is no subtitle, add unit, period, and sample size there.
5. If the source appears only in a distant footnote, put a short form inside the figure.
6. If gridlines are darker than the data, lighten them until they recede.
7. If every point carries a value label, keep only where the claim turns.
8. If a bar baseline is not zero, the length lies. ⚠️ Bars start at zero by convention.

## Procedure

1. Write the title as the claim; check it does not repeat the axis text.
2. Write the subtitle: metric, unit, period, geography, sample size.
3. Label lines at their ends, or bars inside where the text fits.
4. Delete the legend once every series is labelled.
5. Set axis titles to unit-bearing text: "Revenue, USD millions", not "Value".
6. Set the baseline from the form: zero for bars and areas; a stated range for lines.
7. Remove tick marks, top and right spines, background fills, drop shadows.
8. Lighten gridlines below the data's visual weight.
9. Add one callout on the turning point, carrying its value.
10. Add the source line: publisher, dataset, retrieval date.

## Anti-patterns

- **Legend for two series.** Forces back-and-forth eye travel. Fix: label each line at its end.
- **"Value" as an axis title.** The unit is left to guesswork. Fix: name the metric and its unit.
- **Every point labelled.** Labels collide and signal disappears. Fix: endpoints and the turning point only.
- **Heavy grid, faint data.** Inverts the hierarchy. Fix: lighten the grid.

## Done checklist

- [ ] Title states the finding and does not repeat the axis.
- [ ] Subtitle carries metric, unit, period, and sample size.
- [ ] Series are direct-labelled wherever space allows.
- [ ] Bars and areas start at zero.
- [ ] A source line names the publisher and the retrieval date.

## Sources

- Tufte, _The Visual Display of Quantitative Information_: <https://www.edwardtufte.com/book/the-visual-display-of-quantitative-information/>
- Wilke, "Figure titles and captions": <https://clauswilke.com/dataviz/figure-titles-captions.html>
- Wilke, "Balance the data and the context": <https://clauswilke.com/dataviz/balance-data-context.html>
- Wilke, "Small axis labels": <https://clauswilke.com/dataviz/small-axis-labels.html>
- FT Visual Vocabulary: <https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary>