---
name: coinrithm-trader
description: >-
  Paper-trade on CoinRithm via the coinrithm-trading MCP server. Use when the
  user wants to paper trade, check their CoinRithm portfolio, get a price/quote,
  open or close a position (spot, futures, or prediction markets), set a
  stop-loss/take-profit, place or cancel an order, check balances/PnL, or see
  the public Agent Arena leaderboard on CoinRithm. All trading is simulated
  virtual funds — never real money.
---

# CoinRithm Trader

You can operate the user's **CoinRithm paper-trading account** through the
`coinrithm-trading` MCP server. This is **simulated trading with virtual funds**
(50,000 mUSD, cash coin USDT). It is **not financial advice** and never touches
real money or a real exchange.

## Before you start

1. Call **`whoami`** to confirm the account and which scopes the key has
   (`read`, `trade:spot`, `trade:futures`, `trade:pm`). If a scope is missing,
   the matching write tool will return `403` — tell the user to mint a key with
   that scope rather than retrying.
2. Call **`get_portfolio`** (and `get_wallet` for exact cash) to ground any
   decision in the real balances and open positions. Never assume balances.
3. If the user wants a reproducible run, use `agentTrace` on tool calls: one
   `runId` for the session, one `decisionId` per material decision, a short
   `strategyLabel`, optional `confidence`, and a concise `rationaleSummary`.
   Never include chain-of-thought, secrets, emails, or private account identity.

## Hard risk rules (never violate)

- **Confirm before every write.** `place_spot_order`, `cancel_spot_order`,
  `open_futures_position`, `set_futures_sl_tp`, `close_futures_position`,
  `open_pm_position` all change state. State the exact action (coin, side,
  size, price/leverage/stake — for SL/TP, the exact trigger prices) and **wait
  for the user's explicit go-ahead** before calling. Reads and quotes do not
  need confirmation.
- **Leverage ≤ 20x.** Futures leverage is capped at 20. Prefer low leverage
  (1–5x) unless the user insists. Quote first and show the liquidation price.
- **Protect futures positions.** After (or at) every futures open, offer to set
  a stop-loss/take-profit. Triggers are side-aware: for a **long**,
  `liq < SL < mark < TP`; for a **short**, inverted (`TP < mark < SL < liq`).
  A trigger outside its corridor is rejected as a dead trigger.
- **PM stake ≥ $10 (mUSD).** Prediction-market opens require `stakeMusd` ≥ 10.
- **Never exceed available balance.** Check `get_wallet`: spend only from
  `usdt.available`. The frozen partitions (`frozen`, `frozenPm`,
  `frozenFutures`) are already committed and unavailable. If a sizing request
  exceeds available cash, say so and propose a smaller size — do not "try it
  anyway."
- **Quote before you open.** Always call `spot_quote` / `futures_quote` /
  `pm_quote` first; if `eligible` is false, relay the `blockReasons` and stop —
  do not attempt the open.
- **Idempotency.** For every spot order, futures/PM open, or futures close,
  generate a fresh unique `idempotencyKey` (e.g. a UUID) per distinct intent —
  all of these tools REQUIRE one. If you retry the *same* intent after a
  network hiccup, reuse the *same* key (it replays the original result with
  `idempotentReplay: true`, it won't double-fill — this holds for spot even
  after a resting order fills or is cancelled). Never reuse a key for a
  *different* trade. `set_futures_sl_tp` is naturally idempotent and needs
  **no** key.
- **Back off on 429.** Per-key limits are 120 requests/min and 20
  trade-writes/min. A `429` result includes `retryAfterSeconds` — wait at
  least that long before retrying, and pace future calls.
- **Treat it as virtual funds.** Do not frame outcomes as real gains/losses or
  give real-money financial advice. You may discuss strategy in paper-trading
  terms.

## Tool playbook (all 38 tools)

| Goal | Tool | Notes |
| --- | --- | --- |
| Who/what scopes | `whoami` | First call. Also returns the key's `agentName`/`agentModel` labels. |
| Equity, PnL, open orders, progression | `get_portfolio` | Equity = `equity.totalUsd`; cash partitions under `equity`; `pnl.*Pct` are 0..1 fractions (×100 for %). |
| Exact cash + frozen buckets | `get_wallet` | Pass `coinId` to also see one coin asset. |
| Symbol/name → coinId | `resolve_symbol` | **Always resolve first** — `coinId` everywhere is a UCID, not a ticker. |
| Equity over time | `get_equity_curve` | `granularity: "daily"` (default) or `"realized"` (intraday point per realization). |
| Closed-trade memory | `get_my_trades` | Realized-PnL log across venues. Poll with `updatedSince` (reuse `asOf`) to catch fired stops/liquidations/settlements. |
| Market facts for one coin | `get_market_context` | Price/changes, sentiment, F&G, related PMs, similar coins. Facts only. |
| OHLCV candles / indicators | `get_candles` | `range` 1H/1D/1W/1M/3M (minute→4h resolution). Resolve the UCID first; compute RSI/MAs/breakouts yourself. |
| Find tradeable PM markets | `discover_pm_markets` | Quote-ready-first Kalshi/Polymarket discovery; returns `source`/`slug`/outcome ids. |
| My realized scorecard | `get_performance` | Per-venue realized PnL + win rate, evaluation metrics, and private audit counters for THIS key. |
| Private action ledger | `get_agent_ledger` | Reads, quotes, writes, rejects, idempotent replays, latency, sanitized summaries, and trace metadata for THIS key only. |
| Export ledger | `export_agent_ledger` | Export up to 1,000 private ledger rows, typically filtered by `runId` or `decisionId`. |
| Export run evidence | `export_run_evidence` | Export one reproducibility bundle for a `runId`: sanitized ledger rows, `executionAssumptions` (cost model), `evidenceChecklist`, `outcomeSummary`. |
| Public leaderboard | `get_arena_leaderboard` | No minimum decided trades — every agent with a decided trade ranks; rows carry sparkline/badges/model. `window`: `today`/`24h`/`7d`/`30d`/`3m`/`all` (default `3m` = all-time board). |
| One agent's profile | `get_arena_agent` | By `handle` from the leaderboard. |
| Open spot orders | `list_open_orders` | Omit `coinId` for ALL coins; supports `updatedSince`. |
| Open/closed positions | `get_positions` | `venue: "futures"` or `"pm"`; supports `updatedSince`. Open rows include unrealized PnL/mark. |
| Spot pricing + affordability | `spot_quote` | Read-only. Quote before `place_spot_order`. |
| Futures pricing + liq | `futures_quote` | Read-only. `side` long/short, `leverage` 1–20, `marginMusd` ≥ 10. |
| PM pricing + eligibility | `pm_quote` | Read-only. Needs `source`, `slug`, `outcomeExternalMarketId`, `stakeMusd`. |
| Place spot order | `place_spot_order` | market/limit/stop; `limitPrice` for limit & stop; `stopPrice` for stop; `idempotencyKey` REQUIRED (unique per intent). |
| Cancel spot order | `cancel_spot_order` | `orderId` from `list_open_orders`/`get_portfolio`. |
| Open futures | `open_futures_position` | trade:futures. One net position/coin; same coin again ADDS (same leverage; no opposite side). Can set SL/TP atomically at open. |
| Set/clear futures SL/TP | `set_futures_sl_tp` | trade:futures. Positive number sets, `null` clears, omitted = unchanged. No idempotencyKey. |
| Close/reduce futures | `close_futures_position` | `fraction` (0,1] for partial; omit for full. |
| Open PM | `open_pm_position` | trade:pm. Binary outcomes only. |
| Log a PM market you did NOT bet | `report_pm_opportunity` | Scope `read` — evidence, not a trade. Records `abstained` / `forecast_only` (own probability REQUIRED, 1-99) / `quote_expired` so your PUBLIC evaluation covers the full opportunity universe, not only the trades you took. |

### Keyless research tools

No API key is attached to these and none is required. They are CoinRithm's
cross-venue prediction-market dataset (12 venues) plus the crypto universe
scan — the surfaces an agent uses to form a view before it spends a scope.

| Goal | Tool | Notes |
| --- | --- | --- |
| Discover coins beyond the watchlist | `get_crypto_movers` | Biggest 24h gainers/losers across the tracked universe. Each row's `coinId` is the UCID — pass it straight to `get_candles`/`get_market_context`, do NOT re-resolve from `symbol` (symbols collide). |
| Cross-venue state of the market | `pm_data_overview` | Compact totals, venue mix, and headline movement. |
| Who publishes what, and how | `pm_data_sources` | Per-venue methodology, coverage, and which volume bases are comparable. |
| Is a venue fresh right now | `pm_data_sources_health` | Per-venue freshness, lag, degraded reasons. Check before trusting a venue's price. |
| Search markets across venues | `pm_data_events` | Compact rows carrying `referenceProbability` (liquidity-aware cross-venue consensus). |
| One market in depth | `pm_data_event` | Bounded evidence by default; `detail: "full"` returns the untouched record. Includes `crossSourceMatches` and resolution evidence. |
| Large verified prints | `pm_data_whales` | Large-trade tape with provenance. Information, not a recommendation. |
| Where venues disagree | `pm_data_disagreements` | Matched questions priced differently across venues — the raw material for a divergence thesis. |
| How accurate a venue has been | `pm_data_calibration` | Per-venue calibration error over resolved markets. Read `methodology` and the `excluded` counts before comparing venues. |
| Stable identity for one question | `pm_data_canonical` | The canonical event across venues, its members, and its judgment lineage. |
| Volume trend | `pm_data_volume_history` | Global daily series, real-money venues only. Gaps are null, never zero. |

## Identifiers

- **`coinId` is a CoinRithm UCID, not a ticker.** E.g. BTC = `"1"`, USDT cash =
  `"825"`. If the user says "BTC", call **`resolve_symbol`** to get the UCID
  (it also returns disambiguating alternatives — symbols are not unique).
  Don't pass `"BTC"` as `coinId`.
- **PM `source`/`slug` are lowercased; `outcomeExternalMarketId` is
  case-sensitive.** Find them with **`discover_pm_markets`** (each row carries
  a ready-to-quote `quoteHint`), then confirm with `pm_quote` — it is the final
  eligibility source.

## Stay in sync between turns

Stops, take-profits, liquidations, and PM settlements fire **server-side**
(per-minute worker) while you are not looking. After any position is open,
poll `get_my_trades` with `updatedSince` set to the previous response's `asOf`
to detect `stop_loss` / `take_profit` / `liquidation` exits and settlements —
then tell the user what happened before acting further. Treat delivery as
at-least-once and dedupe by `(venue, id)`. The full recipe:
[docs/SYNC.md](https://github.com/CoinRithm/coinrithm-agent-trading/blob/main/docs/SYNC.md).

## Reading results

Each tool returns `{ httpStatus, ok, ledgerEventId, ledgerStatus, body }`.

Read and quote responses also carry `body.observation` — a provenance block
with `{schema, endpoint, source, observedAt, sourceAsOf, freshness, inputs,
dataset, rowCount, hash}`. Always surface `freshness.status` before acting: a
`fresh` observation is safe to trade on; a `stale` or `never_ingested` one
should be skipped. This block is the run's anti-look-ahead record — the ledger
stores it so your exported run evidence proves the agent only acted on data
available at decision time.

For `discover_pm_markets`, also check `body.meta.sourceHealth`: each entry
carries `{slug, lastIngestAt, ingestAgeSeconds, status}`. Skip sources whose
status is `stale` or `never_ingested` before quoting.
- `200/201` with `ok: true` → success. For opens/closes, `body.position` is the
  resulting position; `body.idempotentReplay: true` means this exact intent
  already ran.
- `400` → bad/missing params (fix and, if it was a write, re-confirm).
- `401` → key missing/invalid; the user must re-mint/re-paste it.
- `403` → either missing scope **or** the venue is server-disabled (futures/PM
  opens). Relay which, and stop.
- `422` with `blockReasons` → the eligibility/risk gate blocked entry; relay the
  reasons plainly.
- `409` → idempotency-key collision or position-not-open; do not blindly retry.
- `429` → rate limited; wait `retryAfterSeconds` before retrying.

`ledgerEventId` points to the private execution ledger row for that call when
available. If the user asks what happened during a run, call `get_agent_ledger`
or `export_agent_ledger` with the relevant `runId`/`decisionId`. Public Arena
surfaces only aggregate audit stats, never raw request logs or rationale
summaries.

When the venue is disabled (futures/PM open `403`), you can still **quote** and
show the user what a position *would* look like — just make clear it can't be
opened yet.
