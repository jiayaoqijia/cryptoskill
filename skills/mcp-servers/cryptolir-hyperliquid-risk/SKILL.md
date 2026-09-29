---
name: hyperliquid-risk
description: "How to size Hyperliquid trades and set leverage so an agent stays inside its owner's caps by design rather than by bouncing off them: what the per-order and daily notional limits actually count, why every order sent costs its full size for the day whether or not it trades, why closing a position also consumes the budget, when to set leverage, and how to read liquidation distance. Use alongside hyperliquid-trading before deciding a size or a leverage. NOT a substitute for the caps themselves, which are enforced server-side."
homepage: https://hyperliquid.gitbook.io/hyperliquid-docs
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "requires":
          { "env": ["AGENTGLOB_RUNTIME_URL", "AGENTGLOB_RUNTIME_TOKEN"] },
      },
  }
---

# Hyperliquid — sizing, leverage and staying inside the limits

Your owner sets limits on what you may trade. They are enforced on the server
and you cannot change them. This skill is about **not needing them** — trading
in a way that stays comfortably inside, instead of discovering each edge by
being refused.

A refusal is not a free retry. It burns a rate limit shared with every other
agent, and an agent that repeatedly probes its own ceiling looks exactly like
one trying to get around it.

## You cannot see your own limits

There is no way to ask what your caps are or how much of today's budget you have
already used. You learn a limit exists only when an order is refused for
crossing it.

So:

- **Keep your own running tally.** A successful order response carries a
  `notionalUsd` field — **that** is the number charged against you, not your own
  `price × size`. The server rounds price to 5 significant figures and size to
  the asset's precision before charging, so your arithmetic will drift. Add up
  the returned figures.
- **If you need to know a limit, ask your owner.** Do not probe for it by
  sending progressively larger orders.
- **When you are refused, the message names the number.** `order_cap_exceeded`
  and `daily_cap_exceeded` both say what the cap was. Remember it for the rest of
  the session and report it to the person.

## What actually counts against you

There are four limits: a **per-order** notional cap, a **daily** notional cap, a
**maximum leverage**, and an **allowlist** of assets.

Notional means **price × size in dollars** — the full face value of the trade,
not the margin it ties up. A $2,000 position at 10× leverage uses $200 of your
money but counts as **$2,000** of notional. At high leverage the daily cap binds
far sooner than the account balance does.

### Every order you send costs its full size for the day

This is the rule that matters most, and it is not the intuitive one.

The daily counter is charged **when the order is sent**, at the full size you
asked for. It is refunded **only** when the request fails outright — a cap
refusal, a rejected signature, an unreachable exchange. It is **not** refunded
when:

- **The order rests and you cancel it.** A `Gtc` order that never trades still
  costs its whole notional for the day.
- **The order partly fills.** An `Ioc` that fills a tenth and cancels the rest is
  charged for **all** of it. The counter is never reconciled against what
  actually executed.
- **The exchange rejects that individual order.** Those come back inside an
  otherwise-successful response (see `hyperliquid-trading`), so nothing failed
  from the server's point of view — and the budget stays spent.

The practical consequences:

- **Placing and cancelling is not free.** Repricing a resting order five times
  costs five times the notional against your day, even though only one order
  could ever have filled. Decide the price once.
- **Get the order right the first time.** Read the book before you send, not
  after you are refused.
- **A stablecoin swap counts too.** `hl_swap` draws from the same daily total
  as your orders. Unlike an order, only the part that actually sold is
  charged, and a swap that sells nothing costs nothing. Convert before you
  trade, not after you have spent the day on orders.
- **Leave room to close.** A reduce-only order is still an order and still
  costs. An agent that spends its whole allowance opening positions **cannot
  close them**, and is stuck holding risk until the counter resets.
- **The day is a UTC day.** It resets at midnight UTC, which is the middle of
  the afternoon or the middle of the night depending on where the person is.
  Never say "it resets at midnight" without saying UTC.

Cancelling itself adds nothing — the cost was already taken when the order went
out. So cancel a stale order rather than leaving it resting; just do not treat
place-and-cancel as a free way to probe the market.

## Sizing

- **Work out the notional first, in dollars**, then convert to asset units.
  Someone asking for "$500 of ETH" at $3,000 means `sz: 0.1667`, not `sz: 500`.
- **Stay well under the per-order cap** — aim for a fraction of it, not the last
  dollar. A cap you land exactly on leaves nothing for the next trade and no room
  for a price that moved between reading and sending.
- **Do not slice an order to get past a cap.** Splitting a refused $1,000 order
  into five $200 orders defeats the limit your owner set. If a trade does not fit,
  it does not fit — say so and stop.
- **Do not average down.** Adding to a losing position because the price fell is
  the fastest way through a daily cap and into a liquidation. If you were wrong,
  being wrong at twice the size does not fix it.
- **Small accounts have minimums.** Hyperliquid rejects orders below its minimum
  value. That is a real floor, not a glitch — and per the rule above, a rejected
  order has still spent its budget, so check the size before sending rather than
  finding the floor by trial.

## Leverage

`hl_set_leverage` takes a `coin`, a `leverage` and `isCross`.

**Set leverage before you open the position.** Changing it while a position is
open moves the liquidation price on money already at risk — an increase can put
a position that was comfortable within reach of being closed out.

- **Higher leverage does not increase profit, it decreases the distance to
  liquidation.** At 20× a 5% move against you wipes out the margin. At 2× the
  same move is a bad day.
- Requests over your owner's maximum are refused with `leverage_exceeded`. Use a
  lower number; do not ask repeatedly.
- **Cross** margin (`isCross: true`, the default) shares the whole account
  balance as collateral — one bad position can pull the others down with it.
  **Isolated** confines the damage to that position's own margin. Prefer isolated
  when you are opening something speculative alongside existing positions.

## Liquidation is the real risk

If the price reaches your `liquidationPx`, the exchange closes the position for
you and the margin is gone. This is not a possibility to mention once — it is the
number to watch.

From `hl_account` → `clearinghouseState`, each position carries `liquidationPx`.
Compare it to the current price and express the gap as a percentage. **"BTC would
have to fall 8% to liquidate this"** is useful; "the position is open" is not.

Report it unprompted when the gap is small. Nobody is watching the screen for you.

## There is no automatic stop-loss

You cannot leave a protective order resting. Nothing closes a losing position
while you are not looking. This is the single most important thing to be honest
about:

- **Never imply a position is protected.** If someone asks you to "set a stop at
  $90,000", the truthful answer is that you cannot, and that the only way to
  close it is for you to be running and to place the order yourself.
- If you are asked to watch a position, watching means **checking on a sensible
  interval, not polling in a loop** — the rate limit is shared with the whole
  fleet. Minutes, not seconds.
- Between your checks, the position is unprotected. Say so, so the person can
  decide whether that is good enough.
- **Your ability to close can be taken away.** Cancelling and closing both go
  through the same policy check as opening. If your owner disables Hyperliquid,
  empties the allowlist, or removes a coin while you hold a position in it, you
  can no longer cancel or reduce it. If that happens, say so immediately and
  plainly — a human has to act.

## Rules

- **The caps are your owner's decision, not a target to spend.** Finishing the
  day well inside them is a good outcome, not an underperformance.
- **Stop after an unexpected loss and report it.** Do not trade your way back.
- **When a refusal, a failure and an unclear response leave you unsure what
  position you hold, stop trading and read the account.** Acting on a guess about
  your own position is worse than doing nothing.
- **You are not a financial adviser.** You can size a trade someone asked for and
  explain what the numbers mean. Deciding whether to take the risk is theirs, and
  if they ask you what they should do, say that plainly.
