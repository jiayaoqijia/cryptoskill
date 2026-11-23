# Scout level-ticker di dalam tema — angka lengkap & cara reproduce

Sumber: `~/.hermes/scripts/narrative_laggard_scout.py` (dibuat 14 Okt 2026).
Data: klines harian Binance, cache `~/.hermes/data/narr_hist_cache.json` (12 jam), bucket tema
= `THEMES` di `deep_dive_daily.py` (satu sumber, jangan bikin daftar kedua).
Uji: 240 hari, 13.366 observasi anggota, likuiditas filter ≥ $1,5jt/hari (rata-rata 30d).

## Perintah

| command | isi |
|---|---|
| `study` | grup lintas-anggota: laggard vs leader, dibanding tema dingin (kontrol) |
| `grid` | 12 varian sinyal level-ticker, tema panas vs kontrol + delta alpha |
| `scan` | kandidat live (bar harian yang UDAH TUTUP), dipakai deep dive blok [1d] |

## Hasil `grid` (dibeli hari T, hasil T+1/T+3/T+7)

```
sinyal                         n      f3      f7      a3      a7| kontrol n      f3      a3  delta a3
L0 laggard vol<1x            406   -0.8%   -2.4%   -0.2%   -1.8%       8789   +0.3%   +0.2%     -0.4%
L1 laggard+tertinggal        307   -1.1%   -3.2%   -0.4%   -2.3%       5053   +0.2%   +0.2%     -0.5%
L2 laggard+breadth naik      208   -1.1%   -2.6%   -0.1%   -2.1%       2133   -0.2%   +0.4%     -0.5%
Q1 vol mulai 1,0-1,5x        321   +0.9%   +0.6%   +0.8%   +1.3%       1497   +0.0%   -0.3%     +1.2%
Q2 vol masuk 1,5-3x          299   +2.1%   +0.6%   +2.1%   +1.1%        629   -1.0%   -1.2%     +3.3%
Q3 vol masuk >3x              97   -1.9%   -4.1%   -1.7%   -4.1%        145   -0.8%   -1.8%     +0.2%
V1 vol>=1,5x harga diam      396   +1.1%   -0.6%   +1.2%   -0.2%        774   -1.0%   -1.3%     +2.5%
H1 anggota blowoff r1>=3%    356   -0.3%   -0.8%   +0.2%   +0.2%       1788   +0.5%   +0.3%     -0.1%
H2 anggota r7>=8% (ngejar)   806   +0.3%   -0.7%   +0.6%   +0.3%       1694   -0.7%   -1.0%     +1.6%
K1 coil harga |r7|<=3%       209   +1.3%   -0.1%   +1.1%   -0.3%       2641   +0.4%   +0.1%     +1.0%
K2 coil+vol mulai>=1,2x       78   +2.6%   +2.1%   +2.3%   +1.6%        252   -0.4%   -0.7%     +2.9%
```

"tema panas" = vol3/30 tema 1,2–3,0x · r1 ≤ +4,5% · breadth ≥ 50%.
"kontrol" = vol3/30 < 1,0x atau breadth < 35%.

## Robustness Q2

- hit f3 > 0: 52% (panas) vs 41% (kontrol) · P(f3 ≥ +3%): 37% vs 26%
- paruh lama (n=149): f3 +0,6% · a3 +1,0% · median f3 −0,5%
- paruh baru (n=150): f3 +3,5% · a3 +3,2% · median f3 +1,0%
- 65% kasus besok masih ≤ +2% → masih bisa masuk, bukan sinyal chasing
- kurva vr: 1,0–1,3x a3 +0,6% · 1,3–1,5x +1,2% · 1,5–2,0x **+2,7%** · 2,0–2,5x +2,4% ·
  2,5–3,0x −0,8% · 3,0–4,0x −0,7% · >4x −2,6%

## Kenapa "laggard tanpa volume" kalah

Di tema dingin grup itu positif (+0,2% a3), di tema panas negatif (−0,4% a3). Jadi bukan cerita
mean-reversion yang bisa dipanen: justru narasinya yang membuat ticker itu ditinggal. Di dalam
tema yang sedang dipilih market, perbedaan volume = perbedaan keputusan market — yang nggak
kemasukan volume itu yang di-skip, bukan yang mengantre.

Cara baca yang dipakai user: "kalau uang masuk ke narasi, yang belum gerak bukan antrian ke belakang,
tapi tanda market nolak." Yang benar: cari yang volumenya udah masuk TAPI harganya belum naik.

## Catatan implementasi

- `last_closed_index(ts)` di `narrative_rotation_early.py`: bar harian wajib udah tutup
  (`min_frac=1,0`), bar 4 jam boleh dipakai kalau ≥50% (`min_frac=0,5`).
- `scan` deep dive memfilter baris berawalan `   *` dari scout (kandidat) supaya tabel tema
  gak dobel dengan blok [1c].
