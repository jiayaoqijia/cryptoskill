---
name: santiment-api
description: Query the Santiment GraphQL API for on-chain, financial, social, and development crypto metrics across 2,000+ assets
version: 1.1.5
author: Santiment <support@santiment.net>
tags: [santiment, crypto, graphql, on-chain, metrics, blockchain, defi, exchange-flows, social-sentiment, mvrv, whale-tracking]

triggers:
  - type: keyword
    keywords: [santiment, crypto metrics, on-chain data, exchange flows, mvrv, nvt, social volume, whale tracking, active addresses, crypto analytics, token age, exchange inflow, exchange outflow, dev activity]
    priority: 90
  - type: pattern
    patterns:
      - "(?i)(query|fetch|get)\\s+(santiment|crypto|on-chain)"
      - "(?i)santiment\\s+api"
      - "(?i)(mvrv|nvt|exchange.*(inflow|outflow|balance))"
      - "(?i)(daily.active.addresses|social.volume|dev.activity)"
    priority: 85
  - type: intent
    intent_category: crypto_data_analysis
    priority: 95

parameters:
  - name: metric
    type: string
    required: false
    description: Santiment metric name (e.g., price_usd, daily_active_addresses, mvrv_usd)
  - name: slug
    type: string
    required: false
    description: Asset identifier (e.g., bitcoin, ethereum, cardano)
  - name: from
    type: string
    required: false
    description: Start of time range (ISO 8601 or relative expression like utc_now-7d)
  - name: to
    type: string
    required: false
    description: End of time range (ISO 8601 or relative expression like utc_now)
  - name: interval
    type: string
    required: false
    default: "1d"
    description: Data granularity (5m, 1h, 1d, 7d)

prerequisites:
  env_vars:
    - SANTIMENT_API_KEY
  skills: []

composable: true
persist_state: false

scripts:
  enabled: true
  working_directory: ./scripts
  definitions:
    - name: santiment_query
      description: Execute a Santiment GraphQL query for any metric, asset, and time range
      type: python
      file: santiment_query.py
      timeout: 30
    - name: santiment_discovery
      description: Discover available metrics and asset slugs from the Santiment API
      type: python
      file: santiment_discovery.py
      timeout: 30

metadata:
  openclaw:
    emoji: "📊"
    requires:
      env: [SANTIMENT_API_KEY]
    primaryEnv: SANTIMENT_API_KEY
---

# Santiment GraphQL API

Query the Santiment API — a GraphQL platform providing 750+ metrics for 2,000+ crypto assets across 12 blockchains. Fetch on-chain, financial, social, and development data for the cryptocurrency market.

## Endpoint and Authentication

- **GraphQL endpoint:** `https://api.santiment.net/graphql`
- **Interactive explorer:** `https://api.santiment.net/graphiql`

Every request requires an API key in the `Authorization` header (`Authorization: Apikey <KEY>`). The user must provide their own key — never hardcode or assume one. If `$SANTIMENT_API_KEY` is set in the environment, use it directly. Otherwise, ask the user for their key (free tier available at https://app.santiment.net/account#api-keys).

All requests are HTTP `POST` with `Content-Type: application/json`. **Use GraphQL variables** to separate the query template from runtime values — this avoids quote-escaping errors. In curl, use a heredoc with a quoted delimiter (`<< 'QUERY'`) so the shell doesn't interpret `$variable` as environment variables.

```bash
curl -s -X POST https://api.santiment.net/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Apikey $SANTIMENT_API_KEY" \
  -d @- << 'QUERY'
{
  "query": "query($metric: String!, $slug: String, $from: DateTime!, $to: DateTime!, $interval: interval) { getMetric(metric: $metric) { timeseriesData(slug: $slug, from: $from, to: $to, interval: $interval) { datetime value } } }",
  "variables": {
    "metric": "price_usd",
    "slug": "bitcoin",
    "from": "utc_now-7d",
    "to": "utc_now",
    "interval": "1d"
  }
}
QUERY
```

### Variable Types

Use these GraphQL types in `query(...)` variable declarations:

| Parameter | Type |
|---|---|
| `metric` | `String!` |
| `slug` | `String` |
| `selector` | `MetricTargetSelectorInputObject` |
| `from` / `to` | `DateTime!` |
| `interval` | `interval` |
| `aggregation` | `Aggregation` |
| `transform` | `TimeseriesMetricTransformInputObject` |

## Core Query: `getMetric`

Nearly all data flows through `getMetric`. Pass a metric name string and then select one sub-field that determines the shape of the response data.

### Sub-fields

Choose exactly one sub-field per `getMetric` call:

| Sub-field | Returns | When to use |
|---|---|---|
| `timeseriesData` | `[{datetime, value}]` | Default choice — returns a time series with explicit field selection. Use for charting, trend analysis, or any case where individual data points matter. |
| `timeseriesDataJson` | Pre-formatted JSON string | Quick dump without specifying return fields. Useful for rapid prototyping but less control over output shape. |
| `timeseriesDataPerSlugJson` | JSON object keyed by slug | Fetch the same metric for multiple assets in a single API call. Pass `selector: { slugs: ["bitcoin", "ethereum"] }`. This counts as one API call, making it much more efficient than separate queries per asset. |
| `aggregatedTimeseriesData` | Single numeric value | Need one summary number (average, sum, last value) over a time range. Lowest complexity, most quota-friendly. |
| `histogramData` | Array of bucketed ranges | Distribution data — e.g., how much ETH was bought at each price range. Less commonly needed. |
| `metadata` | Metric metadata object | Discover available slugs, aggregations, selectors, intervals, and data type for a metric. Call this before querying an unfamiliar metric. |
| `availableSince` | ISO 8601 date string | Check how far back data exists for a given metric and slug. Prevents wasted calls on empty time ranges. A return value of `1970-01-01T00:00:00Z` means the metric has **never been computed** for this slug. |
| `lastDatetimeComputedAt` | ISO 8601 timestamp | Check data freshness — when the metric was last computed for a slug. |

### Parameters

These parameters are passed to the sub-field, not to `getMetric` itself:

| Parameter | Type | Description | Example |
|---|---|---|---|
| `slug` | String | Asset identifier. Use for single-asset queries. | `"bitcoin"`, `"ethereum"` |
| `selector` | Object | Advanced selection. Use instead of `slug` when you need multi-asset queries, or filtering by `owner`, `label`, `holdersCount`, or `source`. | `{ slug: "bitcoin", source: "cryptocompare" }` |
| `from` | String | Start of time range. Accepts ISO 8601 timestamps or relative expressions. | `"2024-01-01T00:00:00Z"`, `"utc_now-30d"` |
| `to` | String | End of time range. Same format as `from`. | `"utc_now"` |
| `interval` | String | Time granularity between data points. | `"5m"`, `"1h"`, `"1d"`, `"7d"` |
| `aggregation` | Enum | Override the default aggregation method. Options: `AVG`, `SUM`, `LAST`, `FIRST`, `MEDIAN`, `MAX`, `MIN`, `ANY`. | `AVG` |
| `transform` | Object | Post-processing transform applied to the result. | See Transforms section. |

**Important:** `slug` and `selector` are mutually exclusive. Use `slug` for simple single-asset queries. Use `selector` when querying multiple slugs at once (`{ slugs: [...] }`) or when a metric requires additional selector fields like `holdersCount` or `owner`.

### Relative Time Expressions

The `from` and `to` fields accept relative expressions: `utc_now-<N><unit>` where unit is `d` (day), `w` (week), `m` (month), or `y` (year). Preferred over hardcoded dates.

- `"utc_now"` — current time
- `"utc_now-7d"` — 7 days ago
- `"utc_now-1m"` — 1 month ago
- `"utc_now-1y"` — 1 year ago

### Transforms

Apply transforms directly in the query to post-process data server-side. Pass the `transform` parameter to `timeseriesData`:

| Transform | Effect | Use case |
|---|---|---|
| `{type: "moving_average", movingAverageBase: N}` | Replace each value with the average of the preceding N values | Smooth noisy metrics like MVRV, social volume |
| `{type: "consecutive_differences"}` | Replace each value with the difference from the prior value | Compute daily change from a cumulative metric |
| `{type: "percent_change"}` | Replace each value with the percent change from the prior value | Normalize changes across metrics with different scales |

Transforms reduce the number of returned data points by N-1 for moving averages. Request a slightly wider time range to compensate.

## Dynamic Discovery

When you don't know the exact metric name for a user's request, follow this 3-step workflow. Always prefer dynamic discovery over hardcoded values.

### Step 1 — Fetch the metric list

```graphql
{
  getAvailableMetrics
}
```

Returns 1,000+ `snake_case` strings. **The response is large** — save to a file with `-o` and read it directly (e.g., `open()` in Python). Do not pipe the contents through stdin at any stage — neither from curl nor when processing the file afterward:

```bash
curl -s -X POST https://api.santiment.net/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Apikey <YOUR_API_KEY>" \
  -d '{"query": "{ getAvailableMetrics }"}' \
  -o /tmp/santiment-metrics.json
```

Filter by plan with `getAvailableMetrics(product: SANAPI, plan: BUSINESS_PRO)`.

### Step 2 — Search by keywords

Search the saved file for keywords matching user intent. Example: whale activity → search for `holder`, `top`, `whale`, `supply`, `amount_in`. See `references/metrics-catalog.md` for intent-to-keyword mappings.

### Step 3 — Inspect metadata before querying

Once you have candidate metrics, fetch metadata to confirm compatibility:

```graphql
{
  getMetric(metric: "amount_in_top_holders") {
    metadata {
      availableSlugs
      availableAggregations
      availableSelectors
      dataType
      defaultAggregation
      minInterval
    }
  }
}
```

This reveals required selectors (e.g., `holdersCount`), supported slugs, and minimum interval. Requesting a smaller interval than `minInterval` returns an error. See `examples/query-patterns.md` example 5 for a worked example.

### Find a project's slug

Look up a specific project by slug to verify it exists and see its details:

```graphql
{
  projectBySlug(slug: "bitcoin") {
    slug
    name
    ticker
    infrastructure
  }
}
```

Browse all projects paginated (useful when the user provides a token name or ticker instead of a slug):

```graphql
{
  allProjects(page: 1, pageSize: 50) {
    slug
    name
    ticker
  }
}
```

### Check data availability for a metric and slug

Before making a large timeseries query, verify that data exists for the desired metric-slug combination and check freshness:

```graphql
{
  getMetric(metric: "daily_active_addresses") {
    availableSince(slug: "ethereum")
    lastDatetimeComputedAt(slug: "ethereum")
  }
}
```

### Check access restrictions for your plan

Understand what historical range your API key can access for each metric. Call this to avoid wasted queries that would return restriction errors:

```graphql
{
  getAccessRestrictions(product: SANAPI, plan: BUSINESS_PRO, filter: METRIC) {
    name
    isAccessible
    isRestricted
    restrictedFrom
    restrictedTo
    minInterval
  }
}
```

## Error Handling

The API always returns HTTP **200**, even for errors. Always parse the JSON and check for the `errors` array.

A typical error response:

```json
{
  "data": { "getMetric": null },
  "errors": [
    {
      "message": "The metric 'nonexistent_metric' is not a valid metric.",
      "locations": [{ "line": 2, "column": 3 }]
    }
  ]
}
```

When `data` contains `null` and `errors` is present, the query failed. Common errors:

| Error | Cause | Fix |
|---|---|---|
| Invalid metric name | Metric string doesn't exist | Verify with `getAvailableMetrics` |
| Invalid slug | Asset slug not recognized | Verify with `allProjects` or `projectBySlug` |
| Interval too small | Requested interval below minimum for this metric or plan | Check `metadata { minInterval }` |
| Time range restricted | Historical range exceeds plan allowance | Check `getAccessRestrictions` |
| Complexity too high | Query requests too many data points | Reduce time range, increase interval, or fetch fewer fields |
| HTTP 429 | Rate limit exceeded | Back off exponentially and retry after a delay |
| Empty timeseries (no error) | On-chain metric not computed for this asset's chain | Check `availableSince` for epoch, then `projectBySlug { infrastructure }`. See `references/metrics-catalog.md` Ghost Data section. |

**Empty data is not the same as zero data.** When `timeseriesData` returns `[]` without errors, do NOT tell the user there is no activity. On-chain metrics are only computed for indexed chains. Check `references/metrics-catalog.md` Ghost Data section for the diagnostic flow.

The one exception to the HTTP 200 rule is rate limiting: HTTP **429** means the account's quota is exhausted. See `references/rate-limits.md` for details.

## Quick Reference: Building a Query

Follow these steps to construct any Santiment API query:

1. **Pick a metric** — use directly if known, otherwise follow Discovery Workflow.
2. **Pick a slug** — resolve names/tickers via `projectBySlug` or `allProjects`.
3. **Pick a time range** — relative expressions preferred. Check `availableSince` first.
4. **Pick an interval** — `"1d"`, `"1h"`, `"7d"`. Larger intervals reduce complexity.
5. **Pick a sub-field** — `timeseriesData` for series, `aggregatedTimeseriesData` for single value, `timeseriesDataPerSlugJson` for multi-asset.
6. **Optionally add** — `transform`, `selector` (instead of `slug`), or `aggregation` override.
7. **If data is empty** — check `availableSince` for epoch. If epoch, the metric isn't computed for this slug's chain. Report unavailability and suggest alternative metrics.

Execute via curl with the user's API key and parse the JSON response. Always check for the `errors` array before processing `data`.

## Additional Resources

Consult these reference files for detailed information:

- **Metrics catalog** — `references/metrics-catalog.md` — keyword-to-metric mapping for translating user intent into search terms, plus 20 curated quick-reference metrics and naming conventions
- **Rate limits** — `references/rate-limits.md` — tier limits, complexity scoring, and optimization strategies to avoid quota exhaustion
- **Query patterns** — `examples/query-patterns.md` — 6 worked examples with both GraphQL and curl, including discovery workflow and ghost data diagnostics
