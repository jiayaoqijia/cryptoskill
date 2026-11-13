# Integrating Koinju with your stack

Three rough shapes:
- **Federate** — leave Koinju where it is, query it from your DB or app on demand.
- **ETL** — copy slices of Koinju data into your DB on a schedule.
- **Cache** — keep only the latest values close to your trading loop.

Pick by latency tolerance: federation is freshest but per-query slow; ETL is cheap to query but stale; cache is fastest but narrow.

## Postgres

### A) Pull-side join in Python (lightweight, ad-hoc)

```python
import os, pandas as pd, psycopg2, clickhouse_connect

pg = psycopg2.connect(host="...", dbname="...", user="...", password="...")
your_df = pd.read_sql(
    "SELECT ts, market, signal FROM trades WHERE ts >= now() - interval '7 days'",
    pg,
)

ch = clickhouse_connect.get_client(
    host=os.environ["KOINJU_DB_HOST"], port=8443, secure=True,
    username=os.environ["KOINJU_DB_USER"], password=os.environ["KOINJU_DB_PASSWORD"],
    database="api",
)
koinju_df = ch.query_df("""
    SELECT start AS ts, market, close
    FROM api.ohlcv_1h
    WHERE market IN ('BTC-USDT', 'ETH-USDT')
      AND start >= now() - INTERVAL 7 DAY
""")

merged = your_df.merge(koinju_df, on=["ts", "market"], how="left")
```

### B) ETL Koinju → Postgres (nightly job)

```python
import psycopg2.extras

rows = ch.query("""
    SELECT start, exchange, market, open, high, low, close, volume
    FROM api.ohlcv(candle_duration_in_minutes = 1440)
    WHERE start >= today() - 1
""").result_rows

with pg, pg.cursor() as cur:
    psycopg2.extras.execute_values(cur,
        "INSERT INTO koinju_ohlcv_1d "
        "(start, exchange, market, open, high, low, close, volume) "
        "VALUES %s ON CONFLICT (start, exchange, market) DO UPDATE SET "
        "  open=EXCLUDED.open, high=EXCLUDED.high, low=EXCLUDED.low, "
        "  close=EXCLUDED.close, volume=EXCLUDED.volume",
        rows,
    )
```

Schedule with cron, systemd timer, or your orchestrator.

### C) Federate from your ClickHouse to Postgres + Koinju

If you have a ClickHouse instance, you can join Postgres tables and Koinju tables in a single SQL statement:

```sql
SELECT k.start, k.market, k.close, p.signal
FROM   remoteSecure('host.koinju.io:9440', api.ohlcv_1h, 'KOINJU_DB_USER', 'KOINJU_DB_PASSWORD') AS k
LEFT JOIN postgresql('pg-host:5432', 'db', 'trades', 'pg_user', 'pg_pass') AS p
       ON p.ts = k.start AND p.market = k.market
WHERE k.start >= now() - INTERVAL 1 DAY;
```

## ClickHouse (you already run one)

### A) `remoteSecure()` — query Koinju from your ClickHouse

Simplest path: keep your ClickHouse as the front door and federate the parts you need.

```sql
SELECT *
FROM remoteSecure('host.koinju.io:9440', api.ohlcv_1h, 'user', 'password')
WHERE market = 'BTC-USDT'
  AND start >= now() - INTERVAL 7 DAY;
```

`remoteSecure(host, database.table, user, password)`. The password sits in the query in clear text; in production use a **named collection**:

```sql
CREATE NAMED COLLECTION koinju AS
  host='host.koinju.io', port=9440,
  user='...', password='...';

SELECT * FROM remoteSecure(koinju, api.ohlcv_1h)
WHERE market = 'BTC-USDT' AND start >= now() - INTERVAL 1 DAY;
```

### B) ETL via `INSERT INTO ... SELECT FROM remoteSecure(...)`

```sql
INSERT INTO local.koinju_ohlcv_1h
SELECT *
FROM remoteSecure(koinju, api.ohlcv_1h)
WHERE start >= now() - INTERVAL 1 DAY
  AND market IN ('BTC-USDT', 'ETH-USDT', 'SOL-USDT');
```

Schedule hourly or daily. Deduplicate with `ReplacingMergeTree(start, exchange, market)` if you re-run overlapping windows.

### C) Refreshable Materialized View (ClickHouse Cloud)

```sql
CREATE MATERIALIZED VIEW local.koinju_ohlcv_1d_mirror
REFRESH EVERY 1 HOUR
ENGINE = ReplacingMergeTree
ORDER BY (exchange, market, start)
AS SELECT * FROM remoteSecure(koinju, api.ohlcv(candle_duration_in_minutes = 1440))
WHERE start >= now() - INTERVAL 30 DAY;
```

### Trade-offs

| Pattern | Pros | Cons |
|---|---|---|
| `remoteSecure()` per query | always fresh; no storage | per-query network latency; no local indexing |
| ETL (`INSERT ... SELECT`) | fast local queries; can add own indexes | staleness; storage cost |
| Hybrid (recent local, history federated) | hot path fast, no full mirror | extra logic for the cutover |

## Redis caching

Pattern: a worker fetches the latest values for the markets you care about at a cadence, writes to Redis with a TTL slightly longer than the polling interval.

```python
import os, time, redis, clickhouse_connect

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
ch = clickhouse_connect.get_client(
    host=os.environ["KOINJU_DB_HOST"], port=8443, secure=True,
    username=os.environ["KOINJU_DB_USER"], password=os.environ["KOINJU_DB_PASSWORD"],
    database="api",
)

MARKETS = [("binance", "BTC-USDT"), ("binance", "ETH-USDT")]
POLL_S  = 5

while True:
    rows = ch.query("""
        SELECT exchange, market, argMax(close, start) AS close
        FROM api.ohlcv_1m
        WHERE (exchange, market) IN %(markets)s
          AND start >= now() - INTERVAL 5 MINUTE
        GROUP BY exchange, market
    """, parameters={"markets": MARKETS}).result_rows

    pipe = r.pipeline()
    for exchange, market, close in rows:
        pipe.setex(f"koinju:price:{exchange}:{market}", POLL_S * 3, close)
    pipe.execute()
    time.sleep(POLL_S)
```

**Tips**:
- Sub-second freshness → use REST `/trade` (the `api.ohlcv_1m` view has a 1-minute floor).
- Many markets → batch them into one SQL query (above) rather than one per market.
- `setex(key, POLL_S * 3, value)` gives a grace window if the worker stalls.
- Key convention: `koinju:{class}:{exchange}:{market}` keeps things grep-able and consistent across services.
- For pub/sub (downstream services react to updates), `PUBLISH koinju:price:updates "{exchange} {market} {close}"` after each write.
