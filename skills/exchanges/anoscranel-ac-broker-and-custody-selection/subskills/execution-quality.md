---
name: execution-quality
domain: investing/execution-quality
trigger: "Measuring the execution a broker actually delivers."
anti_trigger: "Not for choosing order types for a single trade, and not for market-structure theory."
scope: "Routing, best execution, and how to measure the slippage a provider actually delivers."
status: seedling
---

# Execution quality

## Standard

Best execution is an obligation to take reasonable steps, not a promise of the best price, and the difference matters when comparing providers. What can be measured is the slippage actually delivered: the difference between the price at the moment the order was submitted and the price achieved, compared with a benchmark such as the arrival mid or the volume-weighted average over the day.

The measurement requires data the provider may not volunteer, which is why it is done from the investor's own records. A sample of trades with timestamps and fills produces a distribution, and the median and the tail of that distribution say more about a provider than any statement about routing. Where the sample is small, the record says so rather than concluding.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/>.

## Decision rules

- Record the benchmark used: arrival mid, interval VWAP, or closing price.
- Record slippage per trade, then summarise by median and by worst decile.
- Record the sample size and the period; small samples are labelled as such.
- Record any execution venue disclosure the provider publishes, and treat it as a claim.
- Separate slippage from commission and from FX conversion, so the three are not conflated.
- Where a provider's fills cannot be timestamped, record that limitation.

## Procedure

1. Export trades with submission times and fill prices.
2. Obtain a reference price series for the same timestamps.
3. Compute slippage against the chosen benchmark.
4. Summarise by median, decile, and instrument type.
5. Compare with the provider's own disclosures.
6. Record the findings and their limits.

## Anti-patterns

- Judging execution from a single trade.
- Comparing slippage across providers without a common benchmark.
- Blending commission into the slippage figure.
- Treating a provider's execution statistics as audited fact.
- Concluding from a sample that is too small to support it.

## Done checklist

- [ ] Benchmark chosen and recorded.
- [ ] Slippage computed per trade.
- [ ] Median and worst decile reported.
- [ ] Sample size and period stated.
- [ ] Provider disclosures recorded as claims.
- [ ] Limits of the measurement recorded.

The comparison is most useful between two accounts the same investor actually uses, because the benchmark and the instruments are then common; comparing across investors introduces differences in order size and timing that the sample cannot separate.

## Sources

- Order handling and best-execution context: <https://www.sec.gov/investor>
- Industry execution-quality guidance: <https://www.finra.org/>
- Market data for benchmarks: <https://fred.stlouisfed.org/>
