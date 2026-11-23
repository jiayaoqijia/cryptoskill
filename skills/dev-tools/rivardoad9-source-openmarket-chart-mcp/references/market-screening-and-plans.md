# Screening markets and writing setups (OpenMarket data)

For the request "scan the market and give me N tickers with a plan", usually RR 1:2 intraday. Deliver picks with real
levels, not prose. Measurement script: `scripts/om_market_screen.py`.

## 1. Universe in one call
`market_screen` with `exchange: BINANCE_FUTURES`, `category: PERPETUAL`, `where: [{field: "volume24hUsd", op: "gt",
value: 100000000}]`, `sort: {field: "volume24hUsd"}`, `limit: 60`. One call scans the whole venue (785 markets) and
returns rows as arrays: `rawSymbol, lastPrice, priceChange24h (fraction), volume24hUsd, oiChange24h (fraction)`.
Liquidity floor of 100M USD volume is the practical cut for a plan someone will actually execute.

## 2. Shortlist before spending weight
Keep: rising OI alongside rising price (positioning, not just spot drift), moderate 24h change, 15m ATR roughly
0.4 to 1.5 percent. Drop parabolics — RSI(15m) above ~80, or price more than ~4 ATR above EMA20 — because the stop has
to go far below the candle and the RR dies; drop "failed pump" shapes (up on the day but below EMA20 and EMA50, position
in the lower third of the 24h range, volume ratio below ~0.5). Majors with 15m ATR under ~0.2 percent (BTC/ETH in a quiet
tape) cannot reach a 2R target in a day; say that instead of forcing a plan.

## 3. Candles per candidate
`points` per symbol: `type: TRADE_SIDE_AGNOSTIC_AGG`, `exchanges: ["BINANCE_FUTURES"]`, `rawSymbol`, `interval:
FIFTEEN_MINUTES`, `lookback: "5d"` → 480 bars. Cache each symbol's rows to disk; a rerun then costs no weight. The free
plan's 10 weight per 60s means about ten symbols per minute — expect a `{"error": "rate_limited"}` body, sleep ~7s and
retry rather than abandoning the batch.

## 4. Arithmetic worth doing
EMA20/50/200 on 15m closes; Wilder RSI14; ATR14 as a percent of price; ATR against its own 100-bar average (compression
below ~0.8 = a base, expansion above ~1.3 = a move already running); 24h change vs close 96 bars back; volume ratio of
the last 24 bars against the prior 96; high/low of the last 12 and 24 bars; 24h and 5-day high/low as the level map.

## 5. Turning measurements into a plan
- Entry is either the break of the two-hour shelf high (continuation) or the pullback to EMA20 while RSI has reset to
  roughly 45 to 60 (tighter stop). Give the trigger explicitly: "15m close above X".
- Stop sits behind real structure — the shelf low, the 24h low, or EMA20 — never a bare ATR multiple, and the plan names
  that structure in words.
- Risk percent = (entry − stop) / entry. Target = entry + 2 × risk, then check the target against the 24h high and the
  5-day high: a target just above the day high is a continuation plan that needs a breakout, so label it as one instead
  of implying there is clear air above.
- State RR per pick (2.0 vs 1.8 is worth saying), the invalidation ("15m close below the stop, and the day's structure
  is broken under EMA50"), and the funding check: 0.01 percent per 8h is the neutral baseline, so a reading at that level
  means not crowded and no carry cost.

## 6. Deliverable shape for this user
Ranked picks, one block each: current price and 24h change, RSI/ATR, EMA positions, the structural read, then entry,
stop with its structure, risk percent, target, RR, invalidation. Then the rejects with a one-line reason each (he asks
for the bad ones too) and one honest line when every pick leans the same way — correlated positions are one risk, so
size accordingly. Indonesian, casual, no dash bullets, no tables. Close on the risk note, not on an offer.

## 7. Record the result
He keeps a watchlist named `Hermes` empty for exactly this. `watchlist_list` → find its id → `watchlist_add_symbols`
with refs `EXCHANGE:SYMBOL` (e.g. `BINANCE_FUTURES:NEARUSDT`) → read it back with `watchlist_get` and report what is
in it. Verified write, not "I added them".
