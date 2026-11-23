# Token & cost audit of a Hermes install

Use when the user asks "what are you doing all day", "which task burns the most tokens", "how do we make this
cheaper", or before/after any efficiency change (record the numbers so the next audit can compare).

Run `scripts/token_usage_audit.py` for the standard view; hand-write the SQL below when you need a cut it does
not print.

## Where the numbers actually live

`$HERMES_HOME/state.db` — SQLite. The `sqlite3` CLI is frequently not installed; use stdlib `sqlite3` from
`python3` and open it read-only so a live gateway never blocks:

```python
con = sqlite3.connect("file:/home/ubuntu/.hermes/state.db?mode=ro", uri=True)
```

Tables that matter:

- `session_model_usage` — one row per session × model × task: `api_call_count`, `input_tokens`, `output_tokens`,
  `cache_read_tokens`, `reasoning_tokens`, `estimated_cost_usd`, `task`.
- `sessions` — one row per session: `source` (`telegram`, `cron`, …), `title`, `started_at` (unix seconds),
  `message_count`, `api_call_count`, and the same token columns.
- `system_prompts` (`hash`, `prompt`) — the fixed per-call prompt; `len(prompt) / 3.6` approximates its tokens.

## The five cuts that answer the question

```sql
-- 1. everything, ever
SELECT sum(api_call_count), sum(input_tokens), sum(output_tokens), sum(cache_read_tokens)
FROM session_model_usage;

-- 2. per day (server local time; adjust the '+7 hours' offset to the host TZ)
SELECT date(started_at,'unixepoch','+7 hours') d, count(*), sum(message_count), sum(api_call_count),
       sum(input_tokens), sum(output_tokens), sum(cache_read_tokens)
FROM sessions WHERE started_at > strftime('%s','now') - 30*86400
GROUP BY d ORDER BY d;

-- 3. worst sessions (title tells you what the marathon was)
SELECT id, source, title, message_count, api_call_count, input_tokens, output_tokens, cache_read_tokens
FROM sessions
ORDER BY (coalesce(input_tokens,0)+coalesce(cache_read_tokens,0)+coalesce(output_tokens,0)) DESC LIMIT 12;

-- 4. the scheduled fleet's slice
SELECT count(*), sum(input_tokens), sum(output_tokens), sum(cache_read_tokens)
FROM sessions WHERE source='cron' AND started_at > strftime('%s','now') - 30*86400;

-- 5. by work type — this is where the surprise usually is
SELECT coalesce(nullif(task,''),'(main turns)'), count(*), sum(api_call_count),
       sum(input_tokens), sum(output_tokens), sum(cache_read_tokens)
FROM session_model_usage GROUP BY 1 ORDER BY 5 DESC;
```

Per-call context size = `cache_read_tokens / api_call_count` for a task row. That single ratio is the number to
attack in main turns.

## How to read it (rules, not vibes)

- **Volume is not the bill.** `cache_read` is the cheapest token class by a wide margin, so raw totals overstate
  money. Report the split, say that out loud, then argue from proportions — those do hold.
- **Measure the cron fleet before blaming it.** Scheduled jobs are usually `no-agent` script jobs that spend
  ZERO LLM tokens; a fleet of dozens of jobs can be a low single-digit percentage of usage. Do not propose
  throttling schedules until cut 4 proves cron is actually material — and if the numbers kill that theory, say so.
- **Main turns are normally the hog** (well over half). The cause is structural: every API call re-sends the
  whole history plus the system prompt plus every tool schema, so long sessions get quadratically worse, and an
  average context above 100k tokens per call is normal in a long one. Levers, in order: start a NEW session per
  project instead of continuing a marathon; keep huge output on disk (have a script print a summary rather than
  reading a 20k-character file into context); let compression run.
- **The one line item with a clean knob is the post-turn review fork** (`task='background_review'`), which is
  spawned to update memory and skills. The source comment estimates ~30K tokens per event; the stored numbers
  routinely come out many times higher, because each fork loops with its own tool calls. Its cost lands in whole
  sessions, so per-event cost = that session's total, not per API call.
- **Cron never pays for that fork** — cron runs are constructed with `skip_background_review=True`.

## Cost of ONE action ("kalau gw lempar link ke bot X, boros token ga?")

The whole-install cuts above answer "what burns the most", not "is THIS action cheap". Measure one
action as a delta on the LANE's own DB: run it exactly once, snapshot before and after. One
`hermes -p <profile> chat -q "<the action>"` starts a FRESH session, so the delta IS that action's
marginal cost.

```python
q = ("select coalesce(sum(api_call_count),0), coalesce(sum(input_tokens),0),"
     "coalesce(sum(cache_read_tokens),0), coalesce(sum(output_tokens),0) from session_model_usage")
con = sqlite3.connect("file:/home/ubuntu/.hermes/profiles/<p>/state.db?mode=ro", uri=True)
```

- **`session_model_usage.last_seen` is a Unix epoch FLOAT, not ISO text.** A filter like
  `where last_seen > '2026-10-14'` (or `substr(last_seen,1,10)`) matches nothing and comes back as
  an EMPTY result, which reads as "no usage" instead of an error — you will misread it as a broken
  DB. Compare against `time.time() - days*86400`. (`sessions.started_at` is epoch seconds too, so
  that one wants `date(started_at,'unixepoch')`.)
- `input_tokens` (fresh, billed) and `cache_read_tokens` (cheap) are separate counters — a large
  prompt is not a large bill. The billed driver is `output_tokens` + `reasoning_tokens`, so a lane
  that reasons long costs like a main turn however small its documents are.
- Measured reference points on this install, enough to answer a per-action question in one shot: a
  capture persona replies ~330 output tokens per call against ~1.270 on the main analysis lane; one
  X link = ~16 calls / 9,7k fresh input / 7,9k output / 100 s; one long article = ~10 calls / 9,5k
  fresh input / 3,9k output / 85 s. One main-lane user turn normally runs 10-30 calls / 25-75k
  tokens, so a routed action is roughly a third to a fifth of it — and it runs in the LANE's own
  session, which is the bigger saving: the main chat's context does not grow.
- Answer shape for "boros ga": the action's own numbers, the comparison against one main-lane turn,
  the structural win, then the single habit that keeps it cheap (one item per message instead of a
  batch dump, short replies). Answer in tokens — a custom provider reports `estimated_cost_usd` 0,
  so do not invent a dollar figure.

## Knobs

Set them with `hermes config set KEY VALUE`; never hand-edit `config.yaml`.

| Key | Effect |
|---|---|
| `memory.nudge_interval` | iterations between memory-review forks (default 10) |
| `skills.creation_nudge_interval` | iterations between skill-review forks (default 15) |
| `compression.threshold`, `compression.target_ratio` | how early history is compressed |

Raising the two nudge intervals cuts review frequency roughly proportionally; `0` disables the automatic review
entirely, at the cost of skills/memory only changing when explicitly asked. Offer that trade-off explicitly
instead of applying it silently.

## Report shape this user wants

Ranked by share, every line carrying a real number, one honest caveat about cache pricing, then three or four
ranked levers each with its trade-off — and name the suspicion the data killed, not only the one it confirmed.
Close by offering to apply the top lever and re-measure in a week.
