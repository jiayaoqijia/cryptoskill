# Chart perbandingan harga / token (resep siap pakai)

Dipakai 2 Okt 2026 untuk ILV vs IMX (chart "struktur" + "peta level rencana"). Generator lengkap:
`~/.hermes/scripts/diag/make_ilv_imx_chart.py`; hasil: `~/obsidian-vault/attachments/ilv-imx-*.png`.

Semua angka dari data nyata: **klines Binance keyless** (`/api/v3/klines?symbol=ILVUSDT&interval=1d&limit=365`),
di-cache ke `/tmp/gc/<SYMBOL>.json` dulu supaya render ulang tidak memanggil API lagi.

## 1. Tick sumbu harus magnitude-aware (bug yang bikin sumbu cuma 1 tick)

`while (ymax-ymin)/step > 12: step *= 2` dengan `step = 1.0` **gagal untuk aset di bawah $1**:
rentang $0,085–$0,212 dibagi step 1,0 sudah < 12 → loop tidak jalan → **cuma satu garis tick**
($0,185) dan skala tak terbaca. Pakai langkah yang diturunkan dari orde besar rentang:

```python
def nice_step(lo, hi, max_ticks=8):
    span = max(hi - lo, 1e-12)
    raw = span / max_ticks
    base = 10.0 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if base * m >= raw:
            return base * m
    return base * 10
```

Hasil: ILV (span 3,35) → step 0,5 (7 tick); IMX (span 0,127) → step 0,02 (6 tick);
panel index 76–137 → step 20 (80/100/120 — angka bulat, enak dibaca).

## 2. Label boleh di luar plot, tapi harus di-resolve anti-tumpuk

Kolom label kanan **wajib** lewat resolver, bukan `y(value)` langsung — dua level yang berdekatan
(0,1906 vs 0,2023, atau 3,60 vs 3,75) akan saling menimpa dan hasilnya tak terbaca:

```python
def resolve(rows, min_gap=18):        # rows: (y, teks, warna, x, anchor, size, weight)
    out, prev = [], None
    for y, *rest in sorted(rows, key=lambda r: r[0]):
        yy = y if prev is None or y - prev >= min_gap else prev + min_gap
        out.append((yy, *rest)); prev = yy
    return out
```

## 3. Garis horizontal panjang = teks harus dipotong sendiri (clip horizontal)

Catatan/legenda satu baris yang mulai di kolom kanan (mis. `x = 765`, font 14 ≈ 7 px/karakter)
**terpotong tepi kanvas** kalau > ~62 karakter: `1360 - 765 = 595 px`. Baris pertama catatan ini
kejadian nyata terpotong di "(34,5 juta vs 163,1|". Aturan: pecah jadi baris ≤ 60 karakter, atau
hitung `x + 7*len(teks) <= W - 30` sebelum menulis. Naikkan `svg_h` ~23 px per baris tambahan.

## 4. Pita level lebih kebaca daripada garis tunggal

Zona entry/trim = `<rect>` setinggi level + dua garis putus-putus di tepinya, `opacity="0.15"`:
pita hijau 3,90–4,05 (entry), pita kuning 5,00–5,21 (target trim), garis merah putus-putus 3,60
(invalidasi). Di sisi log (peta level) label pita ditaruh di tengah pita, label garis di **atas**
garisnya — dan tetap lewat resolver no. 2.

## 5. Peta level skala log (entry–invalidasi–target dalam satu gambar)

Rentang 2,5 → 16 di skala linear menekan semua level penting jadi tumpukan di dasar; skala log
menyebarnya. Jarak tiap level ditulis sebagai % dari harga terakhir di kolom kanan
(`v/cur*100-100`), plus garis harga sekarang sebagai acuan 0%.

## 6. Panel performa relatif = rebased ke 100

Dua aset di-reset ke 100 pada titik awal (`ck[i]/ck[-base]`): pembanding yang jujur, dan sering
**membantah** narasi "yang ini lebih kuat". Kejadian nyata: 90 hari ILV +30% vs IMX +29% (seri),
sementara 30 hari terakhir IMX malah menang (+45% vs +36%) — itu ditulis apa adanya di gambar
(`fill=AMBER`) supaya chart tidak jadi alat pembenaran. Selalu tambahkan baris "jujur:" seperti ini
kalau angka tidak sepenuhnya mendukung pilihan yang direkomendasikan.

## 7. Gaya angka Indonesia

Pemisah desimal **koma** di seluruh gambar (label, tick, persen): helper
`num(v, d) = f"{v:,.{d}f}".replace(",", "@").replace(".", ",").replace("@", ".")`. Campur titik dan
koma dalam satu gambar = cacat yang langsung ditangkap verifikasi vision.

## 8. Legenda per panel, warna harus konsisten dengan garisnya

Tulis nama + warna di dalam SVG (`harga harian` / `MA30 (oranye)` / `MA90 (ungu)`), jangan andalkan
subjudul. Label level MA berwarna lain dari garisnya bikin verifikasi vision salah baca — kalau ada
dua elemen berwarna sama (mis. MA30 dan pita target), ganti warna atau jelaskan namanya.
