---
name: report-impermanent-loss-vs-holding
description: Use when reporting impermanent loss, comparing an LP position to simply holding, or back-testing a pool: computes divergence loss from the price ratio with worked examples at 2x, 5x, and 0.5x moves.
---

# Report impermanent loss vs holding

Impermanent loss is the value gap between providing liquidity and holding the same tokens; it is a function only of the price ratio, not of fees, so it must be shown separately from fee income.

## Procedure

1. Compute the price ratio `k = P_new / P_old` between entry and now (or between two candidate exit points).

2. Use the closed form: `IL = 2*sqrt(k)/(1+k) - 1`, always <= 0.

3. Worked example — enter at 2,000 USDC/ETH, price doubles (k = 2):

   python3 -c "import math; print(2*math.sqrt(2)/3-1)"
   -0.0572

   So IL = -5.72%. At 5x it is `2*sqrt(5)/6-1 = -25.5%`; at 0.5x it is the same -5.72% (IL is symmetric in k and 1/k).

4. Concrete pool check — 100 ETH / 200,000 USDC at price 2,000 (L=4472.1):
   - price 4,000: reserves become `x=70.71 ETH`, `y=282,842.7 USDC`; value = `565,685.4`.
   - HODL is `100*4000 + 200,000 = 600,000`.
   - deficit = `565,685.4 - 600,000 = -34,314.6` = -5.72% of HODL. Consistent with the formula.

5. Compare against fees: only continue if `cumulative_fees > |IL|`. Convert IL to USD with the position size at entry.

6. Report IL both as a percentage and in USD, and always next to the HODL benchmark for the same period — a -5.7% IL that beat HODL by 3% in fees is a gain, a -5.7% IL with 1% fees is a loss.

## Pitfalls

- Calling it "impermanent": if you exit or the ratio persists, the loss is realized. The label is not protection.
- Reporting IL alone without fees or the HODL benchmark — it overstates the loss and hides whether the LP outperformed.
- Using USD return as the ratio: k must be the price ratio of the two tokens, not the dollars in the pool.

## Verification

    python3 -c "import math; k=2; print(2*math.sqrt(k)/(1+k)-1); print((70.710678*4000+282842.71)/600000-1)"
    -0.0572...
    -0.05719...

Both paths agree to four decimals; a mismatch means reserves or the HODL set are wrong.

Report entry ratio, current ratio, IL %, IL in USD, and cumulative fees to date.
