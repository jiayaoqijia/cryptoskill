---
name: auctions-and-halts
domain: investing/auctions-and-halts
trigger: "Understanding auction mechanics and trading halts before relying on them."
anti_trigger: "Not for predicting opening prices, and not for choosing a security."
scope: "Opening and closing auctions, limit-up and limit-down halts, and circuit breakers."
status: seedling
---

# Auctions and halts

## Standard

The opening and closing auctions concentrate a day's liquidity into two moments, and they set prices that everything else references. The closing auction in particular has become the largest liquidity event of the day for many instruments, which is why orders that arrive late can move it and why the published indicative price before the close is watched so closely.

Halts are the other mechanism. A limit-up/limit-down band pauses trading when the price moves too far too fast, and market-wide circuit breakers pause everything at stated thresholds. A halt is not a signal about value; it is a procedural stop, and the resumption auction is where the price discovery happens.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record whether the order is intended for the auction or for continuous trading; they are different markets.
- For auction orders, record the indicative price and the imbalance where published.
- Never assume a halt will be short; plan for the resumption and the gap.
- Record the halt reason class if published, without inferring more than the exchange states.
- Orders resting through a halt are re-evaluated at resumption; a pre-halt price is not a price.
- Circuit-breaker thresholds are recorded as rules, not as predictions.

## Procedure

1. Identify the trading session the order targets.
2. For auctions, record the indicative price and any published imbalance.
3. For a halted instrument, record the halt time, class, and expected resumption.
4. Decide whether existing orders should stand or be cancelled before resumption.
5. Record the decision and its reasoning before the auction or resumption.
6. Verify execution against the auction print.

## Anti-patterns

- Treating the last pre-halt trade as the current value.
- Sending market orders into a reopening auction without checking the indicative price.
- Assuming a halt protects the price from gapping.
- Ignoring the closing auction when sizing an exit.
- Inferring news from a halt when the exchange published only a procedural reason.

## Done checklist

- [ ] Target session identified.
- [ ] Auction indicatives recorded where applicable.
- [ ] Halt class and resumption recorded.
- [ ] Stand-or-cancel decision recorded before the event.
- [ ] Execution verified against the print.

## Sources

- Regulatory context for auctions and halts: <https://www.sec.gov/investor>
- Investor education on trading mechanics: <https://www.investor.gov/introduction-investing>
- Exchange-rule context for circuit breakers: <https://www.finra.org/rules-guidance>

The practical rule is to know, before the session, which of your orders would be affected by an auction or a halt, and what you want to happen to them. Most of the damage in these events comes from orders nobody thought about, resting in the book when the mechanism fired.
