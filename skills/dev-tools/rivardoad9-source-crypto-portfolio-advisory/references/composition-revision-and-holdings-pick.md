# Revisi komposisi + protokol "pilih A atau B" (8 Okt 2026)

Dua hal yang muncul bareng di satu sesi dan berulang tiap kali user ngobrol komposisi:
(1) dia **merevisi target bobotnya sendiri** di tengah jalan, (2) dia minta **dipilihin satu**
dari dua koin. Dua-duanya keputusan uang → jawabannya harus angka, bukan opini.

## 1. Revisi target: jangan dilawan, tapi jangan di-amin juga

Kasus nyata: pagi dia nulis sendiri `ETH 40% · SOL 20% · TAO 20% · ONDO 20%`, siang dia revisi jadi
*"komposisi gw keknya mau Tao, Sui, Sol aja"*. Yang benar: **verifikasi komposisi barunya**, bukan
negosiasi ulang keputusan yang udah dia ambil. Urutan langkahnya:

1. **Kuantifikasi delta risiko buku**, bukan per koin: beta buku (bobot × beta, kas = beta 0),
   HHI = Σ bobot² → nama efektif = 1/HHI, lalu terjemahkan ke uang: *"kalau BTC -20%, sleeve ini -28%
   (versi sekarang -18%)"*. Pakai `scripts/book_risk_composition.py --live SOL=40 SUI=30 TAO=30`.
2. **Sebut fakta struktural yang dia perlu tau, satu kali** — bukan buat nolak, bilang eksplisit
   *"bukan buat nolak, cuma biar nggak kaget"*:
   - 0% BTC/kas = **nggak ada bantalan**; pas flush korelasi alt → 1 dan yang beta 1,5+ turun paling dalam.
   - **Nama paling tipis likuiditasnya** (quoteVolume 24 jam), karena itu yang paling gede slippage-nya
     buat porsi riil. Nyata: TAO $42,5M vs SUI $82M vs SOL $234M.
   - **Kalau namanya baru** (belum pernah dipantau): cek jadwal unlock dulu. SUI aman — 31 Okt cuma
     21,73M SUI (±$2,4M, 0,05% float), bulanan kecil, nggak ada cliff; kontras ONDO cliff Jan-2027.
   - **Leader yang udah lari tapi lagi istirahat.** Nyata: SUI 30h +39,9% (alpha +33,8pp), SOL +12,5%
     (+6,4pp), TAO +12,4% (+6,3pp), tapi 7h tiga-tiganya **negatif**. Framingnya: *"lu beli pemimpin
     yang lagi istirahat, bukan yang murah"* — bukan warning, cuma kasih tau posisi siklusnya.
3. **Tawarin SATU varian yang lebih rapi, dengan angka** — bukan ceramah. Nyata: `SOL 35 / SUI 25 /
   TAO 25 / kas 15%` → beta 1,41 → 1,20, dan kas-nya jadi amunisi beli pas flush. Satu kalimat:
   *"tinggal bilang, gw ganti angkanya."*
4. **SINKRONKAN script pengingat.** Ini langkah yang paling gampang kelupaan: kartu cron yang udah
   terjadwal masih ngirim komposisi LAMA (`rebalance_plan.py` masih ETH40/SOL20/TAO20/ONDO20).
   Patch `TARGET`, `KELUAR`, docstring (kasih tanggal + kata "revisi"), baris urutan/toleransi, dan
   daftar `TRANCHE`, lalu **jalankan script-nya** dan tempel kartunya sebagai konfirmasi.
5. **Aset yang keluar karena cap pribadi user, sebut alasannya sekali.** Nyata: ONDO 20,8% masih
   1,7× cap 12% miliknya → ikut keluar semua, dan itu sekaligus beresin pelanggaran cap-nya.

### Pitfall nyata dari step 4

Guard "kas kurang → rapikan porsi beli" di script kepicu sama **selisih $0,01** (float noise):
`kas < -0.01`. Akibatnya kartu ngeluarin note *"kas cuma $1.011 (kurang $0)"* yang bikin panik.
Ambangnya harus material: **`kas < -1.0`**. Aturan umum: tiap guard numerik di kartu uang pakai
ambang minimal $1 (atau 0,1% total), jangan 1 sen.

## 2. "pilih A atau B" → jawab SATU nama, jangan dua-duanya

Dia nanya *"pilih wld atau virtual"*. Yang dia mau: **putusan + alasan berurutan**, bukan analisis
bolak-balik. Bentuk yang landed:

1. **Verdict di baris pertama** ("Pilih WLD.").
2. **Faktor konkret, diurut dari yang paling praktis** (bukan paling intelektual):
   likuiditas 24 jam (WLD $40,9M vs VIRTUAL $9,7M = 4,2× — paling gampang kena slippage waktu keluar) →
   struktur daily vs EMA20/EMA50 → **alpha 7 hari vs BTC** (WLD -3,44% / a7 -3,0pp vs VIRTUAL -4,63% / -4,2pp) →
   jejak whale ($13,5M / 7 wallet vs $0,8M / 1 wallet).
3. **Akui kalau ini bukan pilihan bagus-vs-jelek**: *"skor monitor WLD 58 vs VIRTUAL 57 — praktis seri,
   dan dua-duanya di-flag KURANGI. Jadi ini jelek vs jelek, satu lebih likuid."* Ngakuin itu bikin
   putusannya kredibel; nyembunyiin bikin dia ngerasa dijualin.
4. **Kasih tie-break buat pertanyaan yang nggak dia tanyain**: *"kalau cuma jual satu dulu → jual
   VIRTUAL duluan"* (relative strength paling lemah + likuiditas paling tipis = paling mahal kalau
   dipaksa keluar pas market jelek). Ini yang sering dia pakai beneran.
5. **Kalau dia tetap mau nyimpen satu**: dananya dari **nama yang melanggar cap/tesis** (ONDO 20% → 12%),
   bukan dari core. Dan ingetin narasinya numpuk: WLD/VIRTUAL dua-duanya AI-Compute, sama kayak TAO.

Pitfall: jangan jawab "tergantung selera risiko lu" atau nyodorin dua-duanya dengan bobot setengah-setengah.
Dia nanya pilihan karena mau dipilihin.
