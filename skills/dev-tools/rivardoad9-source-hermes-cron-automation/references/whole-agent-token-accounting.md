# Whole-agent token accounting ("boros token ga kita?")

Companion to `token-burn-audit.md` (which covers **cron runs** via `~/.hermes/cron/usage_audit.jsonl`).
Use this when the user asks about the *whole* agent's burn — chat + cron + subagents — instead of one job.
The answer is usually counter-intuitive: the chat, not the cron fleet, dominates.

## Fleet view first

```bash
hermes insights --days 7     # sessions, msgs, tokens, platform split, top tools, top skills
```

It prints a platform table (e.g. `cron` vs `telegram` sessions/tokens) — enough for a first cut — and
`Cost: Unknown (no pricing data)` for custom `base_url` providers (a DeepSeek endpoint, etc). **That is
expected, not a bug**: report tokens, and label any $ figure as an *assumed* price sheet, never as measured.

## Session store (the real breakdown)

`~/.hermes/state.db`, table `sessions`. Useful columns:
`source, title, model, started_at, message_count, tool_call_count, api_call_count, input_tokens,
output_tokens, cache_read_tokens, cache_write_tokens, reasoning_tokens, estimated_cost_usd, cost_status`.
(`session_model_usage` has the same counters split per model/task.)

```python
import sqlite3, time
c = sqlite3.connect(f"{HOME}/.hermes/state.db")
now = time.time()
def agg(src, days):
    return c.execute("""select count(*), sum(input_tokens), sum(output_tokens),
        sum(cache_read_tokens), sum(api_call_count), sum(estimated_cost_usd)
        from sessions where source=? and cast(started_at as real) > ?""", (src, now - days*86400)).fetchone()
for s in ("cron", "telegram", "cli", "subagent"):
    n, fin, fout, cache, api, cost = agg(s, 7)
    print(f"{s:<9} sesi={n} fresh_in={fin or 0:,} out={fout or 0:,} cache_read={cache or 0:,} "
          f"TOTAL≈{(fin or 0)+(fout or 0)+(cache or 0):,} api={api or 0} est=${cost or 0:.2f}")
```

- Cron session ids look like `cron_<job_id>_<yyyymmdd>_<hhmmss>`; `title` = `<job name> · <Mon DD HH:MM>`.
  A per-entity research run costs ≈700k tok (≈92k fresh in + ≈9k out + ≈616k cache read) — the loop's tool
  results re-sent as cache are what make the number look big.
- Per-job rollup: group by `re.sub(r'\s*·.*$', '', title)`, then cross-check the name against
  `cron/jobs.json`; names no longer there are **deleted jobs** — label them "sudah dihapus" and exclude them
  from the current-burn table (their old runs can still dominate a 7-day sum).
- `source='subagent'` captures delegated work; check it before blaming cron.

## Pitfalls (all hit in one session)

- **`started_at` is an epoch *string*, not a datetime** (`'1791217349.9154'`). A `where started_at >
  datetime('now','-7 days')` filter matches **nothing and returns an empty result set** — no error, no
  warning, and it reads like "no sessions". Always `cast(started_at as real) > time.time() - days*86400`.
- **Divide by 1e6** when applying a `$/M tok` price. Forgetting it turns ~$14/week into ~$13M/week; sanity
  check the magnitude (a personal VPS agent is single-digit $/day) before it reaches the user.
- **Separate `cache_read_tokens` from fresh input before judging.** 90–96% of a long-running profile's total
  is cache reads, billed at a fraction of input price. A scary total is usually long-context chatter, not new
  work — say so instead of quoting the headline number.
- Don't rank "boros" by total tokens alone; rank by fresh input + output first (that's the billable work),
  then mention cache as context.

## Verdict shape (this profile, Oct 2026)

7 d ≈ 310M tok total, but only ~9.5M fresh input + ~3.3M output. **Chat ≈ 94% of the burn** (a long Telegram
session re-sends ~100k cached context *every turn*; 7 sessions, 2,699 API calls), **cron ≈ 6%** (~18M; of 68
jobs, 55 are `no_agent` = 0 tokens and only 5 recurring agent jobs burn anything). Highest-leverage lever is
therefore **a new session per topic** (`/new` drops per-turn context ~100k → ~30k, ≈$24/mo in the assumed
price sheet) — not trimming crons.

Reporting: verdict first ("gak boros; yang makan chat, bukan cron"), then the fresh/out/cache split, then the
price assumption **labelled as an assumption**, then the one lever that matters, then the priority action +
"gas". Never answer a cost question with a single alarming total, and don't close with "mau gw buatkan?".
