---
name: snapshot-fx-rates-at-posting-time
description: Use when amounts cross currencies and a ledger must stay reproducible. Stores the FX rate used at the moment of posting and never restates a past conversion with a newer rate.
---

# Snapshot FX rates at posting time

A foreign amount must be converted at the rate in effect when it was posted, then frozen. Recomputing last quarter's total with today's rate changes closed books — a restatement you did not intend.

## Procedure

1. At post time fetch the rate from a named source with a timestamp: `{"pair":"EUR/USD","rate":1.0873,"as_of":"2026-10-08T14:00:00Z","source":"ecb"}`.
2. Store the rate **and** the source and timestamp on the row, alongside the source amount, so the conversion is reproducible without re-querying the feed.
3. Store the rate as a scaled integer or exact decimal (say 8 dp), never a float: `rate_e8 = 108_730_000`. Reconstruct as `value / 10**8` only for display.
4. Convert with the snapshot: `usd_minor = mulDiv(eur_minor, rate_e8, 10**8)`, rounded once, for the base-currency figure.
5. Never join a past transaction to the current rate table; the rate table is a time series and you already captured the point.
6. If a rate is unavailable, block the post rather than defaulting to a stale value silently; record the gap.
7. For a base-currency report, sum the stored base amounts (each converted at its own row's rate), not the sum of foreign amounts times today's rate.
8. Keep both the transaction amount and the base amount; an FX gain/loss report needs the pair.
9. Store the precision the rate was published to, so a display layer never implies more precision than the source had.
10. For a revaluation, compute the delta between the posting rate and the closing rate explicitly; a silent restate hides the gain or loss.
11. Reject a rate of zero or a negative — both are feed errors, not prices.
12. Version the feed; if a provider corrects history, record that you deliberately kept the original snapshot.

## Pitfalls

- Re-running a report with a live feed produces different totals each day; only the snapshot is authoritative.
- A timezone-less `as_of` lets two systems pick different rates for the "same" moment; always store UTC.
- Using the mid rate when the posting applied a bid/ask or a card-network rate invents a spread; store the rate that was actually applied.
- A float rate multiplies a float into money; keep the rate exact and the product in integer arithmetic.
- Round-tripping (EUR -> USD -> EUR) with a single-direction rate loses the spread and drifts; store direction pairs.
- Fetching the rate inside a transaction that then rolls back can leave the stored snapshot orphaned; fetch, then post, then commit.

## Verification

    psql -c "SELECT COUNT(*) FROM txn WHERE rate_e8 IS NULL AND currency <> 'USD'"   # expect 0 for posted rows
    python3 -c "print((100_00 * 108_730_000) // 10**8)"   # 1.0873 * 100.00 -> reproducible

Pass when every foreign posting carries a rate, source and UTC timestamp. Report the rate source and a reproduced conversion.
