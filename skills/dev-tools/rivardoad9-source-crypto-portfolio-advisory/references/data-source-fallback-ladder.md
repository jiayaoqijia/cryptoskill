# Tangga fallback sumber data keyless (verified 3 Okt 2026)

Companion to `live-market-data-sources.md` (endpoint per sumber) — file ini soal **urutan pindah sumber
saat satu endpoint kena rate-limit**, plus cara misahin **mesin** dari **narasi** per token.

## 1. CoinGecko 429 → jangan ulang, ganti bentuk panggilan

Kejadian nyata 3 Okt 2026: panggilan `/coins/{id}` buat 4 aset (WLD, TAO, ONDO, ASTER) berurutan
**semua** balas `HTTP 429` walau sudah `time.sleep(8–10)` + retry 5x. Yang berhasil:

**Langkah 1 — bulk, satu request buat N aset.** `/coins/markets` jauh lebih tahan 429 daripada N panggilan
`/coins/{id}`:

```
https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd
  &ids=worldcoin-wld,bittensor,ondo-finance,aster-2
  &price_change_percentage=7d,30d&sparkline=false
```

Balikin harga, `market_cap`, `fully_diluted_valuation`, `ath`, `market_cap_rank`,
`circulating_supply`/`total_supply` — cukup buat float & overhang.

**Langkah 2 — Binance buat harga + % perubahan** (independen dari rate limit CoinGecko):

```
api/v3/ticker/24hr?symbol=WLDUSDT
  → lastPrice, priceChangePercent, highPrice, lowPrice, quoteVolume

api/v3/klines?symbol=WLDUSDT&interval=1d&limit=95
  → hitung sendiri: 7d = last/cl[-8]-1 · 30d = last/cl[-31]-1 · 90d = last/cl[-91]-1
    high/low 30d = max(hi[-30:]) / min(lo[-30:]) · high/low 90d = max(hi) / min(lo)
```

Ini sumber buat **"jarak harga ke high 30 hari"** — angka yang dipakai buat inferensi timing entry user
(lihat `portfolio-state-reconciliation.md`).

**Langkah 3 — dominasi makro.** `market_regime.py` bisa balik `BTC.D 0%` kalau fetch CoinGecko-nya 429,
dan verdict script-nya jadi ngawur (`BTC.D 0% | 7d -57,18pp → "tailwind ringan buat alt"`). **Jangan
pernah kutip BTC.D 0%** — itu fetch gagal, bukan angka.

```
# PRIMARY (keyless, kuota lega, satu request untuk semuanya)
https://api.coinpaprika.com/v1/global
  → market_cap_usd · bitcoin_dominance_percentage · market_cap_change_24h
https://api.coinpaprika.com/v1/tickers?limit=10
  → top N mcap: rank, symbols, quotes.USD.{price,market_cap,volume_24h,
    volume_change_24h,percent_change_24h,percent_change_7d,percent_change_30d}

# FALLBACK
https://api.coingecko.com/api/v3/global
  → data.market_cap_percentage.{btc,eth,usdt} · data.total_market_cap.usd
    · data.market_cap_change_percentage_24h_usd
```

CoinGecko 429 itu **per-IP dan bisa nempel berjam-jam sampai berhari-hari**, jadi jangan tulis "data gagal"
cuma karena `/global` dan `/coins/markets` dua-duanya 429 — pindah ke CoinPaprika dulu. Pakai
`User-Agent: Mozilla/5.0` (CoinPaprika balas 403 tanpa UA yang kelihatan browser), dan simpan hasil sukses
terakhir ke cache JSON: kalau dua sumber gagal, baca cache dan tandai `stale: true` di laporan, baru kalau
cache juga nggak ada tulis `data gagal`. Angka basi yang dilabeli basi lebih berguna daripada baris kosong,
tapi angka basi tanpa label adalah kebohongan.

## 2. Fee / mesin token — DefiLlama summary

```
https://api.llama.fi/summary/fees/<slug>?dataType=dailyFees
  → total24h, total7d, total30d, totalAllTime
```

Dipakai buat pertanyaan "token ini punya mesin apa, atau narasi doang?" — verified 3 Okt 2026:
`aster` $223,2k/24j · $0,97M/7d · $5,83M/30d · all-time $0,48B; `ondo-finance` $255,5k/$1,30M/$6,46M.
Slug ≠ ticker: `aster` (bukan `aster-dex`), `ondo-finance`. `bittensor` balas **400 Bad Request** (nggak
ada di fee-adapter) → skip, jangan ulang.

`https://api.llama.fi/emission/<slug>` balas **HTTP 402 Payment Required** di plan sekarang. Jangan
habiskan turn nge-probe endpoint ini — pakai sumber unlock di bawah.

Bandingkan fee ke mcap: fee tahunan ≈ `total30d × 12`; rasio ke mcap = P/F kasar. Mesin buyback+burn
(ASTER: 80–99% fee harian → buyback + burn) hanya berarti kalau **volume tetap jalan** — kalau volume
kering, mesinnya mati dan tesisnya balik jadi narasi.

## 3. Jadwal unlock / cliff — sumber web

- `unlocks.app` / `crypheat.com/unlock-calendar` — kalender cliff, tanggal, estimasi nilai USD.
- `tokenomist.ai/<slug>` — tokenomics, % buyback/burn, allocation, cliff vs linear release.
- Berita resmi (CoinMarketCap top stories, Yahoo/BeInCrypto) buat verifikasi klaim "emission dipotong X%"
  — jangan percaya halaman proyek sendiri.

**Dua bentuk yang harus dibedakan di laporan:**

| Bentuk | Contoh (3 Okt 2026) | Implikasi |
|---|---|---|
| Cliff bertanggal | ONDO 18 Jan 2027, 1,71B ≈ 35% MC | tanggal exit yang bisa ditulis, trim sebelumnya |
| Drip dari float rendah | ASTER float 35%, insider cliff buka 18 Sep 2026 → ±+27% circ/tahun | menjelaskan harga **flat** 30d saat peer +33–52% |

Pelajarannya: token yang **flat saat narasinya lagi panas** biasanya sedang mencerna supply, bukan
"ketinggalan" — cek unlock sebelum nyebut dia lemah.

## 4. Deteksi drift data dalam satu perintah

Sebelum narik data baru, lihat dulu apa yang script lokal benar-benar pantau — sering jadi bukti state
basi:

```
python3 ~/.hermes/scripts/holdings_watch.py --debug
```

Baris tabelnya = aset yang benar-benar dipantau. Beda dari yang user sebut ⇒ reconcile dulu
(`portfolio-state-reconciliation.md`).
