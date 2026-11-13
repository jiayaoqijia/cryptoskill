---
name: crypto-option-margin
domain: crypto-trading/crypto-option-margin
trigger: "Computing margin and liquidation risk on a short crypto option."
anti_trigger: "Not for venue diligence, and not for predicting the underlying."
scope: "Margin, portfolio offsets, and the liquidation of short options."
status: seedling
---

# Crypto option margin

## Standard

A short option on a crypto venue is margined, and the margin is computed against the position's risk rather than its premium. Venues differ in how they model that risk: some use a fixed percentage of notional, some a scenario-based methodology that accounts for offsets across a portfolio, and some require the full collateral for a cash-secured put. The differences are large enough that the same position can be safe on one venue and liquidatable on another.

Liquidation is the consequence. Because crypto markets trade continuously and can gap, a short option can move from comfortably margined to under-margined within minutes, and the venue will close the position at whatever price is available. The record should state the liquidation price or the collateral shortfall scenario, computed from the venue's own methodology.

Primary sources: <https://www.cftc.gov/> and <https://www.bis.org/>.

## Decision rules

- Record the venue's margin methodology and whether portfolio offsets apply.
- Record the collateral posted and its currency.
- Compute the underlying move that would trigger a margin call or liquidation.
- Record the buffer between the current price and that level.
- Record the venue's liquidation procedure and its fees.
- Record the effect of a fall in the collateral currency on the margin ratio.

## Procedure

1. Record the methodology from the venue's documentation.
2. Record collateral and its currency.
3. Compute the liquidation level at the current position size.
4. Record the buffer as a percentage move.
5. Record the liquidation procedure.
6. Recompute after any material move.

## Anti-patterns

- Assuming equity-option margin rules apply.
- Ignoring portfolio offsets that a different position would change.
- Measuring the buffer in premium rather than in underlying move.
- Forgetting the collateral currency's own volatility.
- Leaving the liquidation price uncomputed.

## Done checklist

- [ ] Methodology recorded.
- [ ] Collateral recorded.
- [ ] Liquidation level computed.
- [ ] Buffer recorded as a percentage move.
- [ ] Procedure recorded.
- [ ] Recomputation trigger set.

The methodology also changes with the portfolio: adding an offsetting position can reduce margin on one venue and increase it on another, so the same set of trades has different risk depending on where it is held, and a hedge that is capital-efficient in one account can be forced into liquidation in another. The record should name the venue whose rules it uses.


## Sources

- Regulatory guidance on crypto derivatives: <https://www.cftc.gov/>
- Margin and collateral standards: <https://www.bis.org/>
- Investor education on margin risk: <https://www.investor.gov/introduction-investing>
