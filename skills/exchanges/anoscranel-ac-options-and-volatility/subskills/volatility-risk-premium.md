---
name: volatility-risk-premium
domain: crypto-trading/volatility-risk-premium
trigger: "Assessing the gap between implied and realised volatility and what it pays for."
anti_trigger: "Not for predicting volatility, and not for recommending a position."
scope: "Implied versus realised volatility, selling versus buying volatility, and the tail that pays for the premium."
status: seedling
---

# Volatility risk premium

## Standard

Implied volatility has historically exceeded subsequently realised volatility on average. That gap is the volatility risk premium, and it exists because someone must be paid to bear the risk of a large move. Selling options collects the premium; the seller's compensation is precisely the tail risk they accept.

The honest framing is a trade-off, not an edge. A short-volatility position earns a small, steady amount most of the time and loses a large amount occasionally, and the losses cluster in the moments when liquidity disappears. Any claim that the premium is free must be tested against a maximum-loss statement and a stress scenario, because the average conceals the distribution.

Primary sources: <https://www.cboe.com/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Compare implied with realised volatility over a stated window, and note the measurement method.
- State the maximum loss of any short-volatility structure in full.
- Model a stress scenario with a volatility spike and a gap in the underlying.
- Record the premium collected against the capital at risk.
- Note that short volatility correlates with short credit and short liquidity risk.
- Any strategy claim states its sample and its drawdown, not just its average.

## Procedure

1. Compute implied and realised volatility over the same window.
2. Record the difference and its history.
3. State the maximum loss and the margin requirement of the structure.
4. Run a stress case with a gap and a vol spike.
5. Compute premium collected per unit of capital at risk.
6. Record the trade-off and the conditions under which it fails.

## Anti-patterns

- Presenting the premium as a riskless carry.
- Quoting average returns without the drawdown.
- Sizing a short-vol position without the maximum loss.
- Assuming the historical premium persists.
- Ignoring the correlation between volatility spikes and liquidity.

## Done checklist

- [ ] Implied and realised volatility measured on the same window.
- [ ] Difference and history recorded.
- [ ] Maximum loss and margin stated.
- [ ] Stress case run.
- [ ] Premium per unit of risk computed.
- [ ] Failure conditions recorded.

## Sources

- Options volatility data and research: <https://www.cboe.com/>
- Investor education on options risk: <https://www.investor.gov/introduction-investing>
- Market volatility indices: <https://fred.stlouisfed.org/>

The distribution is the message: a strategy that earns small amounts frequently and loses large amounts rarely has an attractive average and an unattractive survival profile. Writing the drawdown and the recovery arithmetic next to the average keeps the record honest about which of the two the holder is actually exposed to.
