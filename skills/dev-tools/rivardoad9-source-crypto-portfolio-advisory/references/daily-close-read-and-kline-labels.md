# Baca hasil candle harian setelah tutup + label baris klines

Saudara dari `level-and-daily-close-claims.md` (cara verifikasi klaim "belum close di <level>" sebelum
candle tutup). File ini buat momen **sesudah** tutup: dia ngirim *"gmn, daily udh close nih"* sekitar
07:2x WIB. Kalau nanti digabung, section 4 & 5 di bawah ini yang pindah ke file itu.

Kontekstual: Binance candle harian open 00:00 UTC = **07:00 WIB**, jadi candle yang baru tutup
07:00 pagi itu candle yang open 07:00 WIB kemarin.

## 1. Yang dia mau: verdict + konsekuensi, bukan recap harga

Bentuk yang landed (8 Okt 2026, 07:2x WIB):

1. Baris pertama sebut candle mana: *"candle 08 Okt 07:00 WIB — semua merah, dan ONDO lu selamat tipis"*.
2. Per aset: close + % vs open, lalu posisi vs **EMA20d/EMA50d**. Nyata: BTC 83.321 (-2,60%, atas EMA50d
   80.243, bawah EMA20d 84.050) · ETH 2.574 (-4,57%, nyender EMA50d 2.555, cuma +0,7%) · SOL 116,30
   (-3,65%) · TAO 291,40 (-5,70%) · ONDO 0,4702 (-4,31%) · WLD 0,5209 (-5,57%).
3. **Level yang dia pantau dijawab eksplisit**, plus marginnya: ONDO close 0,4702 → level **0,46 nggak
   tembus** (+2,2% margin, "level masih idup"), tapi nggak ada konfirmasi naik karena di bawah EMA20d.
4. **Satu verdict + konsekuensi timing**, dengan pemicu berangka: *"ini bukan close risk-on (semua di
   bawah EMA20d kecuali SUI) → tranche 50% sekarang, bukan borong; tranche 2 kalau BTC balik > 84.050
   atau SUI/SOL reclaim EMA20d; tranche 3 kalau BTC wick 81.604 tanpa close di bawah."*

Pisahkan **komposisi** dari **timing** secara eksplisit: *"target itu soal komposisi, bukan soal arah.
Jadi tetap jalan, cuma jangan sekaligus."* Tanpa kalimat itu dia gampang kebaca close merah = batalin
rencana, atau sebaliknya borong di close merah.

## 2. Pitfall — indeks & label baris klines (kejadian nyata 8 Okt 07:24 WIB)

```python
k = get("https://api.binance.com/api/v3/klines?symbol=ONDOUSDT&interval=1d&limit=121")
closed_now = k[-2]   # k[-1] = candle yang MASIH JALAN; k[-2] = yang baru tutup
```

- **Timestamp baris klines = waktu OPEN, bukan close.** Baris `k[-2]` yang dicetak *"close 07 Oct 07:00"*
  sebenarnya candle yang **tutup 08 Okt 07:00 WIB** (open 07 Okt 07:00). Label pakai waktu TUTUP, atau
  tulis `open 07 Okt 07:00 → close 08 Okt 07:00`. Kalau nggak, dia (dan lu) bingung candle mana yang
  lagi dibahas — lu bakal ngejelasin "close kemarin" padahal itu close pagi ini.
- **Cek jam dulu** (`date`). Jam 07:0x = candle baru jalan beberapa menit → "close terakhir" adalah candle
  sebelumnya. Hati-hati juga kalau run-nya 06:5x: candle yang jalan itu milik sesi kemarin, jadi
  `k[-2]` masih candle dua hari lalu.
- Angka yang dibandingkan ke **level** harus dari baris tutup, bukan `lastPrice` ticker. Ticker = harga
  live saat itu; level dijawab pakai close.
- Jangan campur EMA harian (dari klines 1d) dengan EMA 4H dari sesi sebelumnya — sebut timeframenya.

## 3. Ringkas checklist

```
date                       # jam WIB dulu — nentuin candle mana yang "tutup terakhir"
klines 1d limit=121 → k[-2] = candle tutup terakhir (label = waktu TUTUP)
per aset: close, % vs open, EMA20d/EMA50d, jarak ke level user (%)
verdict: risk-on atau bukan? → borong atau tranche (pemicu ditulis angkanya)
kalau ada target komposisi: pisahkan komposisi vs timing
```
