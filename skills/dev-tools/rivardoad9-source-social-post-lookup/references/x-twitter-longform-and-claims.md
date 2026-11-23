# Post long-form X + validasi klaim (verified 28 Sep 2026)

Pelengkap `references/x-twitter.md` (§3 media, §5 batas long-form). Dua hal di bawah ini muncul waktu
user nempel `x.com/0xchainink/status/2103936661386318331` dan bilang **"validasi ini"**.

## 1. Long-form kepotong? Gambarnya yang menyelamatkan

Gejalanya: `.display_text_range` mis. `[0,279]`, ada `.note_tweet.{id}`, kalimat menggantung di tengah
`t.co/shortlink`. **Jangan berhenti di "teksnya kepotong"** — post seperti ini hampir selalu
melampirkan **infografis berisi daftar lengkapnya** (thread panjang → 1 gambar berisi semua kartu).

1. Ambil `.mediaDetails[].media_url_https`, unduh resolusi penuh:
   `https://pbs.twimg.com/media/<file>.jpg?name=orig` (CDN publik, tanpa auth; 619 KB–4 MB itu normal).
2. Transkrip pakai vision dengan instruksi **"baca apa adanya, jangan menyimpulkan"** — minta semua
   angka, tanggal, ticker, dan URL persis seperti tertulis.
3. Baru simpulkan. Contoh nyata: teks API cuma nampilin **2 dari 8** item ("1️⃣ $ONDO / 2️⃣ $QNT"),
   gambar yang ngasih 8 item lengkap + angka `$2T`, `1.7B`, `October 19` — dan 6 item sisanya justru
   memuat klaim yang paling perlu diverifikasi.
4. Expand `t.co` buat memastikan: `curl -s -o /dev/null -w '%{redirect_url}' https://t.co/<code>`.
   Kalau hasilnya `/status/<id>/photo/1`, itu tanda tambahan bahwa isi pentingnya memang di gambar.

Tetap sebut batasnya ke user: *"teks API kepotong, isi lengkap gw ambil dari OCR gambarnya"*.

## 2. "Validasi ini" = tiap klaim dibalikin ke sumber primer

Reputasi akun (verified/centang biru, fav tinggi) **bukan** bukti. Untuk tiap item:

- Cari **sumber primer**: rilis perusahaan/bursa/klub, PRNewswire, blog resmi proyek. Agregator cuma
  buat cek tanggal, bukan bukti utama.
- Catat **tanggal rilis vs tanggal post**. Semua 8 berita di contoh ini terbit 17–24 Sep sementara
  post-nya 26 Sep → **rangkuman, bukan sinyal awal**, dan post-nya nol angka harga/PnL.
- Tandai **bumbu**: angka yang kedengaran lebih besar dari kenyataannya (contoh: "1,7B akun bank" =
  akun yang disentuh software vendor Infosys, bukan 1,7B pengguna Chainlink; tanpa nama bank, tanpa
  timeline, tanpa komitmen fee — dan LINK turun 4,4% saat rilis), status "pending regulatory review"
  yang ditulis seolah pasti, serta "dipilih **perusahaan** X" yang tidak otomatis berarti tokennya
  dapat aliran nilai.
- Tutup dengan **kondisi harga sekarang** (%24j/%7h, gap MA20) supaya kelihatan mana yang masih di depan
  dan mana yang udah dibayar (QNT: berita 24–25 Sep di $97,95 → sekarang $270,86).

Output yang user terima: verdict per klaim + sumber + angka penentu + kesimpulan "ini sinyal atau
rangkuman". Kelanjutan berupa posisi/alokasi masuk ke skill `crypto-portfolio-advisory`
(lihat `references/kol-post-to-positions.md` di sana).
