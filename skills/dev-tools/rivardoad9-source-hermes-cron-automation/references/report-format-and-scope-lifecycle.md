# Report format & scope lifecycle (recurring report jobs)

Companion to `grounded-reports-crons.md` — that file covers the collector→writer data pipeline; this one
covers what happens *after* the first report ships: the user reacts to the format, changes the scope, and
you have to evolve the job without breaking grounding.

Proven on the daily 20:00 "Trade Radar" job (`7ecff29f4af2`) over one evening of iteration, 27 Sep 2026.

## 1. When the user dislikes the format, offer templates — don't tweak blindly

Do not re-send the same shape with one word changed. Build 3–4 candidate templates and let them choose:

- Render every template **with real, verified data**. Illustrate per-item blocks with a candidate whose
  numbers were already verified earlier in the session (here: a token with a dated, verified catalyst).
  **Never invent placeholder figures to demonstrate layout** — this user reads invented numbers as
  fabrication, even in a mock-up.
- Put each template in a fenced block so the platform renders it literally, then one line per option on
  what it optimises for (scanability / narrative depth / information density / brevity).
- State your recommendation explicitly, and expect a "campur" answer (e.g. card layout + one table from a
  different option). Ask which parts to mix; don't guess.

## 2. Locking the chosen format into the prompt

The prompt must pin all of this, or the writer drifts back to prose within two runs:

- exact section order and the emoji/label headers;
- the sub-line labels inside an item block (e.g. `Tesis : / Angka : / Risiko : / Entry : / Exit :`);
- per-section caps **and** a total length ceiling;
- **what may be cut when over budget** — "potong yang paling tidak penting — jangan potong angka
  entry/exit/size". Cutting rules matter more than the ceiling: a writer told only "max 20 lines" will
  drop the numbers that make the report actionable.
- rendering rules: **no markdown tables, no code blocks** on Telegram (tables don't render, alignment
  collapses), separators `·` / `|`, abbreviated money (`$84,9k`, `$2,4M`), one consistent symbol
  spelling per report (a run wrote "NEARPAD/NEARCAT" in one section and "NEARKAT" in another).
- a fallback block for the empty case (0 candidates), so a quiet night still produces the chosen shape.

## 3. Removing a segment is three edits, not one

The user cut the LP segment ("yang pool LP ga perlu sih, fokus gw lg ga disna"). The next report still
described a holding as *"masih di daftar HINDARI, cov 11,3×"* — vocabulary inherited from the section it
had been told to ignore. Leakage shows up in the *rest* of the report, not in the removed section.

1. Decide whether to keep collecting it (cheap sections: keep, so it's available if focus returns).
2. Tell the prompt to ignore that section **and its terminology**, naming the forbidden words explicitly.
3. Name the substitute source for anything that used to come from it — "untuk peringatan PAID pakai harga,
   mcap, likuiditas dari bagian [1] saja".

Then re-fire and grep the delivered report for the retired vocabulary before calling it done. Also re-check
the prompt's `[N]` section references after any collector edit: a stale index is how "ignore section 4"
quietly becomes "ignore nothing". When a sleeve/segment is dropped for the user's *investment* focus too,
record that on the advisory side (see `crypto-portfolio-advisory`) — the report change follows the focus
change, not the other way round.

## 4. Test-fire budget

Every `cronjob action='run'` sends a real message to the user's chat. One evening of format iteration
consumed three fires — about the ceiling. Fire once per *meaningful* change (new pipeline, scope change,
final format), never for cosmetic micro-edits; batch the small stuff and let the scheduled run prove it.
With `continuity=true` the test reports also become the "previous run" baseline the next real run diffs
against — fine, but know that it happens.

## 5. QA every first-of-its-kind run from the output file

`read_file ~/.hermes/cron/output/<job_id>/<ts>.md` — not the delivered copy. Check, in order:
numbers vs collector output → claims vs known-verified facts → presence of retired vocabulary → line
count vs the cap → whether the empty-case block fired correctly. The one factual error caught this way
(keyword-to-conclusion drift: a dead bill reported as a live catalyst) is written up in
`grounded-reports-crons.md`; the QA pass is what caught it, so it is not optional.

## 6. Collector pitfalls that reach the report

- **Timestamp filters that silently no-op.** These local alert DBs store `ts_utc` as ISO-8601 strings
  (`2026-09-27T12:23:22+00:00`), not epoch ints — a `WHERE ts_utc > ?` bound with an `int(time.time())`
  cutoff returns **every** row, so a "24 jam" section printed whale transfers from a month earlier. Bind
  an ISO cutoff string and add `AND sym IS NOT NULL AND usd IS NOT NULL` to drop news rows sharing the
  table. Sanity-check each time-windowed section against the newest timestamp it prints.
- **Mislabeled units propagate as confident nonsense.** A section printed `umur {age_days:.1f}h` for a
  value already in days — a 2-day-old token read as "1.7h". Re-read labels whenever a section is added.
- **Dump CLI output shape before writing the parser.** `gmgn-cli market trending` errors without
  `--interval` and returns `{"data":{"rank":[...]}}`; `market trenches` returns
  `{"completed":[],"near_completion":[],"new_creation":[]}` at top level. Sample `--limit 1 --raw`, print
  top-level keys, and keep parsers tolerant (try several key names) so a shape change degrades into a
  "catatan data" note instead of a crash.

## Related

- `grounded-reports-crons.md` — collector shape, prompt blocks, hard-facts block, the CLARITY failure.
- `crypto-portfolio-advisory` → `references/low-cap-token-triage.md` — analysis method for the low-cap
  segment such reports tend to carry.
