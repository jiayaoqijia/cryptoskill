---
name: airdrop-opportunity-scan
description: Screen current crypto airdrop opportunities by real odds.
---

# Airdrop opportunity scan (saringan 3 lapis)

## Kapan dipakai

User minta "cariin airdrop potensial sekarang" / "yang lagi ramai". Jangan jawab dari list aggregator
telanjang — list itu penuh skema "sign up, trade, refer" yang digiring voting komunitas.

Termasuk lanjutannya: satu-dua kata berupa nama proyek atau dompet yang baru dia lihat di list
("suilend", "slush wallet itu apa") — itu masih sesi airdrop yang sama, bukan pertanyaan kamus. Jawab
dengan memakai saringan yang sama (status token, biaya, risiko), bukan deskripsi produk saja.

## Saringan (urutannya penting)

1. **Uang beneran di pasar prediksi.** Polymarket punya tag `token-launch`; ambil live lewat API Gamma
   (tanpa auth, jangan scrape HTML-nya):
   `https://gamma-api.polymarket.com/events?closed=false&limit=60&order=volume24hr&ascending=false&tag_slug=token-launch`
   Tiap event punya `markets[].question/outcomes/outcomePrices` (harga 0-1 = probabilitas) + `volume24hr` +
   `liquidity`. Ini ranking yang paling jujur soal "lagi ramai": volume 24 jam = duit yang naro.
   Cari juga `https://gamma-api.polymarket.com/public-search?q=airdrop` (banyak yang vol 0 = mati, buang).
2. **Konfirmasi dari tim.** Label `Confirmed` di airdrops.io (`/hot/`, `/latest/`) atau pernyataan resmi
   (CMO/founder) di artikel. Beda jauh antara "konfirmasi" dan "spekulasi".
3. **Biaya & effort farm.** Airdrops.io kasih `Difficulty` + `Cost to Farm` per halaman proyek — kutip apa
   adanya (contoh Polymarket: Hard / High). Perp DEX = fee trading, testnet = waktu, passive (bandwidth) =
   uptime.

## Sumber pendukung

- `https://cryptorank.io/drophunting` — dashboard potensial + kolom **raise/funds** (skor kualitas: $68M jauh
  lebih serius dari $2,8M) dan TwitterScore.
- Artikel "top airdrops <bulan> <tahun>" (CoinGecko, DL News, Bankless, Bitcoin Foundation) — berguna buat
  konteks tokenomics (mis. Hyperliquid 38,88% supply disimpen, LayerZero 15,3%). **Cek tanggalnya**: yang umur
  9 bulan sering nyebut proyek yang tokennya udah launch.
- CoinDesk/CoinMarketCap buat verifikasi "udah launch belum" — penting, karena dashboard ".io hot" tetap
  nampilin proyek yang dropnya udah lewat (Lighter launch 30 Des 2025).
- `https://yields.llama.fi/pools` (JSON, tanpa auth) — APY + TVL live semua pool di semua chain; filter field
  `chain` (contoh 'Sui'). Pakai buat nguji klaim APY/TVL dari dompet atau protokol sebelum nyaranin: "up to 8% APY"
  itu pool mana, TVL berapa, berapa porsi reward token vs base. APY 85-400% di CLMM hampir selalu TVL tipis +
  insentif token, bukan bunga — sebut apa adanya.

## Wajib dicek sebelum menyarankan

- **Udah TGE atau belum.** Kalau tokennya udah jalan, farming-nya udah basi — bilang terus terang.
- **Snapshot status.** Kalau snapshot udah kena, partisipasi baru nggak ada artinya.
- **Geo.** Contoh Polymarket.com nggak kebuka buat resident US (harus app Polymarket US khusus).
- **Sybil.** Proyek besar hampir semua punya anti-sybil: satu dompet dengan history wajar, jangan multi-wallet,
  wash volume biasanya dibuang eksplisit.

## Bahaya yang selalu diingatkan ke user

- Airdrop bukan gratis: gas + bridge + fee trading bisa lebih gede dari nilai drop.
- Nggak pernah kasih seed phrase; connect cuma ke domain resmi. Penipuan airdrop = jalur kerugian nomor satu.
- Verifikasi kontrak/domain sebelum user connect wallet — tawarin itu sebagai langkah default.

## Undian sosial harian (post-to-earn / draw)

Kalau syaratnya "posting tiap hari, pemenang diundi, hadiah dikirim ke wallet": itu bukan farm dan
bukan airdrop biasa — odds-nya dihitung per hari, dan yang menentukan cuma jam posting + nomor
peserta yang benar. Alurnya ada di `references/social-giveaway-verification.md`.

Tiga aturan yang paling sering bikin salah:

1. **Nomor peserta dibaca dari kontrak** (`tokenOf`/`agentOf`), bukan dari preview di situs — situs
   suka nampilin nomor demo.
2. **Jendela waktu dihitung dari status situs** ("output complete · awaiting draw"), bukan dari teks
   FAQ; FAQ bisa meleset sehari dari jadwal yang benar-benar jalan.
3. **Menang dibuktikan lewat transfer token hadiah ke wallet** (`eth_getLogs`, topic2 = wallet),
   bukan lewat daftar pemenang di halaman yang cuma me-render belasan dari ratusan baris.

Pengingat harian: cron 2x sehari yang membaca timeline akun dulu dan **senyap kalau sudah posting**.
Jangan kirim pengingat buta — user nggak mau diganggu buat hal yang sudah dia kerjakan.

## Format jawaban yang user suka

Tier: (1) paling disaranin, (2) terkonfirmasi tapi butuh modal, (3) rame di berita tapi jangka panjang,
(4) udah kelewat. Tiap item: apa itu, bukti (dengan angka odds/volume + tanggal), cara farm, risiko.
Tutup dengan aturan main biaya. Sertakan sources (skill `grounded-citations`).

## Pertanyaan satu kata ("suilend", "slush wallet itu apa", "predict.fun?")

Jawab singkat dan tetap pakai saringan, bukan ensiklopedia:

1. **Apa itu** dalam dua-tiga baris: produk utamanya, jaringannya, siapa di belakangnya, sejak kapan jalan.
2. **Status tokennya** — udah TGE atau belum, tanggalnya kalau ada, dan kalau udah jalan: harga, market cap,
   jarak dari ATH, dan volume 24 jam. Halaman protokol DefiLlama memberi semuanya dalam satu tembakan
   (TVL, fee, revenue, mcap, harga, ATH). Microcap dengan volume harian ratusan dolar wajib disebut begitu
   apa adanya: itu angka yang bikin lu nggak bisa keluar, bukan detail teknis.
3. **Verdict: target atau alat.** Kalau tokennya udah jalan, bilang lurus — "ini bukan tiket airdrop, dia
   alat"; yang masuk akal dipakai adalah produknya (liquid staking, lending) sambil menyusun aktivitas buat
   drop lain di ekosistem itu.
4. **Kejadian besar terakhir yang mengubah tesis**, dengan tanggal — akuisisi, warning regulator, program
   buyback yang ada deadline-nya. Yang paling sering kelewat: token yang secara eksplisit dikeluarkan dari
   akuisisi platformnya, artinya kesuksesan produk nggak otomatis ngalir ke token. Bilang begitu.
5. Kalau yang ditanya dompet: sebut jaringan yang didukung, bahwa kuncinya self custody, dan **install hanya
   dari domain resmi atau developer resmi di app store** — dompet adalah target phishing nomor satu, jadi
   tawarin verifikasi link/kontrak sebelum dia connect.

