# Wallet-connect: what the Position entity can and cannot tell us

Measured live against the Uniswap v3 mainnet subgraph on 2026-09-11, before writing any
feature code. These constraints decide the design, so they are written down first.

## The Position entity

    id owner pool token0 token1 tickLower tickUpper liquidity
    depositedToken0 depositedToken1 withdrawnToken0 withdrawnToken1
    collectedFeesToken0 collectedFeesToken1
    feeGrowthInside0LastX128 feeGrowthInside1LastX128 transaction

## Finding 1 — `collectedFees*` is a WITHDRAWAL record, not an EARNINGS record

Sample of 200 live positions with `liquidity > 0`:

| measurement | result |
|---|---|
| `collectedFeesToken0` AND `collectedFeesToken1` both zero | **171 / 200 (85.5%)** |
| distinct owners in sample | 145 |

Then the decisive check — positions whose `collectedFeesToken0` is exactly `0`, asking whether
the fee-growth accumulator is also zero:

| measurement | result |
|---|---|
| positions with `collectedFeesToken0 == 0` | 150 |
| ...of which `feeGrowthInside0LastX128 != 0` | **71 (47.3%)** |

`collectedFees*` only populates when the LP calls `collect()`. Those 71 positions earned fees
and never collected them. **The field measures withdrawals, and its name reads like earnings.**

**Consequence, and it is not negotiable:** wiring `collectedFees*` into realized return would
tell roughly half of all uncollected wallets "you earned $0 in fees" while the chain disagrees.
That is exactly the advertised-APR defect this project exists to expose — a number whose label
has drifted from the thing it measures — reproduced by us, in our own product, pointed at the
user's own money. We do not ship it.

## Finding 2 — `deposited*` / `withdrawn*` are LIFETIME CUMULATIVE, not entry state

| measurement | result |
|---|---|
| one-sided deposits (exactly one of token0/token1 is zero) | **150 / 200 (75.0%)** |
| positions with any withdrawal recorded | 27 / 200 |
| positions with both deposits zero | 0 / 200 |

75% one-sided is not exotic LP behaviour; it is what a cumulative counter looks like. A position
deposited, withdrawn, and re-deposited reports totals that were never simultaneously true. So
`deposited*` cannot be read as "what the position was worth at entry" — which is the single
input a realized-return calculation most needs.

## What this means for the feature

The honest version of wallet-connect is **position discovery**, not a per-position P&L number
derived from fields that do not mean what they are named:

1. **Read the wallet's positions from the subgraph** — `owner`, `pool`, `tickLower`/`tickUpper`,
   `liquidity`. These are reliable and they are the actual point: they tell us WHICH POOLS the
   wallet is in and AT WHAT RANGE.
2. **Convert ticks to a real range width** (`1.0001^tick`), then feed that into the existing,
   tested `positionRealized` path. The user's actual range replaces the assumed +/-2x.
   This is the genuine upgrade: every number on the site until now assumed a range;
   a connected wallet knows it.
3. **Do not compute a fee figure from `collectedFees*`.** Where fees are uncollected, say so
   and mark it unmeasurable. `measurable: false`, never a fabricated 0 — the rule the repo
   already enforces everywhere else.

Entry-time valuation needs `positionSnapshot` or mint-transaction reconstruction. Until that is
built and canaried, per-position realized P&L from a wallet is **not measured**, and the UI must
not imply otherwise.

## Canary for this lane

A position with known uncollected fees must render as "fees uncollected — not measurable from
this data", never `$0`. If it ever renders `$0`, the feature is reproducing the defect and is
broken by definition.
