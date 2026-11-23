# Kuesioner riset: review instrumen, sebar, tes QA

Konteks: user mahasiswa minta bantuan kuesioner (biasanya Google Forms) untuk tugas Riset Pemasaran /
Metodologi. Yang dia butuh hampir selalu bukan "isiin dong", tapi angka respons yang cukup dan bisa
dipertahankan di depan dosen.

## Batas keras: dummy bukan data

Menolak mengisi respons palsu untuk dianalisis, berapa pun jumlahnya (10 pun tidak). Alasannya teknis, bukan
moral, dan itu yang disebut ke user:

- Uji validitas, reliabilitas, dan hipotesis dihitung dari baris yang ada. Baris karangan menggeser rata-rata
dan mengecilkan varians, jadi hasilnya kelihatan rapi — justru kerapian itu yang bikin curiga.
- Pola buatan gampang kebaca: durasi pengisian seragam, matriks dijawab lurus, timestamp berdekatan.
- Risikonya jatuh ke user (sanksi akademik), bukan ke agent.

Sampaikan sekali, satu-dua kalimat, lalu langsung pindah ke yang bisa dikerjakan. Jangan mengulang ceramah
saat user menawar ("cuma 10"). Tiga hal yang benar dan bisa langsung dieksekusi: review instrumen, paket
distribusi, dan tes QA 2 respons yang dihapus sebelum analisis.

## Review instrumen sebelum disebar

Cek berurutan, laporkan hanya temuan yang nyata (jangan mengarang masalah):

1. **Screening gate.** Opsi di luar kriteria (mis. "di bawah 18", "di atas 35") harus mengarahkan ke section
   penutup / menolak, bukan cuma dicatat. Kalau cuma dicatat, sampel kecampur dan harus dibuang manual.
   Cek di struktur form: apakah opsi itu punya aksi "go to section". Jangan cek dengan mengirim respons di
   luar kriteria — itu menambah baris sampah yang harus dihapus.
2. **Titik lelah.** Matriks dengan >6 baris x >3 kolom adalah tempat orang keluar. Usulkan memotong ke merek
   inti + satu kategori "lain".
3. **Tipe pertanyaan vs maksud.** Pertanyaan "apa alasannya" yang dibikin checkbox pilihan tertutup =
   kehilangan alasan yang tidak terduga. Tambah opsi "Lainnya" bertipe teks.
4. **Typo** di judul/pertanyaan. Form riset yang typo bikin responden ragu, dan gampang kelihatan.
5. **Anonim vs login.** Tanpa login: response rate bagus, tapi tidak ada cara dedupe selain cek manual di
   sheet. Dengan "batasi 1 respons": lebih bersih tapi butuh akun Google. Sebutkan trade-off-nya, jangan
   putuskan sendiri.
6. **Estimasi waktu** di intro harus jujur. Kalau isinya 4 bagian dan matriks panjang, tulis 5–10 menit,
   bukan "beberapa menit".

## Sebar: urutan yang benar-benar menambah respons

Broadcast grup itu paling murah tapi paling rendah yield. Urut dari yang paling nembus:

1. DM personal ke ~20 orang yang jelas masuk kriteria (bukan broadcast), satu per satu. Minta forward ke 2
   orang. Ini penyumbang terbesar per menit usaha.
2. Grup WA angkatan / alumni, kirim 19:00–21:00, bukan pagi.
3. Story IG / Threads: screenshot form + satu kalimat alasan riset, bukan link telanjang.
4. Titip ke 3–5 orang yang punya audiens relevan (komunitas fashion/thrift) untuk repost.
5. Dosen / koordinator kelas forward ke kelas lain — biasanya penambah terbesar dalam sehari.

Target n: PLS-SEM pakai patokan 10 x jumlah indikator terbesar (biasanya 100–150); regresi 5–10 x jumlah
variabel (50–80 cukup). Lolos screening biasanya 70–80% dari yang klik, jadi sebar ke ~1,4 x target.

Template DM (sesuaikan, jangan kirim generik):

> Halo [nama], gw lagi riset pemasaran buat tugas kuliah, objeknya [merek]. Butuh 5 menit lu isi kuesioner,
> kriteria lu masuk ([umur] dan pernah beli [kategori] setahun terakhir). Nggak minta nama atau email.
> Ini linknya [link]. Kalau ada 2 temen yang cocok, boleh forward ya.

## Tes QA: isi form tanpa klik satu-satu

Tujuan: membuktikan form jalan (section, gate, matriks, pertanyaan wajib) dan menemukan cacat desain.
Dua respons, profil berbeda, supaya jalur validasi benar-benar teruji.

**Jangan pakai klik radio satu per satu untuk matriks panjang.** Renderer Google Forms berat; ratusan klik
di satu halaman bisa bikin tab stall di tengah jalan dan pilihan yang sudah diisi hilang. Jalur HTTP lebih
cepat, atomik, dan hasilnya bisa diverifikasi.

### 1. Ambil struktur + entry id

```bash
curl -sL --compressed -A "Mozilla/5.0" "<VIEWFORM_URL>" -o /tmp/form.html
```

Entry id tidak ada di HTML statis (dirender JS). Ambil dari blob konfigurasi:

```python
import re, json
h = open('/tmp/form.html', encoding='utf-8', errors='replace').read()
data = json.loads(re.search(r'FB_PUBLIC_LOAD_DATA_\s*=\s*(\[.*?\]);\s*</script>', h, re.S).group(1))
items = data[1][1]          # daftar item: section header + pertanyaan
fbzx = re.search(r'name="fbzx" value="(\d+)"', h).group(1)   # token sesi, wajib ikut
```

Tipe item (`it[3]`): `2` pilihan ganda, `4` checkbox, `5` linear scale, `7` grid/matriks, `8` section header,
`6` halaman penutup. Entry id: `it[4][0][0]` untuk tipe 2/4/5.

**Grid punya entry id per baris**, bukan satu untuk seluruh matriks:

```python
rows = [(r[0], (r[3] or [''])[0]) for r in it[4]]   # (entry_id, label baris)
opsi = [o[0] for o in it[4][0][1]]                  # opsi kolom
```

Kirim ke id baris, bukan id matriks — kalau salah, cuma satu baris yang masuk dan sisanya dianggap kosong.

### 2. Susun payload + validasi dulu

Bandingkan setiap nilai dengan daftar opsi hasil parsing, dan untuk grid pastikan jumlah nilai = jumlah baris.
Kalau ada yang tidak cocok, Google membalas halaman form lagi tanpa error yang jelas — kelihatan sukses
tapi tidak tersimpan.

```python
payload = [(f"entry.{eid}", v) for eid, values in answers for v in values]
payload += [("fvv", "1"), ("pageHistory", "0,1,2,3"), ("fbzx", fbzx)]
```

`pageHistory` harus memuat semua halaman. Tanpa itu, form multi-bagian menganggap jawaban halaman
belakang tidak ada.

### 3. POST + verifikasi isi balasan, bukan status

```python
req = urllib.request.Request(FORM_RESPONSE_URL, data=urllib.parse.urlencode(payload).encode(),
                             headers={"User-Agent": "Mozilla/5.0",
                                      "Content-Type": "application/x-www-form-urlencoded"})
html = urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "replace")
assert any(k in html for k in ("已记录", "recorded", "telah direkam")), "tidak tersimpan"
```

HTTP 200 saja bukan bukti: form yang ditolak juga balas 200 dengan halaman form lagi. Cek string konfirmasi,
idealnya juga cari elemen error validasi (`freebirdFormviewerViewItemsItemErrorMessage`).

### 4. Laporkan supaya bisa dihapus

Setelah submit, kirim ke user: **timestamp WIB tiap respons** dan **jawaban pembeda** (profil yang dipakai),
plus langkah hapus yang benar: tab Respons → ikon Google Sheets → hapus dua baris terbawah (Delete row, bukan
filter/sembunyikan) → cek jumlah respons di form turun 2. Baris tes yang tertinggal di sheet akan ikut
terhitung di analisis dan merusak exactly hal yang tadi ditolak.

## Jebakan yang sudah kena

- Submit tanpa login itu memang bisa (POST biasa, 200). Artinya form terbuka untuk bot; sebutkan ke user
  sebagai risiko kualitas data, bukan sebagai alasan untuk tidak menyebar.
- Dua respons dengan profil sama tidak menguji apa pun. Bedakan umur/pekerjaan/frekuensi dan minimal satu
  jalur matriks, supaya section logic dan required-field benar-benar terlewati.
- Form yang minta login Google menyimpan progres per akun; POST tanpa sesi tetap jalan, tapi jangan pakai
  akun user untuk itu.
