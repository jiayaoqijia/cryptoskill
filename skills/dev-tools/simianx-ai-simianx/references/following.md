# Following a run

Everything a run produces for the user (a finished analyst, a decision, a matched news story) is written by the
server as one **update** for your key, with a sentence (`say`) in the request language and, when a question goes with
it, an `ask`. You read updates from one feed, relay them, and ack them. The numbers in the table are fixed.

## The feed: `GET /v1/updates`

```
GET /v1/updates?ack=<id>&after=<id>&wait=30&limit=50&kinds=decision,next_run&notify=1
```

| Param | Meaning |
|---|---|
| `ack` | the id of the last update you **relayed to the user**. Every unacked update up to it is acked and never sent again |
| `after` | only ids above this (default 0: everything still unacked) |
| `wait` | 0–30 s: hold the request until an update exists |
| `limit` | ≤ 100 (default 50) |
| `kinds` | comma list of kinds (below) |
| `notify` | `1`: only updates the user must hear (`notify_user: true`) |

```json
{"code": 200,
 "notify": "Tell the user each update above now, then call GET /v1/updates?ack=912&wait=30 again …",
 "data": {"updates": [
    {"id": 911, "kind": "indicator_done", "notify_user": true,
     "say": "Technicals on BTC (15m): bullish — price reclaimed the 20 EMA with rising volume.",
     "ask": null, "data": {"agent": "indicator", "symbol": "BTC", "timeframe": "15m", "analysis_id": "…"},
     "next_run_at": null, "source": {"type": "live", "id": "<session id>"}, "event_id": "…", "created_at": "…"},
    {"id": 912, "kind": "decision", "notify_user": true,
     "say": "Decision on BTC (15m): open long. Entry 61000–61200, stop 60200, target 63000, confidence 7/10. …",
     "ask": "Do you want me to connect your exchange and place or manage this order for you?",
     "data": {"action": "open", "side": "long", "entry_low": 61000, "entry_high": 61200, "entry_type": "limit",
              "stop": 60200, "target": 63000, "confidence": 7, "invalidation": "close below 60200", "timeframe": "15m",
              "expires_at": "…", "market": "crypto", "symbol": "BTC", "analysis_id": "…", "rationale": "…"},
     "next_run_at": "2026-10-23T01:15:00Z", "source": {"type": "live", "id": "…"}, "event_id": "…", "created_at": "…"}],
   "cursor": 912, "pending": 0,
   "next_step": "Tell the user each update above now, then call GET /v1/updates?ack=912&wait=30 again …"}}
```

Semantics:

- Updates come oldest first and **stay until acked**. Reading sets nothing but `fetched_at`; only `ack` acks. A crash
  between reading and relaying therefore resends the same rows; an acked row never returns. Ack with the id of the
  last row you relayed, on your next call: `?ack=912`.
- `cursor` is the last id in the page; `pending` is how many `notify_user` rows still wait after it (page again at
  once when it is above 0).
- `notify_user: false` rows are bookkeeping for code (ticks, config echoes); relay only `notify_user: true`.
- The feed is per key: it holds the runs this key started (and its news watches). It costs no points.
- Every other response you get while rows wait carries `data._pending = {"count": n, "url": "/v1/updates?wait=30"}`
  and a first line in `notify` telling you to relay them. Do that first.

## Kinds

| kind | from | what to tell the user |
|---|---|---|
| `deep.started` | deep | the committee started, how many analysts |
| `deep.analyst_done`, `deep.researcher_done` | deep | one line each: who, stance, confidence, headline |
| `deep.debate_start`, `deep.debate_done` | deep | round n of m opens on topic X (A vs B) / round n closed: who prevailed, one line |
| `deep.verdict` | deep | the full plan: rating, confidence, entry range, stop, target, reasons, risks |
| `deep.report` | deep | the PDF link (`data.url`) |
| `deep.paused`, `deep.stopped`, `deep.error` | deep | say it; `paused` is the points exception (see SKILL.md Rules) |
| `fundamental_done`, `indicator_done`, `intelligence_done` | quick · live · autopilot | one line each |
| `decision` | quick · live · autopilot | the full plan + the `ask` (exchange / broker) |
| `next_run` | quick · live · autopilot | when the next analysis runs (`data.when`, ISO; say it in the user's time zone) |
| `session_start`, `session_end` | live | session running / ended (`data.reason`: `stopped`, `agent_left`) |
| `autopilot.started`, `autopilot.stopped`, `autopilot.paused` | autopilot | one line |
| `position.changed` | autopilot | the simulated book moved: one line |
| `news`, `news.burst` | news watch | the `say` line; on high value also the `ask` (offer a quick read) |

## The table

| Run | How to check | Interval | Longest wait | Stop when |
|---|---|---|---|---|
| Deep research | `/v1/updates`, or `GET /v1/analysis/deep/{id}/events?after=<cursor>&wait=30` | call again the moment a call returns; no long-poll available → **every 10 s exactly** | 30 min (about 10 in practice) | `deep.report` (or `deep.stopped` / `deep.error` / `deep.paused`) |
| Quick read | `/v1/updates`, or `GET /v1/analysis/quick/{id}?wait=30` | same | 10 min (1–2 in practice) | status `done` / `partial` / `failed` |
| Live session | WebSocket frames; `/v1/updates` to catch up | WebSocket as frames arrive; HTTP fallback every 10 s exactly | until stopped | `session_end` |
| Autopilot | `/v1/updates`, or `GET /v1/autopilots/{id}/events?after=…&wait=30` | same | until stopped | `autopilot.stopped` / `autopilot.paused` |
| News watch | `/v1/updates` | same | until deleted | the watch is deleted |

Rules that go with the table:

- Never shorten a timeout. When the longest wait passes and the run is still open, start the same wait again and
  tell the user "still running, I keep watching". Never exit silently.
- Every time you are woken, process **all** new updates (from the cursor) before you wait again.
- If the user asks "how is it going?" in the middle, relay what finished and was not yet relayed, then answer.
- When you start following, say one sentence ("started; I will tell you each step as it finishes"). No technical
  detail, no points.

## One progress = one exit

Agents that run background commands and are woken only when the command **exits** (Grok Bot, dots, Muse and
similar) cannot relay step by step with a command that waits for the whole run: nothing wakes them in between. The
command must exit on every new update. `scripts/follow_run.py` in this repository does exactly that (Python 3,
standard library only; copy it to the agent's computer):

```
export SIMIANX_API_KEY=simx_live_…
python3 follow_run.py updates --ack <last id>        # the feed: all runs of this key
python3 follow_run.py deep <id>                      # one deep run, by its events
python3 follow_run.py quick <id>                     # one quick read
python3 follow_run.py live <id>                      # one live session (HTTP fallback)
python3 follow_run.py autopilot <id>                 # one autopilot
```

Behaviour, verbatim for the task you schedule:

> Run `python3 follow_run.py updates --ack <id>`. It exits with code 0 and the new updates on stdout (one JSON line
> each: `id, kind, say, ask, next_run_at, data`) as soon as there is one, 2 after 60 s of nothing, 3 when every run
> is over. On 0 tell the user each line, then re-run with the `ACK=<id>` printed on the last line. On 2 re-run at
> once. Never set a shorter timeout than 60 s; never stop re-arming while a run is open.

Options: `--interval 10` polls every 10 s exactly instead of long-polling (for networks that cut long requests),
`--max 60` is the longest one invocation waits (default 60 s), `--until-idle` makes `updates` exit 3 when the feed
is empty and nothing is pending. The last line is always `ACK=<id>`: pass it back next time.

Agents that can hold a connection (Claude Code, Codex, a bot you wrote) do not need the exit trick: keep the
long-poll loop, the SSE stream (`stream=1`, resume with `Last-Event-ID`) or the WebSocket open and relay each item.

## Per-run endpoints (the same updates, scoped to one run)

- Deep: `GET /v1/analysis/deep/{id}/events?after=<cursor>&wait=30` → `data.events[]` with `type`, `step`, `agent`,
  `say`, `notify_user`, `next_step` (and `stance`, `verdict`, `topic`, `index`, `result` where they apply), `data.cursor`,
  `data.status`, `data.busy`. `stream=1` for SSE.
- Quick: `GET /v1/analysis/quick/{id}?wait=30` returns as soon as **any** agent finished since your last call
  (`data.run.results` per agent, `data.run.analyses[]`, `data.next_candle_close_at`).
- Live: the WebSocket (`references/live.md`); `GET /v1/live/sessions/{id}` for the state.
- Autopilot: `GET /v1/autopilots/{id}/events?after=<cursor>&wait=30` (`references/autopilots.md`).

Whichever you use, the rows also sit in `/v1/updates` until acked, so the feed is the one place that never loses
anything after a cut.
