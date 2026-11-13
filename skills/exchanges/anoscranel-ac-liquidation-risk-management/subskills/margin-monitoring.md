---
name: margin-monitoring
domain: crypto-trading/margin-monitoring
trigger: "Use when setting up pre-trade and daily margin monitoring checks, liquidation distance thresholds, and size-reduction tripwires."
anti_trigger: "Not for calculating initial position geometry, executing post-liquidation recovery, or managing cross-exchange basis."
scope: "The pre-trade and daily checks: liquidation distance vs realised volatility, funding drain, OI shifts, the tripwires that force a size cut."
status: seedling
---

## Standard
Continuous margin monitoring is the primary defense against unexpected liquidation. Professional risk management requires strict pre-trade validation and ongoing daily audits comparing liquidation distance against realized volatility, cumulative funding rate drains, and open interest (OI) shifts. As realized volatility expands, the distance between mark price and liquidation price must widen proportionally to prevent normal price oscillation from triggering margin calls. Cumulative negative funding payments act as a persistent tax that steadily erodes account equity, compressing the liquidation buffer over time. Sudden open interest contractions indicate long or short liquidation flushes that can instantly alter market depth and invalidate current margin assumptions. Pre-established tripwires must force automated or manual position size reductions when risk metrics breach safety bands.

Primary sources for the claims here: <https://www.binance.com/en/support/faq/margin-call-and-liquidation-in-futures-trading-360033516312> and <https://www.okx.com/help/risk-management-rules>.

## Decision rules
1. Establish a mandatory pre-trade checklist requiring liquidation distance to exceed 3x the 24-hour Average True Range (ATR) for the target trading pair.
2. Enforce a daily audit of cumulative funding rate expenses; force a position size reduction if funding drain exceeds 1.5% of total account equity within a 24-hour window.
3. Configure automated Telegram or webhook alerts for any position where the liquidation distance compresses to within 5% of current mark price.
4. Execute immediate position trimming whenever open interest drops by more than 15% within a 4-hour window accompanied by abnormal volume spikes.

## Procedure
1. Run pre-trade calculations comparing planned liquidation distance against current 24h ATR and realized volatility percentiles.
2. Check cumulative funding payments accrued over the preceding funding epochs and factor them into remaining margin equity.
3. Monitor open interest and volume metrics via exchange APIs to detect early warning signs of market-wide deleveraging.
4. Set up multi-tier margin alert thresholds (warning at 10% distance, critical at 5% distance).
5. Execute pre-planned position size cuts immediately upon breaching any tripwire without waiting for market recovery.

## Anti-patterns
- Setting up a trade and never checking the liquidation distance again, assuming market prices will remain stable indefinitely.
- Ignoring cumulative negative funding drain until it silently consumes the entire margin buffer and triggers liquidation.
- Disabling margin alerts during high volatility periods due to notification fatigue.
- Failing to reduce position size when market realized volatility doubles, leaving the position dangerously under-buffered.

## Done checklist
- [ ] Pre-trade liquidation distance verified to exceed 3x 24h ATR.
- [ ] Daily funding drain audited and factored into account equity.
- [ ] Multi-tier margin proximity alerts configured and tested.
- [ ] Open interest velocity monitored for sudden deleveraging signals.
- [ ] Pre-established tripwire size-reduction rules ready for immediate execution.

## Sources
- Binance Risk Management and Margin Call Rules: https://www.binance.com/en/support/faq/margin-call-and-liquidation-in-futures-trading-360033516312
- OKX Risk Management and Position Monitoring Guide: https://www.okx.com/help/risk-management-rules
