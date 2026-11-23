# Threshold-gated daily digest cron (collector + LLM writer, TWO output modes)

Proven 2 Okt 2026 building "Deep Dive Harian — narasi & setup (ambang 8/10)"
(job `f73edbbd7416`, `0 8 * * *`, script `deep_dive_daily.py`, deliver origin, continuity=true).

## The user-facing rule that drives the design

User first asked: *"deep dive tiap hari, filter dulu, minimal conviction 8/10 — kalau kurang jangan
dikasih gambarannya."* Then refined it: *"kalau gada paling kayak lu bilang aja belom ada, dan kasih
gambarannya berupa narasinya apa dan potentialnya gmn."*

→ The gate suppresses the **full report**, not the **message**. Two modes:

- **Mode A** (best candidate >= threshold): full report + chart attachment.
- **Mode B** (nothing >= threshold): short (~900 char) message — "belum ada yang lolos 8/10" + the
  day's highest score and what it failed on + **narrative map with real numbers** + dated catalyst
  potential + one line on what we're waiting for. No chart.

**Do NOT wire the `[SILENT]` convention into a research digest.** `[SILENT]` is for watchdogs
(`agent-run-silence-and-backfill-rules.md`); a "no qualifying setup" day still owes the user the
landscape paragraph. When a user asks for a threshold, ask/confirm which axis the gate closes —
the picture, or the message.

## Architecture: why collector + writer (never LLM-only)

- **Collector** `~/.hermes/scripts/<job>.py` (no LLM, ~40 s for 7 sections):
  - one function per section, each in `try/except` appending to a `NOTES` list printed last as
    `[7] CATATAN DATA` with `!` prefix — a run with a dead source still produces a usable report
    that *says* what is missing;
  - compact aligned text on stdout (this goes straight into the prompt) **plus** JSON dump to
    `~/.hermes/data/<job>_latest.json`;
  - rolling state `~/.hermes/data/<job>_state.json` (last ~14 snapshots) so the writer prints
    delta-vs-yesterday instead of re-describing every day;
  - never exits non-zero on total failure — print the note and `sys.exit(0)`, or a crashed collector
    silently kills the whole job.
- **Writer** (agent) does judgment + prose only. Prompt must say: *"SEMUA angka HARUS dari output
  collector ini, jangan mengarang. Baris `!` di catatan data = sebutkan bagian yang kosong."*

### Collector sections that worked (crypto flavour, reusable shape)

| # | Section | Source pattern |
|---|---------|----------------|
| 1 | narrative heat / cold | `coingecko.com/api/v3/coins/categories`, filter `market_cap >= 50e6` |
| 2 | narrative members | `/coins/markets?category=<id>&per_page=12&price_change_percentage=24h,7d,30d` |
| 2b | **exchange movers** | `binance.com/api/v3/ticker/24hr`, keep `quoteVolume >= 5e6`, drop stablecoins + `UP/DOWN/BULL/BEAR` + `1000`-prefixed |
| 3 | attention | `gmgn-cli market hot-searches --chain sol --interval 24h --limit 30` |
| 4 | smart-money signals | `gmgn-cli market signal --chain sol --groups '[{"signal_type":[12]}]'` |
| 5 | CEX technicals | `klines?interval=1d&limit=200`: pos in 90d range, MA30/MA90, vol7/vol30, distance to 90d/365d high |
| 6 | delta vs previous run | read state file, print `harga ±% · pos90 a→b · vol7/30 x→y` |
| 7 | data notes | every failed source, `!`-prefixed |

Field notes that mattered:
- `/coins/markets` rows for RWA/stablecoin-ish categories have **$0 volume** — filter members by
  `total_volume >= 1e6` or the "top narrative" is 12 untradeable vault tokens.
- A giant category (Tokenized Assets/RWA) can top the 24h leaderboard purely by composition — tell
  the writer to read it as rebalancing, not as a new narrative.
- GMGN signal payload carries the risk fields that make filtering mechanical:
  `rug_ratio`, `is_honeypot`, `is_wash_trading`, `top_10_holder_rate`, `suspected_insider_hold_rate`,
  `top70_sniper_hold_rate`, `smart_degen_count`, `renowned_count`, `holder_count`, `liquidity`.
  Its `volume_24h`/`swaps_24h` came back **0** for most rows — don't sort by them, sort by
  `smart_degen_count` / `market_cap`.
- CoinGecko free tier 429s: retry with escalating sleep (4s → 8s → 12s) and record the failure in
  notes rather than dying.

## Make the threshold mechanical (rubric + hard disqualifiers)

Score 0-10 so a writer can't rationalise a 6 into an 8:
`0-3` dated & fresh catalyst · `0-3` technical structure (range position, MA alignment, volume trend)
· `0-2` liquidity & access · `0-2` risk/overhang.
**Auto-disqualify (score capped at 5):** honeypot or wash-trading true, rug_ratio > 0.5, DEX pool
liquidity < $500k, breakout with 7d/30d volume ratio < 1.0, no dated catalyst, or already +60% in 7
days (chasing).

## Catalyst freshness rule (added after a real miss)

"Find a catalyst" is not enough. First delivered run scored a token 8/10 citing an automated-buyback
mechanism as the live catalyst — the mechanism is real, but it went live ~4 months earlier and was
presented as if it were news. Hard rules now in the prompt:

- every catalyst needs **a date AND a named source** (media/blog name — "internet" doesn't count);
- catalyst older than ~45 days → state its start date and **cut the score**; stale ≠ fresh;
- undated / unverifiable catalyst = **0 points** and cannot carry the threshold.

Then **spot-check the delivered run's claims yourself** with web_search before trusting the output
(both claims in that run were real — the defect was freshness framing, not fabrication).

## Chart attachment (Mode A only)

Use a generic spec-driven generator (see `rendered-chart-qa.md` in the chart skill) instead of
hand-writing SVG per run: JSON spec in → PNG + machine-readable summary out
(`price, ma30, ma90, pos90, dist_high90, vol_ratio, levels[].pct, ok, content_ratio`).
Prompt rule: *the generator's printed numbers are the official ones for the report and must match the
prose*; if `ok=false` or `content_ratio` outside range, don't send the image. If the ticker has no
USDT pair on the exchange → send text only, never substitute a different ticker to have something to
show.

## Verification loop that actually catches problems

1. `~/.hermes/cron/output/<job_id>/<ts>.md` → read the `## Response` tail. Confirm the mode matches
   the score and that numbers match the collector output (the prompt/collector header are also in
   there, so you can diff).
2. Append-only decision log `~/.hermes/data/<job>_log.md`, written by the agent:
   `- <tgl WIB> | mode A <TICKER> / mode B | skor <x/10> | <1-line reason>`. This is what you read
   when the user later asks "how were the last few days".
3. Stat the delivered PNG and the vault note the job claims to have written — agent self-reports.
4. First run of any new report cron always needs this QA pass; a leak on run 1 is a **prompt** bug,
   not a job bug — patch the prompt, re-run, don't create a second job (`seen`/state would fork).

## Tightening a long prompt without re-sending it

Once the prompt is several KB and you only need a small rule change, patch
`~/.hermes/cron/jobs.json` directly (see `jobs-json-direct-injection.md`): back up → load JSON →
find the job by **`id`** → `str.replace` on `job['prompt']` → dump `ensure_ascii=False, indent=2`.
Then verify the new rule is present **and** that `schedule`, `enabled`, `next_run_at` survived.
