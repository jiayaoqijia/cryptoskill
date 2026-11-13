---
name: order-book-imbalance
domain: investing/order-book-imbalance
trigger: "Reading displayed depth and its changes as evidence."
anti_trigger: "Not for predicting price, and not for identifying participants."
scope: "Depth imbalance, spoofing tells, and why displayed liquidity is not real liquidity."
status: seedling
---

# Order book imbalance

## Standard

The order book shows the size resting at each price, and the imbalance between bid and ask depth is widely read as a short-term signal. The reading assumes the displayed size is genuine. Often it is not: quotes can be cancelled before they trade, sizes can be displayed on one side to influence perception while the real order executes elsewhere, and depth can be refreshed faster than a human can respond.

The honest approach measures persistence rather than a snapshot. Depth that remains available through several price changes is different from depth that disappears as the price approaches it, and the difference is measurable by sampling the book repeatedly rather than reading it once. The record should state the sampling interval and what happened to the depth when the price moved toward it.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/>.

## Decision rules

- Record the sampling interval and the depth measure used.
- Record the imbalance at each sample and the persistence across samples.
- Record the depth's behaviour as the price approaches it: absorbed, cancelled, or refilling.
- Record the trade-through rate against the displayed size.
- Record the venue of the displayed quotes, since dark liquidity is not shown.
- Record the spoofing tell: large displayed size that disappears without trading.

## Procedure

1. Sample the book at a stated interval.
2. Compute the depth imbalance per sample.
3. Measure persistence across samples.
4. Track the depth as the price moves toward it.
5. Compare displayed size with traded size.
6. Write the observation with the sampling stated.

## Anti-patterns

- Reading a single snapshot as the state of the book.
- Treating displayed depth as executable size.
- Ignoring cancellations, which look like depth until they vanish.
- Comparing imbalances across names with different tick sizes.
- Concluding manipulation from one observation.

## Done checklist

- [ ] Sampling interval and measure recorded.
- [ ] Imbalance per sample computed.
- [ ] Persistence across samples measured.
- [ ] Depth behaviour near the price recorded.
- [ ] Displayed versus traded size compared.
- [ ] Observation written with the sampling.

The measure also depends on what is counted as depth: orders at the touch, orders within a few ticks, and total displayed size produce different imbalances from the same book, and a comparison between two names is only meaningful when both are measured the same way. The record should state the depth definition as precisely as it states the sampling interval.


## Sources

- Market structure and order handling: <https://www.sec.gov/investor>
- Trading practice guidance: <https://www.finra.org/>
- Investor education on market structure: <https://www.investor.gov/introduction-investing>
