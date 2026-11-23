# Artikel riset sendiri → deck presentasi + naskah bicara

Dipakai saat user mengirim artikel/paper kelompoknya sendiri (DOCX/PDF) lalu minta PPT dengan daftar
bagian tetap, sering sekalian "kasih DOCX script tiap pembahasan karena gw butuh pemahaman juga".
Deck dan naskah adalah dua file: deck untuk audiens, naskah untuk pembicara.

## Aturan yang tidak boleh dilanggar

1. **Semua angka di slide harus ada di artikel.** Ekstrak teks artikel sekali, jadikan itu satu-satunya
   sumber angka. Kalau ragu, cari string angkanya di teks hasil ekstraksi sebelum menulisnya ke slide.
2. **Bagian yang diminta tapi tidak ada babnya di artikel** (mis. "green theory") disusun dari sitasi
   yang sudah ada di daftar pustaka artikel + konstruk yang benar-benar diukur. Jangan menambah referensi
   baru untuk menutup bagian itu; sebut di chat bahwa bagian itu rangkaian, bukan bab baru.
3. **Hipotesis yang ditolak tetap tampil** dengan koefisien dan p-nya, dan ditandai visual (bar abu, label
   "paling mungkin ditolak"), bukan dihapus. Menyembunyikan satu jalur yang gagal adalah cara tercepat
   kehilangan kredibilitas di ruang sidang.
4. **Jangan menyimpulkan signifikan dari koefisien saja**: kutip p atau interval kepercayaan. Jangan
   menaikkan "84% pernah membeli" pada pertanyaan centang-banyak menjadi pangsa pasar atau konversi.
5. **Model pengukuran sebelum koefisien jalur.** Satu slide berisi tabel ambang (loading, alpha, CR, AVE,
   HTMT) supaya angka jalur di slide berikutnya tidak muncul tanpa syarat.
6. **Angka robustness ikut tampil** kalau artikel melaporkannya (mis. n=100 utama, n=96 uji ketahanan),
   sebagai catatan kecil di slide jalur, bukan dihapus karena "bikin ramai".

## Bentuk deck

- Judul cover = **temuan**, bukan judul artikel. Contoh pola: "Orang membeli X, jarang menyebutnya lebih
  dulu" untuk kasus ingatan rendah tapi pembelian tinggi. Subjudul menyebut sampel dan segmen.
- Satu ide per slide, maksimal tiga angka besar, dan label tiap angka menyebut pertanyaannya
  (top-of-mind vs pertimbangan vs pembelian) karena tiga indikator itu tidak saling menggantikan.
- Konteks perusahaan/pasar ditaruh di kolom terpisah dengan catatan "angka konsolidasi grup, bukan pasar
  lokal" supaya tidak dipakai menyimpulkan perilaku konsumen.
- Grid tetap: 13.333×7.5 in, margin 0.85, kicker 10.5 pt accent caps, judul 29 pt bold, isi 12–13 pt,
  garis rambut 0.75 pt sebagai pemisah, footer + nomor halaman.
- Prosa mengalir, bukan bullet bertanda hubung; user ini membaca daftar berpoin sebagai output AI.
- Palet: netral + satu aksen (hitam #14171F, abu #6B7280, aksen merah/biru). Warna dipakai untuk satu
  hal: menandai temuan yang gagal atau variabel terkuat.

## Bentuk naskah (DOCX terpisah)

Tiap slide dapat satu halaman dengan tiga blok:

- **Tujuan slide** — satu kalimat: apa yang harus audiens percaya setelah slide ini.
- **Script** — ditulis untuk diucapkan: kalimat pendek, tanpa "hadirin yang berbahagia", angka
  diucapkan sebagai kata ("nol koma dua delapan tiga"), dan setiap paragraf membawa satu angka.
- **Kalau ditanya** — 1–3 Q&A dengan jawaban yang memuat angka aslinya, termasuk pertanyaan yang
  menyerang metode (n kecil, nonprobabilitas, PLS vs regresi).
- Slide berat metode dapat tambahan **Yang perlu dipahami**: alasan di balik pilihan, bukan ringkasan.

Tambahan yang membuat naskah benar-benar dipakai: page break per slide (heading tidak boleh menggantung
sendiri di dasar halaman), perkiraan durasi total, dan daftar potong kalau slot presentasi lebih pendek.
Lampiran: tabel angka yang gampang salah diucapkan + Q&A metode.

## Alur kerja

1. Ekstrak artikel: `zipfile` + regex `word/document.xml` (atau `scripts/docx_to_text.py`), simpan ke
   `/tmp/<topik>.txt`. Grep heading berpola `^[0-9]+(\.[0-9]+)*\s+` untuk menemukan batas bab.
2. Ambil tabel hasil + bagian pembahasan + simpulan, dan catat variabel mana yang ditolak.
3. Tulis generator deck (`python-pptx` ad-hoc, bukan spec JSON) dengan helper `tx/paras/rule/stat/table`
   supaya grid konsisten; simpan satu file `build_deck.py`.
4. Tulis generator naskah (`python-docx`) di file terpisah, isi teks script sebagai string literal yang
   sudah final — jangan generate prosa dari template.
5. Render QA: `soffice --headless --convert-to pdf` untuk keduanya, lalu `pymupdf` → PNG dpi 90–110,
   periksa dengan `vision_analyze` (tumpang tindih, teks kepotong, heading menggantung), perbaiki, ulang.
6. Kirim PPTX + PDF deck + DOCX naskah + PDF naskah. PDF wajib karena font tidak ikut di PPTX.

## Jebakan

- Grafik native: label sumbu bawaan memakai titik desimal walau dokumen berbahasa Indonesia, dan
  `BAR_CLUSTERED` menaruh kategori pertama di bawah — detail perbaikannya ada di skill `powerpoint`.
- Konsistensi format: naskah menulis "0,283" sementara slide menulis "0.283" terbaca sebagai dua angka
  berbeda; samakan sejak generator, bukan setelah render.
- Jangan mengarang slide tambahan ("rekomendasi strategi nasional") di luar daftar bagian yang diminta;
  tambahan hanya kalau datanya menopang.
- Deck yang terlalu padat: kalau satu slide butuh lebih dari ~70 kata di badan, pecah jadi dua slide atau
  pindahkan detailnya ke naskah.
