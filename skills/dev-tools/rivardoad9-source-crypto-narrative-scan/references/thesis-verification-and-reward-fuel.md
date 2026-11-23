# Verifying a handed-to-you thesis + reward-token fuel math (worked 4 Okt 2026)

Companion to `catalyst-and-flow-verification.md` and `single-token-move-attribution.md`. This file
exists because the flow now regularly starts with **someone else's thesis**: a forwarded tweet, a
podcast clip, a chart screenshot with the label cropped out. The failure mode is restating the
thesis back to the user; the job is to run each dot against live data and say which ones hold.

## The method ("connecting the dots"), per-dot

Source that triggered this: @aveai_id status 2106738605901398079 (summary of @zachvierrr ×
@hansupermanz) — the method it teaches is: narrative momentum → a token that represents the
narrative → a *direct* link to the parent asset → launchpad/LP ecosystem connection → holder
red flags → visual identity / UGC → sizing discipline. Every one of those is checkable.

| Dot | Question | Where the answer comes from |
|---|---|---|
| 1 | Is the parent narrative still early or already cooling? | 7d change, distance from 120d high, **volume trend** — Binance klines for the parent asset; `market_regime.py` for the sector regime |
| 2 | Is the mechanism real? | `gmgn-cli token info/security/pool` (tax %, pair quote asset, mint/freeze revoked, LP burned) + the project's own site + press |
| 3 | Ecosystem / launchpad link? | `launchpad`, `dev.creator_open_count`, `dev.ath_token_info` |
| 4 | Who holds it **now**? | `token holders` top-50: tags, avg_cost cohorts, `native_balance` |
| 5 | Is smart money / KOL still in? | `gmgn-cli token traders --tag smart_degen|renowned` |
| 6 | What is the FUEL? | see formula below |
| 7 | What is the entry? | trigger / stop / RR off the pool's own high-low structure |

## The fuel formula — the dot almost everyone skips

For a tax / reflection / reward token (holders get paid in another asset), distribution is a
function of **turnover, not price**:

```
holder yield ≈ tax% × (24h volume ÷ market cap)
```

| Moment | Volume 24h | MC | Tax | Implied yield |
|---|---|---|---|---|
| peak (7 Sep 2026) | $22M | $124M | 3% | ≈ 0,53%/day |
| 4 Okt 2026 | $2,39M | $43,6M | 3% | ≈ 0,16%/day |
| 4 Okt 2026 (calendar day only) | $0,69M | $43,6M | 3% | ≈ 0,05%/day |

So the engine's fuel decayed **3–10×** *before* the token's −76% drawdown. State it that way: a
reward token's price is a claim on future volume, and "price is down 76%" plus "yield is down 10×"
is a decaying asset, not a discount.

## Worked case — ZCAT / Anonymous Cat (`HcRLc9VDgjLeK154xDawfb1dmVJ98DoSqcwTHGqiDeJR`, Solana)

Verified dots (all from live calls, 4 Okt 2026 ~23:00 WIB):

- **Mechanism real**: Token-2022 transfer-fee extension, permanent **3%** on transfers → converted to
  ZEC → auto-airdrop to wallets holding ≥$20 (no claim/stake). Paired **ZCAT/ZEC** (Raydium) and
  ZCAT/SOL (Meteora). `mint`+`freeze` revoked (null authorities), LP 95% blackhole/burn, no honeypot.
  Cumulative paid: ~$5M by 9 Sep, ~$8M by 16–17 Sep (~2.320 ZEC ≈ $2,8M as of 7 Sep, 470k payouts).
- **Ecosystem**: launchpad **StonkFun** (lets a token pick its own quote asset — that is why a ZEC
  pair exists); creator is a **serial launcher (367 tokens, funded from Binance)** whose ATH token is
  **STONK** (~$140–337M ATH MC) — still trading, so the link is real, not marketing.
- **Parent narrative cooling**: ZEC $1.319, +191%/90d, +157%/60d, **−16,9%/7d**, **−22,3% from its
  120d high** ($1.653 on 26 Sep), daily volume $612M (23 Sep) → $64M (4 Okt).
- **Chips**: top20 = 25,9% / top50 = 40,8% of supply; **35 of the top 50 carry a `bundler` tag and 42
  arrived via `transfer_in`**; **bundler share of volume = 48%**; bot-degen rate 22,7%. Two cost
  cohorts: avg cost 0,0008–0,003 (unrealized +300% … +5.800%) and avg cost 0,085–0,11 (−47% … −59%,
  ≈8% of supply trapped overhead).
- **Flow**: 7 smart-money wallets, **all 7 exited 100%**, net realized only +$2,4k (5 of 7 at a
  loss); 30 tracked KOLs, nearly all at $0 holdings. That is the opposite of "SM masih nampung".
- **Falsified red flag**: the forwarded method warns "top holders hold a lot of SOL = bots/dumpers".
  Here only **2 of 50 wallets held ≥200 SOL** (3.220 SOL, 987 SOL) — the structural risk was
  bundle-distributed chips, not SOL-rich whales. **Always run the source's red flags as tests and
  report the one you actually found, even when it contradicts the source.**
- **Price shape at the time**: $0,0452, MC $43,6M, +28,9% on the day off a 0,0306 low (3 Okt);
  resistance 0,0496 (day high, only ~+10% away) vs support 0,0324 (−28%) → no edge at the quote;
  the trade only exists as "break & hold > 0,0496 → 0,055–0,062, stop < 0,0430".

## Market-wide reads used in the same report (keep these three panels together)

1. **Regime line** (`market_regime.py`) — mandatory one-liner on every setup.
2. **Our own narrative detector** (`narrative_rotation_early.py` → `narr_rotation_state.json`) — it
   ranks themes; here it put **Privacy (the ZEC leg) last at 2,3** with volume 0,26x while AI/Compute
   led at 7,2. Quoting the detector is what turns "the narrative is cooling" from opinion into data.
3. **Where the bot money is right now**: `gmgn-cli market signal --chain sol --mc-min 1000000 --raw`
   (fresh signal board) + `market trending --interval 1h --min-volume 500000 --raw`.

## MC-print / bot-churn sanity check on hot boards

A signal board being full does not mean opportunity. On 4 Okt 2026 the top two rows were tokens with
**MC $410M / $407M, ~2.950 / 3.036 holders, $1,1M / $0,3M daily volume** → **MC ÷ liquidity ≈ 220×**.
Print `MC ÷ liq` and `MC ÷ holders` before quoting any MC; when they are absurd, say the MC is not
trustworthy instead of repeating it. Same board: a cluster of 4-letter tickers ending in `F`
(DOTF/VSOF/WOTF/ATFS/ECTF/WAIF/USDF/GOIF) all firing within ~20 minutes = one launch family's churn,
not a narrative.

## Data plumbing that made this possible (when GMGN is banned mid-investigation)

- `https://api.dexscreener.com/latest/dex/tokens/<mint>` — every venue's pairs for one token: price,
  liquidity, 24h volume, 6h/24h change, txns (`h24` is a **rolling** window). `/latest/dex/search?q=ZEC`
  found the narrative's competing tokens.
- `https://api.geckoterminal.com/api/v2/networks/solana/pools/<pool>/ohlcv/{minute,hour,day}?aggregate=1&limit=48&currency=usd`
  — pool OHLCV for levels; `/pools/<pool>` gives reserve/volume/price_change/transactions.
  **`ohlcv_list` is newest-first: sort by timestamp or your "last" bar is the oldest** (an actual
  +32,8% bounce was briefly read as −24,8%). Fields are strings — cast with `float()`.
- `https://api.binance.com/api/v3/klines?symbol=ZECUSDT&interval=1d&limit=120` — CEX benchmark for
  the parent asset, no key.
- GMGN heavy endpoints (`token holders`, `token traders`) need **~15–20 s between calls**; the
  bundled `analyze.py` in `gmgn-holder-analysis` fires three calls concurrently and is the fastest way
  to earn a ban. One call, then sleep, then parse locally.
