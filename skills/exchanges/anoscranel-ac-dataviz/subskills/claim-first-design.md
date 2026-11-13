---
name: claim-first-design
domain: writing/dataviz
trigger: "Deciding what a chart must prove before drawing it; a title that names the topic; a figure that argues nothing"
anti_trigger: "Choosing the chart type once the claim is fixed (subskills/chart-selection.md); the five-test audit of a finished chart (subskills/chart-review.md)"
scope: "Turning a data question into the one sentence a chart must support; headline as conclusion; one chart one claim"
status: seedling
---

# Claim-First Design

## Standard

- **Cairo, _How Charts Lie_ (2019)**: a chart is an argument, not a container for data. <https://wwnorton.com/books/9781324001997>
- **Wilke, "Telling a story"**: the figure serves one narrative point; decoration that serves none competes with it. <https://clauswilke.com/dataviz/telling-a-story.html>
- **Tufte, _The Visual Display of Quantitative Information_**: a mark either carries data or earns its place. <https://www.edwardtufte.com/book/the-visual-display-of-quantitative-information/>
- **FT Visual Vocabulary**: chart choice starts from the sentence the reader must leave with. <https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary>
- ⚠️ House convention: the headline states the finding, not the topic. "Revenue" fails; "Revenue fell 8% after the March price rise" passes.

## Decision rules

1. If the claim will not fit one sentence with a subject, a direction, and a number, do not draw yet.
2. If the sentence needs two "and"s, it is two claims: split the charts or drop one.
3. If the claim is a comparison, the headline names both sides and the gap.
4. If the claim is change, the headline names the change and its period, not the metric alone.
5. If the reader would act the same either way, the chart earns no space.
6. If the data is exact values in under seven rows, show a table. ⚠️ House threshold.
7. ⚠️ House: headline at most twelve words and one number, so the eye lands on a single fact.

## Procedure

1. Name the decision the chart serves and who makes it.
2. Write the sentence in plain words: what changed, by how much, against what.
3. Name the comparison: baseline, peer, target, or prior period.
4. Fix the metric, unit, and period; they return later as the subtitle.
5. Draft the headline by adding the number and verb to the topic.
6. Delete every second claim from the panel; park it in a note.
7. Cover the caption and read the chart. If the claim does not survive, the chart fails.
8. Restore the caption as subtitle: unit, period, sample size, source; record the claim beside the figure number.

## Anti-patterns

- **Topic headline.** "Q3 performance" tells nobody anything. Fix: state the finding with its number.
- **Chart as data dump.** Every column plotted because it exists. Fix: plot only what the claim needs.
- **Two claims in one panel.** Attention splits and neither reads. Fix: two panels, or one panel plus one sentence.
- **Claim asserted, chart silent.** The title says "surge", the line is flat. Fix: change the claim to fit the data, never the reverse.
- **Claim with no comparison.** A lone number is not a finding. Fix: add the baseline, peer, or prior period.
- **Figure that repeats the paragraph.** Fix: cut one.

## Done checklist

- [ ] The claim exists as one sentence with subject, direction, and number.
- [ ] The headline states the finding, not the topic.
- [ ] The chart carries exactly one claim.
- [ ] The claim survives with the caption covered.
- [ ] A comparison is visible inside the frame.

## Sources

- Cairo, _How Charts Lie_: <https://wwnorton.com/books/9781324001997>
- Wilke, "Telling a story": <https://clauswilke.com/dataviz/telling-a-story.html>
- Tufte, _The Visual Display of Quantitative Information_: <https://www.edwardtufte.com/book/the-visual-display-of-quantitative-information/>
- FT Visual Vocabulary: <https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary>