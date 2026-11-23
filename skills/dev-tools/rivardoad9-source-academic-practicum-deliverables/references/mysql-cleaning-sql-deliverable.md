# Tugas berbasis database: cleaning MySQL + deliverable SQL + laporan Word

Dipakai untuk tugas yang alurnya: CSV kotor → MySQL → query analisis → Power BI → laporan Word
(contoh: BDE06 HR Analytics, tutorial SQL & Power BI). Berlaku juga untuk kerja data lain yang
menuntut file `.sql` yang benar-benar jalan, bukan sekadar tempelan query di dokumen.

## 0. Baca modulnya dulu

Yang menentukan bentuk kerjaan: daftar luaran, ketentuan tambahan (measure DAX, koneksi MySQL,
flowchart), jumlah pertanyaan analisis + batas kata, dan nama file yang diminta. Pertanyaan analisis
sering minta **angka spesifik** — jadi query harus menghasilkan angka itu, bukan narasi umum.

Kalau user bilang "output SQL aja, sisanya gw kerjain", kirim **persis itu**. Bagian lain dikerjakan
hanya kalau diminta di pesan berikutnya.

## 1. Pasang database lokal dan jalankan script-nya

Script yang belum pernah dieksekusi bukan deliverable. Pasang MySQL/MariaDB lokal, lalu jalankan
file final dari database kosong:

```bash
sudo -n apt-get install -y --no-install-recommends mariadb-server mariadb-client
sudo -n systemctl start mariadb
sudo -n mysql -e "SELECT VERSION();"
```

Cek dua variabel sebelum `LOAD DATA`: `SELECT @@secure_file_priv, @@local_infile;`
(`NULL` = tidak dibatasi; `local_infile=1` = LOCAL diizinkan di sisi server).
Klien tetap butuh `--local-infile=1`.

Dataset tutorial BDE06 (HR, 22.214 baris): `github.com/Irene-arch/HR-Dashboard-MySQL-PowerBI`,
file `Human Resources.csv`. Kolom: id, first_name, last_name, birthdate, gender, race,
department, jobtitle, location, hire_date, termdate, location_city, location_state.

## 2. Pola yang terbukti: staging VARCHAR → tabel bersih

1. `hr_raw` semua kolom `VARCHAR` — CSV memang kotor, jangan paksa tipe di awal.
2. `LOAD DATA LOCAL INFILE ... FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;`
   Pakai `\n` (bukan `\r\n`) lalu `UPDATE ... SET col = TRIM(TRAILING '\r' FROM col)` pada kolom
   terakhir, supaya file LF maupun CRLF sama-sama masuk.
3. Konversi tanggal dengan `CASE WHEN col LIKE '%/%' THEN STR_TO_DATE(col,'%m/%d/%Y') WHEN col LIKE '%-%' THEN STR_TO_DATE(col,'%m-%d-%Y') END`.
4. Bangun `hr_clean` lewat `CREATE TABLE ... AS SELECT` (kolom turunan: age, tenure, status), lalu
   `ALTER TABLE` untuk PK + index. Power BI connect ke tabel bersih ini, bukan ke staging.

## 3. Jebakan data yang hampir pasti muncul

- **Tahun dua digit terbaca ke masa depan.** MySQL memetakan tahun `00-69` ke `20xx`, jadi karyawan
  lahir 1964 yang ditulis `64` jadi 2064 → usia negatif (pernah sampai -43) dan seolah ada ratusan
  karyawan di bawah 18 tahun. Deteksi: `SELECT MIN/MAX(TIMESTAMPDIFF(YEAR, bd, CURDATE()))` dan
  `SUM(bd > CURDATE())`. Perbaikan: `UPDATE ... SET bd = DATE_SUB(bd, INTERVAL 100 YEAR) WHERE bd > CURDATE()`,
  lalu verifikasi ulang rentang usia. Tanpa langkah ini, laporan akan memuat temuan palsu.
- **Tanggal PHK di masa depan** (di dataset ini 1.018 baris, sampai 2041): jangan dihapus diam-diam.
  Set `NULL` (dianggap masih aktif) + kolom `catatan_kualitas`, lalu laporkan jumlah dan dampaknya di
  bagian kualitas data.
- **`terminated` adalah keyword** (bagian dari `LOAD DATA ... TERMINATED BY`). Alias `SUM(...) AS terminated`
  bikin syntax error 1064. Pakai alias lain (`n_terminated`, `keluar`).
- Setelah cleaning, **hitung mundur dampaknya**: berapa karyawan aktif kalau baris bermasalah dibiarkan?
  Angka pembanding itu yang dipakai untuk menjelaskan Veracity di laporan.
- **Bucket masa kerja harus disesuaikan dengan data.** Dataset yang tidak punya hire setelah 2020 membuat
  semua karyawan aktif bermasa kerja >6 tahun; bucket 0-1/1-3/3-5 tahun jadi nol semua dan grafiknya mati.
  Pakai bucket 10 tahunan dan jelaskan alasannya di komentar.

## 4. Verifikasi sebelum kirim

1. Jalankan seluruh file dari nol: `mysql --local-infile=1 -u root < tugas.sql > out.txt 2> err.txt; echo $?`.
   Exit 0 + `err.txt` kosong = script jalan. Cek juga output tiap query masuk akal (tidak NULL semua).
2. Cross-check integritas load dengan pandas: jumlah baris, distribusi satu kolom kategorikal, jumlah
   sel kosong. Kalau angka SQL dan pandas sama, parsing tidak menggeser data.
3. **Cocokkan setiap angka yang dikutip di dokumen Word ke database** lewat script: hitung ulang klaim
   dengan SQL, bandingkan string. Ini menangkap dua jenis salah: angka yang berubah setelah revisi, dan
   pembulatan. Contoh nyata: 27,01 + 27,74 + 26,46 = 81,21 tetapi hasil sebenarnya 81,20 — jumlah dari
   angka yang sudah dibulatkan bukan angka bulat dari total. Hitung persentase dari numerator/denominator,
   jangan menjumlahkan persentase per kelompok.

## 5. Flowchart di Word (rubrik hampir selalu minta)

- Simbol standar: oval (mulai/selesai), persegi panjang (proses), belah ketupat (keputusan), silinder
  (database), jajar genjang (input/output). Tulis legendanya di caption supaya tidak perlu kotak legend.
- Alur minimal: sumber data (HRIS/absensi/formulir, tandai online vs offline-to-online) → import CSV →
  cleaning → gerbang validasi (baris gagal ditandai, tidak masuk tabel final) → tabel bersih → query SQL →
  Power BI + DAX → dashboard → keputusan HRD.
- Graphviz (`sudo -n apt-get install -y graphviz`, `dot -Tpng -Gdpi=200`) memberi hasil rapi; kotak
  bercabang jangan diberi panah balik yang membingungkan — pakai `shape=note` untuk catatan kualitas data.
- **Ukuran gambar dihitung, bukan ditebak.** `tinggi = lebar × (px_tinggi / px_lebar)`. Area A4 dengan
  margin 2,5 cm ≈ 24,7 cm tinggi; sisakan ~6 cm untuk caption + paragraf penjelasan. Flowchart 10 node
  vertikal biasanya aspect ~1,45, jadi lebar 11-12 cm. Kalau kelebihan, perkecil ranksep/nodesep dan
  pendekkan label ke satu baris sebelum mengecilkan font.

## 6. Bentuk dokumen Word

- Halaman 1: identitas (nama/NIM/kelas/tanggal) + tabel tautan 3 berkas (SQL, DAX, PDF screenshot) dengan
  placeholder titik-titik; user yang mengisi tautannya.
- Halaman 2: flowchart + caption + 3-5 kalimat penjelasan yang menyebut nama tabel nyata (`hr_raw`,
  `hr_clean`) dan jumlah query.
- Halaman 3+: jawaban per nomor, 150-250 kata, tiap klaim membawa angka. Pertanyaan "pengembangan mandiri"
  wajib memuat potongan query asli + tabel hasilnya, bukan cuma cerita.
- Sertakan file measure DAX terpisah (`.dax`, bukan `.txt` yang ambigu) kalau rubrik meminta unggahan
  measure; isinya dipisah per measure dengan komentar **angka hasil yang harus muncul** di data user,
  plus pemetaan measure → visual di bagian bawah file. Lihat catatan di
  `bde06-powerbi-sales-dashboard.md` untuk konteks Power BI-nya.
- Tabel tautan di halaman 1 biasanya menuntut tiga berkas (SQL, DAX, PDF screenshot dashboard). Yang
  dikerjakan user: isi identitas, unggah ketiga berkas, dan ambil screenshot dashboard dari mesinnya sendiri.

## 7. "Mana file tabel bersihnya?" — tabel bukan file

`hr_clean` hasil `CREATE TABLE ... AS SELECT` hanya hidup di dalam database. User akan mencarinya sebagai
file dan tidak menemukannya. Begitu laporan selesai, ekspor dan kirim sekalian:

```bash
sudo -n mysql hr_analytics -e "
SELECT emp_id, first_name, ..., hire_date, IFNULL(term_date,''), status, tenure_years,
       city, state, IFNULL(catatan_kualitas,'')
INTO OUTFILE '/tmp/hr_clean.csv'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\"'
LINES TERMINATED BY '\n' FROM hr_clean ORDER BY emp_id;"
```

- `INTO OUTFILE` tidak menulis header → tambahkan baris header sendiri di Python, tulis dengan
  `encoding="utf-8-sig"` supaya Excel tidak mengacak karakter.
- Bungkus kolom nullable dengan `IFNULL(col,'')`; tanpa itu sel kosong keluar sebagai `\N` dan terbaca
  sebagai teks di Power BI.
- Verifikasi dari **file CSV-nya**, bukan dari database: `pd.read_csv` → shape, distribusi `status`, jumlah
  baris bercatatan harus sama dengan hasil query. Angka yang sama = bukti file itu memang tabel bersihnya.
- CSV ini juga jalur cadangan resmi saat koneksi Power BI gagal, jadi sebutkan itu di chat.

Kalau rubrik meminta `hr_clean` **dan** koneksi MySQL, dua-duanya diserahkan: CSV untuk bukti isi tabel,
MySQL untuk screenshot koneksi.

## 8. Repo tutorial bukan sumber DAX

Repo tutorial bergaya "HR Dashboard MySQL PowerBI" umumnya mengirim dua `.pbix` yang **tidak punya satu pun
measure** dan tidak benar-benar konek ke MySQL: query dijalankan manual, hasilnya diekspor per tabel ke CSV,
lalu diimpor sebagai tabel terpisah. Jangan janjikan file DAX dari repo sebelum membuktikannya — cara
memeriksa `.pbix` ada di skill `powerbi-pbix-reverse-engineering` (bagian verifikasi klaim DAX). Temuan itu
justru bahan refleksi yang bagus untuk user: dashboard dia konek database, punya measure, dan bisa refresh.
