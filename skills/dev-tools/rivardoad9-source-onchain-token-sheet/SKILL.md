---
name: onchain-token-sheet
description: "Use when reading a token on-chain sheet vs thresholds."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [onchain, gmgn, screening, lp, meteora, telegram]
    related_skills: [gmgn-token, gmgn-holder-analysis, data-chart-images]
---

# On-chain token sheet (GMGN screenshot → verdict)

User sering kirim screenshot GMGN tab **Data** (mobile) dan minta "itungin / ini gmn".
Jangan baca mata doang: tarik data live, lalu jalankan sheet 12 metrik + gate LP.

## Langkah

1. **Ambil CA.** Screenshot biasanya cuma nampilin potongan alamat. Cari:
   `gmgn-cli market search --chain sol -q <NAMA_TOKEN> --raw > /tmp/x.json`
   lalu pilih entri dengan `liquidity` terbesar & symbol cocok. Screenshot juga nampilin
   pair quote + `Current Quantity/Initial` — itu dipakai buat verifikasi pool yang bener.
2. **Jalankan checker** (angkat semua angka + verdict sekaligus):
   `python3 ~/.hermes/scripts/diag/token_sheet.py <CA>`
   Script ini manggil `gmgn-cli token info` + `token pool` + `market search` (buat tax) dan
   mencetak verdict HIJAU/KUNING/MERAH + gate LP.
3. **Kalau unit/derived number ambigu, cross-check — jangan asumsi.** Contoh nyata:
   `total_fee` GMGN tidak berlabel. Buktinya dia **SOL**, bukan USD: `total_fee/umur` ≈
   `0,25% × volume24` dalam SOL (dua token berbeda cross-check konsisten, rasionya 1,2–1,5x
   karena fee tier dinamis). Baca USD → fee/TVL 0,09% (nggak masuk akal); baca SOL → 6–11%.
4. **Laporkan** verdict + hitungan, sebut angka mana yang bikin gugur, dan pisahkan
   "kesimpulan LP" dari "kesimpulan beli" (arahnya beda, lihat bawah).

## Ambang batas

| Metrik | 🟢 | 🟡 | 🔴 |
|---|---|---|---|
| Tax beli+jual | 0% | 1–5% | >5% |
| Top 10 holder | <20% | 20–50% | >50% |
| Bundler | <5% | 5–30% | >30% |
| Phishing/entrapment | <10% | 10–30% | >30% |
| Insider/sniper/dev hold | 0% | <10% | >10% |
| Liq ÷ MC | >5% | 1–5% | <1% |
| Volume 24j ÷ Liq | 0,5–5x | 5–20x | <0,1x atau >20x |
| Net buy 24j | plus | tipis | minus terus |
| Holder | >5.000 | 1.000–5.000 | <1.000 |
| Umur pool | >14 hari | 3–14 hari | <3 hari |
| Bot degen rate | <20% | 20–50% | >50% |
| Token dibuat dev ini (`creator_created_count`) | ≤3 | ≤50 | >50 |

**Aturan keras: satu MERAH = gugur**, hijau banyak bukan penebus.

Gate LP engine (`flowmetrix-ai-agent/src/config/env.ts`): **volume/TVL ≥ 2,5x** +
**fee/TVL ≥ 6,1%/24 jam** (MIN_FEE_COST_COVERAGE 2,5 × FORCED_EXIT_SLIPPAGE_PCT 2% + gas) +
TVL **$50rb–$500rb** + tiket ≤2% dari likuiditas band. `MAX_FEE_TVL_RATIO 0,25` → >25%/24j
= TVL collapse, bukan yield.

## Pitfalls

- **`>20x turnover` itu MERAH di sheet beli, tapi HIJAU di sheet LP.** Satu metrik dua arti.
  Jangan lupa bilang ke user kalau angkanya dipakai buat LP.
- **Pool `pump_amm` sering ber-quote token aneh** (SKHY, PUMP, meme lain), bukan SOL/USDC.
  Konsekuensinya LP = long dua memecoin sekaligus; LP vs stable tidak berlaku. Selalu cek
  `quote_symbol` — dan tulis di laporan.
- **Quote token punya harga sendiri**: `quote_reserve_value / quote_reserve` = harga quote.
  Dipakai buat ukur kedalaman & apakah harga token konsisten dari dua sisi.
- **IL vs fee**: bandingkan `fee kumulatif ÷ TVL awal` lawan `|IL|` (IL = `2√r/(1+r) − 1`,
  r = kenaikan harga dari harga awal pool). Contoh: pool naik 7,8x → IL −36,5%; fee 57–97%
  TVL awal = LP awal profit; pool lain naik 8,0x → IL −37,3% tapi fee cuma 35% = **fee tidak
  nutup IL**.
- **Umur pool <3 hari** = jangan LP walau fee/TVL-nya gede; fee kemarin belum tentu fee besok.
- **Harga baru naik 3–4x dalam 6–24 jam** = masuk LP sekarang = masuk di puncak spike;
  IL paling nyakitin justru setelah pump.
- Setelah kirim laporan, user biasanya lanjut kirim token lain — sebutkan hitungan yang bisa
  dipakai ulang (mis. resolusi unit Total Fees) biar tidak diulang.
