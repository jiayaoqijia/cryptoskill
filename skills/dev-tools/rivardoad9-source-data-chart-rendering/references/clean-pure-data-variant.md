# Varian "clean / pure data" + aturan sumbu (studi kasus 29 Sep 2026)

## Kapan dipakai

User bilang **"buat versi clean"**, **"pure data aja"**, atau minta label personal dihapus —
contoh asli: *"buat versi clean coba dengan modal 1000$, trus tulisan engine LP diapus aja, jadi pure data aja"*
(setelah 5 chart sebelumnya penuh narasi "engine kita"/"LIVE apa adanya").

## Aturan render ulang

1. **Jalanin ulang run-nya di parameter yang diminta** (`npm run wfo:mc -- --arms=live --capital=1000 --coverage=1.0`
   → `--dump`), bukan menskalakan angka atau memakai ulang PNG lama. Versi clean harus sekuat versi naratif.
2. **Buang semua kata yang menunjuk pelaku**: "engine kita", "LIVE apa adanya", "modal gw", "kita jalankan".
   Ganti dengan label yang menyebut variabelnya: `pengali 2,5x` / `pengali 1,0x`, `akun $1.000`, `setelan terpasang`.
3. Sisakan hanya: judul (akun · horizon · metode), subjudul berisi setelan yang **identik di kedua sisi**
   + variabel tunggal yang dibedakan, panel data, tabel metrik, dan satu paragraf catatan kaki.
4. Judul harus **berdiri sendiri** (chart ini biasanya dibagikan ke orang lain) — nomor panel ("5 · …") boleh dilepas.
5. "Clean" = netral, **bukan** menghilangkan kejujuran: caveat batas atas (look-ahead k + survivor bias) tetap
   di kaki halaman, bersama setup lengkap (dataset, ukuran posisi, gas, slippage, mode k).
6. Tetap verifikasi dengan `vision_analyze`; sekalian cek "ada nggak tulisan non-data yang ketinggalan".

## Sumbu log untuk kurva yang rentangnya satu orde

Kasus: dua kurva di akun yang sama berakhir `$6.009` vs `$598`. Di skala linear kurva rugi terlihat datar
seperti garis nol → pembaca menyimpulkan "tidak ada bedanya".

- Pakai **skala log10** dan **tulis "(skala log)" di judul sumbu** — jangan sembunyikan transformasinya.
- Tick di nilai bulat: `$400 / $600 / $1.000 / $1.500 / $2.500 / $4.000 / $6.000`; batas bawah ambil sedikit
  di bawah titik terendah kurva (mis. 400 saat minimum ~$514).
- Kanvas tetap `W = 1280` dengan area plot sampai ~950 dan kolom label di `R + 18` supaya label tidak terpotong.

## Bahan panel yang terbukti jalan (perbandingan dua setelan)

- Kurva equity (log) + garis putus-putus modal awal + label "N trade · M pool" per kurva.
- Bar **per fold out-of-sample** berpasangan (satu warna per setelan, dua batang per fold) — langsung
  menunjukkan *di mana* perbedaannya (mis. 7 dari 10 fold nol trade di satu setelan).
- Tabel metrik: trade · pool · WR · PF · net Σ · equity compounded · expectancy/trade · maxDD kurva ·
  MC maxDD p95 · MC cluster p5/p50/p95 · P(profit) i.i.d./blok/cluster.
- Bar horizontal lantai gate (mis. 5,24% vs 2,10%) kalau yang dibandingkan adalah setelan gate.
