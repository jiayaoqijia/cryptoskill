---
name: aero-vote-radar
description: Decide where to allocate sAERO on Aero (formerly Aerodrome) across its 7 networks, and check a wallet's stakes and 47 h timers. Use when someone asks which Aero pool pays best for their sAERO, how to split a stake, when they can move their allocation again, or what their current allocation earns. Read-only; never touches keys.
---

# aero-vote-radar

On Aero, sAERO holders allocate their stake to pools and earn those pools'
fees and incentives, split by how much sAERO each pool holds. So the question
is never "which pool has the highest APR". It is "which pool pays best **for my
amount, after my own stake dilutes it**". This tool answers that from the
hourly scan of Aero's contracts behind aero.deftools.xyz.

## Start here

If the person has a wallet address, **run `my-stakes` first.** It shows what
they already hold, where it is allocated and when each network lets them move
it, so the advice starts from their real position.

```bash
npx aero-vote-radar my-stakes 0x...                 # stakes, allocations, 47 h timers
npx aero-vote-radar recommend --address 0x...       # split for their stake vs their current split
npx aero-vote-radar recommend --amount 25000        # split for an amount
npx aero-vote-radar pools --amount 25000            # full ranking
npx aero-vote-radar pools --steady                  # pools that kept paying hour after hour
```

`--chain base|ethereum|optimism|arbitrum|ink|robinhood|arc` limits to one
network. Add `--json` for machine-readable output.

## As an MCP server

```bash
npx aero-vote-radar-mcp
```

Tools: `list_pools`, `recommend_allocation`, `get_my_stakes`.

## Things to get right

**The person allocates, not you.** Nothing here signs or sends. They enter the
split on app.aero.xyz/markets/allocate and press Save allocation. Aero has no
link that pre-fills it. Never describe an allocation as done.

**The 47 h timer is per network.** A stake can move on a network only 47 hours
after it last allocated there. A timer of 0 means it has never allocated
there and can do so now. Say when the next move is possible.

**Size changes the answer.** Dilution means a large stake can't use the thin
pools a small one can. Never carry a split from one amount to another; rerun it.

**Rates move hour to hour.** Fees arrive in lumps and incentive programs start
and end. A pool on top this hour may not be next hour. For someone who won't
check often, prefer `pools --steady`: pools where at least 75% of 24+ hourly
samples paid half their own average or more.

**Check the scan's age.** Every answer carries `checkedAt`. The scan runs
hourly; if it is more than 3 hours old, say the figures may be stale.

**A network can fail to answer.** Wallet reads list it under `notRead`. Its
timers and allocations are missing, not zero. Say so.

**No predictions about price.** This tool measures what pools pay per day. It
says nothing about whether AERO goes up.

## Web page

**[aero.deftools.xyz](https://aero.deftools.xyz)**: the same figures, nothing to install.

## Source

[github.com/araxis33/aero-vote-radar](https://github.com/araxis33/aero-vote-radar) (MIT).
