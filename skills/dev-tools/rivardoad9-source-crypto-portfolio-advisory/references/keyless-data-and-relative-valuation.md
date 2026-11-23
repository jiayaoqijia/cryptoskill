# Addendum 1 Okt 2026 — fallback data keyless, valuasi relatif chain, rename ticker

Lanjutan `references/live-market-data-sources.md` §1–§7 (endpoint dasar: CoinGecko markets, Binance
klines, Fear&Greed, DefiLlama dexs/yields, GeckoTerminal pools, DexScreener, cek modal on-chain).
Tiga blok baru di bawah semuanya terpakai di sesi GRAM (TON) 1 Okt 2026.

## A. Kalau CoinGecko 429 — urutan fallback

- **Harga cadangan:** `https://coins.llama.fi/prices/current/coingecko:<id>,<id2>` → `price` + `confidence`.
- **Supply / mcap / rank:** `https://api.coinlore.net/api/tickers/?start=0&limit=100` (satu call:
  `rank`, `price_usd`, `market_cap_usd`, `csupply`, `tsupply`, `percent_change_24h/7d`).
  ⚠️ Harga CoinLore bisa **basi/skew**: TON tampil $1,60 padahal Binance & DefiLlama $1,50 → cross-check
  harga vs CEX klines yang dipakai buat tren; CoinLore dipakai buat **supply/mcap** aja. Nggak ada
  filter symbol (`?search=gram` balikin top-100) → saring sendiri di Python.
- **Tren / MA / vol realized:** Binance klines (`api.binance.com/api/v3/klines?symbol=<X>USDT&interval=1d`).
  Aset hasil rename dapat symbol baru (`GRAMUSDT`, listing 2 Jul 2026 → cuma ~92 candle harian): tandai
  "data parsial", jangan sebut MA100 seolah setahun.
- **ID CoinGecko nggak ikut ganti nama:** TON→GRAM tetap `the-open-network`, `symbol` = `gram`,
  name = "Gram (prev. Toncoin)". Verifikasi dari respons, jangan nebak id dari ticker baru.
- 429 itu **sementara** — `sleep(6)` × 3–4 percobaan akhirnya lolos. Jangan permanen ganti sumber
  gara-gara sekali 429.

## B. Valuasi relatif: mcap vs TVL chain vs fee chain (wajib sebaris peer)

- `https://api.llama.fi/v2/chains` (TVL semua chain, 1 call) ·
  `https://api.llama.fi/v2/historicalChainTvl/<CHAIN>` (riwayat + ATH TVL → "turun berapa % dari puncak").
- `https://api.llama.fi/overview/fees/<chain>?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true&dataType=dailyFees`
  → `total24h/7d/30d/1y`; `dataType=dailyRevenue` buat bagian yang diklaim chain.
- Dua rasio yang dipakai, **selalu sebaris 4–5 peer** (1 Okt 2026):

  | | mcap | TVL chain | mcap/TVL | mcap/fee 1y |
  |---|---|---|---|---|
  | ETH | $328,9B | $53,2B | 6,2x | 70,2x |
  | SOL | $64,2B | $6,5B | 9,8x | 17,4x |
  | BNB | $107,0B | $5,7B | 18,8x | 133x |
  | TRX | $32,0B | $5,7B | 5,7x | 389x |
  | HYPE | $29,8B | $1,2B | 24,6x | – |
  | GRAM | $4,2B | **$54,3M** | **78x** | **10,5x** |

  Punchline yang dipakai: sisi **fee** murah (10,5x), sisi **pemakaian on-chain** mahal (78x) ⇒ harganya
  premium atas narasi/distribusi, bukan atas aktivitas → verdict "watchlist, bukan taruhan upside".
- ⚠️ `dailyRevenue` sebuah chain bisa **hampir nol** (TON $18,4rb/hari — fee habis ke validator): jangan
  print fee chain sebagai "value accrual token".
- **Supply overhang:** `https://defillama.com/unlocks/<chain>` (halaman, bukan endpoint) + catatan riset
  pihak ketiga. TON: Believers Fund ±37 jt GRAM/bulan (event ke-15 dari 39; berikutnya 23 Okt 2026 =
  $54,9 jt ≈ 1,3% float) + cliff "Inactive Miners" **1.081 m GRAM** satu event (Feb 2027).
- **Staking native TON:** `https://tonapi.io/v2/staking/pools` → 1.080 pool dengan `total_amount` + `apy`
  (median 21%; Tonstakers 132,3 jt GRAM @16,03%). Yield tinggi **tapi dibayar dalam token yang
  max-supply-nya ∞** ⇒ itu dilusi, bukan free money. Jangan jual sebagai "APY 20%".

## C. Rename ticker ≠ swap (koreksi di awal laporan)

TON→GRAM (15 Jun 2026, vote TON Vote 81,22%): **kontrak sama, chain sama (The Open Network tetap TON),
1:1, tanpa token baru / migration / claim.** Istilah "swap" cuma bahasa exchange (KuCoin dkk: "TON swap
to GRAM 1:1"). Kalau user nyebut "token Gram yang swapped dari TON", koreksi duluan — dan tekankan
**nggak ada halaman claim/migrate GRAM yang sah; semua itu wallet drainer.**

## D. Verifikasi trade LP yang diklaim di post/screenshot

Rebuild timeline dari candle 1 menit (GeckoTerminal pool OHLCV + `before_timestamp` = batas ATAS
eksklusif), konversi harga USD → unit pool pakai klines 1 menit aset quote, lalu cek PnL vs claimable
fee vs angka "APR" UI dan daftar yang nggak bisa dibuktiin (nggak ada wallet/tx). Resep lengkap:
skill `defi-platform-due-diligence`, `references/lp-trade-claim-forensics.md`.
