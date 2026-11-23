# Narrative ticker shortlist — "kasih gw N ticker dengan narasi terbaik/terseksi"

Use when the user asks for a **ranked shortlist of liquid, established tickers** chosen by narrative
quality: "coin dengan narasi terbaik dan terseksi, coba kasih gw 3 ticker", "coba 5 ticker",
"ena vs wld mana narasinya lebih menarik". Different shape from the other two scan references:

| ask | reference |
|---|---|
| memecoin / cross-chain meta, addresses, GMGN | `narrative-scan-multichain.md` |
| "which coins held up / strongest now" | `relative-strength-scan.md` |
| top N tickers by narrative, majors to mid-caps | **this file** |

## 1. Universe (fixed basket, one script)

~35 Binance USDⓈ-M perps covering every theme the user tracks. Keep the list in the script so runs are
comparable: majors (BTC ETH BNB XRP SOL AVAX HBAR), L1/L2 (SUI SEI TIA ARB OP STRK ZK), DeFi (AAVE
PENDLE CRV LDO MORPHO EIGEN ETHFI AERO JUP), RWA (ONDO LINK), stablecoin/yield (ENA SKY), privacy
(ZEC), perp DEX (HYPE), AI/DePIN (TAO FET RENDER VIRTUAL), memes (DOGE PEPE PUMP).

## 2. Data pull (all keyless, one python heredoc)

```
tickers : GET https://fapi.binance.com/fapi/v1/ticker/24hr          # every symbol, one call
funding : GET https://fapi.binance.com/fapi/v1/premiumIndex         # lastFundingRate
klines  : GET fapi.binance.com/fapi/v1/klines?symbol=S&interval=1d&limit=120
OI      : GET fapi.binance.com/fapi/v1/openInterest?symbol=S        # koin → x harga = notional
crowd   : GET fapi.binance.com/fapi/v1/futures/data/topLongShortAccountRatio?symbol=S&period=1h&limit=1
HL ctx  : POST https://api.hyperliquid.xyz/info {"type":"metaAndAssetCtxs"}
          → midPx, funding, openInterest, dayNtlVlm per coin (cross-venue sanity check)
```

Per symbol compute and print in one table: `last · 24h% · 7d% · 30d% · vsMA7 · vsMA30 · ATR14% ·
vol7d avg $M · % below 120d high`, then OI ($M), funding %, top-trader long %.

## 3. Theme score from the user's own scanner (context, not the verdict)

`~/.hermes/data/narr_rotation_state.json` + `~/.hermes/logs/narr_rotation.log` carry the theme ranking
from `narrative_rotation_early.py scan` (run it if stale). Baseline 10 Okt 2026: RWA/Tokenized 6,8
(konfirmasi), Gaming 6,3, Infra/DePIN 6,3, L2/Scale 6,0 (TELAT), Meme 4,0, DeFi 3,6, L1 3,6, Privacy
3,6, **AI/Compute 3,0 (paling dingin)**.

Use it to catch the contradiction the user cares about: **one name ripping while its sector score is
the coldest = idio move, not a sector move — say that out loud.** (WLD +12% on 10 Okt with AI/Compute
3,0 was exactly this; STRK's move happened with L2 already labelled TELAT.)

Also pull 24h movers vs the majors: if BTC/ETH/SOL are flat (10 Okt: BTC 82.741 +0,4%, ETH 2.496
+0,1%, SOL 110,1 −0,3%) then every gainer is idiosyncratic — state it so the user doesn't read beta.

## 4. Rank on three axes (never on 30d % alone)

1. **Narasi** — is there a mechanism with value accrual (buyback, fee switch, licensed rails, staking)
   or just a story? Is there a **dated catalyst** in the last ~2 weeks? A narrative with an on-chain
   number to watch (USDe $7,5B gate, AQAv2 payment, ETF inflows) beats a vibe.
2. **Arus** — vol7d avg, OI $, funding, top-trader long %. Crowd ≤65% long = belum crowded (a plus);
   >70% long = rawan long squeeze (a minus). Funding slightly negative on a riser = healthy.
   Net-short crowd on a strong name (ZEC 45,1% long vs 54,9% short) = squeeze fuel, name it.
3. **Risiko harga** — ATR14%, % below 120d high, MA7/MA30/MA90 position. "Masih di atas MA90 tapi di
   bawah MA7/MA30" = uptrend utuh, cuma konsolidasi. ≥20% di bawah puncak = masih butuh kerja.

Freeze the ranking, then write the exclusions.

## 5. Per-candidate catalyst search (mandatory)

One `web_search` per shortlisted ticker ("<token> rally/news <bulan> <tahun> catalyst") + verify the
claim against the exchange data. Record: mechanism, date, who (issuer/regulator/exchange), and what
the token actually gets. Prefer primary sources (protocol blog, PR Newswire, The Block) over
price-prediction pages. Also capture the honest counter-argument (e.g. ONDO pra-IPO notes = unsecured
SPV obligations in BVI, bukan saham, hanya non-US; ZEC ETF = taruhan harga, custody transparan).

## 6. Output shape (Bahasa Indonesia, this user)

Header table of rank, then per ticker: **narasi 1 baris → angka (skala/katalis) → data harga (ATR,
7d/30d, posisi MA, jarak dari puncak, volume, OI, funding, crowd) → risiko → skenario masuk**.
Then:
- **"Yang nggak masuk, dan alasannya"** — 3 names max, each with the number that disqualified it. This
  section is what makes the answer trustworthy; the user reads it and stops asking "kenapa bukan X?".
- **"Cara pakai"** — stop ≥ 1× ATR, leverage maks 2–3x, risiko 1–2% modal per posisi, and a worked
  size example (modal 1.000 dolar + stop 10% → posisi 100–200 dolar).
- **Watch list** — the 2–3 live numbers that would confirm/kill the thesis (next AQAv2 payment, USDe
  toward 7,5B, tutup harian di atas level X).
- Disclaimer: "bacaan rule based, bukan saran investasi." **No closing question.**
- Save `~/obsidian-vault/N Ticker Narasi Terbaik (DD Mon YYYY).md` and name the file in the reply.

Styling for this user: casual "gw/lu", **no "-" character anywhere in the message** (ranges use
"sampai", bullets use "•"), ringkas but the numbers stay.

**Tiered count:** when the user escalates ("coba 5 ticker"), keep the top-3 stable and ADD candidates
— but **re-pull every number in a fresh run**, never reuse the previous turn's prices. Delete or skip
the superseded smaller note so the vault has one file per ask, and say you did.

## 7. Worked example 10 Okt 2026 (baseline to diff against)

| # | ticker | last | ATR | 7d/30d | vs MA7/MA30 | dr puncak 120d | narasi & katalis |
|---|---|---|---|---|---|---|---|
| 1 | HYPE | 84,37 | 5,0% | −5,5% / +7,4% | −4,4% / −4,1% | −14,0% | 97% fee → buyback AF (~45,7jt HYPE); AQAv2 bayar $14,58jt 6 Okt; 3 ETF ≈ $478jt |
| 2 | ONDO | 0,4964 | 8,4% | −1,0% / +45,0% | +2,0% / +9,3% | −18,8% | RWA skor 6,8; Private Markets pra-IPO AI 6 Okt; DTCC Fund/SERV 16 Sep; topLong 71,9% (crowded) |
| 3 | AAVE | 174,42 | 6,7% | −3,9% / +44,7% | −0,3% / +14,6% | −7,2% | Aavenomics 3.0 27 Jun 2026; $33,61B supply/$13,23B borrow; funding −0,001% (belum crowded) |
| 4 | ZEC | 1.226 | 8,5% | −6,0% / +13,6% | −4,6% / −10,7% | −27,8% | ETF spot privasi pertama AS (ZCSH 25 Agu 2026); shielded 30% supply; topLong 45,1% vs short 54,9% |
| 5 | STRK | 0,0708 | 10,5% | +30,6% / +153,6% | +20,5% / +63,5% | −8,8% | ZK + Bitcoin: strkBTC 2 Okt, v0.14.4 5 Okt, 900jt STRK staked; paling berisiko dikejar |
| bench | JUP | 0,3726 | 8,7% | +13,4% / +66,0% | +5,3% / +22,2% | −4,0% | Jup Lend > Kamino; kalah karena vol harian cuma $46jt |
| bench | WLD | 0,5591 | 10,7% | −6,5% / +41,4% | +3,6% / +17,7% | −22,7% | AI identity seksi, tapi sektor AI skor 3,0 + 60% supply rilis s/d Jul 2028 |
| bench | ENA | 0,2207 | 10,4% | −7,7% / +54,5% | −3,4% / +4,3% | −25,1% | unlock 5 Okt udah lewat; buyback gated USDe $7,5B vs $4,9B |

## 8. Pitfalls

- **Kline path: use Binance `fapi/v1/klines` for everything, including HYPE** (HYPE, ONDO, ZEC all have
  Binance futures pairs). A naive Hyperliquid `{"type":"candle","coin":"HYPE",...}` POST came back
  **HTTP 422** in this session; `metaAndAssetCtxs` (mid, funding, OI, dayNtlVlm) worked fine and is the
  right Hyperliquid call for context. One code path = fewer failure modes.
- **Aggregator/prediction pages go stale or wrong.** CoinStats showed ZEC at $1.556 while Binance live
  was $1.226; an OKX page showed ONDO $0,5054 dated 30 Sep with a different 7d %. Trust the exchange
  API, timestamp the scan in the note, and never lift a price from a search snippet.
- **30d % ranks squeezes to the top.** STRK (+153,6%) is the strongest momentum and the riskiest entry;
  its Layer-1 story is still "under consideration" with no governance decision. Offer a pullback entry
  and say plainly it's the chase-risk name.
- **Quote the ratio, don't imply it.** Chasing WLD at 0,556 with a sane stop below 0,49 against a first
  target at 0,60 is <1:1 — if the R:R is bad at market, say so and give the pullback zone instead.
- **Unlock/supply overhang decides "cheap" or not:** HYPE ~22% circulating and unlock s/d 2027; WLD 60%
  not yet released (linear to Jul 2028). Check circulating vs total before using "jauh di bawah ATH".
- **Don't re-derive themes by hand** — the bucket definition lives in `THEMES` (`deep_dive_daily.py`) and
  is reused by `narrative_rotation_early.py`; a second theme list will drift (see SKILL.md Step 4b).
