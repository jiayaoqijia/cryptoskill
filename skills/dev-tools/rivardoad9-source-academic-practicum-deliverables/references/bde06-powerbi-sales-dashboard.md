# Studi kasus: Modul BDE06 — Power BI Sales & Marketing Dashboard (UBM)

Sesi 19 Sep 2026. User mahasiswa Prodi Digital Business, Universitas Bunda Mulia (UBM).
Kalau user balik dengan modul/tugas yang sama, semua angka & bahan di bawah sudah siap — tinggal verifikasi
ulang dari file yang dia kirim, jangan asal tempel.

## Modul (DOCX) — isi yang menentukan bentuk kerjaan
`PB4MAT_Modul_BDE06_PowerBI_Sales_Dashboard.docx`, mata kuliah **BDE06 Big Data & Business Intelligence**.
Video wajib: *Sales & Marketing Dashboard — Power BI* (Abdelytics, `youtu.be/9xouxe7qsd4`) + dataset dari
Google Drive modul.

Tahapan praktik: **A** Power Query (video 1:06–13:00) · **B** Model & relasi (13:00–22:00) ·
**C** DAX measures + halaman Overview · **D** halaman Product Details & visual lanjutan (SVG sparkline,
lollipop, navigasi halaman, filter pencarian, data bar).

Tugas mandiri:
- **Tahap 1 (bukti proses):** file `.pbix` + 4 screenshot — (a) Power Query dengan tabel dimensi, (b) Model
  view semua relasi, (c) halaman Overview, (d) halaman Product Details — digabung ke 1 Word/PDF.
  **WAJIB: setiap screenshot menampilkan nama + NIM mahasiswa di kanvas laporan (bukan watermark editor).**
- **Tahap 2 (data spesifik):** 3 produk profit tertinggi + angkanya; perbandingan revenue in-store vs online
  + selisihnya; bulan revenue tertinggi & terendah + nilainya.
- **Tahap 3:** analisis bisnis 150–250 kata — lead source & kampanye mana yang diprioritaskan anggarannya.
- **Tahap 4:** refleksi teknis 1 kendala (sparkline/lollipop) atau risiko relasi di Tahap A.

Rubrik: Model Data 25% · DAX & Visual Overview 25% · Halaman Product Details 20% ·
Jawaban Data Spesifik 15% · Interpretasi & Refleksi 15%.

## Dataset yang dikirim user (5 CSV, mendarat di `~/.hermes/cache/documents/`)
| File | Bentuk | Catatan |
|---|---|---|
| `sales_data.csv` | 2000 × 20 | **identik** dengan rekonstruksi dari `.pbix` sumber: total Revenue 1.640.365. Tanggal format `dd/mm/yyyy` (text) |
| `Customer.csv` | 1232 × 2 | `Customer Name`, `Customer Plan` (Basic 801 / Premium 431) |
| `Country Flag.csv` | 8 × 2 | `Country`, `flag` (base64 PNG → data category Image URL) |
| `product_stock_table.csv` | 15 × 3 | `Product`, `Stock Quantity`, `Img` (URL gambar) |
| `Sales_Target.csv` | 32 × 3 | `Month`, `Year`, `Target` = 50.000/bulan |

Kolom `sales_data.csv`: Sales ID, Customer Name, Product, Sales Date, Sales Amount (USD), Cost Price (USD),
Sales Channel, Country, Region, Sales Rep, Marketing Campaign, Lead Source, Conversion Rate (%), Sessions,
Views, Follow-ups, Closed Deal?, Customer Feedback, Customer Plan, Customer Rating.

**Cacat data yang harus dilaporkan ke user (temuan nyata):**
1. `Sales_Target.csv` kolom `Year` tahun pertamanya tertulis **2002** (harusnya 2022) → relasi target blank
   12 bulan. Fix: Power Query *Replace Values* 2002→2022 (atau pakai CSV versi betulan di paket).
2. Periode data **1 Jan 2022 – 30 Agu 2024**; Agustus 2024 terpotong (1–30) → jangan dipakai sebagai
   "bulan terendah" tanpa catatan; yang aman Agustus 2023.
3. `Sales Date` format `dd/mm/yyyy` sebagai text → kalau salah parse, relasi ke Calendar gagal tanpa error jelas.
4. Region & Country tidak konsisten antar baris (negara sama bisa muncul di beberapa region) → `dimCountry`
   hasil distinct berisi **32 baris** (bukan 8); merge dimensi harus pakai **dua** kolom (Country + Region).

## Model target (hasil bedah `.pbix` sumber, repo `Irfan-Shaik-45/Sales-Marketing-Dashboard`)
12 tabel: `factSalesData` (2000) + `dimCustomers` (1232) · `dimProduct` (15) · `dimChannel` (2) ·
`dimCountry` (32) · `dimLeadSource` (5: Referral, Email, Cold Calling, Social Media, Website) ·
`dimMarketingCampaign` (5: Fall Sales Campaign, Summer Deals 2024, Spring Promo 2024, Winter Promo 2023,
New Year Campaign) · `dimSalesRep` (8) + `Calendar` (1096, DAX `CALENDARAUTO`) · `Country Flag` ·
`product_stock_table` · `All Measures` (44 measure).
7 relasi many-to-one dari `factSalesData[* ID]` ke tiap dimensi + `Calendar[Date] ↔ factSalesData[Sales Date]`.

Calendar (verbatim):
```dax
Calendar = ADDCOLUMNS(CALENDARAUTO(),
  "Year", YEAR([Date]), "Month", FORMAT([Date], "mmm"), "Monthnum", MONTH([Date]),
  "Weekday", FORMAT([Date], "ddd"), "Weeknum", WEEKDAY([Date]),
  "Qtr", "Q-" & FORMAT([Date], "Q"),
  "WeekType", IF(WEEKDAY([Date])=1 || WEEKDAY([Date])=7, "Weekend", "Weekday"))
```
Halaman Overview = 12 visual di kanvas **1300×750** (posisi lengkap ada di blueprint hasil `pbix_deep.py`):
textbox judul `#3F53E0` (Sales Marketing bold 20pt + Dashboard italic 24pt), slicer `Calendar[Year]`,
**Card (new) 5 kolom** dengan reference label measure panah, line `Revenue` vs `Revenue PM` + constant line
50.000, bar `Revenue by Lead Source` (trik `Base Zero`/`Rev % of lead`/`Whole`), donut Sales Channel,
bar Marketing Campaign, bar Region (lollipop via `Blank1`/`Revenue`/`Blank2`), tabel Country +
`Revenue Sparkline`, **Shape map** (butuh map JSON), page navigator, textbox label.
Halaman Product Details = tabel besar: `Product ID, Img, Product, Avg Rating, Scoring, Stock Quantity,
No of Invoices, Sum of Sales Amount (USD), Views, Revenue, Revenue Sparkline, Cost, Cost Sparkline, Profit,
Profit Lollipop` + slicer tahun + navigator.

## Angka verifikasi (dihitung dari dataset user — dashboard yang benar harus memunculkan ini)
Total 3 tahun: Revenue **1.640.365** · Cost **1.286.164** · Profit **354.201**.

| Tahun | Revenue | Cost | Profit | Views | Avg Conversion |
|---|---|---|---|---|---|
| 2022 | 600.956 | 468.768 | 132.188 | 45.313 | 17,5 |
| 2023 | **629.510** | **493.176** | **136.334** | **45.861** | **17,2** |
| 2024 | 409.899 | 324.220 | 85.679 | 30.847 | 17,2 |

→ angka dashboard contoh (`$630K/$493K/$136K/46K/17`) = **tahun 2023**, bukan total.

- **Top 3 produk by profit (semua periode):** Gaming Console Z 28.549 · Soundbar 360 25.886 · Drone Vision 25.103.
  2023: Soundbar 360 11.176 / Gaming Console Z 11.111 / Tablet Z 10.168. 2022: Gaming Console Z 11.601 /
  Monitor HD 24 11.296 / Smartphone X 9.840. 2024: Drone Vision 8.503 / Soundbar 360 6.791 / Smart TV QLED 6.764.
- **Channel:** Online 1.101.350 (67,1% / profit 239.360) vs In-Store 539.015 (32,9% / 114.841) → selisih **562.335**.
- **Bulan:** tertinggi **Apr 2023 = 64.713**; terendah **Agu 2023 = 42.464** (Feb 2024 42.821; Agu 2024 43.232 parsial).
  Rata-rata bulanan 51.261; 17 dari 32 bulan di atas target 50.000.
- **Lead source (revenue / profit / margin):** Email 383.811 / 82.561 (21,5%) · Referral 337.926 / 69.369 (20,5%) ·
  Social Media 322.174 / 71.709 (22,3%) · Cold Calling 305.155 / 62.314 (20,4%) · Website 291.299 / 68.248 (23,4%).
- **Campaign (revenue / profit):** Spring Promo 2024 357.372 / 77.433 · New Year Campaign 329.040 / 69.974 ·
  Winter Promo 2023 322.474 / 73.175 (margin 22,7% tertinggi) · Fall Sales 316.026 / 64.834 · Summer Deals 2024 315.453 / 68.785.
- **Region:** Europe 448.266 > Asia 427.030 > North America 389.391 > South America 375.678.
- **Target:** total 1.640.365 vs target 1.600.000 = **102,5%**; terbaik Apr 2023 129,4%, terburuk Agu 2023 84,9%.
- Interpretasi (Tahap 3) yang datanya dukung: prioritaskan **Email + Social Media** (volume & margin), geser
  dari **Cold Calling + Fall Sales Campaign**; jadwalkan kampanye utama kuartal-1 s/d awal kuartal-2
  (Feb–Apr, konsisten >100% target).

## Yang diserahkan ke user (paket ramping, 6 file, ~61 KB)
`1_DAX_measures.txt` (44 measure + header cara pakai & format/DataCategory) ·
`2_Panduan_Build_BDE06.md` (langkah dimap ke Tahap A–D + koordinat visual + checklist submit) ·
`3_Angka_Dashboard_Verifikasi.md` (jawaban Tahap 2 + bahan Tahap 3/4) · `4_map_json_countries.json` ·
`5_theme_SalesMarketing.json` · `6_Sales_Target_FIXED.csv`.
Sengaja TIDAK dikirim: dataset (user sudah punya dari modul), tabel model siap-import, `.pbix` orang lain.

## Artefak di disk (server ini)
`/home/ubuntu/pbix/` — `pbix_inspect.py`, `pbix_deep.py`, `pbix_model.py`, `pbix_export.py`,
`build_package.py`, `build_ramping.py`, `hitung_tugas.py`, `angka_bde06.txt`, `target/` (hasil bedah .pbix +
`DAX_measures.txt`, `data/*.csv`), `BDE06_RAMPING/`, `BDE06_PowerBI_file_yang_dibutuhin.zip`, `.venv/`
(pbixray + pandas + yt-dlp).
