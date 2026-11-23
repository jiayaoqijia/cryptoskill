---
name: openmarket-chart-mcp
description: Use when wiring, reading or screening OpenMarket data.
---

# OpenMarket chart MCP (read + control charts)

Trigger: user drops `https://mcp.openmarket.xyz/llms.txt` (often with "connect to chart <id>"), or asks to read/control
an OpenMarket chart. Remote MCP, Streamable HTTP, OAuth 2.1 with DCR + PKCE. Docs: that llms.txt is authoritative.

## 1. Wire the server (OAuth, headless box)
```bash
hermes mcp add openmarket --url https://mcp.openmarket.xyz/ --auth oauth --connect-timeout 15
hermes config set mcp_servers.openmarket.auth oauth      # add saves enabled:false and drops auth when the flow can't run
hermes config set mcp_servers.openmarket.enabled true
hermes config set mcp_servers.openmarket.oauth.timeout 1800   # default 300s is too short for a human round-trip
```
`hermes mcp add` cannot complete OAuth non-interactively: it falls back to "continue without authentication", and the
saved entry then lacks `auth: oauth`. The `hermes config set` pair above is the fix. The patch/write tools REFUSE to edit
`~/.hermes/config.yaml` (security guard) — use `hermes config set`.

## 2. Complete the flow with the paste-back path
```bash
# pty + background so the callback listener stays alive across turns
hermes mcp login openmarket        # run with terminal(pty=True, background=True)
```
It prints an authorize URL and binds `http://127.0.0.1:<port>/callback`. The user opens the URL on THEIR device (phone
is fine), picks the access level on the consent page, then the browser fails to load the loopback callback — they copy
the full URL from the address bar and send it. Feed it back with
`process_manage(action="submit", data="<full redirect url>")`. Success prints `Authenticated — N tool(s) available`.

Access levels on the consent page: "Read only" / "Read and control charts" / "Read, control charts and trade"
(+ "Alerts and watchlists", ticked by default). Granted scopes land in `~/.hermes/mcp-tokens/openmarket.json`
(`scope` key) and decide which tools are even advertised: `mcp:read` (+`mcp:chart`) gives 34 tools, `mcp:trade` adds 8
order/account tools, `mcp:alerts` adds the `alert_*`/`watchlist_*` set (49 total). Recommend chart+alerts, NOT trade,
unless the user asks: trade orders execute from the user's own tab.

## 3. Use the tools when the session predates the connector
A running gateway loads MCP tools at session start; a freshly added server is absent from `tool_search` until a new
session or the user sends `/reload-mcp`. Bridge immediately with `scripts/om_call.py` (uses the stored token, refreshes
it when within 120s of expiry):
```bash
<V>/bin/python3 om_call.py chart_workspace_select '{"workspaceId":"gCFPxwgy"}' chart_status '{}' chart_read '{}'
```
where `<V>` is the venv that carries mcp 2.0 (find it: `grep -rl "streamable_http_client" /home/ubuntu/.hermes/installs/*/environments/*/venv/lib/python3*/site-packages/mcp/client/`).
The `mcp` package in `~/.hermes/hermes-agent/venv` is too old (no `streamablehttp_client`); the tools' python 3.14
interpreter has no `mcp` at all — the `installs/.../venv` one is the interpreter that works.

## 4. Working order after connecting (per llms.txt)
1. `chart_workspace_select` with the id from the user's sentence (never assume the active workspace).
2. `chart_status {}` → connection + active workspace.
3. `chart_refresh {}` → name, url, layout, panes (symbol/exchange/interval), every indicator with settings.
4. `chart_read {}` → the numbers on screen (last, change over visible bars, high/low/volume, indicator values).
5. Offer ONE visible change and wait for a yes; report what changed after making it.

## 5. What the connector does not cover (answer from here, do not hunt)
- **Chart appearance / theme: no tool writes it**, and the workspace document carries no theme field at all. It is an
  ACCOUNT setting — dark or light mode plus one of eight named colour themes (Kiyotaka, Percept, Seoul, Shanghai,
  Classic, Sourgum, Carbon, Quartz) — with per-chart colour overrides saved into the workspace. Send the user to the UI:
  the sun/moon toggle and the two-dot theme button in the top bar, or right-click the chart → Settings… → Main → Style
  (Background, Bullish/Bearish Candle, Bullish/Bearish Volume, Grid). Guide: openmarket.xyz/learn/charting/themes-and-appearance
- **Exchange / account connection:** Brokerage Execution (US stocks) is Alpaca OAuth; crypto execution is Wallet
  Execution on Hyperliquid with a browser-held agent key that cannot withdraw. The platform never asks for exchange API
  keys, so Binance and every other venue is a DATA source only. When the user asks whether to connect an exchange, split
  data from account, then say plainly that a trade-permission key turns order entry into one click from the chart they
  are already staring at (that is the behavioural risk, on top of holding the key) and that read-only is the ceiling.

## 6. Screening markets and building setups
Recurring ask: "scan the market and give me N tickers with a plan" (usually RR 1:2 intraday). Full recipe, thresholds
and the deliverable shape: `references/market-screening-and-plans.md`. Tools: `market_screen` for a liquid universe in
one call, `points` for candles per candidate, `metric_screen` for funding/OI across the shortlist, arithmetic in python.
Measure with `scripts/om_market_screen.py` (rate-limit aware, caches bars, prints metrics + level sheet). Finish by writing the picks into a watchlist: `watchlist_list` for the ids, and for a themed screen a dedicated list
via `watchlist_create` (name the theme; put the screen's scores/dates in `description` — it is the only place the
reasoning survives, since symbols carry no annotation) rather than burying the screen in the user's working `Hermes`
list. Then `watchlist_add_symbols` with `EXCHANGE:SYMBOL` refs and verify with `watchlist_get`.
**Resolve every ref with `symbol_resolve` before the add:** `watchlist_add_symbols` is all-or-nothing, so one ref the
directory refuses rejects the whole batch and a 7-symbol add fails entirely over one bad venue. To put the setup on the chart and draw the trade position on
it, follow `references/charting-trade-positions.md`. For live prices across a handful of held or planned symbols use one
`markets` call — `{"coins":["NEAR","HYPE"],"categories":["PERPETUAL"],"exchanges":["BINANCE_FUTURES"]}` returns
`rawSymbol` + `lastPrice` (+ `oiChange24h`) for all of them, where the same job with `points` costs one rate-limit unit per
symbol (a dashboard refreshing every minute will trip the window on `points` alone).

## Pitfalls
- `chart_read` answers from the user's LIVE tab; `chart_refresh`/`chart_status` answer from the synced workspace state.
  They can disagree for a few seconds when the user is switching symbol/interval — re-read before reporting numbers.
- `chart_symbol` / `chart_create` / `watchlist_add_symbols` validate against the symbol directory; `unknown_market`
  returns candidates instead of applying. Never retry the same pair.
- `load:` from `chart_symbol` must be `loaded` before describing the pane as showing data (`empty`/`error` are not).
- `exchange_license`: some markets' data cannot be shared with agents; drawings/indicators still work.
- Data rate on the free plan is 10 weight per 60s window (candle history 167h, Plus 364d); chart reads, screens and
  `points` all draw on it, so a batch of `points` calls trips it after roughly ten. A tripped call answers
  `{"error": "rate_limited", ...}` instead of its normal payload — a script that indexes the payload dies, so check for
  the key, log the symbol, and retry after the window (or sleep ~7s between calls).
- **The free plan's candle window (167h) is a hard wall for long timeframes, not a rate-limit problem to retry.**
  `points` with a long `lookback`, and `metric_get` on `interval: DAY` (any period), answer `tier_forbidden` carrying
  `detail.served_window_hours` and `detail.needed` — at DAY even EMA13 wants 64 daily bars, so *nothing* fits and no
  parameter unlocks it (Plus serves 364d). Never "fix" this by quietly reading a shorter interval and reporting it as
  the daily read. For daily/weekly work pull the venue's own klines, no auth and no quota: futures
  `https://fapi.binance.com/fapi/v1/klines?symbol=<SYM>&interval=1d&limit=400`, spot
  `https://api.binance.com/api/v3/klines?symbol=<SYM>&interval=1d&limit=400` — rows are
  `[openTime,o,h,l,c,volume,closeTime,quoteVolume,trades,...]` (read by index; `row[7]` is USD turnover). Feed them to
  `scripts/daily_ta.py`. Keep OpenMarket for what it does serve at HOUR: live `metric_get` positioning.
- **Every tool answers with an `{"error": ..., "message": ...}` DICT instead of raising** when it refuses, so treat any
  result as untrusted until that key is checked. A wrong parameter name (`drawingIds` where the tool wants `ids`) or a bad
  argument shape comes back as `invalid_arguments` and your next step then runs on a false assumption — a second drawing
  on the same pane, or a link the user opens to an untouched chart.
- **The symbol directory is not the exchange.** A venue can be live on the exchange and absent from the directory
  (Raydium's perp trades on Binance futures; the directory carries Raydium only as `BINANCE` spot). `symbol_resolve`
  answering candidates with `bound: null` means that exact ref will be refused — switch to a venue the directory does
  carry, verify the exchange side against its own API when the user asks why — a `status: SETTLING` on
  `/fapi/v1/exchangeInfo` means the contract is being delisted, which is the ordinary reason a perp the venue
  still lists in a ticker call is absent from the directory, and the spot ref is then the only correct one —
  and say in the reply which venue you used
  so the chart pane matches his expectation. Never compose or force the ref.
- Epoch ms on this server is scenario time, not wall-clock; do not "correct" it against `date`.
- Chart tools take the SHORT interval form (`15m`, `1h`, `1d`); the long enum (`FIFTEEN_MINUTES`) is refused there and
  belongs to the data tools (`points`, `metric_screen`). Pick the form by tool family or pay a failed round trip each.
- The free plan caps chart geometry: `chart_grid` allows 1 cell, `chart_layout` 2 panes, and the refusal names both
  numbers. For three or more tickers build one workspace per ticker with `chart_create` instead of attempting `3H`.
  Indicators are capped too — Free holds 3 per pane (`plan_limit: This chart pane holds 4 indicators, the most the Free
  plan allows on one pane (3)`), and the order-flow heatmaps (`ORDERBOOK_HEATMAP` via alias `orderbook`/`heatmap`,
  `HYPERLIQUID_LIQUIDATION_HEATMAP`, `HYPERLIQUID_TPSL_HEATMAP`) are refused outright with
  `INTERNAL: heatmap4K requires plus tier` — no settings value unlocks them, so when the user asks for a Bookmap look
  the honest answer is the paid tier (Plus $29/mo, $348/yr; batas Free vs Plus **dan add-on data CME Group yang dibeli terpisah** ada di
  `references/plans-and-market-data-addons.md`),
  or render it yourself from the free raw book feed (`points` `type=BLOCK_BOOK_SNAPSHOT_AGG`, `blockSize` required) —
  see the `bookmap-liquidity-heatmap` skill. Still free and closest to order flow: `VOLUME_FOOTPRINT` (alias
  `footprint`), `VISIBLE_RANGE_VOLUME_PROFILE`, `CUMULATIVE_VOLUME_DELTA`, `ORDERBOOK_DEPTH`. `chart_indicator_list`
  enumerates all 65 types with `placement` (onchart/offchart) and accepted aliases — call it before guessing a name.
- `chart_refresh` and `chart_status` need a LIVE session for the target workspace, which a workspace you just created
  does not have (`no live session for workspace ...`). Verify chart writes with `chart_show` / `chart_drawing_list`,
  which read the saved document with no session, and pass `workspaceId` on every `chart_*` call so the user's own
  workspace is never the one being edited.
- Result shapes are not uniform across tools, and a parser written off a dict-looking sample crashes: `market_screen`
  rows are ARRAYS (columns `rawSymbol, lastPrice, priceChange24h, volume24hUsd, oiChange24h`, where `priceChange24h` is
  a fraction, and the default `limit` is 20) while `points` returns `series[0]` with `columns` (`t,o,h,l,c,v`) and
  `rows` arrays. The `columns` come back as LONG names (`t, open, high, low, close, volume`), so a parser that zips them
  against the short `o/h/l/c/v` gets `None` for every bar — read the row POSITIONALLY (`row[1:6]` =
  open/high/low/close/volume) or map both spellings.
- `chart_screenshot` answers with an image content block (base64), not text, so a text-only bridge prints nothing:
  iterate the result content, base64-decode the block whose `type == "image"` into a PNG, and send that PNG as evidence
  after any visible chart change.
- Indicator colours you set through the connector survive a theme switch (`colorsCustomized` is sticky), so say so when
  the user worries that changing theme will wipe the lines you added.

## 7. A chart the user screenshots from ANOTHER app

Recurring ask: he sends a TradingView/Bookmap/mobile-app screenshot of one pair (often 1D) with his own EMA ribbons,
boxes and trendlines, plus a decision question — "solid long, atau nunggu turun ke mana". The screenshot is a QUESTION
with his target levels on it, not evidence: read it with `vision_analyze` for the exact axis/labels, then verify every
number against live data before answering. Workflow, deliverable shape and the standing user preferences:
`references/chart-question-answers.md`. Long-timeframe indicators: `scripts/daily_ta.py` (venue klines, stdlib only).
