# Scenario Analysis

**As of:** {{AS_OF}}  
**Base currency:** {{BASE_CURRENCY}}  
**Data coverage:** {{DATA_COVERAGE}}  
**Portfolio value:** {{TOTAL_VALUE}}

## 1. Scenario definitions

| Scenario | Type | Shocks | Rationale | Source |
|---|---|---|---|---|
| Risk-off | Hypothetical | BTC −30%, ETH −40%, alts −50% to −70% | Broad de-risking | {{SOURCE}} |
| Stablecoin depeg | Hypothetical | 5% and 20% depeg; redemption gate | “Cash” is not cash | {{SOURCE}} |
| Bridge/chain halt | Hypothetical | 7-day pause; wrapped-asset discount | Exit/custody failure | {{SOURCE}} |
| Correlation → 1 | Hypothetical | All risky assets move together | Diversification failure | {{SOURCE}} |
| Liquidity haircut | Hypothetical | 25% of normal volume | Forced-sale loss | {{SOURCE}} |
| Reverse stress | Modeled | {{REVERSE_SHOCKS}} | Find mandate breach | {{SOURCE}} |

## 2. Results

| Scenario | Portfolio loss | % | Worst position | Contribution | First breached limit |
|---|---:|---:|---|---:|---|
| Risk-off | {{LOSS_1}} | {{PCT_1}} | {{WORST_1}} | {{CONTRIB_1}} | {{BREACH_1}} |
| Depeg | {{LOSS_2}} | {{PCT_2}} | {{WORST_2}} | {{CONTRIB_2}} | {{BREACH_2}} |
| Bridge halt | {{LOSS_3}} | {{PCT_3}} | {{WORST_3}} | {{CONTRIB_3}} | {{BREACH_3}} |
| Correlation → 1 | {{LOSS_4}} | {{PCT_4}} | {{WORST_4}} | {{CONTRIB_4}} | {{BREACH_4}} |
| Liquidity haircut | {{LOSS_5}} | {{PCT_5}} | {{WORST_5}} | {{CONTRIB_5}} | {{BREACH_5}} |
| Reverse stress | {{LOSS_6}} | {{PCT_6}} | {{WORST_6}} | {{CONTRIB_6}} | {{BREACH_6}} |

## 3. Interpretation

- **Largest vulnerability:** {{LARGEST_VULNERABILITY}}
- **First position to fail:** {{FIRST_FAILURE}}
- **What the portfolio can absorb:** {{ABSORB}}
- **What it cannot absorb:** {{CANNOT_ABSORB}}

## 4. Assumptions and limits

- Correlations: {{CORRELATION_ASSUMPTION}}
- Liquidity: {{LIQUIDITY_ASSUMPTION}}
- Stablecoin redemption: {{REDEMPTION_ASSUMPTION}}
- Modeled outputs are not probabilities: {{MODEL_NOTE}}

## 5. Falsifiers

{{FALSIFIERS}}

> Scenarios are conditional exercises, not forecasts. Reverse stress is not a probability estimate.
