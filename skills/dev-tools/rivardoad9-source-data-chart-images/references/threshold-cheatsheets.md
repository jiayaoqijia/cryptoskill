# Threshold cheat sheets — banks, derivation, calibration

Content bank behind the two reference cards ("on-chain bagus vs jelek", "kalau mau LP angka bagus
berapa"). Keep the numbers exact; these thresholds are the product.

## Card 1 — on-chain screening (per-metric thresholds)

| Metrik | 🟢 | 🟡 | 🔴 |
|---|---|---|---|
| Tax beli & jual | 0% | 1–5% | >5% |
| Top 10 holder | <20% | 20–50% | >50% |
| Bundler | <5% | 5–30% | >30% |
| Phishing / entrapment | <10% | 10–30% | >30% |
| Insider / sniper / dev hold | 0% | <10% | >10% |
| Rug ratio | <10% | 10–30% | >30% |
| Mint & freeze dicabut | Ya / NoMint | — | Belum |
| Liq ÷ MC | >5% | 1–5% | <1% |
| Volume 24j ÷ Liq | 0,5–5x | 5–20x | <0,1x atau >20x |
| Net buy 24j | plus & volume gede | tipis / campur | minus terus |
| Holder | >5.000 & naik | 1.000–5.000 | <1.000 |
| Umur pool | >14 hari | 3–14 hari | <3 hari |

Mental model to pair with the table — three questions, and one red answer ends the review:
1. Bisa keluar nggak? (liq, tax, mint/freeze, LP burned)
2. Yang pegang siapa? (top 10, bundler, phishing, insider/dev)
3. Ada yang beli beneran nggak? (volume, net buy, holder growth)

Loud greens never redeem a red. Say that explicitly on the card.

## Card 2 — LP gate (real constants, not vibes)

Source: `flowmetrix-ai-agent/src/config/env.ts`.

| Konstanta | Nilai | Arti |
|---|---|---|
| `MIN_FEE_TVL_RATIO` | 0.008 | fee/TVL 24h ≥ 0,8% cuma buat jadi kandidat |
| `MAX_FEE_TVL_RATIO` | 0.25 | >25%/24h = TVL collapse, bukan yield asli |
| `MIN_TVL_USD` / `MAX_TVL_USD` | 50 000 / 500 000 | kecil: kena gas · besar: fee kekecilan |
| `MIN_FEE_COST_COVERAGE` | 2.5 | fee 24h ≥ 2,5x biaya round-trip |
| `FORCED_EXIT_SLIPPAGE_PCT` | 2.0 | asumsi concession saat keluar paksa |
| `MIN_DOWNSIDE_COVER_PCT` / `MIN_UPSIDE_COVER_PCT` | 45 / 15 | floor lebar range (clamp) |

**Effective floor ≈ fee/TVL 6,1% per 24 jam** (≈2 200%/th) — 2,5 × (2% slippage + gas). Reported
outcome on live data: 33 pools passed the first filter, **2** cleared the gate. Pair this with the
non-negotiable reality line: LP = jual volatilitas; walk-forward live was **−18,7% @$300** and
**−40,2% @$1 000**, so good fee/TVL ≠ profit.

Scale rows used on the card:
- fee/TVL 24h: <0,8% 🔴 · 0,8–2% 🔴 · 2–6,1% 🟡 marginal · 6,1–25% 🟢 · >25% 🔴
- volume/TVL 24h: <1x 🔴 mati · 1–2,5x 🟡 · 2,5–5x 🟢 · 5–20x 🟢 panas · >20x 🔴 wash/churn

## One metric, two meanings (state the lens)

`volume/TVL > 20x` is 🔴 on a **buy** screen (bot churn, gampang digoyang) but is exactly what you
want for **LP fee income**. The same number flips verdict depending on the question. Whenever a card
is reused across both lenses, label which one is being applied — otherwise the card contradicts itself.

## Unit-ambiguity pitfall (cost a whole analysis)

Exchange UIs print fee totals with **no unit label** (GMGN pool row: `Total Fees ≋ 208`). Resolve by
cross-check, never by assumption: `fees_24h ≈ volume_24h × known pool fee rate`.

Worked: bukangi on `pump_amm`, volume 24h $2,75 jt, fee rate ~0,25% → ~$6,9 rb/hari ≈ 58 SOL/hari;
cumulative `total_fee` 208 × $119,30/SOL ≈ $24,8 rb over ~3 hari → the SOL reading is the consistent
one. The two readings flip the verdict: USD ⇒ fee/TVL 0,24%/24h (fail, same as ZEC), SOL ⇒ 8–9,5%/24h
(pass the 6,1% gate). Put the uncertainty on the card / in the answer instead of silently picking one.

## Resolving a token from a dashboard screenshot

`gmgn-cli market search -q <nama/simbol> --chain sol --raw` → gives CA, `launchpad_platform`,
`exchange`, `created_at` (pool age), `mcp` (MC), `ath_market_cap`, `total_fee`, holder count,
`total_buy_tax`, creator. Then `gmgn-cli token pool|info --chain sol --address <CA> --raw` for
reserves (`base_reserve_value` / `quote_reserve_value` → quote-token price and depth),
`price.price_*` for the 1m/5m/1h/6h/24h ladder, and the buy/sell volume split.

Parse with a small key-walker that prints only the interesting fields — the raw search dump ran to
105 KB and was truncated. `created_at` is epoch seconds: age_in_days = (now − created_at)/86400.

## Worked calibration examples (30 Sep 2026)

- **ZEC** (screenshot): Total Fees $5,39 rb ÷ Liq $2,22 jt = **0,24%/24h** → below the 0,8% candidate
  minimum → not an LP candidate, even though tax 0, bundler 1,14%, holders 122 rb were green.
  `Phishing wallet 70,99%` = the single red that ends it.
- **bukangi** `3iUTyNYW6xKv5kZUjtbrEDTsuJTrSVwvB3bQtxkLpump` (pump_amm, pair bukangi/**SKHY**, 3 hari):
  screening 6🟢 / 4🟡 / 1🔴 (red = volume/TVL 32,3x, 1 014 swap/jam); LP view fee/TVL 6,5–9,5%/24h and
  vol/TVL 32,3x → **passes the gate**, but the quote token is another memecoin, price +316% in 6h, and
  net flow 24h **−$70 rb** (net selling under a rising price) → not an entry. Reusable point: a
  "+300% in 6h with net outflow" candle means the quote side is dry, not that buyers are winning.
