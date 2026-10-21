# Autopilots

An autopilot runs the four live agents (indicator, intelligence, fundamental, decision) on one symbol on a schedule,
optionally managing a paper position. Everything it does lands in an event log you read with a cursor.

## Connect your own real-trading system

You can use the API's analyses and signals to drive your own authorized trading system. Your integration reads
the event log below and submits real orders through your broker or exchange API, using your own account and
permissions. SimianX's position history and manual position actions remain simulations inside the platform.
Check real order status and fills with your execution system; a simulated fill in SimianX does not confirm an
external fill. Use the event cursor to resume processing and check `expires_at`, when present, before using a signal.

## Start

`POST /v1/autopilots` (scope `automation:manage`, metered: each analysis cycle costs the models it uses; `typical_points_per_cycle` in the answer)

```json
{"asset": "crypto", "symbol": "BTC", "timeframe": "15m", "tier": "fast",
 "agents": ["indicator", "intelligence", "fundamental", "decision"],
 "intervals": {"indicator": 900, "decision": 900},
 "ai_position_control": true, "timing_gate": false,
 "webhook": {"url": "https://example.com/hook", "secret": "…", "events": ["live_crypto_position_opened"]},
 "language": "en"}
```

- `asset`: `crypto` or `stock`; `symbol`: `BTC`, `BTC-USDT-SWAP`, `NVDA`.
- `timeframe`: crypto `1m 5m 15m 1H 4H 1D`; stock `1m 15m 1H 1D 1W 1mo`.
- `tier` picks a model per agent (`fast | standard | frontier`); `models` `{agent: model_id}` overrides per agent (paid
  plans; ids from `GET /v1/models`, `live.crypto` / `live.stock` lists; an unknown id is 400 `invalid_parameter` with
  `data.allowed`). `PATCH /v1/autopilots/{id}` with `models` or `tier` changes them for the next cycles.
- `intervals` are seconds per agent (≥ 60). Without them the account's saved defaults apply.
- `ai_position_control` (default true): the decision agent opens, moves and closes a paper position; `position.changed`
  events follow. `webhook` is optional (HMAC-signed `X-SimianX-Signature: sha256=…` over `"<ts>.<body>"` when `secret` is set).
- Answer: `data.autopilot` (id, session_id, status, models, intervals…), `data.cursor` (start reading events here), `data.events_url`.
- Limits: running autopilots per plan (Free 1, Starter 2, Plus 3, Pro 10) and `ai_concurrency`; 429 `autopilot_limit` / `ai_concurrency` when full.

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

Cursors are stable for 7 days (the stream holds the recent tail; older cursors are served from the table).

## History

- `GET /v1/autopilots/{id}/analyses?agent=decision&limit=20&before=<timestamp>&include=text`
- `GET /v1/autopilots/{id}/positions?status=open|closed&limit=20` (positions with their operations)
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
timeframes (`1m 15m 1H`) can only enter while the US market is open, pre- or post-market included (409 `market_closed`
with `data.next_open_et`); `1D 1W 1mo` autopilots hold their bracket overnight and can enter any time at the last
price. One action runs at a time per autopilot (409 `state_conflict`, retry in a moment). With
`ai_position_control: true` the decision agent may later move or close what you opened; set it to `false` if the
book is yours alone (the agent still analyses and fires `signal.fired`).

```bash
curl -s $API/v1/autopilots/$ID/actions -H "Authorization: Bearer $SIMIANX_API_KEY" -H 'Content-Type: application/json' \
  -d '{"action":"open","side":"long","notional_usd":1000,"stop_loss":96000,"take_profit":108000}'
```

## Run one agent now

`POST /v1/autopilots/{id}/run {"agent": "decision"}` (metered like the schedule; `data.typical_points`). Answer 202:
the run is queued and its result arrives in the event log as `analysis.completed` / `analysis.failed` (then the
schedule continues from that completion). 409 `run_in_progress` while that agent is queued or running, 429
`run_too_soon` (with `Retry-After`) within 60 s of its last result, 409 `state_conflict` while the owner has the live
page open on the same session (it runs the agents itself). On a stock autopilot outside market hours the indicator
and decision agents answer `analysis.completed` with `skipped: market_closed`.

## Control

- `GET /v1/autopilots` (`?status=running`, `?archived=1`), `GET /v1/autopilots/{id}`
- `PATCH /v1/autopilots/{id}` with any of `timeframe`, `tier` / `models`, `intervals`, `timing_gate`, `language`, `ai_position_control`.
  `timeframe` behaves like the `set_timeframe` action (closes the book first); `ai_position_control: false` cancels the
  resting order and closes the open position (`close_reason: user_disabled`, no notification, still in the event log).
- `POST /v1/autopilots/{id}/stop`, `POST /v1/autopilots/{id}/start` (restart, same checks as create), `DELETE /v1/autopilots/{id}` (archive; must be stopped)

Stops from the web app also appear as `autopilot.stopped` in the log, so a runner always learns about them.
