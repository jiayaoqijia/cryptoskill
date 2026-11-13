---
name: chart-review
domain: writing/dataviz
trigger: "A figure is about to ship; someone asks whether a chart is honest or accessible; a dashboard needs a pass-or-fix verdict"
anti_trigger: "Building the chart from the claim upward (subskills/claim-first-design.md); diagnosing one named fault such as a truncated axis (subskills/misleading-patterns.md); reviewing the report text around the figure"
scope: "The pre-publish audit of one chart or a dashboard: the five tests in order and what to change first"
status: seedling
---

# Chart Review

## Standard

- **Chartability** (Elavsky et al., _Computer Graphics Forum_ 41(3), 2022): an ordered set of heuristics and tests for visualization accessibility, run as an audit rather than a skim. <https://chartability.fizz.studio/>
- **WCAG 2.2**: SC 1.4.1 use of colour and SC 1.4.11 non-text contrast are the two criteria a static chart most often fails. <https://www.w3.org/TR/WCAG22/>
- **Tufte, _The Visual Display of Quantitative Information_**: the honesty test lives in the relation between drawn size and the number drawn. <https://www.edwardtufte.com/book/the-visual-display-of-quantitative-information/>
- ⚠️ House convention: five tests in fixed order, a written verdict, and the first failing test sets the fix order.

## Decision rules

1. If the claim test fails, stop; no styling rescues a chart that argues the wrong thing.
2. If the decode test fails, change the form before the colour.
3. If the accessibility test fails, fix in order: encoding, then palette, then styling.
4. If the honesty test fails, fix the scale or baseline before any label.
5. If the source test fails, the chart is unverifiable; withhold it rather than annotate it.
6. If the chart passes all five but reads slowly, that is craft, not a defect.
7. If a dashboard fails, review the worst tile first; one bad tile discredits the grid.

## Procedure

1. **Claim.** Cover the caption, read the chart, write the sentence it supports, compare with the title.
2. **Decode.** Name the encoding and its rung on the perceptual ladder; check the claim needs no finer precision.
3. **Accessibility.** Run Chartability's structure and contrast checks. <https://chartability.fizz.studio/>
4. Verify each graphical object at 3:1 against its background. <https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html>
5. Run the greyscale and colour-blindness passes.
6. **Honesty.** Compare visual ratio with numeric ratio; check baselines, dual axes, area scaling, window, aggregation, precision.
7. **Source.** Confirm publisher, dataset, retrieval date, sample size, and the numbers against the source.
8. Read the figure at final display size: printed page, slide, or phone width.
9. Write the verdict: PASS, FIX with a list, or REBUILD with the reason.
10. Order fixes by leverage: claim, form, scale, labels, palette, decoration.

## Anti-patterns

- **Polishing before testing.** Hours of styling on a chart whose claim is wrong. Fix: claim test first.
- **Colour audit as full audit.** Contrast passes while the axis lies. Fix: all five tests, in order.
- **Reviewing a screenshot without the data.** Visual and numeric ratios cannot be compared. Fix: get the numbers or withhold the verdict.
- **Verdict by adjective.** "Looks good" is not a review. Fix: name the test that passed or failed.
- **Fixing everything at once.** The change cannot be attributed. Fix: apply the fix list in one ordered pass.

## Done checklist

- [ ] Claim written down and compared with the title.
- [ ] Encoding named and matched to the precision needed.
- [ ] Chartability and 3:1 contrast checks run.
- [ ] Greyscale and colour-blindness passes done.
- [ ] Honesty and source tests run against the numbers.

## Sources

- Chartability: <https://chartability.fizz.studio/>
- Elavsky et al. 2022: <https://doi.org/10.1111/cgf.14522>
- WCAG 2.2: <https://www.w3.org/TR/WCAG22/>
