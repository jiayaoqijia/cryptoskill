# Koinju API Data Tables (SQL)

All in the `api` database. **To verify any of this against the live server, run `bash ~/.claude/skills/koinju/scripts/probe-schema.sh` — it dumps every `api.*` table and its columns.** Don't trust this doc against runtime errors; the live schema is the source of truth.

Connect via `clickhouse-connect`:

```python
import os, clickhouse_connect

client = clickhouse_connect.get_client(
    host=os.environ["KOINJU_DB_HOST"],
    port=int(os.environ.get("KOINJU_DB_PORT", "8443")),
    secure=True,
    username=os.environ["KOINJU_DB_USER"],
    password=os.environ["KOINJU_DB_PASSWORD"],
    database=os.environ.get("KOINJU_DB_DATABASE", "api"),
)
```

## Gotcha: `Decimal` columns aren't JSON-serializable

Most numeric columns are `Decimal(P, S)` in ClickHouse and come back as `decimal.Decimal` objects (in object-dtype pandas columns) from `query_df()`. **These are not JSON-serializable**, so anything that goes through JSON — Plotly, FastAPI, `json.dumps`, `requests` payloads — fails with `TypeError: Object of type Decimal is not JSON serializable`.

Cast to float before passing on. A reusable helper:

```python
import decimal

def decimals_to_float(df):
    """Cast object-dtype Decimal columns to float64."""
    for col in df.columns:
        non_null = df[col].dropna()
        if len(non_null) > 0 and isinstance(non_null.iloc[0], decimal.Decimal):
            df[col] = df[col].astype(float)
    return df

df = decimals_to_float(client.query_df("..."))
```

Or explicitly per known numeric column (slightly faster, more obvious):

```python
for col in ("open", "high", "low", "close", "volume"):
    if col in df.columns:
        df[col] = df[col].astype(float)
```

The bundled scripts already do this — copy the `_decimals_to_float` pattern when writing your own.

## Gotcha: option-chain snapshots are intermittent — use `max(timestamp)`, not a fixed interval

`api.option_chains` is **snapshot-based**, not streaming. Cadence varies by exchange and by market — Deribit can be sub-minute, OKX and Bybit are often ~30 minutes between snapshots. A fixed filter like `timestamp >= now() - INTERVAL 10 MINUTE` silently drops everything for the slower venues, giving you an empty DataFrame and a confusing "smile" with no rows.

The right pattern is **per-exchange `max(timestamp)`**, bounded to a generous window (e.g. 1 DAY for the bookkeeping subquery, then a `s.timestamp = p.latest_ts` equality match):

```sql
WITH per_exchange AS (
    SELECT exchange,
           min(expiration) AS exp,
           max(timestamp)  AS latest_ts
    FROM api.option_chains
    WHERE underlying_asset = 'BTC'
      AND exchange IN ('okx', 'bybit')
      AND expiration > now()
      AND timestamp >= now() - INTERVAL 1 DAY
    GROUP BY exchange
)
SELECT s.exchange AS exchange,    -- explicit alias; see note below
       s.strike, s.mark_iv, s.option_type, s.expiration
FROM api.option_chains s
INNER JOIN per_exchange p ON s.exchange = p.exchange
WHERE s.underlying_asset = 'BTC'
  AND s.expiration = p.exp
  AND s.timestamp  = p.latest_ts
ORDER BY s.exchange, s.strike;
```

For a single exchange the pattern simplifies to a scalar subquery:

```sql
SELECT *
FROM api.option_chains
WHERE exchange = 'deribit' AND underlying_asset = 'BTC'
  AND timestamp = (
      SELECT max(timestamp) FROM api.option_chains
      WHERE exchange = 'deribit' AND underlying_asset = 'BTC'
        AND timestamp >= now() - INTERVAL 6 HOUR
  );
```

**Why the `s.exchange AS exchange` alias**: `JOIN ... ON` returns the column qualified as `s.exchange`, so downstream `GROUP BY exchange` / pandas `df["exchange"]` / Plotly `color="exchange"` all break unless you alias explicitly. (`USING (exchange)` collapses the column but is brittler in ClickHouse for the join shape we need here.)

## Gotcha: `mark_iv` is in percent, not decimal

`api.option_chains.mark_iv` (and `bid_iv` / `ask_iv`) are published as **percentage values**: `25.0` means 25%, not `0.25`. For Plotly axes use `ticksuffix="%"`, **not** `tickformat=".0%"` (which would scale by 100 and display 2500%).

```python
fig.update_yaxes(ticksuffix="%", title="implied volatility")
```

Empirically verified on OKX and Bybit. Other exchanges should follow the same convention, but if a chart's y-axis looks ~100× too high or too low, this is the first thing to check.

## `api.ohlcv` — candles (parameterized view)

**Parameter**: `candle_duration_in_minutes` (1, 5, 15, 60, 240, 1440, ...). Aggregates the raw 1m table on the fly. _Columns in the Live schema reference appendix below._

Always include a `start >=` filter to bound the scan.

```sql
SELECT *
FROM api.ohlcv(candle_duration_in_minutes = 60)
WHERE exchange = 'binance' AND market = 'BTC-USDT'
  AND start >= now() - INTERVAL 7 DAY
ORDER BY start DESC;
```

Convenience views: `api.ohlcv_1m`, `api.ohlcv_1h`. **There is no `api.ohlcv_1d`** — for daily candles use `api.ohlcv(candle_duration_in_minutes = 1440)`.

## `api.trade` — tick trades

Always filter on `timestamp >=` to bound the scan. _Columns in the Live schema reference appendix below._

```sql
SELECT exchange, market, timestamp, price, quantity, side
FROM api.trade
WHERE market LIKE 'BTC%'
  AND timestamp > toStartOfDay(now())
ORDER BY timestamp DESC
LIMIT 20;
```

## `api.funding_rate` — perpetual funding

Notes: the time column is `timestamp` (not `funding_timestamp` — old name). There is **no** `mark_price` on this table. _Columns in the Live schema reference appendix below._

```sql
SELECT exchange, market, timestamp, funding_rate
FROM api.funding_rate
WHERE market LIKE '%BTC%'
  AND timestamp >= now() - INTERVAL 7 DAY
ORDER BY timestamp DESC;
```

## `api.option_chains` — option Greeks & IV (note: plural)

Table name is `option_chains` (plural). _Full column list in the Live schema reference appendix below._ Notable columns:

- `instrument_name` — exchange-native identifier (e.g. `BTC-26MAR27-90000-P-USDT`).
- `option_type` — Enum8 `'C'` / `'P'` (single char, **not** `'call'/'put'`). Note: `api.market_option.option_type` uses the full words `CALL`/`PUT` — inconsistency between the two tables.
- `mark_iv` / `bid_iv` / `ask_iv` — implied vol (in **percent**, not decimal — see gotcha above). Use `mark_iv` for the smile.
- Greeks: `delta`, `gamma`, `vega`, `theta` — **no `rho`**.
- `index_price` / `underlying_price` — spot index vs the **per-expiry forward**. For Deribit, the forward (`underlying_price`) is the Black-76 pricing underlying, **not** spot. To recompute IV + Greeks from premiums yourself (e.g. for history older than the snapshot window), see [`option_iv_greeks.md`](option_iv_greeks.md).

There is no `market` column — filter on `underlying_asset` + `quote_asset` + `expiration` + `strike`, or use `instrument_name`.

```sql
SELECT exchange, instrument_name, strike, mark_iv, delta, gamma
FROM api.option_chains
WHERE underlying_asset = 'BTC'
  AND exchange = 'deribit'
  AND timestamp = (
      SELECT max(timestamp) FROM api.option_chains
      WHERE underlying_asset = 'BTC' AND exchange = 'deribit'
        AND timestamp >= now() - INTERVAL 6 HOUR
  )
ORDER BY expiration, strike;
```

**Per-exchange materialized views** (same columns): `api.option_chains_mv_binance`, `_bybit`, `_deribit`, `_okx`. Query these directly when you know the exchange — typically faster than the parent table.

## ~~`api.option_smile`~~ — does NOT exist

There is **no pre-aggregated `option_smile` view**. To build an IV-vs-strike smile, query `api.option_chains` directly:

```sql
WITH per_exchange AS (
    SELECT exchange,
           min(expiration) AS exp,
           max(timestamp)  AS latest_ts
    FROM api.option_chains
    WHERE underlying_asset = 'BTC' AND exchange IN ('okx', 'bybit')
      AND expiration > now()
      AND timestamp >= now() - INTERVAL 1 DAY
    GROUP BY exchange
)
SELECT s.exchange AS exchange, s.strike, s.mark_iv, s.option_type
FROM api.option_chains s
INNER JOIN per_exchange p ON s.exchange = p.exchange
WHERE s.underlying_asset = 'BTC'
  AND s.expiration = p.exp
  AND s.timestamp  = p.latest_ts
ORDER BY s.exchange, s.strike;
```

See [`scripts/plot_option_smile.py`](../scripts/plot_option_smile.py) for the runnable version.

## ~~`api.volatility_index`~~ (DVOL) — does NOT exist

There is **no `api.volatility_index` table**. DVOL is Deribit's published volatility index, not exposed by Koinju as a separate table. Workarounds:

- **Compute synthetic ATM IV** from `api.option_chains` — filter to expirations near 30 days out, take the ATM strike's `mark_iv`.
- **Fetch official DVOL** directly from Deribit's REST API (out of scope for this skill).

## Market metadata — `api.market_spot`, `api.market_future`, `api.market_option`

> **For plain "what markets exist?" listings, prefer the public REST endpoints (`/market/spot`, `/market/future`, `/market/option/active`) — no auth, no SQL setup. See [`rest.md`](rest.md). The SQL tables are useful for analytical joins (e.g. enriching `api.trade` rows with market metadata).**

_Full columns in the Live schema reference appendix._ Notes:

- Table names are `market_<class>` — **not** `<class>_markets` (an old naming).
- `market_spot` keys on `base_asset` + `quote_asset`; `market_future` and `market_option` key on `underlying_asset` + `quote_asset` (no `base_asset`).
- `market_option.option_type` uses **full words** (`CALL` / `PUT`) — inconsistent with `option_chains.option_type` which uses single chars (`C` / `P`). Both tables, same concept, different encoding.
- `expiration` is nullable on futures (perps have no expiration) and required on options.

Example — BTC spot pairs:

```sql
SELECT exchange, market_symbol
FROM api.market_spot
WHERE base_asset = 'BTC' OR quote_asset = 'BTC';
```

## `api.koinju_market_name_lookup`

Internal symbol-mapping dictionary (keyed by `(exchange, websocket_name, :SPOT|:FUTURE|:OPTION)`). Rarely queried directly — the user-facing `api.*` tables already resolve canonical names through it.

## Coverage

Live exchange coverage: `SELECT DISTINCT exchange FROM api.trade WHERE timestamp > now() - INTERVAL 1 HOUR`.

25+ exchanges historically supported. Use the query above for ground truth on what's currently live.

## Live schema reference (autogenerated)

The handwritten table sections above cover usage and gotchas. The block below is a complete column-level reference for every public `api.*` table, regenerated from live `DESCRIBE` by `koinju skill build-schemas`. If the live server adds or renames a column, this is where you see it first.

<!-- AUTOGEN START: schemas -->

_Generated from `clickhouse/tables/api/**/*.sql` — 13 public objects. Run `koinju skill build-schemas` to refresh._

#### `api.funding_rate`
_Type: `VIEW` (`clickhouse/tables/api/views/funding_rate.sql`)._

Columns (from SELECT aliases): `exchange`, `contract_type`, `market`, `timestamp`, `funding_rate`

_Types not declared in view DDL. For exact types run `DESCRIBE (SELECT * FROM api.funding_rate LIMIT 0)` — add the parameter for parameterized views, e.g. `api.ohlcv(candle_duration_in_minutes = 1440)` — or `bash scripts/probe-schema.sh funding_rate`._

#### `api.market_future`
_Type: `VIEW` (`clickhouse/tables/api/views/market.sql`)._

Columns (from SELECT aliases): `exchange`, `market_symbol`, `underlying_asset`, `quote_asset`, `settling_asset`, `denomination_asset`, `expiration`, `contract_size`, `contract_type`, `future_type`, `exchange_specific_symbol`

_Types not declared in view DDL. For exact types run `DESCRIBE (SELECT * FROM api.market_future LIMIT 0)` — add the parameter for parameterized views, e.g. `api.ohlcv(candle_duration_in_minutes = 1440)` — or `bash scripts/probe-schema.sh market_future`._

#### `api.market_option`
_Type: `VIEW` (`clickhouse/tables/api/views/market.sql`)._

Columns (from SELECT aliases): `exchange`, `market_symbol`, `underlying_asset`, `quote_asset`, `settling_asset`, `expiration`, `strike`, `contract_size`, `contract_type`, `option_type`, `exchange_specific_symbol`

_Types not declared in view DDL. For exact types run `DESCRIBE (SELECT * FROM api.market_option LIMIT 0)` — add the parameter for parameterized views, e.g. `api.ohlcv(candle_duration_in_minutes = 1440)` — or `bash scripts/probe-schema.sh market_option`._

#### `api.market_spot`
_Type: `VIEW` (`clickhouse/tables/api/views/market.sql`)._

Columns (from SELECT aliases): `exchange`, `market_symbol`, `base_asset`, `quote_asset`, `exchange_specific_symbol`

_Types not declared in view DDL. For exact types run `DESCRIBE (SELECT * FROM api.market_spot LIMIT 0)` — add the parameter for parameterized views, e.g. `api.ohlcv(candle_duration_in_minutes = 1440)` — or `bash scripts/probe-schema.sh market_spot`._

#### `api.ohlcv`
_Type: `VIEW` (`clickhouse/tables/api/views/ohlcv.sql`)._

Columns (from SELECT aliases): `start`, `end`, `exchange`, `market`, `open`, `high`, `low`, `close`, `volume`, `count`, `duration_minutes`

_Types not declared in view DDL. For exact types run `DESCRIBE (SELECT * FROM api.ohlcv LIMIT 0)` — add the parameter for parameterized views, e.g. `api.ohlcv(candle_duration_in_minutes = 1440)` — or `bash scripts/probe-schema.sh ohlcv`._

#### `api.ohlcv_1h`
_Type: `VIEW` (`clickhouse/tables/api/views/ohlcv.sql`)._

Columns (from SELECT aliases): `start`, `end`, `exchange`, `market`, `open`, `high`, `low`, `close`, `volume`, `count`, `duration_minutes`

_Types not declared in view DDL. For exact types run `DESCRIBE (SELECT * FROM api.ohlcv_1h LIMIT 0)` — add the parameter for parameterized views, e.g. `api.ohlcv(candle_duration_in_minutes = 1440)` — or `bash scripts/probe-schema.sh ohlcv_1h`._

#### `api.ohlcv_1m`
_Type: `VIEW` (`clickhouse/tables/api/views/ohlcv.sql`)._

Columns (from SELECT aliases): `start`, `end`, `exchange`, `market`, `open`, `high`, `low`, `close`, `volume`, `count`, `duration_minutes`

_Types not declared in view DDL. For exact types run `DESCRIBE (SELECT * FROM api.ohlcv_1m LIMIT 0)` — add the parameter for parameterized views, e.g. `api.ohlcv(candle_duration_in_minutes = 1440)` — or `bash scripts/probe-schema.sh ohlcv_1m`._

#### `api.option_chains`
_Type: `TABLE` (`clickhouse/tables/api/option_chains.sql`)._

| Column | Type |
|---|---|
| `exchange` | `LowCardinality(String)` |
| `timestamp` | `DateTime64(9, 'UTC')` |
| `instrument_name` | `String` |
| `underlying_asset` | `LowCardinality(String)` |
| `quote_asset` | `LowCardinality(String)` |
| `expiration` | `DateTime64(9, 'UTC')` |
| `strike` | `Decimal(38, 18)` |
| `option_type` | `Enum8('C' = 1, 'P' = 2)` |
| `bid_price` | `Decimal(38, 18)` |
| `ask_price` | `Decimal(38, 18)` |
| `last_price` | `Decimal(38, 18)` |
| `mark_price` | `Decimal(38, 18)` |
| `index_price` | `Decimal(38, 18)` |
| `underlying_price` | `Decimal(38, 18)` |
| `mark_iv` | `Decimal(38, 18)` |
| `bid_iv` | `Decimal(38, 18)` |
| `ask_iv` | `Decimal(38, 18)` |
| `delta` | `Decimal(38, 18)` |
| `gamma` | `Decimal(38, 18)` |
| `vega` | `Decimal(38, 18)` |
| `theta` | `Decimal(38, 18)` |
| `open_interest` | `Decimal(38, 18)` |
| `volume_24h` | `Decimal(38, 18)` |
| `state` | `LowCardinality(String)` |
| `meta` | `String` |

#### `api.option_chains_mv_binance`
_Type: `MATERIALIZED VIEW` (`clickhouse/tables/api/option_chains_mv.sql`)._

Columns (from SELECT aliases): `exchange`, `timestamp`, `instrument_name`, `underlying_asset`, `quote_asset`, `expiration`, `strike`, `option_type`, `bid_price`, `ask_price`, `last_price`, `mark_price`, `index_price`, `underlying_price`, `mark_iv`, `bid_iv`, `ask_iv`, `delta`, `gamma`, `vega`, `theta`, `open_interest`, `volume_24h`, `state`, `meta`

_Types not declared in view DDL. For exact types run `DESCRIBE (SELECT * FROM api.option_chains_mv_binance LIMIT 0)` — add the parameter for parameterized views, e.g. `api.ohlcv(candle_duration_in_minutes = 1440)` — or `bash scripts/probe-schema.sh option_chains_mv_binance`._

#### `api.option_chains_mv_bybit`
_Type: `MATERIALIZED VIEW` (`clickhouse/tables/api/option_chains_mv.sql`)._

Columns (from SELECT aliases): `exchange`, `timestamp`, `instrument_name`, `underlying_asset`, `quote_asset`, `expiration`, `strike`, `option_type`, `bid_price`, `ask_price`, `last_price`, `mark_price`, `index_price`, `underlying_price`, `mark_iv`, `bid_iv`, `ask_iv`, `delta`, `gamma`, `vega`, `theta`, `open_interest`, `volume_24h`, `state`, `meta`

_Types not declared in view DDL. For exact types run `DESCRIBE (SELECT * FROM api.option_chains_mv_bybit LIMIT 0)` — add the parameter for parameterized views, e.g. `api.ohlcv(candle_duration_in_minutes = 1440)` — or `bash scripts/probe-schema.sh option_chains_mv_bybit`._

#### `api.option_chains_mv_deribit`
_Type: `MATERIALIZED VIEW` (`clickhouse/tables/api/option_chains_mv.sql`)._

Columns (from SELECT aliases): `exchange`, `timestamp`, `instrument_name`, `underlying_asset`, `quote_asset`, `expiration`, `strike`, `option_type`, `bid_price`, `ask_price`, `last_price`, `mark_price`, `index_price`, `underlying_price`, `mark_iv`, `bid_iv`, `ask_iv`, `delta`, `gamma`, `vega`, `theta`, `open_interest`, `volume_24h`, `state`, `meta`

_Types not declared in view DDL. For exact types run `DESCRIBE (SELECT * FROM api.option_chains_mv_deribit LIMIT 0)` — add the parameter for parameterized views, e.g. `api.ohlcv(candle_duration_in_minutes = 1440)` — or `bash scripts/probe-schema.sh option_chains_mv_deribit`._

#### `api.option_chains_mv_okx`
_Type: `MATERIALIZED VIEW` (`clickhouse/tables/api/option_chains_mv.sql`)._

Columns (from SELECT aliases): `exchange`, `timestamp`, `instrument_name`, `underlying_asset`, `quote_asset`, `expiration`, `strike`, `option_type`, `bid_price`, `ask_price`, `last_price`, `mark_price`, `index_price`, `underlying_price`, `mark_iv`, `bid_iv`, `ask_iv`, `delta`, `gamma`, `vega`, `theta`, `open_interest`, `volume_24h`, `state`, `meta`

_Types not declared in view DDL. For exact types run `DESCRIBE (SELECT * FROM api.option_chains_mv_okx LIMIT 0)` — add the parameter for parameterized views, e.g. `api.ohlcv(candle_duration_in_minutes = 1440)` — or `bash scripts/probe-schema.sh option_chains_mv_okx`._

#### `api.trade`
_Type: `VIEW` (`clickhouse/tables/api/views/trade.sql`)._

Columns (from SELECT aliases): `exchange`, `market`, `side`, `quantity`, `price`, `timestamp`, `trade_id`

_Types not declared in view DDL. For exact types run `DESCRIBE (SELECT * FROM api.trade LIMIT 0)` — add the parameter for parameterized views, e.g. `api.ohlcv(candle_duration_in_minutes = 1440)` — or `bash scripts/probe-schema.sh trade`._

<!-- AUTOGEN END: schemas -->

