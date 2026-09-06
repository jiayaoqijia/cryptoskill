# Santiment API Skill

Query the Santiment GraphQL API for on-chain, financial, social, and development crypto metrics across 2,000+ assets and 12 blockchains.

## Overview

This skill enables AI agents to fetch cryptocurrency market data from the [Santiment API](https://api.santiment.net/graphql). It covers:

- **750+ metrics** including price, on-chain activity, exchange flows, holder behavior, social sentiment, and development activity
- **2,000+ assets** across 12 blockchains
- **Dynamic discovery** — find metrics and assets at runtime instead of relying on hardcoded lists
- **Ghost data detection** — diagnose empty results for on-chain metrics on non-indexed chains

## Configuration

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SANTIMENT_API_KEY` | Yes | Santiment API key. Free tier available at https://app.santiment.net/account#api-keys |

Set the key before invoking scripts:

```bash
export SANTIMENT_API_KEY="your_api_key_here"
```

## Scripts

| Script | Description | Input |
|---|---|---|
| `santiment_query.py` | Execute a GraphQL query for any metric, asset, and time range | `{"metric", "slug", "from", "to", "interval", ...}` |
| `santiment_discovery.py` | Discover available metrics, asset slugs, and metric metadata | `{"action": "metrics\|slugs\|metadata", ...}` |

Both scripts read JSON from stdin and write JSON to stdout. They use only Python standard library (`urllib`, `json`).

### santiment_query.py

Constructs and executes a `getMetric` query against the Santiment API.

**Input fields:**

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `metric` | string | Yes | — | Metric name (e.g., `price_usd`) |
| `slug` | string | No | `bitcoin` | Single asset identifier |
| `slugs` | string[] | No | — | Multiple assets (uses `timeseriesDataPerSlugJson`) |
| `from` | string | No | `utc_now-30d` | Start of time range |
| `to` | string | No | `utc_now` | End of time range |
| `interval` | string | No | `1d` | Data granularity |
| `sub_field` | string | No | `timeseriesData` | Query sub-field |
| `aggregation` | string | No | — | Override aggregation method |
| `transform` | object | No | — | Post-processing transform |
| `selector` | object | No | — | Advanced selector (overrides slug/slugs) |

**Example:**

```bash
echo '{"metric":"price_usd","slug":"bitcoin","from":"utc_now-7d","to":"utc_now","interval":"1d"}' | \
  python3 scripts/santiment_query.py
```

### santiment_discovery.py

Discover available metrics, project slugs, and metric metadata.

**Input fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `action` | string | Yes | `metrics`, `slugs`, or `metadata` |
| `search` | string | No | Filter keyword (for `metrics` and `slugs` actions) |
| `metric` | string | Conditional | Required for `metadata` action |

**Examples:**

```bash
# Find exchange-related metrics
echo '{"action":"metrics","search":"exchange"}' | python3 scripts/santiment_discovery.py

# Search for Bitcoin's slug
echo '{"action":"slugs","search":"bitcoin"}' | python3 scripts/santiment_discovery.py

# Get metadata for a specific metric
echo '{"action":"metadata","metric":"daily_active_addresses"}' | python3 scripts/santiment_discovery.py
```

## Query Patterns

The skill supports these `getMetric` sub-fields:

| Sub-field | Returns | Use case |
|---|---|---|
| `timeseriesData` | `[{datetime, value}]` | Time series for charting and analysis |
| `aggregatedTimeseriesData` | Single numeric value | Summary statistics (avg, sum, etc.) |
| `timeseriesDataPerSlugJson` | JSON keyed by slug | Compare multiple assets in one call |

See `examples/query-patterns.md` for 6 worked examples with curl commands.

## Supported Parameters

| Parameter | Example Values | Description |
|---|---|---|
| `metric` | `price_usd`, `mvrv_usd`, `exchange_inflow` | Metric name (snake_case) |
| `slug` | `bitcoin`, `ethereum`, `cardano` | Asset identifier |
| `from` / `to` | `utc_now-7d`, `2024-01-01T00:00:00Z` | Time range (relative or ISO 8601) |
| `interval` | `5m`, `1h`, `1d`, `7d` | Data granularity |
| `aggregation` | `AVG`, `SUM`, `LAST`, `MEDIAN` | Override default aggregation |
| `transform` | `{"type": "moving_average", "movingAverageBase": 7}` | Server-side post-processing |

## Error Handling

The API returns HTTP 200 for all responses, including errors. Always check for the `errors` array in the JSON response.

| Error Type | Cause | Resolution |
|---|---|---|
| Invalid metric | Metric name doesn't exist | Verify with `getAvailableMetrics` |
| Invalid slug | Asset not recognized | Verify with `allProjects` |
| Interval too small | Below metric's minimum | Check `metadata { minInterval }` |
| Complexity exceeded | Too many data points requested | Reduce time range or increase interval |
| HTTP 429 | Rate limit exceeded | Back off exponentially and retry |
| Empty data (no error) | On-chain metric on non-indexed chain | See ghost data detection in `references/metrics-catalog.md` |

## Rate Limits

API calls are limited by tier. Key optimization strategies:

- Use `aggregatedTimeseriesData` when a single value suffices
- Use `timeseriesDataPerSlugJson` to batch multiple assets into one call
- Prefer larger intervals (`1d` over `1h`) when high granularity isn't needed
- Check `availableSince` before querying to avoid wasted calls

See `references/rate-limits.md` for tier limits and complexity scoring details.

## Examples

See `examples/query-patterns.md` for 6 worked examples:

1. **Timeseries** — Daily Bitcoin price
2. **Multi-asset comparison** — Exchange inflows for BTC/ETH/XRP
3. **Transform** — MVRV with 7-day moving average
4. **Aggregated value** — Average daily active addresses
5. **Discovery workflow** — Finding and querying an unknown metric
6. **Ghost data detection** — Diagnosing empty on-chain results

## Best Practices

- **Discover dynamically**: Use `getAvailableMetrics` instead of hardcoding metric names
- **Check metadata first**: Call `metadata` on unfamiliar metrics to learn required selectors and minimum intervals
- **Validate data existence**: Use `availableSince` before large time range queries
- **Batch multi-asset queries**: Use `timeseriesDataPerSlugJson` with `slugs` instead of separate calls
- **Handle ghost data**: When on-chain metrics return empty, run the diagnostic flow before reporting "no activity"
- **Use GraphQL variables**: Separate query templates from runtime values to avoid escaping issues
