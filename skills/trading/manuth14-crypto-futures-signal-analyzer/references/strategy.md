# Strategy specification (from author's supplied src/strategy.py)

Requires >=30 1m candles and >=30 15m candles, otherwise HOLD.
15m trend is bullish iff latest close > EMA21, otherwise bearish (including equality).
EMA is pandas `ewm(span=N, adjust=False).mean()` seeded with first close.
1m RSI14 uses rolling simple means of positive and negative close differences. Replace a zero average loss with 0.00001 before dividing.
1m volume MA10 is the mean of the latest ten volumes, including current candle.
BUY iff bullish AND EMA9 > EMA21 AND RSI < 48 AND volume > MA10.
SELL iff bearish AND EMA9 < EMA21 AND RSI > 52 AND volume > MA10.
Otherwise HOLD. No fresh EMA crossover required.
This tool filters unfinished candles and uses Binance spot klines, so it is not necessarily identical to an original bot using unfinished candles or futures contract data.

## Data source (v1.1)
Public Binance USD-M Futures klines (`https://fapi.binance.com/fapi/v1/klines`); completed candles only. No API credentials or trading endpoints. Exchange access varies by region.
