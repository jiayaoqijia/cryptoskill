# Ohlcv Streaming

<!-- Synced from `api/python_vs_sql/ohlcv_streaming/` by `koinju skill sync-recipes`. Edit the source, not this file. -->

## Source article

# OHLCV streaming download (ShrimpyApp / CCXT OHLCV)

- **Article**: https://medium.com/coinmonks/python-scripts-for-ccxt-crypto-candlestick-ohlcv-charting-data-83926fa16a13

## What's different about this page

Unlike the other Compute Engine pages — which show a SQL query that
*replaces* a chunk of pandas — this page shows a SQL query **wrapped
in Python** to download a multi-million-row OHLCV history straight to
a Parquet file. The point isn't a clever aggregate; it's that pulling
"every 1-minute BTC-USDT candle on 4 exchanges for a calendar year"
is a 20-line Python helper rather than a paginated CCXT loop with
retries, rate-limiters, and a hopeful `.to_parquet()` that may or may
not OOM.

## What we compute

A simple multi-exchange OHLCV pull — no aggregation, no analytics —
designed to produce a row count well above what `client.query_df()`
would comfortably load into a pandas DataFrame:

- 1-minute candles
- `BTC-USDT` on `binance`, `okx`, `kucoin`, `gateio`
- 1 calendar year (2024)
- ~525,600 minutes × 4 exchanges ≈ **~2 million rows**

The Python helper (`download.py`) wraps this query and streams the
result directly to a Parquet file using clickhouse-connect's
`raw_stream(... fmt='Parquet')`. The server emits Parquet; the
client copies bytes to a file. **Bounded RAM** regardless of result
size — driven by HTTP chunk size, not row count.

## Why streaming over `query_df()`

`client.query_df()` materialises the entire result set into a pandas
DataFrame in process memory. For a few thousand rows that's fine; for
two million it's ~500 MB of pandas overhead even after Decimal →
Float coercion. Larger pulls (multi-year, multi-asset) silently OOM
notebooks.

`client.raw_stream(query, fmt='Parquet')` returns an iterator of HTTP
chunks. The server materialises rows on its side, encodes them as
Parquet (column-chunked, via ClickHouse's streaming format pipeline),
and ships them in chunked-transfer-encoded bytes. The client never
sees more than one chunk at a time.

## Why Parquet (and not CSV)

The first version of this page used `CSVWithNames`. Same December
window benchmark on the koinju cluster:

| format         |   size   | wall time |
| -------------- | -------- | --------- |
| `Parquet`      | ~5.4 MB  |   ~5.3 s  |
| `CSVWithNames` | ~17.4 MB |   ~7.4 s  |

Parquet is ~3× smaller on disk and ~30 % faster end-to-end. It's also
typed (no string-to-float reparsing on load), self-describing, and
the standard archival format for tabular tick / candle data. Use
CSV only when downstream tooling can't read Parquet.

## What we drop from the article

The article's CCXT script does pagination, rate-limiting, retry on
transient errors, response normalisation, and matplotlib charting. We
keep just the **download** — that's the part that benefits from a
single SQL pull. Charting is a downstream concern: once the Parquet
is on disk, point any plotting library at it.

## Test design

This page intentionally **does not** have a parity test. There's no
pandas-equivalent that would round-trip the same dataset (the whole
point is that loading-it-all-into-pandas is what we're avoiding).

The smoke test exercises a **tiny window** — 1 day × 1 exchange,
~1,440 rows — and asserts:

1. The streaming helper writes a non-empty Parquet file.
2. The file's row count (read back via pyarrow) matches a separate
   `SELECT count(*)` run for the same window.
3. The Parquet schema matches the expected column list.

This verifies the script is **operational** without burning quota
downloading millions of rows on every CI run. Users wanting to verify
the streaming behaviour at scale should run `download.py` directly
against a wide window — quota and disk willing.

# OHLCV streaming download — Python wrapper

**Source article**: [ShrimpyApp — Python Scripts for CCXT Crypto Candlestick OHLCV Charting Data](https://medium.com/coinmonks/python-scripts-for-ccxt-crypto-candlestick-ohlcv-charting-data-83926fa16a13)
**Published doc**: [`sql-cookbook/ohlcv-streaming`](https://docs.koinju.io/sql-cookbook/ohlcv-streaming)

## Why this page is different

Other Compute Engine pages show a SQL query that *replaces* pandas.
This one is the opposite — a small Python wrapper around a trivially
simple SQL query, designed to **download more candle data than fits
in RAM** straight to a Parquet file.

The article's CCXT script does pagination, rate-limit handling, retry,
response normalisation and matplotlib charting. We keep just the
*download* — the part that actually benefits from streaming.

## Files

- `query.sql` — the multi-exchange OHLCV pull (the one rendered in the
  doc page).
- `download.py` — the streaming wrapper using `clickhouse-connect`'s
  `raw_stream(... fmt='Parquet')`.
- `test_ohlcv_streaming.py` — smoke test on a tiny window (1 day × 1
  exchange, ~1,440 rows). No parity test (no pandas-equivalent that
  round-trips the same dataset; the whole point is bounded RAM).

## Running the smoke test

```bash
uv run pytest api/python_vs_sql/ohlcv_streaming/ -m parity
```

Test loads `KOINJU_SQL_USER` / `KOINJU_SQL_PASSWORD` from `.env` via
`dotenv.load_dotenv()`. Asserts: file is written and non-empty,
Parquet schema matches the expected column list, row count matches a
separate `count(*)` for the same window.

## Downloading a real dataset

```bash
uv run python -c "
from pathlib import Path
import clickhouse_connect, os, dotenv; dotenv.load_dotenv()
from api.python_vs_sql.ohlcv_streaming.download import build_query, download_to_parquet
c = clickhouse_connect.get_client(
    host='<provided_database_url>', port=8443, secure=True,
    username=os.environ['KOINJU_SQL_USER'], password=os.environ['KOINJU_SQL_PASSWORD'],
    database='public_data')
nbytes = download_to_parquet(
    c,
    build_query(['binance','okx','kucoin','gateio'], 'BTC-USDT', '2024-01-01', '2024-12-31'),
    Path('btc_ohlcv_2024.parquet'))
print(f'{nbytes/1e6:.1f} MB written')
"
```

For a year of 1-minute BTC-USDT × 4 exchanges, expect ~65 MB / ~2 M
rows / ~65 s with Parquet (vs ~210 MB / ~90 s as CSV).

## ClickHouse SQL

```sql
SELECT start, exchange, market,
       toFloat64(open)   AS open,
       toFloat64(high)   AS high,
       toFloat64(low)    AS low,
       toFloat64(close)  AS close,
       toFloat64(volume) AS volume
FROM api.ohlcv(candle_duration_in_minutes = 1)
WHERE market = 'BTC-USDT'
  AND exchange IN ('binance', 'okx', 'kucoin', 'gateio')
  AND start >= toDateTime('2024-01-01')
  AND start <  toDateTime('2024-12-31') + INTERVAL 1 DAY
ORDER BY exchange, start
```
