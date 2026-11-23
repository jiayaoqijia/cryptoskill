# Probabilitas "market besok naik atau turun" — base rate, bukan ramalan

Trigger: "kasih probabilitas market besok", "besok breakout nggak", "weekend tipis, besok naik ya",
"firasat gw breakout". Jangan jawab dengan satu angka rasa. Jawab dengan base rate + kondisi + sebaran
skenario + level konfirmasi/invalidasi.

## 1. Aturan bentuk jawaban

1. **Pisahkan tiga pertanyaan** yang sering digabung user: (a) arah close besok, (b) apakah level kunci
   ditembus, (c) apakah tren baru mulai. Angka untuk (b) biasanya jauh lebih kecil dari (a), dan itulah
   koreksi yang paling berguna.
2. **Selalu sertakan baseline.** "59% naik" tidak berarti apa-apa tanpa "base rate harian 51%".
3. **Selalu sertakan n.** Sel di bawah ~30 sampel dilabeli lemah atau dibuang.
4. **Sebut horizon dan zona waktu.** Close harian BTC = 00:00 UTC; sesi ekuitas AS tutup 21:00 UTC. Satu
   hari yang sama punya dua definisi.
5. **Tutup dengan apa yang membatalkan.** Level + kondisi volume, bukan perasaan.

## 2. Cara hitung (Binance klines, keyless)

```python
# paginate dari 2017: 1000 candle/request, startTime = candle terakhir + 1 hari
# https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&startTime=...&limit=1000
# pakai open/high/low/close/volume; hitung MA20, low20, high20, vol7
cond = close < MA20 and close <= low20 * 1.03 and vol < 0.6 * mean(vol[-7:])
# lalu hitung dari semua hari yang cond=True:
#   P(close besok > close hari ini)
#   P(high besok > high20)  -> probabilitas breakout sejati
#   P(low besok <= close * 0.993) -> probabilitas level support disentuh
#   P(|close besok / close - 1| <= 0.015) -> probabilitas chop
```

Hasil yang terverifikasi (BTC 2017–Okt 2026, saat itu close $82.094, MA20 $83.395, low20 $81.491,
high20 $86.530, volume 27% dari rata-rata 7 hari):

| ukuran | angka | n |
| --- | --- | --- |
| base rate hari naik | 51,1% | 3.349 |
| base rate Senin naik | 50,8% | 478 |
| setup di atas (close<MA20, ≤3% dari low20, vol<0,6×) → besok naik | 59,3% | 108 |
| Minggu volume tipis → Senin naik | 54,1% | 148 |
| Jumat VIX ≥20 → Senin BTC naik | 61,2% | 152 |
| besok langsung tembus high20 | **1,9%** | 108 |
| besok menyentuh −0,7% | 63,0% | 108 |
| close besok dalam ±1,5% | 58,3% | 108 |
| median range harian | 3,1% | 108 |

Angka kerja yang dipakai: **57% hijau / 43% merah**, breakout 2–4%, chop 81,5k–84,5k ~58%. Itu contoh
bentuk keluaran, bukan angka yang boleh dipakai ulang tanpa hitung baru.

## 3. Pitfall yang paling mahal: alignment tanggal

Data yang sama bisa menghasilkan kesimpulan yang berlawanan kalau harinya tidak sejajar:

- "VIX naik >15% hari apa pun → BTC besok naik" = **29,2%** (n=106).
- "Jumat VIX ≥20 → Senin BTC naik" = **61,2%** (n=152).

Yang benar adalah pertanyaan user: dia trading **Senin**, bukan "besok" versi UTC. Selalu sejajarkan sinyal
ekuitas (close 21:00 UTC) ke sesi crypto yang dimaksud, dan sebut asumsinya.

Pitfall lain:
- **Jangan kutip sel n kecil.** Volume <0,35× rata-rata memberi 14,3% tapi n=7 — itu noise, bukan temuan.
- **Setup weekend bukan konfirmasi.** Range weekend tipis sering disapu di pembukaan Senin; sebut ini
  eksplisit sebelum user memasang stop ketat dari harga weekend.
- **Volume weekend 27% dari normal** adalah fakta yang menaikkan risiko fake move, bukan bukti arah.

## 4. Gabungkan dengan posisi user

Probabilitas arah bukan lampu hijau untuk menambah risiko. Cek dulu: kas %, beta tertimbang, dan apakah
posisi baru akan membuat satu salah menghapus fleksibilitas. Kalau kas 0% dan beta di atas 1,5, jawabannya
bukan "long", tapi "kalau mau ekspresi, tanpa leverage dan ukurannya kecil".

Struktur yang bisa diberikan: tunggu sesi likuid (pembukaan AS ~20:30 WIB), konfirmasi close di atas level,
invalidasi close di bawah level, target di high20 — bukan target yang dikarang.

## 5. Kalau user menyebut "base rate" dari sumber lain

Prediction market memberi harga probabilitas yang berbeda dari base rate historis; itu dua hal berbeda.
Kalau memakai Polymarket, ikuti `macroai-news-ops` → `references/polymarket-transport-and-market-selection.md`,
dan sajikan keduanya sebagai dua estimasi, bukan satu angka final.

## 6. "<ticker> paling sering balik kalau kena flush" — uji, jangan aminin

Klaim pemulihan adalah hipotesis yang bisa diukur, dan user sering membawanya sebagai keyakinan ("ini ticker yang
menurut gw potential dan kalau kena flush paling sering balik"). Jangan jawab dengan setuju atau dengan cerita 2021:
jalankan `scripts/post_flush_recovery.py UNI AAVE INJ SUI` dan sajikan tabelnya.

Dua kondisi yang dipakai, keduanya dari klines harian BTC vs alt (3 tahun):

1. **Hari flush:** BTC close ≤ −4% (n≈43 dalam 3 tahun). Hitung return alt +5/+10/+20 hari dari hari itu.
2. **Rezim koreksi:** BTC 30d ≤ −10% (n≈155 hari). Hitung return alt 20 hari ke depan. Ini yang paling dekat dengan
   "market lagi flush beberapa minggu", dan hasilnya bisa beda jauh dari tes satu-hari.

Pembacaan yang dipakai:

- **Win ~50% dengan median ~0% = tidak ada edge pemulihan**, cuma ikut market. Itu jawaban yang jujur, bukan alasan
  mencari nama lain.
- **20d win < 40% + median negatif = nama yang paling salah dijadikan kendaraan pemulihan.** Di satu run, nama yang
  user paling yakin justru paling jelek di dua tes (win 37% / median −5,3% setelah flush; win 28% / median −7,9% di
  rezim koreksi), sementara nama yang dia baru jual justru punya bounce 10 hari terbaik. Sampaikan urutannya, bukan
  cuma verdict — urutan itulah yang mengubah bobot porto.
- **Selalu cetak beta/korelasi/vol di run yang sama.** Tiga nama dengan beta 1,25–1,33 dan korelasi 0,58–0,69 bukan
  tiga posisi, tapi satu taruhan alt-beta; itu yang harus jadi rekomendasi utama (turunkan konsentrasi + sisakan kas),
  lebih dari sekadar memilih pemenang antar nama.
- **Bedakan "harga belum ikut" dari "harga sudah lari".** Nama yang di 82% rentang 1 tahun setelah +18% dalam 30 hari
  dibeli karena kekuatan harga, bukan karena pemulihan; cek posisi rentang sebelum menyusun trim, karena statistik
  pemulihan yang bagus di nama yang sudah lari tetap entry yang buruk.
- **Statistik ini tidak menjanjikan apa pun ke depan.** Ia hanya mengurutkan mana yang historisnya paling tidak buruk
  setelah flush — sebut itu eksplisit sebelum user menaikkan ukuran posisi.
