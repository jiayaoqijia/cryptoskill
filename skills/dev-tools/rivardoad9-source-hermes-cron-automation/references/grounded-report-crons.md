# Grounded report crons (collector script → LLM writer)

Pattern proven 2026-09-27 building the daily 20:00 "Trade Radar" job (`7ecff29f4af2`,
collector `~/.hermes/scripts/trade_radar.py`, ~10 s, read-only).

## Why split it

An LLM-only report cron re-derives numbers with tools every run (slow, and it eventually invents
one). A collector script fixes the numbers; the agent's job becomes judgment + prose. The user's
requirement — "jangan ngasih signal aneh-aneh, kalau nggak ada ya bilang nggak ada" — is only
enforceable when the raw data (including "there is nothing here") is already on the table.

## Shape of the collector

- One function per section, each in try/except, failures appended to a `notes` list printed as the
  last section: `[8] CATATAN DATA  ! meteora page 3 err …`. A run with a dead source still produces
  a usable report that *says* what is missing.
- Print compact aligned text (this goes straight into the prompt) **and** dump JSON to
  `~/.hermes/data/<job>_latest.json` for later reuse.
- Keep a state file (`<job>_state.json`) with the previous run's snapshot per candidate so the next
  report can say "Δvs lalu: mcap +…, holder −…, liq +…" instead of re-describing yesterday.
- Header line must carry the timestamp and the instruction:
  `=== TRADE RADAR DATA — 27 Sep 2026 20:28 WIB ===` /
  `(bahan mentah untuk laporan trade 20:00; SEMUA angka dari sini, jangan dikarang)`.

Section list used here: `[1] HOLDINGS` (delegate to the existing watchdog script with `--debug` and
reuse its lines), `[2] NEWS 24 JAM`, `[3] SMART MONEY & KOL`, `[4] LP SEHAT vs HINDARI`,
`[5] LOW CAPS + security`, `[6] COIN BARU (new launches)`, `[7] FLOW (whale + liquidations)`,
`[8] CATATAN DATA`.

## Prompt blocks that carry the weight

1. Grounding rule + failure honestc: *"SEMUA angka di laporan HARUS dari output itu. Jangan
   mengarang angka/harga/berita/nama proyek. Kalau ada baris '!' di catatan data, sebutkan singkat
   bagian mana yang kosong."*
2. Null outcome authorized: *"Jangan memaksa sinyal. Pasar adem / tidak ada setup = jawaban 'malam
   ini nggak ada yang layak' + 2-3 alasan. Itu jawaban yang benar dan dihargai."* Plus: never
   recommend an item the collector already listed under "HINDARI".
3. Named forbid list: no leverage; any news claim must rest on a news line in the output.
4. Repeat handling: *"Kalau kandidat yang sama dibahas beberapa hari berturut-turut dan belum
   bergerak, tulis 'masih dipantau (hari ke-N)' alih-alih mengulang analisis penuh."* (pairs with
   `continuity=true`).
5. **FAKTA YANG WAJIB DIPEGANG (jangan dibalik)** — the fix for the CLARITY error below. Content of
   the block is a list of *verified current statuses* with dates, e.g.:
   - CLARITY Act **failed cloture 15 Sep 2026 (49–50)**, no new vote scheduled → never present as a
     positive regulatory catalyst; live catalysts are X, Y, Z instead.
   - Token supply/unlock facts (circulating %, inflation, cliff size + date).
   - Any dated event the report keeps referring to (buyback start date, etc.).
   Then the meta-rule: *"Kalau menyebut berita, dasarnya harus baris news di output script."*

## The failure this prevents (2026-09-27, first delivered run)

The collector's news section pulled in a headline whose keywords included "clarity act". The writer
turned that into "Regulasi makin ramah (Clarity Act, SEC) → angin positif buat ONDO" — factually
wrong (the bill had died 12 days earlier) and directly contradicting the thesis work done earlier in
the same session. Symptom to watch for generally: **keyword-to-conclusion drift** whenever the
collector passes raw headlines through to the writer.

QA loop that caught it: `read_file ~/.hermes/cron/output/<job_id>/<ts>.md` → compare each number to
the collector output (all correct) → compare each *claim* to known-verified facts (one wrong) →
patch the prompt with the hard-facts block. Do this on the first run of every new report cron.

## Related

- Silent-threshold watchdog sibling (same session): `holdings_watch.py` on `*/15`, `no_agent=true`,
  prints only when a threshold trips, per-alert cooldowns in state JSON. See
  `silent-and-dedupe-patterns.md` and `watchdog-design-and-testing.md`.
- Watchdog/digest/radar split for the same subject matter: watchdog 15 m (silent), digest 08:00
  (numbers + news), radar 20:00 (opportunity hunting). Three separate jobs, one collector each —
  do not merge them into one giant prompt.
