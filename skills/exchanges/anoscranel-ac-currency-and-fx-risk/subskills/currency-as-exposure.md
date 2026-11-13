---
name: currency-as-exposure
domain: investing/currency-as-exposure
trigger: "Treating currency as its own exposure rather than as background noise."
anti_trigger: "Not for forecasting currencies, and not for tactical FX trading."
scope: "Currency as its own exposure: correlation, diversification claims, and the evidence."
status: seedling
---

# Currency as exposure

## Standard

Currency is an exposure with its own return, volatility, and correlation to the rest of the portfolio. Treating it as background noise is a choice, and usually an unintended one: an unhedged global portfolio is partly a bet on the currencies of the markets it holds.

The diversification claim deserves scrutiny. Currency returns are driven by interest differentials, terms of trade, and risk sentiment, and their correlation to equities is unstable — sometimes negative in a crisis, sometimes positive. A currency position that diversifies in one regime can amplify losses in another, and the record should say which regime was tested.

Primary sources: <https://fred.stlouisfed.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record currency exposure as a share of the portfolio by currency, not by asset.
- Compute the portfolio's currency contribution to return and volatility where the data allows.
- Test the currency's correlation to equities across at least two regimes.
- Record whether the exposure is intended or incidental.
- Where the exposure is incidental, record the hedge decision that made it so.
- Do not attribute diversification to currency without the regime-specific evidence.

## Procedure

1. Map holdings to currencies and compute shares.
2. Estimate the currency contribution to return and volatility.
3. Test correlation across at least two regimes.
4. Classify the exposure: intended or incidental.
5. Record the hedge decision behind it.
6. Record the evidence and its regime dependence.

## Anti-patterns

- Treating currency as noise.
- Quoting a correlation from one regime.
- Attributing diversification without testing the stress case.
- Ignoring incidental exposure created by a hedge elsewhere.
- Sizing a currency bet without calling it one.

## Done checklist

- [ ] Exposure mapped by currency.
- [ ] Contribution estimated where data allows.
- [ ] Correlation tested across regimes.
- [ ] Exposure classified intended or incidental.
- [ ] Hedge decision recorded.
- [ ] Evidence and regime dependence recorded.

## Sources

- Exchange-rate and correlation data: <https://fred.stlouisfed.org/>
- Investor education on currency exposure: <https://www.investor.gov/introduction-investing>
- Regulatory context for portfolio disclosure: <https://www.sec.gov/investor>

The honest test is to decompose the portfolio's return into asset and currency components for a period and look at the split. Most investors discover the currency contribution is larger than expected, and that discovery is more useful than any framework for deciding whether to hedge.

The decomposition also reveals hidden concentration: a portfolio spread across ten countries may still have most of its currency exposure in one or two, because the smaller holdings are small in currency terms too. Recording the shares rather than the country count is what makes the concentration visible.
