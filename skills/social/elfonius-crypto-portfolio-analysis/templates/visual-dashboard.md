# Visual Dashboard / Chart Pack

**As of:** {{AS_OF}}  
**Base currency:** {{BASE_CURRENCY}}  
**Data coverage:** {{DATA_COVERAGE}}  
**Mode:** Full Review  
**Benchmark:** {{BENCHMARK}}

> One chart = one finding. Exact numbers live in tables; charts explain the trade-off.

## 1. Chart index

| ID | Chart | Question it answers | Decision it supports | Source |
|---|---|---|---|---|
| V1 | Allocation | What do I own? | Concentration review | {{SOURCE_V1}} |
| V2 | Concentration vs limits | Is any limit breached? | Rebalance / review | {{SOURCE_V2}} |
| V3 | Cluster map | Is diversification real? | Cluster cap | {{SOURCE_V3}} |
| V4 | Performance vs benchmark | Did the portfolio beat its benchmark? | Keep / change | {{SOURCE_V4}} |
| V5 | Drawdown | How bad was the downside? | Risk tolerance | {{SOURCE_V5}} |
| V6 | Risk-return / risk contribution | Where is the risk coming from? | Risk budget | {{SOURCE_V6}} |
| V7 | Correlation heatmap | Are assets independent? | Diversification | {{SOURCE_V7}} |
| V8 | Liquidity ladder | Can I exit at size? | Liquidity plan | {{SOURCE_V8}} |
| V9 | Scenario tornado | What happens in a shock? | Stress limit | {{SOURCE_V9}} |
| V10 | Tokenomics / DeFi health | Is value captured and safe? | Position review | {{SOURCE_V10}} |

## 2. Chart specifications

### V1 — Allocation

- **Finding:** {{V1_FINDING}}
- **Type:** horizontal bars, sorted descending.
- **Data:** weights and values; cluster totals in a second panel.
- **Annotation:** top-1 and top-2 weights.
- **Limit:** {{V1_LIMIT}}
- **Caption:** “Weights as of {{AS_OF}}; cluster totals count shared dependencies once.”
- **What it does not show:** liquidity, cost basis, or future returns.

### V2 — Concentration vs limits

- **Finding:** {{V2_FINDING}}
- **Type:** bullet bars for top-1, top-2, top-3, largest cluster.
- **Annotation:** excess over the policy limit.
- **Caption:** “Limits are policy inputs, not universal advice.”

### V3 — Cluster map

- **Finding:** {{V3_FINDING}}
- **Type:** stacked horizontal bar or treemap.
- **Annotation:** shared chain/stablecoin/bridge/oracle.
- **Caption:** “Different tickers can share one failure path.”

### V4 — Performance vs benchmark

- **Finding:** {{V4_FINDING}}
- **Type:** growth of 100 or cumulative TWR; benchmark line.
- **Annotation:** excess return and window.
- **Caption:** “{{RETURN_BASIS}}; window {{WINDOW}}; no annualization under one year.”

### V5 — Drawdown

- **Finding:** {{V5_FINDING}}
- **Type:** underwater curve.
- **Annotation:** peak, trough, recovery.
- **Caption:** “Daily marks; stale prices can understate the drawdown.”

### V6 — Risk-return / risk contribution

- **Finding:** {{V6_FINDING}}
- **Type:** scatter (volatility vs return) or risk-contribution bars.
- **Annotation:** largest risk contributor.
- **Caption:** “Window {{RISK_WINDOW}}; past risk is not a forecast.”

### V7 — Correlation heatmap

- **Finding:** {{V7_FINDING}}
- **Type:** annotated heatmap, clustered order.
- **Annotation:** highest pairwise correlation.
- **Caption:** “Window {{CORR_WINDOW}}; correlation is not causation and can shift in stress.”

### V8 — Liquidity ladder

- **Finding:** {{V8_FINDING}}
- **Type:** horizontal bars of exit days at 1%, 5%, 10%; stressed case lighter.
- **Annotation:** first position above the mandate window.
- **Caption:** “Executable venue volume, not market cap.”

### V9 — Scenario tornado

- **Finding:** {{V9_FINDING}}
- **Type:** bars of P&L impact; zero baseline; reverse-stress marker.
- **Annotation:** first breached limit.
- **Caption:** “Modeled shocks, not probabilities.”

### V10 — Tokenomics / DeFi health

- **Finding:** {{V10_FINDING}}
- **Type:** supply/unlock area or health-factor bar with liquidation line.
- **Annotation:** next unlock or distance to liquidation.
- **Caption:** “Source {{SOURCE_V10}}; not a guarantee of value capture or safety.”

## 3. Visual QA

- [ ] Every chart has a finding title, not a topic title.
- [ ] Units, currency, as-of date, source, and window are visible.
- [ ] Bars start at zero; log axes are labeled.
- [ ] No 3D, no pie with more than five slices, no unlabeled dual axis.
- [ ] Color is not the only distinction; grayscale works.
- [ ] Exact values are in a table, not only in the chart.
- [ ] Modeled or estimated data is labeled.
- [ ] The visual pack is shorter than the argument.

## 4. Files

- `charts/V1-allocation.png`
- `charts/V2-concentration.png`
- `charts/V3-clusters.png`
- `charts/V4-performance.png`
- `charts/V5-drawdown.png`
- `charts/V6-risk-return.png`
- `charts/V7-correlation.png`
- `charts/V8-liquidity.png`
- `charts/V9-scenarios.png`
- `charts/V10-tokenomics-defi.png`

> A chart pack is not a substitute for the IPS-lite, source table, or decision record.
