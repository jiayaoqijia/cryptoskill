# REALIZED — one page, for judges

**ETHOnline 2026 · The Graph — AI Tooling / AI Use Case · also submitted to 1inch**

Live: **[realized.drainfun.xyz](https://realized.drainfun.xyz)** · Deck: **[/deck](https://realized.drainfun.xyz/deck)** · Repo: **[jiggy-cadence/realized](https://github.com/jiggy-cadence/realized)**

---

## The problem, in one sentence

Advertised LP APR is fee income annualized. **It has no price term, so it is positive by
construction** — a pool cannot advertise a loss, no matter what happened to the people in it.

## What we built

Realized return = **fees + impermanent loss** (IL ≤ 0 always), computed live from The Graph's
historical `poolDayData`, served to humans and agents from one implementation of the math.

## Reproduce it in 30 seconds

```bash
# No API key. CORS open. Our server proxies its own Graph key.
curl "https://realized.drainfun.xyz/api/position/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640?entry=2026-07-28&range=2"

# What would closing it cost, right now, with live gas?
curl "https://realized.drainfun.xyz/api/simulate-exit/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640?entry=2026-07-28&stake=25000"
```

## Agent surface (the track deliverable)

| surface | where |
|---|---|
| **MCP server, 7 tools** | `bin/mcp-server.js` — `find_pool` · `realized_return` · `position_realized` · `simulate_exit` · `audit_pools` · `explain_gap` · `rank_pools` |
| **OpenAPI 3.1** | [`/openapi.json`](https://realized.drainfun.xyz/openapi.json) — every route, shape and error code |
| **Agent SKILL** | [`SKILL.md`](SKILL.md) — reporting rules, not just endpoints |
| **llms.txt** | [`/llms.txt`](https://realized.drainfun.xyz/llms.txt) |
| **Library** | `packages/core` — plain ESM, no build step |
| **Test vector in the API response** | real inputs + real expected output, so an agent can verify our math instead of trusting it |

Copy-paste MCP config for Claude Desktop / Cursor is in the [README](README.md#3-or-as-an-mcp-server-for-agents).

## Key numbers, with their ranges

| claim | value |
|---|---|
| Pools advertising positive while LPs realized negative | **37%** of the 102 pools clearing our liveness gate · **141 of 256** tracked overall |
| Across assumed range widths (tight → full) | 62.1% · 55.1% · 46.9% · 37.1% |
| Independent windows tested | **110 of 110** show the defect at tight and moderate ranges |
| Chains · venues | 5 chains · Uniswap v3 + Aerodrome (different codebase, same defect shape) |
| 1inch price cross-check | **99.2% agreement** across 255 pools, median divergence **0.078%** |

## Why The Graph is load-bearing

Not because the data is unreachable by RPC — **we checked that claim and it was wrong.**
`feeGrowthGlobal0X128` is public pool state readable at any historical block (verified against a
live archive node, 2026-09-11). What isn't tractable is the join: a Q128 token-unit accumulator
becomes per-day USD only with an archive node, a block lookup per day boundary, and a historical
price for *both* tokens at each one — repeated per pool. At 256 pools across 5 chains that's
thousands of archive calls per rebuild. The Graph publishes that join already computed.

**The claim is practicality, not impossibility.** We corrected it rather than keep the stronger-
sounding version.

## What refuses to produce a number

| situation | what we return |
|---|---|
| Fees earned but never collected | `measurable: false` + reason — **never `$0`** (of 150 positions reading zero collected, **71 had real accrued fees**) |
| Window too short to price | `measurable: false` + reason |
| Stable-pair canary fails | the build **refuses to write output** |
| Gas/slippage without a verified source | `unavailable` + reason, never a guess |
| Closing a position (not a swap) | slippage is a **measured zero**, not a missing field |

## What we deliberately did *not* ship

We built a pool-selection signal. One split showed **+1.64pt edge** — the flashiest thing we had.
Walk-forward across 112 windows with the scorer deliberately not retuned: **five runs, five
failures** against a pre-registered bar. Then a noise decoy (hash of the pool address) scored
**62.1%** against our real signal's **61.8%** — the decoy won.

So we deleted it and shipped the failure table. **REALIZED reports a track record, never a
forecast.**

## The caveat we quantified instead of hedging

We hold fees constant across range widths, which is unfair to us: concentrated positions earn
more fees in range. Three reviewers asked *how much*. Measured, crediting Uniswap's own
capital-efficiency multiplier (9.47× at tight, 3.41× at moderate):

| range | no credit | theoretical uplift | 2× theoretical |
|---|---|---|---|
| tight (w=1.25) | 62.1% | **44.9%** | 39.1% |
| moderate (w=2) | 55.1% | **37.1%** | 25.0% |

**The defect survives every regime**, including a credit the geometry doesn't justify.
Out-of-range positions receive no uplift — the version least favourable to our own thesis.
Script: [`scripts/fee-uplift-bound.js`](scripts/fee-uplift-bound.js)

## Known limits, stated plainly

- Fees are **pool-level**, not per-position. We report what a representative LP at that range
  earned, not your exact wallet share. The wallet endpoint gives your real *range*, which is the
  input that actually moves the answer.
- Adjacent walk-forward windows share market regime — not fully independent.
- Coverage is Uniswap v3-heavy plus Aerodrome. Venues that can't clear the stable-pair canary are
  **excluded and marked untrusted**, never reported as clean.
- Packages aren't published to npm; the repo is the install path.

## Honesty box

The README carries our own retractions: a headline correlation that didn't reproduce, a v2
formula applied to a v3 venue, a canary that nearly deleted correct code, an annualized figure
that rendered as −988% (impossible — an LP can't lose more than the stake), and a headline whose
denominator didn't match the table below it.

We publish those because a project that has never caught itself being wrong has not been looking.
