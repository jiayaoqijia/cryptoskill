---
name: margin-and-collateral
domain: investing/margin-and-collateral
trigger: "Managing margin calls and collateral eligibility at institutional scale."
anti_trigger: "Not for predicting margin changes, and not for legal advice."
scope: "Initial and variation margin, eligibility, haircuts, and the call process."
status: seedling
---

# Margin and collateral

## Standard

Margin at institutional scale has two components with different purposes. Variation margin settles the current mark-to-market, moving value daily between the parties. Initial margin covers the potential future exposure over the close-out period, and it is posted against a model rather than a realised loss. A position can be fully variation-margined and still require substantial initial margin.

Collateral eligibility and haircuts decide what the posted margin is worth. Cash, government securities, and corporate bonds are accepted at different haircuts, and a haircut is a discount to market value that absorbs price moves between calls. Posting a large amount of an ineligible or high-haircut asset increases the funding requirement even when the notional is unchanged.

Primary sources: <https://www.bis.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the margin methodology and the close-out period it assumes.
- Record variation margin frequency and the dispute process.
- Record initial margin and the model behind it.
- Record eligible collateral and the haircut applied to each type.
- Record the call process: notice, deadline, and the consequence of missing it.
- Record the funding plan for a call and the assets available to meet it.

## Procedure

1. Record the methodology and its parameters.
2. Record current variation and initial margin.
3. Record collateral posted and its haircuts.
4. Record the call process and deadlines.
5. Record the funding plan and the eligible assets.
6. Update after each material move.

## Anti-patterns

- Treating initial margin as a fixed deposit.
- Ignoring haircuts when computing available collateral.
- Assuming a call deadline is negotiable.
- Posting ineligible collateral and expecting it to count.
- Leaving the funding plan unwritten until a call arrives.

## Done checklist

- [ ] Methodology recorded.
- [ ] Margin amounts recorded.
- [ ] Collateral and haircuts recorded.
- [ ] Call process recorded.
- [ ] Funding plan written.
- [ ] Updates scheduled.

A useful discipline is to hold the collateral in more than one form: posting only the asset with the lowest haircut concentrates the position in that asset's market, and a move in its price raises the haircut exactly when more collateral is needed. Diversifying the posted collateral is a risk decision, not an administrative preference.


The funding plan should also name the source of last resort, because margin calls do not wait for a convenient moment and the assets that are eligible are often the same ones the strategy is using for its own collateral elsewhere.


## Sources

- Margin standards for central counterparties: <https://www.bis.org/>
- Market structure context: <https://www.sec.gov/investor>
- Investor education on margin: <https://www.investor.gov/introduction-investing>
