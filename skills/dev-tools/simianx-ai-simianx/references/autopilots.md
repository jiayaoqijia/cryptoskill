# Autopilots

An autopilot runs the four live agents (indicator, intelligence, fundamental, decision) on one symbol on a schedule,
**server side**: it keeps going when you are offline, which is the difference from a live session
(`references/live.md`, which needs you connected). Optionally it manages a paper position. Everything it does lands
in the updates feed and in an event log you read with a cursor.

## What the user hears

Every analysis and every decision of an autopilot started over the API is an update in `GET /v1/updates`
(`references/following.md`), with a `say` line: `autopilot.started`, then per cycle `fundamental_done`,
`indicator_done`, `intelligence_done` (whichever finishes first comes first), `decision` (the full plan), `next_run` (when the next cycle runs), and `position.changed` when the simulated book moves;
`autopilot.stopped` / `autopilot.paused` at the end. Relay each as it arrives; when you were away, the feed has
everything you missed, poll it every 10 s exactly (or `wait=30`) and catch up from the cursor. When the user asks
"what is running?", list the autopilots (symbol, timeframe, since when, next run, last decision).

## Simulated positions

An autopilot's positions, its position history and the manual position actions are simulations inside SimianX:
SimianX places no real orders and has no access to exchange, broker or bank accounts. Code that reads the event log
below resumes from the event cursor and checks `expires_at`, when present, before using a signal.

## Start

`POST /v1/autopilots` (scope `automation:manage`, metered: each analysis cycle costs the models it uses; `typical_points_per_cycle` in the answer)

```json
{"asset": "crypto", "symbol": "BTC",
 "agents": ["indicator", "intelligence", "fundamental", "decision"],
 "intervals": {"indicator": 900, "decision": 900},
 "ai_position_control": true, "timing_gate": false,
 "webhook": {"url": "https://example.com/hook", "secret": "…", "events": ["live_crypto_position_opened"]},
 "language": "en"}
```

- `asset`: `crypto` or `stock`; `symbol`: `BTC`, `BTC-USDT-SWAP`, `NVDA`.
- `timeframe`: crypto `1m 5m 15m 1H 4H 1D`; stock `1H 1D 1W 1mo`. Default: the saved one (`GET /v1/settings`).
- Models: the user's saved setup (`GET /v1/settings`); `models` `{agent: model_id}` overrides per agent for this autopilot
  (paid plans; ids from `GET /v1/models`, `live.crypto` / `live.stock` lists; an unknown id is 400 `invalid_parameter` with
  `data.allowed`). `PATCH /v1/autopilots/{id}` with `models` changes them for the next cycles.
- `intervals` are seconds per agent (≥ 30; fundamental ≥ 1800; ≤ 86400, out-of-range values are clamped). Without them the account's saved defaults apply.
- `ai_position_control` (default true): the decision agent opens, moves and closes a paper position; `position.changed`
  events follow. `webhook` here is the engine's own per-autopilot notification channel (HMAC-signed
  `X-SimianX-Signature: sha256=<hex>`, the HMAC-SHA256 of `"<ts>.<raw body>"` with `ts` from the `X-SimianX-Timestamp`
  header, when `secret` is set); account-wide webhooks that carry every
  update of every run are `POST /v1/webhooks` (`references/developers.md`).
- `timing_gate` (crypto, default false): while the autopilot holds no position and no resting order, our timing-gate
  model scores each decision candle before the indicator and decision agents run. Gated timeframes are the ones the
  active model has a threshold for (now 1m, 5m, 15m); others run as usual. Below the threshold both agents skip that
  candle without a model call:
  - the decision answers `analysis.completed` with `skipped: "timing_gate"`, `model` (the gate model, `SX-1`; a
    retrained model becomes `SX-2`, …), `conclusion.gate` (`passed: false`, `score`, `threshold`, `candle_close`,
    `timeframe`, `model_name`; `score` / `threshold` may be null) and `points`: 0.05 the first time the candle is
    skipped, 0 when a manual `run` hits the same candle again (one charge per candle);
  - the indicator answers `analysis.completed` with `skipped: "timing_gate"` and no new report: the latest
    indicator report stays the current one.
  A manual `run` goes through the gate too; breaking-news decisions are not gated.
- Answer: `data.autopilot` (id; session_id, the session it runs on: `/v1/live/sessions/{id}` answers 404 for it, use the autopilot's `id`; status, models, intervals…), `data.cursor` (start reading events here), `data.events_url`,
  `data.next_step` (keep following). Ask the human before starting one that manages a paper position.
- Limits: running autopilots per plan (Free 0: 403 `plan_required`, Starter 2, Plus 3, Pro 10); all in use: 409
  `autopilot_limit` (stop one first; waiting does not free a slot); `ai_concurrency` 429 when analyses are running.
- Send an `Idempotency-Key` (MCP: `idempotency_key`) so a retry after a timeout returns this autopilot instead of
  starting a second one.
- Stopping or archiving ends the analysis, not the paper book: an open position keeps its stop and target and a
  resting order can still fill. To be flat, `close` and `cancel_order` first (actions below); archive is undone by
  `POST /v1/autopilots/{id}/start`.

## Read the event log

`GET /v1/autopilots/{id}/events` (free; does not count against points, only against requests)

| Param | Meaning |
|---|---|
| `after` | cursor = `id` of the last event you processed. Omit to get the newest 50 and a cursor. |
| `wait` | 0–30 s: hold the request until something arrives after `after` |
| `types` | comma list to filter |
| `limit` | ≤ 200 |
| `stream=1` | server-sent events instead (`id:` = cursor, `event:` = type; `event: reconnect` → reconnect with the last id) |

Event types: `autopilot.started`, `autopilot.stopped` (`data.reason`: requested | insufficient_points), `autopilot.paused_budget`,
`autopilot.config_updated`, `autopilot.action` (what the API was told to do by hand: `data.action`, `data.agent` for runs), `analysis.completed` (`data.agent`, `data.conclusion`, `data.proposal` for the decision agent, `data.points`),
`analysis.failed`, `signal.fired` (a long/short proposal: side, confidence, entry_price, stop_loss, take_profit; `expires_at` set),
`position.changed` (`data.operation`: open | add | reduce | close | close_and_reverse | update_sl | update_tp | update_both |
place_order | fill_order | cancel_order…, with side, quantity, entry_price, stop_loss, take_profit, pnl, capital; `expires_at` set).
Every field of these payloads is listed under "Field reference" below.

Cursors are stable for 7 days (the stream holds the recent tail; older cursors are served from the table).

## History

- `GET /v1/autopilots/{id}/analyses?agent=decision&limit=20&before=<timestamp>&include=text`
  (rows with `agent: "gate"` are decision candles the timing gate skipped; `?agent=decision` lists them with the
  decisions. `gate` is not a filter value of its own: `?agent=gate` is 400 `invalid_parameter`)
- `GET /v1/autopilots/{id}/positions?status=open|closed&limit=20` (positions with their operations; the AI's hold checks
  are summed per position as `holds` and `last_hold`, `include=holds` lists them all)
- `GET /v1/autopilots/{id}/logs`

## Act on the paper book by hand

`POST /v1/autopilots/{id}/actions` (scope `automation:manage`, free, counts as a heavy request). The autopilot's paper
position is the one the decision agent trades, so what you do here shows up in the agent's own history, is watched by
the stop-loss / take-profit monitor, and lands in the event log (`position.changed` with `expires_at`, plus an
`autopilot.action` record). Prices are always the server's current price (`data.price`, `data.price_source`:
`live`, `recent_bar` or `last_close`); you never send one.

| `action` | Fields | Notes |
|---|---|---|
| `open` | `side` (`long`/`short`; stock: `long` only), `quantity` **or** `notional_usd`, `stop_loss?`, `take_profit?` | 409 `position_exists` if a position or resting order exists; 400 `insufficient_capital` beyond the paper capital |
| `add` | `quantity` or `notional_usd` | adds at the current price (cost averaging) |
| `reduce` | `quantity`, `notional_usd` or `fraction` (0–1) | a full reduce is a close |
| `close` | – | closes at the current price (`close_reason: manual`) |
| `set_levels` | `stop_loss?`, `take_profit?` (at least one) | 400 `invalid_levels` when a level sits on the wrong side of the price |
| `place_order` | `side`, `order_type` (`limit`; crypto also `stop`), `price`, `quantity` or `notional_usd`, `stop_loss?`, `take_profit?`, `expires_in?` (s, default 86400) | a limit waits below (long) / above (short) the market, a stop the other way; filled by the monitors, `position.changed` `fill_order` follows |
| `replace_order` | any of `price`, `stop_loss`, `take_profit`, `expires_in` (stock also `quantity`) | 409 `no_pending_order` when nothing rests |
| `cancel_order` | – | |
| `set_timeframe` | `timeframe` | cancels the resting order and closes the position (`close_reason: timeframe_changed`) first, then moves the autopilot; `data.closed_position`, `data.cancelled_order` |

Every answer carries `data.position`, `data.pending_order`, `data.capital` (`initial`, `realized_pnl`, `occupied`,
`available`) and `data.cursor`. `open`, `add`, `place_order` and `set_timeframe` need a running autopilot (409
`autopilot_not_running`); closing, reducing, moving levels and cancelling work on a stopped one too. Stocks: intraday
timeframes (`1H`) can only enter while the US market is open, pre- or post-market included (409 `market_closed`
with `data.next_open_et`); `1D 1W 1mo` autopilots hold their bracket overnight and can enter any time at the last
price. One action runs at a time per autopilot (409 `state_conflict`, retry in a moment). With
`ai_position_control: true` the decision agent may later move or close what you opened; set it to `false` if the
book is yours alone (the agent still analyses and fires `signal.fired`). Paper only, and only when the user asks:

```bash
curl -s $API/v1/autopilots/$ID/actions -H "Authorization: Bearer $SIMIANX_API_KEY" -H 'Content-Type: application/json' \
  -d '{"action":"open","side":"long","notional_usd":1000,"stop_loss":96000,"take_profit":108000}'
```

## Field reference (paper book and events)

The same fields are in `GET /v1/openapi.json` under `components.schemas` (`Position`, `Operation`, `Capital`,
`PaperState`, `TimeframeChanged`, `Event`, `PositionChanged`, `Proposal`, `AnalysisCompleted`). Prices are USD, quantities are coins or
shares, `null` means not set. A script can rely on these names without waiting for a first trade.

**Position** (`GET …/positions` → `data.positions[]`, newest first; `data.position` / `data.pending_order` of an action)

| Field | Meaning |
|---|---|
| `id`, `side` | `long` or `short` |
| `status` | `placed` (entry order waiting), `open`, `closed`, `force_closed`, `cancelled`; an entry order that was cancelled or expired ends `cancelled` (crypto) or `force_closed` (stock), `close_reason` says which |
| `quantity`, `entry_price`, `current_price`, `close_price` | size and prices; `current_price` is the monitor's last mark |
| `stop_loss`, `take_profit` | current levels |
| `pnl`, `pnl_percentage` | USD and percent: unrealised while open, realised once closed |
| `position_value_usd`, `fees` | quantity x current price; simulated fees so far |
| `order_type`, `limit_order_price` | `market`, `limit` or `stop`; the resting price of an entry order |
| `close_reason` | `ai_decision`, `manual`, `stop_loss`, `take_profit`, `user_disabled`, `timeframe_changed`, `order_expired`, `order_cancelled`, `connection_closed`, `system_error`; stock also `market_closed`, `orphan_stop_loss`, `orphan_take_profit` (a level hit while nobody watched) |
| `timeframe`, `opened_at`, `filled_at`, `closed_at` | |
| `operations[]` | positions endpoint only: every change, oldest first (below); `holds` + `last_hold` sum up the AI's hold checks |

**Operation**: `id`, `type` (`open`, `add`, `reduce`, `close`, `close_and_reverse`, `update_sl`, `update_tp`,
`update_both`, `place_order`, `fill_order`, `cancel_order`, `expire_order`, `replace_order`, `wait_order` (the AI kept a
resting order), `hold`), `execution_price`,
`quantity_change` (+ added, − removed), `before_quantity`, `after_quantity`, `stop_loss`, `take_profit` (after the
operation), `realized_pnl`, `fee`, `confidence` (the decision's confidence in percent, 0–100; a manual crypto action records
100, an engine fill or cancel of a crypto entry order 0), `pnl_at_operation`, `pnl_percentage_at_operation`,
`rationale`, `created_at`.

**Capital** (`data.capital` of an action): `initial`, `realized_pnl`, `occupied` (open position + resting order),
`available` (= initial + realized_pnl − occupied; more than this is 400 `insufficient_capital`). `set_timeframe`
answers differently: `action`, `timeframe`, `previous` (or `unchanged: true`), `closed_position`, `cancelled_order`,
`autopilot`, `cursor`.

**Event** (`GET …/events` → `data.events[]`, then `data.cursor`): `id` (pass as `after`), `type`, `autopilot_id`, `ts`,
`expires_at` (on `signal.fired` and `position.changed`: act before it or skip the event), `data`:

- `signal.fired`: `agent`, `analysis_id`, `action` (`long`/`short`), `side`, `score`, `confidence` (0–1), `risk_level`,
  `entry_type` (`market`/`limit`/`stop`), `entry_price`, `stop_loss`, `take_profit`, `rationale`.
- `position.changed`: `symbol`, `market`, `operation` (an operation type above, never `hold` or `wait_order`), `operation_id`,
  `position_id`, `side`, `status`, `execution_price`, `quantity_change`, `quantity`, `entry_price`, `position_value`,
  `stop_loss`, `take_profit`, `pnl`, `pnl_percentage`, `pnl_at_operation`, `capital_remaining`, `capital_initial`,
  `current_price`, `rationale`.
- `analysis.completed`: `agent`, `analysis_id`, `timeframe`, `model`, `points`, `skipped` (`timing_gate`,
  `extension_guard`, stock `market_closed` / `market_holiday`, or null), `signal`, `conclusion`, and for the decision agent `proposal` (the `signal.fired` fields;
  `action` may also be `hold`, `wait` or `no_trade`).

## Run one agent now

`POST /v1/autopilots/{id}/run {"agent": "decision"}` (metered like the schedule; `data.typical_points`). Answer 202:
the run is queued and its result arrives in the event log as `analysis.completed` / `analysis.failed` (then the
schedule continues from that completion). 409 `run_in_progress` while that agent is queued or running, 429
`run_too_soon` (with `Retry-After`) within 60 s of its last result, 409 `state_conflict` while the owner has the live
page open on the same session (it runs the agents itself). On a stock autopilot outside market hours the indicator
and decision agents answer `analysis.completed` with `skipped: market_closed`. With `timing_gate` on, the indicator and
decision agents answer `analysis.completed` with `skipped: timing_gate` on a candle the gate skips (see Start).

## Control

- `GET /v1/autopilots` (`?status=running`, `?archived=1`), `GET /v1/autopilots/{id}`
- `PATCH /v1/autopilots/{id}` with any of `timeframe`, `models`, `intervals`, `timing_gate`, `language`, `ai_position_control`.
  `timeframe` behaves like the `set_timeframe` action (closes the book first); `ai_position_control: false` cancels the
  resting order and closes the open position (`close_reason: user_disabled`, no notification, still in the event log).
- `POST /v1/autopilots/{id}/stop`, `POST /v1/autopilots/{id}/start` (restart, same checks as create), `DELETE /v1/autopilots/{id}` (on request) (archive; must be stopped)

Stops from the web app also appear as `autopilot.stopped` in the log, so a runner always learns about them.
