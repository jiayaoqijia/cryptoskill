# Audit "udah paling optimal belum?" — tes dominasi (verified 28 Sep 2026)

Dipakai kalau user nanya: *"kasih semua tesis lu berdasarkan portofolio rekomen lu, semuanya secara
deepdive, apakah itu udh paling optimal?"* — pertanyaan ini **bukan** minta restatement rencana,
ini minta rencananya **diserang**. Kalau jawabannya "ya udah optimal", lu gagal.

## 1. Aturan main: optimal ex-ante mustahil, dominasi bisa dibuktiin

Bilang terus terang di jawaban: nggak ada alokasi yang bisa dibuktiin optimal sebelum kejadian.
Yang bisa dibuktiin cuma **dominasi** — kandidat revisi lebih baik di sumbu terukur dibanding alokasi lama.
Tiga sumbu, harus bagus **bareng** (bukan tukar-tukaran):

1. **EV** model naik.
2. **Harga di skenario bear naik** (terhadap pagar portofolio, mis. $900).
3. **Konsentrasi sleeve terbesar turun.**

Contoh nyata v3 → v4: EV +9,5% → **+9,8%** · bear −36,2% → **−34,8%** ($893 → $913) · sleeve terbesar
20% → **18%**. Tiga-tiganya naik ⇒ jujur bilang "v3 bukan optimal".

Kalau cuma dua dari tiga yang naik, itu trade-off — sebut mana yang lu beli dan mana yang lu bayar.

## 2. Uji yang wajib dijalanin (satu variabel per uji)

- **Swap tunggal cari sleeve terlemah.** Geser satu sleeve ke kandidat pengganti: "HYPE 12% → ETH"
  ⇒ EV +10,0%, bear −35,6% (dua-duanya naik) = HYPE sleeve terlemah dari yang high-profile.
  "LP 11% → ETH 6 + cash 5" ⇒ bear malah **−37,0%** = LP punya fungsi peredam → **dikecilin (11→8),
  jangan dihapus**. Pelajaran: sleeve yang EV-nya rendah bisa tetap berguna kalau variance-nya rendah.
- **Varian ekstrem buat nunjukin harga EV maksimum.** Tanpa cash ⇒ EV **+11,6%** tapi bear **−40,9%**
  ($827, nembus pagar $900). Sebut sebagai pilihan yang **sadar ditolak**, bukan direkomendasi diam-diam.
- **Ranking EV per aset dipakai buat MENOLAK.** QNT 30h **+340,6%** → EV sendiri **−10,2%**
  (beli setelah +340% = EV negatif). NEAR +185%. ZEC 30h +93,7% walau mcap $26,3 miliar → EV +4,5%.
  Angka inilah yang bikin daftar penolakan kredibel, bukan selera.
- **Float jadi kolom, bukan catatan kaki.** Temuan yang mengubah alokasi: **HYPE circ 23%**
  (FDV $86 miliar vs mcap $19,8 miliar) walau cuma −9,1% dari ATH → diturunin 12→8%.
  Nama "price discovery" dengan 77% supply belum beredar = **overhang**. Cek juga TAO 54% ·
  ONDO 49% · XPL 45% — satu baris angka ini sering mengalahkan seluruh cerita naratif.
  Alat: `scripts/market_screen.py` (+ `$FDV = harga × total_supply`).

## 3. Tesis per sleeve: isi minimum tiap blok

User minta "semua tesis" — satu blok per sleeve, tiap blok wajib punya: **angka live** · **mekanisme
value accrual** (fee share / buyback / burn / yield — atau "nggak punya", sebut terus terang) ·
**katalis bertanggal** · **risiko + syarat falsifikasi** · **verdict bobot**. Contoh format yang dipakai:

| Sleeve | Tesis inti | Mekanisme | Katalis | Risiko / falsifikasi |
|---|---|---|---|---|
| INJ 18% | −85,8% ATH, mcap $745 juta | burn auction mingguan (6,85 juta INJ dibakar) | buyback-burn + Stockdrop 30 Sep | kalah di perp DEX vs HYPE; falsifikasi: revenue turun 2 kuartal / gagal breakout <$6 |
| AAVE 6% | −77,6% ATH, 96% circ | AWW: 100% revenue → DAO + buyback otomatis (205k AAVE ≈ 1,28% supply) | Aavenomics 3.0 | borrow fee −25% dari puncak; budget buyback $50 juta→$30 juta/thn |
| ETH 10% | −46,5% dari puncak 2025, **100% circ** | staking-ETF + treasury perusahaan (bukan fee) | Glamsterdam | value capture lemah: burn 3,26 ETH/hari vs issuance ~1.700/hari = net inflasi |

Sleeve tanpa mekanisme value accrual (mis. ONDO: nggak ada fee-share) ditulis apa adanya — itu yang
menurunkan bobotnya, bukan narasinya yang salah.

## 4. Koreksi diri eksplisit (wajib kalau ada)

Audit sering nemu kesalahan **gw sendiri**. Contoh nyata 28 Sep: gw model alokasi "sekarang" dari vault
blueprint 27 Sep (BTC 35 / ONDO 35 / cash 20) padahal posisi riil user ONDO 10 / INJ 7 / TAO 3 / XPL 3 /
memes 1 / **cash 76%** → satu baris tabel + seluruh EV pembanding salah.
Buka jawaban dengan: **"asumsi gw sebelumnya salah — ini posisi riil lu"**, tampilkan angka koreksinya,
baru lanjut. User menghargai koreksi diri eksplisit jauh lebih dari rencana yang dipertahankan.
**Aturan tetapnya: pastikan komposisi live dulu sebelum ngitung EV apa pun.**

## 5. Closing yang jujur

Tutup dengan batas kepercayaan, bukan jualan: multiplier skenario = asumsi gw; yang robust cuma
**urutan EV** + temuan struktural (float, ada/nggaknya fee-share, mcap). Sebut juga apa yang bikin gw
ganti lagi: (a) burn ETH pulih pasca-Glamsterdam → ETH naik; (b) borrow revenue AAVE stabil → AAVE naik;
(c) revenue burn INJ turun 2 kuartal → INJ turun; (d) HYPE buka jadwal emisi → tinjau ulang.
