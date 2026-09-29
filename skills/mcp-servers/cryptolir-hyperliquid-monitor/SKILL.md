---
name: hyperliquid-monitor
description: "Read Hyperliquid market data and this agent's own trading account: mid prices, order book, candles, funding rates, perp metadata, open positions, margin, spot balances, resting orders, recent fills and fee tier. Read-only — it places no orders, changes nothing and moves no funds. Use when asked what a market is doing, what this agent holds, how a position is performing, or whether an order filled. NOT for placing, changing or cancelling orders."
homepage: https://hyperliquid.gitbook.io/hyperliquid-docs
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires":
          { "env": ["AGENTGLOB_RUNTIME_URL", "AGENTGLOB_RUNTIME_TOKEN"] },
      },
  }
---

# Hyperliquid — reading the market and your account

Hyperliquid is a perpetual-futures exchange. This skill covers **reading only**.
Nothing here signs anything, spends anything or changes anything.

You need the **Hyperliquid MCP** for these reads. If you have no `hl_market_data`
or `hl_account` tool, it is not installed on you — say so plainly and tell your
owner to add it from **dashboard → the agent → Tools → Add MCP → Hyperliquid**.
Do not try to reach the exchange another way.

Reading works even when trading is switched off for you. The two are separate:
an agent that is refused every order can still read everything below.

## Two kinds of read, and the difference matters

**Market data** (`hl_market_data`) is public information about the exchange —
prices, the book, candles. It is the same for everyone and involves no account.

**Account data** (`hl_account`) is *your own* trading account, and only ever
that. The address is filled in by the server from the wallet bound to you. There
is no parameter for someone else's address and asking for one is refused. If a
person asks you to look up another trader's positions, you cannot — say so
rather than reaching for a workaround.

## Market data

`hl_market_data` takes a `kind`:

| `kind` | What you get | Also needs |
|---|---|---|
| `allMids` | Current mid price for every perp. The cheapest way to answer "what is X trading at". | — |
| `l2Book` | Order book depth for one asset — bids and asks with sizes. | `coin` |
| `candleSnapshot` | OHLCV candles for a period. | `coin`, `interval`, `startTime` |
| `meta` | Every perp: name, `szDecimals` (size precision) and `maxLeverage`. | — |
| `metaAndAssetCtxs` | `meta` plus live context per asset: mark price, open interest, funding. | — |
| `fundingHistory` | Historical funding rates for one asset. | `coin`, `startTime` |
| `predictedFundings` | Upcoming funding across venues. | — |

`interval` is a string like `1m`, `15m`, `1h`, `1d`. `startTime` and the optional
`endTime` are epoch milliseconds — pass `endTime` to bound a candle or funding
range instead of pulling everything up to now.

**`meta` is the source of truth for what exists.** If an asset is not in
`meta.universe`, it is not tradeable here — do not guess at ticker spellings.
Symbols are bare, like `BTC` and `ETH`, not `BTC-USD` or `BTCUSDT`.

## Your account

`hl_account` takes a `kind` and nothing else:

| `kind` | What you get |
|---|---|
| `clearinghouseState` | Perp account: account value, margin used, and every open position. |
| `spotClearinghouseState` | Spot token balances. |
| `openOrders` | Resting orders that have not filled. Each carries an `oid`. |
| `frontendOpenOrders` | The same, with extra display detail. |
| `userFills` | Recent fills — what actually executed, at what price. |
| `portfolio` | Account value over time. |
| `userFees` | Your fee tier. |

You can **read** spot balances but you cannot trade spot — orders are perps only.
The one exception: if spot holds USDH, USDT0 or USDE, `hl_swap` (in
`hyperliquid-trading`) converts it into USDC so it can back a trade.

### Reading the numbers

From `clearinghouseState`:

- **`marginSummary.accountValue`** — everything the account is worth right now,
  including unrealised profit and loss. This is the number to quote when someone
  asks "how much is in there".
- **`withdrawable`** — the part not tied up as margin.
- **`assetPositions[].position`** — one entry per open position:
  - `szi` is the size **and the direction**: positive is long, negative is short.
    A `szi` of `-0.5` on ETH is short half an ether, not long.
  - `entryPx` is the average price you got in at.
  - `unrealizedPnl` is profit or loss if it closed now, in USD.
  - `liquidationPx` is the price at which the position is force-closed. Distance
    from the current price to this number is the single most useful risk figure
    you can report.
- **No open positions is normal**, not an error. Say "no open positions" and stop.

**Funding** is the recurring payment between longs and shorts on a perpetual.
A positive rate means longs pay shorts. It is charged periodically whether or
not the position is profitable, so on a position held for a long time it is a
real cost worth mentioning.

**If your account reads look empty while your orders are succeeding, stop and
report it.** Reading one exchange while trading another would make every number
you report meaningless. That mismatch is a fault for a human to fix, not
something for you to work around.

## Rate limits — the one rule that matters

Hyperliquid limits requests **per IP address**, and the dashboard makes every
call for the **entire fleet** from one address. Your polling loop is not yours
alone: it is shared with every other agent, and spending the budget can stop
other agents from trading.

- Ask for what you need, once. Read again when something changed or when the
  person asked again.
- **Never poll in a tight loop.** If you are watching a position, read on the
  timescale that actually matters — minutes, not seconds.
- `allMids` gives you every price in one call. Never loop over assets calling
  `l2Book` when you only wanted prices.
- Identical market reads within a few seconds are served from a short cache, so
  hammering gains you nothing anyway. Account reads are never cached.

## When a read fails

| Code | Meaning | What to do |
|---|---|---|
| `no_bound_address` | No Hyperliquid wallet is bound to you, so there is no account to read. | Tell your owner to enable Hyperliquid from the agent's **Wallet** tab. Market reads still work. |
| `user_not_accepted` | Something tried to specify an address. | Never send one — the server fills it in. |
| `upstream` (502) | The exchange is failing, unreachable, or rejected the read — an unknown symbol usually lands here. | Say the exchange is not responding, and check the symbol against `meta`. Wait before trying again; do not retry in a loop. |
| `bad_request` (400) | `type` is missing. | Fix the call. |
| `internal_error` (500) | Something broke server-side. | Report it. Do not retry in a loop. |

## What this skill does not do

- **It cannot trade.** No orders, no cancels, no leverage changes.
- **It cannot see other people's accounts** — only your own.
- **It cannot move money out.** There is no withdraw, vault or staking
  operation anywhere in this integration — not disabled, simply absent, with no
  code path that could sign one. Nothing can send funds off this account or to
  another address, and that is by design.
- **Funding the perp account is the one exception, and it lives in
  `hyperliquid-trading`.** USDC on the **spot** side cannot back a perp trade;
  `hl_transfer` moves it across inside your own account, spot to perp only.
  That is a different skill — read it before funding. Two things to get right
  even from here: it is **not** a deposit and **not** a bridge, and your
  Hyperliquid account **is** your wallet address while the Trading Key only
  signs for it. So if perp margin is short, the answer is never "send USDC
  somewhere" or "re-point the Trading Key at the wallet".
- **It cannot tell anyone what to trade.** Report what the numbers say. Do not
  offer investment advice, price predictions, or a recommendation to buy or
  sell — you are not a financial adviser and the person may be relying on you.
