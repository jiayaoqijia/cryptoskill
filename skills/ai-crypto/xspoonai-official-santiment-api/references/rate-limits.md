# Santiment API Rate Limits

## Tier Limits

| Tier | Monthly calls | Per hour | Per minute |
|---|---|---|---|
| Free | 1,000 | 500 | 100 |
| Sanbase Pro | 5,000 | 1,000 | 100 |
| Sanbase Max | 80,000 | 4,000 | 100 |
| Business Pro/Max | Higher (custom) | Higher | Higher |

## Key Rules

- Rate limits are **per account** — all API keys on one account share limits.
- Each GraphQL **query** inside a request counts as one API call (a single HTTP request can contain multiple queries).
- HTTP **429** = rate limited. Back off and retry.
- **Free tier**: 1 year of historical data, 30-day lag on real-time data.

## Complexity Scoring

Every request is scored for complexity (~50,000 max). Complexity grows with the number of data points returned:

- **Wider time range + smaller interval = more data points = higher complexity.**
- If complexity is exceeded, the request is rejected before execution.
- The error message will indicate the complexity limit was exceeded.

## Optimization Strategies

Use these strategies to minimize API calls and stay within limits:

1. **Use `aggregatedTimeseriesData`** when you only need a summary number — returns a single value instead of a full series.
2. **Use `timeseriesDataPerSlugJson`** with `slugs` to batch multiple assets into one call instead of making separate calls per asset.
3. **Prefer larger `interval` values** (e.g., `"1d"` over `"1h"`) when high granularity isn't needed.
4. **Narrow the time range** — only fetch the period you actually need.
5. **Cache responses** — avoid re-fetching data that hasn't changed.
6. **Check `availableSince`** before querying — avoids wasting calls on time ranges with no data.
