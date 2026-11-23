# Multi-panel + tabel: chart per-modal (studi kasus 29 Sep 2026)

Contoh ke-4 dari seri WFO engine FlowMetrix: user minta *"re present engine kita menggunakan modal itu"* →
satu halaman yang menjawab "kalau modalnya $280 / $700 / $1.400 hasilnya berapa", terdiri dari:

1. **3 kurva equity** (satu warna per modal, label `$X (modal $Y)` di kolom kanan luar plot).
2. **Panel bar lantai fee/TVL** per modal — bagian yang menjelaskan *kenapa* hasilnya bukan fungsi linear.
3. **Panel bar band** (k=p25/median/p75) + leave-one-pool-out.
4. **Tabel HTML** di halaman yang sama: trade · WR · PF · net · % modal · expectancy · maxDD · MC p5 · P(profit)
   + catatan kaki (dua konvensi P&L, angka per bulan, status lapangan).

Generator: `~/.hermes/scripts/diag/make_cap_chart.py` → `attachments/wfo-4-modal-nyata.png`.

## Yang bikin gagal pertama kali (dan fix-nya)

| Gejala | Sebab | Fix |
|---|---|---|
| Catatan di bawah tabel terpotong, bukan tabelnya | tinggi `<table>` + catatan kaki tidak dihitung di `H` | hitung tinggi tabel manual (`n_baris × row_px + catatan`) lalu tambahkan ke total; kalau ragu, lebihkan 90px — sisa kanvas cuma latar belakang, bukan error |
| Judul panel bertabrakan dengan label nilai batang | label ditaruh `-40px` di atas batang tertinggi | naikkan `base` (dasar batang) atau beri jarak ≥ 60px antara judul panel dan label teratas |
| Kurva modal kecil "hilang" di antara kurva besar | satu skala linear untuk semua | tetap satu skala (perbandingan modal memang tujuannya), tapi tebalkan garis + tulis nilai akhir di kanan per kurva |

## Aturan isi yang dipakai

- Kolom "net" vs "compounded" **ditulis dua-duanya** — jangan tampilkan yang paling menguntungkan saja.
- Setiap panel punya judul yang menyatakan pertanyaannya ("kenapa akun kecil dihukum", "batas atasnya selebar apa?").
- Subjudul wajib menyebut **status kejujuran**: "angka ini batas atas (k TVL dari data hari ini + universe yang
  sudah tahu pemenangnya)" dan status lapangan (wallet kosong / mode signal-only / cron paused) supaya proyeksi
  tidak dibaca sebagai posisi live.
