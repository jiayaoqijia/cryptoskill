# Measuring a protocol's revenue / buyback run-rate

Companion to `references/fee-token-valuation-ceiling.md`. Read this **before reusing any run-rate, P/S or
"priced above its revenue share" conclusion from that page** — see the stale-figures warning at the bottom.

## The rule: measure the counter, never infer it

```python
# 1. read the cumulative counter + its timestamp
# 2. read it AGAIN after a known gap
pace_per_day = (B - A) / elapsed_hours * 24
```

`volume × assumed take rate` is a **guess**, and it is the guess that gets reused for months. On StonkFun
(30 Sep 2026) it understated the real pace ~3×:

| Counter | 12:05 UTC | 14:18 UTC | Δ over 2h13m | Pace |
|---|---|---|---|---|
| `revenue.totalRevenueUsd` | $29.110.000 | $29.222.229 | +$112.229 | **≈$1,2M/day** |
| `revenue.totalBuybackUsd` | $17.390.000 | $17.449.009 | +$59.009 | **≈$640k/day** |
| burn feed, `source == "buyback"` only | — | — | $43.218 in 1h13m | ≈$850k/day |

The vs-volume inference had said $420k/day. Two independent methods (counter delta + burn feed) landing
within ~30% of each other is what makes a run-rate quotable; one inference is not.

## Second witness: the burn ledger

`/api/public/v1/tokens/{mint}/burns` is the cheapest independent check — sum `valueUsdAtBurn` over a window
and divide. **Filter by `source`**: the feed mixes `buyback` (large, every few minutes) with
`quote-revenue` (tiny, the quote asset's transfer tax, ~2% of the total). Unfiltered, the dust dilutes the
buyback rate. Also useful: `lastBurnAt` from *today* proves the flywheel is running right now, which no
promo page can establish.

## Reporting discipline

- Quote the **USD pace** (`$ per day`), never just a token count — the burn count *falls* as price rises,
  which is exactly the confusion bull threads exploit.
- Label it as a **pace, not a settled run-rate** when the window is short or the day is hot (2h on a launch
  day is a spike read, not a trend).
- State the invalidation level: the revenue/day below which the buyback stops mattering.
- Anything derived from a run-rate — P/S, share-parity vs the sector leader, the scenario table — must be
  **recomputed** when the pace changes. A conclusion computed on a 3×-low rate does not survive.

## ⚠️ Stale figures in `fee-token-valuation-ceiling.md` (corrected, not yet edited in place)

That page still carries two numbers this session falsified:

| There | Correct |
|---|---|
| "run-rate ≈ **$420k/day** ≈ $153M/yr"; "P/S ≈ 1,4x"; "share-parity ≈ $140M vs live" | ≈**$1,2M/day** revenue, ≈$640–850k/day buyback → **recompute P/S and share-parity**; the "priced above its revenue share" punchline was built on the 3×-low rate |
| "cheaper than 1% flat only above **~$190** per trade" | break-even is **$95 per swap**; $190 is where FOMO's $0,95 floor stops binding (two different crossovers) — math in `references/execution-venue-fees.md` |

Fix both in place when a foreground session can edit that file.
