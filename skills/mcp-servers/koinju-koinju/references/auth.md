# Authentication

Koinju provides two ways to access market data:

- **REST API** (`api.koinju.io`) — simple HTTP, header-based auth.
- **SQL API** (ClickHouse) — heavy analytics over the same data, full SQL access.

Both share the same credentials, supplied via environment variables.

## Environment variables

| Variable | Required | Used by | Notes |
|---|---|---|---|
| `KOINJU_API_KEY` | yes | REST | Value of the `x-api-key` header |
| `KOINJU_DB_HOST` | yes | SQL | **Bare hostname only** — no `https://`, no port, no trailing slash. Right: `abc123.koinju.io`. Wrong: `https://abc123.koinju.io:8443/`. The dataroom often shows the full URL; copy just the hostname. |
| `KOINJU_DB_USER` | yes | SQL | ClickHouse username |
| `KOINJU_DB_PASSWORD` | yes | SQL | ClickHouse password |
| `KOINJU_DB_PORT` | no | SQL | Defaults to `8443` (clickhouse-connect HTTPS). Don't append this to `KOINJU_DB_HOST`. |
| `KOINJU_DB_DATABASE` | no | SQL | Defaults to `api` |

Persist them in your shell profile (`~/.zshrc`, `~/.bashrc`) or load them per-project with `direnv` / `python-dotenv`:

```bash
export KOINJU_API_KEY=...
export KOINJU_DB_HOST=...
export KOINJU_DB_USER=...
export KOINJU_DB_PASSWORD=...
```

For a single chmod-600 file that you source manually:

```bash
install -m 600 /dev/null ~/.koinju.env
$EDITOR ~/.koinju.env       # add the four exports above
echo 'source ~/.koinju.env' >> ~/.zshrc
```

## Helper to read them (Python)

The helper **auto-sources `.koinju.env` (project-local, in cwd) then `~/.koinju.env` (global fallback)** — project-local wins per-var, and any env var already set in the current process wins over both (via `setdefault`). This means users running scripts from inside a `koinju-demo/` project get their `.koinju.env` picked up automatically, and users with a global `~/.koinju.env` don't need to `source` it each shell. Use this same helper in any ad-hoc Python you write.

```python
import os

REQUIRED = ("KOINJU_API_KEY", "KOINJU_DB_HOST", "KOINJU_DB_USER", "KOINJU_DB_PASSWORD")


def _autosource_koinju_env() -> None:
    """Load `export FOO=bar` lines from .koinju.env (cwd) then ~/.koinju.env.

    Project-local `.koinju.env` wins per-var over global `~/.koinju.env`;
    existing env vars in the current process win over both (via `setdefault`).
    """
    for path in (".koinju.env", os.path.expanduser("~/.koinju.env")):
        if not os.path.isfile(path):
            continue
        with open(path) as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("export "):
                    line = line[7:]
                if "=" not in line:
                    continue
                key, _, value = line.partition("=")
                value = value.strip().strip('"').strip("'")
                os.environ.setdefault(key.strip(), value)


def load_koinju_credentials() -> dict[str, str]:
    _autosource_koinju_env()
    missing = [v for v in REQUIRED if not os.environ.get(v)]
    if missing:
        raise RuntimeError(f"Missing Koinju env vars: {', '.join(missing)}")
    return {
        "api_key":     os.environ["KOINJU_API_KEY"],
        "db_host":     os.environ["KOINJU_DB_HOST"],
        "db_port":     int(os.environ.get("KOINJU_DB_PORT", "8443")),
        "db_user":     os.environ["KOINJU_DB_USER"],
        "db_password": os.environ["KOINJU_DB_PASSWORD"],
        "db_database": os.environ.get("KOINJU_DB_DATABASE", "api"),
    }
```

## If the user has no credentials

The Koinju credential flow is **paid sign-up → emailed dataroom link → credentials page**. Don't position the dataroom as a self-serve front door — it's the post-purchase portal.

1. **Don't have credentials yet?** Pick a plan at https://koinju.io/pricing. Koinju emails a link to your private dataroom (`https://dataroom.koinju.io/<your-tenant>`) once sign-up completes.
2. **Already signed up?** Check your inbox for the dataroom invitation. The REST API key and ClickHouse host / user / password live on the credentials page inside the dataroom.
3. **Stuck (no email, lost access, enterprise onboarding)?** Email `support@koinju.io` with subject "Koinju API credentials request" — they'll send a OneTimeSecret link.

Once they have the values, have them `export` the four variables in their shell profile (or a sourced `~/.koinju.env` as shown above).

## Free demo database (no credentials)

An agent without credentials can query one validated UTC day, 18 October 2026 (`2026-10-18`), through the free demo database: no sign-up, user `demo` with an empty password. In `api`, `public_data` and `reference_data` the names and columns are production's, so the same SQL runs unchanged with a paid login later.

| Setting | Value |
|---|---|
| Host | `sn7u7x3woz.eu-central-1.aws.clickhouse.cloud` |
| Port | `8443` (HTTPS), `9440` (native, TLS) |
| User / password | `demo` / empty |
| Database | `api` |

```python
import clickhouse_connect

client = clickhouse_connect.get_client(
    host="sn7u7x3woz.eu-central-1.aws.clickhouse.cloud",
    port=8443,
    secure=True,
    username="demo",
    password="",
    database="api",
)
print(client.query("SELECT min(timestamp), max(timestamp) FROM api.trade").result_rows)
```

- It holds one day, 18 October 2026 (`2026-10-18`), and is not refreshed; the query above gives its bounds. Bound a query by that day, `timestamp >= '2026-10-18' AND timestamp < '2026-10-19'`, not by `now()`: a window such as `now() - INTERVAL 3 DAY` finds nothing from 22 October.
- It is read only: 10 s and 2 GB per query, and per IP address per hour 300 queries, 1.7 GB of answers and 60 s of query time.
- `load_koinju_credentials()` and the bundled scripts need all four `KOINJU_*` variables non-empty, so connect directly as above.
- A query that asks for a truncated answer (`result_overflow_mode = 'break'`) must also set `use_query_cache = 0`, or it fails with code 731.
- Reference: https://docs.koinju.io/free-demo-database

## REST API

| Endpoints | Auth | Free | Dev | Pro | Biz | Enterprise |
|---|---|---|---|---|---|---|
| `/market/*` (spot, future, option listings) | none | 10 req/s | 10 req/s | 10 req/s | 10 req/s | custom |
| `/ohlcv`, `/trade`, `/funding-rate`, `/volatility-index`, `/stats` | `x-api-key` | 100/day | 1k/day | 10k/day | 50k/day | custom |

Send the API key in the `x-api-key` header. Free tier returns up to 100 items per call; Dev/Pro 1000; Biz unlimited.

## SQL API

ClickHouse over HTTPS on port 8443. Same credentials work via:

- `clickhouse-connect` (Python)
- `clickhouse-rs` (Rust)
- `clickhouse-go` (Go)
- `clickhouse-client` CLI
- Most BI tools (Grafana, Metabase, Tableau, ...)

See `references/data-tables.md` for the available `api.*` views.
