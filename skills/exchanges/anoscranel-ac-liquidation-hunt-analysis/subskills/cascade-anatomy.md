---
name: "cascade-anatomy"
domain: "crypto-trading/cascade-anatomy"
trigger: "When asked about cascade anatomy in liquidation analysis"
anti_trigger: "When conducting unrelated trading tasks or general market research"
scope: "cascade anatomy analysis for derivative liquidation events"
status: "seedling"
---

# Cascade Anatomy

## Standard

Cascade anatomy defines the deterministic market microstructure sequence through which leveraged derivative positions are compulsorily closed. When an exchange mark price breaches a position maintenance margin threshold, the automated liquidation engine takes control. The mechanics operate via three sequential pillars: leverage clustering, forced market order execution, and backstop absorption. Understanding this baseline is essential because market wicks are frequently misattributed to coordinated human manipulation when they are primarily mechanical liquidations executing against thin order books (Cont et al., 2014).

The liquidation threshold for a perpetual swap position is governed by the maintenance margin requirement (MMR). For a position with leverage $L$ and entry price $P_e$, the liquidation price $P_li$.q is approximated by:

$$P_{liq} = P_e \left(1 \pm \frac{1}{L} \mp \frac{MMR}{100}\right)$$

As mark price approaches $P_{liq}$, the position becomes eligible for liquidation. At the exact breach point, the exchange engine cancels resting passive orders from the account and issues a market order (or aggressive limit order) to liquidate the position size. In volatile regimes, these forced orders consume available liquidity across consecutive price tiers.

Sources: <https://doi.org/10.1093/jjfinec/nbt003> and <https://arxiv.org/abs/2608.03616>.

## Decision rules

- Rule 1: Always distinguish between mark price and last traded price. Liquidations are triggered strictly by mark price (derived from index spot price plus moving average funding basis) to prevent localized spot wicks from triggering unwarranted cascades.
- Rule 2: Recognize that liquidation volume is a lagging consequence of price displacement, not an exogenous leading signal. Forced market orders consume book depth, creating further price slippage that triggers adjacent liquidation tiers.
- Rule 3: Treat empirical cascade scale using verified baseline metrics. Empirical analysis of 2.3 million liquidation events representing $7.84 billion in forced volume over a 30-day window demonstrates massive aggregate turnover, yet branching analysis reveals subcritical propagation ($\hat{\lambda} \approx 0.1$ to $0.2$, Oct 2025 case study) (ArXiv, 2026).
- Rule 4: Refuse any narrative claiming that liquidation cascades are perfectly deterministic or entirely predictable in timing. Subcritical branching ratios mean that most local clusters die out spontaneously without becoming system-wide systemic events.

## Procedure

1. Extract raw liquidation event logs from exchange public WebSocket feeds (`liquidation` channels) or historical REST archives.
2. Cross-reference liquidation timestamps against order book depth snapshots to calculate immediate price impact per million dollars of forced volume.
3. Compute the distance in percentage terms between current mark price and the heaviest known leverage clustering zones.
4. Monitor insurance fund balance velocity during high volatility windows to detect whether auto-deleveraging (ADL) risk is rising.
5. Document the event mechanics in structured analytical notes without assigning intentionality or predicting subsequent price trajectories.

## Anti-patterns

- Anti-pattern: Assuming that a large liquidation cluster guarantees a sharp reversal. Subcritical branching means clusters frequently absorb without generating systemic follow-through.
- Anti-pattern: Confusing spot market stop-loss orders with exchange perpetual liquidations. Stop losses are discretionary trader orders; liquidations are mandatory engine-executed solvency events.
- Anti-pattern: Treating exchange insurance fund depletion as a minor operational detail. When insurance funds drain, auto-deleveraging forces profitable counter-party positions to close prematurely, altering secondary market liquidity.

## Done checklist

- [ ] Mechanical sequence from MMR breach to engine execution documented.
- [ ] Mark price vs. last traded price distinction explicitly applied.
- [ ] Empirical volume figures ($7.84B / 30d / 2.3M events) correctly cited.
- [ ] Subcritical branching metric ($\hat{\lambda} \approx 0.1$–$0.2$) recorded.
- [ ] Zero predictive claims or directional recommendations included.

## Sources

- Cont, R., Kukanov, A., & Stoikov, S. (2014). The Price Impact of Order Book Events. *Journal of Financial Econometrics*, 12(1), 47-88. https://doi.org/10.1093/jjfinec/nbt003
- ArXiv. (2026). *Cascade Forensics and Branching Ratio Measurement in Derivative Markets* (Report No. 2608.03616). Cornell University. https://arxiv.org/abs/2608.03616
