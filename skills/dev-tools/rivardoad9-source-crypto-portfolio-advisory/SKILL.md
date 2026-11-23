---
name: crypto-portfolio-advisory
description: "Use when allocating crypto capital or vetting a holding."
triggers:
  - alokasi modal crypto
  - pantau portofolio koin
  - untung rugi porto
  - porsi koin portofolio
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [crypto, portfolio, allocation, thesis-verification, lp, risk]
    related_skills: [onchain-analytics, defi-platform-due-diligence, gmgn-token, gmgn-track, hermes-cron-automation]
---

# Crypto portfolio advisory (this user)

## When to Use

User asks any of: "main di ranah mana — spot, LP, atau trade meme", "portofolio gw gmn", "kalau lu jadi
gw", "upside maksimal", "alokasi modal $X", "coba review holdings gw", "tesis gw soal <token> gmn",
"pantes nggak" about a position, "<A> atau <B>" / "better A atau B" between two tickers, "diversifikasi atau
konsentrasi di mana", "bikin porto dari nol / rombak total, pokoknya dibikin tanpa lihat porto gw", or a holding's thesis needs
re-checking (news, unlocks, catalyst dates). Answer a concentration question with MEASURED beta and
correlation, never with prose about not putting all eggs in one basket — recipe + the interpretation
bands are in `references/theme-concentration-and-unlock-timing.md`.
Not for single-token DD → `gmgn-*` / `onchain-analytics`; not for platform scam-rating →
`defi-platform-due-diligence`.

## Communication contract (learned corrections — do not re-litigate)

- Bahasa Indonesia santai (gw/lu), but **laporan lengkap & jujur** — no hedging fog, no padding.
- **Never validate a thesis reflexively.** This user rewards the direct correction: "tesis lu setengah
  bener, dan yang salah justru bagian katalis Q4-nya" landed well. Nge-amin a weak thesis is the failure mode.
- **Never fabricate numbers or news.** If a source is missing, say so. State model assumptions explicitly
  and label them ("angka return ini asumsi gw, bukan ramalan — yang robust cuma urutannya").
- **Do not close with "mau gw buatkan?"** State the next action or the plan.
- Long analyses go to the Obsidian vault (`/home/ubuntu/obsidian-vault/`) with `[[wiki links]]`; chat
  carries the decision, the key table, and the vault file name.
- Never execute trades, LP entries, or withdrawals. Sizing and levels are the deliverable; the user
  clicks. Say plainly what is manual.
- User is a student, **not** an office worker — never frame advice around salary/office routine.
- Do not claim fictional sales/revenue numbers for their business side.

## Workflow

1. **Pull live data, never memory.** CoinGecko (price + 90d series → MA20/MA50, % of 30d range,
   vol), DefiLlama (`yields.llama.fi/pools` for staking/stable APY; protocol TVL/fees), DexScreener
   (token mcap/liquidity/pair age), GMGN CLI (smart money/KOL flow, token security), Meteora datapi for
   LP pools, `api.alternative.me/fng` for sentiment. Compute in Python and print tables — never eyeball.
   Kalau CoinGecko balas 429 (per-IP, bisa nempel berhari-hari), urutan pindah ke CoinPaprika + pola cache
   ada di `references/data-source-fallback-ladder.md` §1.
   Untuk konteks makro (VIX, UST, oil, DXY, SPY/XLF, gold, ES) pakai TradingView scanner — keyless dan tetap
   jalan saat Yahoo/Stooq/FRED memblokir: `references/live-market-data-sources.md` §8. Untuk pertanyaan
   "probabilitas besok / besok breakout nggak", hitung base rate + conditional dari klines dan pisahkan
   probabilitas arah dari probabilitas breakout: `references/next-day-probability-base-rates.md`. Kalau klaimnya
   soal "Fed injeksi likuiditas besok", verifikasi jenis operasinya dulu (reverse repo itu drain, bukan injeksi):
   `references/liquidity-injection-claim-check.md`.
2. **Vet every holding with the five checks** — detail + worked examples in
   `references/holdings-thesis-verification.md`:
   1. *Claim vs mechanism* — "backed by BlackRock/$X" is usually product-level; check whether the token
      itself has a claim on anything (fee share, buyback, burn) or is governance-only.
   2. *Catalyst with a date* — a catalyst without a date is a hope; verify current status (legislative
      catalysts die — a 49–50 cloture vote killed one mid-session). "Ada filing ETF" / "menjelang
      approval" masuk kategori ini: verifikasi filenya, label fasenya, dan pakai base rate launch —
      `references/etf-filing-catalyst-and-launch-base-rate.md` (launch alt ETF 2025: 4 dari 4 nama
      negatif 30 hari sesudahnya; re-rating-nya terjadi di fase antisipasi, bukan saat launch). File yang
      sama juga memuat cara memverifikasi klaim "arus/AUM ETF melonjak": AUM ≠ arus, YTD ≠ sekarang, dan
      baris Total Farside ≠ net flow.
   3. *Supply structure* — circulating/total, inflation rate, cliff unlocks as % of float, with dates.
   4. *Upside room* — % from ATH, and whether it is "cheap because it fell" or price discovery at ATH.
   5. *Beta* — realized daily vol, so sizing reflects what a −40% week actually does to the position.
   To rank the whole fee-token universe rather than one holding (annualized revenue ÷ mcap, buyback, next cliff), use the
   keyless DefiLlama recipe in `references/fee-token-valuation-ceiling.md`. Ask "ticker mana yang harganya miss dari
   fundamental" is the divergence cut of the same file — it needs the revenue-materiality filter, or the top of the table
   is all dust-revenue chains; reusable runner: `scripts/revenue_divergence_screen.py` (CoinPaprika + DefiLlama,
   prints yield table and the `revCh30 − ch30` gap ranking).
   Kalau user bawa sendiri beberapa ticker untuk dinilai, atau mau nambah aset baru ke buku yang sudah ada,
   rubriknya (chart vs mekanisme, siapa yang membiayai, dan cara mengakui koreksi dengan angka) ada di
   `references/adding-assets-and-conviction.md`.
3. **Rank sleeves by what the market is actually paying**, not narrative: check DEX volume trend, launch
   heat, and smart-money ticket sizes. Quiet on-chain + majors near highs = spot/LP regime, not meme
   regime, and say so instead of forcing a meme pick. Kandidat dari universe likuid (universe dari top-100 mcap,
   gate mekanis empat syarat, dan cara membaca hasil "0 lolos") ada di `references/entry-screen-liquid-majors.md`.
   Kalau yang terjadi adalah **shock satu-event** (hack exchange, withdrawal halt, kaskade likuidasi), screen-nya
   beda: ranking kekuatan relatif pakai `scripts/crash_relative_strength.py`, dan aturan entry/trim-nya di
   `references/drawdown-and-trim-decisions.md` §5.
   Kalau klaimnya berbentuk "<ticker> paling sering balik kalau kena flush" dan dia bawa sendiri daftar namanya, itu
   hipotesis yang bisa diuji, bukan selera: `scripts/post_flush_recovery.py UNI AAVE INJ` mencetak return 5/10/20 hari
   setelah hari BTC ≤ −4% (n≈40 dalam 3 tahun), return 20 hari di dalam rezim BTC 30d ≤ −10%, plus beta/korelasi/vol.
   Urutannya sering membalik yang dia percaya — sajikan tabel win-rate + median per nama, jangan cuma verdict.
4. **Model scenarios and compare portfolios.** bull/base/bear per asset with explicit probabilities →
   per-sleeve EV contribution and total. Always show the user's *current* allocation in the same table,
   and state the punchline when bear cases are similar but upside differs.
5. **Size with guardrails, then write the ladder**: tranche entries (60/20/20 style), explicit exit
   levels, and a soft floor for the whole portfolio. Risk money and core money are separate sleeves —
   never refill one from the other. Kalau arahnya justru keluar dari exchange ke self-custody/hardware
   wallet, jangan mulai dari rekomendasi device: baca saldo riil (spot + Earn + futures), tarik tabel fee
   dan minimum withdraw per jaringan dari `/sapi/v1/capital/config/getall`, lalu susun urutan redeem → test
   transfer → sisa → gas → whitelist. Resep lengkap, caveat seedless, dan lever kebiasaannya ada di
   `references/exchange-exit-and-self-custody.md`.
6. **LP sleeve screening** → `references/meteora-dlmm-lp-screening.md`. Short version: never rank pools
   by fee/TVL alone; high fee/TVL correlates with tokens mid-dump, so pair it with the token's own trend,
   holders, age, and a position-size-aware cost model.
7. **Vault note** with tables, sources, dated facts, and `## Lihat juga` links to related notes.
   Kalau user minta **laporan lengkap / PDF**, resep build-nya (Chromium print-to-pdf, halaman landscape buat chart
   dan tabel lebar, prober lebar tabel, verifikasi halaman) ada di `references/portfolio-report-pdf-build.md`.

## Pitfalls

- **Extrapolating "% from ATH" into expected return.** Cheap-because-it-dumped and price-discovery are
  opposite setups; label which one each asset is.
- **Ignoring the fixed-cost floor when capital is small.** Gas + 2% exit slippage is nearly fixed, so the
  entry threshold scales with position size ($200 → 6,1% fee/TVL; $1.000 → 5,25%).
- **Treating an unproven system as an edge.** If a strategy's ledger has not demonstrated positive
  expectancy, cap its sleeve and say the number of episodes required — out loud.
- **Recommending the loudest thing on social.** Transaction counts can look balanced while price bleeds
  60%: that is retail dip-buying into distribution, not strength. A single KOL buy with no smart-money
  confirmation is a red flag, not a signal.
- **Stale numbers presented as current.** Every quoted figure carries its date. When the user's remembered
  number differs from live data ("mcap sekarang 35M" vs live $27,2M), show both and explain the gap.
- **"Ada mekanisme buyback" ≠ "buyback-nya jalan".** Cek alokasi harian terkininya + apakah tokennya dibakar.
  SKY memangkas alokasi buyback dari 300.000 → 37.600 USDS/hari (13–14 Mar 2026) dan pembeliannya tidak membakar
  token; tesis "deflasi" jadi tinggal nama. AAVE sebaliknya: alokasi jalan sejak Apr 2025 (>205rb AAVE), permanen
  $50jt/tahun (Okt 2025), otomatis lewat Aavenomics 3.0 (Jun 2026) — rantai tanggal yang bisa diaudit.
- **Jangan kutip field perubahan DefiLlama (`change_30dover30d`, `change_7dover7d`); jumlahkan sendiri `totalDataChart`.**
  Field itu dihitung di basis yang beda dan bisa membalik tanda: LINK terbaca +20,4% dari field, sementara penjumlahan
  30 hari terakhir vs 30 hari sebelumnya = −21% → harus ralat di depan user. Jumlahkan seri harian (30 vs 30 sebelumnya,
  atau 4 pekan penuh), kutip hasil jumlahnya, dan kalau angka field sudah terlanjur masuk jawaban, ralat di pesan yang
  sama dengan kedua angka — jangan diamkan.
- **`binance_porto.py --json` itu sumber kebenaran, snapshot `.json`-nya bukan.** File state bisa ketinggalan satu
  putaran trade (masih UNI+SUI padahal buku live sudah UNI+AAVE+INJ), jadi tarik `--json` fresh tiap kali ngomong soal
  bobot. Percaya `qty`/`price`/`avg_cost` saja: `pnl_pct`/`pnl_usd` nggak konsisten dengan `avg_cost × qty` (posisi
  yang baru dibeli tampil −27% padahal harga vs avg_cost cuma −0,2%) — hitung PnL sendiri dari `avg_cost` vs `price`.
- **Nambah alt beta-tinggi nyaris nggak nurunin risiko porto.** Ukur beta tertimbang sebelum/sesudah: TAO 1,67 ·
  SUI 1,65 · INJ 1,38 · AAVE 1,51 → stress BTC −30% cuma bergerak −48,5% → −45,9%. Yang beneran nurunin cuma kas.
  Kerjanya beda: alt buat return, kas buat risiko — jangan jual yang satu sebagai yang lain.
- **Inflasi supply (% cap per tahun) adalah angka yang membunuh tesis hold.** WLD: laju unlock turun 43% (24 Jul 2026)
  tapi tetap 2,9 juta token/hari (~$1,5jt/hari ≈ 27,6% mcap/tahun, revenue nol) → tahan harga = melawan arus supply.
  HYPE: unlock bulanan ~2,7% float (≈32%/tahun) dengan float baru 22,2% → P/S 20× di mcap tapi ~90× di FDV.
- **Jangan baca "posisi di X% rentang 1 tahun" sebagai satu gate saja.** Nama dengan tesis 8/10 bisa jadi 5,5/10
  sebagai entry baru (INJ: 98% rentang, revenue 0,31%/thn) — pisahkan nilai tesis vs nilai entry di scorecard.
- **Nyaranin jual posisi yang baru dia buka.** Sebelum nyusun daftar trim, tarik timestamp `myTrades`
  per aset: yang dibeli <48 jam terakhir masuk kolom TAHAN (kecuali melanggar cap atau grade-nya paling
  lemah), dan kas bantalan diambil dari nama paling lama/oversized. Churn bikin user baca rekomendasinya
  sebagai plin-plan, bukan analisa. Resep + kalimatnya: `references/target-weights-rebalance.md` §0.
- **Setup lama yang sudah kena invalidasi wajib disebut ulang.** Kalau level batal setup sebelumnya sudah ditembus
  harga (AAVE 2 Okt: batal <$163, sekarang $161), bilang ini setup BARU di struktur lebih rendah — jangan biarkan
  user mengira trade lamanya masih jalan.
- **Kekuatan relatif di hari crash bukan sinyal beli.** Nama yang naik ~20% di minggu −5% sudah 7–12% di atas EMA20 4h;
  entry-nya limit di EMA20 dengan stop di bawah EMA50, dan R:R-nya disebut angkanya. Kalau USDT ≈ 0, rekomendasinya
  trim nama paling lemah — bukan beli baru — dan hasil jualnya jangan diputar ke laggard lain. "API exchange normal"
  juga bukan "withdrawal buka": beda rail, beda risiko. Detail: `references/drawdown-and-trim-decisions.md` §5.

## Deliverable shape that works here

Telegram: short verdict first → per-sleeve table with $ amounts → the scenario table → execution
(tranches/levels) → numbered guardrails → vault file name. Rejections are listed explicitly with the
number that disqualified them; the user reads those as evidence the screen was real.

When the ask is a *ranking* ("analisa menyeluruh" + "kasih ranking koin yang lolos kriteria"), prose is the wrong
shape: give a scorecard — one line per candidate, a 0–2 score per gate, the total beside it, tiers by total, and an
explicit rejection line for every name that failed — with "belum terverifikasi" written into any cell that could not
be checked (an unverified gate never scores as a pass, and a mis-read cliff wrongly deletes a good candidate). Gate
weights + the universe recipe: `references/fee-token-valuation-ceiling.md`.

**"Bikin porto dari nol" — no anchoring to the current book.** Treat it as a different question from
"rebalance porto gw" and say so out loud, because the two produce opposite answers: the rebalance asks what
to trim inside the book he already has, the from-scratch build asks what deserves capital at all. Deliverable:
one allocation table with $ amounts for his actual capital, a two-line thesis per sleeve (mechanism + the one
risk that kills it), and a tranche ladder. The cash weight is an OUTPUT of the screen and the regime line (how many names clear the gates),
never a taste decision — justify it with the pass count. And if a name you recommended in the earlier, narrower
context fails the clean-build screen, put it in the rejection table yourself (`UNI/LINK: both fail the
volume-arrival gate — those calls were swaps inside his own book, not top-100 picks`); this user reads that
as the proof the rebuild was actually unanchored.
