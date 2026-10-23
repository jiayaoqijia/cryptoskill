# Quick read (one pass)

The four live agents run once on a symbol and a timeframe: indicator (the chart), intelligence (the news flow),
fundamental (the business or the coin), decision (a call with entry, stop and target). No schedule, no position. For
"what do the agents think of SOL on the 1H right now". To keep analysing, start a live session
(`references/live.md`); to keep watching while you are away, an autopilot (`references/autopilots.md`).

`POST /v1/analysis/quick` (scope `analysis:run`, metered)

```json
{"asset": "crypto", "symbol": "SOL", "timeframe": "1H", "tier": "fast",
 "agents": ["indicator", "intelligence", "fundamental", "decision"], "language": "en"}
```

Answer `202`: `data.run.id`, `status: queued`, `data.poll_url`, `data.next_candle_close_at` (ISO: when the next
candle of this timeframe closes), `data.next_step` (keep following).

## Follow

Each agent's result is an update the moment it lands (`fundamental_done`, `indicator_done`, `intelligence_done`, then
`decision`, then `next_run`), each with a `say` line: read them from `GET /v1/updates?ack=…&wait=30`
(`references/following.md`), or hold the run itself:

`GET /v1/analysis/quick/{id}?wait=30` → returns as soon as **any** agent finished since your last call (not only at
the end), with `run.status` (`queued | running | done | partial | failed`), `run.results` per agent (`status`,
`analysis_id`), `run.analyses[]` (agent, timeframe, model, conclusion) and `next_candle_close_at`. `?include=text`
adds the full write-ups. Call again until the status is terminal; longest wait 10 minutes (usually 1–2).

`GET /v1/analysis/quick?limit=20` lists recent runs.

Stock runs use the market data plane and are not available while the US market is closed in some environments; the
API answers 503 `stock_live_unavailable` in that case.

## What to say

One sentence per agent as it finishes (the `say` line). On the decision: the full plan (open or not, direction,
entry, stop, target, confidence, what invalidates it), "analysis, not investment advice", when the next candle
closes, and the question: connect the user's exchange (crypto) or broker (stock) to place and manage the order?
Then offer to keep analysing with a live session or an autopilot. No points.

## Models

`tier` (`fast | standard | frontier`) picks one model for every agent; `models` `{"indicator": "<id>", "decision": "<id>"}`
overrides per agent on paid plans. Ids and prices come from `GET /v1/models` (`live.crypto`, `live.stock`); an id
outside the catalogue for that market is refused with 400 and `data.allowed`. Free accounts run every agent on
`free_model`, whatever they send.

## The old path

`POST /v1/analysis/live` and `GET /v1/analysis/live/{id}` (skills ≤ 1.0.5) still answer the same run, with
`Deprecation`, `Sunset: 2026-12-01` and `Link: …; rel="successor-version"` headers. Use `/v1/analysis/quick`.
