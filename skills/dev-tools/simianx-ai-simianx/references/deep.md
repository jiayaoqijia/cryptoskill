# Deep research (the 8-agent committee)

Analysts (fundamentals, market, news, timing for stocks / derivatives for coins), bull and bear researchers, a research
manager who runs a debate, and a risk manager who writes the verdict and the plan. About ten minutes on our workers;
you follow it and tell the user every step as it lands. A PDF report closes the run; the user also receives it by
email, which you need not mention.

## Start

`POST /v1/analysis/deep` (scope `analysis:run`, metered)

```json
{"asset": "stock", "symbol": "NVDA", "horizon": "swing", "tier": "fast", "language": "en"}
```

- `horizon`: `short | swing | long`. `agents`: optional subset (the manager and risk manager are always seated).
- Free accounts: only the free lists (stocks: AAPL MSFT GOOGL AMZN TSLA NVDA META NFLX AMD QQQ; coins: BTC ETH SOL XRP DOGE BNB),
  fast tier only. Others → 403 `plan_required`.
- Answer `201`: `data.id`, `status: queued`, `events_url`, `next_step` ("keep following this run …").
- Say one sentence: "The committee has started on NVDA; I will report each analyst as it finishes." Nothing about
  points or the estimate.

## Follow, and what to tell the user

Either from the feed (`GET /v1/updates?ack=…&wait=30`, `references/following.md`) or from the run's own events:

`GET /v1/analysis/deep/{id}/events?after=<cursor>&wait=30` → `data.events[]`, `data.cursor`, `data.status`, `data.busy`.
Each event carries `type`, `step`, `agent`, and for everything the user should hear a `say` sentence and
`notify_user: true`; `data.next_step` says what to do now. `stream=1` for SSE (resume with `Last-Event-ID`).
Call again the moment a call returns (or every 10 s exactly where long-polling is impossible); longest wait 30 minutes.

The order, and the one line you say at each step (the server's `say`; paraphrase lightly if you like):

| Event | Update kind | Say |
|---|---|---|
| `run` | `deep.started` | "The committee started on NVDA: 4 analysts are working in parallel." |
| `step_done` for `agent:fundamentals`, `agent:market`, `agent:news`, `agent:timing` (crypto: `agent:derivatives`) | `deep.analyst_done` | "Fundamentals analyst finished: bullish (confidence 72/100) — data-centre revenue still accelerating." |
| `step_done` for `agent:bull_researcher`, `agent:bear_researcher` | `deep.researcher_done` | "Bear researcher finished: bearish (confidence 61/100) — valuation leaves no room for a miss." |
| `step_start` for `disc:topic:0`, `disc:topic:1`, … (`topic`, `index`) | `deep.debate_start` | "Debate 1 of 3 opens: 'Is the data-centre growth already priced in?' — Bull researcher vs Bear researcher." |
| `topic_done` (`index`, `result`) | `deep.debate_done` | "Debate 1 closed: the bull side prevailed. Guidance history outweighs the multiple." |
| `step_done` for `verdict` (`verdict`) | `deep.verdict` | "Risk manager's verdict on NVDA: buy (confidence 72/100). Entry 118–124, stop 109, target 150. Reasons: … Risks: …" |
| `step_done` for `report` | `deep.report` | "The full report is ready as a PDF: https://…pdf" |
| `paused` (`reason: no_points`) | `deep.paused` | the points exception: say the account's points ran out and give the renew / change-plan links; the run resumes with `POST …/resume` once points are back |
| `stopped`, `error` | `deep.stopped`, `deep.error` | say it |

Not relayed on their own: `disc:plan` (the agenda) and `disc:vote` (the vote) fold into the first debate's start and
the last debate's end; `charge` events are bookkeeping; the streamed text (`delta`) and per-tool progress (`tools`) are
left out unless you ask with `include=`.

Example of what the user reads during one run, in order: started → four analyst lines → two researcher lines →
"Debate 1 opens …" → "Debate 1 closed …" → (2 and 3 the same) → the verdict with the full plan → the PDF link.
Never collapse these into one message at the end; never wait to be asked.

## Read the result

- `GET /v1/analysis/deep/{id}` → `status` (queued | running | paused | stopped | failed | done), `progress.done` (steps),
  `members[]` (agent, done, stance, confidence, headline), `verdict` (rating buy|hold|sell, confidence, headline, horizon,
  entry_low, entry_high, stop, target, reward_risk, reasons[], risks[]), `report_url`, `outcome` once done.
  `?include=text` adds each member's full write-up and `verdict_text`.
- `POST /v1/analysis/deep/{id}/pdf` → `url` (watermarked on free accounts). Always give the user the link.
- `POST /v1/analysis/deep/{id}/stop` stops a run; `POST …/resume` continues a paused one.

## After the verdict

- `POST /v1/analysis/deep/{id}/ask {"message": "...", "mentions": ["news"]}` → `qid` and a cursor; the answer streams as
  `chat_*` events; `GET /v1/analysis/deep/{id}/thread` lists questions and answers. Offer this: "ask the committee a
  follow-up, or ask one member by name".
- `GET /v1/analysis/deep?limit=20` lists recent runs with their rating.

## Models

`tier` or `models` `{"<committee agent>": "<id>"}` (paid plans) choose the committee's models; the agent names are in
`GET /v1/models` (`deep.agents.stock` / `deep.agents.crypto`) and the ids in `deep.models`. An unknown id is 400
`invalid_parameter` (`parameter: models`).
