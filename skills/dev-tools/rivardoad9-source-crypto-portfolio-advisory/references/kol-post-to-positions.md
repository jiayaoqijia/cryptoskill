# Dari post KOL/hype ke posisi (verified 28 Sep 2026)

Trigger: user nempel post X berisi daftar ticker ("8 Altcoin Moves This Week") lalu minta
"validasi ini" / "posisi portofolio rekomen dari lu, narasinya bakal gmn".

Aturan pertama: **jangan nilai naratifnya, nilai harga vs katalisnya.** Untuk tiap ticker tarik
`%24j`, `%7h`, `gap ke MA20`, `% dari ATH`, mcap (lihat `references/live-market-data-sources.md`
atau langsung `scripts/market_snapshot.py`), lalu klasifikasi:

| Klas | Tanda | Aksi |
|---|---|---|
| Sudah dibayar di muka | `%7h` ekstrem **ATAU** gap MA20 > +100% (contoh nyata: QNT +307,6% 7h / MA20 +187,8%; NEAR +175% 30h) | **TOLAK**, sebut angkanya |
| Katalis masih di depan | 7h belum gerak + tanggal jelas (INJ −0,8% 7h, burn + Stockdrop 30 Sep) | kandidat utama |
| Berita ada, mekanisme lemah | klaim korporat tanpa fee-share/komitmen (LINK "1,7B akun" = akun yang disentuh software Infosys, tanpa nama bank/timeline/fee; LINK malah turun 4,4% saat rilis) | TOLAK |
| Simbolik | listing derivatif/futures (UNI & BCH masuk CME 19 Okt, masih pending regulatory review) | TOLAK |
| Risiko, bukan katalis | migrasi kontrak/upgrade (TEL → 18 desimal: upgrade manual, legacy 2-desimal deprecate, exchange belum otomatis, ladang phishing) | TOLAK sebagai trade |

Dua tes tambahan yang selalu dipakai:

- **Tanggal rilis berita vs tanggal post.** Kalau semua berita 2–6 hari lebih tua dari post-nya →
  itu **rangkuman, bukan sinyal awal**, dan kalau tidak ada satu pun angka harga/PnL di dalamnya,
  itu konten engagement. Bilang apa adanya.
- **"Siapa yang nangkep fee?"** Rilis korporat ("bank X pilih vendor Y") biasanya sampai ke
  **perusahaan**, bukan ke tokennya. Token tanpa klaim (fee-share/buyback/burn/on-chain revenue)
  naik cuma karena narasi → posisinya paling rapuh pas narasi itu dikoreksi.

## Cara narasi diterjemahkan ke lapis portofolio

Dari 8 berita satu post, lapisnya cuma 4 — dan porternya begini:

1. **Tokenized equity / RWA = jalur masuk modal** (tokenisasi ~$30B, $16B masuk/12 bulan; channel
   termuda yang masih naik saat ETF & stablecoin turun) → ONDO, INJ, NEAR.
2. **Rel bank on-chain (B2B)** — nilainya ke perusahaan dulu, timeline tahunan (TCH akses bank H1 2027)
   → Quant/Chainlink. Pasar sudah membayar di muka (QNT +308% 7h) = bukan tempat masuk.
3. **Legitimasi/derivatif institusional** (CME, perp DEX) → nambah "investability", bukan revenue.
4. **Value accrual** (buyback/burn/revenue share; rekor buyback $638M sampai Agu) → pembeda yang
   paling dibayar institusi. INJ (staking→revenue + burn) & HYPE (buyback) lolos; ONDO (tanpa
   fee-share) paling lemah di sumbu ini.

Hasil yang diharapkan: verdict per klaim + sumber primer + angka penentu, lanjut ke tabel alokasi
(`SKILL.md` §Workflow 4–7) dengan **rejection list berisi angka**, seperti di
[[Portofolio Rekomendasi v2 + Narasi Q4 2026 (28 Sep 2026)]].

## Jangan lupa makro di atas narasi mikro

Post KOL nggak pernah nyebut: Fear&Greed (74 = Greed), odds Fed (65% hike Oktober), UST 10y
(5,116%, tertinggi sejak Jul 2007), settlement Treasury $202B di tanggal month-end/quarter-end,
atau trend volume DEX (`/overview/dexs` change_7d). Itu yang nentuin **timing tranche** — narasi
mikro nentuin **apa yang dipegang**, makro nentuin **kapan masuk**.
