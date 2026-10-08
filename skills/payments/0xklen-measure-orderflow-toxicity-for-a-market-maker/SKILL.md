---
name: measure-orderflow-toxicity-for-a-market-maker
description: Use when a market maker or RFQ quote is bleeding on fills against informed flow: measuring post-fill price drift, adverse selection per size bucket, and setting a cut-off venue or counterparty.
---

# Measure orderflow toxicity for a market maker

Toxic flow is flow that fills you exactly before price moves against your inventory; the measure is not win-rate but the drift of the mid after each fill, split by the counterparty and size that caused it.

## Procedure

1. Record every fill with the mid at fill time from the same venue's book, plus the timestamp. Compute the mid 5 s and 60 s later from the same source.

2. Signed drift for a maker fill: if you bought, adverse drift is `mid_t+ - fill_price` measured downward; if the mid falls after your buy, that fill was toxic. Use a uniformly signed series so winners and losers can be summed.

   ```bash
   python3 -c "d=[-3,-1,2,5,-4,7,-2]; print(sum(d)/len(d))"
   ```

3. Bucket by notional: <$10k, $10k–$100k, >$100k. Retail-sized flow is usually benign; the >$100k bucket carrying positive adverse drift is where the market maker is being picked off.

4. Bucket by counterparty. Pull the taker address per fill and compute mean drift per address. One address with consistently large adverse drift is either informed or running a latency arbitrage against your quotes.

5. Compare against a control: the drift on your own two-sided quotes with no fill. If the unfilled mid also drifts, you are measuring volatility, not toxicity.

6. Set a cutoff. Widen the spread for buckets whose 60 s adverse drift exceeds your half-spread; a bucket where mean adverse drift beats the spread is unprofitable to quote regardless of volume.

7. Re-measure weekly. Toxicity shifts as new searchers arrive; a change in the address mix is a leading indicator of the drift worsening.

## Pitfalls

- Using a single venue's mid to grade fills made on another venue; the cross-venue basis shows up as false toxicity.
- Attributing drift to a taker when the same block contains an unrelated liquidation; strip blocks with abnormal volume before grading.
- Measuring drift at a horizon shorter than the inventory holding period; a 100 ms drift is noise if you hold for minutes.
- Ignoring that a large benign order also moves the mid; check whether the taker's own next trade reverses it, which indicates uninformed flow rather than informed.
- Averaging across the whole book; a small toxic tick can be swamped by high-volume benign flow at a different size.

## Verification

    python3 -c "d=[-3,-1,2,5,-4,7,-2]; print('mean', sum(d)/len(d))"

Group fills by size and by taker, compute mean 60 s signed drift per group, and flag any group whose drift exceeds your half-spread. Report per-bucket drift, the worst counterparty, and the spread change made.
