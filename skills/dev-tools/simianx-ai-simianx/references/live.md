# Live analysis, once

The four live agents run one pass on a symbol, no schedule, no paper position. Good for "what do the agents think of
SOL on the 1H right now".

`POST /v1/analysis/live` (scope `analysis:run`, metered; `typical_points` in the answer)

```json
{"asset": "crypto", "symbol": "SOL", "timeframe": "1H", "tier": "fast",
 "agents": ["indicator", "intelligence", "fundamental", "decision"], "language": "en"}
```

Answer `202`: `data.run.id`, `status: queued`, `poll_url`. Then

`GET /v1/analysis/live/{id}?wait=30` → holds up to 30 s until the run ends (`done | partial | failed`) and returns
`run.results` per agent (`status`, `analysis_id`, `points`) and `run.analyses[]` (agent, timeframe, model, conclusion,
points). `?include=text` adds the full write-ups. `GET /v1/analysis/live?limit=20` lists recent runs.

Stock runs use the market data plane and are not available while the US market is closed in some environments; the API
answers 503 `stock_live_unavailable` in that case.

## Models

`tier` (`fast | standard | frontier`) picks one model for every agent; `models` `{"indicator": "<id>", "decision": "<id>"}`
overrides per agent on paid plans. Ids and prices come from `GET /v1/models` (`live.crypto`, `live.stock`,
`models[].typical_points_per_call` per agent); an id outside the catalogue for that market is refused with 400 and
`data.allowed`. Free accounts run every agent on `free_model`, whatever they send.
