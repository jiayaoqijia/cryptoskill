---
name: crypto-daily-brief
version: 1.0.0
author: Hermes Agent
license: MIT
description: "Use when building a daily crypto market brief."
triggers:
  - riset pagi crypto
  - morning brief
  - brief harian btc
  - daily market recap + pdf
metadata:
  hermes:
    tags: [crypto, research, daily-brief, pdf, chart, cron, news]
    related_skills: [crypto-portfolio-advisory, hermes-cron-automation, agent-reach-channels]
---

# Daily crypto market brief

## When to Use

User asks for a recurring market read: "riset pasar crypto tiap pagi", "news BTC 24 jam + verdict",
"kasih screenshot chart + link berita + pdf", or asks to fix/extend the brief that already runs at 06:00.
Not for portfolio allocation questions → `crypto-portfolio-advisory`. Not for cron mechanics in general →
`hermes-cron-automation`.

## The pipeline that exists (reuse it, do not rebuild)

| Piece | Path |
|---|---|
| Data + chart + PDF + JSON | `~/.hermes/scripts/crypto_morning_research.py` |
| Output per day | `~/.hermes/data/morning_research/<YYYY-MM-DD>/{chart_btc.png, brief.pdf, data.json}` |
| Cache global mcap/BTC.D | `~/.hermes/data/morning_research/cache_global.json` |
| Cron | `Crypto Morning Brief 06:00`, `script: crypto_morning_research.py`, deliver `origin` |

Run it directly and read stdout before scheduling anything:

```bash
timeout 180 python3 ~/.hermes/scripts/crypto_morning_research.py 2>&1 | head -20
```

Sections, in order: macro (total mcap, BTC.D) → BTC snapshot (24j/7j/30j, position in 30d range, EMA20/50/200,
funding, OI) → mechanical verdict with the reason list → top 10 mcap → 24h news digest → `FILES` line.
Every section is failure-tolerant: a dead source prints an ERROR line instead of killing the run.

## Rules that make the output trustworthy

1. **The verdict is mechanical and its reasons are printed.** Score from position vs EMA20/50/200, 24j/7j
   momentum, RSI, funding. Never let the chat message invent a verdict the data does not support, and never
   drop the reason list — the user checks the reasoning, not just the label.
2. **Every news item carries its real link.** Dedup across feeds, tag which coin each item is about. A digest
   without links is unfalsifiable, and this user is comparing it against another agent that produces prose.
3. **Numbers come from the run, not from memory.** If a section errored, say which source failed. Padding a
   failed section with numbers from yesterday's read is the one unforgivable failure here.
4. **Chart is drawn from klines, not screenshotted from a website.** matplotlib candlestick + volume + EMA,
   `dpi=165`, dark facecolor — a rendered chart survives the PDF embed and stays legible at 90 dpi.
5. **Verify generated artifacts before announcing them.** `pymupdf` opens the PDF, prints page count, image
   count per page and text length; render page 1 to PNG and actually look at it. A PDF that exists but shows a
   broken image or a cut-off table is not delivered.

## Scheduling shape (delivery is the hard part)

Cron prompt must be self-contained and must own the delivery, because nobody can answer a cron question:

- Tell the agent the script output is injected above and to build the message from it.
- Fix the shape: verdict line → BTC snapshot → 2–3 lines on top-10 winners/losers → 4–5 news items with links
  → one "yang gw pantau hari ini" line with concrete levels (7d low, EMA20d).
- Bullets use `•`, never `-` (user preference, applies to every chat deliverable).
- End the message with **two `MEDIA:` lines using the paths verbatim from the `FILES` line** (PNG then PDF).
  Without that instruction the job runs, produces files, and delivers text only.
- Cap length (~22 lines before attachments) so the brief stays a morning brief.
- Fire the job once right after creating it (`cronjob_manage action=run`) and label it `UJI COBA` in the prompt,
  so attachment delivery is proven end-to-end before the first real 06:00 send.
- The first fire may report a `Script Error` while still delivering text: the cron runner's `/usr/bin/python3` does
  not carry the tool venv, so `import matplotlib` dies there. The script must self-heal (probe
  `~/.hermes/tools/python-*/bin/python3` and `os.execv` the first one that imports matplotlib) — see
  `hermes-cron-automation`. Prove the fix by running the script with `/usr/bin/python3` explicitly, not with the
  session python; only then is the 06:00 path clean.
- Quote the daily token cost from `~/.hermes/cron/usage_audit.jsonl` (`total_tokens` for the job_id), not from
  intuition. The floor for a script-plus-short-message job is ~40k; a brief like this lands ~60–90k when the
  script succeeds, and a run that had to debug a broken script costs ~200k. Say which number you measured and
  which one you expect.

## Pitfalls

- **CoinGecko 429 is per-IP and sticks for hours.** Do not read it as "source down": `/v1/tickers` and
  `/v1/global` on CoinPaprika are keyless and generous, and they cover price, 24h/7d/30d change, mcap, volume
  and BTC.D in one or two requests. Send a browser `User-Agent` (Paprika 403s without one), keep CoinGecko as
  fallback, and cache the last good global so a bad morning degrades to a labelled `stale` line.
  Pindah sumber lengkapnya ada di skill `crypto-portfolio-advisory`, file
  `data-source-fallback-ladder.md` bagian 1 (CoinGecko 429 → CoinPaprika → cache).
- **A feed that returns 200 is not a feed that has items.** Parse, dedup, and print the count; if the digest is
  short, say "cuma N item" instead of silently shipping three.
- **Scheduling without a test run wastes a morning.** The first failure is almost always the delivery step
  (no `MEDIA:` lines, wrong absolute paths), not the data step.
- **Do not turn the brief into a trading call.** Levels and what to watch belong in it; position sizing and
  allocation belong to `crypto-portfolio-advisory`, and the brief must not restate stale advice from the day before.
