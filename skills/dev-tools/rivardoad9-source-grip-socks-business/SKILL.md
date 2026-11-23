---
name: grip-socks-business
description: Use for the grip socks Pilates venture and its workbook.
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [grip-socks, pilates, sourcing, workbook]
    related_skills: [xlsx, market-field-research]
---

# Grip socks Pilates venture

## When to Use

Pakai saat Do bertanya soal grip socks Pilates: penawaran pabrik (Sofia, Kaia), harga studio, update workbook riset, atau isi PDF panduan industri.

Do membangun brand grip socks kecil untuk studio Pilates Jakarta. Fokus: batch pertama kecil, bukan produksi besar.

## Berkas

- Folder kerja: `~/grip-socks-research/`
- Workbook: `Riset_Grip_Socks_Pilates.xlsx`, dibangun oleh `build_report.py` (8 sheet: Ringkasan, Riset Studio, Benchmark Harga, Supply, Pasar, Rencana Aksi, Template & Skrip, Vendor Pabrik)
- Uploader: `upload_drive.py`, memakai `FILE_ID` tetap `13RCJroYfyqJPbFw6gK5iqaybBD2g5Ju56QYgMFx2Kno`
- PDF panduan: `build_pdf.py` → `Panduan_Industri_Grip_Socks_Pilates.pdf` (reportlab, 15 hlm)

Perintah update workbook: `cd ~/grip-socks-research && python3 build_report.py && ~/.hermes/google_venv/bin/python upload_drive.py`

Jangan pernah membuat Sheet baru. Link harus tetap: https://docs.google.com/spreadsheets/d/13RCJroYfyqJPbFw6gK5iqaybBD2g5Ju56QYgMFx2Kno/edit

## Data lapangan (per 20 Okt 2026)

Harga jual studio: WE 70k, SCULPTOREE 99k, pilasentials 100k, Sou 165k, Alora 185k, Rolla 199k, YONEX 200k, ALO 300k. Median 192k. 3/3 studio menyatakan wajib dan menjual sendiri.

PT Sofia Socks: MOQ 60 pasang per desain/warna/ukuran (dijawab 22 Okt; di bawah 60 tidak bisa). Harga 35k/pcs, sudah termasuk antislip, bordir, DAN screen baru (revisi 21 Okt, membatalkan biaya screen 350k). Di 120 psg 25-28k/pcs. Sampel 250k, hangus kalau batal, masuk DP kalau lanjut. Sample 30 hari kerja termasuk screen baru, tapi tergantung antrean mesin. DP 50%, pelunasan sebelum kirim. Ongkir belum dihitung.

PT Kaia: menolak 48 pasang, minimum 120 per desain/warna/ukuran. Base 33-35k/pcs PLUS antislip/bordir 3-6k/pcs, screen antislip 500k per desain/ukuran, screen bordir 100k. Sampel 200k per desain (dikreditkan kalau lanjut, hangus kalau batal), jadi 7-10 hari kerja atau 10-14 hari kalau pakai antislip/bordir. Efektif 36-41k/pcs, artinya 4,9-5,5jt untuk 120 psg. Bukan opsi batch pertama.

## Aturan negosiasi

- Jangan bilang "mau mulai produksi" ke pabrik. Pakai "lagi bandingin beberapa pabrik buat batch pertama".
- Jangan tanya payment term atau minta katalog di pesan pertama.
- Jangan pitch ke studio sebelum ada sampel yang lolos tes cuci 10x.
- Jalur cepat: pakai pattern antislip existing + logo bordir di cuff, hindari screen baru (screen yang makan 30-40 hari).
- Batch pertama satu desain. Naik ke tier 120 psg hanya kalau sell-through terbukti, karena modalnya 5x.

## Alur pemenuhan pesanan

- Barang selalu masuk ke Do dulu. Jangan minta pabrik drop-ship langsung ke studio: surat jalan dan invoice pabrik ikut masuk dan membuka HPP 35k di depan studio yang beli 65k, dan QC per pasang (jahitan, antislip, ukuran, bordir) tidak bisa dilewati. Drop-ship hanya untuk repeat order SKU yang sudah terbukti.
- Kas: DP studio 50% dipakai untuk bayar DP pabrik. Sample 250k sudah jadi bagian DP itu, jadi uang yang keluar sebelum ada barang jadi cuma 250k.
- Angka kerja batch pertama: 60 psg x 35k = 2,1jt; jual 65-70k ke studio = 3,9-4,2jt, laba kotor 1,8-2,1jt.

## Sebelum transfer biaya sampel

Sampel 250k adalah satu-satunya uang yang keluar sebelum ada barang jadi, jadi konfirmasi dulu — yang masih
terbuka hanya ini, jangan tanyakan ulang yang sudah dijawab (MOQ 60 per desain/warna/ukuran sudah fix):

1. **Sampel 250k dapat berapa pasang, dan boleh beda ukuran?** Perlu lebih dari satu ukuran untuk menilai
   fitting 36-40.
2. **Harga 35k/pcs untuk qty 60 sudah termasuk ongkir ke Jakarta atau belum?**
3. **Lead time kalau pakai pattern antislip existing tanpa screen baru?** Antrean screen baru yang bikin
   30 hari kerja; pattern existing bisa memotong itu.
4. **Minta penawaran tertulis** karena ada kontradiksi: 20 Okt screen baru 350k terpisah, 21 Okt dinyatakan
   35k/pcs sudah termasuk screen. Jangan transfer berdasarkan chat lisan.

Sampel lulus hanya kalau: antislip tidak mengelupas setelah 10× cuci, jahitan tumit utuh, ukuran pas, bordir
cuff tidak kaku.

Konsekuensi waktu yang harus disebut sebelum dia bayar: 30 hari kerja ≈ 6 minggu → sampel akhir November,
batch pertama baru Januari kalau menunggu sampel dulu. Ini pilihan sadar Do, bukan detail teknis.

## Konteks pribadi

Do menunggu uang saku bulanan; anggaran realistis batch pertama sekitar Rp1,4 juta. MOQ Sofia 60 psg = Rp2.100.000, jadi batch pertama hanya jalan kalau ada pre-order dari studio. Jangan sarankan order 120 psg, dan jangan sarankan nombok modal sendiri di atas 1,4jt.
