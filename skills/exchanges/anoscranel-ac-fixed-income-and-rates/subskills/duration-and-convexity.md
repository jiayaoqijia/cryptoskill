---
name: duration-and-convexity
domain: investing/duration-and-convexity
trigger: "Measuring and using interest-rate sensitivity in a bond portfolio."
anti_trigger: "Not for credit risk, and not for rate forecasting."
scope: "Duration as rate sensitivity, convexity as its curvature, and the portfolio arithmetic that follows."
status: seedling
---

# Duration and convexity

## Standard

Duration is the first derivative of price with respect to yield, expressed in years. It answers a practical question: if yields rise by one percentage point, roughly what percentage does the price fall. Modified duration gives the approximation; convexity corrects it for larger moves, and the correction is always in the investor's favour for a plain bond, which is why convexity is described as positive.

Portfolio duration is a weighted average, which makes it useful and slightly deceptive: two portfolios with the same duration can have very different cash-flow timing, and therefore very different behaviour when the curve changes shape rather than shifting in parallel. Duration measures a parallel shift; the curve rarely shifts in parallel.

Primary sources: <https://fred.stlouisfed.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Report modified duration and the price change implied for a one-point move.
- Report convexity where the position is long-dated or the move is large.
- Distinguish Macaulay from modified duration; use modified for price sensitivity.
- Use key-rate durations where the curve's shape matters, not just its level.
- Portfolio duration is recorded with the cash-flow profile, not as a single number.
- Duration matching for a liability is stated with the assumption of a parallel shift.

## Procedure

1. Compute Macaulay and modified duration for each holding.
2. Compute the portfolio's weighted duration and its key-rate exposure.
3. Estimate price change for plus and minus one point, with convexity.
4. Check the estimate against a full re-pricing.
5. Record the cash-flow profile alongside the duration figure.
6. Note where the parallel-shift assumption is load-bearing.

## Anti-patterns

- Using duration as a complete description of rate risk.
- Ignoring convexity on long-dated positions.
- Comparing durations across portfolios with different cash-flow timing.
- Assuming a parallel shift when the curve is twisting.
- Presenting a single duration number for a portfolio with barbell structure.

## Done checklist

- [ ] Duration computed per holding, modified where used for price.
- [ ] Portfolio duration and key-rate exposures computed.
- [ ] Price change estimated with convexity.
- [ ] Estimate checked against full re-pricing.
- [ ] Cash-flow profile recorded.
- [ ] Parallel-shift assumption noted.

## Sources

- Interest-rate data and curve series: <https://fred.stlouisfed.org/>
- Investor education on bond risk: <https://www.investor.gov/introduction-investing>
- Regulatory context for fixed-income risk disclosure: <https://www.sec.gov/investor>

The practical use is portfolio-level: a barbell of very short and very long bonds can match the duration of a bullet portfolio while behaving very differently when the curve twists. That is why duration alone is never the answer to 'what happens if rates move', and why key-rate exposure belongs in the record whenever the portfolio is not a simple ladder.
