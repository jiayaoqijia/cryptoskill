# Pola verifikasi: berita infrastruktur, domain phishing, dan koin kelewat cap

Companion `holdings-thesis-verification.md` (lima check) + `data-source-fallback-ladder.md`.
Semua kejadian di bawah **verified 6 Okt 2026** (sesi "virtual x ondo ?"); angkanya akan basi, **polanya** yang dipakai.

## 1. "Connectivity ≠ order flow" — berita infrastruktur yang bukan katalis

Kasus: **16 Sep 2026, broker-dealer Ondo (Oasis Pro Markets) jadi anggota tokenisasi pertama DTCC
Fund/SERV** — rail yang memproses >85% order reksa dana AS, 1.300+ klien, DTCC sendiri dikutip di
press release. Semua surface check lolos: nyata, bertanggal, counterparty besar, ada rilis resmi.
**Tetap bukan katalis** — dan tokennya **turun ~5% hari itu**.

Tiga spesifik yang harus ada sebelum berita rail/membership/lisensi dihitung katalis:

| Tanya | Kalau tidak ada |
|---|---|
| Produk / share class mana yang eligible? | itu konektivitas, bukan revenue |
| Counterparty mana yang benar-benar switch on? | demand-nya masih hipotesis |
| Tanggal go-live-nya kapan? | itu harapan 2027+ |

Kelas berita yang diperlakukan sama (diskon): "menjadi anggota asosiasi", "menyelesaikan perizinan",
"berencana memperluas akhir tahun ini", atau rilis yang mengulang fakta yang sudah pernah dipublikasi.
**Yang dilacak: transaksi live pertama**, bukan keanggotaannya — itu satu-satunya event bertanggal yang
berujung ke fee.

Uji cepat sebelum menulis: kalau judul berita tidak memuat produk + counterparty + tanggal,
tulis di laporan "konektivitas, bukan order flow" dan jangan naikkan bobot karena berita itu.

## 2. Fee switch / value capture — cek status, jangan terima "expected H2"

Untuk token yang tesisnya bergantung pada revenue share (ONDO contohnya): jangan berhenti di kalimat
"fee switch diharapkan H2 2026". Cari **proposal on-chain / vote / tanggal eksekusi**. Per 6 Okt 2026:
belum ada proposal, sementara H2 tinggal 2,5 bulan ⇒ perlakukan sebagai **opsi yang kemungkinan geser ke
2027**, bukan katalis dalam horizon posisi. Sumber yang bisa dipakai: `tokenomist.ai/<slug>`,
halaman governance resmi proyek (domainnya diverifikasi dulu — lihat §3), allium/datawallet-style report,
berita crypto yang menyebut tanggal.

Kalimat yang dipakai user sebagai standar: *"produknya menang, token-nya ketinggalan"* — bisnis bagus
tidak otomatis mereprice token selama tidak ada klaim arus kas.

## 3. Domain phishing yang muncul di hasil search

Cari "`<proyek> governance vote`" → hasilnya memunculkan `proposal-ondofoundation.app` yang mengaku
"Ondo Global Markets governance portal" dan meminta **connect wallet** untuk vote. Domain resmi Ondo =
`ondo.finance`; domain itu **bukan** domain resmi yang terverifikasi.

Aturan:
1. Jangan pernah merekomendasikan link connect-wallet / claim / airdrop yang datang dari hasil search.
2. Cocokkan domain ke situs resmi + handle X proyek; kalau beda → **peringatkan eksplisit di balasan
   yang sama** ("jangan connect wallet / jangan tanda tangan apa pun") dan sebut domain resminya.
3. Jangan taruh link itu di vault note sebagai referensi tanpa label peringatan.

## 4. GMGN pada market cap besar — tag-nya bukan sinyal

`gmgn-cli token holders --chain base --address <VIRTUAL> --tag smart_degen --limit 5` → **0 wallet**
(6 Okt 2026). Itu keterbatasan cakupan tag, bukan bukti tidak ada smart money. Yang tetap berguna dari
GMGN di koin besar:
- angka **likuiditas pool DEX** (VIRTUAL Base **$4,74M** vs mcap $550M ⇒ slippage nyata saat sizing),
- holder count sebagai sanity check.

Bandingkan juga `circulating_supply` GMGN vs CoinGecko: VIRTUAL 497M (GMGN, Base) vs 660M/1B (CoinGecko)
— **sebut sumbernya** saat mengutip float, jangan campur dua angka dalam satu tabel tanpa asal.

## 5. Dua aturan entry/posisi yang dipakai user

- **Puncak range 30 hari ≠ entry.** VIRTUAL: 100% dari range 30h, +49,9% dalam 60 hari, tapi masih 16%
  dari ATH ⇒ pantulan dari dasar, bukan price discovery. Ukuran satelit, dan sebut **level pullback**
  (MA50 ≈ $0,71) daripada menyarankan nambah sekarang.
- **Koin 3× di atas cap sendiri ≠ "hold".** Snapshot live: ONDO $580 = **42,3%** dari $1.373 sementara
  cap user 12%. Jawabannya ladder trim eksplisit (sekarang / di level X / paling lambat tanggal Y) +
  ke mana hasilnya pergi (BTC/cash) — bukan diskusi tesis yang seimbang.

## 6. Beta vs BTC — pakai script, jangan kira-kira

`scripts/beta_vs_btc.py <coingecko-id> …` → beta = cov(log-return koin, log-return BTC)/var(BTC) dari
seri harian 180 hari, plus corr, vol harian, MA20/MA50, posisi range 30h, dan proyeksi "BTC −30% → koin
≈ −X%". Angka 6 Okt 2026: ONDO beta 1,07 (corr 0,41) · VIRTUAL beta 1,40 (corr 0,62) — VIRTUAL lebih
"amplifier BTC" walau ATH-nya lebih jauh, dan itu yang dipakai untuk sizing, bukan % dari ATH.
