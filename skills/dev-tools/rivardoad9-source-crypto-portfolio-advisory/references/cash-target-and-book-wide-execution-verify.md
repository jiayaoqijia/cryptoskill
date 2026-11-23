# Kas sebagai target + verifikasi eksekusi satu buku penuh (8 Okt 2026, sesi siang)

Lanjutan `target-weights-rebalance.md` dan `composition-revision-and-holdings-pick.md`. Dua hal baru
yang muncul setelah user merevisi komposisi dan mengeksekusi sendiri di chat.

## 1. Bobot yang user sebut sering nggak berjumlah 100 % — jangan diisi sendiri

Kejadian nyata: dia nulis *"30, 20 tao 20 sui, 20cash"* = **90 %**. Aturannya:

1. **Jumlahkan dulu** bobot yang dia sebut, cetak totalnya di baris pertama jawaban; jangan langsung
   dipakai sebagai 100 %.
2. Selisihnya **taruh di kas** (default paling konservatif — bukan ngarang bobot baru buat koin), dan
   bilang apa adanya: *"30+20+20+20 = 90, jadi 10 % sisa gw taro di kas juga → kas 30 %, bukan 20 %.
   Kalau 10 % itu mau masuk SOL (SOL 40), bilang."*
3. **Kas jadi target kelas satu**, bukan cuma sisa. Begitu dia minta kas, masuk konfigurasi sebagai
   `KAS_TARGET` + guard *"kas dijaga min X %"* — tanpa itu kartu bakal ngabisin semua kas jadi $0.
4. **Settle kas sekali di akhir, jangan di dalam loop delta.** Bug nyata: kas dikurangi di dalam loop,
   lalu guard `kas − total_buy < min_kas` dobel-ngitung → semua porsi beli ke-skala jadi **$0** dan kartu
   nyetak `BELI: SOL $0`. Pola benar: loop cuma kumpulin delta (+kas dari trim), `kas_akhir = kas −
   total_buy` satu kali, guard diskalakan dari `kas − min_kas`. **Test wajib:** jalanin `--json` dan cek
   `beli` nggak nol / nggak kelebihan sebelum kartu dikirim.
5. **Kas besar = beta turun, sebut angkanya.** SOL30/SUI20/TAO20 + kas 30 % → beta buku **0,98**
   (BTC −20 % ⇒ porto ±−20 %) vs **1,41** kalau full-invest. Framing kas: *bantalan + amunisi beli pas
   flush*, bukan modal nganggur.

## 2. "gw dah update porto" = verifikasi satu buku penuh, bukan satu simbol

Dia bilang *"gw dah update porto"* — itu pemicunya. Jangan percaya dan jangan cuma cek 1–2 koin:

```python
# loop SEMUA simbol relevan (yang keluar + target + yang nggak dia sebut)
bp.call("/api/v3/myTrades", k, s, {"symbol": sym, "limit": 1000, "fromId": fid}, signed=True)
```

Cetak per-trade `HH:MM:SS · JUAL/BELI · qty @ harga = $ · fee`, lalu ringkas realized per nama
(average-cost replay), baru tabel posisi sekarang + gap vs target per koin.

Temuan nyata: yang dia kerjain cuma **jual ONDO + WLD (realized −$60,1 dan −$17,1)**, **beli SUI $260**,
**tambah TAO $100 (jadi 30,1 %)**, sementara **SOL belum dibeli** dan VIRTUAL/BOME masih nyangkut.
Kalau gw cuma cek ONDO/WLD, gw bakal bilang "beres" — padahal 3 item rencana belum jalan.

**Batas kepercayaan `myTrades`:** Binance Convert, transfer keluar, dan withdrawal **nggak muncul** di
`/api/v3/myTrades`, jadi replay bisa nyisa qty hantu (kasus: SOL 1,05 di replay, **0** di
`/api/v3/account`). **Saldo live yang menang** soal kepemilikan; `myTrades` = bukti apa yang ditrade.

## 3. Bentuk laporan yang landed

`trade history` (per-trade + realized) → `posisi live` (qty, $, %) → `gap vs target per koin`
(✓ / kelebihan $X / belum dibeli) → **satu pertanyaan uang yang beneran nggantung** (*"SOL-nya kelewat
apa lu batalkan sengaja? Kalau iya, targetnya gw ganti, bukan gw paksa"*). Bukan daftar pertanyaan, dan
jangan nge-push di koin yang dia udah putusin masuk — sebut fakta, sisanya dia.
