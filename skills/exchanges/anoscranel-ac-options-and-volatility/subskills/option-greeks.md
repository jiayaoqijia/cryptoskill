---
name: option-greeks
domain: crypto-trading/option-greeks
trigger: "Reading and aggregating an option position's sensitivities."
anti_trigger: "Not for predicting the underlying, and not for pricing models."
scope: "Delta, gamma, theta, and vega, and the portfolio-level aggregation of each."
status: seedling
---

# Option greeks

## Standard

The four first-order sensitivities describe different risks. Delta measures the change in price for a small move in the underlying. Gamma measures how delta itself changes, which is why a delta-neutral book can become directional after a large move. Theta measures the decay of time value, which is income for the seller and cost for the buyer. Vega measures sensitivity to implied volatility, which moves independently of the underlying.

Reading them together is the point. A position can be delta-neutral, gamma-negative, theta-positive, and vega-negative: it earns carry in calm markets and loses sharply in a move, which is exactly the short-volatility profile. Stating only delta hides that.

Primary sources: <https://www.cboe.com/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record all four greeks for the position and aggregate them across the book.
- Note the sign of gamma explicitly; a short-gamma book needs a stated maximum loss.
- Theta is recorded as a daily amount, not as a percentage, so its size is visible.
- Vega is recorded against a stated vol move, typically one point.
- Greeks are re-read after any large underlying move, because they are local.
- Where the model's assumptions are questionable, record the model and its limits.

## Procedure

1. Pull the position's greeks from the venue or model, with the model named.
2. Aggregate delta, gamma, theta, and vega across the book.
3. Convert theta to a daily currency amount and vega to a one-point move.
4. Identify the dominant risk among the four.
5. Recompute the greeks under a large underlying move.
6. Record the sensitivity summary with the model and date.

## Anti-patterns

- Reporting delta alone.
- Treating greeks as constants across a move.
- Quoting theta as an annual percentage.
- Ignoring vega in a position whose thesis is about volatility.
- Using a model without stating its assumptions.

## Done checklist

- [ ] Four greeks recorded per position and aggregated.
- [ ] Gamma sign and maximum loss stated where short.
- [ ] Theta in daily currency.
- [ ] Vega per vol point.
- [ ] Greeks recomputed under a large move.
- [ ] Model and date recorded.

## Sources

- Options industry education and market data: <https://www.cboe.com/>
- Investor education on options risk: <https://www.investor.gov/introduction-investing>
- Regulatory context for options disclosure: <https://www.sec.gov/investor>

Greeks that are recomputed after every material move are worth more than greeks computed once: the numbers describe a local surface, and a position's risk can change sign after a gap. The record's job is to keep the recomputation cheap by storing the model and the inputs alongside the results.
