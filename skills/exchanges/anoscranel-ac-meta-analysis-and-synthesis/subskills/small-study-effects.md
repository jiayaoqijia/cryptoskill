---
name: small-study-effects
domain: research-operations/small-study-effects
trigger: "Investigating whether small studies tell a different story than large ones."
anti_trigger: "Not for declaring publication bias as fact, and not for the conduct layer."
scope: "Funnel asymmetry, trim-and-fill, Egger's test, and their honest limits."
status: seedling
---

# Small-study effects

## Standard

A funnel plot arranges studies by their effect estimate against a measure of their size. If only sampling noise operates, small studies scatter widely and symmetrically around the pooled effect; precision grows with size. Asymmetry — small studies favouring one direction more than their large counterparts — can indicate selective publication or poor conduct in small studies, but it can also indicate genuine heterogeneity: small studies may be conducted in higher-risk settings where the true effect is larger.

The tests inherit this ambiguity. Egger's regression has low power below roughly ten studies; the rank-correlation test lower still. Trim-and-fill imputes the missing symmetric studies, which assumes the asymmetry's cause and produces a number whose purpose is sensitivity exploration, not a corrected truth. The honest output is not "publication bias confirmed" but "asymmetry present; these are the candidate explanations; here is the estimate with and without adjustment."

Primary sources: <https://training.cochrane.org/handbook/current/chapter-11> and <https://training.cochrane.org/handbook/current/chapter-10>.

## Decision rules

- Pre-specify one asymmetry test as primary; run others as sensitivity.
- State that all asymmetry tests are underpowered below ten studies.
- Interpret asymmetry as small-study effect, not as proven publication bias.
- Run trim-and-fill as sensitivity only, and label its adjusted estimate as assumption-dependent.
- Check whether asymmetry survives restriction to low-risk-of-bias studies.
- Report the asymmetry finding whether or not the synthesis result survives it.

## Procedure

1. Plot the funnel with study size or standard error on one axis.
2. Run the pre-specified asymmetry test.
3. List the plausible explanations: selection, small-study conduct, genuine heterogeneity.
4. Test the heterogeneity explanation by subgroup or meta-regression if such a variable exists.
5. Run trim-and-fill as a sensitivity; record the adjusted estimate.
6. Report tests, caveats, and the sensitivity result.

## Anti-patterns

- Declaring "publication bias confirmed" from one underpowered test.
- Omitting the test when its p-value threatens the finding.
- Presenting the trim-and-fill estimate as the corrected truth.
- Running every available test and reporting only the significant one.
- Ignoring asymmetry because the pooled estimate is non-significant anyway.

## Done checklist

- [ ] Funnel plot drawn and inspected.
- [ ] Primary asymmetry test run as pre-specified.
- [ ] Power limitation stated.
- [ ] Alternative explanations listed and tested where possible.
- [ ] Trim-and-fill labelled as sensitivity.
- [ ] Findings reported regardless of direction.

## Sources

- Cochrane Handbook, reporting biases chapter: <https://training.cochrane.org/handbook/current/chapter-11>
- Cochrane Handbook, considering bias in analyses: <https://training.cochrane.org/handbook/current/chapter-10>
- Methods articles: <https://www.biomedcentral.com/methods>
