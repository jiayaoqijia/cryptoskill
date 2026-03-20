---
name: binance-watchlist
version: 1.0.0
description: Scan a full Binance spot watchlist using multi-indicator TA scoring. Returns ranked trading opportunities sorted by signal strength. No API key required (uses public data). Use for Binance scanning, watchlist screening, signal ranking, or finding the best trade setup right now.
author: JamieRossouw
tags: [binance, watchlist, crypto, trading, ta, signals, scanner]
---
# Binance Watchlist Scanner

Scans 20 Binance spot pairs every cycle and ranks them by TA signal strength.

## Default Watchlist
BTC ETH SOL XRP TRX DOGE ADA AVAX BNB LINK LTC SUI ARB OP NEAR DOT ATOM UNI MATIC

## Indicators Used
RSI(14), MACD(12/26/9), EMA cross (9/21), Bollinger Bands(20), OBV divergence, StochRSI(14)

## Output
Ranked list of opportunities:
```
🔥 TOP SIGNALS RIGHT NOW
+4 ARB/USDT | RSI=38 | MACD cross | OBV rising | $0.82
+3 LINK/USDT | RSI=42 | EMA bull cross | $14.20
+2 SOL/USDT | RSI=55 | BB support | $86.50
-3 ETH/USDT | RSI=79 | Overbought | $1,990
-4 XRP/USDT | RSI=83 | MACD death cross | $1.45
```

## Usage
```
Use binance-watchlist to find the best trade setup right now

Use binance-watchlist to scan all 20 pairs and rank signals

Use binance-watchlist for the top 3 buy opportunities
```

## Speed
~30 seconds for full watchlist scan. No API key needed.
