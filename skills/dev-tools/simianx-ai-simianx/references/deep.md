# Deep analysis (8-agent committee)

Analysts (fundamentals, market, news, timing for stocks / derivatives for coins), bull and bear researchers, a research
manager who runs a debate, and a risk manager who writes the verdict and the plan. Runs on our workers; you follow it.

## Start

`POST /v1/analysis/deep` (scope `analysis:run`, metered; `data.estimate` is the up-front estimate in points)

```json
{"asset": "stock", "symbol": "NVDA", "horizon": "swing", "tier": "fast", "language": "en"}
```

- `horizon`: `short | swing | long`. `agents`: optional subset (the manager and risk manager are always seated).
- Free accounts: only the free lists (stocks: AAPL MSFT GOOGL AMZN TSLA NVDA META NFLX AMD QQQ; coins: BTC ETH SOL XRP DOGE BNB),
  fast tier only. Others → 403 `plan_required`.
- Quote first: `POST /v1/analysis/quote {"endpoint":"deep.create","asset":"stock","tier":"fast"}`.
- Answer: `data.id`, `status: queued`, `events_url`.

## Follow

- `GET /v1/analysis/deep/{id}` → `status` (queued | running | paused | stopped | failed | done), `progress.done` (steps),
  `members[]` (agent, done, stance, confidence, headline), `verdict` (rating buy|hold|sell, confidence, headline, horizon,
  entry_low, entry_high, stop, target, reward_risk, reasons[], risks[]), `charged`, `report_url`, `outcome` once done.
  `?include=text` adds each member's full write-up and `verdict_text`.
- `GET /v1/analysis/deep/{id}/events?after=<cursor>&wait=30` → progress events (`run`, `step_start`, `step_done`, `charge`,
  `paused`, `done`, `error`, `chat_*`); `stream=1` for SSE. The streamed token text is left out unless `include=delta`.
- A run pauses with `paused` + `reason: no_points` when the next stage cannot be covered; `POST /v1/analysis/deep/{id}/resume`
  after the points come back. `POST .../stop` stops it.

## After the verdict

- `POST /v1/analysis/deep/{id}/ask {"message": "...", "mentions": ["news"]}` → `qid` and a cursor; the answer streams as
  `chat_*` events; `GET /v1/analysis/deep/{id}/thread` lists questions and answers.
- `POST /v1/analysis/deep/{id}/pdf` → `url` (watermarked on free accounts).
- `GET /v1/analysis/deep?limit=20` lists recent runs with their rating.

## Models

`tier` or `models` `{"<committee agent>": "<id>"}` (paid plans) choose the committee's models; the agent names are in
`GET /v1/models` (`deep.agents.stock` / `deep.agents.crypto`) and the ids in `deep.models`. An unknown id is 400
`invalid_parameter` (`parameter: models`). The run is metered on the models that actually answered.
