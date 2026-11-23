# Laporan PDF porto (resep yang jalan)

Trigger: user minta "laporan lengkap" / "laporan PDF" / rapor yang bisa dibaca di HP atau dikirim orang.
Terverifikasi 16 Okt 2026 (`~/.hermes/scripts/diag/make_laporan_aave_2026-10-16.py`, 17 halaman, 4 chart).

## Tanpa library PDF

Server ini nggak punya pandoc/weasyprint/wkhtmltopdf/libreoffice/poppler. Yang ada: Chromium di
`~/.hermes/tools/chromium-1208/chrome-linux64/chrome`. Jadi: HTML → PDF.

```bash
"$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=/path/out.pdf file:///tmp/report.html
```

## Struktur yang dipakai

1. Dokumen terang (`#16202e` di atas putih) walau chart-nya tema gelap — enak dibaca/diprint; chart gelap jadi
   kontras yang bagus. Jangan bikin PDF gelap penuh.
2. Section bernomor: ringkasan eksekutif (5 poin) → kondisi porto + masalah struktural → metodologi/rubrik →
   tesis utama → kontra-argumen → kenapa bukan yang lain (satu sub-bagian per kandidat) → base rate/konteks →
   rencana eksekusi → yang belum terverifikasi + apa yang bakal ngubah pikiran → lampiran (tabel mentah,
   skor per gate, sumber, versi "data bersih" tanpa label internal).
3. Setiap klaim angka dikasih sumber + tanggal di tubuh teks; lampiran C = tabel sumber (sumber, dipakai buat apa, kapan).
4. Tabel dibaca dari cache JSON data mentah (`kandidat_rows.json`, `ma_stats.json`, `betas.json`) — jangan
   hardcode angka di generator, biar bisa rerun.

## CSS yang wajib

```css
@page { size: A4; margin: 13mm 11mm; }
@page land { size: A4 landscape; margin: 10mm 10mm; }   /* halaman lebar */
.landpage { page: land; }
table.screen { font-size: 7.4pt; }                       /* tabel >10 kolom */
.pb { page-break-before: always; }
.nb { page-break-inside: avoid; }
```

- **Chart harus di halaman landscape sendiri** (`<div class="landpage">`). Chart PNG-nya 1400px; kalau dipasang
  di kolom portrait A4 (~703px) teks 12px di dalam chart jadi ~6px → nggak kebaca.
- **Tabel >10 kolom juga landscape** + font 7,4pt, kalau nggak kolom terakhir kepotong.

## Verifikasi sebelum kirim

1. Jumlah halaman + jumlah gambar:
   ```python
   d = open(pdf,'rb').read(); d.count(b'/Type /Page') - d.count(b'/Type /Pages'); d.count(b'/Subtype /Image')
   ```
2. Baca ulang teksnya pakai `read_file(pdf)` — `read_file` mengekstrak text layer PDF, jadi kelihatan kalau ada
   bagian yang kosong/rusak (urutan baris bisa acak; yang penting isinya ada).
3. Prober lebar tabel: potong blok HTML tabelnya + CSS-nya ke file probe, screenshot Chromium dengan lebar
   halaman tujuan (portrait ~703px, landscape ~1047px), lalu `vision_analyze` — tanya "ada kolom terpotong?"
   Ini ketangkep satu kali: tabel 13 kolom aman di 1047px tapi bakal kepotong di 703px.
4. Chart-nya sendiri diverifikasi `vision_analyze` dulu (lihat skill `data-chart-rendering`).

## Pitfall yang sudah kena

- Judul lampiran nulis "18 koin" padahal tabelnya 34 baris → **hitung jumlah baris dari data**, jangan tulis manual.
- Semua chart dirender 1400px lebar lalu ditaruh portrait → teks chart nggak kebaca. Selalu halaman landscape.
- Bar chart SVG: lebar bar dihitung `w * (R-L)`, bukan `w * unit * 100`. Salahkan prober, bukan pembaca.
