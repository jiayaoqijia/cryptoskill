---
name: weighting-schemes
domain: investing/weighting-schemes
trigger: "Choosing or reading a weighting scheme and its concentration effect."
anti_trigger: "Not for predicting returns, and not for fund selection."
scope: "Cap, equal, fundamental, and what each does to concentration."
status: seedling
---

# Weighting schemes

## Standard

The weighting scheme converts a selected set of securities into a portfolio, and it decides the exposure more than the selection does. Capitalisation weighting lets the largest companies dominate and produces a portfolio that is concentrated by construction, while equal weighting diversifies but requires constant rebalancing and so generates turnover.

Schemes between those two make different trades. Fundamental weighting selects on accounting measures rather than price, which introduces a value tilt and a rebalancing pattern driven by reported data. Capped schemes preserve the selection while limiting single-name weight, at the cost of a defined rebalancing process. The record states the scheme, the concentration it produces, and the turnover it implies.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the weighting scheme and its inputs.
- Record the resulting concentration: top holding, top ten, and the effective number of names.
- Record the turnover the scheme implies at the stated rebalancing frequency.
- Record any tilt the scheme introduces relative to the selection universe.
- Record the rebalancing mechanism, since equal and fundamental schemes require one.
- Record the concentration's behaviour as constituents appreciate.

## Procedure

1. Record the scheme and its inputs.
2. Compute concentration measures at inception.
3. Estimate turnover over a year.
4. Identify any systematic tilt.
5. Record the rebalancing mechanism.
6. Write the weighting summary with its consequences.

## Anti-patterns

- Assuming equal weighting is neutral, when it is a small-cap tilt.
- Ignoring the turnover equal weighting requires.
- Comparing concentration across indices with different schemes.
- Treating a fundamental tilt as an absence of tilt.
- Overlooking how concentration grows between rebalances.

## Done checklist

- [ ] Scheme and inputs recorded.
- [ ] Concentration computed.
- [ ] Turnover estimated.
- [ ] Tilt identified.
- [ ] Rebalancing mechanism recorded.
- [ ] Summary states consequences.

The effective number of names is the most useful single concentration measure here, because it converts a weight distribution into the equivalent count of equally weighted holdings, which makes schemes with different inputs comparable on the dimension that matters.


The turnover estimate also belongs beside the concentration measure, because the two together describe the scheme's practical cost: a concentrated scheme with low turnover and a diversified one with high turnover are different propositions at the same headline exposure.


Recording the scheme's rebalancing requirement beside its weights closes the last gap, since the same weight distribution costs very different amounts to maintain depending on how often it must be restored.


## Sources

- Index methodology context: <https://www.sec.gov/investor>
- Investor education on index construction: <https://www.investor.gov/introduction-investing>
- Market and fundamental data: <https://fred.stlouisfed.org/>
