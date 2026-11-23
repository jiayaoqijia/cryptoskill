---
name: lowcap-priority-alerts
description: "Alert low caps by priority tier: urgent vs normal."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
prerequisites:
  commands: [python3, curl, gmgn-cli]
metadata:
  hermes:
    tags: [crypto, alerts, low-cap, x-twitter, nitter, cron, priority]
---

# Low-cap alerts with priority tiers (P1 urgent / P2 fast / P3 normal)

Build/operate a three-lane alerting system that watches **X (Trump, gov, regulator,
influencers, fast-news accounts)** and **on-chain low caps** (GMGN hot-searches), then
delivers each event on the lane matching how fast the user must react.

## Report format (keep this standard)

One shared formatter lives in `lowcap_common.py` — **never hand-roll per-lane output**,
it drifts and the lanes stop looking like a set.

Shape every message as: **title → `_stamp_` → `RULE` → numbered cards → `RULE` → legend**.

```
📋 **P3 · BIASA** — low cap roundup
_Min 27 Sep 2026 · 23:06 WIB · 94 dilacak · 46 lolos layar dasar_
━━━━━━━━━━━━━━━━━━

**PALING RAMAI & LOLOS LAYAR**

**1.** ✅ **boar** `base`
   🎯 conviction **4.4/10** 🟠 TIPIS
      _liq 2.0 · holder 2.0 · mom 0.9 · insider 0.0 — dibatasi dari 4.9 (insider sedang distribusi)_
   mcap $1.4M · liq $331K (24.2%)
   1j -31% · 24j -31% · turnover 14%
   holder 4,187 · top10 16%
   🔍 INSIDER — 🔴 distribusi insider
   smart money 1 (kol)  ·  insider 3
      creator 1 · fresh_wallet 2
   token gratis (beli $0): 60 dari 99 holder (61%) · 23 sudah jual
   cluster wallet: 2 grup ← pindah/cuci wallet (terbesar 4 wallet, dana rentang 209 hari)
```

Rules that make it scannable on a phone:
- **One fixed 4-line card per token** (`coin_card()`): header / mcap+liq / change+turnover /
  holders+top10. Fixed columns beat one long `·`-separated line that wraps mid-number.
- Number every item `**N · KIND**` (P2) or `**N.**` (P1/P3).
- `/50M`-style thresholds and thresholds come from the constants — `usd()` and `pct()`
  avoid the ugly `$1000K` and `-0%` renderings.
- **Headline sections must only contain tokens that PASS the base screen.** Sorting the
  busiest list by raw attention once put 4 of 6 junk tokens at the top of the digest.
- Put rejects in a compact one-line **"DILEWATI"** block with the *reason*
  (`fail_reason()`), never as full cards — and never silently drop them.
- Dedupe across sections (a token shown as "busiest" must not repeat as "gaining").
- Legends: `base_screen_note()` (thresholds + ✅/⚠️ key) and `impulse_note()` for the
  >2000%/1h artifact warning.

## When to Use

Use this skill when the user asks for:
- alerts on low caps / "Trump nge-tweet" / influencer moves / "X lagi rame"
- **priority levels** on alerts (urgent/butuh-fast vs biasa)
- changes to an existing tiered alert pipeline

## Architecture (5 lane = 5 cron job, semua `no_agent=True`)

| Lane | Script | Cron | Latency | Meaning |
|---|---|---|---|---|
| **P1 · URGENT** | `lowcap_collect.py` | `*/5 * * * *` | ≤5 min | must check now |
| **P2 · FAST** | `lowcap_p2.sh` → `lowcap_alert.py --tier p2` | `*/15 * * * *` | ≤15 min | emerging, watch |
| **P3 · BIASA** | `lowcap_p3.sh` → `lowcap_alert.py --tier p3` | `0 8,14,20 * * *` | digest | awareness only |
| **EARLY WATCH** | `early_watch.py` | `*/30 * * * *` | ≤30 min | final-stretch + migrated, **gate = preset filter user** |
| **EW TRACK** | `early_watch_track.py` | `*/2 * * * *` | +15m/30m/1j/4j/24j | ukur hasil alert (ledger) |
| **SMART MONEY** | `sm_lane.sh` → `sm_lane.py` | `*/20 * * * *` | ≤20 min | ikut jejak wallet ber-record (diukur sendiri) |
| **SM REGISTRY** | `sm_watch_cron.sh` → `sm_watch.py --run --quiet` | `*/10 * * * *` | — | collector jejak wallet (silent) |
| **WINNER STUDY** | `winner_study_cron.sh` → `winner_deepdive.py --brief` | `30 8 * * 1` | mingguan | deep dive pola winner vs loser SEMUA lane + uji saring kriteria (30 Sep 2026) |

All three are `no_agent=True` + `deliver=origin` and **silent when nothing fires**
(empty stdout = no message). Shared code lives in `lowcap_common.py`; state/DB:
`~/.hermes/data/lowcap_alert.db` (tables `social`, `coins`, `meta`) and
`~/.hermes/data/lowcap_alert_state.json` (cooldowns).

### Kirim ke bot alert (@memescallsbot) — dipasang 28 Sep 2026

Semua lane (P1/P2/P3/EARLY WATCH/TRACK) **nembak Bot API sendiri** ke `@memescallsbot`,
kredensial `~/.hermes/data/perf_bot.json` (mode 600).

**Kenapa BUKAN `deliver: telegram:<chat_id>` di cron:** chat_id DM private == user id,
jadi kiriman cron tetap keluar dari bot gateway (`@your_gateway_bot`) dan mendarat di chat
LAMA. Satu-satunya cara pesan tampil DI bot alert = pakai token bot itu.

Wiring: tiap lane punya `run()` yang nangkap stdout `main()` (`contextlib.redirect_stdout`)
lalu panggil `lowcap_common.deliver()`:

- **kirim sukses → stdout KOSONG** → cron diam, jadi **nggak dobel** di chat lama.
- **kirim gagal → teks DICETAK ke stdout** → `deliver: origin` jadi jaring pengaman;
  alert nggak pernah hilang cuma gara-gara bot/jaringan mati.
- Mode manual/diagnostik **cetak lokal, nggak pernah dikirim**: `--digest`, `--all`,
  `--selftest`, `--local`. Kill-switch seluruh lane: `ALERT_PUSH=off`.
- Jejak tiap percobaan kirim: `~/.hermes/data/alert_push.log`

**PITFALL MAHAL (28 Sep 2026):** daftar argumen "cuma lihat" ada di
`lowcap_common.LOCAL_FLAGS`. Argumen baru yang nggak didaftarkan di situ = **sobek**:
`should_push()` balikin True → stdout ditangkap → **langsung terkirim ke bot**.
Kejadian nyata: `sm_lane.py --preview` belum terdaftar → 2 kartu tes nyasar masuk
`@memescallsbot`. Sekarang `--preview/--json/--dry-run/--no-push` sudah di daftar dan
ADA SELFTEST-nya di `lowcap_common`. **Tiap bikin argumen mode-lihat baru → tambah ke
LOCAL_FLAGS + tambah tes `should_push([...]) is False`.**

## Lane SMART MONEY + registry wallet TERUKUR (28 Sep 2026)

Latar: papan skor merah (3 dari 29 call masih untung). Perbaikan lama cuma nyentuh
*keluarnya* alert; yang belum pernah digarap: **dari mana call-nya datang**.

**Ide intinya: berhenti percaya tag GMGN (`smart_degen_count`), UKUR sendiri.**

| File | Peran |
|---|---|
| `sm_watch.py` | tarik `gmgn-cli track smartmoney` (feed buy/sell wallet besar) → `~/.hermes/data/sm_watch.db` (tables: `trades`, `wallet_stats`, `runs`) |
| `sm_lane.py` | cari token yang baru dibeli wallet ber-record → saring → kartu + `call_ledger.jsonl` (lane `SMART MONEY`) |
| `winner_study.py` | gabungkan fitur SAAT call vs hasil terukur → cari kriteria winner |

**Cara hitung record wallet (yang bikin ini beda dari fitur GMGN):** round-trip
per `(wallet, token)` = harga jual terakhir ÷ harga beli pertama, dari trade yang
KITA lihat sendiri. Ditutup → masuk hit-rate & median (butuh `n_closed ≥ 3` baru
disebut **ber-record**); belum ditutup → ditulis "holding", bukan dihitung menang.
Ledger feed itu jendela bergulir, jadi angka wallet baru matang setelah beberapa hari
cron `*/10` numpuk.

**Gate lane SMART MONEY** (`G` di `sm_lane.py`, semua konstanta, gampang di-tuning):
mc $80K–$60M · liq ≥ $40K · liq/mcap ≥ 6% · holder ≥ 250 · top10 ≤ 35% ·
bundler ≤ 25% · mc/ATH ≥ 15% · **harga sekarang ≤ 50% di atas harga masuk wallet** ·
harga/1 jam lalu ≤ 2,5x · wallet ber-record ≥ 1 (jalur cadangan: ≥ 3 wallet, dan
kartu WAJIB tulis "belum terbukti"). "Ber-record" = `S.rated()`: `n_closed ≥ 5`
**dan** hit-rate ≥ 60% — ambang yg sama dipakai kartu `smartmoney_lines()`.

**Argumen penting:** `--run --chains sol,bsc` (collector), `--report` (papan wallet),
`--lookup --chain sol --address X` (wallet mana yang masuk token ini),
`--preview` (lihat calon, JANGAN kirim), `--selftest` (20 tes).

### Hasil deep dive 28 Sep 2026 — kenapa winrate jelek (angka, bukan feeling)

Diukur dari 30 call yang punya checkpoint (`early_watch_outcomes.jsonl`):

- **Puncak TERUKUR ≥1,2x: cuma 2 dari 30 (7%).** ≥1,5x: 1. ≥2x: **0**.
  Semua medan turun (−28% sudah terjadi 15 menit setelah call).
- **28 dari 30 token sudah bikin ATH LIFETIME-nya SEBELUM checkpoint 15 menit kita.**
  ATH@call ≈ ATH@4j (rasio 1,00) → pump-nya lewat sebelum kita nyampe.
- **`ath_mc` lifetime GMGN bukan hasil call kita.** Contoh `keb`: mc0 $16, `peak_mult`
  x14.104 → rata-rata puncak jadi x489 = omong kosong. **Label yang bener = puncak
  checkpoint terukur** (`winner_study.py` cuma pakai itu, dan buang checkpoint >4 jam).
- Aturan keluar nggak nyelametin: TP 1,5x + SL 0,8 cuma nambah winrate 10%→13%
  (rata-rata x0,70). Kalau entry-nya udah −30% dalam 15 menit, exit rule bukan obat.
- Petunjuk kasar per lane (n kecil, JANGAN dijadikan kebijakan): call mcap besar (P2,
  ≥$1M) median akhir ≈1,0x; EARLY WATCH mcap ~$5K median ≈0,60x.

**Kesimpulan: masalahnya di WAKTU MASUK (telat), bukan di exit.** Karena itu
`early_watch.py` sekarang merekam fitur anti-chase SAAT call (`near_high` = posisi
harga vs high lokal dari seri `mk`, `run_up`, `age_min`) dan ngasih penalti skor
`chase_pen` kalau harga nempel puncak lokal + udah lari — plus nulis **semua fitur
yang dibutuhkan studi** ke `~/.hermes/data/ew_features.jsonl` (GRATIS: field-nya
sudah ada di feed yang memang kita tarik; nol panggilan GMGN tambahan).

### DEEP DIVE 30 Sep 2026 — 180 call, lintas lane (`winner_deepdive.py`)

User: *"calls kita dah banyak nih, saring lagi dan deep dive pola winner dan loser, fokus di
winnernya"*. 180 call punya checkpoint (93 belum). Yang beda dari `winner_study.py`:
baca **semua lane** (`call_ledger.jsonl` + `early_watch_ledger.jsonl`), atribusi
**per-call** (`address` + **jam call** — bukan per-address; call ulang setelah cooldown = call
baru), dan misahin tegas puncak checkpoint vs `ath_mc`.

**Hasil (angka, bukan feeling):**

- Puncak terukur: **≥3x 2 (1,1%) · 2–3x 8 (4,4%) · 1,5–2x 19 (10,6%) · 1,2–1,5x 21 (11,7%)
  · <1,2x 130 (72,2%)**. Median puncak **x1,01** vs median `kini` **x0,57**.
- **Dari yg sempat ≥1,2x (50 call): cuma 10 (20%) masih ≥1,5x saat kini; 6 di 1–1,5x;
  34 (68%) UDAH KASIH BALIK ke bawah 1x.** Median x1,52 → x0,46.
- **Kapan puncaknya:** +15m 26% · +30m 20% · +1j 28% · +4j 26%. Hampir separuh puncak di
  **30 menit pertama**.
- **Semua aturan keluar median-nya ≤1x** (SEMUA lane): keluar +15m x0,96 (41% untung) ·
  +30m x0,96 · +1j x0,88 · +4j x0,78; TP 1,5x/2x/3x + SL 0,7 nggak nurunin apa-apa.
  **Artinya: belum ada edge — di entry maupun di exit.** Jangan naikin size; itu kesimpulan
  datanya, bukan pesimisme.
- **Per lane:** EARLY WATCH 88 call, **22% pernah ≥1,5x** tapi median kini **x0,34** (spike
  lalu mati) · P2 57 call 11% ≥1,5x, kini x0,91 · P3 29 call 10%, kini x0,92.
  P2+P3 = satu-satunya yg nggak bleeds (x0,96–0,99 di semua horizon) tapi juga nggak naik.
- **Per jenis call:** `near_completion` (preset FINAL STRETCH) 33% ≥1,5x (tertinggi, 52 call)
  tapi kini x0,27 · BREAK 12% · IMPULS 18% (median puncak x1,24, kini x0,51) · HOT 8% ·
  GAINER 12% · **KOL 0/7, AKUMULASI 0/6, `completed`/MIGRATED 0/7 — belum pernah sekali pun
  ≥1,5x.**
- **Band conviction NGGAK bisa ngeranking:** 🟠 TIPIS **15%** ≥1,5x (48 call) vs 🟢 BAIK
  **10%** (21) vs 🟡 SEDANG **0%** (10) — urutannya kebalik dari janji label.
- Profil pemenang: median mc0 **$24K** / liq0 $19K / **liq/mcap 80%**, sedangkan yg gugur
  mc0 $270K / liq 42,8% (ini **confound lane**: pemenang mayoritas dari EW micro-cap).
- **Uji saring fitur: TIDAK ADA gate yg lolos bersih.** Kandidat terkuat `liquidity ≥ $14,9K`
  (keep 16/17 pemenang, buang 21/38 gugur) & `bundler_trader_amount_rate ≥ 0,16–0,20`, TAPI
  yg "terpisah" itu justru fitur yg ngasih **spike**, bukan hasil: `bundler ≥0,16` lebih
  tinggi di pemenang. Di target yg bener (hasil yg BISA DICAIRKAN) separatornya malah
  kebalik/berisik. Yang arahnya stabil: `age_min` (menang ~57–58 mnt vs gugur ~37–39) dan
  `x_user_follower` lebih kecil — **hipotesis, bukan gate** (n=24/36).

**Kesimpulan: masalah bukan di gate, tapi (a) entry masih kejap di spike & (b) exit nggak
dipakai.** 68% pemenang kasih balikin semua.

#### Yang DIUBAH ke engine-nya (30 Sep 2026)

1. **`winner_deepdive.py`** (baru) — lintas lane, 4 blok: sebaran puncak · retention puncak→kini ·
   **simulasi aturan keluar** (`keluar +15m/+30m/+1j/+4j`, `TP … prio`, `TP+SL`) · **uji saring
   ambang** (`retain ≥75% pemenang, buang ≥35% yg gugur`) · per lane/kind/band/skor.
   ```bash
   python3 winner_deepdive.py              # lengkap (~15 KB)
   python3 winner_deepdive.py --brief      # ≤3900 char, buat cron mingguan
   python3 winner_deepdive.py --lane "EARLY WATCH"   # per lane + split kebijakan
   python3 winner_deepdive.py --tier 2     # label pemenang digeser
   ```
   Cron mingguan `30 8 * * 1` (job `255aabfe0444`) sekarang jalanin ini, bukan `winner_study.py`.
2. **Papan skor (`early_watch_track.py`): verdict & median PUNCAK pakai puncak checkpoint
   (`obs`), BUKAN `peak` yg bisa = batas atas `ath_mc`.** ATH lifetime tetap ditampilkan,
   dipisah + dilabeli `batas atas (ATH token)`. 2 tes baru: (a) token yg CUMAN punya ATH
   sebelum call **nggak boleh** dapet label `🎢 SPIKE LALU MATI` (padahal mult-nya flat),
   (b) token yg beneran spike 4x lalu ambruk **wajib** kena `SPIKE LALU MATI`. 47/47 lulus.
   Efek nyata: tally berubah dari banyak "SPIKE LALU MATI" jadi 132 💀 TURUN — itu gambarannya
   yg jujur.
3. **"Jejak terukur" nempel di kartu, bukan cuma di papan skor** (`lowcap_common.track_line()`):
   tiap kartu bawa rekor JENIS/preset-nya sendiri, mis.
   `📉 jejak terukur **BREAK** (33 call): 12% pernah ≥1,5x · median kini x0.96 · keluar terbaik +15m x0.97`.
   Label = puncak checkpoint (max `mult` ≤4 j). Dipasang di kartu EARLY WATCH (per preset),
   kartu P2/P3 (`track_line(lane="P2", key=fired[0])`) dan item KOL.
   **`TRACK_MIN_N = 8`** — di bawah itu *nggak dicetak*. `small=True` → 5–7 call boleh tampil
   TAPI wajib bawa cap `(sampel kecil, belum kesimpulan)`.
4. **`conviction_note()` sekarang nyetak rekor band + peringatan** kalau urutan terukur ≠
   urutan yg dijanjikan label (`band_track_line()`). Skor yg nggak bisa ngeranking jangan
   disembunyiin di balik label "BAIK".
5. **Gate `LOWCAP_DEAD_KIND_GATE` — NYALA di lane P2 sejak 30 Sep 2026 (keputusan user).**
   Di-export di `lowcap_p2.sh` (`export LOWCAP_DEAD_KIND_GATE=on`), BUKAN di kode — jadi
   `--selftest`/jalur manual default-nya tetap OFF dan perilakunya tetap bisa dibandingin.
   Buang jenis call yg 0% ≥1,5x dgn sampel ≥`DEAD_KIND_N`(=5) — sekarang KOL 0/7 &
   AKUMULASI 0/6. Aturannya:
   - gate jalan **SEBELUM** `items[:6]` → jenis mati nggak makan slot kartu sehat;
   - yg dibuang **DITULIS di kartu** (`⚙️ gate jenis tanpa rekor NYALA — di-skip: …`) dan
     dicatat di heartbeat `lowcap_alert_p2.last` kalau sampai 0 item — **nggak boleh hilang senyap**;
   - logikanya fungsi murni `gate_dead_kinds(items, dead)` → 6 tes offline di
     `lowcap_alert.py --selftest` (tanpa data live, tanpa jaringan).
   Matiin: buang `export` di `lowcap_p2.sh` atau set `LOWCAP_DEAD_KIND_GATE=off`.
   **Lane P3 nggak butuh** (jenisnya HOT/GAINER, dua-duanya punya rekor).
6. Tes: `lowcap_common --selftest` **32/32** (7 tes baru buat track_record/track_line/dead_kinds,
   pakai data palsu di tmp + `peak_mult: 99` buat mastiin dia nggak kepakai).

**Belum di-eksekusi (butuh keputusan user):** naikin `EW_MIN_SCORE`/gate umur
(`age_min ≥45 mnt`) atau ngunci exit ≤30 mnt di kartu. Semua itu geser perilaku lane →
omong dulu, jangan diam-diam.

### Aturan studi kriteria winner (`winner_study.py`)

Ini yang bikin pertanyaan "fitur apa yang bedain winner" akhirnya bisa DIJAWAB:

1. **Fitur harus direkam SAAT CALL.** Rekonstruksi belakangan = mustahil / bias.
   `ew_features.jsonl` (~50 field) + fallback ledger lama (dipetakan `mc0→market_cap`,
   dst) + `call_ledger.jsonl` (semua lane) → join **by address**, bukan `ts`
   (ts fitur & ledger ditulis milidetik terpisah — bug nyata, sudah ada tesnya).
2. **Nggak ada kesimpulan di bawah `MIN_N = 8` per kelompok.** Ditulis "belum cukup
   data", bukan dipaksa jadi kriteria.
3. **Cuma disebut "kandidat kriteria" kalau selisih median ≥30%** (angka) / ≥25 poin
   (biner) — dan tetap dilabeli hipotesis.
4. Ledger nyata pakai key `horizon` (bukan `horizon_h`) — salah baca key = 103 baris
   hasil jadi 0 dan laporannya **diam-diam kosong**. Sudah ada tes regresi khusus.

Kalau lane diam: baca `~/.hermes/data/alert_push.log` dulu
(`ts | lane | KIRIM/GAGAL | n char | message_id`) — bedain "nggak ada sinyal" dari
"bot-nya yang rusak".
- Konversi Markdown→HTML + pemotong pesan: `lowcap_common.md_to_html()` / `tg_chunks()`.
  **Satu implementasi saja** — `perf_report_send.to_html()` sengaja cuma nitip ke situ.

### Bot alert DIMATIKAN (30 Sep 2026 — arahan user "non aktif memebot")

Bot **@memescallsbot** (kredensial `~/.hermes/data/perf_bot.json`) **dimatikan**: nggak ada
kiriman lagi. Kill-switch-nya di **satu titik**, `lowcap_common.meme_bot_off()`:

```bash
rm ~/.hermes/data/memebot_off     # balikin kirim ke bot
ls -la ~/.hermes/data/memebot_off # cek status (ada = mati)
MEMEBOT_PUSH=off                  # cara kedua (env), buat sekali jalan
```

- Cakupan: **semua** jalur kirim lewat `deliver()` = P1 `lowcap_collect.py`, P2/P3
  `lowcap_alert.py`, `early_watch.py`, `early_watch_track.py`, `sm_lane.py`. Cuma 6 file
  itu yg nembak ke bot ini (`grep -rln "deliver(\|tg_push(" *.py`).
- **WAJIB: teksnya TIDAK boleh dicetak.** Kalau dicetak, cron `deliver: origin` ngeflood DM
  utama — perbedaan penting: **matiin bot ≠ pindahin ke DM.** Jadi `deliver()` balik
  `(False, "dimatikan")` + tulis status `MATI` di `alert_push.log`, stdout tetap kosong.
- **Lane-nya tetap JALAN** (scan, ledger, checkpoint, `ew_features.jsonl`, heartbeat) → jejak
  terukur & studi winner terus nambah. Yang mati cuma kirimannya. Cek sehat = mtime
  `*.last` + baris `| MATI |` di `alert_push.log`.
- `perf_report_send.py` (perintah MANUAL) tetap bisa dipakai: kalau bot mati dia **cetak
  lokal** — yg dimatikan kirimannya, bukan kemampuan user minta laporan.
- 7 tes offline di `lowcap_common --selftest` (flag ada/nggak ada, env, "nggak dicetak",
  status MATI kecatat) — **39/39 lulus**.

Bukti live 30 Sep: `./lowcap_p3.sh` → `stdout 0 byte` + log
`P3 | MATI | 8339 char | dimatikan (MEMEBOT_PUSH off)`. Bandingkan 3 baris sebelumnya yg
masih `KIRIM | … | message_id`.

## X access: nitter RSS, NOT the X API

`xurl` is often not installed and the X API free tier is ~100 reads/month, plus
`syndication.twitter.com` returns 429 from servers. Instead discover public **nitter**
instances and read `https://<instance>/<handle>/rss`:

```bash
curl -s https://status.d420.de/api/v1/instances   # healthy + rss == usable
curl -sL "https://shitter.thepixora.com/realDonaldTrump/rss" | head -c 400
```

Key details:
- Cache the working instance in DB `meta.host_used` and try it **first** next run.
- Try at most ~3 instances per handle — trying all of them makes one run take 3+ minutes.
- **Parallelise** handle fetches (`ThreadPoolExecutor(max_workers=6)`); 24 handles
  sequentially = 3m18s, parallel = **16s**.
- Media-only posts come through as literally `"Video"` / `"Photo"` — ignore those as text.

## Tier definitions

Handle tiers (`TIER_A/B/C` in `lowcap_common.py`):
- **A** — head of state / gov / regulator / market-mover personally: Trump, WhiteHouse,
  POTUS, SECGov, CFTC, federalreserve, elonmusk, cz_binance
- **B** — crypto KOLs who move low caps: saylor, cobie, blknoiz06, MustStopMurad, theunipcs…
- **C** — fast-news / on-chain: WatcherGuru, tier10k, DeItaone, TreeNewsFeed, lookonchain

**P1 fires on any of:** A-account market-relevant post ≤25 min old · urgent wording
(hack/approved/delisted/rate cut…) from A or C · cashtag from A · **cluster** (≥3 distinct
accounts same cashtag within 30 min) · rug/hack wording matching a **tracked** low cap.

**P2 fires on:** single KOL cashtag · 2-account cluster in 60 min · on-chain impulse
(ch1h ≥ +60% AND turnover ≥ 50% of mcap) · re-entry in hot ranks (BREAK) · buy/sell
ratio ≥ 1.5 with volume ≥ $500K (AKUMULASI).

**P3** = roundup digest: busiest low caps, those passing the base screen, healthy gainers.

Base screen before *any* token deserves a mention: mcap $150K–$50M · liq ≥ $150K ·
**liq/mcap ≥ 3%** · top10 ≤ 40%.

## Conviction score (/10) — first thing on every card

Every card leads with a conviction score so a token can be triaged at a glance. It is
**not** a black box: the four components are printed on the line under the score.

| Component | Max | Source | What it answers |
|---|---|---|---|
| likuiditas | 2,5 | DB | bisa keluar kalau mau jual? |
| sebaran holder | 2,5 | DB | terkonsentrasi di sedikit wallet? |
| kesehatan momentum | 2,0 | DB | naiknya masuk akal atau artefak/parabola? |
| kualitas pemegang | 3,0 | scan insider | yang masuk smart money atau distributor? |

Bands: **💎 TINGGI** ≥8 · **🟢 BAIK** ≥6 · **🟡 SEDANG** ≥4,5 · **🟠 TIPIS** ≥3 · **🔴 HINDARI** <3.

**The insider verdict is a CEILING, not just a deduction.** `INSIDER_DUMP` caps the score at
**4,4** and `INSIDER_WARN` at **5,9** — otherwise a token with 23 bundlers can still score 6,0
"BAIK" off liquidity and momentum alone. That exact bug was caught in live output (bukangi) and
the cap is what fixed it. When the cap binds, the card says so: `— dibatasi dari 6.0 (insider
sedang distribusi)`.

Only components 1–3 come from the DB, so they are free. Component 4 needs a GMGN scan; when the
budget is spent or GMGN is banned it scores a **neutral 1,5** and the card prints
`— insider netral, belum diukur`. Never silently treat unmeasured as safe, and never hand it the
full 3,0 — a high score built on absent data is a fabricated report.

Regression: `python3 lowcap_alert.py --selftest` (offline, no network).

## Insider enrichment on the card (P2 + P3)

Each alert card answers "who actually bought this?" — is there smart money in, or is the
holder base *allocated* and now being distributed. Backed by
`~/.hermes/scripts/insider_scan.py` (see the `gmgn-insider-rotation-scan` skill for the full
method, thresholds and track-record baselines).

Wiring: `insider_budget(3)` at the top of `tier_p2()` / `tier_p3()`, then
`insider_lines(chain, address)` appended to each card. **Budget is mandatory** — GMGN is a
leaky bucket per IP, and P1 (`*/5`) plus P2 (`*/15`) plus P3 already spend calls on
`market hot-searches` × 4 chains.

Behaviour to keep:
- **Silent skip, never a fake "all clear."** If the budget is spent or GMGN is cooling down,
  `insider_lines()` returns `[]` and the card simply has no insider block. Absent means
  **not measured**, not "safe" — say that out loud if the user asks why a block is missing.
- Results cache in the `insider_scan` table of `lowcap_alert.db` (360 min TTL), so re-running
  a lane inside the TTL costs **zero** GMGN calls.
- P1 stays untouched — it is the news-driven lane and must not wait on a holder scan.

## P1 relevance gate — substring matching bit us twice

`is_market_relevant()` in `lowcap_common.py` decides whether a tier-A/C post is worth an
urgent alert. It used to be plain substring matching, which fired on **39 of 475 stored
posts** that had nothing to do with markets:

| matched | because the text said |
|---|---|
| `sec` | "America is free, strong, **sec**ure" (a Gold Star proclamation) |
| `gold` | "**Gold** Star Mother's Day" |
| `eth` | "toge**th**er", "whe**th**er" |
| `sol` | "**sol**diers", "**sol**ution", "**Sol**idity", "**sold**" |
| `ban` | "**ban**k" |
| `defi` | "**defi**nitely" |
| `etf` | random URLs |

The real incident: P1 URGENT pinged a presidential proclamation about military families.
Fix has two halves — **word boundaries for short/ambiguous keywords** (`MKT_WHOLE`), and
**`MKT_NOISE` phrases stripped before matching** (`"gold star"`). Long unambiguous keywords
keep substring matching so `deregulation` still matches `regulation`.

The second half matters more: **a cashtag IS the market signal.** The gate used to run
before `cashtags()`, so `@lookonchain: whale deposited 541,009 $HYPE ($49.55M)` was
**skipped** — the only reason it ever fired was the accident of "sold" containing "sol".
Now `if not tags and not is_market_relevant(txt): continue`. Net over the stored corpus:
**14 noise killed, 6 genuine signals restored, 0 regressions.**

When you touch this filter, **replay the whole `social` table** (old logic vs new) and
print the diff — do not judge by a couple of examples. `lowcap_collect.py --selftest`
carries the regression cases (8 checks).

## Lane EARLY WATCH — pra-graduate pump.fun (dipasang 28 Sep 2026)

User kirim screenshot kartu GMGN "👀 EARLY WATCH · SOL · JACK" → model kartu itu dipakai.

`~/.hermes/scripts/early_watch.py` — sumber `gmgn-cli market trenches --type new_creation`.
**BEDA PERMAINAN** dari P2/P3: mcap $2K–$50K, umur <24 jam, bonding <100%. Layar P2/P3
(batas bawah $150K) sengaja nge-exclude zona ini. Cron `*/30`, `no_agent=True` → output
script ditempel apa adanya, jadi **stdout kosong = DIAM** (tanpa biaya LLM).

Jebakan yang WAJIB diinget (semua ketemu dari data nyata, bukan tebakan):

- `renounced_mint` / `renounced_freeze_account` / `s_qsafe` == "ya" untuk **SEMUA** token
  pump.fun → NOL daya beda. Jangan pernah dipakai sebagai nilai plus di kartu.
- Pembeda yang BENERAN jalan: `creator_created_count` (kelihatan **1** vs
  **617 / 2322 / 3119 / 6361 / 18853** = pabrik token), `rug_ratio`, `bot_degen_rate`,
  `bundler_trader_amount_rate`, `top70_sniper_hold_rate`, `image_dup` (copycat).
- **Kurva sehat: liq > mcap (~150%).** Kejadian 28 Sep: `久留美` LP $2K vs MC $54K = **3,7%**
  tetap dapet skor **9,7 "MENARIK"** → tambah gate `min_liq_mcap = 0.30`.
- **Skor bagus dari ketiadaan aktivitas itu menyesatkan** → `MIN_ALERT_SCORE = 7.5` +
  batas atas aktivitas (swaps <5 → cap 4.5; <10 → cap 6.0). Polanya sama persis dengan
  cap conviction insider: **batas atas, bukan pengurang.**
- `usd()` membulatkan ke "$2K" → pesan gate jadi tolol **"liq $2K < $2K"**. Pakai
  `usd_p()` (format koma) untuk nilai ambang.
- `gmgn-cli` itu symlink ke `~/.local/bin`; `gmgn_raw()` resolve sendiri (PATH-independent,
  aman dipanggil cron tanpa `export PATH`).

Selftest: `python3 early_watch.py --selftest` — 66 tes offline, termasuk pagar
"kurva kering TIDAK BOLEH disebut MENARIK" + **tes spec yang ngunci angka preset user**.
Debug: `python3 early_watch.py --all` → tampilkan yang gugur + alasan, abaikan cooldown & skor.

### GATE = SETINGAN FILTER USER (28 Sep 2026, sore) — sumber kebenaran baru

User kirim **dua JSON preset filter** dari UI-nya (tab `finalStretch` & `migrated`) dengan
perintah "ikutin settingan gw ini". Sejak itu gate lane ini BUKAN angka tuning gw lagi,
tapi `PRESETS` di `early_watch.py` — disalin **apa adanya** dari JSON itu:

| Filter (JSON user) | Field feed GMGN | finalStretch | migrated |
|---|---|---|---|
| protocols | `launchpad_platform`/`exchange`/`launchpad` | pump, liquidAfAmm, riseRich, stonkfun, pve | pump, liquidAfAmm, riseRich, stonkfun (pve FALSE) |
| age | `created_timestamp` | 10–300 menit | ≤24 jam |
| marketCap | `market_cap` | ≥ $12.000 | (kosong) |
| top10Holders | `top_10_holder_rate` | 15–30% (ADA MIN) | 15–30% |
| devHolding | `dev_team_hold_rate`, `creator_balance_rate` | ≤2% | ≤2% |
| snipers | `sniper_count` **dan** `top70_sniper_hold_rate` | ≤12 (dua-duanya) | ≤12 |
| insiders | `suspected_insider_hold_rate`, `rat_trader_amount_rate` | ≤8% | ≤8% |
| bundle | `bundler_trader_amount_rate` | ≤30% | ≤30% |
| holders / botUsers | `holder_count` / `bot_degen_count` | ≥30 / ≥30 | ≥100 / ≥100 |
| fees | `total_fee` (SOL) | ≥0,4 | ≥1 |
| tab | tipe trenches | `near_completion` | `completed` |

Aturan yang wajib dipegang:

- **Angka preset DIKUNCI tes** (`spec finalStretch/migrated = JSON user apa adanya`).
  Kalau ada yang geser ambang diam-diam → tes gagal. Geser = ngomong dulu ke user.
- **Skor gw nggak lagi ngebuang token** yang lolos filter user (dulu `MIN_ALERT_SCORE 7.5`
  ngebuang). Skor sekarang cuma **urutan tampilan + info di kartu**. Kalau mau nyaring lagi:
  `EW_MIN_SCORE=7.5`.
- **Lapis-2 `extra_fails()`** = pelajaran kita SENDIRI (rug_ratio ≤0,10 · `liq/mcap ≥30%`
  kasus 久留美 · bukan wash-trading). Default ON, `EW_EXTRA_GUARDS=off` buat matiin.
  Sengaja dipisah supaya kelihatan mana "settingan user" mana "tambahan kita".
- **Tidak ada pre-filter server-side lagi** di `fetch()`. Ini pernah nyakitin: `--max-progress 0.98`
  diam-diam membuang SEMUA token `completed` (progress = 1,0). Sekarang `fetch()` cuma kirim
  `--type` + `--limit`; **semua filter dipasang lokal** → bisa di-selftest offline + dihitung
  per-filter berapa yang gugur.
- **Platform yang nggak kebaca dilaporkan**, bukan diam-diam dibuang: header nulis
  "_⚠️ N token gugur cuma gara-gara platform-nya nggak kebaca di daftar lu_". `PLATFORM_OF`
  memetakan nama JSON user → string feed (`pump` → pump.fun/pump/pump_amm; meteora/mayhem
  TIDAK masuk daftar karena di JSON user `meteoraAmm`/`mayhem` = false).
- Kalau preset diubah, cek juga: kartu nampilin tab asalnya (`🎚 FINAL STRETCH/MIGRATED`),
  ledger + `ew_features.jsonl` nambah field `preset` + `tipe` (bahan studi winner per tab).

**Hasil live pertama (28 Sep 09:50 WIB, 120 token ditarik):** FINAL 1/60 lolos, MIGRATED 1/60.
Pemblokir terbesar: bot (`bot_degen_count`) + fee + `top10` MIN 15% (token post-migrate
meteora top10-nya cuma 1–4% → kena batas MIN). ~39–63 token gugur murni karena platform
di luar daftar user.

### Ledger hasil — jawaban untuk "model ini bagus nggak?"

28 Sep 2026 user kirim screenshot @0xkotori (tool "Bump Sol Chain Alert") yg pamer
"🚀 332X · $JACK". Pertanyaan sebenarnya bukan "kartunya bagus nggak" tapi "buktinya mana".
**Kartu pemenang ≠ bukti model bagus** — yg nggak kelihatan itu berapa ratus token lain yg mati.

Verifikasi $JACK (kline 1h + token info, 28 Sep 2026) — ini yg WAJIB dicek tiap kali
ada yg pamer multiplier:
- ATH `$7.065.967` → **larinya nyata**, bukan klaim palsu.
- Tapi candle ATH-nya: **high $6.799.425, close $284.413.** Kartu "332X" lahir **di dalam
  wick ~20 menit** itu (kartunya jam 13:40-13:41, candle 13:00-14:00).
- Sekarang MC ~$220K = **−96,9% dari ATH**. Yg beli saat lihat kartu ($6,3M): **−96,5%**.
  Yg beli di alert ($18,9K) dan tahan: masih x11,6.
- View **kartunya** 9 / 6 / 5; post yg memamerkannya **4.7K view** — diposting SETELAH.

**Aturan: selalu laporkan `puncak` DAN `kini`, jangan cuma multiplier.** Puncak di low-cap
sering cuma wick detik-an yg nggak bisa dijual. Ini berlaku ke kartu kita sendiri juga.

Wiring (SATU ledger untuk SEMUA lane — jangan bikin ledger per-lane, laporannya drift):
- `lowcap_common.call_entry(lane, kind, coin, score=, band=, why=)` + `call_ledger_append()`
  → `~/.hermes/data/call_ledger.jsonl`. Dipakai P2 (CLUSTER/KOL/IMPULS/BREAK/AKUMULASI)
  dan P3 (HOT/GAINER). `early_watch.py` nulis file sendiri
  (`early_watch_ledger.jsonl`, lane default `EARLY WATCH`).
- **Cuma call yang BENAR-BENAR terkirim yang dicatat.** P2 motong ke 6 kartu
  (`items[:6]`) — ledger ditulis SETELAH pemotongan. Kalau nggak, kita nyatat call yang
  nggak pernah dikirim dan rekam jejak kita jadi bohong.
- Call **tanpa kontrak** (kashtag KOL yg nggak ada di `coins`) TETAP dicatat dgn
  `address: null`; P2 nyoba nyambungin dulu lewat `sym_index()`. Tujuannya supaya
  laporan bisa bilang berapa call yang nggak bisa diukur — bukan diem-diem dibuang.
- Blok "DILEWATI" P3 **tidak** masuk ledger: itu daftar ditolak, bukan call.
- `early_watch_track.py` (cron `*/2`, job `b5f2cc853e01`) baca KEDUA ledger, cek ulang
  **+15m / +30m / +1j / +4j / +24j**, nulis `early_watch_outcomes.jsonl`. DIAM kalau nggak
  ada checkpoint baru. `MAX_CALLS=25` pagar per ronde, `SLEEP=3` antar call (leaky bucket).
  **Horizon 72j DIBUANG** (arahan user 28 Sep 2026: *"rotasi meme coin cepet"*). Horizon
  disimpan sebagai jam pecahan (`0.25` = 15 menit, `0.5` = 30 menit) dan labelnya lewat
  `hl()` (`0.25` → `+15m`). Cron `*/2` bikin checkpoint 15m keukur paling lambat +17m.
- **Dedupe wajib saat membaca.** P3 jalan 3x/hari tanpa cooldown, jadi token yg sama
  muncul berulang. `read_alerts()` nyimpen satu posisi per `(lane, kontrak)` = kemunculan
  PALING AWAL. Tanpa itu satu call kehitung 3x dan papan skornya ngasal.
- **Kunci checkpoint = `(kontrak, JAM CALL, horizon)`.** `ts` wajib masuk kunci; tanpa itu
  token yg di-call ulang setelah cooldown 6 jam dianggap checkpoint yg sama dan call
  keduanya nggak pernah diukur.
- Ledger gagal nulis **jangan pernah** matiin alert: `call_ledger_append()` balikin 0 dan
  nggak raise (ada tesnya: path `/proc/...` → 0, bukan exception).
- Override path buat tes: env `CALL_LEDGER_PATH` / `EW_LEDGER_PATH` / `EW_OUTCOMES_PATH` /
  `EW_DATA_DIR`. **Selalu tes pakai ledger terpisah di `/tmp`** — jangan kotori rekam jejak
  asli pakai run tes (token yg di-call cuma buat tes bikin statistiknya ngasal).

### Kartu papan skor (`early_watch_track.py`) — 5 TERAKHIR + TOTAL (28 Sep 2026)

User: *"signal kita kebanyakan tuh, paling kek lu bikinnya versi 5 terakhir aja, trus
bawahnya tuh total brp brp tulis, kayak rata rata signal lu timeframe bla bla bla brp yg
punya record bagus dan brp yg rug"*.

Kartu **CALL — PAPAN SKOR** (`--digest`) dan **CALL — HASIL** (tick cron saat ada
checkpoint baru) sekarang berisi:

1. **5 CALL TERAKHIR** — 5 yg paling BARU (by `ts` call), BUKAN yg paling cuan.
   Dipotong oleh `MAX_DETAIL = 5`. Kalau call ≤ 5, judulnya `SEMUA CALL (n)`.
2. **TOTAL n CALL TERUKUR** — dihitung dari SELURUH call, bukan dari 5 yg ditampilkan:
   `🟢 masih untung (kini ≥1x)` vs `🔴 rug/mati (kini <1x)` (+ berapa yg sempat naik ≥3x
   lalu ambruk), median & rata2 `x kini`, median puncak (BUKAN rata2 puncak — satu token
   sampah bikin rata2 jadi x489), plus terbaik/terburuk sepanjang riwayat.
3. **TIMEFRAME** — median `x` per horizon (+15m/30m/1j/4j) dari checkpoint TERAKHIR per
   `(kontrak, jam call, horizon)`; kalau semua ≤1x kartu WAJIB bilang "belum ada edge,
   jangan nambah size" — jangan dipoles jadi "hampir profit".

**Daftar penuh tetap ada**, cuma tidak dikirim lagi: `--digest --full` (semua baris),
`call_perf_report.py` (per-timeframe, kalibrasi conviction), ledger mentah. Memotong
yang DIKIRIM ≠ menyembunyikan data — kalau angka total & daftar penuh nggak bisa
direproduksi, itu laporan yang bohong.

Verifikasi: `python3 early_watch_track.py --selftest` — tes khusus memastikan (a) cuma
`MAX_DETAIL` baris dicetak, (b) yg dicetak = yg TERBARU, (c) TOTAL tetap menghitung
semua, (d) angka untung+rugi jumlahnya 100%, (e) jalur kartu "HASIL" bawa ringkasan yg sama.

### Laporan performa (`call_perf_report.py`) — on-demand, TIDAK dikirim otomatis

28 Sep 2026 user: *"nnti bikin report performance… kumpulin performance call lu 1h, 4h,
24h-nya gmn, dan strategy lu bagusnya di timeframe brp"*. Jadi tracking-nya otomatis
(cron), laporannya dibaca saat diminta — jangan push.

```bash
python3 call_perf_report.py            # laporan teks siap kirim
python3 call_perf_report.py --json     # ringkasan bentuk mesin
```

**Kirim ke bot Telegram:** `perf_report_send.py` → bot **@memescallsbot**, kredensial di
`~/.hermes/data/perf_bot.json` (mode **600**; jangan pernah cetak tokennya).
`--learn-chat` narik `chat_id` dari `getUpdates` setelah user `/start` (bot ini nggak punya
consumer lain, jadi aman — **beda dgn bot engine yg jangan di-getUpdates**). `--ping` tes
koneksi, `--dry` cek isi tanpa kirim. Balik `message_id` tiap bagian = bukti dari Telegram.

**Pakai `parse_mode=HTML`, JANGAN Markdown.** Isi laporan penuh underscore
(`call_perf_report.py`, `early_watch_track.last`) dan Markdown Telegram nganggepnya italic →
pesan gagal/rusak. Di konverter `to_html()` italic **cuma** dikonversi kalau ngisi satu baris
penuh — mid-baris sengaja dibiarkan, kalau tidak nama file ikut kena. Pesan di atas ~3900
char dipotong per baris (jangan sampai motong di tengah tag).
Isi: hasil per timeframe (median, rata2, %naik, %≥2x) → **timeframe paling bagus + pola
decay** (`+1j x1,11 → +4j x1,35 → +24j x0,75` = edge paling gede di 4 jam, berarti keluar
sekitar 4 jam) → kalibrasi conviction → call terbaik/terburuk → per lane → catatan jujur.

Aturan yang WAJIB dipegang:
- **`MIN_N = 5` per horizon.** Di bawah itu laporan harus bilang "belum bisa disimpulkan"
  + "jangan ubah strategi". Ngarang kesimpulan dari 3 data itu persis penyakit yg kita
  kritik dari kartu orang.
- Kalau **semua median ≤1x** → cetak "belum ada edge … bukan alasan nambah size".
  Jangan dipoles jadi "hampir profit".
- **P1 (berita X) nggak dihitung** — itu call berita, bukan call harga.
- Patokan pakai **median**, bukan rata-rata (tahan outlier 300x), plus `%naik` supaya
  distribusi bimodal kelihatan (median bagus bisa nyembunyiin banyak call mati).

Verdict (`verdict()`) — selftest `early_watch_track.py --selftest` **31/31**:

| Verdict | Syarat |
|---|---|
| 🚀 HIDUP | kini ≥2x **dan** ≥50% puncak |
| 🎢 NAIK, TAPI DARI PUNCAK | kini ≥2x tapi <50% puncak |
| 🎢 SPIKE LALU MATI | puncak ≥3x, kini <1x |
| ✅ NAIK TIPIS | 1x ≤ kini < 2x |
| 🩸 TURUN DARI PUNCAK | kini <1x, puncak ≥3x |
| 💀 TURUN | sisanya |

**Bug yg ketangkep selftest sendiri:** aturan naif `kini ≥2x → 🚀 HIDUP` melabeli JACK
**HIDUP** padahal drawdown-nya −96,9%. Itu **persis** framing menyesatkan yg kita kritik
dari kartu orang. "Masih naik" WAJIB dipecah: masih deket puncak vs udah kasih balik.
Ikutin pola ini kalau bikin metrik baru — tulis tes pakai kasus nyata yg menyesatkan.

### Gate `max_bot` nolak JACK — dicatat, JANGAN langsung dilonggarin

Saat alert $JACK: bot **38,1%** > `max_bot` 0,25 → **GUGUR**. Semua gate lain lolos
(liq/mcap 87%, holder 96, top10 31,3%, sniper 0%, bundle 13,8%, kreator 1× launch).
**Bot satu-satunya filter yg blokir** — dan bot-nya nyata, bukan artefak: sekarang masih
31,7%, `top_entrapment_trader_percentage` 14,3%, `fresh_wallets` 1000.

**Keputusan: jangan longgarin karena 1 kasus.** Ngelonggarin filter demi 1 pemenang =
overfit. Ukur dulu lewat ledger, putusin kalau datanya cukup.

## Verification (always do this)

```bash
cd ~/.hermes/scripts
python3 lowcap_collect.py --selftest     # offline; must print SEMUA LULUS
python3 insider_scan.py --selftest       # offline; must print LULUS (0 gagal)
python3 lowcap_alert.py --selftest       # offline; conviction logic, LULUS (0 gagal)
python3 lowcap_common.py --selftest      # offline; 32 tes (HTML, potong pesan, jalur kirim bot, jejak terukur)
python3 early_watch.py --selftest        # offline; 66 tes (gate preset user + anti-chase + kurva kering)
python3 early_watch_track.py --selftest  # offline; 47 tes (verdict puncak-checkpoint, dedupe, kunci, horizon, 5-terakhir+total)
python3 winner_deepdive.py --brief        # studi pola winner/loser (juga jalan tiap Senin 08:30)
python3 call_perf_report.py --selftest   # offline; 33 tes (median, MIN_N, decay, coverage)
./lowcap_p3.sh                            # always prints (no cooldown)
./lowcap_p2.sh                            # silent if all on cooldown = correct
python3 early_watch_track.py             # silent if no checkpoint due = correct
python3 early_watch_track.py --digest    # kartu: 5 call terakhir + TOTAL (baca 2 ledger)
python3 early_watch_track.py --digest --full   # daftar SEMUA call (audit/debug)
python3 call_perf_report.py              # LAPORAN PERFORM saat user minta — TIDAK auto-kirim
```

`--selftest` injects synthetic posts/coins and asserts all four P1 triggers fire **and**
that both guardrails hold (stale >25 min post does NOT fire; single TIER-B post does NOT
become P1). It cleans up after itself.

Jalur kirim **jangan** diverifikasi dari stdout lane-nya — sukses = stdout sengaja
kosong. Bukti terkuat = baris `KIRIM ... | <message_id>` di
`~/.hermes/data/alert_push.log`, karena `message_id` itu balasan Telegram. Cara cepat:
`python3 early_watch.py && tail -3 ~/.hermes/data/alert_push.log`.
`ALERT_PUSH=off python3 early_watch.py` = lihat teksnya tanpa kirim.

## Pitfalls

- **Cron yang DIAM dan cron yang RUSAK kelihatan identik.** Semua lane di sini pakai
  konvensi "stdout kosong = jangan kirim pesan", jadi sukses senyap dan mati senyap
  **nggak bisa dibedain dari chat**. Setiap lane `no_agent` WAJIB nulis jejak hidup tiap
  jalan via `lowcap_common.write_heartbeat()`: `~/.hermes/data/early_watch.last`,
  `early_watch_track.last`, `lowcap_alert_p2.last`, `lowcap_alert_p3.last` — isinya
  `timestamp | rows=.. lolos=.. kartu=..`. Cek kesehatan = mtime file lebih baru dari
  jadwal terakhir. Penulisan dibungkus `try/except OSError` — **jejak gagal nulis jangan
  pernah bikin alert mati.**
- **Jangan nyimpulin performa dari sampel kecil.** `MIN_N = 5` per horizon; di bawah ~30 call
  angkanya masih kebisingan. "Median x1,4" dari 8 data bisa jadi x0,6 di 8 data berikutnya —
  dan kita bakal naikin size berdasarkan sampah. Laporan wajib nyetak peringatan itu sendiri.
- **`ath_mc` GMGN = ATH token, dan bisa terjadi SEBELUM kita call.** Jadi `x puncak` itu batas
  atas optimistis, bukan hasil. Selalu laporin bareng `x kini` (yang realistis dijual), dan
  kalau ATH-nya cuma wick 20 menit, sebut itu terang-terangan di laporannya.
- **JEBAKAN FIELD (ketemu 30 Sep 2026): `peak_mult` di `early_watch_outcomes.jsonl` BUKAN
  puncak checkpoint — itu `ath_mc ÷ mc0` (ATH lifetime ÷ harga call).** Bukti: `ass` mc0
  $4.722, ath_mc $1.017.780 → `peak_mult` 215,54 persis. Analisis yg pakai `peak_mult`
  sebagai "puncak" bakal ngeklaim median x2,39 + 61% call pernah ≥2x, **padahal median
  puncak asli x1,01 dan cuma 16% yg pernah ≥1,5x**. Selalu hitung puncak sendiri:
  `max(mult)` untuk `horizon ≤ 4` per `(address, alert_ts[:13])`. Klaim hasil call WAJIB
  dari `mult`/puncak-checkpoint, bukan dari field itu.
- **Jangan optimasi "puncak" — optimasi hasil yg BISA DICAIRKAN.** Fitur yg misahin pemenang
  versi-puncak (`bundler ≥0,16`, `liquidity ≥$14,9K`) justru yang bikin spike lalu mati.
  Target yg bener = `mult` saat keluar (mis. +15m). Kalau separatornya ilang/balik arah di
  target itu, berarti fiturnya nggak berguna — jangan dipaksa jadi gate.
- **`cronjob(action='run')` balik `FAILED — Job is already running` itu BUKAN error job.**
  Artinya tick scheduler kebetulan lagi pegang job itu. Verifikasi dari `~/.hermes/cron/jobs.json`
  (`next_run_at` maju = tick jalan) atau mtime file jejak — **jangan dari status return
  run manual**, itu bisa bilang gagal padahal job-nya sehat.
- **Cron `script` field may not accept arguments.** `script: "lowcap_alert.py --tier p2"`
  risks being treated as a literal filename. Use small `.sh` wrappers (`lowcap_p2.sh`) that
  `exec python3 lowcap_alert.py --tier p2`. Verified working.
- **Don't hammer nitter.** 6 workers is fine; sequential-with-1s-sleep is fine too, but
  don't raise concurrency much higher or instances start blocking the IP.
- **Anything >+2000% in 1h on a sub-$2M mcap is often a fresh-pool artifact**, not a real
  move. The P2 formatter appends a warning instead of hiding it — keep that honesty.
- **GMGN rate-limits hard** and returns *empty stdout* (not an error) while banned. Treat
  empty stdout as "skip", never as valid data, and throttle ≥3s between calls.
  A burst gets `HTTP 429 ... Rate limit resets at <ts> (~Ns remaining)` and **every retry
  extends the ban by 5s up to 5 minutes** — so never loop-retry. `insider_scan.py` parses the
  reset, writes `~/.hermes/data/gmgn_cooldown.txt`, and refuses calls while it is active; a
  file lock at `~/.hermes/data/gmgn_gate.txt` spaces calls across processes so the lanes
  don't collide.
- Cooldowns are per-lane: P1 90 min/post, 6 h/cluster, 6 h/token. Without them a
  trending ticker spams every run.
- Never claim an alert was delivered from the script's own stdout — since 28 Sep 2026
  success is *defined* as empty stdout. Evidence = `alert_push.log` line with the
  Telegram `message_id`, or the message itself in the bot.
