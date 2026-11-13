---
name: fx-leverage-and-margin
domain: investing/fx-leverage-and-margin
trigger: "Setting FX leverage and understanding what a margin call means there."
anti_trigger: "Not for predicting gaps, and not for securities margin."
scope: "Retail leverage caps, margin computation, and the weekend gap."
status: seedling
---

# FX leverage and margin

## Standard

FX margin is usually expressed as a percentage of notional, and retail leverage is capped in many jurisdictions at levels far below what the venue would otherwise offer. The cap matters less than the arithmetic it produces: at fifty-to-one, a two percent move against the position consumes the entire margin, and at twenty-to-one a five percent move does. Those are ordinary weekly ranges in several pairs.

The structure of the risk differs from securities margin in one important way: FX trades nearly continuously during the week and then stops for the weekend, while news does not. A position held over a weekend can gap through its stop when the market reopens, and the loss is realized at the opening price rather than at the stop. That is why weekend exposure is a sizing decision rather than an operational detail.

Primary sources: <https://www.bis.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the leverage offered, the cap that applies, and the margin percentage actually used.
- Compute the adverse move that would consume the margin at the position size.
- Compare that move with the pair's ordinary weekly range.
- Record weekend exposure and the largest gap in the pair's recent history.
- Treat stops as instructions rather than guarantees, and record the slippage assumption.
- Record the venue's margin-close-out procedure and its timing.

## Procedure

1. Record the applicable leverage cap and the venue's margin percentage.
2. Compute the move that exhausts the margin.
3. Compare with the pair's weekly range and with its largest gap.
4. Decide whether the position is held over the weekend, and record why.
5. Record the close-out procedure and the slippage assumption.
6. Write the leverage summary with the gap scenario.

## Anti-patterns

- Choosing leverage because the venue offers it.
- Computing margin from the account balance rather than from notional.
- Assuming a stop bounds the loss through a weekend gap.
- Ignoring the close-out procedure until a margin call arrives.
- Treating an ordinary week's range as the worst case.

## Done checklist

- [ ] Leverage cap and margin percentage recorded.
- [ ] Margin-exhausting move computed.
- [ ] Weekly range and largest gap compared.
- [ ] Weekend holding decision recorded.
- [ ] Close-out procedure recorded.
- [ ] Gap scenario written.

## Sources

- Retail leverage rules and market structure: <https://www.bis.org/>
- Investor education on leveraged currency products: <https://www.investor.gov/introduction-investing>
- Exchange-rate and volatility data: <https://fred.stlouisfed.org/>
