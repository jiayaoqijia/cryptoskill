---
name: polyhub-discover
description: Query Polyhub public discover APIs for tags, trader rankings, trader detail by address, and market tag lookup by condition IDs.
---

# Polyhub Discover

Version: v0.3.8

Use this skill when the user wants public discover data from Polyhub.

## Requirements

- `curl` is available.
- `POLYHUB_API_KEY` is not required.

`POLYHUB_API_BASE_URL` is fixed to `https://polyhub.skill-test.bedev.hubble-rpc.xyz`.

## Workflow

1. Use the terminal to call Polyhub public APIs with `curl`.
2. Only pass filters the user explicitly requested.
3. Summarize results clearly instead of dumping raw JSON when the response is large.
4. The API returns `ALL-HUBBLE` as an internal tag name. Always display it as **All Markets** (or 全部市场) to the user.

## Base Setup

```bash
BASE="https://polyhub.skill-test.bedev.hubble-rpc.xyz"
```

## Intent Mapping

- List discover tags: `GET /api/v1/markets/tags`
- List traders by tag: `GET /api/v1/traders-v2/`
- Look up trader stats by address: `GET /api/v1/traders/by-address`
- Look up market tags by condition IDs: `GET /api/v1/markets/by-condition-ids`

## Common Calls

### List tags

```bash
curl -sS --fail-with-body "$BASE/api/v1/markets/tags"
```

### List traders for a tag

Required params:

- `tag`
- `time_range`: `all` or `30d`

Optional params:

- `limit`
- `offset`
- `filterBots`
- `sort_by`
- `sort_direction`
- numeric range filters such as `pnl_min`, `roi_min`, `trade_count_30_min`

```bash
curl -sS --fail-with-body \
  "$BASE/api/v1/traders-v2/?tag=Politics&time_range=all&limit=10&offset=0"
```

Guidance:

- Use `tag=CROSS-TAG` when the user wants cross-tag discover results.
- Use `time_range=30d` for recent performance.
- Prefer descending sort unless the user asked otherwise.

### Trader detail by address

```bash
curl -sS --fail-with-body \
  "$BASE/api/v1/traders/by-address?user_id=0x1234..."
```

### Market tag lookup by condition IDs

Validation:

- `ids` must be non-empty.
- Limit to `200` IDs per request.

```bash
curl -sS --fail-with-body \
  "$BASE/api/v1/markets/by-condition-ids?ids=0xabc,0xdef"
```

## Error Handling

- `400`: invalid params
- `500`: backend query failed or unavailable
