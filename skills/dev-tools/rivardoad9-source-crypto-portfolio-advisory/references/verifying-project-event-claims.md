# Verifikasi klaim "proyek X pause / token crash" dari link sosmed

Trigger: user kirim link X yang isinya bencana sebuah proyek/token ("payments paused", "$TOKEN dumps
50%", "protocol ganti model") — biasanya **user punya posisi** di token itu, jadi jawabannya harus:
klaimnya benar/tidak + apa yang berubah material + level invalidation.

## Urutan kerja (jangan dibalik)

1. **Transkrip klaim lengkap**: `api.fxtwitter.com/<user>/status/<id>` (teks + metrik), lalu
   `vision_analyze` semua media — chart resmi proyek & screenshot dashboard biasanya ada di gambar.
2. **Korroborasi ≥2 media independen** (frasa persis via `web_search`). Kalau akurat, bilang akurat;
   jangan tambah FUD.
3. **BACA HALAMAN RESMI PROYEK DULU — di situ sering ada berita yang lebih material dari klaimnya.**
   Contoh nyata (UsePaid, 29 Sep 2026): `/capital-flow` + docs menunjukkan **split fee berubah hari itu
   05:29:01.939Z dari 80% penerima / 20% burn → 65% penerima / 10% treasury / 25% burn**, ditambah
   **jendela klaim manual 14 hari** (unclaimed → treasury) dan saldo lama ditulis eksplisit
   *"possible future paths, not completed migrations"* (= tidak dijamin). Tak satu pun ada di thread.
4. **Ukur seri harga sendiri**:
   - GeckoTerminal: `api.geckoterminal.com/api/v2/networks/solana/tokens/<mint>` → ambil pool, lanjut
     `…/networks/solana/pools/<pool_addr>/ohlcv/day?limit=20`.
     **Pitfall:** id dari `/tokens/` berformat `solana_<addr>` — prefix `solana_` harus dipotong, kalau
     tidak → 404.
   - DexScreener: `api.dexscreener.com/latest/dex/tokens/<mint>` → liq, FDV, `priceChange` h1/h6/h24, volume.
   Hitung Δ dari **snapshot lama** (vault note / state watchdog) vs sekarang, plus Δ dari puncak.
5. **Cek mekanisme burn benar-benar apa.** Kalau mereka bilang "buy & burn": `getTokenSupply` via RPC
   publik untuk supply, dan cek incinerator Solana `1nc1nerator11111111111111111111111111111111`
   (`getTokenAccountsByOwner`). Supply turun sementara incinerator cuma pegang ~402 token = mereka
   pakai **instruksi SPL burn**, bukan kirim ke incinerator. Jangan klaim burn terverifikasi kalau
   cuma percaya dashboard mereka.
6. **Bandingkan angka headline dengan grafik resmi proyek sendiri.** Kasus nyata: klaim "$1,54M fee
   dalam 24 jam = 26x hari sebelumnya", sementara grafik harian mereka menulis 27 Sep $623,5k vs
   26 Sep $115,6k (= 5,4x; 26x berarti hari sebelumnya $59k). Dua angka resmi dari akun yang sama
   tidak rekonsiliasi → laporkan sebagai temuan.
7. **Frame keputusan**: runner-up skenario (p5-ish), invalidation konkret, dan mana yang rusak
   (rail distribusi) vs mana yang masih jalan (mesin fee + burn).

## Pitfall yang sudah kena

- **Dashboard itu pihak berkepentingan, bukan bukti.** Screenshot "Realized PnL $21.124 dari $1.000"
  berasal dari UI tool yang sedang dipromosikan; di screenshot yang sama `1.622 trades` tidak cocok
  dengan `913W+159L = 1.072`, dan `Open Invested $2.185` > modal yang diklaim $1.000. Selalu cek
  konsistensi internal + provenance.
- **Bedakan rail vs engine.** Pause pembayaran (pihak ketiga, mis. X Money) tidak mematikan mesin fee;
  cek feed live buyback/burn untuk memastikan bagian itu masih jalan.
- **Kuantifikasi.** Burn run-rate (~$20–45rb/hari ≈ 0,2–0,4% mcap/hari) vs penurunan −56%/hari:
  itulah jawaban yang user butuh — burn bukan penggerak harga.
- **Likuiditas = risiko exit.** Liq pool turun 52–67% dalam 2 hari sementara volume harian tetap besar
  → masukkan ke invalidation (mis. "liq pool utama < $500rb → keluar").
- Akhiri dengan **level + horison** (mis. "rail belum balik 14 hari", "mcap < $8M"), bukan pertanyaan
  "mau gw pantau?".
