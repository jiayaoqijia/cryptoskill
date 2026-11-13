---
name: risk-budgeting-across-strategies
domain: crypto-trading/risk-budgeting-across-strategies
trigger: "allocate risk across strategies, risk budget, loss at invalidation"
anti_trigger: "capital allocation, per trade sizing, single strategy backtest"
scope: Allocating risk by loss-at-invalidation rather than capital across strategies.
status: seedling
---

# Risk Budgeting Across Strategies

## Standard

Risk budgeting dictates that portfolio capital must be distributed according to the maximum potential loss at invalidation rather than nominal capital allocation. In crypto trading, allocating equal capital across a high-frequency market-making strategy, a directional momentum strategy, and a basis trading strategy creates severe hidden risk imbalances if volatility and leverage differ. A risk budget establishes a fixed percentage of total portfolio equity that can be lost if every active strategy hits its pre-defined invalidation stop simultaneously. By establishing explicit risk limits per strategy, portfolio managers prevent high-leverage or high-volatility trading systems from dominating overall portfolio volatility during turbulent market regimes.

Primary sources for the claims here: <https://www.iosco.org/library/pubdocs/pdf/IOSCOPD735.pdf> and <https://www.cfainstitute.org/>.

## Decision rules

- Every active strategy must operate under a strict, pre-committed dollar risk limit defined as the exact loss incurred when all active positions hit their thesis invalidation prices.
- Total portfolio risk across all concurrent active strategies must not exceed the maximum aggregate drawdown threshold established by the overarching portfolio risk mandate.
- Capital allocation must adjust dynamically based on strategy risk density; high-leverage strategies receive smaller capital allocations to maintain identical risk contributions across the portfolio.
- Strategy additions or scaling decisions require available capacity within the existing portfolio risk budget without expanding total aggregate risk limits.

## Procedure

1. Calculate the maximum potential capital loss for each individual strategy if all current positions reach their pre-determined invalidation stops simultaneously.
2. Sum the individual strategy risk contributions to verify total portfolio exposure against the aggregate risk cap.
3. Scale down capital allocations for strategies exhibiting higher volatility, greater leverage, or tighter invalidation thresholds until risk contributions equalize.
4. Monitor real-time risk utilization against the allocated budget continuously during active trading sessions across all venues.
5. Freeze new trade entries for any strategy exceeding its allocated risk budget until positions are closed or overall risk is reduced.

## Anti-patterns

- Allocating capital equally across disparate strategies without evaluating leverage, volatility, or stop-loss distance.
- Treating unrealized trading profits as available risk budget expansion during high-volatility market events.
- Failing to define a clear, enforceable invalidation price for every active position within a running strategy.

## Done checklist

- [ ] All active strategies have explicit dollar-risk limits tied directly to invalidation stops.
- [ ] Aggregate portfolio risk sum equals or is less than the mandated risk ceiling.
- [ ] Capital allocations reflect risk contribution parity rather than nominal balance equality.

## Sources

- Risk Management Association: https://www.rmahq.org/
- International Organization of Securities Commissions (IOSCO): https://www.iosco.org/library/pubdocs/pdf/IOSCOPD735.pdf
- Financial Stability Board (FSB): https://www.fsb.org/
- CFA Institute: https://www.cfainstitute.org/
