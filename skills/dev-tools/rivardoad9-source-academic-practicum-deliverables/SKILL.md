---
name: academic-practicum-deliverables
description: "Modul tugas kuliah + dataset jadi paket sesuai rubrik."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [kuliah, tugas, modul, docx, rubric, dataset, deliverable]
---

# Deliverable praktikum kuliah (modul + dataset → paket siap kerja)

## When to Use / Kapan pakai
- User (mahasiswa) kirim **modul/praktikum** (DOCX/PDF) berisi capaian pembelajaran, tahapan, tugas
  mandiri, dan **rubrik penilaian** — lalu minta bantuan mengerjakan (Power BI, Excel, SQL, Python, dll).
- User kirim **dataset praktikum** (sering beberapa CSV) bareng modulnya.
- User minta bantuan kuesioner riset (Google Forms): review instrumen, nyebar, atau minta "diisiin dummy".
- User bilang hal seperti “kasih file sesuai yg dibutuhin aja” / “jangan kebanyakan file”.
- User kirim **artikel/paper kelompoknya sendiri** lalu minta deck presentasi (struktur bagian ditentukan
  user) dan/atau naskah bicara tiap bagian → `references/paper-to-deck.md`.

Skill ini soal **alur kerja & bentuk deliverable**. Tooling khusus Power BI (bedah `.pbix`, ekstrak measure
DAX, layout visual) ada di skill terpisah: `powerbi-pbix-reverse-engineering`.

## Lane & workspace untuk user ini
- Persona khusus tugas: profil `asdos`, bot Telegram `@tugaskmpus_bot`. Persona, skill map, dan batas
  kerasnya (jangan ngarang angka, jangan ngaku submit, tolak kerja-laundering) ada di
  `~/.hermes/profiles/asdos/SOUL.md` — baca file itu kalau tugas yang sama dikerjakan dari lane lain,
  supaya aturannya tidak bercabang.
- File kerja tinggal di `~/tugas/`: `inbox/` (kiriman user), `data/` (dataset + teks modul), `out/`
  (deliverable siap kirim), `arsip/` (semester lalu, per kode MK). Taruh output baru di `out/` — root
  `~/tugas` masih campur file lama (foto buku, PDF jawaban) dan bukan tempat naruh hasil baru.

## Prinsip (urutan berpikir, bukan urutan tool)
1. **Baca modulnya dulu.** Deliverable, bobot rubrik, dan “kata kunci wajib” (mis. “screenshot harus ada
   nama + NIM”) menentukan bentuk kerjaan. Jangan langsung ngoprek dataset.
2. **Petakan tiap komponen rubrik → langkah/file konkret.** Buat tabel bobot → apa yang harus ada.
   Komponen yang gampang kelewat (dan mahal): watermark nama+NIM di dalam kanvas/laporan, jumlah tangkapan
   layar minimum, file hasil kerja sendiri (bukan file orang lain), format pengumpulan (1 Word/PDF).
3. **Angka = patokan cek, bukan jawaban siap salin.** Hitung angka yang diminta dari dataset yang user
   kirim, lalu sajikan sebagai “angka ini yang harus muncul di kerjaan lu kalau benar”.
   Label draf untuk bagian interpretasi, dan suruh user membaca ulang dari hasil kerjanya sendiri.
   Kalau modul menyertakan kunci jawaban (lampiran output / kunci dosen), pakai kunci itu sebagai
   **validator metode**, bukan sumber angka: hitung ulang dari data mentah, lalu bandingkan. Cocok berarti
   metode lu benar dan aman diklaim; beda berarti ada parameter yang salah — cari dulu sebelum mengirim,
   jangan kirim angka kunci sebagai hasil hitungan sendiri.
   Hitung angka **di dalam script generator dokumen**, bukan diketik ulang ke teks: satu nilai
   dipakai untuk tabel dan kalimat naratif lewat f-string, supaya angka di prosa tidak bisa
   menyimpang dari angka di tabel setelah revisi.
4. **Paket ramping.** Hanya file yang dipakai. Sebut eksplisit apa yang **tidak** dikirim + alasannya
   (dataset sudah ada di modul, file orang lain tidak boleh disubmit, dsb).
5. **Integritas.** File contoh/orang lain (GitHub, repo teman) = referensi belajar, jangan disarankan
   submit apa adanya. Tugas yang mensyaratkan bukti proses (screenshot Power Query/Model) memang harus
   dikerjakan user sendiri — bantu dengan panduan, bukan dengan hasil jadi.
   Kalau user minta **ganti nama di file tugas teman** (“jadi punya gw”) atau minta diparafrase biar tidak
   kelihatan nyontek: jangan dikerjakan, termasuk versi “cuma ganti nama doang”. Yang ditawarkan adalah
   bangun ulang: hitung sendiri dari dataset modul, susun ulang strukturnya, tulis ulang kalimatnya, isi
   identitas user. Sertakan kesalahan yang ada di file sumber (notasi hipotesis tertukar, label pasangan
   Tukey kebalik, angka uji beda) sebagai alasan konkret kenapa menyalin merugikan, bukan sebagai ceramah.
   Sampaikan batas ini sekali, singkat, lalu langsung kirim hasil bangun ulangnya.
6. **Data riset harus dari responden nyata.** Kalau user minta kuesionernya diisi "dummy/palsu" — walau cuma
   10 baris — tolak bagian itu sekali dengan alasan teknis (uji validitas dan reliabilitas berdiri di atas
   baris karangan, dan pola jawaban buatan gampang kebaca penilai), lalu langsung tawarkan yang benar: review
   instrumen, paket distribusi, dan tes QA 2 respons. Tes QA bukan data: sebut timestamp dan jawaban persisnya
   supaya user bisa menemukan barisnya, dan ingatkan hapus sebelum analisis. Jangan mengulang penolakan saat
   user menawar turun jumlahnya — satu kali cukup, sisanya eksekusi.

## Langkah
1. **Ekstrak teks modul.** Coba `read_file`; kalau gagal (`document extraction failed`) atau butuh tabel,
   pakai `scripts/docx_to_text.py` (zipfile + XML, tanpa dependency). Yang penting ditangkap dari modul:
   identitas sesi, tahapan + rujukan timestamp video, daftar tugas, rubrik + bobot.
2. **Inventaris dataset yang user kirim.** File kiriman user mendarat di `~/.hermes/cache/documents/`
   (nama `doc_<hash>_<nama_asli>`). Cek: kolom, jumlah baris, periode, total angka kunci.
3. **Validasi silang kalau ada sumber kedua** (mis. rekonstruksi dari sumber lain, README repo): kalau
   kolom & total identik → aman mengklaim “angka kerjaan lu = angka hitungan gw”.
4. **Data hygiene SEBELUM menyusun relasi/rumus.** Cari: typo tahun (`2002` vs `2022`), bulan terpotong di
   ujung periode, format tanggal ambigu (dd/mm vs mm/dd), kolom kategorikal yang diubah jadi tabel dimensi.
   Laporkan temuan + cara betulinnya di langkah 1 user (Power Query: *Replace Values* / *Change Type*).
5. **Hitung angka yang diminta rubrik**: top-N (mis. profit tertinggi), perbandingan antar segmen, bulan
   tertinggi/terendah, pencapaian target, margin. Sertakan angka pendukung interpretasi (share %, margin %)
   plus “bahan refleksi teknis” = daftar kendala nyata yang bakal user alami saat membangun.
6. **Rakit + kirim.** ZIP kecil, isinya disebut satu-satu (fungsi 1 baris per file), plus **3 hal paling
   gampang bikin nilai bocor** di pesan. Tutup dengan tawaran bantuan konkret (“kirim pesan error/screenshot,
   gw betulin”) — bukan pertanyaan retoris.

## Jebakan
- **Dataset modul yang TIDAK ikut dikirim (kasus SPSS/IBM sample data).** Modul SPSS sering nyuruh pakai file
  bawaan instalasi (`Samples → English`, mis. `grocery_1month.sav`). File itu **tidak bisa diunduh** dari web:
  ibm.com memblokir extractor (PDF/HTML balik 5-300 byte), tidak ada mirror GitHub (udah dicek: code search API
  butuh auth 401, repo search + tree walk nol hasil, DDG/Mojeek/curl-search nol), dan tidak ada di mesin user.
  Jangan habisin 10+ tool call ngejar file itu. Yang benar: (a) angka **file-fixed** (N populasi, nama variabel,
  rata-rata populasi) baru bisa dipastiin kalau user kirim `.sav`-nya — minta itu; (b) angka yang **bergantung
  undian user** (N sampel, rata-rata sampel, batas CI) memang MUSTAHIL dikasih dari jauh, karena SPSS ngundi
  tiap kali; (c) yang bisa langsung dikirim = lembar jawaban siap-isi + tulisan naratifnya. Baca `.sav` pakai
  `uv venv /tmp/x && uv pip install pyreadstat pandas` (pandas wajib: pyreadstat import-nya butuh pandas).
- **Bikin lembar jawaban siap-isi (bukan cuma penjelasan).** Untuk ICA/kegiatan kelas, deliverable paling
  berguna = satu DOCX: tiap bagian modul, checkbox udah ditandai (☒/☐), jawaban naratif udah jadi, dan slot
  angka ditandai `______________` + 1 baris italic "record from your SPSS output" pakai jalur menunya.
  Tulis **dalam bahasa modul** (modul Inggris → dokumen Inggris; coaching bahasa Indonesia taruh di chat).
  Tambah tabel "self-check sebelum submit" dari submission checklist modul. Bonus murah: file `.sps` (SPSS
  syntax) yang jalanin populasi→sampel 10%→95% CI dalam 3 blok — pakai placeholder SATU nama variabel
  (bukan `VARIABLES=ALL`, yang bisa kena variabel string) + komentar cara gantinya.
- **Tabel kosong di modul itu tempat jawaban, bukan hiasan.** Isi persis di urutan dan label modul
  (`Group Statistics`, `Levene’s Test`, baris `t-test`), satu tabel per blok, lengkap dengan angka yang
  diminta kolomnya. Tambah satu tabel ringkasan keputusan (uji / statistik / Sig / tolak-tidak) di depan
  supaya penilai cepat; sisipkan tabel itu setelah ringkasan teks, bukan menggantikan jawaban per butir.
- **Samakan parameter alat hitung dengan alat yang dipakai modul.** SPSS menghitung Levene’s Test dengan
  `Based on Mean`, sedangkan default `scipy.stats.levene` adalah `center="median"` — bedanya tipis tapi bisa
  membalik keputusan baca baris. Pakai `stats.levene(a, b, center="mean")` untuk mereproduksi SPSS.
  Uji t berpasangan = uji satu sampel atas selisih: nilai t, df, dan p harus identik dengan
  `stats.ttest_1samp(d, 0)`; kalau tidak identik, ada yang salah pada data atau pemasangan barisnya.
- **Data simulasi harus dinyatakan, bukan disamarkan.** Modul yang mengizinkan “data dibuat secara wajar”
  tetap menuntut kejujuran: tulis `data simulasi` di dokumen dan sebutkan keterbatasannya di chat. Jangan
  menyajikannya seolah responden nyata.
- **Script SQL yang belum dijalankan bukan deliverable.** Jalankan file `.sql` dari database kosong
  (`mysql --local-infile=1 < tugas.sql`), pastikan exit 0 dan stderr kosong, baru dikirim. Setelah dokumen
  jadi, cocokkan **setiap** angka yang dikutip ke database lewat script — jangan andalkan ingatan atau
  penjumlahan persentase (jumlah persentase yang sudah dibulatkan tidak sama dengan persentase total).
- **DOCX belum selesai sebelum dilihat.** Konversi ke PDF (`soffice --headless --convert-to pdf`), render
tiap halaman jadi PNG (`pymupdf`, dpi 95), lalu periksa satu per satu: gambar + paragraf kepotong halaman,
tabel melewati margin, atau ada halaman yang isinya cuma dua baris. Hitung lebar gambar dari aspect ratio
(`tinggi = lebar × px_tinggi / px_lebar`) **sebelum** build, bukan setelah kelihatan jelek.
- `read_file` bisa gagal di `.docx` walau file ada → pakai `scripts/docx_to_text.py`. Kalau nama file berisi
  spasi/kurung, `cp` dari shell bisa gagal walau filenya ada; salin lewat Python (`shutil.copy` +
  `glob`) ke path sederhana dulu.
- **Jangan asal upgrade deliverable jadi bundel besar.** User pernah menegur: “kasih file sesuai yg
  dibutuhin aja”. Bundel 20+ file (aset, contoh tabel, file referensi) menambah noise, bukan nilai.
- Dataset modul sering bercacat: typo tahun bikin lookup gagal (target blank 12 bulan), kolom tanggal
  masih text (relasi Calendar gagal tanpa error jelas), ujung periode tidak penuh (bulan terakhir parsial).
- Angka di contoh/template sering **angka satu tahun tertentu** (mis. `$630K` = filter 2023), bukan total —
  cek konteks filternya dulu sebelum menyimpulkan kerjaan user salah.
- Kalau rubrik minta “tidak boleh jawaban generik dari AI”, jangan bikin jawaban generik: tiap klaim
  interpretasi harus nempel ke angka spesifik hasil hitungan sendiri.
- **Analisis kelompok gampang salah dibaca.** "Porsi terbesar berasal dari kelompok X" bukan "risiko tertinggi di
  kelompok X"; rate butuh denominator per kelompok. Korelasi level unit (departemen/cabang) bisa berlawanan dengan
  level individu — laporkan keduanya dan ambil kesimpulan dari level yang datanya cukup.
- **Gambar dashboard buatan sendiri bukan screenshot Power BI.** Kalau user belum/bisa membuka Desktop, sebut PNG
  hasil query sebagai referensi layout di chat dan di nama file; jangan biarkan dipakai sebagai bukti screenshot.
- Bagian esai (mis. 150–250 kata) beri **kerangka + angka**, dan bilang user harus mengganti kalimat yang
  nggak dia pahami. Jangan menyamar sebagai tulisan user.

## Aturan deliverable untuk user ini
- Kirim **hanya file yang dibutuhkan**, satu ZIP kecil, dan sebutkan isinya per file.
- Sebutkan isi yang sengaja **tidak** dikirim + alasannya.
- Bahasa Indonesia santai (gw/lu) di chat; isi dokumen deliverable tetap rapi & formal-sopan.
- **Kalau user memutuskan submit apa adanya, berhenti menjual perbaikan.** Setelah temuan besar (mis. file
dashboard yang dikumpulkan ternyata salinan tutorial), satu putaran penjelasan + jalur perbaikan sudah cukup.
Kalau jawabannya "udah lah gw kumpulin aja", terima tanpa mengulang daftar masalah: sebut satu kalimat jujur
tentang apa yang akan dilihat penilai, satu-dua cek 10 detik yang benar-benar murah (akses folder Drive =
"anyone with the link", berkas ada di slot yang benar), lalu tutup. Mengulang pitch setelah keputusan diambil
terbaca sebagai tidak mendengar — dan ini user yang butuh ditopang, bukan didesak.
- **Jangan tutup dengan “mau gw buatkan X?”** — langsung kerjakan, atau sebut langkah berikut yang bisa gw ambil.
- **Identitas dan nama file.** Nama, NIM, dan kelas diisi persis seperti yang user sebut; jangan pernah
  mengarang NIM atau memakai identitas pemilik file sumber. Nama file deliverable memuat NIM
  (`Laporan_<topik>_<Nama>_<NIM>.docx`) supaya dosen tidak perlu membuka isinya. Setelah mengganti
  identitas, cek metadata DOCX juga (lihat skill `docx`).
- **Kerjakan persis slice yang diminta.** Kalau user bilang “output SQL aja, sisanya gw kerjain”, kirim SQL
  saja dan sebut sisanya belum dikerjakan. Bagian tambahan (flowchart, jawaban, refleksi) dikerjakan saat
  diminta di pesan berikutnya, bukan diborong di awal.

## File pendukung
- `references/people-analytics-scorecard.md` — tugas People Analytics (CSV karyawan/absensi/penjualan/survei →
  MySQL → dashboard): muat data + NULLIF tanggal kosong, bukti index & ukuran tabel, jebakan porsi vs rate dan
  ecological fallacy, bentuk dokumen 2 halaman + lampiran, dan upload Drive lewat REST (quote `q`, refresh token).
- `references/questionnaire-fieldwork.md` — kuesioner riset: batas dummy vs tes QA, checklist instrumen sebelum
  disebar, urutan kanal distribusi + target n, dan cara mengisi Google Forms lewat `FB_PUBLIC_LOAD_DATA_`
  (entry id per baris grid) + POST `formResponse`, termasuk verifikasi string konfirmasi.
- `scripts/docx_to_text.py` — ekstrak paragraf + tabel dari `.docx` (zipfile + ElementTree, tanpa pip).
- `references/spss-mean-comparison-tests.md` — uji beda rata-rata (independent/paired/One-Way ANOVA +
  Tukey) untuk lembar jawaban: kapan pakai yang mana, cara memilih baris output, pemetaan scipy → kolom
  SPSS, dekomposisi SS dan η² tanpa statsmodels, format kalimat pelaporan, dan jebakan notasi H₀.
- `references/bde06-powerbi-sales-dashboard.md` — studi kasus lengkap modul BDE06 (UBM, Power BI Sales
  Dashboard): struktur tugas, schema dataset, angka verifikasi, temuan cacat data, rubrik → langkah.
- `references/mysql-cleaning-sql-deliverable.md` — tugas CSV kotor → MySQL → Power BI → Word: setup DB lokal,
  pola staging VARCHAR, jebakan tahun dua digit & tanggal masa depan, verifikasi script + angka, ukuran
  flowchart Graphviz untuk A4, dan bentuk dokumennya.
- `references/paper-to-deck.md` — artikel riset sendiri → deck presentasi + naskah bicara (DOCX): urutan
  11 bagian, judul slide = temuan, angka wajib ketelusuran ke artikel, pola script per slide (tujuan/script/
  kalau ditanya), dan QA render sebelum kirim.
- `references/pb5mat-ica5-spss-sampling-2026-09-22.md` — ICA 5 PB5MAT (UBM): modul SPSS 20 menit
  "Population → Sample → Estimate → CI", isi 12 part + submission checklist, bentuk deliverable yang dipakai
  (DOCX lembar jawaban siap-isi + `.sps`), dan kenapa angkanya tidak bisa dikasih dari jauh.
