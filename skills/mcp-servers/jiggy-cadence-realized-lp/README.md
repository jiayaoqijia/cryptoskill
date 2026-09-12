# REALIZED

<!-- Judge front door. The repo root carries build notes next to judge docs because the
     README permalinks cite exact line numbers (v4.js#L101-L194 etc.) and moving files hours
     before a deadline breaks those anchors for cosmetic gain. This map is the fix instead. -->

### Start here

| if you are… | read | why |
|---|---|---|
| **judging, 2 minutes** | [`FOR-JUDGES.md`](FOR-JUDGES.md) | problem, method, key numbers with ranges, 30-second reproduction |
| **judging The Graph — AI track** | [`SKILL.md`](SKILL.md) + [`llms.txt`](llms.txt) | the agent surface: 7 MCP tools, reporting rules |
| **judging The Graph — composability** | [`COMPOSABILITY.md`](COMPOSABILITY.md) | one query shape across 3 protocols / 4 chains / 6 venue-chain pairs |
| **judging Uniswap** | [`FEEDBACK.md`](FEEDBACK.md) + [Verify our integration](#verify-our-integration--every-claim-at-its-line) | developer feedback citing Uniswap's own schema; every claim at its line |
| **running it** | [Use it in 30 seconds](#use-it-in-30-seconds) | no API key needed, CORS open |
| **checking our honesty** | [Honesty box](#honesty-box) · [Canaries](#canaries) | our own retractions, and the failure we shipped instead of a signal |

**Repo layout**

```
packages/core/src/   the library — all math and subgraph access (start at realized.js, v4.js)
bin/                 api.js (HTTP) · mcp-server.js (7 agent tools)
scripts/             build-*.js regenerate everything; spike-hunt*/probe-* are the
                     experiments we ran and published as failures, kept on purpose
data/                generated corpora + the evidence behind published findings.
                     Large and tracked deliberately — see REVIEW-GUARDRAILS.md before grepping
test/                canary.test.js — the negative control this project exists for
```

> **TL;DR** — Every DEX shows liquidity providers an APR made only of fees, so it can never
> display a loss. Realized computes the number that can: **fees + impermanent loss**, from The
> Graph's historical `poolDayData`. Live site: **[realized.drainfun.xyz](https://realized.drainfun.xyz)**
> · library: `packages/core` · MCP server: `bin/mcp-server.js` (7 tools)
>
> **Judging this?** [`FOR-JUDGES.md`](FOR-JUDGES.md) is the one-page version: problem, method,
> key numbers with their ranges, what refuses to produce a number, what we deliberately did
> *not* ship, and a 30-second reproduction.
>
> **Uniswap judges:** [`FEEDBACK.md`](FEEDBACK.md) is our developer feedback on the v3 and v4
> subgraphs — what worked, and the four things that cost us build time, each with the file and
> line it produced. Integration points to verify are listed at the bottom of that file.

**The problem.** You provide liquidity, the dashboard says +12% APR, and months later your
position is worth less than if you had done nothing. The dashboard was not lying about fees —
it simply has no term for price. Advertised APR is fee income annualized, so it is *positive by
construction*.

**The solution.** Realized adds the missing term. Give it a pool and an entry date; it returns
what an LP actually took home, next to what was advertised, with the gap named.

**Why it's credible.** Every number is recomputed live from The Graph and regenerable end-to-end
by [`scripts/build-corpus.js`](scripts/build-corpus.js). On live Uniswap v3 data, **34–62% of
pools advertised a positive APR while LPs went backwards** — and the share rises the tighter
your range.

### A real position

```
USDC/WETH · entered 2026-07-28 · held 45 days · ±2x range

  advertised APR      +2.58%   ← what the DEX showed
  fees earned         +0.48%
  impermanent loss    -2.57%
  ------------------------------
  realized           -16.95% annualized   ← what you actually made
```

In range the entire time. No liquidation, no exotic pair. The advertised number was not
wrong about fees; it was structurally incapable of showing the loss.

Those figures are live, so they move as the window slides. Reproduce them yourself:

```bash
curl "https://realized.drainfun.xyz/api/position/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640?entry=2026-07-28&range=2"
```

### Who this is for

| you are | you get |
|---|---|
| **an LP** | the real number for a position you already hold, at your entry date and range |
| **a dashboard / protocol team** | an API + npm package so your UI can stop showing a metric that cannot go negative |
| **an AI agent** | an MCP server whose tools answer "did this pool actually pay?" instead of reciting APR |

### Use it in 30 seconds

```bash
# 1. Ask the live API (no key, no install)
curl "https://realized.drainfun.xyz/api/position/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640?entry=2026-07-28&range=2"

# 1b. Don't know your range? Read it off-chain from your address (read-only, no signing)
curl "https://realized.drainfun.xyz/api/wallet/0xYourAddress"

# 2. Or in code — the math is a standalone package in this repo
git clone https://github.com/jiggy-cadence/realized && cd realized && npm install
```

```js
// packages/core is self-contained: no build step, no bundler, plain ESM.
import { gatewayUrl, fetchPoolFrom, positionRealized } from './packages/core/src/index.js';
const pool = await fetchPoolFrom(gatewayUrl(process.env.GRAPH_API_KEY), poolId, entryTs);
positionRealized(pool, 2).realizedReturnPct;   // the number your dashboard can't show
```

### 3. Or as an MCP server, for agents

Paste this into Claude Desktop (`claude_desktop_config.json`), Cursor (`.cursor/mcp.json`), or any
MCP client, then restart it:

```jsonc
{
  "mcpServers": {
    "realized": {
      "command": "node",
      "args": ["/absolute/path/to/realized/bin/mcp-server.js"],
      "env": { "GRAPH_API_KEY": "your-subgraph-studio-key" }
    }
  }
}
```

**7 tools:** `find_pool` · `realized_return` · `position_realized` · `simulate_exit` ·
`audit_pools` · `explain_gap` · `rank_pools`

A free Graph key comes from [Subgraph Studio](https://thegraph.com/studio/). **Or skip the key
entirely** — every tool above is also a plain HTTP GET against our server, which proxies its own
key:

```bash
curl "https://realized.drainfun.xyz/api/find?q=WETH/USDC"
```

Ask your agent: *"I entered the USDC/WETH 0.05% pool on 2026-07-28 at a ±2x range. What did I
actually make, and what would it cost me to close?"*

Machine-readable spec for every endpoint: **[`/openapi.json`](https://realized.drainfun.xyz/openapi.json)**
(OpenAPI 3.1) — so an agent never has to guess a request shape or an error code.

### Deciding whether to exit, not just checking the score

```bash
curl "https://realized.drainfun.xyz/api/simulate-exit/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640?entry=2026-07-28&range=2&stake=25000"
```

Same math as `position_realized`, reframed around the moment of deciding: net dollars on a
stated stake, today — now including what it actually costs to get out.

**Gas is measured.** Live gas price from 1inch × estimated units for `decreaseLiquidity` +
`collect` (~270k), priced in the chain's native token. The price is live; the units are an
estimate, so the figure ships with `isEstimate: true` rather than posing as exact.

**Slippage on a plain close is zero — and that zero is measured, not missing.** Closing a v3
position isn't a swap: you get *both* tokens back at the current tick, so there's no price
impact. Slippage only appears if you then consolidate into one token:

```bash
curl "https://realized.drainfun.xyz/api/simulate-exit/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640?entry=2026-07-28&stake=25000&consolidate=true"
```

That estimate is an explicit **lower bound** — modelled against total pool TVL, while a
concentrated pool's depth at the active tick is thinner, so real impact is likely higher.

`netAfterCostsUsd` is `null` unless *both* costs are known. A partial subtraction dressed as a
complete number is the exact defect this project exists to expose.

### Your real range, not an assumed one

Every realized number needs a range width, and `±2×` is a guess. Paste an address and we read the
band you actually set:

```bash
curl "https://realized.drainfun.xyz/api/wallet/0xYourAddress"
```

**Read-only — no signing, no wallet connection, no permissions.** It is a subgraph lookup against a
public address. You get each open position's real `tickLower`/`tickUpper`, a derived `range.widthX`
to feed straight into `/api/position/`, and a plain-language label for humans.

It is position **discovery**, not per-position P&L — and that is a measured decision, not a missing
feature. Two Position fields look like they'd hand you fees and entry value. Both are traps:

- `collectedFees*` is a **withdrawal** record, not an earnings record — it populates only when the
  LP calls `collect()`. Measured live: of 150 positions with `collectedFeesToken0 == 0`, **71 had
  non-zero `feeGrowthInside0LastX128`**. They earned fees and never collected. So uncollected fees
  report `measurable: false` with a reason and **never `$0`** — a fabricated zero is a number whose
  label lies, which is the precise defect this project exists to expose, aimed at the user's own
  money.
- `deposited*`/`withdrawn*` are **lifetime cumulative**, not entry state — 75% of live positions
  read as one-sided because of it. They ship namespaced under `cumulative` and must not be read as
  position value.

Every response carries a `limits` block stating both, and token `decimals` ship beside every raw
amount so no consumer has to guess a divisor.

### What we do NOT claim

The narrow claim is the strong one, and it is the only one we make:

- **We do not claim "LPs lose to HODL."** Sometimes they do, often they don't. Not our finding.
- **We claim the advertised metric is systematically uninformative** about realized outcomes
  for concentrated positions — and we measure it live rather than asserting it.
- **Fee uplift for concentrated ranges is not modelled.** Tighter positions earn more fees than
  we credit them, so tight-range losses shown here are **lower bounds**. The direction is
  robust; treat tight-range magnitudes as bounded, not exact.
- **Fees are pool-level, not per-position.** We cannot see your individual liquidity share, so
  this is what a representative LP at that range earned, not your exact wallet. `/api/wallet/`
  gives us your real *range*, which is the input that actually moves the answer — it does not
  give us your fees, and we refuse to invent them (see below).
- **IL is computed closed-form** from entry/exit price ratio, not by replaying every rebalance.

Full limitations, sensitivity across gates, and a retracted claim we killed ourselves are in
[Honesty](#honesty-what-we-checked-and-what-we-retracted) below.

---

## The defect

Advertised APR is fee income, annualized. It has no price term. So it is **positive by
construction**: a pool cannot advertise a loss, no matter what happened to the people in it.

Realized return = fee income **+ impermanent loss** (IL is always ≤ 0).

This isn't academic. Our own trading stack scored an LP position `+1.7% WIN` when the real
outcome was about **−14%**, because resolution was fee-only and arithmetically could not lose.
That call is the negative control in [`test/canary.test.js`](test/canary.test.js) — the test
that failure never had.

## Verify our integration — every claim, at its line

*For Uniswap and The Graph judges: this table is the map. Each row is a claim we make somewhere
else in this README, next to the exact code that implements it.*

### Uniswap stack integration

| what we integrated | where, exactly |
|---|---|
| **Uniswap v3 subgraph IDs, 4 chains** (mainnet, Arbitrum, Polygon, Base) | [`venues.js:10-15`](packages/core/src/venues.js#L10-L15) |
| **Uniswap v4 subgraph ID** (mainnet) | [`venues.js:20-22`](packages/core/src/venues.js#L20-L22) · [`v4.js:30`](packages/core/src/v4.js#L30) |
| **v3 position-state read** — the range is on the NFT, so `tickLower`/`tickUpper` is a lookup | [`wallet.js:121-144`](packages/core/src/wallet.js#L121-L144) (`POSITION_FIELDS`) · fetch at [`wallet.js:146`](packages/core/src/wallet.js#L146) |
| **v4 position reconstruction** — the v4 `Position` entity has no tick range, so we replay events | [`v4.js:101-194`](packages/core/src/v4.js#L101-L194) (`reconstructPositions`) |
| **v4 paging by `origin`, not `sender`** (`sender` is the position manager contract — returns zero rows) | [`v4.js:39-93`](packages/core/src/v4.js#L39-L93), query at [`v4.js:58`](packages/core/src/v4.js#L58) |
| **v4 `amount: 0` filter** — ~48% of events are fee-collection no-ops; counting them invents positions | [`v4.js:107`](packages/core/src/v4.js#L107) and [`v4.js:216`](packages/core/src/v4.js#L216) |
| **v4 transferred-in positions** — net-negative keys classified, size withheld | [`v4.js:140-153`](packages/core/src/v4.js#L140-L153) (`incompleteHistory`) |
| **v4 self-audit shipped in every response** (`audit.checks[]` + `allPass`) | [`v4.js:196-251`](packages/core/src/v4.js#L196-L251) (`auditReconstruction`) |
| **Per-venue capability map** — v4 is `realizedReturn:false, exitSimulation:false` on purpose | [`venues.js:38-74`](packages/core/src/venues.js#L38-L74) (`CAPABILITIES`) |
| **Concentrated-liquidity IL math** (v3/v4 range geometry, not the v2 formula) | [`concentrated.js:17-54`](packages/core/src/concentrated.js#L17-L54) |
| **Developer feedback for the Uniswap track** | [`FEEDBACK.md`](FEEDBACK.md) |

### The Graph integration

| what | where, exactly |
|---|---|
| **Gateway URL built from a Subgraph Studio key** (live data, no mocks) | [`realized.js:43-46`](packages/core/src/realized.js#L43-L46) (`gatewayUrl`) |
| **The single query function every venue and chain goes through** | [`realized.js:48-69`](packages/core/src/realized.js#L48-L69) (`query`) |
| **`poolDayData` historical fetch** — the join that makes realized return computable | [`realized.js:86-166`](packages/core/src/realized.js#L86-L166) |
| **Realized return = fees + IL**, one implementation for all venues/chains | [`realized.js:251-321`](packages/core/src/realized.js#L251-L321) (`positionRealized`) |
| **Exit simulation** with live gas and measured-zero slippage | [`realized.js:168-249`](packages/core/src/realized.js#L168-L249) |
| **Venue/chain resolution** — one map, not one code path per chain | [`venues.js:81-89`](packages/core/src/venues.js#L81-L89) (`subgraphId`, `venueList`) |
| **MCP server, 7 tools** | [`bin/mcp-server.js`](bin/mcp-server.js) — tool defs at lines [24](bin/mcp-server.js#L24), [44](bin/mcp-server.js#L44), [73](bin/mcp-server.js#L73), [104](bin/mcp-server.js#L104), [136](bin/mcp-server.js#L136), [155](bin/mcp-server.js#L155), [167](bin/mcp-server.js#L167) |
| **HTTP API** (`/api/wallet`, `/api/position`, `/api/simulate-exit`, `/api/venues`) | [`bin/api.js`](bin/api.js) — venue dispatch + address validation at [`api.js:216-240`](bin/api.js#L216-L240) |

### The refusals — where we decline to produce a number

These are the lines that make the honesty claims checkable rather than rhetorical.

| refusal | where |
|---|---|
| **Uncollected fees → `measurable:false`, never `$0`** (of 150 positions reading zero collected, 71 had real accrued fees) | [`wallet.js:174-200`](packages/core/src/wallet.js#L174-L200) (`describePosition`), rationale at [`wallet.js:241`](packages/core/src/wallet.js#L241) |
| **Truncated v4 event history → `openPositions:null`**, positions withheld entirely | [`v4.js:253-300`](packages/core/src/v4.js#L253-L300) (`walletV4`) |
| **Aerodrome wallet lookup → explicit error** (no per-owner Position entity) | [`venues.js:64-72`](packages/core/src/venues.js#L64-L72) · [`api.js:229`](bin/api.js#L229) |
| **Malformed address → `400` on every venue path** | [`api.js:216-232`](bin/api.js#L216-L232) |
| **Stable-pair canary fails → the build refuses to write output** | [`test/canary.test.js`](test/canary.test.js) |

---

## What this is

An MCP server + library that computes **realized** LP return from The Graph's historical
`poolDayData`, and compares it to the advertised number.

- `realized_return(pool)` — fees, IL, realized vs advertised, for one pool
- `audit_pools(n)` — corpus-wide scan with sensitivity + canary
- `explain_gap(pool)` — where the difference came from

Why The Graph specifically: per-day fee totals in USD are **derived aggregates** produced by
the indexer.

**Could you get this from an RPC node instead?** Partly, and we checked rather than asserted.
`feeGrowthGlobal0X128` is public state on every v3 pool, readable at any historical block —
verified live against an archive node on 2026-09-11. So fee *accrual* is reconstructible.

What isn't cheap is everything after that. The accumulator is a Q128 value in token units, so
per-day USD requires an archive node, a block lookup for each day boundary, a historical price
for **both** tokens at each boundary, and the whole thing repeated per pool. For a 256-pool,
5-chain, daily-resolution corpus that is thousands of archive calls per rebuild.

So the honest claim is **practicality, not impossibility**: The Graph publishes that join
already computed and consistent across every pool we measure. An earlier version of this README
said "there is no RPC path," which was too strong — corrected here for the same reason the rest
of this project exists.

## Findings (live, reproducible)

Regenerate everything with `GRAPH_API_KEY=... node scripts/build-corpus.js` →
[`data/corpus.json`](data/corpus.json). Diff it against the subgraph yourself.

### The defect survives every knob we can turn

Uniswap v3 LPs **concentrate** their liquidity into a price band. Inside a band, impermanent
loss is amplified; once price leaves the band you are fully converted into the losing asset and
the loss is no longer "impermanent" at all. Full-range is therefore the **most generous possible
case for the pool** — so we report every range, and the finding has to survive all of them.

| range (±width) | median IL | median realized | knocked out of range | advertised + while real − |
|---|---|---|---|---|
| tight ±1.25x | −1.28% | −0.86% | 25/102 | **62%** |
| moderate ±2x | −0.46% | −0.04% | 0/102 | **50%** |
| wide ±4x | −0.27% | +0.02% | 0/102 | **45%** |
| full-range (v2-equivalent) | −0.13% | +0.06% | 0/102 | **34%** |

Every row is the same 102 live volatile pools over the same 30-day window. Only the assumed
LP range changes. The direction never flips: **the tighter and more realistic your position,
the more the advertised number lies to you.**

> The fee term is held constant across ranges, which is deliberately unfair to us —
> concentrating earns more fees too, so some of that IL is earned back. We did not model the
> fee uplift because we cannot measure per-position fees from pool-level data. The
> **direction** of the defect is what survives; treat the magnitudes as bounded by that caveat.

### It is not one lucky month, and it is not one chain

Every number above came from a single 30-day window ending the day we ran it — one draw.
"34–62% of pools mislead" could have been a fact about DeFi or a fact about August 2026, and
nothing in the repo could tell the difference. So we re-ran the whole instrument twice more.

**Stability check** ([`scripts/walk-forward.js`](scripts/walk-forward.js) →
[`data/walkforward.json`](data/walkforward.json)): 13 overlapping 30-day windows over 210 days of
mainnet. 13 of 13 trusted, 0 untrusted, defect present in every one — tight-range min 44%,
median 59%, max 69%.

> Those 13 windows step every 15 days but span 30, so adjacent windows share half their data.
> They are **not** independent samples. It is a stability check, not a hypothesis test.

**Independent months, four chains** ([`scripts/history-run.js`](scripts/history-run.js) →
[`data/history.json`](data/history.json)): strictly **non-overlapping** 30-day tiles — no shared
days, so the window count is a real sample count.

| chain | trusted months | oldest | tight ±1.25x | moderate ±2x | full-range |
|---|---|---|---|---|---|
| mainnet | 30 | 2024-04-20 | 26–69% (med 54%) | 23–57% (med 39%) | 11–43% (med 23%) |
| arbitrum | 30 | 2024-04-20 | 31–87% (med 60%) | 14–75% (med 46%) | 3–58% (med 26%) |
| base | 27 | 2024-04-20 | 55–95% (med 67%) | 38–82% (med 54%) | 18–57% (med 33%) |
| polygon | 23 | 2024-04-20 | 17–92% (med 56%) | 4–91% (med 43%) | 0–68% (med 21%) |

**110 independent monthly windows across 4 chains.** The defect is present on every chain and in
nearly every month. Base is worst: its *best* month still had 55% of pools advertising a positive
APR to a tight-range LP who lost money.

**No Wayback Machine required.** We were about to reconstruct history by scraping archived DeFi
dashboards. Checked the primary source first: `poolDayData` reaches **2021-05-05** on mainnet
(1,952 days for USDC/WETH). The subgraph carries full history natively — no archive gaps, no HTML
parsing, no third-party copy. One query saved an entire subsystem.

**Chains reported as unavailable, never as clean.** Optimism's subgraph answers, but only 29 pools
clear the TVL floor, leaving n=12 per window — below our n≥20 bar, so all 30 windows are marked
`trusted: false` and **no Optimism number is quoted anywhere**. BNB, Celo and Avalanche return
`bad indexers` / `no allocations` on the decentralized network. A chain we could not measure is
never reported as a chain without the defect.

### Not a Uniswap artifact

Everything above is Uniswap v3. If the defect lived only there, the honest headline would be
"Uniswap's advertised APR is broken" — a much smaller claim. So we ran the **same instrument,
unchanged**, on an independent DEX: [`scripts/cross-dex.js`](scripts/cross-dex.js) →
[`data/cross-dex.json`](data/cross-dex.json).

| venue | chain | trusted months | tight ±1.25x | moderate ±2x | full-range |
|---|---|---|---|---|---|
| **Aerodrome Slipstream** | base | 24 | 23–69% (med 51%) | 12–63% (med 30%) | 0–43% (med 16%) |

Different team, different codebase, different incentive model (veAERO emissions rather than pure
fee capture) — **same defect, same shape, same range-ordering.** It is a property of how
concentrated liquidity advertises itself, not a quirk of one DEX.

### What each venue can actually answer

Not every venue supports every question, and the differences are not cosmetic — they come from
what the subgraph exposes. `/api/venues` publishes this as booleans so an agent can **check**
capability instead of assuming it.

| venue | chains | source | pool analytics | wallet lookup | real range | realized return | exit sim |
|---|---|---|---|---|---|---|---|
| **Uniswap v3** | mainnet, arbitrum, polygon, base | position **state** | yes | yes | yes | **yes** | **yes** |
| **Uniswap v4** | mainnet | **event reconstruction** | yes | yes | yes | **no** | **no** |
| **Aerodrome** | base | pool-only | yes | **no** | — | — | — |

**Why v4 is a different kind of answer.** The v4 `Position` entity carries only
`id`/`tokenId`/`owner`/`origin`/`createdAtTimestamp` — **no tick range at all.** In v3 the range
sits on the position NFT, so reading "the band you actually set" is a lookup: the chain already
did the bookkeeping. In v4 the range exists only in the event log, so we reconstruct it by summing
signed `ModifyLiquidity.amount` per `(pool, tickLower, tickUpper)`.

That is bookkeeping, not new mathematics — and it is worth being precise about what it buys and
what it costs. It supports the range and in/out-of-range. It does **not** support realized return
or exit pricing, and we refuse to compute them rather than publish a confident wrong number:
**event-derived state is a strictly weaker evidence class than a state read, and it inherits gaps
a state read never has.** Three of those gaps are handled explicitly, each found by measurement:

- **~48% of v4 events are `amount: 0`** fee-collection no-ops. Counting them invents positions at
  real-looking tick ranges, so they are discarded.
- **Removals with no matching add** mean the position was transferred in — its adds happened under
  a different `origin`. Reported as `incompleteHistory[]` with the reason, size deliberately
  withheld. Neither dropped silently nor counted as liquidity.
- **Over 5000 events, we report nothing.** `openPositions: null` plus an explicit error. Found by
  running the reconstruction across five unrelated wallets: two hit the fetch cap and reported
  **1471 and 501 "open positions"** while every consistency check passed. A truncated sum is
  self-consistent and wrong — **consistency is not completeness.** The audit now checks both, and
  ships `audit.checks[]` + `audit.allPass` in every v4 response.

Lookups key on **`origin`** (the EOA), never `sender` — `sender` is the position manager contract
and matches nothing.

**Uniswap v2 is excluded on purpose.** v2 LP shares are fungible and always full-range, so "read
the range you actually set" has no meaning there. Adding it would dilute the claim, not extend it.

**Aerodrome is pool-level only.** Its subgraph exposes no per-owner Position entity, so
`/api/wallet?dex=aerodrome` returns an explicit error. Our own capability map claimed otherwise
until we tested it — the map was the thing that was wrong, not the endpoint.

**SushiSwap v3 is reported as unmeasurable, not as clean.** Its subgraph answers, but only 8 pools
clear the $250k TVL floor and none is a stable/stable pair — so the canary cannot prove the
instrument works there. All 30 windows are `trusted: false` and **no SushiSwap number is quoted**,
including the 12.5% sitting in the raw JSON. PancakeSwap v3 (BSC + Ethereum), QuickSwap v3 and
Camelot v3 return `bad indexers` / `subgraph not found`. Six venues probed, two answered, one
could be validated.

### The volatility check is a falsification test, not a finding

Impermanent loss is *mathematically* a function of price divergence, so the defect **must** get
worse in volatile months. That is a prediction our own theory makes — if the data did not show it,
our instrument would be broken. Across 110 windows, misleading% vs realized volatility:

| range | Pearson | Spearman |
|---|---|---|
| tight | 0.430 | 0.572 |
| moderate | 0.341 | 0.447 |
| wide | 0.303 | 0.384 |
| full | 0.235 | 0.285 |

Positive, and monotonically stronger as the range tightens — exactly what the math requires. We
ran it to try to break ourselves and failed to.

> **This is NOT evidence about macro, equities, or crypto beta.** We did not test those series and
> will not imply we did. With enough candidate predictors you can find a "relationship" to
> anything. A correlation predicted in advance from an identity is a self-check; a correlation
> found by fishing would be a story.

### Per-pool trust: which pools' advertised APR has historically been honest

Walk-forward: does advertised APR at day *T* predict realized return over *T..T+30*?

- **0% sign-flip rate** (advertised APR trustworthy): `USDT/USDf`, `AUSD/USDC`, `cbETH/WETH`,
  `WBTC/cbBTC`, `tBTC/WBTC`, `LINK/WETH`
- **60–71% sign-flip rate** (advertised APR routinely lied): `FET/WETH`, `DAI/WETH`,
  `QNT/WETH`, `PEPE/WETH`

The trustworthy set is entirely correlated pairs and the untrustworthy set is entirely
divergent ones — the instrument is sorting by the mechanism that actually causes the error,
which is evidence it measures something real rather than noise.

## Honesty box

Things that are true and inconvenient, kept here on purpose:

- **RETRACTED: `corr(advertised, realized) = 0.06` was this README's headline and it does not
  reproduce.** It existed in no committed code. Recomputed honestly (`lib/realized.js`
  `pearson`/`spearman`, run by `build-corpus.js`) it lands at **Pearson 0.08–0.16, Spearman
  0.30–0.33 raw; 0.33–0.38 trimmed** across three liveness gates. That is a real spread driven
  by outlier choice and rank-vs-linear, so quoting any single number as *the* correlation was
  the mistake. The correlation is reported as a **range with its estimator named**, and the
  headline is now the pool-count finding, which is measured directly rather than estimated.
  Found 2026-09-07 by grepping our own repo for the number and not finding it.
- **An earlier correlation of +0.42 was also wrong** (lookahead in the liveness gate, dead pools
  included). Two bad correlations in a row is why this metric no longer leads the README.
- **The v2 formula was being applied to a v3 venue.** Until 2026-09-07 every realized return
  here used constant-product IL, which is correct only for full-range positions. That silently
  reported the best case for every pool. Fixed in [`lib/concentrated.js`](lib/concentrated.js);
  the old number is kept as the `full` row above so the change is auditable rather than
  overwritten.
- **Our convergence canary failed us first, and it was right to.** The new v3 math was checked
  by asserting it converges to the v2 formula as range → ∞. Against a hand-picked epsilon it
  "failed" and nearly got correct code deleted. The error actually falls at the analytic rate —
  11.0x, 10.1x, 10.0x per 100x range — so the test now asserts **the rate, not a threshold**.
  A tolerance you tune until it passes is a parameter; a convergence rate is not.
- **"1 in 3 pools mislead you" was retracted as a headline** because it moved 41%→34% with the
  liveness cutoff. It appears above only as a full grid across ranges *and* gates, labeled as
  what it is.
- **"LPs lose to HODL" is not our discovery.** Topaze Blue / Bancor established that in 2021.
  Our contribution is not the loss — it is the *calibration of the advertised metric*.
- **DefiLlama already ships yield predictions** (11,489 pools carry `predictedClass` /
  `predictedProbability`). What nobody publishes is whether those predictions were *right* —
  **so we graded them**, twice, because the first grade was wrong in two different ways.
  Attempt 1: wrongly concluded no retrospective archive exists (it does — Wayback Machine,
  517 snapshots of `/pools` back to Oct 2022, full predictions payload intact). Attempt 2
  (n=69 pools, capped by rate-limiting): reported a clean **+3.2pp edge over baseline**.
  Attempt 3, same method with backoff and no fetch failures (n=459 pools, 8,092 graded
  instances): **the edge flips sign across bands** (strict 0%: −1.4pp: WORSE than guessing;
  mid 5%: +4.5pp; loose 10%: +1.5pp). Overall accuracy is not a finding — it moves with the
  band, and the small sample's clean number was a fluke of which pools survived rate-limiting.
  **What DID survive the 6x larger sample: their stated confidence is genuinely calibrated.**
  bin1 n=1987 edge −0.3pp, bin2 n=2639 edge +3.1pp, bin3 n=3466 edge **+8.3pp** — monotonic,
  wide spread, holds up. The model's raw accuracy is a mirage; its self-reported confidence is
  an honest, usable signal. See `data/llama-grade-backdated.json` and
  `scripts/grade-llama-backdated.py`. Either way: the target variable (fee-only apy) was
  already shown near-orthogonal to actual LP outcome (ceiling test above, corr=−0.008).
- **The liveness gate is imperfect.** Activity/volume/TVL alone let dead tokens through;
  `priceCollapsed()` closes most of that, with the threshold set from *observed* depeg data
  (real depegs bottomed at 2–4% of peak, so a <1% cutoff would have caught none of them).

## Canaries

Every number here is gated on instruments proving they can find a known-present signal first:

- Stable/stable pairs **must** show ~0 impermanent loss, or the whole run is marked untrusted
  and `build-corpus.js` **refuses to write output** (exit 1). Live: worst |IL| = 0.0007%.
- IL math is checked against closed-form constant-product values (r=2 → −5.72%, r=4 → −20%).
- "Unmeasurable" stays distinguishable from "zero" — a missing price returns
  `measurable: false`, never a fabricated 0.
- Every headline is reported at **three** liveness cutoffs. If a finding flips across them,
  it is labeled a parameter, not a finding.
- **The correlation estimator has its own canary.** `corr(advertised APR, fee return)` must come
  back clearly positive — both are fee-derived, so a weak value means the estimator is broken,
  not that the market is strange. Live: **0.726**. `build-corpus.js` exits non-zero and refuses
  to write if it drops below 0.3.
- **Concentrated IL is checked against the v2 closed form at four range widths**, asserting the
  convergence *rate* rather than a tuned tolerance.
- **Every historical window runs its own canary.** A window that cannot prove its instrument works
  is emitted as `trusted: false`, never silently dropped — "we could not measure this month" and
  "this month was fine" must not look the same in the output.
- **Survivorship bias is disclosed and points against us.** Pools are ranked by *current* volume,
  so pools that died are absent from historical windows. That makes the past look *better* than it
  was, weakening our thesis rather than inflating it. The subgraph exposes no point-in-time
  ranking, so we state the bias instead of pretending to correct it.
- **Base first returned 0 trusted windows out of 30, and that was the canary working.** The top 80
  Base pools by volume contained no stable/stable pair, so the instrument could not prove it
  measures IL correctly and refused to certify. The fix was to *fetch the canary its reference
  pools* — never to weaken the canary. Those pools are validation-only and excluded from every
  headline. An instrument that confidently reports a number it cannot validate is the exact
  failure this repo exists to prevent.

## Run it

**One command, the whole pitch, live data, no setup beyond a free API key:**

```bash
npm install
GRAPH_API_KEY=your-key node demo.js
```

Get a free key at [thegraph.com/studio](https://thegraph.com/studio) (Subgraph Studio -> create
API key). `demo.js` fetches a live pool sample from The Graph right now, proves its own canary
passes before printing anything, shows one concrete pool's advertised-vs-realized gap across all
four concentration ranges, and reports the misleading-pool rate on that sample. No pre-built
corpus, no server process — everything above is a live number, fetched during that one command.

For the deeper evidence (110 independent monthly windows, 4 chains, cross-DEX, the DefiLlama
grading) or to run the full corpus/MCP server yourself:

```bash
node test/canary.test.js                  # offline math + negative control
GRAPH_API_KEY=... node test/canary.test.js --live
GRAPH_API_KEY=... node scripts/build-corpus.js   # single-window corpus
GRAPH_API_KEY=... node scripts/walk-forward.js   # 13 overlapping windows, mainnet
GRAPH_API_KEY=... node scripts/history-run.js    # 110 independent months, 4 chains
GRAPH_API_KEY=... node scripts/cross-dex.js      # Aerodrome + SushiSwap, same instrument
node scripts/build-report.js                     # render report.html from the JSON
```

The `realized_return` tool takes an optional **`rangeWidthX`** — your actual concentrated
position (1.25 = a tight ±25% band, 2 = typical, 4 = wide, omit for full-range). It answers the
question no yield dashboard answers: *given the range I was actually in, what did I actually
make?* — including whether price left your band, in which case the loss is realized, not
impermanent.

Live example (USDC/WETH, 30d, price ratio 1.3091):

```
full-range realized:  -0.58%
  tight  ±1.25x       -7.95%   OUT OF RANGE
  moderate ±2x        -2.75%
  wide   ±4x          -1.48%
```

MCP client config:

```json
{ "mcpServers": { "realized": {
    "command": "node",
    "args": ["bin/mcp-server.js"],
    "env": { "GRAPH_API_KEY": "your-subgraph-studio-key" } } } }
```

## License

MIT
