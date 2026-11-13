---
name: rebalancing-and-buffers
domain: investing/rebalancing-and-buffers
trigger: "Working out the turnover a methodology implies."
anti_trigger: "Not for predicting returns, and not for fund selection."
scope: "Frequency, buffers, and the turnover the rules imply."
status: seedling
---

# Rebalancing and buffers

## Standard

Rebalancing frequency and the buffer around the selection cut-off together determine how much the index trades. A quarterly rebalance with a hard cut produces a portfolio that changes composition every quarter; the same rules with a buffer that requires a name to fall well below the cut before removal produce far less churn for a similar exposure.

Buffers work by distinguishing the entry threshold from the exit threshold. A security must reach a higher rank to enter and can fall to a lower rank before leaving, which creates a band of stability. The band reduces turnover at the cost of holding names that a strict ranking would have removed, and the record should state both thresholds rather than only the cut.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the rebalancing frequency and the effective dates.
- Record the entry and exit thresholds separately where a buffer exists.
- Estimate the turnover per rebalance from historical changes.
- Record the cost of that turnover at a stated spread assumption.
- Record the stability the buffer provides, in names held across rebalances.
- Record any intra-period adjustment rule, such as for corporate actions.

## Procedure

1. Record the frequency and dates.
2. Record entry and exit thresholds.
3. Estimate turnover per rebalance.
4. Apply a spread assumption for cost.
5. Measure name stability across rebalances.
6. Write the turnover summary.

## Anti-patterns

- Reading only the entry cut-off and assuming the exit is the same.
- Estimating turnover from the number of names changed without their weights.
- Ignoring the cost of rebalancing in the index's documented return.
- Assuming a buffer makes the index static.
- Overlooking intra-period adjustments for corporate actions.

## Done checklist

- [ ] Frequency and dates recorded.
- [ ] Entry and exit thresholds recorded.
- [ ] Turnover estimated.
- [ ] Cost computed at a stated spread.
- [ ] Stability measured.
- [ ] Adjustment rules recorded.

The stability measure is also the one that predicts cost best: an index whose membership changes by a handful of names each rebalance has a very different trading burden from one whose membership turns over by a third, even when both report the same frequency.


The intra-period adjustment rule deserves separate attention for corporate actions, since an index that reconstitutes only at review dates will hold a merged or delisted name in a stale weight until the next date unless the rules address it.


## Sources

- Index methodology disclosure: <https://www.sec.gov/investor>
- Investor education on index rebalancing: <https://www.investor.gov/introduction-investing>
- Market data for turnover estimation: <https://fred.stlouisfed.org/>
