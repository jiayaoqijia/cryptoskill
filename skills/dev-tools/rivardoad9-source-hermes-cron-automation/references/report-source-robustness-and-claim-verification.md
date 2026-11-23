# Report-cron source robustness & claim verification

Companion to `threshold-gated-daily-digest.md` and `grounded-report-crons.md`. Lessons from the
2 Okt 2026 "Deep Dive Harian" build + the two verification passes the user demanded afterwards
("ini bener kah"). Applies to any collector→writer report cron, not just crypto.

## 1. A source can fail "successfully" — catch the silent zero

Minutes apart in the same session, CoinGecko `/coins/categories` returned HTTP 200 with
`market_cap_change_percentage_24h = 0.0` for **every** row, while the exchange-native data showed the
hot sector at **+22%**. A writer handed that zero writes "no narrative heat anywhere" — a
plausible-looking, completely wrong conclusion, and nothing in the notes says the source died.

- Treat *all rows identical / all zero / all null* as a **dead-source signal**, and say so in the
  notes section: `if rows and all(abs(r[k]) < 1e-9 for r in rows): note("<source> balik 0.0% semua ->
  section [N] TIDAK VALID, pakai [fallback]")`.
- Tell the writer in the prompt which sections are load-bearing when the primary is degraded:
  *"Kalau [1] balik 0.0% semua atau ada `!` 429 di catatan data, JANGAN pakai [1], andalkan [1b]+[2b]."*

## 2. Keep an independent backbone from a second source class

Don't let one aggregator be the only read on "what narrative is hot".

- Add an **exchange-native sector bucket**: take the raw mover list (already fetched for the
  gainers/losers section), classify each symbol with a hand-written symbol→theme map, print
  `theme | n | mean 24h | total vol24 | top members`.
- Map-design rule: broad map, accept misses. An extra/wrong symbol simply never matches, so the map
  **cannot fabricate a number** — much safer than fuzzy matching on names. Drop themes with `< 3`
  members (one mover is not a narrative).
- Section order that survived review: `[1]` aggregator heat → `[1b]` exchange sector buckets →
  `[2b]` raw gainers/losers. With `[1]` degraded, `[1b]+[2b]` still answer "where is the money", and
  the two sources cross-check each other (they matched: sector +22.7%, mean of 8 members).

## 3. Exchange API gotchas that cost real debugging

- `/api/v3/ticker/24hr` **without params** (full list, ~2k rows, one call) then filter
  `symbol.endswith("USDT")` is the robust way to price a mixed watchlist.
- `?symbols=[...]` returns **HTTP 400 when *any* symbol in the list is invalid** — one
  delisted/renamed/never-listed ticker kills the whole batch. This is what broke the first two
  attempts. If you must use it, URL-encode the JSON as well; raw `"` and `[` also produce 400.
- Per-symbol `klines` calls are ~0.3 s — a 40-symbol funnel inside a ~60 s collector is fine.

## 4. Keyword-drift attribution is systemic — grow a hard-facts block

Delivered run listed "the LayerZero bridge exploit" as an *overhang of the candidate token*. The event
is real ($292M rsETH, April 2026, DPRK RPC poisoning) but belongs to a different protocol entirely —
the writer grabbed a headline keyword and welded it onto today's candidate. Same class of failure as
the Clarity Act miss in `grounded-report-crons.md`: **raw headlines passing through the writer drift
from keyword to conclusion.**

Countermeasure that worked (cheap): a `FAKTA YANG WAJIB DIPEGANG (jangan dibalik)` block in the
prompt, listing verified current statuses with dates, each phrased as a prohibition:

- "exploit X (April 2026, protocol Y) — JANGAN dikaitkan ke token lain dan JANGAN dipakai sebagai
  katalis/overhang baru";
- "unlock Z tanggal W → jangan pernah disebut katalis positif";
- the *real* dated overhang for the token that keeps getting mis-attributed (e.g. venue delistings
  with their dates) so the writer has something true to reach for instead.

**Grow this block every time a delivered claim turns out wrong.** Also require a named source per
external claim inside the *short* digest mode too — that is where drift hides, because short output
gets less scrutiny than the full report.

## 5. Answering "ini bener kah" — verification scorecard, not a re-summary

The user re-asks this about anything the job delivered. The wanted shape:

1. **Re-pull the numbers from the primary source** and print report-value vs live-value side by side
   (exchange ticker/klines beat any aggregator). State the small deltas honestly — intraday drift of
   1-2% between capture and check is fine and worth saying; a mismatch is a finding.
2. **web_search every external claim** (catalyst, exploit, delisting, unlock) and mark each
   ✅ verified + source name, or ❌ wrong/stale/unsourced. Verify the *date* as well as the fact — a
   true event from months ago presented as a fresh catalyst is still a defect.
3. **Name the defects explicitly, then name what changed** to prevent a repeat (prompt rule, new
   collector section, hard-facts entry).
4. Lead with a count: "8 dari 9 bener, 1 salah" — then the list. A clean re-narration of the report is
   not an answer to this question.

Corollary for the daily job itself: treat the first N delivered runs as needing this QA pass, and
prefer patching the prompt over creating a second job (splits the state/`seen` files).
