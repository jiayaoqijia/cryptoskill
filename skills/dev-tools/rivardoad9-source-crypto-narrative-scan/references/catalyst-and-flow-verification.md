# Catalyst hygiene + flow verification (worked out 2 Okt 2026)

Companion to `sector-heat-and-trap-checks.md`. Both files exist because the scan flow got caught
publishing two different classes of error in one day: a **stale catalyst sold as fresh** and a
**news event attributed to the wrong token**. Treat this file as part of the procedure.

## Rule 1 — A catalyst is only a catalyst if it has a date and a source

Every catalyst claim must carry: **date + one named source** (media/docs/blog — "internet" is not a
source). If you cannot date it, it scores **0** and cannot carry a pick over the conviction bar.

**Freshness ladder** (this is what the daily job's rubric now encodes):

| Age of the catalyst | Treatment |
|---|---|
| dated in the future (e.g. GTA 6, 19 Nov 2026) | full weight — this is the tradable kind |
| ≤ 30 days old | full weight |
| 30–45 days | half weight, name the date |
| > 45 days, still running (a mechanism, a fee switch, a buyback) | name its **start date** and down-weight: a machine that has been on for months is a feature, not news |

**Worked example (2 Okt 2026, AAVE).** The cron report justified an 8/10 with "Aavenomics 3.0 —
automatic buyback, 100% of revenue to governance". Verified true — and **live since ~June 2026**.
So it is a structural quality of the token, not a fresh catalyst. Also in the same report: "Aave V4
Equities Hub on Base" (7 Coinbase-tokenized stocks as collateral, Chainlink oracle, $29M initial
cap) — verified true via the aave.com blog + secondary press, and genuinely new. One real catalyst,
one stale one dressed as fresh: the fix is to score them differently, not to drop the token.

## Rule 2 — Never attach a news event to a token it does not concern

The same report listed "overhang exploit bridge LayerZero" as a **SAND** risk. The exploit is real —
KelpDAO/LayerZero, $292M, RPC poisoning, Lazarus — but it is **April 2026** and it is about
**rsETH**, not SAND. Keyword adjacency produced a confident false claim.

Checks that catch this class:

1. Search the event **without** the token name (`LayerZero exploit KelpDAO`) — if the story doesn't
   mention the token, it isn't the token's catalyst.
2. Ask what the event actually touches (asset, chain, contract field). If the token doesn't hold or
   use that asset, discard it.
3. Then find what the *real* overhang is, with its own date. For SAND: **venue delistings** —
   GMO Coin terminating SAND/CHZ/FIL support **24 Okt 2026** (transfer out until 7 Nov, remainder
   force-sold for yen; announced 9 Sep 2026) plus SBI VC Trade delisting SAND 5 Agu 2026. That is a
   dated, SAND-specific, JPY-selling overhang — the actual risk, not the exploit.

Generalised: an event is only this token's problem if you can say **how** it reaches the token
(asset held, revenue stream, venue, unlock). Write that sentence or drop the item.

## Rule 3 — Verify before publishing, and correct in the open

Publish-then-verify is not acceptable in this lane: the numbers are quoted from a collector but the
*narrative* comes from the model. Before a catalyst or risk ships, run `web_search` on it and keep
the URL. When verification contradicts an earlier claim (yours or a cron's), say so plainly —
"gw salah, yang bener X karena Y, sumber Z" — and patch the prompt/source that produced it. The user
reads an explicit self-correction as reliability, not as weakness; what they will not forgive is a
number or a story that collapses under one search.

## Rule 4 — "Money is all in X, next is Y" → measure flow concentration first

When the user (or you) proposes a rotation target, test whether flow is actually rotating there.

```python
# Binance-only 24h quote volume per symbol, one call, no `symbols=[…]` param
# (the param 400s if ANY symbol is invalid — fetch all tickers and filter instead)
t = get("https://api.binance.com/api/v3/ticker/24hr")
rows = {r["symbol"][:-4]: r for r in t if r["symbol"].endswith("USDT")}
# aggregate across venues / all pools:
get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=<id>&…")
```

Report **both** numbers, labelled (Binance spot vs aggregate) — they differ by 3–10× and the venue
number is the one that decides whether *this* user can size a position.

**Worked example (2 Okt 2026, NFT meta).** Leaders were pulling real money: SAND $351M 24h volume
(+63%), MANA $108M (+19.7%), AXS $76M (+12.6%), GALA $7.1M/CoinGecko $27M. The proposed "next"
laggards had almost nothing: TNSR $1.09M (Binance), BLUR $395k, GHST $109k, BIGTIME $479k — a
**~320:1 SAND:TNSR volume ratio**. Correct finding: the meta is real but flow is **concentrated in
the liquid majors**; laggards catching up is a hypothesis without flow support yet. Say that instead
of endorsing the rotation — and give the laggard a trigger (break above its own structural high with
volume) rather than an entry.

## Rule 5 — Score liquidity on the venue the user trades

Rubric line "liquidity & access" must name the venue. A CEX-listed ticker with <$5M/day on Binance
fails the sizeability bar even when aggregate volume looks acceptable, and the failure is what keeps
it under the conviction threshold. State it as a **sizing warning** (slippage on exit), not just a
score deduction.

## Rule 6 — Laggard fundamental: katalis padat tapi harga turun

Pertanyaan user: "ticker apa yang potential tapi price action belum ngikut". Jangan jawab dari daftar
berita — ukur dulu harganya, baru cari katalisnya.

**Scan cepat (Binance publik, tanpa key, ~8 detik untuk 30+ simbol):**

```python
k = get(f"https://api.binance.com/api/v3/klines?symbol={s}USDT&interval=1d&limit=200")
```

Metrik yang dipakai (harian, semua dari satu respons): `r1 r7 r30 r90`, posisi harga di range 90 hari,
`vol7/vol30`, RSI14, EMA20/50/200, ATR14 dalam persen. Labaas kandidat kalau: **r90 positif tapi r30
negatif**, RSI 33–45, posisi range < 50%, dan ada ≥ 2 katalis bertanggal dalam 7 hari terakhir.

Pitfall teknis: simbol yang listing < 90 hari balik dengan bar lebih sedikit → `max(k[-90:])` tetap
jalan tapi `r90` harus `None`, dan format `f"{None:.1f}"` meledak. Hitung `w = min(90, len(k))` dan
cetak `—` kalau bar kurang dari window.

**Yang membedakan laggard dari sampah:** katalis bertanggal DAN harga belum merespons, contoh pola
yang lolos: satu minggu berisi 3–4 pengumuman institusional (integrasi bank kustodian, data rating
agensi on-chain, tokenisasi komoditas) sementara harga -20% sebulan, RSI 40, di bawah EMA20/50 tapi
masih di atas EMA200. Pola yang gagal: turun 20% dengan katalis cuma unlock kecil (0,2% supply) — itu
noise, bukan laggard.

**Pemisahan wajib di jawaban:** (a) leader yang istirahat (r90 +60% tapi r30 datar, nempel EMA20) —
jangan chase di high, kasih dua skenario breakout/retest; (b) laggard dengan katalis; (c) **daftar yang
di-skip beserta alasannya**. Poin (c) yang bikin jawaban kelihatan riset, bukan daftar belanja.

Tiap kandidat keluar dengan trigger eksplisit: level reclaim (EMA20/50 atau high 20 hari), target
(high 90 hari / high 20 hari), dan invalidasi (low 20 hari / EMA200). Angka level = level tujuan yang
dicek live oleh user, bukan janji.

Buka jawaban dengan satu baris regime (`market_regime.py`): BTC.D + arah 30 hari, breadth, total mcap.
BTC.D naik = headwind alt, jadi output-nya "watchlist + trigger", bukan ajakan masuk.

## Ready-reckoner: verified facts from this session (re-verify, don't trust blindly)

| Claim | Status | Source shape |
|---|---|---|
| Aave V4 "Equities Hub" on Base, tokenized stocks as collateral | TRUE, new | aave.com blog + press |
| Aavenomics 3.0 automated buyback, 100% revenue to governance | TRUE but **live since ~June 2026** | press/Defiant |
| KelpDAO/LayerZero $292M exploit | TRUE, **April 2026, rsETH** — not a SAND event | news, multiple |
| GMO Coin terminating SAND/CHZ/FIL, trading ends 24 Okt 2026 | TRUE, announced 9 Sep 2026 | CMC/JVCEA coverage |
| The Sandbox Studio public launch (multiplayer, monetisation, "Agent Nova") | Oct 2026 per CMC summary — **verify against the official blog before publishing** | single secondary source |
| NFT meta flow concentrated in majors (SAND/MANA/AXS/GALA) | TRUE 2 Okt 2026 | Binance + CoinGecko |
