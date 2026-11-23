# Scan kekuatan relatif saat market turun ("koin mana yang bener-bener kuat")

Companion to `single-token-move-attribution.md` (why ONE token moved) and
`token-news-db-and-unlock-verification.md` (news DB + unlock/close hygiene). This file is the
**breadth** counterpart: not "why did X pump" but "out of the whole market, which names are actually
holding while BTC bleeds".

Trigger: "scan top coin yg performance paling well dan strong pas market crash", "koin apa yang kuat
sekarang", "kiat mana yang bener-bener kuat", or any request for a strength/leaderboard screen.
Not a theme question (→ SKILL.md step 1–5, GMGN heat) and not one-token DD (→ `gmgn-token`).

## 1. Run the scan (script, not ad-hoc)

```bash
python3 ~/.hermes/skills/research/crypto-narrative-scan/scripts/crash_relative_strength_scan.py \
  [--min-vol 5000000] [--top 22]
```

Universe = one `api.binance.com/api/v3/ticker/24hr` call, filtered to `USDT` pairs with
`quoteVolume ≥ $5M`, minus stables and wrapped tokens. Then `klines interval=1d&limit=31` per
candidate in-process (no aggregator, no GMGN — GMGN is for memes/small caps, this is for the liquid
book). Metrics per coin, all computed not eyeballed:

| kolom | arti |
|---|---|
| `chg24 / chg7 / chg30` | perubahan close harian |
| `rs24 / rs7 / rs30` | selisih vs **BTC** di jendela yang sama — ini inti "kuat" |
| `dist_high30` | jarak ke high 30 hari (makin dekat 0 = makin kuat strukturnya) |
| `above20 / above50` | di atas EMA20 & EMA50 harian |
| `vol_exp` | rata-rata volume 3 hari ÷ rata-rata 30 hari |

**Why the venue API and not CoinGecko/CMC:** aggregator snippets go stale and self-contradict (see
`token-news-db-and-unlock-verification.md` §5 — a CoinGecko snippet claimed ONDO "24h −1,20%" against
a live Binance tape of +6,42%). Also `ticker/24hr` without a symbol returns the *entire* universe in
one call, which is what makes a real breadth scan cheap. Only ~90–100 USDT pairs clear the $5M bar,
so the klines loop is small.

## 2. The gate that separates "naik" from "kuat"

Core filter: **`chg7 > 0` AND above EMA20 AND above EMA50 AND `chg24 ≥ −1%`**. Green over the whole
week matters more than green today — a coin that only turned up in the last hour has not been tested
by the drawdown. Report the funnel counts, because the ratio *is* the finding:

> 8 Okt 2026: 89 koin likuid → 47 hijau hari ini → 51 ungguli BTC 7d → 29 hijau + di atas EMA20&50 →
> **27 lolos filter inti**.

## 3. Read the shape of the tape before ranking anything

**Do not accept the user's "market crash" framing without measuring it.** 8 Okt 2026: BTC $82.660
(−0,53% 24j / −2,62% 7d) but **47 of 89 liquid alts were green**, and the red was concentrated in the
majors (ETH −6,43% 7d, SOL −5,01%, SUI −6,44%, TAO −7,02%). Correct framing: **rotation out of majors
into mid-cap alts, not broad risk-off** — and say so in the first lines, because it changes what the
leaderboard means. Recovery-mechanics note: the "crash" narrative came from macro headlines
(US Treasury yields at 19-year highs, Middle East tension + oil, −$485–500M BTC ETF outflow in a day,
$550M of positions liquidated) while alt internals were still bid.

## 4. Trap taxonomy — the part that makes the screen honest

The raw leaderboard is dominated by thin-market squeezes, so every scan ships a **"kelihatan kuat
tapi bukan kekuatan"** list. The script auto-flags the candidates; the *classification* is manual and
must be news-checked via `single-token-move-attribution.md`.

| pola | tanda | contoh 8 Okt 2026 |
|---|---|---|
| **Squeeze pasar tipis** | `chg24 ≥ +40%` sementara volume normalnya cuma $0–5M lalu meledak, dan **nol berita** | OGN **+100% dalam sehari** — fundamental asli (100% fee bersih → buyback OGN, ±14,8% supply sudah dibeli) tapi lonjakan 2× di float tipis = squeeze, bukan tren |
| **Pump tanpa katalis** | naik besar, RSI ekstrem, "no confirmed catalyst" di media | RLC +99,9% (5 Okt), RSI 90, masih −32,8% dari high 30d |
| **Volume tipis** | volume harian pra-lonjakan $0–1M | CTSI +30,9% dengan volume $7M dari biasanya $0–1M |
| **Pump layu** | `chg30` masih besar positif TAPI `dist_high30 ≤ −30%` | QNT 30d +277% tapi −34,7% dari high = distribusi, bukan kekuatan |

Rule of thumb to state in the report: **naik tanpa berita di pasar tipis = squeeze, bukan kekuatan.**
Variabel yang membedakan hanya dua: likuiditas normal dan ada/tidaknya katalis bertanggal.

## 5. Cluster detection: 10 ticker sering cuma 1 taruhan

Group the survivors by ecosystem/thesis before writing anything. 8 Okt 2026: ORCA, RAY, JUP, JTO, MET
semuanya dari kompleks **DeFi Solana dengan revenue riil + katalis governance/produk** — lima ticker,
satu eksposur. Wajib dikatakan: *"ini bukan 5 koin kuat terpisah, ini satu taruhan yang sama."*
Ulangi langkah ini untuk tokenisasi (ONDO, NVDAB, QQQB, STRK) dan AI (NEAR sendirian saat TAO −7% 7d).

## 6. Kelas khusus: token saham tokenized (NVDAB / QQQB)

Saham tokenized di Binance (mis. NVDAB ≈ NVIDIA, QQQB ≈ QQQ) lolos scan ini bukan karena crypto-nya
kuat, tapi karena **bukan beta crypto** — mereka hijau justru saat BTC merah. Berguna sebagai jawaban
"gimana nahan turun tanpa short", dan harus dilabeli eksplisit sebagai eksposur ekuitas supaya nggak
dibaca sebagai sinyal altseason.

## 7. Report shape this user asked for (explicit correction, 8 Okt 2026)

User interrupted the first draft with: **"cari skitar 10 aj dlu, dan kasih tesis ny knpa"** — so:

1. **~10 nama, bukan 22.** Ranking panjang bikin dia nggak bisa mikir. Kirim 10.
2. **Tiap nama wajib ada tesis 1–2 baris: KENAPA kuat, katalis bertanggal, dan satu risiko/angka
   jebakannya.** Tabel angka saja = tidak dijawab. Contoh yang dipakai: ORCA fee-switch (voting
   5–10 Okt) + merger Loopscale → "Formation" masuk pembiayaan AI/robotik/pertahanan, **tapi** proposal
   barunya justru memangkas buyback otomatis 40%→10%; MET DLMM Pro (Solana Summit Singapore 6 Okt) +
   gugatan class action dibubarkan 29 Sep; STRK upgrade mainnet 4 Okt + bahas pindah L2→L1 (target
   2027) dan **paling dekat high 30d (−2,4%)**; JTO bawa saham + perps ke JTX (7 Okt).
3. **Sertakan daftar trap eksplisit** (§4) — dia membaca ini sebagai bukti screen-nya beneran.
4. **Tutup dengan pola besar + apa yang dipantau**, bukan pertanyaan. Dan sertakan catatan jujur
   bahwa semua kandidat naik dengan asumsi BTC cuma koreksi — validasi/invalidasi pakai level BTC
   (8 Okt: support horizontal 81.604).
5. Full tabel + angka lengkap ke vault Obsidian (`Scan Kekuatan Alt saat Market Turun (8 Okt 2026).md`)
   dan sebut nama filenya di chat. Disclaimer "bacaan rule-based, bukan saran investasi" tetap ada.

## Pitfalls

- **Snapshot timing.** Semua kolom dihitung dari satu tarikan data; kalau laporan ditulis >1 jam
  kemudian, sebut jam pengambilan. Jangan campur angka dari dua waktu (lihat §5 file unlock/close).
- **Stablecoin & wrapped bocor ke tabel.** `RLUSD` / `U` / `XAUT` / `PAXG` lolos filter volume; kalau
  dibiarkan mereka nongkrong di daftar "lolos filter inti" dan bikin jumlah kelihatan lebih besar.
  Script sudah mengecualikan stable + `WB*`, tapi emas tokenized (PAXG/XAUT) masih lewat — buang manual
  atau sebut sebagai kelas aset lain.
- **Jangan jual daftar ini sebagai rekomendasi beli.** Ini peta kekuatan; entry tetap butuh lokasi harga
  (`entry-location-and-triggers.md`) dan reconcile posisi/order dulu
  (`portfolio-state-reconciliation.md`).
