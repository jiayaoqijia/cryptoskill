# Santiment GraphQL Query Patterns

Six examples demonstrating distinct API capabilities. Each uses a different sub-field or parameter pattern. All curl commands use GraphQL variables with a heredoc to avoid quote-escaping issues.

## 1. Timeseries — Daily Bitcoin Price

Uses `timeseriesData` with relative time expressions to fetch a daily price series.

```graphql
{
  getMetric(metric: "price_usd") {
    timeseriesData(
      slug: "bitcoin"
      from: "utc_now-7d"
      to: "utc_now"
      interval: "1d"
    ) {
      datetime
      value
    }
  }
}
```

**curl:**

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

## 2. Multi-Asset Comparison — Exchange Inflows

Uses `timeseriesDataPerSlugJson` with a `slugs` selector to fetch one metric for several assets in a single API call.

```graphql
{
  getMetric(metric: "exchange_inflow") {
    timeseriesDataPerSlugJson(
      selector: { slugs: ["bitcoin", "ethereum", "ripple"] }
      from: "utc_now-30d"
      to: "utc_now"
      interval: "1d"
    )
  }
}
```

**curl:**

```bash
curl -s -X POST https://api.santiment.net/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Apikey $SANTIMENT_API_KEY" \
  -d @- << 'QUERY'
{
  "query": "query($metric: String!, $selector: MetricTargetSelectorInputObject, $from: DateTime!, $to: DateTime!, $interval: interval) { getMetric(metric: $metric) { timeseriesDataPerSlugJson(selector: $selector, from: $from, to: $to, interval: $interval) } }",
  "variables": {
    "metric": "exchange_inflow",
    "selector": { "slugs": ["bitcoin", "ethereum", "ripple"] },
    "from": "utc_now-30d",
    "to": "utc_now",
    "interval": "1d"
  }
}
QUERY
```

## 3. Transform — Ethereum MVRV with 7-Day Moving Average

Uses the `transform` parameter to smooth noisy data with a moving average.

```graphql
{
  getMetric(metric: "mvrv_usd") {
    timeseriesData(
      slug: "ethereum"
      from: "utc_now-6m"
      to: "utc_now"
      interval: "1d"
      transform: { type: "moving_average", movingAverageBase: 7 }
    ) {
      datetime
      value
    }
  }
}
```

**curl:**

```bash
curl -s -X POST https://api.santiment.net/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Apikey $SANTIMENT_API_KEY" \
  -d @- << 'QUERY'
{
  "query": "query($metric: String!, $slug: String, $from: DateTime!, $to: DateTime!, $interval: interval, $transform: TimeseriesMetricTransformInputObject) { getMetric(metric: $metric) { timeseriesData(slug: $slug, from: $from, to: $to, interval: $interval, transform: $transform) { datetime value } } }",
  "variables": {
    "metric": "mvrv_usd",
    "slug": "ethereum",
    "from": "utc_now-6m",
    "to": "utc_now",
    "interval": "1d",
    "transform": { "type": "moving_average", "movingAverageBase": 7 }
  }
}
QUERY
```

## 4. Aggregated Value — Average Daily Active Addresses

Uses `aggregatedTimeseriesData` to return a single summary number instead of a time series.

```graphql
{
  getMetric(metric: "daily_active_addresses") {
    aggregatedTimeseriesData(
      slug: "cardano"
      from: "utc_now-30d"
      to: "utc_now"
      aggregation: AVG
    )
  }
}
```

**curl:**

```bash
curl -s -X POST https://api.santiment.net/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Apikey $SANTIMENT_API_KEY" \
  -d @- << 'QUERY'
{
  "query": "query($metric: String!, $slug: String, $from: DateTime!, $to: DateTime!, $aggregation: Aggregation) { getMetric(metric: $metric) { aggregatedTimeseriesData(slug: $slug, from: $from, to: $to, aggregation: $aggregation) } }",
  "variables": {
    "metric": "daily_active_addresses",
    "slug": "cardano",
    "from": "utc_now-30d",
    "to": "utc_now",
    "aggregation": "AVG"
  }
}
QUERY
```

## 5. Discovery Workflow — Finding and Querying an Unknown Metric

Demonstrates the full discovery flow when the user asks for data and you don't know the exact metric name. Scenario: "How much ETH do the top 100 holders own?"

**Step 1 — Fetch all metrics and search by keyword.**

The response is large (1,000+ metrics), so save it to a file with `-o` and read it directly (e.g., `open()` in Python). Do not pipe the contents through stdin at any stage — neither from curl nor when processing the file afterward:

```bash
curl -s -X POST https://api.santiment.net/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Apikey $SANTIMENT_API_KEY" \
  -d '{"query": "{ getAvailableMetrics }"}' \
  -o /tmp/santiment-metrics.json
```

Then search the file for keywords matching the user's intent: `holder`, `top`, `amount`. Matches include `amount_in_top_holders`, `holders_distribution_combined_balance`, and others.

**Step 2 — Inspect metadata for the best candidate.**

```graphql
{
  getMetric(metric: "amount_in_top_holders") {
    metadata {
      availableSlugs
      availableSelectors
      defaultAggregation
      minInterval
      dataType
    }
  }
}
```

The metadata reveals this metric supports `slug: "ethereum"` and requires a `holdersCount` field in the selector. The minimum interval is `1d`.

**Step 3 — Query with the correct parameters.**

```graphql
{
  getMetric(metric: "amount_in_top_holders") {
    timeseriesData(
      selector: { slug: "ethereum", holdersCount: 100 }
      from: "utc_now-30d"
      to: "utc_now"
      interval: "1d"
    ) {
      datetime
      value
    }
  }
}
```

**curl:**

```bash
curl -s -X POST https://api.santiment.net/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Apikey $SANTIMENT_API_KEY" \
  -d @- << 'QUERY'
{
  "query": "query($metric: String!, $selector: MetricTargetSelectorInputObject, $from: DateTime!, $to: DateTime!, $interval: interval) { getMetric(metric: $metric) { timeseriesData(selector: $selector, from: $from, to: $to, interval: $interval) { datetime value } } }",
  "variables": {
    "metric": "amount_in_top_holders",
    "selector": { "slug": "ethereum", "holdersCount": 100 },
    "from": "utc_now-30d",
    "to": "utc_now",
    "interval": "1d"
  }
}
QUERY
```

This example demonstrates the full discovery flow: search the metric list by keywords, inspect metadata to learn required selectors, then construct the query with the correct parameters. The `holdersCount` selector would not have been obvious without the metadata step.

## 6. Ghost Data Detection — Diagnosing Empty On-Chain Results

Demonstrates the reactive diagnostic flow when an on-chain metric returns empty data for a token on a non-indexed chain. Scenario: "Show me daily active addresses for Trust Wallet Token (TWT)."

**Step 1 — Normal query returns empty `[]`.**

```graphql
{
  getMetric(metric: "daily_active_addresses") {
    timeseriesData(
      slug: "trust-wallet-token"
      from: "utc_now-30d"
      to: "utc_now"
      interval: "1d"
    ) {
      datetime
      value
    }
  }
}
```

Response: `{ "data": { "getMetric": { "timeseriesData": [] } } }` — no error, just empty data.

**Step 2 — Check `availableSince` and identify the token's chain.**

Combine the diagnostic checks into a single API call:

```graphql
{
  getMetric(metric: "daily_active_addresses") {
    availableSince(slug: "trust-wallet-token")
    lastDatetimeComputedAt(slug: "trust-wallet-token")
  }
  projectBySlug(slug: "trust-wallet-token") {
    name
    ticker
    infrastructure
  }
}
```

Response reveals:
- `availableSince`: `"1970-01-01T00:00:00Z"` — **epoch = never computed**
- `infrastructure`: `"BEP20"` — TWT lives on BNB Chain, not indexed for on-chain metrics

**curl (combined diagnostic):**

```bash
curl -s -X POST https://api.santiment.net/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Apikey $SANTIMENT_API_KEY" \
  -d @- << 'QUERY'
{
  "query": "{ getMetric(metric: \"daily_active_addresses\") { availableSince(slug: \"trust-wallet-token\") lastDatetimeComputedAt(slug: \"trust-wallet-token\") } projectBySlug(slug: \"trust-wallet-token\") { name ticker infrastructure } }"
}
QUERY
```

**Step 3 — Pivot to a chain-agnostic metric.**

```graphql
{
  getMetric(metric: "price_usd") {
    availableSince(slug: "trust-wallet-token")
    timeseriesData(
      slug: "trust-wallet-token"
      from: "utc_now-7d"
      to: "utc_now"
      interval: "1d"
    ) {
      datetime
      value
    }
  }
}
```

`availableSince` returns a real date (not epoch), and `timeseriesData` returns actual price data — confirming the token has financial data even though on-chain metrics are unavailable.

**Example user-facing response:**

> Daily active addresses is not available for Trust Wallet Token (TWT) because Santiment does not index on-chain data for BEP-20 tokens. However, I can provide price, trading volume, social, and development metrics. Here's the TWT price for the last 7 days: [data]

This example demonstrates the ghost data diagnostic flow: detect empty results, confirm via `availableSince` epoch check, identify the chain, and pivot to available metrics. See `references/metrics-catalog.md` Ghost Data section for the full decision tree.
