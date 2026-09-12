# COMPOSABILITY.md — one query pattern, six venue/chain pairs

**Track:** The Graph — *Best Use of Composable or Standardized Graph Products*
**Project:** [REALIZED](https://realized.drainfun.xyz) · [jiggy-cadence/realized](https://github.com/jiggy-cadence/realized)

> The track asks for *"one query pattern spanning many protocols, or one pipeline reused across
> chains."* This file is the evidence for that claim, measured rather than asserted.

---

## The claim, in one table

| | count | what |
|---|---|---|
| Protocol codebases | **3** | Uniswap v3, Uniswap v4, Aerodrome (a Velodrome/Solidly fork) |
| Chains | **4** | mainnet, Arbitrum, Polygon, Base |
| Venue/chain pairs | **6** | live from [`/api/venues`](https://realized.drainfun.xyz/api/venues) |
| Pools in the corpus | **256** | aerodrome/base 77 · uniswap-v3/mainnet 65 · uniswap-v3/base 59 · uniswap-v3/arbitrum 38 · uniswap-v3/polygon 17 |
| **Venue-specific branches in the math** | **0** | `scorePool` contains no `if (dex === ...)` |
| Pool-analytics query shapes | **1** | one `FIELDS` string, every venue |

Verify the last two yourself:

```bash
# One query shape for every venue -- scripts/build-pools.js:34-35
grep -n "FIELDS" scripts/build-pools.js

# Zero venue branching in the scoring math
grep -n "dex ===\|venue ===\|aerodrome" packages/core/src/realized.js   # returns nothing
```

---

## Why this is composability and not just "we queried four subgraphs"

The track explicitly warns that *simply querying one Subgraph with no composition or
standardization does not qualify.* The leverage here is that **a shared schema shape let one
implementation of a non-trivial financial calculation span three different protocol codebases.**

The pipeline is a single path, reused:

```
VENUES map (6 pairs)                 packages/core/src/venues.js:9-26
   -> one gateway query fn           packages/core/src/realized.js:48   query()
   -> one FIELDS shape               scripts/build-pools.js:34-35
   -> one scoring/IL implementation  packages/core/src/realized.js:335  scorePool()
   -> one canary gate per venue      scripts/build-pools.js:52-58
   -> one corpus                     api/pools.json (256 pools)
```

Adding a venue is **a map entry, not a code path**. `VENUES` is the only place a subgraph ID
lives ([`venues.js:9-26`](packages/core/src/venues.js#L9-L26)), and the build loop iterates it
generically ([`build-pools.js:41-42`](scripts/build-pools.js#L41-L42)):

```js
for (const [dex, chains] of Object.entries(VENUES)) {
  for (const [chain, id] of Object.entries(chains)) {
```

**What became easier because of the shared shape:** Aerodrome is a different protocol by a
different team, and it dropped into the corpus as four lines of config. It now contributes 77 of
our 256 pools — the largest single venue — and it reaches the same verdict as Uniswap v3 through
the same code. That cross-protocol agreement is what upgrades our central finding from "a Uniswap
quirk" to "a property of concentrated-liquidity AMMs." A per-venue implementation would have made
that comparison unfalsifiable, because any difference could have been blamed on our own code.

---

## The standardization has a limit, and we mapped it

Composability claims are only credible if you say where they stop. Ours stops at the
**position** layer, and the break is visible in the capability map
([`venues.js:38-74`](packages/core/src/venues.js#L38-L74)):

| venue | source | pool analytics | wallet lookup | realized return | exit sim |
|---|---|---|---|---|---|
| Uniswap v3 | position-state | yes | yes | **yes** | **yes** |
| Uniswap v4 | event-reconstruction | yes | yes | **no** | **no** |
| Aerodrome | pool-only | yes | **no** | no | no |

- **Pool-level analytics standardize cleanly.** `poolDayData` has the same shape everywhere, so
  one pipeline serves all six pairs.
- **Position-level data does not.** v3 stores the tick range as state on the NFT; v4's `Position`
  entity has no range at all, so it must be reconstructed from `ModifyLiquidity` events
  ([`v4.js:101-194`](packages/core/src/v4.js#L101-L194)); Aerodrome exposes no per-owner
  `Position` entity at all.

So we ship the capability map as a **queryable endpoint** rather than a README footnote — an
agent calls `/api/venues` and learns what each venue can answer *before* asking. That is the
honest version of composability: standardize what genuinely standardizes, and publish a
machine-readable boundary where it doesn't.

**We found that boundary by getting it wrong.** Our capability map previously claimed Aerodrome
supported `realizedReturn` and `exitSimulation` while the endpoint refused those calls — the map
and the code contradicted each other, and the map was the one lying. Caught by calling
`?dex=aerodrome` for two addresses and reading the errors. Corrected 2026-09-11.

---

## Composed with a second, independent source

Beyond The Graph, prices are cross-checked against **1inch Spot Price**
([`packages/core/src/oneinch.js`](packages/core/src/oneinch.js)) — an aggregator independent of
any single pool. Result across 255 pools: **99.2% agreement, median divergence 0.078%.**

This is composition doing real work rather than logo-collecting: if the subgraph's `token0Price`
had drifted from aggregate market price, every downstream IL number would be wrong in a way that
is invisible from inside the subgraph. Live gas for exit simulation comes from the same source
(1inch gas-price v1.5), and degrades to `unavailable` with a reason rather than guessing.

---

## Reproduce the whole pipeline

```bash
# Rebuild the entire 6-pair, 256-pool corpus from live Graph data
GRAPH_API_KEY=<subgraph-studio-key> node scripts/build-pools.js

# Inspect the standardized output
curl "https://realized.drainfun.xyz/api/venues"
curl "https://realized.drainfun.xyz/api/pools" | head -c 600
```

Each venue must independently clear a **stable-pair canary** before its rows are published: a
USDC/USDT-style pair must show ~0 impermanent loss, or that venue is excluded and marked
untrusted rather than shipped ([`build-pools.js:52-58`](scripts/build-pools.js#L52-L58)). One
pipeline, one gate, applied identically to every protocol — including the ones that fail it.
