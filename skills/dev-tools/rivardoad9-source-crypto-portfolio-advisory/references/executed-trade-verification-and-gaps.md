# Verifikasi eksekusi Binance + laporkan gap vs rencana (8 Okt 2026)

Trigger: user bilang *"gw dah update porto"* / *"udah eksekusi"* — atau tiba-tiba komposisinya berubah
tanpa dia cerita. Deliverable-nya: **leg-by-leg apa yang benar-benar terjadi + komposisi live + gap
terhadap target**, bukan ringkasan "sudah sesuai rencana".
Pelengkap `target-weights-rebalance.md` (§4 caranya) dan `portfolio-state-reconciliation.md`.

## 1. Ambil buktinya, dua sumber, jangan salah satu

```python
import importlib.util
spec = importlib.util.spec_from_file_location("bp", "/home/ubuntu/.hermes/scripts/binance_porto.py")
bp = importlib.util.module_from_spec(spec); spec.loader.exec_module(bp)
key, secret = bp.load_keys()
bp.call("/api/v3/myTrades", key, secret, {"symbol": "TAOUSDT", "limit": 20}, signed=True)
# field: time, qty, price, isBuyer, commission  (isBuyer=False → jual)
# saldo: bp.build() / `/api/v3/account` → balances non-nol
```

Laporkan per leg: **jam WIB · qty · harga · USD · realized**. Contoh nyata (jam 07:33–07:41 WIB):

| aksi | qty | harga | USD | realized |
|---|---|---|---|---|
| JUAL ONDO | 575,2 | 0,4707 | $270,75 | −$29,02 (avg 0,5212) |
| JUAL WLD | 379,5 | 0,5256 | $199,47 | −$17,10 |
| BELI TAO | 0,3443 | 290,40 | $99,98 | — |
| BELI SUI | 228,8 | 1,1365 | $260,05 | — (6 fill kecil) |

Total realized hari itu ≈ **−$77,2** + fee ±$0,74 (ONDO dijual dua gelombang: −$31,04 jam 05:18 dan
−$29,02 jam 07:33 — **pisahkan gelombangnya**, jangan digabung jadi satu angka tanpa konteks).
Banyak fill kecil dalam satu menit itu normal (user pecah order), bukan eksekusi gagal — sebut
jumlah fill-nya supaya kelihatan rapi.

## 2. PITFALL: eksekusi user ≠ kartu rencana (jangan diasumsikan)

Kartu bilang SOL 30 / SUI 20 / TAO 20 / kas 30 + jual semua ONDO/WLD/VIRTUAL/BOME. Yang benar-benar
dieksekusi: ONDO ✓ keluar, WLD ✓ keluar, SUI ✓ dibeli, TAO ditambah (jadi 30,1 % bukan 20 %),
**SOL tidak dibeli sama sekali**, VIRTUAL + BOME masih dipegang (walaupun VIRTUAL dijual 1,5 jam
kemudian di 0,7708). Bentuk laporan yang dipakai user:

- komposisi live (kas · TAO · SUI · sisa kecil) dengan $ dan %
- **gap vs target sebagai daftar**: "SUI 19,9 % → pas ✓ · TAO 30,1 % → kelebihan $132 · SOL masih 0
  (target $391) · VIRTUAL+BOME masih nyangkut $120,6"
- langkah penutupnya kalau mau rapi (jual sisa → trim → beli), dengan kas akhir setelah tiap langkah
- **satu pertanyaan** yang cuma dia tahu jawabannya: *"SOL-nya kelewat apa lu batalkan sengaja?"* —
  jangan menuduh dia salah eksekusi, dan jangan mengarang alasan di kepalanya.

## 3. PITFALL: Binance **Convert** tidak muncul di `/api/v3/myTrades`

Rekonstruksi avg-cost murni dari myTrades melaporkan **sisa 1,05 SOL (cost $121,32)** padahal saldo
live SOL = **0**. Penyebabnya: penjualan/konversi lewat fitur **Convert** (dan transfer keluar) tidak
tercatat sebagai trade — jadi residu versi myTrades itu hantu. Aturan keras: **sebelum melaporkan
posisi sisa / realized, rekonsiliasi ke saldo live** (`/api/v3/account`, buang yang nol). Kalau
myTrades bilang punya X dan akun bilang 0, X keluar dari buku lewat jalur lain — sebut itu, jangan
laporkan X.

## 4. PITFALL: target persentase user bisa berjumlah ≠ 100 %

User menulis *"30, 20 tao 20 sui, 20cash"* = **90 %**. Jangan mengarang ke mana 10 % perginya, dan
jangan pura-pura tidak lihat. Pola yang dipakai: **sisa otomatis ke kas**, nyatakan dalam satu baris
(*"30+20+20+20 = 90, jadi 10 % sisa gw taro di kas → kasnya 30 %, bukan 20 %"*), lalu tawarkan **satu
alternatif konkret dengan angka** (*"kalau 10 % itu mau masuk SOL — jadi SOL 40 — bilang"*). Jangan
tutup dengan "mau gw hitung ulang?".

Efek sampingnya berguna: kas yang naik otomatis menyediakan amunisi tranche — hitung β totalnya
(beta_vs_btc.py per koin × bobot, kas dianggap β 0) dan sebutkan: β ex-kas 1,41 → dengan kas 30 %
porto ≈ **0,98** ⇒ BTC −20 % berarti ±−20 % untuk porto, bukan −28 %. Ini yang membuat user nyaman
memegang kas.

## 5. Kalau user menolak satu nama (mis. "SOL gw ngerasa masih bisa ke bawah")

Jangan debat, jangan juga langsung setuju. Uji tesisnya ke data live, sebut yang **mendukung** dia
(Stoch weekly overbought, dua kali ditolak di zona 118–126, +22 % dari low 3 minggu → retest itu
normal) lalu beri **struktur konteks** yang tidak dia lihat (susunan weekly masih bullish = istirahat
di uptrend, bukan trend rusak). Output-nya bukan opini: **trigger level + level invalidasi**, mis.
SOL tranche 1 di 110–111 (EMA6 weekly + EMA50d numpuk), tranche 2 di 99–100 (EMA13 weekly), tesis
batal kalau weekly close < 95,8 (low 30 hari), dan area murah dianggap selesai kalau daily close di
atas EMA20d. Setelah itu baru kartu/target diupdate — biar "nunggu" punya angka, bukan cuma feeling.
