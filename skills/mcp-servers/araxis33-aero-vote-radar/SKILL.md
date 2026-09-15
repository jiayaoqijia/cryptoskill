---
name: aero-vote-radar
description: Decide where to point veAERO in Aerodrome's weekly vote on Base, and check what a vote already cast actually paid. Use when someone asks where to vote, which Aerodrome pool pays best per veAERO, what their veAERO is worth, what last week's vote earned, or wants a vote they can paste into Aerodrome's UI or sign themselves. Reads live Base mainnet data; never touches keys.
---

# aero-vote-radar

Aerodrome pays each week's bribes and trading fees to whoever voted for that
pool, split by weight. So the question is never "which pool has the highest
APR" — it is "which pool pays best **per veAERO, after my own vote dilutes
it**". This tool answers that from live on-chain data and hands back whole
percentages that Aerodrome's voting UI accepts.

Every number comes from Aerodrome's own Sugar and Voter contracts plus
DefiLlama prices. No API keys, no backend, no database, no wallet connection.

## Start here

If the person has an address, **run `review` first.** It scores the vote they
already cast against the epoch that has closed, so every figure can be checked
against their own wallet. Nothing is predicted, so nothing has to be believed —
and it is the fastest way to find out whether they vote at all.

```bash
npx aero-vote-radar review --address 0x...        # what last Thursday actually paid
npx aero-vote-radar my-veaero 0x...               # their locks and voting power
```

Then the recommendation:

```bash
npx aero-vote-radar recommend --address 0x... --vote-ready
npx aero-vote-radar recommend --veaero 25000 --vote-ready --min-consistency 0.5
npx aero-vote-radar backtest --veaero 25000 --epochs 5
```

`--vote-ready` prints whole percentages summing to exactly 100. Rounding each
weight independently tends to total 101% or 102% and leaves the person fudging
the last row by hand.

Add `--json` to any command for machine-readable output.

## As an MCP server

```bash
npx aero-vote-radar-mcp
```

Tools: `list_pool_efficiency`, `recommend_allocation`, `backtest_strategy`,
`get_my_veaero`, `prepare_vote_calldata`.

`prepare_vote_calldata` returns an **unsigned** `Voter.vote` transaction. It
never asks for a key and cannot send anything.

## Things to get right

**A vote expires.** It only counts toward the epoch it is cast in, and epochs
flip Thursday 00:00 UTC. Always say how long is left — `recommend` prints it.

**Don't chase the top row.** A pool showing a four-figure "edge" on low
consistency is one large one-off bribe, not a repeatable weekly opportunity.
`--min-consistency 0.5` filters that class out; pass the same value to
`backtest` so the backtest tests the strategy actually being run.

**Size changes the answer.** Self-dilution means a large budget cannot use the
thin pools a small one can. Never carry a recommendation from one amount to
another — rerun it.

**Say how much to believe it.** Of the ten pools this ranking puts on top,
about six are still on top when the epoch closes (pools paying $1,000+ an
epoch; fewer once near-empty gauges are counted). The weight every per-vote
figure divides by is typically ~20% out. Both figures are measured from the
repo's own scan history and published in `docs/data/timing.json`.

**Within a week there is nothing to chase.** Measured over 69 committed scans,
only about 4% of pool-windows show any change in the underlying reward amounts
at all — an epoch's incentives are essentially fixed by the time a scan sees
them, and the dollar figure moving hour to hour is the reward tokens repricing.
`npm run accrual` is the measurement. Don't tell anyone to watch a pool
mid-week for "money flowing in".

**No predictions about price.** This tool measures incentives per vote. It says
nothing about whether AERO goes up.

## Hosted page

**[aero.deftools.xyz](https://aero.deftools.xyz)** — nothing to install, rescanned
every 6 hours, allocation runs in the visitor's browser.

## Source

[github.com/araxis33/aero-vote-radar](https://github.com/araxis33/aero-vote-radar) — MIT.
