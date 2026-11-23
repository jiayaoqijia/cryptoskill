---
name: crypto-narrative-scan
description: Use when asked which crypto narrative is hottest now.
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [crypto, narrative, memecoin, research, gmgn, multichain]
    related_skills: [gmgn-market, gmgn-track, onchain-analytics, lowcap-priority-alerts, crypto-portfolio-advisory]
---

# Crypto narrative scan (theme-first, cross-chain)

## When to Use

Load when the user asks a **theme-level** question rather than a single-token lookup:

- "cari token dengan narasi terseksi sekarang + reasoning", "deep search", "apa yang lagi panas"
- "worth it masuk ga?" about a **meta/theme** (not one address)
- "narasi mana yang lebih seksi, A atau B?"
- "kenapa sektor X naik / meta ini masih hidup ga?"

NOT for: DD of one token address (`gmgn-token`, `gmgn-contract-dd`), wallet analysis
(`gmgn-wallet-analysis`), or filling the lowcap alert lane (`lowcap-priority-alerts`).

**Core idea:** money/attention data (GMGN) tells you *where*, never *what the story is*.
Narrative identity comes from outside sources (launchpad APIs, token metadata, docs, news).
Then confirm the theme across chains and finish with a ranked verdict + falsifiable plan.

## Step 1 — Attention (what people are searching)

```bash
gmgn-cli market hot-searches --chain sol --chain bsc --chain base --chain eth --chain robinhood \
  --interval 24h --limit 50 --raw > /tmp/hs.json
```

Ranked by `visiting_count` (search heat). **Response `data` is an array of per-chain blocks**
(`[{chain, tokens[]}, …]`) — iterate blocks, not a dict. A ticker repeating at many market caps
(e.g. `SI` at $50M and at $86k) means the symbol is being spammed; always keep the address.

## Step 2 — Money flow (where the money and smart wallets are)

```bash
# where the money is
gmgn-cli market trending --chain sol --interval 24h --order-by volume --limit 40 --raw
# where smart wallets are (1h window)
gmgn-cli market trending --chain sol --interval 1h --order-by smart_degen_count --limit 40 --raw
# what is moving right now — valid order-by names: change1m/change5m/change1h (NOT "change")
gmgn-cli market trending --chain sol --interval 1h --order-by change1h --direction desc \
  --min-volume 200000 --min-marketcap 1000000 --limit 20 --raw
# smart-money (type 12) + KOL (type 20) buys in one request
gmgn-cli market signal --chain sol --groups '[{"signal_type":[12]},{"signal_type":[20]}]' --raw
```

Repeat the trending sweep per chain (`sol`, `bsc`, `base`, `robinhood`). Interpret honestly:
a signal feed full of $2k–$80k mints with 1–2 hits each = **micro-cap churn, no dominant
accumulator** — report that as the finding instead of manufacturing conviction.
Sleep 3–6 s between GMGN calls (see Pitfalls).

## Step 3 — Narrative identity (the step that actually answers the question)

| Source | What it gives |
|---|---|
| Launchpad **public API** (keyless) | what a coin is *paired against*, reward mechanics, graduation |
| `gmgn-cli token info --chain X --address 0x… --raw` | `launchpad`, `link.website`, `twitter_username`, `dev.creator_token_status`, `wallet_tags_stat`, `top_entrapment_trader_percentage`, `bot_degen_rate` |
| Chain explorer / aggregator | chain-wide theme totals (e.g. all tokenized stocks on a chain) |
| `web_search` + `web_extract` | mechanism, value accrual, **controversies**, catalysts |
| `web_search` for "<platform> <token>" | CMC "what is X", Bitquery-style investigations, news explainers |

**The quote/pair asset is the narrative.** A memecoin paired against `NVDAx` (tokenized NVIDIA) is
"stock exposure with meme risk"; a platform token with 60% of revenue going to buyback+burn is
"the equity claim on the meta". Read the pair/reward config before writing a single line of verdict.

Concrete StonkFun example (Solana pair-paired launchpad): see
`references/narrative-scan-multichain.md` for exact endpoints and field names.

## Step 4 — Cross-chain confirmation

Same theme topping Solana **and** Robinhood Chain **and** BSC = a genuine meta; a single-chain spike
is usually just one launchpad's feature. Also name the copycat wave: when a competitor clones the
mechanic (pump.fun enabling stock pairs; BSC `flap_stocks`/`geniusfun` variants), that is validation
**and** commoditization — i.e. mid-cycle, neither early nor over.

## Step 5 — Ranked verdict (report shape this user expects)

1. **Verdict in the first line** — the narrative, and yes/no on entering.
2. **Evidence** with numbers: protocol/chain-wide totals (volume, holders, TVL).
3. **Ranked 1–3 tokens**, each with: address, MC, price, 24h %, volume, holders, smart/KOL counts,
   top-10 %, bot/entrapment %, age, and *what its specific claim is*. Add "already +X% from low /
   −Y% from ATH" so timing is explicit.
4. **Reasoning** — why the narrative has money behind it: real value accrual? distribution?
   external catalyst? **Say plainly when there is none** (pure attention tokens).
5. **Risks section is mandatory**: tax drag, bot/entrapment %, commoditization, and any platform
   controversy found in step 3.
6. **Entry plan labelled as scenario**: concrete entry zone, invalidation level, target — plus what
   would confirm/kill the thesis. Never present it as advice.
7. **Disclaimer**: "bacaan rule-based, bukan saran investasi."
8. **No closing question** ("mau gw buatkan?") — state what you will watch next instead.
9. Save the full write-up (numbers + addresses + sources) as a dated note in the Obsidian vault
   (`~/obsidian-vault/… (DD Mon YYYY).md`) and name the filename in the reply.

## Step 4c — Scout level-TICKER di dalam tema ("ancang-ancang" vs "ketinggalan")

Pertanyaan Zemiz 14 Okt 2026: *tema udah kemasukan volume — ticker mana di tema itu yang
BELUM kemasukan volume / masih ancang-ancang?* Hipotesisnya masuk akal, **tapi salah** — dan
caranya salah itu yang bikin sinyalnya kepakai:

Skrip: `~/.hermes/scripts/narrative_laggard_scout.py` (`study` / `grid` / `scan`; `scan` sudah
dicolok ke deep dive sebagai blok [1d]). Uji 240 hari, 13.366 observasi anggota (likuiditas
≥ $1,5jt/hari), dibanding grup yang sama di tema DINGIN sebagai kontrol:

| sinyal level-ticker | n (tema panas) | f3 | f7 | a3 | kontrol a3 | delta |
|---|---|---|---|---|---|---|
| L1 laggard: vol <1x + harga tertinggal | 307 | −1,1% | **−3,2%** | −0,4% | +0,2% | −0,5% |
| Q1 vol mulai 1,0–1,5x + harga diam | 321 | +0,9% | +0,6% | +0,8% | −0,3% | +1,2% |
| **Q2 vol masuk 1,5–3x + harga diam** | 299 | **+2,1%** | +0,6% | **+2,1%** | −1,2% | **+3,3%** |
| Q3 vol >3x + harga diam | 97 | −1,9% | −4,1% | −1,7% | −1,8% | +0,2% |
| K2 coil \|r7\|≤3% + vol ≥1,2x | 78 | +2,6% | +2,1% | +2,3% | −0,7% | +2,9% |

Aturan:
1. **Yang BELUM kemasukan volume BUKAN kandidat.** Di tema panas dia underperform (f7 −3,2%)
tapi di tema dingin malah positif — jadi bukan mean-reversion yang bisa dipanen: narasinya yang
membuat dia ketinggalan. Delta negatif = sinyal ini memburuk justru karena narasinya.
2. **Yang jalan: volume ticker masuk 1,5–2,5x tapi harga masih diam** (analog B2 level ticker).
Kurva vr: 1,0–1,3x a3 +0,6% · 1,3–1,5x +1,2% · **1,5–2,0x +2,7% · 2,0–2,5x +2,4%** · 2,5–3,0x −0,8%
· >4x −2,6%. **Batas atas wajib** — di atas 2,5x sinyalnya balik negatif.
3. Hit 3 hari 52% vs kontrol 41%; P(f3≥3%) 37% vs 26%; 65% masih ≤+2% besok → ada lead time.
4. **Edgenya kanan-ekor, bukan grind.** Belah dua periode: paruh lama a3 +1,0% (median f3 −0,5%),
paruh terbaru a3 +3,2% (median +1,0%). Rata-rata ditarik outlier → ukur pakai median + hit-rate juga.
5. Penyumbang Q2 tersebar (L1 60, DeFi 56, AI 44, Meme 33, L2 28, Privacy 26) → bukan artefak satu tema.

## Step 4b — Rotasi AWAL (prepare), jangan cuma ranking 24 jam

Ranking rata-rata 24 jam per tema (bagian [1b] `deep_dive_daily.py`) **cuma bisa bunyi SETELAH
flow masuk**. Bukti: L2/Scale dilaporkan 4 Okt 2026 saat bucket sudah +11,4% 24 jam (STRK +25%,
ZRO +14%) — seluruh pergerakan hari-1 hilang, user gak bisa prepare. Kritik user: "kenapa ga call
L2 dari kemarin, sebelum flownya masuk".

Skrip: `~/.hermes/scripts/narrative_rotation_early.py` (cron 2 jam: `narr_rotation_cron.sh`,
`no_agent`, senyap kalau gak ada perubahan). Bucket tema diimpor dari `THEMES` di
`deep_dive_daily.py` — **jangan bikin daftar tema kedua**. Cache: `narr_hist_cache.json` (12 jam),
`narr_hist_4h.json` (30 menit).

| command | isi |
|---|---|
| `study` | backtest alpha 7d + lead-time + post-mortem 21 hari per tema |
| `grid` | uji ulang semua kandidat sinyal (jalankan kalau ngubah ambang) |
| `scan` | status harian: PREPARE / konfirmasi / udah jalan / telat (dipakai deep_dive [1c]) |
| `intraday` | deteksi HARI-1 dari bar 4 jam |
| `all` | scan + intraday (yang dipakai cron) |

**Hasil uji 240 hari, 10 tema, ~2.000 tema-hari** (base rate P(tema r1 besok ≥ +3%) = 15,5%):

| sinyal | n | P(r1 besok≥3%) | lift | alpha 1d | alpha 3d | alpha 7d |
|---|---|---|---|---|---|---|
| B quiet_acc (vol3/30≥1,2 · r1≤2% · breadth≥70%) | 117 | 29,9% | 1,93x | +0,75% | −0,06% | — |
| B2 quiet_cap (vol dibatasi 1,2–2,2x) | 99 | 28,3% | 1,82x | +0,59% | +0,22% | — |
| C coil (\|r7\|≤5% · vol≥1,3x · breadth≥60%) | 45 | 26,7% | 1,72x | +0,46% | +1,95% | — |
| C2 coil_cap (vol 1,3–2,5x) | 43 | 27,9% | 1,80x | +0,47% | +1,92% | — |
| G blowoff_lama (= detektor LAMA, r1≥+5%) | 127 | 32,3% | 2,08x | +0,46% | +1,10% | **−0,20%** |
| H alpha_turn (alpha3d baru balik positif) | 114 | 24,6% | 1,58x | +0,59% | +1,05% | — |
| **A momentum3d (alpha3d≥+4%)** | 266 | 19,9% | 1,29x | +0,01% | **−0,95%** | **−2,20%** |
| F breadth_thrust (breadth≥90% + harga tenang) | 95 | 11,6% | 0,75x | +0,21% | −0,72% | — |
| E leg2 (leg kedua abis koreksi) | 4 | 0% | 0,00x | −1,30% | −2,37% | — |

Aturan pakai:
1. **PREPARE = B2 atau C2** (volume masuk dulu, harga belum) — ini yang dikasih ke user lebih awal.
2. **H** = konfirmasi awal (lift 1,58x).
3. **G** = udah jalan: follow-through cuma 1–3 hari (alpha 3d +1,10%), habis di hari ke-7 (−0,20%).
   Jangan baru masuk setelah tema tampil di ranking 24 jam.
4. **A (ngejar momentum 3d) alpha 7d NEGATIF (−2,20%) → dilarang jadi alasan beli.** Ini persis
   kesalahan yang dikritik user.
5. **Volume ≥3x + r7 ≥ +8% = CLIMAX (euforia akhir), bukan prepare.** Kasus Gaming 4 Okt: vol 3,70x,
   harga flat → label TELAT, bukan PREPARE. Batas ATAS volume wajib ada, kalau tidak
   "quiet accumulation" bakal nyala di puncak distribusi.
6. Sinyal D washout (n=12) & F/E dinyatakan **tidak dipakai** karena sampel kecil / lebih buruk dari base.

**Post-mortem jujur L2 (3–4 Okt 2026):** pop 3 Okt (+7,2%) **tidak ada jejak** di data harian 1–2 hari
sebelumnya (r3 −0,3%/−0,4%, vol3/30 0,92–0,93x = di bawah rata-rata, breadth 44%). Pop itu
news-driven (STRK v0.14.4 mainnet 5 Okt + strkBTC 2 Okt), bukan akumulasi yang terbaca dari
harga/volume sektor. Yang benar-benar bisa dilakukan: (a) deteksi intraday hari-1, (b) lane berita
untuk katalis bertanggal. **Jangan pernah mengklaim bisa memprediksi rotasi 3 hari sebelumnya dari
data sektor** — kalau ada yang tanya kenapa telat, jawab dengan angka ini, bukan alasan.

## Pitfalls

1. **Attention ≠ narrative.** Ranking lists alone produce "SI is #1" with no idea what SI *is*.
   Never publish a pick without resolving the pair asset / metadata / docs.
2. **Volume discrepancies are normal — report both.** Platform-reported 24h volume (single venue)
   vs GMGN aggregate (all venues/routers) can differ ~3× (e.g. $18.5M vs $56.9M). Say which is which.
3. **Include the lottery, labelled as lottery.** +73,988%/1h, +830× tokens are gambling, not a
   narrative; name them explicitly as excluded from picks so the user knows they were seen.
4. **State chain/bridge friction.** If the play needs a bridge or sits outside the automated
   (Solana) engine, say the automated guard cannot monitor or stop it.
5. **Reward/tax mechanics change the math** — 1–3% transfer tax per transaction is a drag on any
   trading plan; check `transferFee.bps` before framing a scalp.
6. **Commoditization risk**: a mechanic every platform now has is no longer an edge — check whether
   competitors cloned it inside the last few weeks.
7. **`gmgn-cli` rate limit**: sleep 3–6 s between calls; the failure signature is **exit 0 with 0
   bytes on stdout** and the real error on stderr; on `RATE_LIMIT_BANNED` stop and wait the announced
   reset (retrying extends the ban). Batch with `sleep` inside one script rather than many short calls.
8. **Kline `time` is milliseconds** — sort by `time` and trust the sorted order; hand-rolled
   `strftime` labels can look non-monotonic and mislead you about candle spacing.
9. **`market_cap` is missing from `token info`** — derive `price × supply` (prices/fields per
   `gmgn-market`, which is the authoritative CLI reference).
10. **Baris terakhir `klines` = bar yang SEDANG JALAN — jangan dipakai untuk metrik harian.**
   Binance mengembalikan bar hari ini yang baru berumur nol–dua jam sebagai elemen terakhir.
   Kalau bar itu ikut dihitung, rata-rata volume 3 hari & 30 hari ketekan → sinyal PREPARE
   hampir gak pernah nyala. Bukti 14 Okt 2026: cron rotasi (tiap 2 jam, 07:00/09:00 WIB =
   00:00/02:00 UTC) selalu kebetulan jalan tepat di awal hari UTC; L2/Scale terbaca vol3/30
   1,50x lalu jatuh ke 1,05x cuma karena hari UTC ganti, padahal bar yang udah tutup = 1,66x
   dengan breadth 78% (bukan 33%). Median volratio seluruh ledger `narr_rotation_snips.jsonl`
   0,665 dan cuma 12% baris ≥1,2 — angka yang gak mungkin kalau bar-nya sehat. Pakai
   `last_closed_index(ts)` (wajib tutup untuk bar harian; `min_frac=0,5` untuk bar 4 jam
   intraday biar deteksi HARI-1 gak mundur satu bar). Cek cepat: volume bar terakhir vs
   sebelumnya — kalau beda >50x, itu bar partial.

## Support files

- `references/catalyst-and-flow-verification.md` — higiene katalis (tanggal + sumber), flow
  concentration, dan **Rule 6: scan laggard fundamental** (Binance klines 30+ simbol → metrik → baru
  cari katalis bertanggal). Wajib dibaca kalau pertanyaannya "ticker apa yang potential tapi harga
  belum ngikut".
- `references/intra-narrative-ticker-scout.md` — angka lengkap scout level-ticker (laggard vs
  Q2/kurva vr/robustness) + cara reproduce; dipakai tiap kali nanya "ticker mana di tema ini".
- `references/narrative-scan-multichain.md` — exact command recipes, keyless platform APIs
  (StonkFun public endpoints + fields), parse snippets, and the report skeleton.
- `references/narrative-snapshot-2026-09-30.md` — worked example / baseline snapshot of the
  "tokenized-stock pair" meta (tokens, numbers, sources) to diff against on future scans.
