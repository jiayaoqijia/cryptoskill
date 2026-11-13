---
name: tranche-attachment
domain: investing/tranche-attachment
trigger: "Working out which slice of pool losses a tranche actually occupies."
anti_trigger: "Not for predicting pool losses, and not for rating the tranche."
scope: "Attachment, detachment, and the loss window a tranche actually occupies."
status: seedling
---

# Tranche attachment

## Standard

A tranche is defined by two points: the attachment point, where it begins absorbing losses, and the detachment point, where it has absorbed all of its principal. Between those two numbers the tranche is the first-loss piece for its own slice of the pool, and beyond the detachment point the tranche is gone. The width of that window is the tranche's notional.

The language matters when comparing structures. A tranche described as "senior" may attach at twelve percent of the pool in one deal and at thirty percent in another, and the same label therefore describes different risk. The record should state attachment and detachment as percentages of the collateral balance, and convert them into the pool loss that produces a loss of principal, rather than using the label the arranger chose.

Primary sources: <https://www.sec.gov/investor> and <https://www.bis.org/>.

## Decision rules

- Record the attachment point and detachment point as percentages of collateral.
- Record the tranche notional and its thickness.
- Record the pool loss required to reach attachment, and to exhaust the tranche.
- Record whether the points are fixed or move with the collateral balance.
- Record any step-down or replenishment that changes the attachment over time.
- Where the tranche is quoted by rating alone, record the attachment and note the label.

## Procedure

1. Extract attachment and detachment from the capital structure table.
2. Compute the loss window in percentage terms.
3. Record whether the structure amortises or replenishes.
4. Compute the pool loss that exhausts the tranche.
5. Record any mechanism that moves the attachment point.
6. Write the tranche summary in loss terms.

## Anti-patterns

- Using the tranche label as a measure of risk.
- Comparing tranches across deals by label rather than by attachment.
- Assuming the attachment point is static through the deal's life.
- Ignoring replenishment that keeps the pool balance constant.
- Treating the detachment point as the maximum loss on the tranche.

## Done checklist

- [ ] Attachment and detachment recorded.
- [ ] Notional and thickness recorded.
- [ ] Loss window computed.
- [ ] Amortisation or replenishment recorded.
- [ ] Attachment movement recorded.
- [ ] Summary written in loss terms.

The attachment point also interacts with the pooling and servicing agreement's definition of loss: a deal that counts charge-offs gross of recoveries will breach its attachment before one that counts them net, so two tranches with identical printed attachment points can be exposed to different realised loss timing depending on the definition in the document.

## Sources

- Securitisation capital structure disclosure: <https://www.sec.gov/investor>
- Securitisation framework and definitions: <https://www.bis.org/>
- Market data and context: <https://www.federalreserve.gov/>
