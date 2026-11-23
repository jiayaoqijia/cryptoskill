# Sumber data live + jebakannya (verified 28 Sep 2026)

Semua endpoint di bawah **keyless** dan sudah dipakai sukses. Script siap jalan:
`scripts/market_snapshot.py` (harga + MA + vol + Fear&Greed) dan `scripts/solana_pool_scan.py` (pool LP).

## 1. Harga / mcap / %ATH — CoinGecko

```
https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=<id1>,<id2>
  &price_change_percentage=24h,7d&order=market_cap_desc
```
- **`price_change_percentage=...` WAJIB.** Tanpa itu `price_change_percentage_7d_in_currency` = `None`
  → kalau formatter-fallback-nya `0` atau `0.0%`, laporan lu **ngarang** angka ("7d datar" padahal
  datanya nggak ada). Kejadian nyata: 8 aset nampil "7d 0,0%" sebelum parameternya dipasang.
- ID ≠ symbol. Yang benar: `ondo-finance` (bukan `ondo`), `injective-protocol`, `quant-network`,
  `theta-token`, `hyperliquid`, `telcoin`. Salah id → aset hilang diam-diam dari respons.
- Rate limit: 429 gampang kena kalau dipanggil berulang cepat. Kasih `time.sleep(3–6)` + retry
  backoff; jangan paralel. Kalau 429, tunggu — bukan tanda endpoint mati.
- Per-aset detail (klaim vs mekanisme, supply) → `/coins/{id}` (lebih besar, pakai hemat).

## 2. MA20/MA50, % rentang 30h, vol realized — Binance klines

```
https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=100
```
Hitung di Python dari close/high/low: MA20, MA50, gap ke MA (%), posisi di rentang 30 hari
(`(last-lo)/(hi-lo)`), `ch30d`, dan vol realized = `pstdev(return 30h) * sqrt(365)`.
- Symbol yang kepakai: BTC, ETH, SOL, INJ, ONDO, NEAR, UNI, LINK, QNT, HYPE, THETA (semua `…USDT`).
- **Aset yang baru listing** (mis. HYPE di Binance) cuma punya sedikit candle → MA20/MA50 `n/a` dan
  `pos30d` menyesatkan. Kalau sejarahnya pendek, tandai "data parsial" dan pakai CoinGecko untuk %ATH.
- **Gap MA20 adalah tes "udah lari belum"** yang paling berguna: QNT +187,8% dari MA20 = dibayar di muka;
  aset dengan gap kecil + katalis bertanggal = kandidat.

## 3. Sentimen — Fear & Greed

`https://api.alternative.me/fng/?limit=8` → `data[0].value`. 70–79 = Greed (jangan nambah posisi baru),
≥75 = Extreme Greed. Bandingkan dengan 7 hari sebelumnya untuk tahu suhu naik atau turun.

## 4. Trend volume (regime) — DefiLlama

- Total: `https://api.llama.fi/overview/dexs?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true`
- Per chain: `https://api.llama.fi/overview/dexs/solana?...` (sama parameternya)

Yang dibaca: `total24h` + **`change_7d`**. Volume DEX turun (mis. Solana −32% 7h) = regime meme/LP
mendingin → kecilin sleeve LP dan bilang apa adanya, jangan jual mimpi fee/TVL tinggi.
`https://yields.llama.fi/pools` untuk APY stable/staking (filter `tvlUsd > 20e6`, `stablecoin`).

## 5. Pool LP Solana — GeckoTerminal (pengganti Meteora datapi)

```
https://api.geckoterminal.com/api/v2/networks/solana/pools?sort=h24_volume_usd_desc&page=1
https://api.geckoterminal.com/api/v2/networks/solana/trending_pools?page=1
```
- Balikin `data[].attributes`: `reserve_in_usd` (TVL), `volume_usd.{h1,h6,h24}`, `price_change_percentage.h24`,
  `pool_fee`/`fee_tier`, `address`. Butuh header `User-Agent` + `Accept: application/json`.
- **Coverage = vol24 / TVL** (proxy fee/TVL). Band praktis: TVL ≥ $30–40k & vol24 ≥ $8–10k.
  Pool cov 20–90x (mis. e/acc-SOL 27,8x) = masih hidup; **cov 200–300x+ dengan TVL < $150k = spike
  token baru** — jangan dianggap "pool terbaik".
- Page 2+ gampang 429 → bikin 1–2 halaman saja, dedupe nama pool.
- Endpoint `dlmm-api.meteora.ag/pair/*` dan `amm-v2.meteora.ag/pools` balas **404** (skema pindah) —
  jangan habiskan turn nge-probe; GeckoTerminal udah cukup buat screening kasar. Detail bin/range
  tetap dari UI Meteora kalau mau eksekusi.

## 6. Token kecil / memecoin — DexScreener

`https://api.dexscreener.com/latest/dex/tokens/<mint>` → sortir `pairs` by `liquidity.usd`.
Yang dibaca: `priceUsd`, `marketCap`, `liquidity.usd` (**per pool**, jumlahkan), `volume.{h6,h24}`,
`priceChange.{h6,h24}`, `txns.h24`, `pairCreatedAt`. Ini yang dipakai buat PAID (pump.fun mint).
**Cek likuiditas per pool, bukan cuma yang tertinggi** — pool kecil yang likuiditasnya turun = tanda LP ditarik.

## 7. Cek modal on-chain (sebelum ngasih alokasi)

- Saldo: `node ~/.hermes/scripts/diag/fm_balance_check.mjs` (baca saldo + jumlah token non-zero;
  baris **"vs modal" pakai konstanta `SOL_DEPOSITS` hardcode — itu bukan P&L**).
- Jejak transaksi: `getSignaturesForAddress(wallet, {limit:N})` → tiap sig `getParsedTransaction`
  dengan `maxSupportedTransactionVersion: 0`, lalu print **Δ saldo wallet** (`meta.preBalances`/
  `postBalances` pada index wallet) + `meta.fee` + program yang dipakai. Program `11111111111111111111`
  (System) doang = transfer SOL biasa (bukan swap/LP) → cek wallet penerimanya; kalau penerima
  langsung nge-fan-out dalam beberapa menit, itu dompet relay (kemungkinan on-ramp ke CEX).
- `~/.hermes/data/fm_manual_positions.json` = posisi LP manual operator. `positions: []` artinya
  **nggak ada LP deployed**, apa pun kata catatan lama.
- Ledger strategi (`~/flowmetrix-ai-agent/data/signal-ledger.jsonl`): hitung baris + berapa yang punya
  outcome. Mayoritas `SKIP` dan **0 outcome** = belum ada bukti edge → sleeve LP tetap terkunci.

## 8. Makro live (VIX, UST, oil, DXY, ekuitas, gold, ES) — TradingView scanner

Keyless, satu request untuk sepuluh simbol. Ini yang dipakai kalau pertanyaan market butuh konteks makro
(risk-off, VIX, yield, oil) — bukan cuma harga koin.

```python
payload = {"symbols": {"tickers": ["CBOE:VIX","TVC:US10Y","TVC:US02Y","NYMEX:CL1!","NYMEX:BZ1!",
           "TVC:DXY","AMEX:SPY","AMEX:XLF","COMEX:GC1!","CME_MINI:ES1!"], "query": {"types": []}},
           "columns": ["close","change","Perf.W","Perf.1M","High.3M","High.6M"]}
# POST https://scanner.tradingview.com/global/scan  (headers: Content-Type, Origin/Referer tradingview.com)
# hasil: data[].s = ticker, data[].d = nilai sesuai urutan columns
```

Mapping yang benar (bukan simbol Yahoo): `^VIX`→`CBOE:VIX`, `^TNX`→`TVC:US10Y`, `CL=F`→`NYMEX:CL1!`,
`BZ=F`→`NYMEX:BZ1!`, `DX-Y.NYB`→`TVC:DXY`, `ES=F`→`CME_MINI:ES1!`, `XLF`→`AMEX:XLF`, `GC=F`→`COMEX:GC1!`.
`change` = % sesi berjalan; `Perf.W`/`Perf.1M` = % seminggu/sebulan; `High.3M` dipakai untuk menguji klaim
"high 4 bulan" (kalau high 3 bulan sama dengan harga hari ini, klaimnya cuma high 3 bulan).

- **Jangan habiskan turn di sumber yang memblokir.** Dari IP VPS ini Yahoo Finance balas 429 untuk semua
  simbol, Stooq balas 404, dan CSV FRED timeout. Satu percobaan masing-masing, lalu pindah ke scanner.
- Angka futures di luar sesi bisa tertinggal; sebut itu saat mengutip ("ES futures, sesi Jumat").
- Aliran dana ETF tetap dari Farside (`farside.co.uk/eth/`, `/sol/`, `/btc/`), parse baris `<tr>` dengan regex
  (`pandas` tidak ada di python sistem). Jumlahkan baris harian sendiri; **baris `Total` bukan net flow**.
