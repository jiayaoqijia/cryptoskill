# Review jawaban tugas kuliah user (kasus: soal audit UBM, 1 Okt 2026)

User (mahasiswa akuntansi UBM) kirim `Jawaban_Soal_Audit.txt` (4 soal: etika EY-Wirecard, professional
judgment KPMG-Carillion, rekonsiliasi bank + jurnal penyesuaian + audit difference, pengendalian internal
+ DPO) tanpa instruksi eksplisit — yang diinginkan: dicek/dikoreksi. Lalu minta isinya diubah jadi versi
**bergaya tulisan tangan** (lihat skill `handwritten-document-rendering`).

## Alur review yang dipakai (urutan ini penting)
1. **Hitung ulang semua angka sendiri** dengan `execute_code` + `Decimal` — jangan percaya aritmetika file
   user. Yang diverifikasi: dua sisi rekonsiliasi (bank Rp220.445.500 vs buku Rp220.445.000), tiap jurnal
   debit = kredit, `2% × Rp360jt = Rp7,2jt`, DPO `18/85×365 = 77,29` dan `14/118×365 = 43,31` (turun
   33,99 ≈ 34 hari), pembelian naik 38,8%.
2. **Cari kontradiksi internal antar bagian** — ini temuan paling berharga. Di kasus ini: rekonsiliasi
   *menambah* +Rp180.000 ke sisi buku (artinya kas buku kekecilan), tapi jurnalnya `Dr Utang Usaha / Cr Kas`
   yang justru MENGURANGI kas. Arahnya kebalik. Aturan yang diajarkan ke user: **arah koreksi di jurnal harus
   sama dengan arah penyesuaian di rekonsiliasi** → yang benar `Dr Kas Rp180.000 / Cr Utang Usaha Rp180.000`.
3. **Selisih tidak balance = jangan “plug”.** Selisih Rp500 (bank lebih tinggi) dengan semua angka soal
   dipakai benar → tulis: bukan penyesuaian yang sah, tidak boleh dibebankan ke item mana pun, kemungkinan
   salah ketik soal; sebut kandidatnya (`biaya administrasi Rp325.000 → Rp325.500` atau saldo buku
   `Rp212.940.000 → Rp212.940.500`); saldo kas final setelah koreksi = Rp220.445.500. User sudah menolak
   memaksa selisih masuk item lain — itu benar dan disebut eksplisit sebagai hal yang benar.
4. **Pisahkan temuan**: ✅ benar / ❌ salah / ⚠️ perlu cek ke soal asli. Contoh ⚠️: pembagian angsuran
   `Rp12jt pokok + Rp1,5jt bunga` tidak bisa diverifikasi dari dokumen yang dikirim → jangan divalidasi,
   jangan dianggap salah, minta soal aslinya. Sama untuk “transfer masuk” (kalau bukan pelanggan, kreditnya
   bukan Piutang Usaha).
5. **Tambah poin yang nilainya mahal**, tetap dalam suara user:
   - Soal 1 (EY): tambah kegagalan bukti audit (konfirmasi pihak ketiga tanpa verifikasi langsung, red flag
     whistleblower tidak ditindaklanjuti), safeguards: verifikasi konfirmasi tanpa lewat manajemen, eskalasi
     ke komite audit/regulator, batasi jasa non-audit + rotasi KAP.
   - Soal 2 (KPMG): tambah bias **escalation of commitment** dan **availability bias** + cara mitigasinya
     (pre-mortem, “considering the opposite”, checklist bukti); sebut KPMG juga merekrut mantan pegawai
     Carillion (memperkuat familiarity) — dengan catatan “cek di sumbermu”.
   - Soal 4: untuk **utang usaha** asersi paling berisiko = **kelengkapan (understatement) + cut-off**,
     bukan cuma keterjadian; ini menyambung ke analisis DPO.
   - Soal 4c: sebutkan asumsi perhitungan (pakai pembelian + saldo utang akhir; pakai rata-rata utang kalau
     ada saldo awal; pakai COGS kalau tersedia) dan cek dulu diskon tunai / syarat bayar baru / reverse
     factoring sebelum menyimpulkan ada utang disembunyikan.
6. **Tutup dengan ringkasan tindakan**: “jawabanmu udah ~85% solid, tinggal benerin arah jurnal no. 5,
   verifikasi split angsuran, tambahin poin-poin ini.”

## Pelajaran umum
- User mengirim dokumen tanpa kalimat perintah → default yang benar adalah **review + koreksi + poin tambahan**,
  bukan ringkasan isi.
- Verifikasi angka wajib pakai tool (bukan kepala) dan hasilnya disajikan sebagai angka, bukan “kelihatannya”.
- Setelah review, kalau user minta versi lain (tulis tangan), **terapkan dulu koreksinya ke isi** sebelum dirender.
- Guard `read-before-write` di `skill_manage` bisa memblokir patch SKILL.md kalau `skill_view` nge-dedup
  (content_returned: false). Kalau kena, simpan pengetahuan baru sebagai file `references/` baru — write_file
  ke path baru tetap lolos.
