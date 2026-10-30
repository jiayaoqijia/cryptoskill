# 13 — Visualization and Charts

## Purpose

Charts are evidence, not decoration. A portfolio report needs a small visual pack that makes concentration, risk, liquidity, and scenarios legible without hiding uncertainty.

## Inputs

- Chart question and the decision it supports.
- Position, return, price, liquidity, or scenario data.
- Source, timestamp, window, unit, and currency.
- Policy limits or mandate thresholds.

## Method

1. Choose the chart type from the selection matrix.
2. Validate the data and denominator.
3. Render at the required size; label units and source/date.
4. Annotate the one finding the reader must see.
5. Check grayscale, colorblind, and small-size readability.
6. Record the limitation and the table that carries exact values.

## Rules

1. **One chart, one question.** If the title is a topic (“Risk”), rewrite it as a finding (“Top-2 is 76% of value”).
2. **A table is better for exact values.** Use charts for comparison, shape, and trade-offs; use tables for numbers a reader must copy.
3. **Every chart carries:** title, unit, as-of timestamp, source, sample/window, and a one-line “what it shows / what it does not.”
4. **No 3D, no pie with more than five slices, no dual axes unless the second axis is essential and labeled.**
5. **Bars start at zero.** Use a log scale only for long-tailed liquidity or price history, and label it.
6. **Do not truncate an axis to exaggerate a move.** If a truncated axis is necessary, annotate it.
7. **Color is secondary.** Use labels, position, and line style; ensure grayscale readability.
8. **Show uncertainty.** Use ranges, scenario bands, or footnotes; do not draw a single forecast line as fact.
9. **Do not mix definitions.** Revenue, fees, emissions, incentives, and tokenholder value never share an unlabeled axis.
10. **Small multiples beat a crowded chart.** If more than 8–10 series, facet or aggregate.

## Chart selection matrix

| Question | Chart | Avoid |
|---|---|---|
| What do I own? | Horizontal bar with weights; stacked bar for clusters | Donut/pie with many slices |
| Is concentration above policy? | Bullet bars: value vs limit | A single “risk score” |
| Is diversification real? | Cluster stacked bar; correlation heatmap | Counting tickers |
| Did I beat the benchmark? | Growth of 100 / cumulative TWR; excess return | Price-only line with no cash flows |
| How bad was the drawdown? | Underwater curve; peak/trough annotation | A single “max DD” number only |
| What is the risk-return trade-off? | Scatter: volatility vs return, bubble = weight | 3D scatter |
| Can I exit? | Liquidity ladder: exit days normal vs stressed, log x | Market-cap bar |
| What happens in a shock? | Tornado/waterfall of P&L by position | A table with no visual priority |
| Is supply diluting me? | Supply/unlock area; emissions vs buyback | Mixing supply and price on one axis |
| Is the DeFi position safe? | Health-factor bar with liquidation line | A green “safe” badge |
| What changed? | Small multiples of thresholds; delta bars | A new full report every time |

## Mandatory visual pack

### Quick Screen (3 charts)

1. Allocation bar with policy limits.
2. Top-1/top-2/top-3 vs limits.
3. Risk snapshot: volatility/CVaR vs limits, or a simple scenario bar.

### Full Review (6–10 charts)

1. Allocation and cluster map.
2. Concentration vs limits.
3. Performance vs benchmark (TWR, net of fees where available).
4. Drawdown / underwater curve.
5. Risk-return scatter or risk-contribution bar.
6. Correlation heatmap.
7. Liquidity ladder (normal vs stressed).
8. Scenario tornado/waterfall.
9. Tokenomics/unlock chart for the largest token exposure.
10. DeFi health/liquidation chart, if material.

### Monitoring (2 charts)

1. Weight change since the prior snapshot.
2. Threshold dashboard: current vs limit for the top five risks.

## Chart specifications

### 1. Allocation

- Horizontal bars, sorted descending; weight labels; policy limit line.
- Cluster total in a second panel or a stacked bar.
- Caption: “Weights as of [date]; cluster totals count shared dependencies once.”

### 2. Concentration vs limits

- Three or four bullet bars: top-1, top-2, top-3, largest cluster.
- Mark the policy limit; color the excess, not the whole bar.
- Caption: “Policy limits are from the IPS-lite, not universal advice.”

### 3. Performance vs benchmark

- Growth of 100 or cumulative TWR; benchmark line; excess return annotation.
- State whether returns are gross/net and whether cash flows are handled.
- Do not annualize a period under one year.

### 4. Drawdown

- Underwater curve; annotate peak, trough, recovery (or “not recovered”).
- Use the same window as the performance chart.

### 5. Risk-return

- X = annualized volatility; Y = annualized return; bubble = weight.
- Label only material positions; use a table for the rest.
- State the window and that past risk is not a forecast.

### 6. Correlation heatmap

- Annotated values; diverging palette; order by cluster or similarity.
- State the window and regime; do not imply causation.
- If more than 12 assets, aggregate or facet.

### 7. Liquidity ladder

- Horizontal bars of exit days at 1%, 5%, and 10% participation; stressed case as a lighter bar.
- Log x-axis if long-tailed; label the threshold.
- Caption: “Exit days use executable venue volume, not global market cap.”

### 8. Scenario tornado/waterfall

- Bars of P&L impact by scenario or by position within a scenario.
- Start at zero; loss is negative, gain positive; label the sign.
- Add a reverse-stress marker at the mandate loss floor.

### 9. Tokenomics/unlocks

- Supply over time; unlock cliff; emissions vs buyback/burn in the same unit.
- Separate price from supply; do not put price on the supply axis.
- Label the source and the next unlock date.

### 10. DeFi health

- Health factor bar with a liquidation line at 1.0; show distance to liquidation.
- Add oracle and collateral labels; do not call a position “safe.”
- If health factor is unavailable, show `not assessable`.

## Data and QA

For every chart, record:

| Field | Required |
|---|---|
| Chart ID | V1, V2, … |
| Question | The decision the chart supports |
| Data | Positions, returns, prices, or scenario outputs |
| Source | URL/API/export and timestamp |
| Window | Dates, frequency, currency |
| Transform | Weight, cumulative, log, index |
| Annotation | The one number or event the reader should see |
| Limitation | What the chart cannot show |

## Design standard

- Background: white or transparent; no gradient.
- Palette: navy `#0B1220`, teal `#2A9D8F`, amber `#E9C46A`, coral `#E76F51`, slate `#6C7A89`; use at most four series colors.
- Font: one sans-serif family; 10–12 pt labels; 14–16 pt title.
- No top/right spines; light horizontal grid only.
- Source/date footer on every chart.
- Export at 200–220 dpi or vector; inspect at 100% and in grayscale.
- Alt text: one sentence with the finding, not “chart.”

## Anti-patterns

- Pie charts with 10 tokens.
- A “risk score” with no components.
- Price chart with no benchmark or cash-flow treatment.
- Revenue and emissions on one axis without labels.
- A correlation matrix with no window.
- A liquidity chart using market cap.
- A scenario chart with no loss floor.
- A chart that repeats the table instead of explaining it.

## Failure modes

- The title describes the data, not the finding.
- The axis starts at a convenient number, exaggerating a move.
- The chart uses color as the only distinction.
- The source/date is missing.
- The chart is a forecast but is labeled as fact.
- The visual pack is longer than the argument.

## Sources

- CFA Institute, *Overview of the Global Investment Performance Standards* (2026): fair presentation, source/date discipline.
- CFA Institute, *Measuring and Managing Market Risk* (2026): risk charts must state method, window, and limitations.
- This skill’s report templates and examples.
