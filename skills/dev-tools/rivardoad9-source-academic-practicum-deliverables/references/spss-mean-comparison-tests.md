# Uji beda rata-rata untuk lembar jawaban (SPSS-shaped output)

Topik yang berulang di modul statistik: dua kelompok dibandingkan, user diminta mengisi tabel output
kosong dan menafsirkannya. Yang dinilai bukan cuma angka, tapi kemampuan memilih uji dan membaca baris
yang benar.

## Memilih uji

| Desain | Uji | Alasan yang harus ditulis |
|---|---|---|
| Dua kelompok orang berbeda, masing-masing satu kondisi | Independent samples t-test | Observasi saling bebas; tiap subjek hanya di satu kelompok |
| Subjek sama diukur dua kali (sebelum/sesudah) | Paired samples t-test | Pengukuran berulang pada subjek yang sama; subjek jadi kontrol bagi dirinya |
| Dua kelompok, tapi varians jelas beda | Independent + koreksi Welch | Asumsi varians homogen tidak terpenuhi |
| Satu kelompok vs nilai target | One-sample t-test | Membandingkan rata-rata dengan konstanta |

Randomisasi adalah alasan yang membuat hasil bisa dikaitkan ke perlakuan. Kalau subjek memilih sendiri
kelompoknya, selisih yang muncul tidak bisa ditafsirkan sebagai efek perlakuan (bias seleksi) — ini
pertanyaan yang hampir selalu muncul di bagian “Langkah” modul.

## Alur membaca output dua baris

1. Lihat **Levene’s Test** dulu: `Sig. ≤ 0.05` → varians tidak homogen → baca baris kedua
   (`Equal variances not assumed`). `Sig. > 0.05` → baris pertama.
2. Baru lihat `Sig. (2-tailed)` di baris yang dipilih. Itu yang menentukan tolak/tidak.
3. Tulis alasannya di jawaban. Nilai t dan df kedua baris hampir sama, jadi dosen mencari kalimat alasan,
   bukan angkanya.

Efek samping yang wajib dijelaskan: df pada baris Welch menjadi pecahan (mis. 27.892) karena koreksi
Welch–Satterthwaite menghitung df dari kombinasi varians dan n, bukan dari n total. Df lebih kecil →
distribusi t lebih lebar → uji lebih konservatif.

Kekeliruan klasik yang layak dibahas di jawaban: membaca baris pertama (angka lebih kecil, tampak “lebih
signifikan”) padahal Levene menolak homogenitas — itu jalan menuju kesalahan Tipe I.

## Pemetaan scipy → kolom SPSS

```python
from scipy import stats

d = [a - b for a, b in zip(after, before)]          # paired: selisih per subjek

stats.levene(a, b, center="mean")                    # SPSS "Based on Mean" (default scipy = median!)
stats.ttest_ind(a, b, equal_var=True)                # baris Equal variances assumed
stats.ttest_ind(a, b, equal_var=False)               # baris Equal variances not assumed (Welch)
stats.ttest_rel(after, before)                       # paired
stats.ttest_1samp(d, 0)                              # harus identik dengan ttest_rel di atas
```

`ttest_ind(...).df` memberi df Welch, bukan n1+n2-2. Interval kepercayaan tidak dikembalikan scipy:
hitung manual dengan `stats.t.ppf(.975, df) * se`, dan laporkan batas bawah–atas.

Effect size untuk dua kelompok independen = `|mean diff| / pooled SD`; sebutkan besar-kecilnya
(±0.2 kecil, 0.5 sedang, 0.8 besar) karena “signifikan” saja tidak menjawab nilai praktisnya.

## Kalimat pelaporan yang dipakai

> Rata-rata X pada kelompok A (M = …, SD = …, n = …) berbeda signifikan dengan kelompok B
> (M = …, SD = …), t(df) = …, p = …, selisih rata-rata = … (95% CI [ …, … ]).

Untuk desain berpasangan tambahkan arah dan persentase: “… atau sekitar 11 persen lebih cepat”.

## Jebakan interpretasi

- **`p = .000` bukan nol.** Itu pembulatan tiga desimal; laporkan `p < .001`. p juga bukan peluang
  kesimpulan salah — itu peluang data seekstrem ini bila H₀ benar. Dua kekeliruan ini sering jadi butir
  soal tersendiri.
- **Signifikan ≠ menguntungkan.** Waktu sesi lebih panjang bisa berarti betah atau bingung. Selalu tutup
  dengan metrik bisnis (konversi, nilai transaksi), bukan cuma angka detik.
- **CI yang hampir menyentuh nol = klaim harus hati-hati.** Kalau batas bawah cuma sedikit di atas nol dan
  sebaran salah satu kelompok sangat lebar, jangan sarankan mengubah strategi menyeluruh; sarankan
  segmentasi dan sampel lebih besar.
- **Tanda negatif mean difference** muncul karena SPSS menghitung Kelompok 1 − Kelompok 2. Jelaskan arahnya
  di kalimat, jangan biarkan pembaca menebak.

## Tiga kelompok atau lebih: One-Way ANOVA + Tukey

| Desain | Uji | Catatan |
|---|---|---|
| 3+ kelompok, satu faktor, varians homogen | One-Way ANOVA → Tukey HSD | Baca Levene dulu |
| 3+ kelompok, varians tidak homogen | Welch ANOVA → Games-Howell | Tukey tidak valid di sini |
| 3+ kelompok, tapi semua pasangan diuji dengan t-test | Salah | 1 − 0,95³ ≈ 14,3% peluang Tipe I |

Urutan baca output: Descriptives → Levene (`Based on Mean`) → ANOVA global → baru Multiple Comparisons.
Kalau ANOVA global tidak signifikan, tabel post-hoc **tidak** ditafsirkan; tidak ada bukti perbedaan,
variasi pasangan itu hanya noise.

`scipy.f_oneway` memberi F dan p, tapi **tidak** memberi tabel SS. Hitung dekomposisinya sendiri:

```python
import numpy as np
from scipy import stats

g = [cashback, free_shipping, point_reward]          # tiap kelompok = list nilai
a = np.concatenate(g); k, N = len(g), a.size
ssb = sum(len(x) * (np.mean(x) - a.mean()) ** 2 for x in g)
ssw = sum(((np.asarray(x) - np.mean(x)) ** 2).sum() for x in g)
msb, msw = ssb / (k - 1), ssw / (N - k)
F = msb / msw
p = stats.f.sf(F, k - 1, N - k)
eta2 = ssb / (ssb + ssw)                             # 0,01 kecil / 0,06 sedang / 0,14 besar
```

Tukey tanpa statsmodels (studentized range ada di scipy). Untuk n seimbang:

```python
se   = np.sqrt(msw / n)                              # n per kelompok, bukan N
q    = abs(diff) / se
padj = stats.studentized_range.sf(q, k, N - k)
hsd  = stats.studentized_range.ppf(.95, k, N - k) * se
ci   = (diff - hsd, diff + hsd)                      # batas CI = ±HSD, sama dengan SPSS
```

Contoh angka yang konsisten: MSW 264,815; n 10 → se 5,146; q kritis (3, 27) 3,506 → HSD 18,04;
selisih 20 tetap signifikan (q 3,89; p ≈ 0,03), selisih 55 dan 35 jelas signifikan. Games-Howell butuh
paket lain (`pingouin.pairwise_gameshowell`); jangan pura-pura Tukey berlaku saat Levene menolak.

Kalimat pelaporan: “Perbedaan antar-program signifikan, F(2, 27) = 29,27, p < 0,001, η² = 0,68 (efek
besar); Tukey menunjukkan Cashback lebih tinggi 55 poin dari Free Shipping (95% CI 36,96–73,04).”

Jebakan khusus ANOVA:

- **H₀ ditulis dengan μ, bukan angka mean.** `H₀: μ₁ = μ₂ = μ₃`, bukan `545 = 490 = 510`; dan H₁ =
  “paling sedikit satu pasang berbeda”, bukan nilai F. Ini kesalahan yang paling sering ada di file
  mahasiswa dan langsung terbaca dosen.
- **Jangan percaya label pasangan di file sumber.** Hitung ulang tanda dan besarnya dari mean tiap
  kelompok: 545 − 490 = 55, bukan 35; label yang tertukar membalik kesimpulan praktisnya.
- **Varians tidak homogen mengubah uji lanjut, bukan kesimpulan ANOVA.** Levene ≤ 0,05 → Games-Howell;
  effect size tetap dilaporkan dari η².
- **η² dari tabel, bukan dari F.** `SSB / SST`; kalau hanya ada F, turunkan lewat `SSB = F·MSW·(k−1)`.
