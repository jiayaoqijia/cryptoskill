---
name: data-chart-rendering
description: Render real data to chart PNGs; no plotting lib needed.
---

# Chart dari data nyata → PNG (tanpa library plotting)

Trigger: user minta **gambar/grafik/chart/diagram** dari angka (hasil backtest, distribusi Monte
Carlo, equity curve, perbandingan harga/bar), ATAU user bilang **"gw kurang kebayang"** saat kamu
menjelaskan sesuatu yang berangka — itu permintaan visual, bukan permintaan penjelasan lebih panjang.

## Aturan isi

Chart HARUS dari data nyata yang baru dihitung (dump JSON dari run yang barusan), bukan ilustrasi
karangan. Kalau angkanya belum ada, jalankan dulu programnya dengan flag dump, baru gambar.

## Alur

1. **Cek plotting lib dulu**, jangan asumsi tidak ada:
   ```bash
   for p in /usr/bin/python3 ~/.hermes/venvs/*/bin/python ~/venvs/*/bin/python; do
     [ -x "$p" ] && "$p" -c "import matplotlib,numpy;print('$p OK')" 2>/dev/null; done
   ```
   Kalau ada matplotlib, pakai itu; kalau tidak, lanjut cara di bawah (jangan buang waktu install).
2. **Siapkan data dump**: tambahkan flag `--dump=<path>` ke program penghasil angka (equity curve,
   band persentil, trade list, window fold) → simpan JSON. Jangan hitung ulang manual di generator.
3. **Tulis generator Python (stdlib saja)**: JSON → HTML berisi **inline SVG**. Pakai template
   `templates/svg_chart_shell.py` (tema gelap, `head()` yang menghitung tinggi dokumen, line + bar chart,
   pola label di luar area plot).
4. **Screenshot dengan Chromium bawaan Playwright** (tidak perlu install browser baru):
   ```bash
   CH=$(ls -d ~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome | head -1)
   "$CH" --headless --no-sandbox --disable-gpu --hide-scrollbars \
         --force-device-scale-factor=2 --window-size=<W>,<H> \
         --screenshot=/tmp/chart1.png file:///tmp/chart1.html
   ```
   `--force-device-scale-factor=2` = teks tajam di Telegram. Error `dbus`/`NameHasOwner` saat start normal.
   Kalau build chrome penuh sedang dipakai proses lain, headless shell yang sama-sama sudah ada di disk
   jalan tanpa daemon: `~/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell`
   dengan flag yang sama (`--no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=2
   --window-size=W,H --screenshot=out.png file://…`). Dua-duanya CLI, jadi cocok untuk render berulang
   dari skrip tanpa nyentuh session browser.
   **Tambahkan `--virtual-time-budget=9000` kalau HTML pakai webfont** (`@import` Google Fonts): tanpa itu
   screenshot diambil sebelum font selesai diunduh dan seluruh tipografi jatuh ke fallback — hasilnya
   kelihatan "hampir benar" padahal font-nya salah. Cek `document.fonts.status` kalau ragu.
5. **Verifikasi SETIAP gambar dengan `vision_analyze` sebelum dikirim** (teks terpotong, label bertumpuk,
   tick berdesakan, kurva keluar area, literal `\n`). Perbaiki → render ulang → cek lagi. Jangan kirim
   chart yang belum kamu lihat sendiri.
6. **Kirim + simpan**: satu baris `MEDIA:/abs/path.png` per gambar; copy ke
   `~/obsidian-vault/attachments/`; simpan generator ke `~/.hermes/scripts/diag/` supaya rerun murah.

## Pitfall yang sudah kena (semuanya bikin gambar rusak)

| Gejala | Sebab | Fix |
|---|---|---|
| Baris bawah hilang/terpotong | tinggi `--window-size` ≠ tinggi dokumen HTML | Hitung `total = padding_atas + judul + jumlah_baris_teks*21 + svg_h + padding_bawah` di generator, `print` nilainya, pakai sebagai tinggi window |
| Tercetak `\n` di teks | `"\\n"` di dalam string Python | Pakai `\n` asli; hitung baris dengan `sub.count("\n")` |
| Tick sumbu Y menumpuk jadi blok | data ekor melesat (kurva bootstrap compounding) → rentang sumbu meledak | Kunci `ymax` dari persentil (p95 × 1,25), **clip** awan dengan `<clipPath>`, step tick adaptif: `while (ymax-ymin)/step > 12: step *= 2` |
| Label nilai menimpa garis | label ditaruh di dalam plot | pindah ke kolom kanan **di luar** plot (`x = R + 12`), sejajar ketinggian garisnya |
| Label kanan terpotong | kanvas kekecilan | `W ≥ 1360`, area plot berakhir ~1150, label di `R + 16` |
| Baris diagram hilang | tinggi SVG di-hardcode | hitung `svg_h` dari jumlah baris × tinggi baris + header/axis |
| Warna tak dijelaskan | legenda tak lengkap | setiap warna harus ada di legenda, termasuk kondisi "nol/absen" (mis. jendela tanpa trade) |

## Gaya visual yang dipakai user (Zemiz)

- Tema gelap: bg `#0b1020`, teks `#e6edf7`, grid `#1e2740`.
- Warna konsisten: hijau `#2ee6a8` = nyata/positif · merah `#ff5c7a` = negatif/in-sample ·
  biru `#3b7dff` = simulasi/pita · kuning `#ffb020` = jendela test · ungu `#c9a4ff` = median.
- Judul bernomor ("1 · …") + subjudul 1–2 baris berisi **cara membaca**, bukan mengulang angka.
  Angka penting juga ditulis sebagai teks di gambar.
- Bahasa Indonesia santai-teknis. Chart pelengkap pesan, bukan pengganti: tetap tulis 2–4 baris
  "cara bacanya" per gambar di chat.

## Poster / artwork dari HTML (bukan chart)

Kalau yang diminta "art", poster, atau sertifikat (bukan grafik angka): kanvas tetap, bukan layout
responsif. Tetapkan `width/height` body persis (mis. 1080×1350 untuk 4:5, 1600×2000 untuk cetak),
posisikan semua elemen `absolute` dengan koordinat angka, dan taruh ornamen di inline `<svg>` beratribut
`viewBox` penuh. Render dua kali lipat (`--force-device-scale-factor=2`) lalu turunkan ke ukuran target:
PNG 3200×4000 bisa 7 MB, JPEG kualitas 92 di ukuran asli cuma ~270 KB dan itu yang dikirim ke Telegram
(PNG master tetap disimpan di scratch). Selalu `vision_analyze` hasil akhirnya sebelum dikirim, dan cek
satu hal spesifik per pass: apakah bentuknya terbaca sebagai objek yang dimaksud, apakah ada teks
bertumpuk, apakah ruang kosong bawah tidak menggantung.

## Contoh nyata (29 Sep 2026, engine FlowMetrix)

Tiga gambar dari dump WFO Monte Carlo: (1) timeline fold train/test, (2) equity out-of-sample +
awan 10.000 resample bootstrap + batas p5/p95, (3) dua panel bar: expectancy in-sample vs
out-of-sample (−60%) dan leave-one-pool-out (+150,6% → +22,7%). Generator:
`~/.hermes/scripts/diag/make_wfo_charts.py`; hasil: `~/obsidian-vault/attachments/wfo-*.png`.
