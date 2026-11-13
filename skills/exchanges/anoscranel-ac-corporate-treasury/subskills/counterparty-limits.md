---
name: counterparty-limits
domain: investing/counterparty-limits
trigger: "Reading how a company limits exposure to banks and derivative counterparties."
anti_trigger: "Not for assessing a bank's credit, and not for recommending a security."
scope: "Deposit and derivative counterparty limits, and concentration in a stress."
status: seedling
---

# Counterparty limits

## Standard

A treasury that holds cash with banks and enters derivatives with them is exposed to their failure, and the policy that governs that exposure is a limit structure rather than a credit opinion. The limits specify how much can sit with any one institution, which institutions are eligible and on what rating, and how the exposure is measured when derivatives are marked to market.

The measurement detail is where the discipline lives. A deposit is straightforward; a derivative's exposure is its replacement cost, which rises when the contract moves in the company's favour and can exceed the notional's apparent smallness. A policy that counts derivative exposure at zero because the notional is notionally matched is not measuring the risk that appears exactly when a counterparty fails.

Primary sources: <https://www.bis.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the eligibility criteria for counterparties, including minimum ratings and any diversification requirement.
- Record the maximum exposure per counterparty, as an amount and as a percentage of the buffer.
- Record how derivative exposure is measured: notional, mark-to-market, or potential future exposure.
- Record any collateral arrangements that reduce exposure.
- Record the aggregate exposure to the banking sector, which concentrates in a stress.
- Record how limits are monitored and by whom.

## Procedure

1. Read the treasury policy's counterparty section.
2. Record eligibility criteria and rating floors.
3. Record the limit structure per counterparty and in aggregate.
4. Record the exposure measurement method for derivatives.
5. Record collateral and netting arrangements.
6. Write the assessment with the concentration stated.

## Anti-patterns

- Measuring derivative exposure at notional rather than replacement cost.
- Applying the same limit to a deposit and to an uncollateralised derivative.
- Assuming rating floors protect against a rapid downgrade.
- Ignoring concentration across banks that share a funding model.
- Treating netting as effective without a legal opinion on enforceability.

## Done checklist

- [ ] Eligibility criteria recorded.
- [ ] Per-counterparty limits recorded.
- [ ] Derivative exposure method recorded.
- [ ] Collateral arrangements recorded.
- [ ] Sector concentration recorded.
- [ ] Monitoring responsibility recorded.

The concentration that matters most is not per name but per funding model: banks that rely on the same wholesale funding, or that share a common exposure to a single market, can fail together, and limits measured name by name will show a diversified book while the stress arrives as one event. Grouping counterparties by funding dependency is the limit that survives a crisis.


## Sources

- Counterparty and collateral standards: <https://www.bis.org/>
- Corporate disclosure of treasury arrangements: <https://www.sec.gov/investor>
- Investor education on counterparty risk: <https://www.investor.gov/introduction-investing>
