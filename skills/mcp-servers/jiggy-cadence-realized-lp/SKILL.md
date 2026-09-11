---
name: realized-lp
description: Check what liquidity providers ACTUALLY earned in a Uniswap v3 or Aerodrome pool — fee income minus impermanent loss — against the fees-only APR that DEX UIs advertise. Use when asked whether an LP position, pool, or yield number is actually profitable, whether an advertised APR is trustworthy, or to audit many pools at once for misleading yield. Backed by live Graph subgraph data.
---

# Realized LP

Advertised LP APR is fee income, annualized. **It has no price term, so it cannot go negative.**
A pool cannot advertise a loss no matter what happened to the people in it. This skill computes
the number that can: `realized = fees + impermanent loss`.

## When to use this

- "Is this pool actually profitable?" / "Is this APR real?"
- "I'm LPing WETH/USDC, am I making money?"
- "Find me pools where the advertised yield is lying"
- Any yield-farming or LP decision where the advertised number is the only evidence on offer

## Quick start (no install, no API key)

```bash
curl -s https://realized.drainfun.xyz/api/pools
```

202 live pools across 4 validated venues. The response embeds its own `schema` and the exact
impermanent-loss formula in `howToComputeRealizedReturn`, so you can compute any range yourself
with no further docs. Fields per pool:

| field | meaning |
|---|---|
| `pair` | token0/token1 symbols |
| `dex` / `chain` | `uniswap-v3` \| `aerodrome` / `mainnet` \| `arbitrum` \| `polygon` \| `base` |
| `r` | price ratio over the window (exit ÷ entry) |
| `fees` | fee income over window, % of entry TVL |
| `adv` | **advertised** APR % — what the DEX UI shows |
| `days` | window length |

### Compute realized return for any range

```js
function il(r, w) {                      // w = range half-width: 1.25 tight, 2 typical, 1e8 full
  const sa = Math.sqrt(1 / w), sb = Math.sqrt(w);
  let pos;
  if (r <= 1 / w) pos = (1 / sa - 1 / sb) * r;
  else if (r >= w) pos = sb - sa;
  else pos = 2 * Math.sqrt(r) - sa - r / sb;
  return ((pos / ((1 - sa) + (1 - 1 / sb) * r)) - 1) * 100;
}
const realizedPct = pool.fees + il(pool.r, 2);
const realizedApr = (realizedPct / pool.days) * 365;
const misleading  = pool.adv > 0 && realizedApr < 0;   // advertised a profit you didn't get
```

**`r <= 1/w` or `r >= w` means price left the band** — the LP is fully converted into the losing
asset and the loss is realized, not impermanent. Always say so; it changes the advice.

## Live queries (MCP server)

For pools not in the cached set, or a custom window, run the MCP server. Needs a free
[Subgraph Studio](https://thegraph.com/studio/) API key.

```bash
git clone https://github.com/jiggy-cadence/realized && cd realized && npm install
```

Paste into Claude Desktop (`claude_desktop_config.json`), Cursor (`.cursor/mcp.json`), or any
MCP client, then restart it:

```json
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

**No key? Skip the MCP server entirely.** Every tool is also a plain HTTP GET against our
server, which proxies its own Graph key — no auth, CORS open:

```bash
curl "https://realized.drainfun.xyz/api/find?q=WETH/USDC"
```

| tool | use |
|---|---|
| `find_pool(query)` | **start here** — resolve `"WETH/USDC"` or `"PEPE"` to ranked poolIds. You never need to know an address. |
| `realized_return(poolId, days?, rangeWidthX?)` | fees vs IL vs advertised for one pool over a recent window |
| `position_realized(poolId, entryDate, rangeWidthX?)` | **what YOU actually made** on a position entered on a *specific date*, however long ago — not "the last 30 days," but "since I actually put money in." See below. |
| `explain_gap(poolId)` | plain-language verdict + the evidence chain that produced it |
| `audit_pools(limit?)` | corpus-wide sweep: how many pools advertise a profit LPs didn't get |

### Stop assuming the range — read the real one

Every number above needs a range width, and `±2×` is a guess. `/api/wallet/{address}` reads what
the LP actually set:

```bash
curl -s "https://realized.drainfun.xyz/api/wallet/0xYourAddress"
```

Read-only. No signing, no wallet connection, no permissions — it is a subgraph lookup on a public
address, nothing more. Returns each open position with its real `tickLower`/`tickUpper`, the
derived `range.widthX`, and a plain-language `range.label`. **Feed `range.widthX` into
`position_realized` (or `/api/position/{poolId}?range=`) to get realized return at the LP's actual
band instead of an assumed one.** That is the whole point of the endpoint.

**It is position discovery, not per-position P&L — deliberately.** Two fields look like they'd
give you fees and entry value. Both lie:

- `collectedFees*` is a **withdrawal** record, not an earnings record — it only populates when the
  LP calls `collect()`. Measured live: of 150 positions with `collectedFeesToken0 == 0`, **71 had
  non-zero `feeGrowthInside0LastX128`** — they earned fees and never collected. So uncollected fees
  return `measurable: false` with a reason, **never `$0`**. Reporting zero there would reproduce the
  exact defect this project exists to expose, pointed at the user's own money.
- `deposited*`/`withdrawn*` are **lifetime cumulative**, not entry state (75% of live positions read
  as one-sided because of it). They are namespaced under `cumulative` and must not be read as
  position value.

Every response carries a `limits` block stating both, and token `decimals` ship beside every raw
amount so you never guess the divisor. Never render a position's fees as a number unless
`fees.measurable` is `true`.

### `position_realized` — the one question every real LP actually has

`realized_return` answers "what does the average LP get in this pool right now."
`position_realized` answers "I put money into this exact pool on this exact date at this exact
range — what have I actually made since." Anchors to a real calendar date, not a fixed lookback:

```json
{ "poolId": "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640", "entryDate": "2026-07-28", "rangeWidthX": 2 }
```

Returns fees earned, impermanent loss, realized return, whether price ever left your band (if
so the loss is **locked in**, not impermanent), and a day-by-day series so you can see exactly
when the position turned. Refuses to answer (`measurable: false`) rather than guess if fewer
than 2 days have passed since entry — there is nothing to measure yet, and 0% is not the honest
answer to "not enough data."

Same math as everywhere else in this project (`lib/concentrated.js`'s own IL formula, not a
separate implementation) — hand-verified in `test/canary.test.js` against an independent,
from-scratch calculation, plus a live check against a real 45-day-old position.

Also available over plain HTTP (no MCP client, no API key — we proxy our own Graph key):

```bash
curl -s "https://realized.drainfun.xyz/api/position/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640?entry=2026-07-01&range=2"
```

`entry` accepts an ISO date or a unix timestamp; `range` is the band width (omit for ±2×, use a
huge value for full range). Errors are explicit and never fabricated: a future `entry`, an
unparseable date, an unknown pool, and a window too short to measure each return a stated reason
rather than a number. The same call backs the date picker on the web UI — one implementation of
the math, three transports (MCP, HTTP, browser).

### `simulate_exit` — decision support for closing a position TODAY

Not a new claim: calls the identical `position_realized` math and reframes it around the
question a holder actually has at the moment of deciding — dollars on a stated stake, not just
percent since entry.

```bash
curl -s "https://realized.drainfun.xyz/api/simulate-exit/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640?entry=2026-07-28&range=2&stake=25000"
```

**Gas is real.** Live gas price from 1inch × estimated gas units for `decreaseLiquidity` +
`collect` (~270k), priced in the chain's native token. The *price* is measured; the *units* are
an estimate, so the response carries `isEstimate: true` and you should report the dollar figure
as approximate. It degrades to `{ available: false, reason }` rather than guessing.

**Slippage is zero for a plain close, and that zero is measured, not missing.** Closing a v3
position is not a swap — `decreaseLiquidity` + `collect` returns *both* tokens at the current
tick, so there is no price impact. Slippage only exists if the holder then chooses to swap one
side into the other:

```bash
curl -s "https://realized.drainfun.xyz/api/simulate-exit/0x88e6...5640?entry=2026-07-28&stake=25000&consolidate=true"
```

With `consolidate=true` the estimate is an explicit **lower bound**: impact is modelled against
total pool TVL, but a concentrated pool's depth at the active tick is thinner than its TVL, so
real impact is likely higher. Say "at least," never "exactly."

`netAfterCostsUsd` is populated **only** when both gas and slippage are known, and is `null`
otherwise — a partial subtraction presented as a complete figure is the same defect this project
exists to expose. If `outOfRange` is true, say plainly that the loss is locked in regardless of
timing — waiting does not un-realize it.

## Reporting rules (these matter more than the numbers)

1. **Always state the range.** The same pool can be honest full-range and misleading at ±1.25×.
   Full-range is the *most generous possible case for the pool* — never quote it alone.
2. **`measurable: false` is not zero.** It means the window couldn't be priced. Say "couldn't
   measure," never "no loss."
3. **Check the canary before quoting an aggregate.** `audit_pools` returns
   `canary.passed` — stable/stable pairs must show ~0 IL. If it's false the instrument is
   unproven and every number in that response is untrusted.
4. **Fees are held constant across ranges**, which is unfair to *this tool*: concentrating earns
   more fees too, so some IL is earned back. The **direction** is reliable; treat magnitudes as
   bounded by that caveat.
5. **This is backward-looking measurement, not a forecast.** It says what happened over the
   window, not what will happen.

## What holds this up

110 independent (non-overlapping) 30-day windows across 4 chains, plus the same instrument run
unchanged on Aerodrome Slipstream — different team, codebase, incentive model — showing the same
defect with the same shape. Venues whose stable pairs can't prove ~0 IL are **excluded, not
reported as clean**. Full tables: <https://realized.drainfun.xyz/report.html>

Data: The Graph. Per-day `feesUSD` are indexer-derived aggregates. **Not** unreachable by RPC —
`feeGrowthGlobal0X128` is public pool state readable at any historical block, verified live
2026-09-11 — but reconstructing per-day USD from it needs an archive node, a block lookup per
day boundary, and a historical price for both tokens at each one, repeated per pool. The Graph
publishes that join already computed across 256 pools and 5 chains. The claim is practicality,
not impossibility.

## Machine-readable API spec

Full OpenAPI 3.1 description of every endpoint, parameter, response shape and error:
<https://realized.drainfun.xyz/openapi.json> — so an agent never has to guess a request shape.
