# People analytics scorecard: CSV → MySQL → dashboard

Pola tugas "People Analytics": beberapa CSV dari sistem berbeda (karyawan, absensi, penjualan, survei
pelanggan) dimuat ke MySQL, diagregasi lewat view, lalu jadi dashboard + ringkasan insight 1-2 halaman.
Rubrik biasanya: database & view, model & DAX, dashboard, insight, etika.

## Muat data
- Pakai skema dan view bawaan modul apa adanya. Jangan mengarang nama kolom dari dugaan: baca `01_schema.sql`
  dan header CSV dulu, karena view turunan (mis. `s.survey_month CHAR(7)`, `salaries.base_salary` tanpa
  `allowance`) berbeda dari asumsi umum.
- `SET GLOBAL local_infile = 1;` lalu jalankan client dengan `mysql --local-infile=1`. Tanpa flag client,
  `LOAD DATA LOCAL` gagal walau server sudah mengizinkan.
- Tanggal resign kosong di CSV: `LOAD DATA ... (..., @resign) SET resign_date = NULLIF(@resign, '')`.
  Tanpa ini: `Incorrect date value: ''` dan seluruh load berhenti di tengah.
- Akhiran baris: `'\n'` untuk file yang dibuat di Linux/macOS, `'\r\n'` kalau CSV pernah disimpan ulang lewat
  Excel — gejalanya kolom bergeser satu posisi, bukan error.
- Checkpoint jumlah baris setelah load (mis. 2.000 karyawan, 928.839 log, 1.500.000 transaksi, 60.000 survei).
  Selisih = header salah terbaca atau baris terpotong, bukan "data sedikit".

## Bukti teknis yang layak ditulis di laporan
- **Integritas**: `LEFT JOIN employees ... WHERE e.emp_id IS NULL` → sebut angkanya (0 = bersih). Jelaskan
  kenapa dicek: join yang membuang baris yatim membuat angka per cabang lebih kecil dari kenyataan tanpa error.
- **Index**: ukur durasi query yang sama sebelum dan sesudah `CREATE INDEX`, lalu `EXPLAIN` (type, key, rows).
  Angka konkret (0,16 s → 0,01 s; 523 baris dibaca vs 928.839) lebih meyakinkan daripada "jadi lebih cepat".
- **Mentah vs view**: `information_schema.tables` untuk `table_rows` + ukuran MB, dan `COUNT(*)` tiap view.
  Ini dasar argumen impor view (10/240/2.000 baris) versus tabel mentah (2,4 juta baris).

## Jebakan analisis yang menurunkan nilai
- **Porsi ≠ rate.** "64% dari yang resign berasal dari kelompok masa kerja ≥3 tahun" adalah komposisi. Kalau
  ditulis "risiko resign tertinggi", klaimnya salah: untuk rate butuh denominator karyawan per kelompok, yang
  tidak tersedia dari tabel resign saja. Tulis sebagai porsi + sebutkan datanya kurang untuk rate.
- **Ecological fallacy.** Korelasi level departemen bisa ekstrem (r = -0,97 dari 5 titik) sementara level individu
  praktis nol (r = -0,03 dari 1.900+ karyawan). Laporkan keduanya dan jelaskan kenapa kesimpulan diambil dari
  level individu, bukan dari agregat yang kebetulan rapi.
- **Indikator flat bukan temuan.** Kalau satu metrik hampir identik di semua unit (mis. absen 2,9-3,0%), jangan
  dipakai sebagai penanda masalah; sebut sebagai kontrol yang berhasil menyempitkan penyebab.
- **Kualitas data = bahan diskusi, bukan catatan kaki.** Transaksi setelah karyawan resign atau sebelum tanggal
  masuk (masing-masing ~5,1%) membuat angka penjualan tidak layak untuk penilaian individual. Sebut jumlah baris
  dan persennya, lalu batasi klaim.
- **Persen sudah dalam persen.** View yang menyimpan `late_pct = 30.8` harus dibagi 100 di measure DAX; format
  `0,0%`. Tanpa itu card menampilkan 3080%.

## Bentuk dokumen yang lolos batas halaman
- Insight 1-2 halaman: temuan utama, tabel bukti, "yang justru tidak terbukti", rekomendasi, batas & etika,
  catatan teknis. Setelah build, konversi ke PDF, hitung halaman, lalu potong kalimat — jangan mengecilkan font
  atau margin supaya kelihatan muat.
- Jawaban tiap pertanyaan modul (tahap eksplorasi, perbandingan, tugas mandiri) masuk **lampiran terpisah**.
  Ini yang menjaga dokumen utama tetap 2 halaman tanpa kehilangan bukti pengerjaan.
- Dashboard: PNG referensi dari query asli + panduan rebuild + theme JSON. Selalu sebut sebagai referensi layout,
  bukan screenshot Power BI (detail di skill `powerbi-pbix-reverse-engineering`).

## Upload ke Drive lewat REST (tanpa SDK)
- Query parameter `q` wajib di-`urllib.parse.quote`. Spasi mentah di URL memicu
  `InvalidURL: URL can't contain control characters`.
- `access_token` berumur sekitar satu jam. Batch upload yang lama bisa mati di tengah dengan 401: refresh dulu
  via `refresh_token` + `client_secret`, simpan token baru, ulangi upload — jangan bongkar ulang semuanya.
- Share di folder induk dengan role `writer`; anak folder mewarisi izin. Verifikasi dengan
  `permissions?fields=emailAddress,role` dan sebut hasilnya, jangan cuma percaya respons API.
- Upload multipart manual: metadata JSON + isi file dengan boundary, endpoint
  `upload/drive/v3/files?uploadType=multipart&fields=id,name,size`.
