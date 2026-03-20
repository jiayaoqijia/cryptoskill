# Technical Indicators

## EMA (Exponential Moving Average)
- Period 20: short-term trend
- Price > EMA = bullish, Price < EMA = bearish
- Formula: EMA = Price × k + EMA_prev × (1-k), where k = 2/(period+1)

## RSI (Relative Strength Index)
- Range 0-100
- < 30 = oversold (buy signal), > 70 = overbought (sell signal)
- Period 14 default

## Bollinger Bands
- Middle = 20-period SMA
- Upper/Lower = SMA ± 2 standard deviations
- Price at lower band + low RSI = strong buy
- Price at upper band + high RSI = strong sell

## Volume Spike
- Current volume > 1.5× average 20-period volume
- Confirms momentum signals
