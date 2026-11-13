---
name: net-interest-margin
domain: investing/net-interest-margin
trigger: "Reading a bank's spread and funding cost, and its sensitivity to rates."
anti_trigger: "Not for predicting rates, and not for credit quality."
scope: "Spread, funding cost, and the rate sensitivity of a banking book."
status: seedling
---

# Net interest margin

## Standard

Net interest margin is the difference between what a bank earns on assets and what it pays for funding, divided by earning assets. It is the core engine of a traditional bank's earnings, and it moves with the shape of the curve, the mix of the book, and the stickiness of deposits. A high margin can mean good pricing power or a riskier loan book; a low margin can mean efficiency or competition.

The second number that matters is the sensitivity disclosure: what management says happens to net interest income if rates move by a stated amount. Those disclosures are model output, not fact, and they depend on assumptions about deposit betas — how much of a rate rise passes through to depositors. In a rising-rate cycle, a low assumed deposit beta flatters the forecast.

Primary sources: <https://www.federalreserve.gov/> and <https://www.fdic.gov/>.

## Decision rules

- Compute the margin from the disclosed interest income and expense, not from a summary figure.
- Record the funding mix alongside the margin; a margin supported by cheap deposits is different from one supported by wholesale funding.
- Read the rate-sensitivity disclosure with its deposit-beta assumption stated.
- Compare the margin with peers and with its own history through a rate cycle.
- Separate margin changes caused by volume from those caused by price.
- Where sensitivity is not disclosed, record that and treat the margin as unhedged.

## Procedure

1. Extract interest income, interest expense, and earning assets.
2. Compute the margin and its year-on-year change.
3. Record the funding mix and the stated deposit beta.
4. Read the sensitivity table and note the assumptions.
5. Decompose the change into volume and price where disclosure permits.
6. Compare with peers on the same definitions.

## Anti-patterns

- Taking a headline margin without the funding mix.
- Treating a sensitivity disclosure as a forecast.
- Ignoring deposit beta assumptions.
- Comparing margins across banks with different loan books.
- Reading a single quarter as the trend.

## Done checklist

- [ ] Margin computed from income and assets.
- [ ] Funding mix recorded.
- [ ] Deposit beta and sensitivity assumptions noted.
- [ ] Peer and history comparison made.
- [ ] Volume and price effects separated.
- [ ] Undisclosed sensitivity recorded.

## Sources

- Federal Reserve bank performance data: <https://www.federalreserve.gov/>
- FDIC quarterly banking profile: <https://www.fdic.gov/>
- Investor education on bank earnings: <https://www.investor.gov/introduction-investing>
