---
name: chart-selection
domain: writing/dataviz
trigger: "Choosing a chart type for a known comparison; the data is ready but the form is undecided"
anti_trigger: "Judging a chart already chosen against how accurately the eye reads it (subskills/perceptual-accuracy.md); the claim is still unwritten (subskills/claim-first-design.md)"
scope: "Choosing a chart type from the comparison the reader must make: magnitude / change over time / distribution / correlation / part-to-whole / ranking / deviation / flow"
status: seedling
---

# Chart Selection

## Standard

- **FT Visual Vocabulary**: nine relationship classes, each with its accepted forms — deviation, correlation, ranking, distribution, change over time, magnitude, part-to-whole, spatial, flow. <https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary>
- **Few, "The Right Graph"**: the graph comes from the question, and most questions reduce to a handful of forms. <https://www.perceptualedge.com/articles/ie/the_right_graph.pdf>
- **Cairo, _How Charts Lie_ (2019)**: the wrong form can be accurate and still mislead, because it invites the wrong comparison. <https://wwnorton.com/books/9781324001997>
- ⚠️ House convention: part-to-whole above roughly five parts becomes a table or a sorted bar.

## Decision rules

1. If the reader compares magnitudes across categories, use bars; horizontal when labels are words.
2. If the reader follows a value over ordered time, use a line; reserve area for one total, never several series.
3. If the reader judges spread, use a histogram, strip plot, or ECDF; a mean alone hides both.
4. If the reader looks for a relationship between two measures, use a scatter; add a fit only when a fit exists.
5. If the reader wants parts of a whole, use a stacked bar for two or three parts; a treemap only when the hierarchy matters.
6. If the reader ranks many items, sort the bars by value and drop the gridlines.
7. If the reader judges distance from a reference, use a diverging bar anchored at zero.

```text
magnitude across categories ....... horizontal bar, sorted
change over ordered time .......... line; area for one series only
distribution of one measure ....... histogram, strip, ECDF
two measures together ............. scatter, fit only if real
parts of one whole ................ stacked bar, treemap if nested
rank across many items ............ sorted bar, dot plot
distance from a reference ......... diverging bar at zero
flow between states ............... Sankey, flows labelled
```

## Procedure

1. Read the claim and underline the verb: compare, follow, judge, rank, trace.
2. Map that verb to one class in the block above.
3. Count the series. Above four on one panel, facet.
4. Check the data type on each axis: category, ordered time, or continuous measure.
5. Take the plainest member of the class; sketch it by hand with three real values.
6. Write the axis units and the ordering rule before styling anything.

## Anti-patterns

- **Pie for ranking.** Angles encode badly and labels crowd. Fix: sorted horizontal bars.
- **Line for unordered categories.** The line implies a path that does not exist. Fix: bars.
- **Area for several series.** Overlapping fills hide each other. Fix: lines, or small multiples.
- **Scatter for a time series.** Order vanishes from the eye. Fix: line on a time axis.

## Done checklist

- [ ] The comparison class is named in one word.
- [ ] The form is the plainest member of that class.
- [ ] Series count fits the form, or the chart is faceted.
- [ ] Axis types match the data types.
- [ ] A three-value sketch reads correctly.

## Sources

- FT Visual Vocabulary: <https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary>
- Few, "The Right Graph": <https://www.perceptualedge.com/articles/ie/the_right_graph.pdf>
- Cairo, _How Charts Lie_: <https://wwnorton.com/books/9781324001997>