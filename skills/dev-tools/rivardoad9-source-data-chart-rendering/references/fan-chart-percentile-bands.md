# Fan chart pita persentil (rentang probabilitas) + tata letak legenda

Dibuat 8 Okt 2026 untuk permintaan user *"cb bikin probability range harga btc"* — satu gambar yang
menjawab "harganya nanti di kisaran berapa", bukan tabel angka saja. Generator yang jalan:
`~/.hermes/scripts/diag/make_btc_prob_chart.py` (stdlib → HTML+inline SVG → screenshot chromium).
Data dump: `~/.hermes/data/btc_prob_range.json` (dari `prediction-market-odds/scripts/deribit_prob_range.py`).
Hasil: `~/obsidian-vault/attachments/btc-prob-range-2026-10-08.png`.

## Bentuk chart-nya

- Sumbu X = horizon waktu **kategorikal** (satu kolom per expiry, jarak sama). Jangan pakai skala
  linear hari: 1 hari vs 351 hari bikin kolom kiri menempel jadi satu dan chart tak terbaca.
  Label dua baris: tanggal ("30 Okt") di atas, jumlah hari ("22 hari") di bawah.
- Pita = **polygon**, bukan dua garis: `poin atas` (P95 maju) + `poin bawah` (P5 mundur) → `fill`.
  Dua pita: P5–P95 opacity ~0.20 (90% kemungkinan), P25–P75 opacity ~0.45 (50% kemungkinan).
- Garis median (P50) warna ungu `#c9a4ff`; garis spot `#ffb020` putus-putus horizontal.
- Label nilai di ujung kanan (P95/P75/P50/P25/P5) **di luar area plot** (`X1 + 22`), masing-masing
  dengan titik kecil; jangan taruh label di dalam pita.
- Kotak anotasi di bawah plot memuat kalimat kunci, mis. "50% kemungkinan (30 Okt): $77.902 - $87.361
  | 90% kemungkinan: $71.730 - $94.878 | IV 35%/tahun" — angka terpenting harus terbaca di gambar,
  bukan cuma di chat.
- Median lognormal **melandai ke bawah** sementara spot datar. Itu artefak model (exp(−σ²T/2)), bukan
  sinyal bearish — jangan dikomentari sebagai "pasar pesimis" (skew asli memang ke kiri, tapi bedanya
  kecil). Sebut eksplisit kalau user menanyakan kenapa median di bawah spot.

## Pitfall tata letak yang kena di sesi ini

| Gejala | Sebab | Fix |
|---|---|---|
| Item legenda terakhir terpotong di tepi kanan ("garis putus kuning = sp…") | 4 item dalam SATU baris; `lx += len(text)*8.6 + 46` melewati lebar kanvas, dan `W` tidak ikut menampung legenda | pecah legenda jadi **2 baris × 2 kolom** (`for row_i, pair in enumerate((leg[:2], leg[2:]))`), reset `lx = 60` tiap baris; hitung `svg_h` dari jumlah baris legenda, bukan hardcode |
| Label horizon tertulis "T+22h" padahal 22 hari | akhiran `h` disalin dari pola T+h jam | tulis satuan sebenarnya: `{days:.0f} hari` (atau "hari"/"d"), jangan campur satuan |
| Pembaca tak tahu sumbu Y itu apa | tick cuma "45k … 145k" | tambah label unit kecil di atas kolom tick: `USD` di `x = X0 - 12, y = Y0 - 18` |
| Legenda mirip garis di plot / warna tak jelas | legend ditulis tanpa contoh visual | tiap entri punya swatch warna sungguhan (termasuk garis putus = swatch kuning), 1 entri per warna yang dipakai |

Skala teks yang bekerja di Telegram: judul 30, subjudul 19, tick 16–17, label hari 15, anotasi 19,
legenda 17, `W = 1400`, `--force-device-scale-factor=2`.

## Verifikasi (wajib, dua putaran di sesi ini)

`vision_analyze` pada PNG-nya **sebelum** dikirim, dan tanyakan hal spesifik: "apakah legenda tampil
penuh 4 item tanpa terpotong, label 'X hari' terbaca, ada teks bertumpuk/terpotong?". Putaran pertama
menemukan legenda terpotong; putaran kedua lolos. Jangan kirim chart yang belum dilihat sendiri.

## Cara mengirim

`MEDIA:/abs/path.png` satu baris + 2–4 baris "cara baca" di chat (pita luar = 90%, pita dalam = 50%,
garis mana median/spot). Tabel angka horizon pendek tetap dikirim sebagai teks — gambar melengkapinya,
bukan menggantinya. Simpan PNG + JSON dump ke `~/obsidian-vault/attachments/`.
