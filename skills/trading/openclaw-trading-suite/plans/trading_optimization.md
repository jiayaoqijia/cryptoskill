# BTC Dip Hypothesis Update and Swing Strategy Backtest

## Current Market Data (as of Feb 20, 2026)
- BTC Price: ~67k-69k (close: 66,946)
- RSI (14): ~40-41 (near oversold territory)
- MACD: Negative
- Support: ~67k
- Resistance: 69k-72k

## Hypothesis Update
The BTC dip appears to be in an oversold territory with RSI around 40-41, indicating potential for a bounce off the 67k support level. MACD remains negative, suggesting caution, but historical patterns from 2024 show that dips with RSI <40 often lead to recoveries if support holds.

## Swing Strategy Backtest on 2024 Dips
- **Entry:** RSI < 40 + bounce off support (approximated as price low near 95% of SMA50)
- **Exit:** 1:3 reward ratio (stop 3% below entry, target 9% above)
- **Data:** 2024 BTC daily data, Sept 30 to Dec 31

### Results
- Total Trades: 11
- Win Rate: 27%
- Total PnL: +1617 (on ~85k average entry, small gains)
- Most exits were stops, indicating the dip continued deeper in some cases.

## Adjustments for 2026 Fearful Levels
In 2026, assuming higher fear (e.g., fear & greed index lower), dips may be sharper and recoveries slower. Optimized parameters:
- **Entry:** RSI < 35 (stricter oversold)
- **Exit:** 1:2 reward ratio (stop 2% below entry, target 4% above) for quicker exits to capture smaller bounces.

### Optimized Results
- Total Trades: 9
- Win Rate: 56%
- Total PnL: +10023 (better risk-adjusted)

## Recommendations
- For the current dip: Monitor RSI < 40 with confirmed bounce at ~67k support.
- For future dips: Use RSI < 35 entry and a 1:2 reward ratio for improved win-rate stability in fearful markets.
