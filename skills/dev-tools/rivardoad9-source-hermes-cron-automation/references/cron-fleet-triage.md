# Cron fleet triage: making the whole schedule effective (verified 5 Oct 2026)

Class of ask: *"apa aja cronjob lu skrng, gw pengen lu saring dan bikin lebih efektif"* — audit the
whole fleet, not one job. Companion to `token-burn-audit.md` (cost ranking + efficiency patterns);
this file is the **triage workflow and the traps that make a healthy lane look worthless**.

Order of operations that worked (64 jobs, 34 active → 28 active):

1. `cronjob action=list` for the surface view (id, state, schedule, `last_status`, `no_agent`).
2. Token burn from `usage_audit.jsonl` (see `token-burn-audit.md`). Reported share-of-total first:
   **one job was 67% of all burn** (a paused X-watch at 695k tok/run, 6 errors).
3. Silence forensics on the `no_agent` majority (below) — this is where the real answers were.
4. Classify every active job: deliverable-now / muted-upstream / broken / redundant.
5. Execute only the reversible, no-judgement-needed fixes; hand the judgement calls to the user.
6. Report: ranked table + what was already done + the "need your OK" list.

## Trap 1 — the output dir is a pruned window, so it cannot prove "never"

`~/.hermes/cron/output/<job_id>/` keeps only ~50 `.md` files. That is ~4 hours for a `*/5` job,
~25 hours for `*/30`, ~2.5 weeks for a 3×/day digest — so "0 non-silent files out of 50" means almost
nothing on a fast lane. Before writing "NEVER alerted", cross-check the lane's durable evidence:
`~/.hermes/data/<lane>.last` (scripts log `<ts> | n kartu`), `*_ledger.jsonl`, `*_outcomes.jsonl`,
`call_ledger.jsonl`, `<lane>.log`, and the lane DBs (`lowcap_alert.db`, `sm_watch.db`).
Phrase findings as "no hit in the last N hours", never a flat "never".

`no_agent` silence IS visible in those md files — the header of a silent run says
`**Status:** silent (empty output)`. And a `(no response section)` / `len=21` "response" in an md file
means the job is a `no_agent` script job, **not** an error and not a blank agent run; real agent rows
read `len=2000+`, and an agent lane whose last 8 responses are `[SILENT]` is genuinely producing nothing.

## Trap 2 — a silent lane is a DELIVERY question before it is a usefulness question

Six jobs kept scanning ~651×/day (LowCap P2/P3, EarlyWatch, EarlyWatch Track, SmartMoney registry +
lane) producing exactly nothing the user could see, because the receiving bot was muted upstream:
sentinel `~/.hermes/data/memebot_off` ("dimatikan atas arahan user; cara balikin: rm …") and
`~/.hermes/data/alert_push.log` (1400+ rows) reading `MATI | dimatikan (MEMEBOT_PUSH off)` for
**every** fire since 30 Sep — 1 002 muted pushes, 0 delivered.

So the diagnostic order is: read the push log → find the sentinel → then decide relight vs pause.
The fix is **pause the producers** (or relight the channel) — never loosen the lane's own filter, which
would make the script lie about why it is quiet. Leave the lane's SQLite/ledger files in place so the
measured track record survives a later relight.

## Trap 3 — level/entry-zone lanes flap at the boundary (duplicate alerts, no delta)

A delta-gated zone lane (`in_zone` boolean per symbol) sent the user **4 identical `masuk ZONA ENTRY`
alerts in 4.5h at the same price** (XRP, band 1.42–1.50, $1.4977–1.4999). The documented rule
"re-arm once price is back above the band top" was implemented literally (`px > hi`) and is not enough:
one tick at/above the top resets the latch, the next tick below re-arms it. Fix: re-arm only after a
**real departure** — `px > hi * 1.02` (~2% margin). See
`references/level-crossing-entry-zone-alerts.md`. Count crossings in the output md files; the state file
will look perfectly correct while the user is being spammed.

## Trap 4 — job sehat, yang dia awasi sudah tidak ada

`last_status: ok` hanya berarti scriptnya exit 0. Periksa **objek yang dia jaga**, bukan job-nya:

- **Monitor posisi** (LP manual, holdings): buka registry-nya. Registry kosong (`positions: []`,
  `updated_at` berbulan lalu) = job memindai daftar kosong 288×/hari. Biaya penuh, manfaat nol.
- **Keeper server/watchdog**: `curl -s -m 3 -o /dev/null -w "%{http_code}" http://127.0.0.1:<port>/` untuk
  tiap port yang dijaga. Semua 200 berarti keeper-nya benar tapi intervalnya berlebihan — 5 menit untuk
  server yang tidak pernah mati cukup 30 menit (hemat 240 fire/hari per job).
- **Watch level harga**: bandingkan level dengan harga sekarang (API) dan dengan posisi user. Level yang
  sudah 20% jauh sementara koinnya tidak lagi dipegang = sisa lane lama.
- `failure_streak > 0` di `jobs.json` = gagal beruntun, bukan gangguan sesaat; silangkan dengan
  `cron_incidents`. Error yang isinya "payload X tidak ditemukan di halaman" berarti sumbernya berubah
  struktur — matikan job-nya, jangan tambah retry.

## Menghitung beban: dari jadwal, bukan dari tabel eksekusi

`executions.db` adalah jendela bergulir ~1000 baris, jadi `WHERE started_at > <7 hari lalu>` tetap
mengembalikan tepat 1000 dan tidak bisa dipakai untuk volume harian. Hitung dari ekspresi cron:

```python
def cnt(tok, total):      # "*/5" -> 288/hari di kolom menit; "8-22/2" -> 8 di kolom jam
    ...                   # tangani *, */N, a-b, a-b/N, dan daftar berkoma
runs_per_day = cnt(menit, 60) * cnt(jam, 24)
```

Total fleet = jumlah `runs_per_day` semua job aktif. Itu angka yang dipakai untuk bilang "31% beban cuma
buat health-check", bukan kira-kira.

Dua sumber lain yang sering disalahpakai:

- **`jobs.json`** berbentuk `{"jobs": [...], "updated_at": ...}`. Job aktif = `enabled: true` **dan**
  `state: "scheduled"`; filter `state == "active"` mengembalikan nol job. Pause = `enabled: false`.
  **`schedule` bukan string** — sekarang objek `{kind: "cron"|"interval", expr, display, tz}`, jadi
  regex 5-field harus dibaca dari `schedule.expr` dan job `every 3h` cuma punya `schedule.display`.
  Regex langsung ke `j["schedule"]`, atau iterasi `jobs.values()` padahal `jobs` itu list, bikin hasilnya
  nol fire / `KeyError: 0` padahal fleet-nya ramai — cek `type()` sekali sebelum menghitung.
- **Jawaban "cron job lu brp skrg" = satu script, empat angka:** total, aktif (`enabled` true), paused,
  dan fire/hari (jumlah `runs_per_day` job aktif) plus 3 job paling rajin. Itu yang dia baca; daftar 56 nama
  tidak. Sebutkan job yang baru dibuat di sesi itu secara terpisah karena dia biasanya nanya efek perubahan
  yang baru saja kita lakukan.
- **`deliveries.db`**: `job_json` dan `content` tersimpan kosong setelah terkirim, jadi tidak bisa
  diatribusikan per job. Yang bisa dikutip cuma total + rentang tanggal (`MIN/MAX(created_at)`),
  mis. "573 pesan dalam 14 hari".

## Efficiency: a tool budget inside the agent prompt

For an agent job that is *wanted* but hunts (Deep Dive: ~517k tok/run, "nothing passed the bar" on 3 of
4 recent runs), the cheapest fix is a hard budget in the prompt, anchored beside the step that already
names the injected collector data:

```
⛔ BUDGET ALAT (efisiensi): all prices/narratives/structure are ALREADY in the injected collector
output — do not re-fetch what you were given. Verify at most 1–2 top candidates and max N web calls
(web_search/web_extract) per run. If the budget runs out without a verified dated catalyst → go
straight to the SHORT mode today. Then write the final report; no re-checking the same data.
```

Keep the daily short report — this user requires "belum ada yang lolos" to be delivered, not silence
(`references/agent-run-silence-and-backfill-rules.md`), so `monitor_script` suppression is the wrong
tool here; the budget is.

## Executing the changes safely

- **Schedule changes go through the `cronjob` tool** (file-side `schedule.expr` edits leave the daemon
  registry stale — `references/cron-schedule-edits-and-doc-bloat.md`); do tool calls first, then
  prompt edits in `jobs.json`, which the scheduler picks up.
- **Back up `jobs.json` before any file surgery** (`cp jobs.json jobs.json.bak_<date>_preprune`), assert
  the anchor string exists before replacing, and confirm the edit landed by re-reading the field.
- **Pause, don't delete** on the first pass: paused jobs cost 0 tokens and keep their prompts (which are
  the valuable, hand-tuned part). Offer the delete/prune list as a separate "gas" step.
- **After an explicit "gas", delete in one batch and verify the FLEET, not each command.** `state:
  "completed"` one-shots (reminders that already fired) are always removable — they can never fire again.
  Loop `hermes cron remove <id>`, then assert: `hermes cron doctor` → "Checked N active job(s)" matches
  the arithmetic, no `next_run_at` sits in the past after the schedule edits, and the recomputed
  run/day total actually dropped by the predicted amount. Every command can print success while the
  total stays put if one id was wrong.
- **Interval changes from a terminal: `hermes cron edit <id> --schedule "*/30 * * * *"`** — same registry as
  the tool, so no daemon desync (unlike editing `schedule.expr` in the file). Quote the expression. A
  keeper going 5 → 30 min cuts 240 fires/day per job; state the tradeoff out loud (worst-case detection
  delay equals the new interval) so the user can veto that one job.
- **Re-test a patched script before leaving** (`python3 <script>` → exit 0, silent when nothing crossed).
- Cadence relaxation is the zero-risk dial for collectors with no logic change: `*/5` → `*/10`
  halves fires (576 → 288/day) with no data loss risk.

## Report shape (this user)

Casual Indonesian gw/lu: state the data source up front, one ranked table, then three blocks —
**what was already executed** (numbered, with the evidence number), **what was found but is waiting for
"gas"** (each with the fix and why it matters), and the priority action. Don't close by asking
"mau gw buatkan?" — name the priority and offer "gas".

## Splitting the fleet across bot lanes ("biar ga semua di sesi ini")

Class of ask: the user wants the cron output split per bot/chat because it feels like everything lands in
one DM. Procedure:

1. **Measure who actually SPEAKS before restructuring anything.** `~/.hermes/cron/executions.db` carries the
   delivery verdict per fire — the one fleet-wide silent-vs-posted measure:

   ```sql
   select delivery_outcome, count(*) from executions group by 1;
   -- per job: join jobs.json names, filter delivery_outcome='delivered'
   ```

   `suppressed`/`suppressed_acked` = the run happened and posted nothing (watchdog/collector with no change).
   A fleet of ~60 jobs typically shows only a handful of `delivered` rows. Report that ratio first: it
   reframes the ask from "move 60 jobs" to "move the N that actually speak", and "everything lands in my
   chat" is usually a misread of the fire count.
   Caveat: `executions` is itself a rolling ~1000-row window (~8 hours for a fleet running `*/5` lanes), so
   read the RATIO, never an absolute per-day volume — for absolute counts use Trap 1's sources
   (`usage_audit.jsonl`, the output dir, the lane logs).
2. **Never assign a lane from `jobs.json` alone.** `deliver` says only where the *agent's final response*
   goes. Follow `script=` through its wrapper (`foo.sh` → `exec bash $HOME/<project>/bar.sh` → the python) and
   read what that script sends: a lane whose script already pushes through another bot's Bot API still shows
   `deliver: origin`. Classifying from the config field alone both invents moves that do nothing and misses
   the lanes already split. See `references/channel-redirect-push-pattern.md`.
3. **A lane that already pushes must get `deliver: local`, not a new target.** The push IS the delivery;
   leaving `origin` duplicates every message into the main DM. Do not "move" such a job — silence its agent
   response.
4. **Grouping that matches this stack:** main DM = conversational/decision jobs (deep dive, trade radar,
   portfolio + risk delta, personal reminders); news bot lane = news/flow/onchain radar; alert+perf bot lane
   = technical alerts + scorecard/performance audits; `local` = DB collectors and infra watchdogs (they have
   nothing to say — deliver is pure noise).
5. **Deliver the split as ONE decision, not a 60-row table.** Two named schemes with the job count per lane
   (safe = only the alert basket moves / aggressive = the main DM keeps only the conversational+
   decision jobs), state which one you recommend, and say you execute on his word. Counts computed in code,
   not eyeballed — the per-lane numbers are what he decides on.
6. Same pass, same reply: flag jobs with `failure_streak > 0` from `jobs.json` and the open `cron_incidents`
   rows — an alert lane failing a dozen consecutive fires for days is invisible in a
   schedule/enabled listing.

