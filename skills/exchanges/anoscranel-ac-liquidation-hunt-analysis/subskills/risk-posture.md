---
name: "risk-posture"
domain: "crypto-trading/risk-posture"
trigger: "When asked about risk posture in liquidation analysis"
anti_trigger: "When conducting unrelated trading tasks or general market research"
scope: "risk posture analysis for derivative liquidation events"
status: "seedling"
---

# Risk Posture

## Standard

Risk posture establishes the disciplined operational framework that survives empirical falsification testing in volatile derivatives markets. Because liquidation hunts cannot be reliably detected in real time and cascade timing is fundamentally unpredictable, traders and analysts must shift from speculative prediction to robust defensive engineering. This leaf defines surviving risk practices, including gap-based sizing anchored by empirical judgment parameters (such as a 4.4% calm-book volatility baseline), stop-loss and invalidation placement outside known leverage clustering zones, and conservative leverage bands that maintain generous liquidation distance.

The primary objective of a surviving risk posture is survival under worst-case structural execution conditions. High leverage (e.g., 100x at 0.5% maintenance margin) places liquidation thresholds dangerously close to current entry prices, ensuring that routine intraday noise triggers compulsory closure. Conversely, structured moderation (e.g., 10x to 25x leverage bands) distances the liquidation price from immediate price fluctuations, aligning position survival with multi-day structural invalidation levels rather than minute-to-minute wick anomalies.

Additional public source for the claims here: <https://arxiv.org/abs/2608.03616>.

Primary public sources for the claims here: <https://arxiv.org/abs/2608.03616>.

## Decision rules

- Rule 1: Size positions based on structural price gaps rather than arbitrary technical indicators, utilizing empirical baseline anchors such as the 4.4% calm-book volatility metric (⚠️ calibrated under stable liquidity conditions).
- Rule 2: Place stop-loss and structural invalidation orders safely outside known leverage clustering and liquidity void zones to prevent premature triggering by routine market noise.
- Rule 3: Enforce conservative leverage bands (10x to 25x maximum) that maintain substantial distance between entry prices and maintenance margin liquidation thresholds ($P_{liq}$).
- Rule 4: Adhere strictly to the analytical refusal list: never generate timing predictions, never assert directional price bias, and never market any product claiming to detect real-time "liquidation hunts."

## Procedure

1. Calculate maximum allowable position size based on portfolio capital and structural gap distance to invalidation levels.
2. Verify that proposed leverage multipliers place liquidation prices well beyond expected multi-standard-deviation market wicks.
3. Audit planned stop-loss placements against historical liquidation heatmaps and order book depth profiles to avoid dense clustering areas.
4. Review proposed analytical outputs to ensure strict compliance with non-predictive, analytical-only boundaries.
5. Archive risk posture parameters in standardized trade discipline logs in accordance with institutional governance standards.

## Anti-patterns

- Anti-pattern: Utilizing high leverage (50x–100x) under the assumption that tight stop-losses protect against liquidation. In fast markets, engine execution lag and slippage bypass stops while triggering liquidations.
- Anti-pattern: Placing stop-loss orders exactly at obvious technical support or resistance levels where liquidation clusters naturally congregate.
- Anti-pattern: Violating analytical boundaries by issuing directional trade calls disguised as liquidation hunt analysis.

## Done checklist

- [ ] Gap-based sizing framework and 4.4% calm-book volatility anchor established.
- [ ] Stop-loss placement guidelines relative to leverage clusters defined.
- [ ] Conservative leverage bands (10x–25x) contrasted with extreme leverage risks.
- [ ] Explicit refusal list (no timing, no direction, no hunt detectors) enforced.
- [ ] Zero trading recommendations or return claims included.

## Sources

- Jorion, P. (2006). *Value at Risk: The New Benchmark for Managing Financial Risk*. McGraw-Hill Education. ⚠️ cited without URL.
- Hull, J. C. (2017). *Risk Management and Financial Institutions*. John Wiley & Sons. ⚠️ cited without URL.
- Reference: <https://arxiv.org/abs/2608.03616>
