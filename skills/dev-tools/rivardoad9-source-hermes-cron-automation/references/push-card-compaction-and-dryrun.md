# Capping what a push card SENDS (and proving a dry run stayed local)

Companion to `report-format-and-scope-lifecycle.md` (§1–6 cover format feedback loops on
LLM-written report jobs) and `alert-script-testing-safe.md` (safe testing of bash alert scripts).
This file covers the two things a **push** lane needs that those don't: how to shrink a card that
grew by printing one line per item, and how to dry-run a lane that sends through its own Bot API
token without dropping test cards into the user's alert bot.

Verified 28 Sep 2026 on the low-cap call tracker (`early_watch_track.py`, cron `*/2`,
`@memescallsbot`).

## 1. "Signal kita kebanyakan" — cap the detail, keep the totals honest

A card that prints one line per tracked item grows without bound. Measured one night of sends:
`1256 → 1832 → 2378 → 2914 → 3225 → 3312 → 3539` chars, ending at **46 lines / 3925 chars** for
29 items. User's ask, verbatim:

> *"itu kan signal kita kebanyakan tuh, paling kek lu bikinnya versi 5 terakhir aja, trus bawahnya
> tuh total brp brp tulis, kayak rata rata signal lu timeframe bla bla bla brp yg punya record bgus
> dan brp yg rug"*

"Too many" almost always means **too many SENT, not too many collected**. Split those two before
deleting anything. Working shape (46→22 lines, 3925→1420 chars, and now the length is CONSTANT as
items accumulate — only the numbers move):

```
**5 CALL TERAKHIR** dari 29 terukur (daftar penuh: `--full` · per-timeframe: <other script>)
<5 item lines>
**TOTAL 29 CALL TERUKUR**
· 🟢 masih untung (kini ≥1x): 3 (10%)
· 🔴 rug/mati (kini <1x): 26 (90%) — 9 di antaranya sempat naik ≥3x lalu ambruk
· median x kini 0.66 · rata2 x0.63 · median puncak x1.77
· terbaik **moin** x1.23 · terburuk **Heart** x0.08 _(seluruh riwayat, bukan cuma 5 di atas)_
**TIMEFRAME** _(median x dari harga saat call)_
· +15m x0.71 · +30m x0.71 · +1j x0.66 · +4j x0.53
· ⚠️ semua median ≤1x — belum ada edge di timeframe mana pun, jangan nambah size
```

Rules that make the SHORT version trustworthy — each was a real bug or a real call:

- **Newest, not best.** Sorting the visible detail by the success metric shows old winners and hides
  the one item the user can still act on.
- **Aggregates come from the FULL population**, recomputed outside the display loop. A totals block
  that sums the 5 visible rows is a new kind of lying report.
- **Median for anything an outlier can reach.** Mean peak printed `x489,2` off one junk item
  ($16 mcap, peak x14.104); the median was `x1.77`.
- **Paired percentages must sum to 100%** — compute the second as `100 − first`, or the card claims
  10% + 89% (both floored off the same 29 items).
- **Never polish "no edge"** into "almost profitable" — reuse the existing MIN_N honesty rule.
- **The full list stays reachable and the card says so** (`daftar penuh: --full`). Capping what you
  SEND ≠ hiding data.
- **Title adapts**: items ≤ cap → print `SEMUA CALL (n)`, don't say "5 terakhir" when there are 3.
- Cap lives in a named constant (`MAX_DETAIL = 5`), not a magic number inside the formatter.
- **Both push paths share the formatter** (manual `--digest` + the cron tick that pushes
  "new checkpoint" cards). One function, one fix — but test both; if the paths ever split, the
  summary silently disappears from the pushed one only.
- **Ambiguity check:** the user said "signal" while two artifacts qualified (the call scoreboard on
  the alert bot and a separate `📊 NILAI SINYAL` card from another cron). Pick the one whose body is
  a per-item list, say in the reply WHICH artifact changed, and offer one line on the other. Don't
  silently change both.

## 2. Dry-running a self-pushing lane without polluting the user's bot

When a lane sends through its **own Bot API token** (not `deliver:`), a safe dry run needs
`ALERT_PUSH=off` **plus** a redirected data dir (`EW_DATA_DIR` / `CALL_LEDGER_PATH` /
`EW_OUTCOMES_PATH` → `/tmp/...`). Then a synthetic item aged 45 minutes produced 2 real checkpoints,
the compacted card printed locally, the heartbeat file was written (`call=1 dicek=2`), and
`alert_push.log` gained no line.

Why it is not optional: the user had to delete three test cards (message_id 5, 6, 8) from the alert
bot. That bot is their measuring instrument — once it looks like it carries test noise, its numbers
stop being trusted. Prove the absence from the send log (`tail -3 alert_push.log`, no new `KIRIM`
line) rather than asserting it from stdout: these lanes are **empty-stdout on success by design**, so
"no output" is not evidence the run worked — `ALERT_PUSH=off` forces the text down the print path
where you can actually read it.

## 3. Regression check that cannot fail

Adding tests for the compacted card, one check was written as `all(<cond> for i in ())` — an empty
generator is always `True`, so it stayed green no matter what the code did. After adding a check,
prove it can go RED (temporarily break the behaviour, or assert on a value that really differs).
A selftest that cannot fail is worse than no selftest: it certifies broken behaviour.

Useful cases for a compaction change specifically: (a) exactly `MAX_DETAIL` rows printed,
(b) those rows are the NEWEST, (c) totals still count the full population, (d) paired percentages
sum to 100, (e) the pushed "fresh" variant carries the same summary block.
