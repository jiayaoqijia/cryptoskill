# Points, limits, keys

## How points work

- The account has one balance: the points of its plan (Free 25 a day; Starter, Plus and Pro monthly). Keys spend from it.
- `GET /v1/models` lists every model with its price in points per million tokens and the typical points of one call per
  live agent; `GET /v1/pricing` has the per-tier typical cost of a whole cycle or run.
- Flat endpoints charge per request (see `GET /v1/pricing`, `endpoints[].points`). AI endpoints are metered on the models
  actually used, like the web app; `pricing.typical` and `POST /v1/analysis/quote` tell you the usual cost before you commit.
- Streams charge per connection hour, counted by the minute.
- A key may carry budgets: `daily_points_budget`, `monthly_points_budget`, `max_points_per_call`. `GET /v1/me` → `key.budget_left`.

## 402

```json
{"code": 402, "notify": "This call needs about 15 points; 3 left until …",
 "data": {"reason": "insufficient_points", "required_points": 15, "available_points": 3, "plan": "starter",
          "resets_at": "2026-11-01T00:00:00Z",
          "actions": {"renew_now": {"url": "https://www.simianx.ai/upgrade?renew=1", "allowed": true, "charges_now": true},
                      "change_plan": {"url": "https://www.simianx.ai/upgrade", "options": ["starter", "plus", "pro"]},
                      "subscribe": {"checkout_url": "https://www.simianx.ai/upgrade?plan=starter"}}}}
```

Hand the relevant link to the human. There is no top-up and no pay-per-call; never ask for card details.

## 429

`data.limit` says which limit: `requests_per_minute`, `requests_per_day`, `heavy_per_minute` (search, candles),
`points_per_minute` (a runaway brake on spend), `ai_concurrency`, `stream_connections`, `news_stream_connections`,
`autopilots`. Honour `Retry-After`.

| Plan | req/min | req/day | heavy/min | points/min | analyses at once | streams | news streams | keys | news delay |
|---|---|---|---|---|---|---|---|---|---|
| Free | 30 | 1,000 | 5 | 5 | 1 | 1 | 0 | 1 | 30 min |
| Starter | 120 | 20,000 | 20 | 30 | 2 | 2 | 0 | 3 | 30 min |
| Plus | 300 | 100,000 | 60 | 80 | 3 | 5 | 1 | 10 | live |
| Pro | 600 | 500,000 | 120 | 300 | 10 | 10 | 3 | 50 | live |

## 426

`{"code": 426, "data": {"reason": "skill_outdated", "minimum_version": "1.1.0", "current_version": "1.1.0", "skill_url": "https://www.simianx.ai/SKILL.md"}}`

Your cached skill is older than the API allows. Re-read `skill_url`, then retry the request with the new version in
`X-SimianX-Skill`. `GET /v1/skill` always answers (it is the update path) and lists the changelog and deprecations.

## Keys

- Scopes: `data:read`, `analysis:run`, `automation:manage`, `keys:manage`, `billing:manage`. A key may create keys
  (`POST /v1/keys`, scope `keys:manage`) only within its own scopes.
- `GET /v1/keys`, `GET /v1/keys/{id}` (with 30-day usage), `PATCH /v1/keys/{id}` (name, budgets, scopes, expires_at,
  ip_whitelist), `DELETE /v1/keys/{id}` (revoke). The token is returned once at creation.
- `GET /v1/usage?days=7` → requests and points by key, endpoint and day.
- Send `Idempotency-Key` on POST / PATCH / DELETE to make retries safe (24 h replay).
