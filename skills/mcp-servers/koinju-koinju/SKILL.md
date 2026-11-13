---
name: koinju
description: >-
  Use this skill for any query mentioning Koinju (koinju.io, api.koinju.io,
  docs.koinju.io, mcp koinju) — getting credentials, connecting, querying, integrating, or
  optimizing the Koinju API. Also use when the user wants crypto market data
  without naming Koinju: historical OHLCV/candles, tick trades, funding rates,
  option chains, implied volatility, vol smile, IV surface, DVOL — across
  13 exchanges, among them Binance, Bybit, OKX, Deribit, Coinbase and Kraken. Covers
  backtesting strategies on crypto price history, quant research, and
  enriching existing ClickHouse/Postgres/Redis stores with crypto data. Do
  NOT use for stock/equity markets or for general ClickHouse architecture
  questions unrelated to Koinju.
metadata:
  author: Dmitry Prokofyev
  version: "0.9.4"
  homepage: https://docs.koinju.io
---

# Koinju API Skill

Help users discover, query, and integrate Koinju's multi-exchange crypto market data into research, backtesting, or production pipelines.

## Quick start (fast-path)

Most "test the API" sessions need only this. Read the Workflow below for nuance.

- **Set up a project**: `bash ~/.claude/skills/koinju/scripts/setup.sh [target-dir]` — auto-detects cwd-empty / uv / venv, scaffolds + installs deps + seeds `main.py` and `.koinju.env`, idempotent. Without `[target-dir]`: cwd if empty (ignoring `.git`), else `./koinju-demo/`.
- **Probe state**: `bash ~/.claude/skills/koinju/scripts/probe-env.sh` — one line like `uv:ok pyproject:found venv:active deps:ok creds:ok project_env:found home_env:found suggest_save_global:no`. Use this before deciding to bootstrap, instead of running 4 separate `command -v` / `python -c import` / `[ -n $VAR ]` probes. If the trailing token is `suggest_save_global:yes` (project `.koinju.env` populated, but no `~/.koinju.env`), propose copying — see [Workflow step 5](#workflow).
- **Verify schema**: `bash ~/.claude/skills/koinju/scripts/probe-schema.sh [table]` — dumps live `api.*` tables and columns. Run before writing SQL against any table you haven't used this session. Note: `DESCRIBE` (what it uses) returns empty for parameterized views like `api.ohlcv` — that's "parameterized view", not "missing"; the script falls back to `SHOW CREATE` and prints the `{param:Type}` signature.
- **Get credentials**: https://koinju.io/pricing → sign up → check email for the dataroom link. The credential template lives at `references/koinju.env.example` (the bootstrap copies it).
- **No credentials**: the free demo database holds one validated UTC day, 18 October 2026 (`2026-10-18`), and needs none (host `sn7u7x3woz.eu-central-1.aws.clickhouse.cloud`, port 8443, user `demo`, empty password, database `api`). See `references/auth.md`; docs: https://docs.koinju.io/free-demo-database
- **Public REST** (no auth — market / product / instrument discovery): `curl -s 'https://api.koinju.io/market/spot' | jq '[.[] | select(.base == "BTC")]'`. See `references/rest.md`.
- **MCP server** : `claude mcp add --transport http koinju https://mcp.koinju.io/mcp`, then `/mcp` to sign in with the Koinju account (no API key in the config), gives nine read-only tools. Seven sit over the REST endpoints — `get_ohlcv`, `get_trades`, `get_funding_rate`, `get_volatility_index`, `get_option_chain`, `get_option_smile`, `get_option_matrix` — spending the account's own API key and REST quota. `find_markets` reads the public market lists with no key, so it spends no quota: call it first, it returns the exact `exchange` and `market_symbol` the data tools want. `run_sql` runs one ClickHouse statement with the account's own SQL login, so the same tables, time limit and daily quota as direct SQL; an answer over 100,000 characters is refused, not cut. Bulk history belongs in SQL. Docs: https://docs.koinju.io/mcp-server
- **Migration**: legacy `KOINJU_HOST` / `KOINJU_USER` / `KOINJU_PASSWORD` → current `KOINJU_DB_HOST` / `KOINJU_DB_USER` / `KOINJU_DB_PASSWORD` (and `KOINJU_API_KEY` is new). See [Migration](#migration-legacy-env-var-names) below for the one-liner.

## Workflow

1. **Capture intent.** Identify the data class the user needs:
   - candles / OHLCV / historical price → `api.ohlcv` (parameterized), `api.ohlcv_1m`, `api.ohlcv_1h` (no `_1d` view)
   - tick trades → `api.trade`
   - funding rates (perpetual) → `api.funding_rate` (time column is `timestamp`, not `funding_timestamp`)
   - option chain / Greeks / IV / smile / DVOL → all via `api.option_chains` (**plural**; there's no `api.option_smile` or `api.volatility_index`)
   - exchange or market coverage → `api.market_spot` / `_future` / `_option` (or REST `/market/*`)

   **Before writing any SQL against a table you haven't queried this session, run `bash ~/.claude/skills/koinju/scripts/probe-schema.sh [table]` to verify columns.** The bundled refs drift; the live schema is the source of truth — but mind the lens: `probe-schema.sh` uses `DESCRIBE`, which returns **empty for parameterized views like `api.ohlcv`**. An empty or error probe means "parameterized view", **not** "table is gone." Confirm with `SHOW CREATE TABLE api.ohlcv`, a `DESCRIBE (SELECT * FROM api.ohlcv(candle_duration_in_minutes = 1440) LIMIT 0)`, or just run the SELECT. (The bundled `probe-schema.sh` already does the `SHOW CREATE` fallback and prints the `{param:Type}` signature for you.)

2. **Choose interface.**
   - **Public REST `/market/*`** — **always use this for any market / product / instrument discovery question** ("what BTC pairs / futures / options exist?", "which exchanges list X?", "list all spot pairs"). No auth, no Python deps, just `curl` + `jq`. Don't fall back to SQL for plain listings. See `references/rest.md`.
   - **Authenticated REST** (`/ohlcv`, `/trade`, `/funding-rate`, `/volatility-index`, `/stats`) — small data pulls, simple HTTP, supports free tier; needs `x-api-key`.
   - **ClickHouse SQL** via `clickhouse-connect` (Python), `clickhouse-rs` (Rust), `clickhouse-go` (Go), or BI tools — heavy analytics, joins, custom aggregations, parameterized candle durations; needs host + username + password.

3. **Auth check.** The bundled scripts and `load_koinju_credentials()` **auto-source `.koinju.env` (project-local, in cwd) then `~/.koinju.env` (global)** — project-local wins per-var; existing env vars still win over both. A user running scripts from inside `koinju-demo/` (with a populated project `.koinju.env`) gets their credentials picked up automatically. When writing ad-hoc Python, copy the `_autosource_koinju_env()` helper from `references/auth.md`. From a shell, source both explicitly:

   ```bash
   [ -f .koinju.env ] && source .koinju.env
   [ -f ~/.koinju.env ] && source ~/.koinju.env
   : "${KOINJU_API_KEY:?}" "${KOINJU_DB_HOST:?}" "${KOINJU_DB_USER:?}" "${KOINJU_DB_PASSWORD:?}"
   ```

   `KOINJU_DB_PORT` (default `8443`) and `KOINJU_DB_DATABASE` (default `api`) are optional.

   If any required var is missing: the cleanest response is to propose the **Project setup
   & dependency bootstrap** flow below — it scaffolds the project, creates a `.koinju.env`
   (project-local, auto-loaded by the scripts), and walks through getting credentials in
   one motion (and bundles dep install too, in case `clickhouse_connect` is also missing).
   **No credentials, and a task that one day of data answers?** Use the free demo database: see `references/auth.md`.
   For the credential-acquisition steps alone:
   **Don't yet have them?** Pick a plan at **https://koinju.io/pricing** — after sign-up
   Koinju emails you a link to **https://dataroom.koinju.io/** where the REST key and
   ClickHouse host / user / password live. **Already signed up but no email / can't access
   the dataroom?** Fall back to **support@koinju.io**. Then have them `export` the
   variables in their shell profile (or a sourced `~/.koinju.env` with `chmod 600`). See
   `references/auth.md` for full details.

4. **Write the query.** Reach for the right reference:
   - **Market / product / instrument discovery** ("what BTC pairs exist?", "which options are listed?") → public `/market/*` endpoints in [`references/rest.md`](references/rest.md). No auth, no SQL. Never reach for `api.spot_markets` / `api.future_markets` / `api.option_markets` for a plain listing.
   - [`references/data-tables.md`](references/data-tables.md) — table schemas, latest-value patterns (analytics, not discovery)
   - [`references/optimization.md`](references/optimization.md) — query perf for trade / year-long ohlcv
   - [`references/backtesting.md`](references/backtesting.md) — strategy vs buy-and-hold workflow
   - [`references/plotting.md`](references/plotting.md) — option smile, vol surface, candlestick, DVOL, equity curve
   - [`references/option_iv_greeks.md`](references/option_iv_greeks.md) — recompute Deribit option IV + Greeks (Black-76 on the forward) from premiums; verified against `mark_iv` / chain Greeks; deep history via the `deribit-option` / `deribit-future` trade tapes
   - [`references/integrations.md`](references/integrations.md) — Postgres / ClickHouse / Redis plug-in patterns
   - [`references/rest.md`](references/rest.md) — REST endpoints (discovery + authed quick lookups). Autogenerated endpoint catalog at the bottom is the canonical reference for paths / params / return shapes.
   - [`references/recipes/`](references/recipes/) — 11 CI-validated cookbook recipes (Bollinger, Sortino, max drawdown, mean-reversion z-score, historical volatility, DCA vs lump-sum, perp funding, spot/perp spreads, cross-exchange arbitrage, OHLCV streaming, correlation). **Reach here before reinventing a metric** — each pairs the Python implementation with the SQL equivalent and a parity test.

5. **Execute & verify.** Run the query, validate the result shape, return to user.

   **Default rendering: markdown tables.** When the result fits on screen (roughly ≤ 50 rows × ≤ 8 columns, no cell wider than ~40 chars), render it as a markdown table in your response — Claude Code renders these natively and they're the most scannable format. For DataFrames: `print(df.to_markdown(index=False))` (needs `tabulate` — bundled in the project-setup deps). For REST / `jq` output: wrap in pandas first, or align text columns with `column -t -s$'\t'`. For single scalars ("current BTC volatility → 47.3%"), state the value in prose with context, not a 1×1 table.

   **Too large for a table:** don't dump. Show head/tail with a `... (N more rows)` indicator, summarize with counts/aggregations, or save the full result to a file (`df.to_csv("out.csv")`, `df.to_parquet("out.parquet")`) and tell the user the path.

   **After the first successful run in a project**, run `bash ~/.claude/skills/koinju/scripts/probe-env.sh` and check the trailing token. If it ends in `suggest_save_global:yes` (project `.koinju.env` populated and working, no `~/.koinju.env`), propose:

   > "Your project `.koinju.env` works. Want me to copy it to `~/.koinju.env` so future Claude sessions in other projects pick up the same credentials automatically?"

   On yes: `cp .koinju.env ~/.koinju.env && chmod 600 ~/.koinju.env`. On no: drop it; don't ask again in the same session. The bundled helpers auto-source both files (project wins per-var), so the global copy doesn't conflict with future per-project overrides.

## Project setup & dependency bootstrap

**Default: run `bash ~/.claude/skills/koinju/scripts/setup.sh [target-dir]`.** It probes cwd (empty → in-place, else `./koinju-demo/`), probes `uv`, runs `uv init` (or `python3 -m venv` fallback), installs `clickhouse-connect pandas plotly tabulate`, seeds `main.py` from the welcome script, creates `.koinju.env` from the bundled template (chmod 600), appends to `.gitignore`, prints the credential URL and run command. Idempotent.

**Two triggers, same script:**

- **Proactive** — user asks "set up a python project for koinju", "scaffold a koinju starter", "create a project to call the API", etc. Just run `setup.sh`; this IS the proposal.
- **Reactive** — a SQL task fails with `ModuleNotFoundError` and/or `KOINJU_*` env vars are unset. **Stop**. Do NOT `pip install` in the current shell. Do NOT hunt for an alternative Python (`/usr/bin/python3`, `python3.10`, ...) — that "works" by accident and confuses the user about which env runs their code. Don't fix one blocker and leave the other.

  1. Probe with `bash ~/.claude/skills/koinju/scripts/probe-env.sh` — one line tells you uv / venv / deps / creds / env-file state.
  2. Propose: *"[Deps / credentials / both] aren't set up — I can scaffold a clean uv project at `./koinju-demo/` that handles it: installs deps, creates a `.koinju.env` (auto-loaded by the scripts), points you at koinju.io/pricing for credentials. OK?"*
  3. If accepted → `setup.sh`. If declined → **print the code you would have run as a fenced block** plus a `koinju.io/pricing` pointer if creds were the missing piece.

For manual bootstrap (no script access, custom requirements, debugging), see [`references/bootstrap.md`](references/bootstrap.md) — full templates, variations (existing project, plotting starter), and the don'ts.

## Migration: legacy env-var names

A project using `KOINJU_HOST` / `KOINJU_USER` / `KOINJU_PASSWORD` (and no `KOINJU_API_KEY`) is on the **old** naming. Current names:

| Legacy | Current |
|---|---|
| `KOINJU_HOST` | `KOINJU_DB_HOST` |
| `KOINJU_USER` | `KOINJU_DB_USER` |
| `KOINJU_PASSWORD` | `KOINJU_DB_PASSWORD` |
| *(none)* | `KOINJU_API_KEY` *(new — required by REST endpoints and the unified `load_koinju_credentials()` helper)* |

Also: rename the file from `.env` / `.env.example` to `.koinju.env` (project-local) or `~/.koinju.env` (global), then `chmod 600`. The bundled scripts and `_autosource_koinju_env()` only look at `.koinju.env` — they don't auto-source `.env`.

One-liner to migrate an existing `.env`:

```bash
sed \
  -e 's/^export KOINJU_HOST=/export KOINJU_DB_HOST=/' \
  -e 's/^export KOINJU_USER=/export KOINJU_DB_USER=/' \
  -e 's/^export KOINJU_PASSWORD=/export KOINJU_DB_PASSWORD=/' \
  .env > .koinju.env \
  && rm .env \
  && chmod 600 .koinju.env \
  && { grep -qxF '.koinju.env' .gitignore 2>/dev/null || echo '.koinju.env' >> .gitignore; }
```

(Stream-rewrite form rather than `sed -i` — portable across GNU and BSD `sed` without the `-i ''` macOS quirk.)

Then have the user add `export KOINJU_API_KEY=...` to `.koinju.env` (grab the REST key from `dataroom.koinju.io`).

**Format reminder for `KOINJU_DB_HOST`**: bare hostname only (e.g. `abc123.koinju.io`). Strip any `https://` scheme, trailing `:8443` port, or trailing `/` if the user copy/pasted the full dataroom URL — `clickhouse-connect` adds the scheme and port itself, and port is set via `KOINJU_DB_PORT` (default 8443).

## Bundled resources

- [`references/auth.md`](references/auth.md) — credential setup (`KOINJU_*` env vars, dataroom URL, support email, Python helper)
- [`references/data-tables.md`](references/data-tables.md) — gotchas (`Decimal`, snapshot cadence, `mark_iv` in percent), per-table notes (`api.ohlcv`, `api.trade`, `api.funding_rate`, `api.option_chains`, `api.market_*`), and an autogenerated full-schema reference appendix regenerated from live `DESCRIBE`
- [`references/optimization.md`](references/optimization.md) — query optimization rules for koinju tables + a worked LINK-USDT example
- [`references/backtesting.md`](references/backtesting.md) — strategy vs buy-and-hold workflow, metrics, common pitfalls
- [`references/plotting.md`](references/plotting.md) — Plotly recipes for option smile, vol surface, candlestick, DVOL, equity curves
- [`references/option_iv_greeks.md`](references/option_iv_greeks.md) — recompute Deribit option IV + Greeks with Black-76 on the forward (`underlying_price`, not spot); one-query SQL solver (`erf` + `arrayFold`) verified against the chain; deep history from the `deribit-option` / `deribit-future` trade tapes
- [`references/integrations.md`](references/integrations.md) — Postgres / ClickHouse (`remoteSecure()`, ETL) / Redis caching patterns
- [`references/rest.md`](references/rest.md) — discovery rule, BTC-product `jq` cookbook, per-tier rate limits, Python example, REST-vs-SQL decision — and an autogenerated endpoint catalog regenerated from `api/market-data.yaml`
- [`references/recipes/`](references/recipes/) — 11 CI-validated cookbook articles (Bollinger, Sortino, max drawdown, mean-reversion z-score, historical vol, DCA vs lump-sum, perp funding, spot/perp spreads, cross-exchange arbitrage, OHLCV streaming, correlation), each with a Python implementation, SQL equivalent, and parity test. Synced from `api/python_vs_sql/`.
- [`references/bootstrap.md`](references/bootstrap.md) — fallback when `clickhouse_connect` is missing: propose a uv project (or print the code if declined); explicit "don't pip install / don't hunt alternative Pythons" guidance
- [`references/koinju.env.example`](references/koinju.env.example) — credential template (the bootstrap `cp`s this to `.koinju.env` and chmod 600s it)
- [`scripts/setup.sh`](scripts/setup.sh) — one-shot bootstrap: cwd-probe, uv-or-venv, install deps, seed `main.py` + `.koinju.env` + `.gitignore`. Pass target dir as `$1`. Idempotent.
- [`scripts/probe-env.sh`](scripts/probe-env.sh) — one-line state probe (`uv:ok pyproject:found venv:active deps:ok creds:ok ...`). Single tool call instead of multiple `command -v` / `python -c import` / `[ -n $VAR ]` invocations.
- [`scripts/probe-schema.sh`](scripts/probe-schema.sh) — dumps live `api.*` tables + columns over the ClickHouse HTTPS interface. Run before writing SQL against an unfamiliar table; **live schema is the source of truth, not the bundled refs**.
- [`scripts/welcome_btc_usdt.py`](scripts/welcome_btc_usdt.py) — runnable demo: 7d of BTC-USDT 1h candles via ClickHouse, Plotly candlestick (used as the seed `main.py` by `setup.sh`)
- [`scripts/plot_option_smile.py`](scripts/plot_option_smile.py) — runnable: BTC option smile across two exchanges at the nearest expiration
- [`scripts/backtest_buy_and_hold.py`](scripts/backtest_buy_and_hold.py) — runnable: SMA(20/50) vs buy-and-hold on any market, reports total return / Sharpe / max drawdown

Deeper SQL recipes ship inside the skill at [`references/recipes/`](references/recipes/). The corresponding GitBook pages live at https://docs.koinju.io/sql-cookbook/.

> **Source of truth:** https://docs.koinju.io. Always prefer the live docs if there's a conflict with bundled references.