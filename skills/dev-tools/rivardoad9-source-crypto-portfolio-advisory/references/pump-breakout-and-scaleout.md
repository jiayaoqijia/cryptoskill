# Cabang NAiK: atribusi pump + rencana scale-out (verified 1 Okt 2026, kasus ALICE)

Pasangan dari `references/price-move-attribution.md` (yang fokus DUMP). Trigger di sini:
"kenapa X naik", "gw barusan TP <token>", "harga sekarang udah +X%", "sisa posisi gw gimana".
Langkahnya sama (ukur dulu → cari katalis → struktur), tapi ada metrik yang cuma relevan di sisi naik:
**posisi futures (OI + funding)** — itu yang membedakan pump berkelanjutan dari short squeeze.

## Langkah 0 — harga WAJIB dari API, bukan dari hasil search

Snippet web search (halaman agregator cached, post Binance Square lama, halaman "price prediction")
bisa **basi jauh** dari spot. Kasus ALICE 1 Okt 2026: snippet nulis $0,12–0,17 sementara spot
**$0,2338**; satu post Square nyebut $0,284. Aturan: search cuma buat **tanggal/headline**, harga selalu
dari `api.binance.com/api/v3/ticker/24hr` + `klines`. Kalau user nyebut angka yang beda jauh dari spot,
tunjukkan dua-duanya dan jelaskan gap-nya.

Ambil: spot 24j (harga, %, high/low, quote volume, jumlah trade) · klines **4h / 1d / 1w ±30 candle**
(base range + high multi-minggu) · MC = circulating × harga · dan kalau tokennya on-chain, saldo wallet
user via RPC (jangan cuma percaya catatan buku).

## Langkah 1 — idiosinkratik atau beta?

Bandingkan %24j token vs BTC + 2 peer sektor. Flat semuanya tapi token +40% → idiosinkratik, lanjut.
Kasus ALICE: BTC +0,17% · TAO +1,38% · ONDO −1,18% vs ALICE **+43,0%** = murni token, bukan market.

## Langkah 2 — posisi futures: OI + funding (langkah penentu)

```python
https://fapi.binance.com/fapi/v1/premiumIndex?symbol=ALICEUSDT          # lastFundingRate
https://fapi.binance.com/fapi/v1/openInterest?symbol=ALICEUSDT          # OI sekarang
https://fapi.binance.com/futures/data/openInterestHist?symbol=ALICEUSDT&period=1h&limit=8
```

Cara baca:
- **OI naik tajam + funding netral/positif** → duit BARU masuk dua arah (long & short baru) — **bukan**
  short squeeze. ALICE: OI 20,5 jt → 33,18 jt ALICE (**+61%** dalam sehari), funding **+0,005%** ≈ netral.
- **Funding negatif ekstrem + OI spike** → short squeeze; geraknya cepat balik begitu short habis.
- **Tanda distribusi**: funding naik (>+0,05%/8 jam) + OI naik terus **sambil harga mandek** → cabut.
- Volume spot juga dicek: ~4x rata-rata harian + jumlah trade besar (123.299) = partisipasi luas, bukan
  satu candle tipis.

## Langkah 3 — struktur: level yang bisa dipakai, bukan "naik banyak"

Tulis eksplisit: **base range** pra-breakout · level **breakout = retest support** · **high multi-minggu
= supply berikutnya** · low multi-minggu · MC (low cap ⇒ gerak 40% itu murah, bukan tanda kualitas).
Kasus ALICE: base 12 hari **$0,1400–0,1754** (breakout di atas $0,175) · high 30 minggu **$0,2652** =
resistance berikutnya, cuma 12% dari harga · low 30 minggu $0,0931 · MC ~$23 jt · harga saat itu $0,2338.

## Langkah 4 — katalis: "nggak ada headline" itu jawaban sah, dan artinya momentum

Cari announcement exchange, blog proyek, Medium, X. Kalau kosong → katakan **"ini murni breakout
volume/OI, bukan re-rating fundamental — anggap momentum"**. Jangan dipaksa jadi narasi, jangan di-skip.

## Langkah 5 — user bilang sudah TP sebagian → konfirmasi angka + rencana sisa

(a) **Konfirmasi pakai angka**, bukan pujian: "+50% dari $0,2338 = entry ~$0,156 — persis tengah base
12 hari, jadi TP lu kena di harga sekarang". Hitung aritmatikanya di depan user (entry di-implikasi dari
level, labeli sebagai implikasi, bukan entry yang diklaim).

(b) **Rencana sisa posisi** (yang ini deliverable-nya):
1. **Trail stop di level breakout yang baru ditembus** (ALICE: $0,175). Kill kalau daily close balik di
   bawah level itu — garis mati, bukan saran.
2. Alternatif lebih kencang: stop di atas separuh body breakout ($0,196–0,20).
3. **Tranche jual berikutnya di supply besar** (high multi-minggu, ALICE $0,265), bukan di angka bulat.
4. Ulangi **tanda distribusi** dari Langkah 2 sebagai trigger cabut sisa posisi.

(c) **Jangan tutup dengan "mau gw buatkan?"** Kalau posisinya tidak ada di vault (kasus ALICE: masuk
portofolio dari obrolan, bukan dari note alokasi v4), katakan terus terang dan minta **entry + size**
supaya bisa di-log dan dipasang watch delta (notifikasi hanya saat ada perubahan).

## Pitfall spesifik cabang naik

- **Nyebut "TP lu bagus" tanpa angka.** Pujian tanpa aritmatika tidak berguna buat trader; user ini
  secara eksplisit minta konfirmasi berbasis angka.
- **Nyampur harga spot dan harga futures.** Mark price futures beda tipis dari spot (ALICE: 0,2335 vs
  0,2338) — sebut mana yang dipakai kalau mengutip level.
- **Menyimpulkan squeeze dari harga saja.** Squeeze butuh bukti funding negatif ekstrem, bukan cuma candle
  vertikal.
- **Ngelapor tanpa cek peer.** Pump +40% di hari market flat adalah fakta kuat; tanpa pembanding, klaim
  idiosinkratik cuma opini.
