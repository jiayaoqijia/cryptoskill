# Auditing cron token burn (which job is expensive, what to trim)

Use when the user asks to rank cron jobs by cost, find waste, or "make this more efficient".
Answer from the real accounting log — never estimate from schedules.

## Sources of truth

| Path | What it gives |
|---|---|
| `~/.hermes/cron/jobs.json` | Job definitions. Dict `{jobs:[...], updated_at}`. **A job's key is `id`, NOT `job_id`.** |
| `~/.hermes/cron/usage_audit.jsonl` | One JSON per **LLM run**: `ts, id, prompt_tokens, completion_tokens, total_tokens, duration_ms, error, deliver_target, model`. Only agent jobs appear. |
| `~/.hermes/cron/executions.db` | SQLite, 1 row per fire (incl. `no_agent` scripts). Columns: status/claimed/started/finished/error. **No token columns.** |
| `~/.hermes/cron/output/<job_id>/<ts>.md` | Full transcript of each agent run: prompt, injected script context, then the agent's answer after the `## Response` heading. |

`no_agent` script jobs never appear in `usage_audit.jsonl` → they are **0 tokens**. Say that explicitly:
their cost is wall-clock / I-O / rate-limit risk, not tokens. (In this profile 35 active jobs, only 5 burn tokens.)

## Gotchas that bit

- Token fields can be `null` → use `r.get(k) or 0`, not `r.get(k, 0)`.
- Row key varies: newer rows use `id`, older use `job_id` → `r.get("id") or r.get("job_id")`.
- `sqlite3` CLI may be absent; use Python's `sqlite3` module inside `execute_code`.
- **Do NOT judge usefulness with `grep -l '[SILENT]' output/<job>/*.md`** — the prompt body itself contains
  the literal `[SILENT]` instruction, so EVERY file matches (100% false positive). Extract the answer instead:
  `awk '/^## Response/{f=1;next} f' file.md`. An empty Response = run errored/blank.
- Job IDs in the audit that aren't in `jobs.json` are deleted jobs — historical residue, label them `?`.
- A single run of 1–3.6M tokens is usually an agent that looped on web fetch + price APIs; look at `duration_ms`
  too (a 1800s run = likely timeout).

## Recipe

```python
import json, collections, datetime
rows = [json.loads(l) for l in open(f"{HOME}/.hermes/cron/usage_audit.jsonl") if l.strip()]
jobs = json.load(open(f"{HOME}/.hermes/cron/jobs.json"))["jobs"]
name = {j["id"]: j.get("name") for j in jobs}
meta = {j["id"]: (j.get("schedule"), bool(j.get("no_agent")), j.get("state"),
                  bool(j.get("enabled")), j.get("enabled_toolsets")) for j in jobs}
g = lambda r, k: r.get(k) or 0
agg = collections.defaultdict(lambda: {"n":0,"tt":0,"dur":0,"err":0})
for r in rows:
    a = agg[r.get("id") or r.get("job_id")]
    a["n"] += 1; a["tt"] += g(r,"total_tokens"); a["dur"] += g(r,"duration_ms")
    a["err"] += 1 if r.get("error") else 0
for jid, a in sorted(agg.items(), key=lambda x: -x[1]["tt"]):
    print(jid, a["n"], f'{a["tt"]:,}', f'{a["tt"]//max(a["n"],1):,}', a["err"], name.get(jid,"?"), meta.get(jid))
```

Then bucket by recency (last 14d) for the *current* burn, and by schedule to project per-day
(`runs/day × avg_tokens`). Report share-of-total — one runaway job usually dominates.

## Efficiency patterns, ranked by impact (observed)

1. **Script-gate the agent invocation.** Deterministic fetch + diff → only invoke the LLM when there is
   genuinely something new. A feed-watcher that ran the agent every 3h at ~740k tok/run (~5.9M/day, 8×/day)
   collapses to ~0 on "nothing new" ticks. Biggest single win.
2. **Pre-run script injects compact context, agent only formats** (the `script:` field). Proven cheaper by
   ~10×: a job fed a pre-computed data block ran ~120k tok vs ~740k when the same job did all fetching
   inside its own tool loop.
3. **Cut cadence.** Halving frequency halves cost immediately; do this when A/B aren't wired yet.
4. **Fix content-moderation kills.** Runs dying with `HTTP 400: Content Exists Risk` (provider rejected the
   scraped text) were ~38% of one job's fires. Fix by moving raw scraping into the script and passing clean
   text, or pinning that job to another model — not by retrying.
5. **Keep `enabled_toolsets` minimal** and cap the tool loop; each tool result re-sends the whole growing
   context (prompt_tokens dominate total).
6. **Merge duplicate collectors** that hit the same upstream feed (two scripts pulling the same RSS).
7. **Relax 2-min collectors** (720 fires/day) to 5 min: 0 tokens but heavy I-O + scrape-block risk.

## Reporting shape (this user)

Casual Indonesian, gw/lu; a ranked table (job, runs, total tok, avg/run, ≈/day) from the audit log;
then an opinionated "least useful" verdict backed by real output (e.g. count of reports whose verdict was
"nggak relevan ke posisi lu"); then the fix list ordered by impact with estimated savings. State the data
source up front so the numbers are auditable. Don't close with "mau gw buatkan?" — state the priority
action and offer "gas" to execute.
