---
name: "folklore-audit"
domain: "crypto-trading/folklore-audit"
trigger: "When asked about folklore audit in liquidation analysis"
anti_trigger: "When conducting unrelated trading tasks or general market research"
scope: "folklore audit analysis for derivative liquidation events"
status: "seedling"
---

# Folklore Audit

## Standard

Folklore audit provides systematic empirical pushback against unverified retail trading myths surrounding liquidation hunts. In high-volatility digital asset markets, analytical software vendors and community commentators frequently promote indicators that lack peer-reviewed validation or rigorous backtesting. This leaf evaluates four major folklore claims: liquidation heatmaps, cumulative volume delta (CVD), top-trader long/short ratios, and the pervasive "95% fake volume" trope. Each claim is subjected to an empirical standards audit to separate marketing folklore from verifiable market microstructure reality. Public evidence anchors the audit: measured wash-trading rates (<https://arxiv.org/abs/2108.10984>) and vendor documentation that heatmaps are estimates, not resting orders (<https://coinglass.com/LiquidationHeatMap/BTC>).

The persistence of trading folklore stems from confirmation bias and survivorship heuristics. Retail participants observe a price bounce following a liquidity cluster and infer intentional market maker predation. However, systematic testing reveals that most claimed edge indicators fail basic falsification hurdles when exposed to randomized placebo controls and out-of-sample datasets.

## Decision rules

- Rule 1: Reject liquidation heatmaps as standalone predictive triggers. Heatmaps display historical aggregate leverage estimates based on static assumptions; they have not been validated by peer-reviewed studies and require rigorous out-of-sample testing before any operational reliance (evaluation was scheduled for 2026-11-08; confirm whether it ran before relying on the result).
- Rule 2: Treat cumulative volume delta (CVD) divergence as descriptive context rather than mechanical signal. While CVD attempts to measure aggressive buying versus selling pressure, unverified CVD spikes frequently occur inside noise bands without generating directional continuation.
- Rule 3: Discount top-trader long/short position ratios as contradictory and noisy sentiment metrics. Different venues define "top traders" via varying account sizes or margin thresholds, rendering cross-platform aggregation unreliable and historically uncorrelated with subsequent price turning points.
- Rule 4: Discard stale estimates of "95% fake volume" as generalized market descriptors. While historical wash trading plagued unregulated venues, modern top-tier derivative exchanges enforce strict surveillance, making blanket volume skepticism analytically unhelpful.

## Procedure

1. Identify the specific indicator or heuristic claimed to predict liquidation hunts (e.g., liquidation cluster proximity, aggressive delta divergence).
2. Check whether the indicator has undergone peer-reviewed out-of-sample testing or pre-registered falsification trials.
3. Test the indicator against randomized placebo price series to determine if apparent success rates exceed random chance.
4. Evaluate data vendor access constraints and pricing tiers to ensure analytical conclusions do not rely on unverified proprietary feeds.
5. Document the audit verdict in analytical notes, categorizing the metric as folklore, descriptive context, or verified mechanical input.

## Anti-patterns

- Anti-pattern: Treating a graphical liquidation heatmap level as a magnetic price target where market makers actively hunt stops. Price moves toward liquidity because order books thin out, not due to malicious intent.
- Anti-pattern: Assuming that positive CVD guarantees immediate upward continuation. Aggressive market orders often absorb resting liquidity without altering structural supply and demand balance.
- Anti-pattern: Accepting vendor claims of proprietary predictive indicators without inspecting their underlying mathematical assumptions and false-positive rates.

## Done checklist

- [ ] Four folklore claims (heatmaps, CVD, ratios, volume) explicitly audited.
- [ ] Heatmap evaluation status checked against the 2026-11-08 date.
- [ ] Placebo testing requirement and false-positive controls established.
- [ ] Vendor pricing and data access realities factored into evaluation.
- [ ] Zero predictive edges or trading recommendations asserted.

## Sources

- Lyons, R. K. (2001). *The Microstructure Approach to Exchange Rates*. MIT Press. ⚠️ cited without URL.
- Hasbrouck, J. (2007). *Empirical Market Microstructure: The Institutions, The Prices, And The Finances*. Oxford University Press. ⚠️ cited without URL.
- Cong, L. W., Li, X., Tang, K., & Yang, Y. (2021). Crypto Wash Trading. arXiv:2108.10984: <https://arxiv.org/abs/2108.10984>
- Coinglass, Liquidation Heatmap — vendor documentation of the estimate mechanics: <https://coinglass.com/LiquidationHeatMap/BTC>
