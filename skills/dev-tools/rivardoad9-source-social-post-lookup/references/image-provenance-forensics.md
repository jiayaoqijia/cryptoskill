# Screenshot → sumber aslinya (provenance) — verified 2026-10-04

Dipakai kalau user kirim **gambar** (screenshot chart/post) tanpa link dan tanya "ini apa?".
Alurnya: baca gambar → lacak sumbernya → tentukan aset/klaimnya → atau bilang terus terang kalau
tidak bisa ditentukan. Jangan pernah menebak ticker lalu menyajikannya sebagai fakta.

## 0. Koreksi penting untuk `references/x-twitter.md` §4/§7

Catatan lama "nitter mati, jangan buang waktu" **tidak akurat** per 2026-10-04. Host nitter sering
ganti; dua yang jalan hari itu:

- `https://nitter.jaydenha.uk` — RSS, HTML status, dan **unduh media** semua jalan
- `https://nitter.meowing.monster` — RSS jalan
- `https://nitter.kareem.one` — balas HTML shell (tidak berguna)

Host alternatif lain biasanya lebih cepat mati. Tetap coba route §1 (syndication JSON,
`cdn.syndication.twimg.com/tweet-result?id=<id>`) untuk isi satu tweet, karena itu paling murah;
nitter dipakai kalau butuh **timeline satu handle**, **thread/reply**, atau **gambar**.

## 1. Lacak gambar → post aslinya

```bash
# timeline satu handle (termasuk RT, judulnya berawalan "RT by @X:")
curl -s -A "Mozilla/5.0" "https://nitter.jaydenha.uk/<handle>/rss"    # <item>…</item>
# halaman status (untuk baca thread + reply + cari media)
curl -s -A "Mozilla/5.0" "https://nitter.jaydenha.uk/i/status/<ID>" -o /tmp/t.html
# unduh medianya (CDN nitter, tanpa auth)
curl -s -A "Mozilla/5.0" -o /tmp/m.jpg "https://nitter.jaydenha.uk/pic/media%2F<FILE>.jpg"
```

Lalu **bandingkan gambar**: label/karakter khas di gambar user harus sama persis dengan media yang
diunduh (di sesi ini, label `1,8742 (765,98%) 18.742` + sumbu `2025…Jul 2027` = identik).
Kalau beda → bukan post itu, lanjut cari.

### Jebakan: URL `/<handle>/status/<id>` TIDAK membuktikan handle itu penulisnya

RT tampil seolah-olah milik si peng-RT (nitter RSS: `RT by @X: …`; `<title>` halaman juga bisa
menampilkan handle yang dibuka). **Penulis aslinya ada di canonical link:**

```html
<link rel="alternate" href="https://x.com/<PENULIS_ASLI>/status/<id>" title="View on X" />
```

Nyata di sesi ini: `/DombaEth27/status/2106412785207005471` → canonical `x.com/LordOfIndra/status/…`
= penulis aslinya `@LordOfIndra`, Domba cuma meng-RT. Salah atribusi = salah lapor.

## 2. Baca gambar dengan crop + zoom, bukan sekali lihat

`vision_analyze` region dipakai berlapis sampai yakin:

1. Full image → orientasi (mana chart, mana teks).
2. Crop per area penting, lalu perbesar 3–4x (PIL `resize(..., Image.LANCZOS)`) sebelum dikirim:
   - kiri-atas chart (biasanya nama simbol/ticker + timeframe)
   - sumbu kanan (skala harga)
   - sisi label/tooltip angka
3. Kamera hp tanpa sengaja memotong badge simbol → tersisa cuma sisa karakter (mis. `⌄ 6`).
   Kalau sumbu harga **dan** nama simbol dua-duanya kosong, ITU TEMUAN, bukan alasan menebak:
   laporkan "ticker tidak ada di gambar".

## 3. Angka label chart = cara menguji hipotesis, bukan hiasan

Label tool TradingView formatnya `entry (pct) target`. Uji konsistensinya:

- `target / entry − 1` harus ≈ `pct`. Contoh sesi ini: `18.742 / 1,8742 = 10,00x` (+900%),
  tapi label menulis `765,98%` → berarti titik ukurnya **bukan** entry itu.
- Kalau pct dipakai: `anchor = target / (1 + pct)`. Di sesi ini `18.742 / 8,6598 = 2,1643` —
  itu titik ukur sebenarnya (kemungkinan garis support/low kedua).
- Rasio bulat (10,00x) = proyeksi yang di-set dari level support, **bukan** harga sekarang.

Konsekuensinya: "harga sekarang" tidak boleh dibaca dari label; jangan buat klaim level harga
berdasarkan itu.

## 4. Kalau asetnya tidak ketentuan: bilang, lalu jelaskan cara mengeceknya

Yang boleh diklaim hanya yang terverifikasi. Urutan check yang dipakai:

1. Harga kandidat dari konteks akun (di sesi ini akunnya posting `$ZRO`/`$NEAR`/`$WLD` ±1 jam dari
   tweet chart) — cek harga live-nya.
2. Filter koin by harga di rentang label (`/api/v3/ticker/price` untuk Binance; CoinGecko
   `/coins/markets` untuk ATH & MC, termasuk kolom `ath`).
3. Filter by ATH ≈ target (target sering dipasang di ATH lama).
4. Forensik waktu: range klines 1 jam pada jam posting vs level label.

Kalau semua nggak cocok → tulis "tidak bisa dipastikan" + kandidat terdekat + alasannya.

## 5. Cek motif sebelum menyimpulkan (penting untuk akun "alpha")

Post chart tanpa nama aset + reply berisi "CARA JOIN BANG TUTOR…", "ini cara sub yah", atau
"akan saya share di sub" = **umpan langganan berbayar**. Sinyal sosial pendukung: reply yang isinya
bertanya "Apa itu bli?" (artinya penontonnya sendiri tidak tahu asetnya).

Output yang benar untuk user: sumbernya siapa, chart-nya bilang apa (angka), apa yang **tidak**
bisa dipastikan, plus peringatan kalau itu jualan sub — bukan tebakan ticker.
