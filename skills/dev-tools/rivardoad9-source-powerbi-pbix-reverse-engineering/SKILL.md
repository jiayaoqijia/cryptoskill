---
name: powerbi-pbix-reverse-engineering
description: "Bongkar & rekreasi dashboard Power BI (.pbix) tanpa Desktop."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [PowerBI, PBIX, dashboard, reverse-engineering, youtube]
---

# Reverse-engineer dashboard Power BI (.pbix) tanpa Power BI Desktop

## Kapan pakai
- User minta dibuatkan / ditiru dashboard Power BI, tapi tidak ada Windows/Desktop (server headless).
- Ada file `.pbix` (punya user atau contoh) yang perlu dibedah: layout, theme, measure DAX, Power Query, dataset.
- User kirim link video tutorial dashboard → butuh isi tutorialnya padahal YouTube ngeblokir IP server.

## Prinsip
`.pbix` = **ZIP**. Di dalamnya: `Report/Layout` (JSON definisi semua visual, UTF-16LE), `DataModel`
(skema + data, terkompresi XPress9), `Report/StaticResources/RegisteredResources/*` (gambar/map JSON),
`DiagramLayout`. Semua bisa dibaca/diekstrak tanpa Desktop.

## Langkah

1. **Siapkan venv** (PEP 668 / tanpa pip):
   ```bash
   uv venv --python 3.14 .venv && uv pip install --python .venv/bin/python pbixray pandas
   ```
   `pbixray` menarik `xpress8`/`xpress9` → itu kunci bisa baca `DataModel`.
   Kalau `import pandas` gagal dengan `numpy._core._multiarray_umath` hilang padahal file `.so` yang
   terpasang berakhiran `cpython-3XX` lain, interpreter venv beda versi dengan wheel yang ada: buat ulang
   venv dengan `--python <versi yang sama>` (jangan pakai default `uv venv`), lalu install lagi.

2. **Bedah layout** (koordinat, ukuran, tipe visual, field, formatting):
   ```bash
   python3 pbix_deep.py file.pbix outdir   # helper: /home/ubuntu/pbix/pbix_deep.py
   ```
   Output: `layout_summary.txt` (manusiawi) + `layout_deep.json`. Layout di-decode `utf-16-le`
   (fallback `utf-8-sig`). Config tiap visual ada di `visualContainers[i].config` → `singleVisual`.

3. **Bedah model + data** (paling berguna):
   ```bash
   ./.venv/bin/python pbix_model.py file.pbix    # schema, measures, M, relasi, dump CSV
   ```
   API pbixray yang penting: `m.tables`, `m.schema`, `m.relationships`, `m.dax_measures`
   (punya kolom **Expression** = formula DAX lengkap), `m.dax_tables` (tabel calculated),
   `m.power_query` (kode M asli, termasuk path sumber → ketahuan nama file dataset),
   `m.get_table("x")` → DataFrame.
   Catatan: `m.columns`/`m.measures` TIDAK ada; pakai `m.schema` + `m.dax_measures`. Format string &
   DataCategory tidak diekspos — infer dari screenshot/`tmschema_columns`.

4. **Angka target = alat verifikasi.** Hitung KPI dari `factSalesData` (revenue/cost/profit/views/
   avg conversion per tahun, share channel) lalu cocokkan dengan angka di screenshot contoh.
   Kalau cocok → data + desain sudah terkonfirmasi, bukan tebakan.

5. **Rekonstruksi dataset**: join fact + dim by ID, susun ulang kolom persis urutan sumber asli →
   `sales_data.csv` flat. Simpan juga tiap tabel model sebagai CSV siap import (lebih cepat untuk user:
   tidak perlu merge di Power Query).

6. **Rakit paket**: `1_data_raw/`, `2_data_siap_import/`, `3_asset_gambar/` (ekstrak RegisteredResources,
   termasuk map JSON untuk shape map), `4_dokumen/` (DAX_measures.txt, PowerQuery_M.txt, blueprint_layout.txt,
   schema, relasi, theme JSON, `Panduan_Rebuild.md`, .pbix referensi). Zip → kirim via MEDIA.

## Tidak ada .pbix sumber: rakit dashboard dari database user

Kalau tugasnya "bikin dashboard Power BI" dan tidak ada file contoh, jangan berhenti di "tidak bisa, Desktop cuma
Windows". Desktop memang Windows-only, tapi yang bisa dikirim dari server headless tetap besar nilainya:

1. **Dashboard referensi (PNG) dari query asli.** Gambar pakai matplotlib langsung dari database, jangan angka
   manual. Ukuran 1600x900, warna kartu putih, background `#F6F4F0`, aksen `#B4502D`. Isinya: 3-4 card KPI, bar
   per kategori, scatter dua sumbu, dua line, tabel ringkasan. Render lalu periksa lewat vision — label sumbu yang
   bertumpuk, tabel yang terpotong footer, dan legenda yang menimpa garis adalah tiga cacat yang selalu muncul dan
   harus diulang sampai bersih.
2. **Sebut gambar itu referensi layout, bukan bukti screenshot.** Kalau user menyerahkannya sebagai screenshot
   Power BI, itu pemalsuan hasil praktikum. Tulis eksplisit di chat dan di nama file (`dashboard_mock.png`, bukan
   `screenshot_dashboard.png`).
3. **Panduan rebuild berurutan** yang bisa diikuti sambil buka Desktop: sambung MySQL (tab **Database**, bukan
   Windows; mode Import), pilih view agregat saja, relasi many-to-one, tabel Calendar DAX + Mark as date table +
   Sort by column, daftar measure siap tempel, ukuran kanvas, posisi tiap visual dalam piksel, interaksi slicer,
   troubleshooting per pesan error, ceklist angka yang harus muncul.
4. **Theme JSON siap impor** (View > Themes > Browse for themes) supaya user tidak menyetel warna satu-satu:
   `name`, `dataColors`, `background`, `foreground`, `tableAccent`, `textClasses`, dan `visualStyles` untuk
   background/border/title. Ini file kecil, tapi paling menghemat waktu user.
5. **Angka DB = checkpoint.** Tulis di panduan angka yang wajib muncul di card/hasil measure. Kalau user dapat angka
   lain, masalahnya di relasi atau filter, bukan di data.

Jangan merakit `.pbix` atau PBIP sendiri tanpa Desktop untuk memvalidasinya. Formatnya bisa ditulis tangan, tapi satu
field salah dan file gagal dibuka — kegagalan yang tidak bisa kita deteksi dari server. Panduan + theme + angka
patokan lebih jujur dan tetap terpakai.

Pitfall khusus kolom persen dari view: kalau view sudah menyimpan `late_pct` = 30.8 (bukan 0.308), measure-nya
`AVERAGE(...) / 100` dengan format `0,0%`. Tanpa pembagian itu card menampilkan 3080%.

## Verifikasi klaim "repo ini punya file DAX" / "pbix-nya konek MySQL"

User yang minta "mana file DAX-nya" dari repo tutorial sering mengira ada file terpisah. Jangan jawab dari
README atau judul repo — buka model `.pbix`-nya dan sebut angka konkretnya.

```bash
curl -sL "https://api.github.com/repos/<owner>/<repo>/git/trees/HEAD?recursive=1"   # buktikan tidak ada .dax
```

Lalu unduh `.pbix` dan periksa:

- `len(m.dax_measures) == 0` → laporan itu **nol measure**. Semua angka berasal dari tabel impor yang sudah
  teragregasi, biasanya nama tabelnya persis nama query (`gender`, `race`, `location`, `turnover_rate`).
  Skema seperti ini tidak bisa di-slice dan tidak bisa di-refresh.
- `m.power_query` → kolom `Expression` memuat kode M. `Csv.Document(File.Contents("C:\\...\\gender.csv"))`
  membuktikan sumbernya snapshot CSV, bukan koneksi database, walaupun judul repo menyebut MySQL.
  Baca jumlah baris/kolom tiap tabel juga: 2 kolom hasil agregat = hasil ekspor query, bukan tabel fakta.

Laporkan ke user dalam bentuk bukti: "8 file, tidak ada .dax; dua .pbix berisi 0 measure dan 11/12 tabel
CSV" — bukan "kayaknya nggak ada". Setelah itu kirim measure buatan sendiri untuk tabel bersih user
(bukan tiruan tutorial), lengkap dengan angka hasil yang harus muncul sebagai pembanding.

## Kalau .pbix yang dikumpulkan user ternyata file tutorial unduhan

Cek tiga hal ini dari model, bukan dari screenshot, sebelum menyimpulkan apa pun:

1. `m.power_query` memuat path `C:\Users\<nama lain>\...` → sumbernya laptop pembuat tutorial, bukan user.
2. Tabel sumber bukan tabel user (`gender`, `race`, `location`) → tidak ada tabel fakta/`hr_clean` milik user.
3. Tiap measure yang user tempel menunjuk tabel yang tidak ada di `m.tables` → measure itu error saat dirender.

Sertakan pembanding angka: hitung ulang KPI dari dataset user di database, lalu bandingkan dengan visual.
Kalau totalnya beda (mis. dashboard 17,5K vs database 19.303 aktif), datanya memang bukan milik user —
sebut angkanya, jangan cuma bilang "beda". Sampaikan sebagai temuan, bukan vonis, lalu beri jalur perbaikan
terpendek (connect ke tabel user, hapus tabel tutorial, ulang screenshot).

## Hemat waktu user: bulk import measure (jangan suruh paste 44x)

Setelah measure diekstrak dari `.pbix`, JANGAN suruh user paste satu-satu di Desktop. Generate dua jalur:

1. **TMDL view (bawaan Desktop baru, tanpa install)** — bentuk blok siap tempel:
   ```
   table 'All Measures'
   	measure 'Revenue' = ```
   			SUM(factSalesData[Sales Amount (USD)])
   			```
   	measure 'Revenue Sparkline' = ```
   			...
   			```
   		dataCategory: ImageUrl
   ```
   (indent pakai TAB; body ekspresi di dalam triple-backtick). Simpan `formatString` DI LUAR script dan
   suruh set manual — format string berisi tanda kutip (`$#,0,"K"`) rawan bikin Apply error.
2. **Tabular Editor 2 (free, .exe portable)** — C# script: `t.AddMeasure(n, expr)`,
   `m.FormatString=...`, `m.DataCategory="ImageUrl"`, plus `if (t.Measures.Contains(n))` biar idempoten.

Fallback terakhir: paste manual (estimasi ~40 menit untuk 44 measure).

## Jebakan yang sering kena
- **YouTube** blokir IP datacenter: `youtube-transcript-api`, `yt-dlp`, invidious/piped mirror semua gagal.
  Yang bisa: `curl -sL -H "X-Return-Format: text" https://r.jina.ai/<url-video>` → dapat judul + channel +
  awal deskripsi (cukup buat identifikasi video). Transkrip penuh tetap mentok → bilang jujur ke user.
- **Cari implementasi lain dari tutorial yang sama** di GitHub = jalan pintas paling ampuh
  (`api.github.com/search/repositories?q=...`, `api.github.com/repos/<r>/git/trees/HEAD?recursive=1`).
  Banyak mahasiswa upload `.pbix` + dataset + README berisi daftar measure.
- Visual `shapeMap` butuh map JSON di-add di pane Format; tanpa itu peta kosong.
- Measure SVG sparkline/lollipop **wajib Data category = Image URL**, dan kode warna pakai `%23` (bukan `#`).
- Kolom gambar (URL produk / base64 flag) juga butuh data category *Image URL*.
- Sparkline SVG biasanya pakai `Calendar[Monthnum]` sebagai sumbu X; kolom `Month` harus *Sort by* `Monthnum`.
- File contoh bisa dibuat Desktop versi lebih baru → Desktop user bisa nolak buka. Tetap berguna untuk
  inspect pane Format.

## Etika
File `.pbix` dari GitHub milik orang lain = **referensi belajar**, jangan sarankan user submit apa adanya
(plagiarisme). Sarankan rebuild sendiri; paket data + DAX yang kita rakit itu yang dipakai.
