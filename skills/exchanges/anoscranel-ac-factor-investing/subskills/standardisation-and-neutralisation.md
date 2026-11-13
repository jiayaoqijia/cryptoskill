---
name: standardisation-and-neutralisation
domain: investing/standardisation-and-neutralisation
trigger: "Making a factor comparable across securities and free of unintended exposures."
anti_trigger: "Not for predicting returns, and not for portfolio construction."
scope: "Winsorising, z-scores, and removing unintended exposures."
status: seedling
---

# Standardisation and neutralisation

## Standard

A raw characteristic is not comparable across securities: a company with a price-to-book of two and one with four are both cheap or expensive only relative to the distribution. Standardisation converts the raw measure into a rank or a z-score within the universe, which makes the scores comparable and gives the sorting a consistent interpretation.

Neutralisation then removes exposures the factor is not meant to carry. A size factor will pick up sector effects if the cheap sectors happen to be small, and a momentum factor can inherit a beta tilt. Regressing the standardised score on the unintended exposures and taking the residual removes them, which changes what the factor measures and therefore what its premium means.

Primary sources: <https://www.nber.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record whether scores are ranks or z-scores, and why.
- Record the winsorising threshold if the raw distribution is heavy-tailed.
- Record the exposures neutralised: sector, size, beta, or country.
- Record the regression used for neutralisation and its specification.
- Record the effect of neutralisation on the factor's characteristics.
- Record what was deliberately not neutralised, and the reason.

## Procedure

1. Choose ranks or z-scores and record the choice.
2. Apply winsorising if the tails distort the scores.
3. Identify the unintended exposures.
4. Regress and take residuals.
5. Compare the factor with and without neutralisation.
6. Record the specification and the decision.

## Anti-patterns

- Sorting raw characteristics without standardising.
- Neutralising without recording the specification.
- Neutralising away the exposure the factor is meant to capture.
- Ignoring the effect of winsorising on the tails.
- Assuming neutralisation improves returns rather than changing the question.

## Done checklist

- [ ] Score type recorded.
- [ ] Winsorising recorded.
- [ ] Exposures identified.
- [ ] Regression specification recorded.
- [ ] Before-and-after comparison made.
- [ ] Deliberate non-neutralisation recorded.

A subtler issue is that neutralisation can remove the very effect being studied: a value factor neutralised against industry will not capture an industry-level re-rating, and a momentum factor neutralised against size will not capture the size-related component of its own signal, so the record should state which effects the factor is intended to include before the residuals are taken.


The winsorising threshold is also worth recording as a number rather than a practice: a one percent threshold and a five percent threshold produce different factor scores for the same securities, and a result that survives at both is stronger evidence than one that depends on the choice, which is a comparison the record makes possible only if both thresholds were noted.


## Sources

- Research on factor construction and standardisation: <https://www.nber.org/>
- Investor education on factor measurement: <https://www.investor.gov/introduction-investing>
- Market data for exposure estimation: <https://fred.stlouisfed.org/>
