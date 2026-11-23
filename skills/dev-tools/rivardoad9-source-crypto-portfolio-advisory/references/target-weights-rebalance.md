# Rebalance dari target bobot yang user kasih (8 Okt 2026)

Trigger: setelah ngobrol soal komposisi rusak, user nulis sendiri komposisinya di chat
(*"eth 40 %, sol 20 %, 20 % tao, 20 % ondo"*). Yang dia minta: **nominal per koin + urutan eksekusi**.
Jangan tanya balik "mau gw itung?" — langsung itung, semua angka dicetak, nol kira-kira.

## 0. Cek KAPAN tiap posisi dibeli, sebelum nyusun daftar jual

Bobot doang nggak cukup buat milih siapa yang dipotong. Tarik timestamp trade per simbol dulu
(`/api/v3/myTrades`, resep di §4) untuk tiap aset yang ada di porto, lalu urutkan dari yang paling
baru dibeli.

- **Aset yang dibeli < 48 jam sebelum analisa masuk kolom TAHAN**, bukan kolom jual — kecuali dia
  melanggar cap atau grade-nya jelas paling lemah. Jual barang yang baru dibuka sejam lalu = churn:
  fee keluar dua kali, dan user baca itu sebagai plin-plan karena dia baru aja memutuskan.
- **Kas bantalan diambil dari nama yang paling lama / paling oversized**, bukan dari yang paling baru.
  Kalimatnya: *"yang gw balikin ke kas TAO/SUI yang udah 41 %, bukan LINK yang lu beli sejam lalu dan
  masih di cost."*
- **Sebut fakta entry-nya sekali** (waktu, harga beli, sekarang di cost atau berapa %) — rekomendasi
  jadi kelihatan nyambung sama riwayat dia, bukan template generik.
- Cost basis `mismatch` (ada transfer masuk) ≠ nggak ada riwayat. Trade history tetap dipakai buat
  urutan entry dan harga beli terakhir; yang nggak boleh diklaim cuma realized PnL.

## 1. Hitung delta (sumber: porto live, bukan ingatan)

`binance_porto.py --json` → `total_usd`, `rows[]` (`qty`, `price`, `usd`, `pct`, `cost.avg_cost`), `caps`.

```
target_usd[k] = total × bobot
delta         = target_usd[k] − usd[k]      → label BELI / JUAL + qty (delta / price)
```

Aset yang nggak muncul di target = **JUAL SEMUA** (sebut qty + $ + pct sekarang apa adanya).
Kerjakan dengan Python dan print tabel; jangan hitung di kepala.

## 2. Urutan eksekusi (yang diminta user setelah angkanya)

1. kas sekarang (satu baris)
2. jual habis yang keluar dari target — **yang paling tipis duluan** (meme/liq kecil), lalu mid cap
3. trim yang dipertahankan (TAO $30,59 + ONDO $10,74 di kasus nyata)
4. baru **BELI** — majors dulu (ETH), lalu yang lain; tunjukkan kas berjalan tiap langkah
5. sisa kas ±$0 + fee ≈ 0,1 % × total volume transaksi

Selalu tambah: *"kasih toleransi ±$15 per koin, jangan ngejar pas 20,00 %"* — ngejar nominal pas
bikin eksekusi kacau di market yang gerak.

## 3. Wajib disebut sebelum user eksekusi (bukan buat ngehalangin)

- **Kas 0 %.** Bandingin eksposur pasar: β porto sekarang *dengan kas dianggap β = 0* vs β target.
  Kasus nyata: sekarang **1,08x** (32 % modal nganggur), target **1,36x**. Terjemahin ke uang:
  BTC −30 % ⇒ porto sekarang ±−32 %, target ±−41 %. Rebalance bisa kelihatan "lebih rapi"
  (4 nama likuid, ada ETH core, 1 narasi bukan 2) tapi risikonya **naik**, bukan turun. Bilang gitu
  terus terang — jangan biarin dia mikir ini pengurangan risiko.
- **β per koin** (45 hari daily, vs BTC — `scripts/beta_vs_btc.py`): ETH 1,01 · ONDO 1,33 ·
  VIRTUAL 1,36 · SOL 1,38 · WLD 1,43 · **TAO 2,08** · BOME 0,95. Sebut β tertinggi di target, lalu
  satu kalimat aksi: *"geser 5 % s/d 10 % dari TAO ke ETH, β target turun ke bawah 1,3x."*
- **Bentrok sama aturan user sendiri.** Nyata: ONDO 20 % = **1,7x cap 12 %** miliknya + unlock cliff
  17 Jan 2027 (35,1 % float, 101 hari). Sebut angkanya **sekali**; jangan dipakai buat ngulang debat
  tesis yang udah selesai.
- **Timing kalau koin baru dibeli borongan.** Cek posisi vs EMA50/EMA200 4H + low 5 hari. Nyata:
  ETH $2.568,79 di bawah EMA50 (2.672) **dan** EMA200 (2.615), low 5 hari 2.538; SOL $115,98 di bawah
  EMA50 (119,22) tapi di atas EMA200 (113,29), nyender low 5 hari. Tawarin pecah 2–3 tranche
  (50 % sekarang / 25 % kalau reclaim EMA / 25 % kalau retest low) — bonusnya otomatis nyisa kas
  10–15 % yang tadi ilang di rencana 0 % kas. Kalimatnya: *struktur nggak peduli timing, entry yang peduli.*
- **Kasih time-stop ke tranche yang nunggu bounce.** Aturannya: *"kalau EMA20 nggak kesentuh dalam
  10 hari, sisa tranche dieksekusi di market"*. Tanpa batas waktu, "tunggu bounce" berubah jadi nggak
  pernah derisk — dan harga yang dimaksud nggak datang. Ini juga yang bikin sisa trim kelihatan
  terencana, bukan nunggu-ntung.

## 4. Verifikasi eksekusi — jangan pernah diklaim dari asumsi

User bisa eksekusi di chat yang sama tanpa bilang. Cek trade history dulu, baru komentar:

```python
import importlib.util
spec = importlib.util.spec_from_file_location("bp", "/home/ubuntu/.hermes/scripts/binance_porto.py")
bp = importlib.util.module_from_spec(spec); spec.loader.exec_module(bp)
key, secret = bp.load_keys()
bp.call("/api/v3/myTrades", key, secret, {"symbol": "ONDOUSDT", "limit": 8}, signed=True)
# field: time, qty, price, isBuyer, commission   (isBuyer=False → jual)
```

Kasus nyata: **jual 575,20 ONDO @ 0,4672 = $268,73, 05:18:56 WIB, fee $0,27** → realized
(0,4672 − 0,52116) × 575,20 = **−$31,04**. Laporkan waktu + qty + harga + fee + realized, plus
posisi setelahnya (575,26 ONDO = $269 = 20,8 % porto) dan porsi lama vs baru. Angka dari trade
history = bukti; "lu kayaknya udah jual" = spekulasi.
