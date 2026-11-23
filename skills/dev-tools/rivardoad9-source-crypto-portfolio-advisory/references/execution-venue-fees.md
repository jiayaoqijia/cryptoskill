# Execution venue fees — break-even arithmetic

Triggered by: *"mending pakai FOMO atau GMGN"*, *"nominal worth it pakai FOMO berapa"*. The deliverable
is **a break-even number and a ticket-size table**, not a vibe. Re-verify rates before quoting (ref/cashback
codes move them); the ones below were live-checked 30 Sep 2026.

## Structures (per swap)

| Venue | Fee | Note |
|---|---|---|
| GMGN | 1% flat | observed take-rate 0,92–0,99% |
| FOMO | 0,5% **with a $0,95 minimum floor** | floor dominates small tickets |
| Platform UI (e.g. stonkfun.xyz) | launchpad's own | always works for pools it launched |

```python
fomo = max(0.005*t, 0.95)      # floor binds below $190
gmgn = 0.01*t
# round trip = 2× either side → same break-even, double the absolute gap
```

## ⚠️ Two thresholds — never conflate them (this was an actual 2x error, corrected in-session)

- **$95 / swap = the break-even vs GMGN.** Below it GMGN is cheaper, above it FOMO is.
- **$190 / swap = where FOMO's floor stops binding** (0,5% of $190 = exactly $0,95). Below $190 you pay a
  flat $0,95; above it a rising 0,5%.

Calling *$190* "the break-even point" is wrong by 2×. When both a minimum floor and a percentage are in
play, there are always two crossovers — the floor-vs-percentage one and the venue-vs-venue one. Name which
one you mean.

## Table to hand over

| Ticket | per swap: FOMO / GMGN | round trip: FOMO / GMGN |
|---|---|---|
| $25 | $0,95 / $0,25 | $1,90 (7,6%) / $0,50 (2,0%) |
| $50 | $0,95 / $0,50 | $1,90 (3,8%) / $1,00 (2,0%) |
| $95 | $0,95 / $0,95 | **seri** |
| $200 | $1,00 / $2,00 | $2,00 / $4,00 |
| $500 | $2,50 / $5,00 | $5,00 / $10,00 |

## Frequency beats ticket size

20 × $30 round trip: FOMO **$38** vs GMGN **$12** → GMGN saves $26. A flat-% venue wins for anyone who
trades small and often; the per-ticket gap only becomes material above ~$200.

Practical line: **don't switch venues for tickets under ~$200** (the delta is cents). FOMO earns its place
at ≥$200 or phone-only.

## Ranked decision order — fee is LAST

1. **Does the venue route the pool at all?** Quote-paired / xStock-quoted LaunchLab CLMM pools need
   Jupiter routing; a cheaper fee on a terminal that can't reach the pool is worthless.
2. Research + execution on one screen (less copy-paste of data between tools).
3. Chain coverage.
4. Fee.

## The token's own tax dominates the venue delta

A 3% transfer tax on both legs = ~6% round trip vs a venue delta of ~0,3–1%. On a $110 ticket the tax cost
(~$6,60) is **22×** the venue difference ($0,30). Never let venue choice be the headline when the coin is
taxed — say plainly that the choice of coin matters more than the choice of terminal.

## Self-custody

Connect the user's own wallet (Phantom) to a terminal web app. A custodial bot wallet cannot be verified
on-chain, which breaks the standing "verify the wallet on-chain, don't trust the book" rule.
