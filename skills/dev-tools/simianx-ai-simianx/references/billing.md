# Points, limits, keys

**For agents.** Calls use the points of the user's plan at the website's rates, within the budgets the user set on
this key. A price check before each run is not needed; when the user asks about costs, the balance or the budgets,
answer from `GET /v1/me`, `GET /v1/usage` or the headers. On a `402` (below), say that the points or this key's budget
ran out and give the links. Code clients read everything here from the headers and `POST /v1/analysis/quote`.

## How points work

- The account has one balance: the points of its plan (Free 20 a day; Starter, Plus and Pro monthly). Keys spend from it.
- `GET /v1/models` lists every model with its price in points per million tokens and the typical points of one call per
  live agent; `POST /v1/analysis/quote` gives the cost of a whole cycle or run on the user's own models.
- Flat endpoints charge per request (see `GET /v1/pricing`, `endpoints[].points`). AI endpoints are metered on the models
  actually used, like the web app; `pricing.typical` and `POST /v1/analysis/quote` give code clients the usual cost.
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

Hand the relevant link to the human, once, plainly. There is no top-up and no pay-per-call; never ask for card
details. A deep run that pauses for points (`deep.paused`) and a news stream that closes with `paused_budget` are the
same case.

## 429

`data.limit` says which limit: `requests_per_minute`, `requests_per_day`, `heavy_per_minute` (search, candles),
`points_per_minute` (a runaway brake on spend), `ai_concurrency`, `stream_connections`, `news_stream_connections`,
`autopilots`. Honour `Retry-After`.

| Plan | req/min | req/day | heavy/min | points/min | analyses at once | streams | news streams | keys | news delay |
|---|---|---|---|---|---|---|---|---|---|
| Free | 60 | 1,000 | 10 | 5 | 1 | 1 | 0 | 1 | 30 min |
| Starter | 120 | 20,000 | 30 | 30 | 2 | 2 | 0 | 3 | 30 min |
| Plus | 300 | 100,000 | 90 | 80 | 3 | 5 | 1 | 10 | live |
| Pro | 600 | 500,000 | 180 | 300 | 10 | 10 | 3 | 50 | live |

## 426

`{"code": 426, "data": {"reason": "skill_outdated", "minimum_version": "1.0.12", "current_version": "1.0.12", "skill_url": "https://www.simianx.ai/SKILL.md"}}`

Your cached skill is older than the API allows. Re-read `skill_url`, then retry the request with the new version in
`X-SimianX-Skill`. `GET /v1/skill` always answers (it is the update path) and lists the changelog and deprecations.
Before that point the API only nudges: a response from a skill behind the current version carries
`data._skill_update = {"current", "yours", "url", "notes"}` and a first line in `notify`; take the new file from
https://www.simianx.ai/SKILL.md and tell the user in one line that the skill was updated.

## Keys

- Scopes: `data:read`, `analysis:run`, `automation:manage`, `keys:manage`, `billing:manage`. `keys:manage` is never a
  default; the user ticks it on the approval page only when they want an agent to manage their keys, and an agent
  uses it only on the user's request. A key may create keys (`POST /v1/keys`) only within its own scopes. Agents
  never receive `billing:manage`.
- `GET /v1/keys`, `GET /v1/keys/{id}` (with 30-day usage), `PATCH /v1/keys/{id}` (name, budgets, scopes, expires_at,
  ip_whitelist), `DELETE /v1/keys/{id}` (revoke, on request). The token is returned once at creation.
- `GET /v1/usage?days=7` → requests and points by key, endpoint and day.
- Send `Idempotency-Key` on POST / PATCH / DELETE to make retries safe (24 h replay, `X-Idempotent-Replay: true`,
  never charged again; a replayed key creation never repeats the token, a webhook its secret). A retry that arrives
  while the first call still runs answers 409 `request_in_progress` (`Retry-After: 3`). Over MCP, pass
  `idempotency_key` in the tool arguments. Details in `references/developers.md`.
- `webhook_endpoints` (Free 0, Starter 2, Plus 5, Pro 10) caps `POST /v1/webhooks`.
