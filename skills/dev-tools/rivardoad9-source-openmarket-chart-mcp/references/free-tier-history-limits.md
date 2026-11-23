# Batas sejarah candle di plan Free (dan cara nuruninnya)

Diverifikasi 11 Okt 2026 di akun Zemiz_11 (plan Free).

## Gejalanya

`points` dan `metric_get` balikin `{"error": "tier_forbidden"}`. Pesan detailnya ngebocorin batasnya:
`served_window_hours: 167`, `longest_interval: HOUR` — artinya plan Free cuma ngladenin ~167 jam
(sekitar 7 hari) sejarah candle, dan cuma sampai interval HOUR.

Yang kena (bukan bug, bukan salah param):

- `points` interval `DAY` buat lookback apa pun (`90d`, `180d`, `365d`) → `tier_forbidden`.
- `points` interval `HOUR` dengan lookback `30d`/`60d`/`90d` → `tier_forbidden`. Lookback pendek (<=7d) aman.
- `metric_get` di `selector.interval: DAY` → `ema` period 13 udah butuh 64 bar harian, langsung ditolak
  (`needed: 64`, `window_hours: 1536`, `served_window_hours: 167`). Jangan buang call ke sini buat analisa harian.

Yang masih jalan: `metric_get` di interval `HOUR` (indikator + feed value: `funding_rate`,
`open_interest`, `open_interest_delta_pct`, `taker_buy_ratio`, `cvd`, `book_imbalance`, `atr`).
Ini yang dipakai buat baca positioning, bukan buat tren harian.

## Jalan keluarnya: API publik Binance (tanpa auth, tanpa key)

Kalau butuh candle harian atau sejarah panjang, jangan maksa OpenMarket. Pakai REST publik Binance
langsung dari server (`urllib` cukup, host ini bisa keluar):

```
futures : https://fapi.binance.com/fapi/v1/klines?symbol=PUMPUSDT&interval=1d&limit=400
spot    : https://api.binance.com/api/v3/klines?symbol=PUMPUSDT&interval=1d&limit=400
```

Bentuk baris: `[openTime_ms, o, h, l, c, volume, closeTime_ms, quoteVolume, trades, ...]` —
indeks 4 = close, indeks 7 = volume quote (USDT). Cukup buat hitung EMA 13/21/33/50/100/200,
RSI Wilder, ATR, Stoch RSI, swing high/low, dan rasio volume.

Catatan: batas `limit` 400 bar harian ≈ 13 bulan. Timestamp bar terakhir bisa bar yang belum tutup,
jadi sebut tanggalnya pas lapor ke user.

## Urutan kerja yang aman

1. Cek harga + struktur pendek pakai OpenMarket (`metric_get` HOUR) — tetap butuh angka venue live.
2. Kalau user nanya EMA harian / tren jangka panjang, ambil klines Binance dulu, baru hitung sendiri.
3. Jangan pernah njawab pertanyaan tren harian dari gambar chart user doang: angka di chart user itu
   level yang dia incer, bukan verifikasi. Selalu cek harga live.
