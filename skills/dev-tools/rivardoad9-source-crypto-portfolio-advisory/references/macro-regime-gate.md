# Macro regime gate — dominance + breadth on EVERY setup

Standing user instruction (2 Okt 2026, verbatim): *"setiap lu kirim setup perhatiin usd.d, btc.d, eth.d dsb.
biar punya conviction yg lbih titnggi."* This is not decoration on a report — it is the gate that decides how
much conviction (and therefore size) a setup deserves. Applies to ad-hoc "masuk mana sekarang" answers and
to the daily deep dive alike.

## Metrics to print (one line, numbers only, no adjective without a number)

| metric | what it answers |
|---|---|
| BTC.D now + **Δ7d** + Δ30d | is money concentrating in BTC or spreading out |
| ETH.D | large-cap alt appetite |
| USDT.D + **stablecoin.d** (USDT+USDC+DAI+USDe…) + Δ7d | cash parked off-exchange = risk-off |
| **breadth**: % of top-100 (ex-stables) beating BTC over 7d and 30d, + median alt 7d vs BTC 7d | is a move a *rotation* or 1-2 names |
| ETH/BTC 7d / 30d | classic alt-strength proxy |
| TOTAL mcap + 24h | context for the whole read |

## Verdict rules (drive the score, not the prose)

- **HEADWIND** — BTC.D **+>0,15pp/7d** *and* breadth **<40%** → conviction **−1…−2**, entry only on a
  confirmation trigger, size explicitly cut. Say the word "headwind" in the report.
- **TAILWIND** — BTC.D **−>0,15pp/7d** *and* breadth **>60%** → conviction **+1 max** (structure/catalyst
  still have to be there).
- `stablecoin.d` rising = risk-off (cut); falling = risk-on (mild plus).
- **Data incomplete → neutral and say so** — never manufacture conviction from a missing series.

Live example (2 Okt 2026, 20:12 WIB): BTC.D 58,85% (+1,67pp/7d) · breadth **21%** top-100 beating BTC ·
median alt 7d **+0,1%** vs BTC **+2,6%** · stablecoin.d 9,45% (−0,16pp/7d) · ETH/BTC −0,87% → **BTC-led,
alt lemah → headwind**. That moved HBAR from ~7/10 to ~6/10 and cut the suggested size from $340-590 to
$150-250 in the same message.

## Keyless recipe (this is the whole trick)

1. `GET api.coingecko.com/api/v3/global` → `market_cap_percentage` (btc/eth/usdt), `total_market_cap`,
   `market_cap_change_percentage_24h_usd`.
2. `GET api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&price_change_percentage=7d,30d`
   — free tier caps history at ~365d, so you **reconstruct past dominance** instead of asking for it:
   `share_ago(bucket) = Σ mcapᵢ/(1+chgᵢ/100) ÷ Σ mcapⱼ/(1+chgⱼ/100)` over the same 250-coin universe.
   That yields a real **7d/30d dominance delta** with no paid API. Breadth comes from the same list
   (count members whose 7d/30d change > BTC's own).
3. ETH/BTC from `api.binance.com/api/v3/klines?symbol=ETHBTC&interval=1d&limit=40`.
4. **CoinGecko 429 is normal here** — retry with 8–12 s backoff. If `/coins/markets` still fails, fall back
   to computing breadth from the ~45 most-liquid Binance USDT pairs (klines 1d limit 40, ~0,12 s sleep
   between calls ≈ 20 s total). Print which source was used; a dominance delta you couldn't compute is
   `None`, never 0.
5. **Cache** the result to `~/.hermes/data/market_regime.json` with `verdict` + a ready-to-paste `line`
   string. Frequency-sensitive consumers (15-min alert crons) read the cache when its mtime is < 6 h, so
   they never hammer CoinGecko.

Script: `~/.hermes/scripts/market_regime.py` (stdlib only; `--json` / `--dump` for inspection). Runs in
~0,6 s when CoinGecko answers, ~20 s via the Binance fallback.

## Wiring (so it is not a promise made in chat)

- `~/.hermes/scripts/deep_dive_daily.py` prints it as **section [0]**, before the narrative sections, via
  subprocess — so the daily collector can never be read without the regime in view.
- The deep-dive cron prompt carries the rule: quote [0] in mode A *and* mode B, headwind cuts the score
  1–2 points, tailwind adds ≤1, and log the regime beside the score.
- `gaming_entry_alert.py` and `holdings_watch.py` append `📊 <line>` to every alert they emit, from cache.

## Interpretation nuance that keeps the read honest

- **Relative strength cuts both ways.** HBAR at 7d +11,5% while BTC did +2,6% and the median alt +0,1% means
  it is inside the 21% minority beating BTC — *relatively* strong, but the environment still argues for
  small size. Report both halves; never present a token's own uptrend as if breadth agreed with it.
- **Breadth is the evidence for "narrow".** A sector basket pumping +20–60% (SAND/MANA/AXS/GALA) while
  breadth is 21% is a narrow rotation — which is exactly why those spikes get rejected fast (ALICE closed
  −15% off its blowoff high the next day). Use breadth instead of calling every pump a rotation.
- **The gate flips.** When BTC.D turns down and breadth crosses ~50%, the *same* tokens earn bigger size.
  Say the trigger out loud ("BTC.D < ~57,2% + breadth >50% → baru layak digedein") so the next decision is
  mechanical.
