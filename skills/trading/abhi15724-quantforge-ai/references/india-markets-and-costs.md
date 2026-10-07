# Indian Markets and Costs

Never apply US conventions. **Rates, lot sizes, expiry days, margin rules and tax treatment change by exchange/regulator circular and Budget. Verify the current value by web search or ask the user; do not rely on memory.** Store verified values in `config/costs.yaml` with a date and source.

## Always specify
- Segment: cash, equity futures, index futures, equity options, index options, currency derivatives, commodity (MCX)
- Trading session and pre-open/closing behaviour for that segment
- Current lot size, tick size, expiry cycle and expiry weekday for the exact contract
- Margin: SPAN + exposure, intraday rules, MIS vs NRML
- Settlement (cash vs physical), exercise style, ITM-expiry risk for stock options
- F&O eligibility/ban list changes, circuit limits, price bands

## Cost model fields (per leg)
Brokerage, STT/CTT, exchange transaction charge, SEBI turnover fee, stamp duty, GST (on brokerage + charges), DP charges (delivery sell), slippage (spread-based, size-aware), impact when size is a meaningful fraction of displayed depth. Tax treatment of P&L depends on the user's situation: flag it, suggest a tax professional, do not compute liability as advice.

Use `scripts/metrics.py --cost-bps` for flat round-trip cost sensitivity; compute exact per-trade costs from the verified config.

## Indian-specific cautions
Expiry-day gamma and pinning, weekly-expiry volume concentration, STT on exercised options, liquidity concentrated near ATM and in index options, F&O inclusion/exclusion, event gaps (RBI, Budget, results, global overnight), circuit-hit illiquidity, broker API rate/modification limits, and exchange/broker rules for algorithmic and API trading (verify current rules before any live automation).
