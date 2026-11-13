---
name: tax-efficiency
domain: investing/tax-efficiency
trigger: "Comparing the tax drag of otherwise similar funds."
anti_trigger: "Not for computing tax, and not for fund recommendations."
scope: "Distributions, turnover, and the tax drag that differs between otherwise identical funds."
status: seedling
---

# Tax efficiency

## Standard

Two funds can hold the same assets and deliver different after-tax results. The differences come from turnover — selling appreciated holdings realises gains that are distributed — and from structure: an ETF's creation and redemption mechanism can reduce in-kind distributions in a way a mutual fund's cash-based redemptions do not.

Tax treatment is jurisdiction-specific, and this leaf does not compute it. What it does is record the facts that determine the drag: distribution history, turnover, the proportion of distributions that were capital gains rather than income, and the fund's structure. Those facts, with a professional's assessment of the jurisdiction, produce the after-tax comparison.

Primary sources: <https://www.irs.gov/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the fund's distribution history and classify distributions as income or capital gains.
- Record turnover and note the relationship between turnover and realised gains.
- Record the structure's effect on distributions where it is disclosed.
- Compare after-tax returns where the fund reports them; otherwise state that they are unavailable.
- Note the jurisdiction and flag the comparison for professional input.
- Where two funds differ materially, record the difference and its likely cause.

## Procedure

1. Pull distribution history for three to five years.
2. Classify each distribution.
3. Record turnover and any realised-gain disclosure.
4. Note structural features that affect distributions.
5. Assemble the comparison facts.
6. Flag the jurisdiction question for professional assessment.

## Anti-patterns

- Comparing pre-tax returns and calling it a selection.
- Assuming all distributions are income.
- Ignoring turnover as a driver of distributions.
- Computing a tax figure in the record.
- Assuming structures behave identically across jurisdictions.

## Done checklist

- [ ] Distribution history pulled and classified.
- [ ] Turnover and realised gains recorded.
- [ ] Structural effects noted.
- [ ] After-tax data recorded or its absence stated.
- [ ] Jurisdiction flagged.
- [ ] Material differences recorded with cause.

## Sources

- Tax administration guidance on investment income: <https://www.irs.gov/>
- Fund distribution disclosure: <https://www.sec.gov/investor>
- Investor education on fund taxation: <https://www.investor.gov/introduction-investing>

The distinction that matters for the comparison is between distributions the holder cannot avoid and gains the holder controls by choosing when to sell. A fund with high turnover converts the second into the first, which is why turnover belongs in the record even when the jurisdiction's treatment is still an open question.

Where the jurisdiction is uncertain, the record should state both the facts and the open question rather than a conclusion; a professional can resolve the question quickly when the underlying distribution history is already tabulated and dated.
