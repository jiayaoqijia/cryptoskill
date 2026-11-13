---
name: charts-per-claim
domain: writing/slide-decks
trigger: "which chart fits this data; turn this table into a chart; is a pie chart OK here; visualize this number"
anti_trigger: "Contrast, color safety and alt text on written charts (subskills/accessibility.md); live dashboards and monitoring views (outside this skill)"
scope: "Choosing the chart from the claim and knowing when a chart is the wrong container"
status: seedling
---

# Charts per Claim

## Standard

- **Cleveland and McGill (1984)**: the graphical-perception ranking. People judge position on a common scale most accurately, then position on identical non-aligned scales, then length, then angle and slope, then area, then volume and color. <https://doi.org/10.1080/01621459.1984.10478080>
- **FT Visual Vocabulary**: choose the chart by the relationship in the claim: deviation, correlation, ranking, distribution, change over time, magnitude, part-to-whole, spatial, or flow. <https://github.com/Financial-Times/chart-doctor>
- **Berinato, Good Charts**: name the claim first. The chart illustrates the claim; it never substitutes for one. <https://store.hbr.org/product/good-charts-the-hbr-guide-to-making-smarter-more-persuasive-data-visualizations/15005>
- **IBCS**: unified notation for business charts: bars and waterfalls, horizontal time axes, consistent scaling across pages. <https://www.ibcs.com/standards/>

## Decision rules

1. If the claim compares a few values, use a horizontal bar. Length beats angle, so a bar beats a pie.
2. If the claim is change over time, use a line or a column. Never a table of every period.
3. If the claim is part-to-whole with more than four parts, use a stacked bar or rank the parts.
4. If exact values decide the matter (compliance, payouts), a table beats any chart.
5. If the datum is one or two scalars, do not chart it. Set the number in large type with one line of context.
6. Use dual axes only when the correlation itself is the claim. Otherwise split into two charts.
7. Never use 3D or gradient fills. They distort the length and area the reader judges (Cleveland).
8. When charts repeat across slides, fix units and scales so slides stay comparable (IBCS).

## Procedure

1. Write the claim sentence for the datum: subject, verb, number.
2. Name the relationship in FT vocabulary terms.
3. Pick the chart family from that vocabulary row.
4. Check the primary encoding against the Cleveland-McGill ranking. Prefer position and length over angle and area.
5. Fix the scale, units, and axis ranges that must repeat across slides.
6. Annotate the claim point directly on the chart, not in a caption.
7. Draft the alt text from the claim sentence. Contrast and reading-order rules live in `subskills/accessibility.md`.

## Anti-patterns

- A pie with twelve slices. Fix: bar, ranked.
- Choosing the chart before writing the claim. Fix: claim first, chart second.
- A truncated axis that amplifies a small difference. Fix: start the axis at a defensible baseline or note the truncation.
- Dual axes implying a correlation nobody claims. Fix: split the chart.
- 3D bars or exploded pies. Fix: flat and whole.
- A legend that forces lookups. Fix: direct labels.

## Done checklist

- [ ] Claim sentence written before the chart was chosen.
- [ ] Relationship named in FT vocabulary terms.
- [ ] Primary encoding is position or length where possible.
- [ ] Scales and units consistent across repeated charts.
- [ ] One or two scalar numbers rendered as type, not charts.
- [ ] No 3D, no dual axes without a correlation claim.

## Sources

- Cleveland and McGill (1984), graphical perception: <https://doi.org/10.1080/01621459.1984.10478080>
- FT Visual Vocabulary, chart-doctor: <https://github.com/Financial-Times/chart-doctor>
- Berinato, *Good Charts*: <https://store.hbr.org/product/good-charts-the-hbr-guide-to-making-smarter-more-persuasive-data-visualizations/15005>
- IBCS standards: <https://www.ibcs.com/standards/>
