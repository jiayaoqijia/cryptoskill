# Crypto relative-strength scan (who is actually strong while the market falls)

Use when the user asks "which coins are strongest right now", "what held up during the crash", or wants a shortlist of genuinely strong names (not just the top gainers). Verified working procedure, Binance spot public API only, no keys.

## 1. Universe (one call, all symbols)

`GET https://api.binance.com/api/v3/ticker/24hr` (no symbol = every pair).

Filter to: `quoteAsset == USDT`, `status` trading, `quoteVolume > 5_000_000`.
Exclude: stablecoins (USDC, FDUSD, TUSD, USDP, DAI, EUR, AEUR, USD1, RLUSD, U), leveraged tokens (`UP`, `DOWN`, `BULL`, `BEAR`, `3L`, `3S`), wrapped (`WBTC`, `WBETH`).
Expect ~90–100 survivors — that is the realistic liquid universe, not the ~2500 listed symbols.

## 2. Per-symbol metrics

`GET /api/v3/klines?symbol=<S>&interval=1d&limit=31` for each survivor (cheap at this size), then compute:

- `chg24` (from the ticker), `chg7`, `chg30` (close vs close N bars back)
- `dist_high30` = % below the 30-day high (closer to 0 = stronger structure)
- `above20` / `above50` = daily EMA20 / EMA50 position
- `vol_exp` = last full day volume ÷ mean of prior 7 days (expansion = participation arriving)

## 3. The four filters (and benchmark against BTC, not absolute)

Keep names that pass **all**: `chg7 > 0` · above EMA20 **and** EMA50 daily · `chg24 >= -1` · `vol24 > $5M`.
Compare against BTC's own `chg7` / `chg30` for relative strength. Reference run: 89 liquid coins → 47 green on the day → 51 beating BTC over 7d → **27 passing all four**.

Frame the tape honestly before the list: count how many are green. If ~half the universe is green while BTC/ETH/SOL are red, the correct headline is **"this is rotation out of majors into mid-caps, not a crash"** — not "everything is crashing".

## 4. Separate real strength from thin-market squeezes (the important step)

Raw % change ranks squeezes first. Treat these as red flags, not strength:

- one-day move ≥ +30% (especially +50–100%)
- prior daily volume ~$0–5M exploding 5–7×
- **zero news** behind it
- RSI > 85 (extreme overbought)
- still > 25% below the 30-day high (gap-and-fade, not a trend)

Real examples worth remembering: OGN +100% in a day with no news and normal volume jumping $5M→$30M; RLC +100% on 5 Oct with no confirmed catalyst and RSI 90; CTSI +31% on a market whose daily volume was $0–1M; QNT "up 277% in 30d" but −34.7% from its high and fading.

Report these separately as **"keliatan paling kuat tapi bukan kekuatan"** so the user doesn't chase them.

## 5. Verify the "why" per name

For each real candidate, find the catalyst rather than asserting one:

- local news tables/DBs (token-news + feed DBs) filtered to the last ~10 days for that symbol
- `web_search` for the specific move; chain/product-launch news often sits in exchange-listing trackers or CMC-style "why is X up today" pages
- **futures flow from `fapi` to tell new money from a squeeze:** open interest change over 24h and the funding rate. `OI +5% with funding only ~+0.005%/8h` = new longs arriving (healthy); funding spiking with OI spiking-then-dropping = crowded leverage / squeeze fuel.

## 6. Patterns to report, not just a list

- **Sector clustering:** if 5 of the top 10 come from one complex (e.g. Solana DeFi: ORCA/RAY/JUP/JTO/MET), say plainly that this is *one bet*, not five independent strong coins.
- **Non-crypto beta shows up green in a crypto drawdown:** tokenized-equity pairs on Binance (e.g. `NVDAB`, `QQQB`) track stocks, so they hold while majors bleed. Useful both as a strength datapoint and as a hedge-free way to stay long without BTC beta — label them as equity exposure, not crypto strength.
- Note which majors are the *sources* of the rotation (ETH/SOL/SUI/TAO negative over 7d) so the read is "money moving", not "money leaving".

## Pitfalls

- **Never state a token unlock schedule from memory.** Check the unlocks page (e.g. DefiLlama unlocks) before using it as a bull/bear argument. A wrong "unlock 24 Oct" was used as an exit rationale for ONDO when the actual next unlock was annual (18 Jan 2027, ~1.71B tokens, ~35% of mcap). A wrong number in a rationale contaminates the whole decision.
- **Public aggregator pages returned in search results can be stale or from a different date** — a leaked snapshot showed +21% 7d and a price range that contradicted the exchange API for the same token. When a page and the exchange API disagree, trust the exchange API and say so.
- Derive every number from live API data in the same run; do not mix in figures from earlier turns, and label the timestamp of the scan.
- Cap the deliverable: the user asks for "about 10" with a thesis each. Give 10 ranked + a separate trap list; do not dump the full 89-row table.
