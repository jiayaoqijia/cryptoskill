---
name: polyhub_discover
description: Explore public discover data on Polyhub without API key auth, including tags, trader rankings, trader detail stats, and market tag lookup.
---

# Polyhub Discover Skill

Version: v0.3.8

## When to use

Use this skill when the user asks about:

- Discover page tag list
- Trader rankings on the discover page
- Cross-tag discover queries
- Filtering and sorting discover traders
- Looking up a trader by address
- Looking up market tags by condition IDs

## Requirements

- `curl` must be available in the runtime environment

`POLYHUB_API_BASE_URL` is fixed to `https://polyhub.skill-test.bedev.hubble-rpc.xyz`.

This skill does not require `POLYHUB_API_KEY`.

## Safety rules

- These are public read-only endpoints. No confirmation step is required.
- Do not invent filter values. Only pass filters the user requested.
- Prefer building query strings from explicit user intent.
- When querying by address, trim whitespace and keep the original checksum/casing if provided.

## Display rules

- The API returns `ALL-HUBBLE` as an internal tag name. When presenting results to the user, always display it as **All Markets** (or 全部市场 in Chinese context). Never show the raw `ALL-HUBBLE` string to the user.

## Tools

Use the `bash` tool to call the API with `curl`.

## Fast Path

For common intents, map user requests like this:

- “discover 页有哪些标签” -> `GET /api/v1/markets/tags`
- “看某个 tag 的 trader 排行” -> `GET /api/v1/traders-v2/?tag=...`
- “跨 tag 找高手” -> `GET /api/v1/traders-v2/?tag=CROSS-TAG`
- “看某个地址在各标签下的数据” -> `GET /api/v1/traders/by-address?user_id=...`
- “查 condition id 对应什么标签” -> `GET /api/v1/markets/by-condition-ids?ids=...`

### Curl base setup

```bash
BASE="https://polyhub.skill-test.bedev.hubble-rpc.xyz"
```

---

## Tags

### Action: List discover tags

- `GET /api/v1/markets/tags`
- Auth: public

```bash
curl -sS --fail-with-body "$BASE/api/v1/markets/tags"
```

Use this when the user wants the discover page tag list or wants to browse available niches first.

---

## Trader Rankings

### Action: List traders for discover

- `GET /api/v1/traders-v2/`
- Auth: public

Core query params:

- `tag` — required
- `time_range` — required: `all` or `30d`
- `limit` — optional, default `10`, max `100`
- `offset` — optional, default `0`
- `filterBots` — optional: `0` or `1`
- `sort_by` — optional: `volume`, `pnl`, `roi`, `avg_adt`, `trade_count_30`, `ev_per_bought`, `timing_score`
- `sort_direction` — optional: `asc` or `desc`

Range filter params:

- `pnl_min`, `pnl_max`
- `volume_min`, `volume_max`
- `roi_min`, `roi_max`
- `avg_adt_min`, `avg_adt_max`
- `trade_count_30_min`, `trade_count_30_max`
- `ev_per_bought_min`, `ev_per_bought_max`
- `timing_score_min`, `timing_score_max`

Validation:

- `tag` is required
- `time_range` must be `all` or `30d`
- `limit` should be between `1` and `100`
- `offset` should be `0` or greater
- `filterBots` should be `0` or `1`

Example: standard discover query

```bash
curl -sS --fail-with-body \
  "$BASE/api/v1/traders-v2/?tag=Politics&time_range=all&limit=10&offset=0"
```

Example: cross-tag query

```bash
curl -sS --fail-with-body \
  "$BASE/api/v1/traders-v2/?tag=CROSS-TAG&time_range=30d&limit=20&offset=0"
```

Example: filtered and sorted query

```bash
curl -sS --fail-with-body \
  "$BASE/api/v1/traders-v2/?tag=Sports&time_range=30d&filterBots=1&pnl_min=1000&trade_count_30_min=30&sort_by=ev_per_bought&sort_direction=desc"
```

Guidance:

- Use `tag=CROSS-TAG` when the user wants discover results across all tags.
- Use `time_range=30d` when the user asks for recent performance.
- Use `filterBots=1` when the user explicitly wants bot filtering.
- Prefer `sort_direction=desc` unless the user explicitly wants ascending order.

---

## Trader Detail

### Action: Get trader stats by address

- `GET /api/v1/traders/by-address`
- Auth: public

Required query params:

- `user_id` — trader wallet address

Optional query params:

- `time_range` — if supported by caller flow

```bash
curl -sS --fail-with-body \
  "$BASE/api/v1/traders/by-address?user_id=0x1234..."
```

Use this when the user clicks into a trader from discover and wants stats across tags.

---

## Market Tag Lookup

### Action: Get market tags by condition IDs

- `GET /api/v1/markets/by-condition-ids`
- Auth: public

Required query params:

- `ids` — comma-separated condition ID list

Validation:

- `ids` must not be empty
- The backend supports up to `200` IDs per request

```bash
curl -sS --fail-with-body \
  "$BASE/api/v1/markets/by-condition-ids?ids=0xabc,0xdef"
```

Use this when the user wants to map market condition IDs back to discover tags.

---

## Strategy: Find Profitable Traders

When the user asks to find traders worth copying (e.g. "帮我找值得跟单的地址", "find me smart money", "谁在赚钱"), follow this multi-step process:

### Step 1: Query top traders

Choose the scope based on user intent:
- If user specifies a tag (e.g. "Sports"), use that tag
- If user wants broad search, use `tag=CROSS-TAG`
- Always use `time_range=30d` unless user asks for all-time

Default filters (user can override any):
- `filterBots=1` (exclude bots)
- `pnl_min=5000` (minimum $5K profit in 30 days)
- `timing_score_min=52` (at least slightly positive alpha)
- `trade_count_30_min=30` (enough trades for statistical significance)
- `sort_by=ev_per_bought`, `sort_direction=desc` (rank by expected return per dollar)
- `limit=15`

```bash
curl -sS --fail-with-body \
  "$BASE/api/v1/traders-v2/?tag=Sports&time_range=30d&filterBots=1&pnl_min=5000&timing_score_min=52&trade_count_30_min=30&sort_by=ev_per_bought&sort_direction=desc&limit=15"
```

### Step 2: Identify hot sub-tags

From Step 1 results, note which tags appear frequently in top results. Common valuable sub-tags under Sports: Soccer, Premier League, UCL, NBA, NHL, Liga MX, Argentina Primera División.

Then query those specific sub-tags with the same filters to find specialists:

```bash
curl -sS --fail-with-body \
  "$BASE/api/v1/traders-v2/?tag=Soccer&time_range=30d&filterBots=1&pnl_min=5000&timing_score_min=52&trade_count_30_min=10&sort_by=ev_per_bought&sort_direction=desc&limit=10"
```

### Step 3: Cross-validate with by-address

For top 3-5 candidates, call by-address to see their performance across ALL tags:

```bash
curl -sS --fail-with-body \
  "$BASE/api/v1/traders/by-address?user_id=0x..."
```

Evaluation criteria (prioritized):
1. **Multi-tag consistency**: Strong in 3+ sub-tags beats one-hit wonder
2. **Alpha Score > 55**: Indicates buy-low-sell-high timing ability (higher = better)
3. **EV/Bought > 0.25**: Good expected return per dollar invested
4. **30D trades >= 30**: Statistically reliable sample size
5. **Positive 30D PnL across tags**: Not just one lucky market

Disqualify if:
- ALL-HUBBLE EV < 0.1 (too many low-quality trades overall)
- Only one sub-tag has positive PnL (single-market luck)
- Alpha = 50 exactly in main tag (no timing edge)

### Step 4: Present results and handoff

Present ranked results in this format:

```
🏆 推荐跟单地址

1. 0x{address}
   📊 Sports 30D: PnL ${pnl}, EV/Bought {ev}, Alpha {alpha}
   📈 强势子标签: {subtag1} (EV {ev1}), {subtag2} (EV {ev2})
   🔗 详情: https://polyhub.hubble.xyz/trader/{address}

想跟单哪个？
A) 我直接帮你创建跟单任务（通过 polyhub_copy skill，需要 API key）
B) 打开网页操作: https://polyhub.hubble.xyz/discover?copy={address}&tag={tag}
```

### Parameter override examples

- "PnL 至少 1 万" → `pnl_min=10000`
- "要更活跃的" → `trade_count_30_min=100`
- "Alpha 要高" → `timing_score_min=60`
- "我要看机器人" → `filterBots=0`
- "看全量数据" → `time_range=all`

### Empty results fallback

If a query returns zero results, progressively loosen filters:
1. Reduce `pnl_min` to 1000
2. Reduce `trade_count_30_min` to 10
3. Remove `timing_score_min`
4. Broaden to `tag=CROSS-TAG` if using a niche sub-tag

---

## Handoff to Copy

After the user selects an address to copy:

1. **Preferred: Skill 直接创建** — If `POLYHUB_API_KEY` is configured, use `polyhub_copy` skill's "Quick Copy from Discover" flow:
   - Check balance via `GET /api/v1/portfolio/stats`
   - If balance sufficient → `POST /api/v1/copy-tasks` with `targetTrader` and optional `filteredByTag`
   - If balance insufficient → direct user to deposit on the web (skill cannot deposit): `https://polyhub.hubble.xyz/copy-history?action=deposit`
2. **Fallback: 网页端跟单** — Provide the deep link: `https://polyhub.hubble.xyz/discover?copy={address}&tag={tag}`
3. Always show the trader detail page link: `https://polyhub.hubble.xyz/trader/{address}`

Note: Depositing funds is **only possible via the web UI**, not through any skill or API.

---

## Error handling

- `400`: Invalid query parameters such as missing `tag`, invalid `time_range`, or empty `ids`
- `500`: Backend query failed or service unavailable
