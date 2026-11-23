# Changing content rules + keeping agent-read docs lean (verified 3 Sep 2026)

Companion to `jobs-json-direct-injection.md` and `jobs-json-schedule-desync.md`. Covers the
other half of this user's Threads stack: content STYLE/CADENCE rule changes and the recurring
token cost of agent-read material files.

## Content rule changes propagate to FOUR places (or they half-apply)

User changed post style 300-450 char → 150-280 char ("postingan panjang keliatan AI, ikutin
gaya gw ngomong"). The rule only actually took effect after updating ALL of:

1. **Material doc the jobs are told to read** — `~/.hermes/threads_outreach/website_material.md`,
   ARAHAN block at top (jobs: "Baca website_material.md — patuhi blok ARAHAN KONTEN AKTIF").
2. **Every content job prompt that hardcodes the old value** — promo 06:00, tips 09:00,
   Dompet 14:30 all had their own "300-450 karakter" GAYA line. A doc-only change loses to the
   job's own inline instruction.
3. **The rekap/improvement job prompt** (da9d3529fac9) — it re-states the style rule when
   instructing improvements ("dalam gaya user: lu/gw, 300-450 char") and goes stale silently.
   Hit this session: rekap still said 300-450 a day after the rule changed.
4. **strategy.md** — log the change so the next rekap can judge it.

After editing: grep doc + all job prompts for the old literal (`300-450`) and assert the count
is what you expect (0 in prompts, only "override" mentions in doc). Exact-match `assert == 1`
before every `.replace()`; a mismatch means the anchor text differs (hidden chars, wrong
substring start) — switch to a tolerant regex (`re.subn(r'\(EKSEKUSI[^)]*\)', ...)`) rather
than guessing at invisible characters.

## Agent-read file bloat is a recurring token tax

Content jobs read `website_material.md` IN FULL every run (7-17 runs/week) and the rekap job
reads `strategy.md` in full daily. Both grew unbounded because the daily rekap APPENDED a new
dated narrative block each morning (~35KB and ~53KB → ~10K and ~15K tokens per read). Fix
pattern (compressed 3 Sep 2026, ~120-130K tokens/week saved):

1. Back up full versions to `<dir>/archive/<file>_<date>_full.md` first.
2. In the material doc: delete the dated narrative blocks ("Update <tanggal>:"), replace with a
   consolidated "ATURAN AKTIF PER SLOT" section. Keep every section a job prompt references by
   ANCHOR NAME — verify after surgery that these still exist exactly once: `ARAHAN KONTEN
   AKTIF`, `FORMAT WAJIB POST DOMPET DIGITAL`, `3 PRODUK FOKUS`, `GAMBAR PRODUK`, `LINK
   WEBSITE`, `DATA EKONOMI DIGITAL`, `DASHBOARD FINANCE`, `no-ai-slop`.
3. In the strategy log: keep header/template + guardrails + only recent entries (~7 days),
   archive the rest.
4. **Embed a maintenance rule INSIDE the doc** telling the recurring improvement agent: "update
   the active block (replace date/content), JANGAN tambah blok narasi 'Update <tanggal>' baru;
   narasi & data view → strategy.md. Jaga dokumen < ~15KB." Without this, the daily agent
   re-bloats the file every morning and the compression is a one-day win.
5. Update the rekap prompt if it points at the log ("file ringkas; entri lama > X ada di
   archive/...").

## Git gotcha

The daily 03:00 auto-commit in `~/.hermes` tracks CONFIG only — business docs under
`~/.hermes/threads_outreach/` were never git-tracked (found 3 Sep 2026: two weeks of strategy
log existed only on local disk). After any large doc/cron edit run
`git add threads_outreach/ cron/jobs.json && git commit` manually — do not rely on the
scheduled backup for these files.
