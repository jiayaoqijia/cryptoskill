---
name: rating-triggers-in-contracts
domain: investing/rating-triggers-in-contracts
trigger: "Finding the contract terms that a rating level activates."
anti_trigger: "Not for legal advice, and not for predicting a rating change."
scope: "Mandates, covenants, and collateral terms that reference a rating."
status: seedling
---

# Rating triggers in contracts

## Standard

A rating level is a defined term in more contracts than holders realise: loan covenants that price a margin step-up or step-down on a rating, collateral agreements that require additional margin if either party is downgraded, investment mandates that restrict what may be held, and derivative contracts that permit termination on a ratings event. Each of these converts an agency opinion into a contractual obligation.

The practical consequence is that a downgrade can cost money without any change in the issuer's ability to pay. A collateral agreement that requires posting on a two-notch downgrade can force a firm to raise cash at the worst moment, and a mandate restriction can force a sale into a market where everyone else is selling for the same reason. The record should list the triggers a position is exposed to, not just the rating.

Primary sources: <https://www.sec.gov/investor> and <https://www.isda.org/>.

## Decision rules

- Record each contract referencing a rating and the threshold it uses.
- Record the agency whose rating is referenced, since contracts often specify one.
- Record the consequence of breaching each threshold: margin, termination, or restriction.
- Record whether the threshold is symmetric, and if a step-up exists.
- Record the cure or remedy provisions.
- Record the aggregate exposure if several contracts trigger together.

## Procedure

1. Identify contracts referencing ratings.
2. Record the referenced agency and threshold per contract.
3. Record the consequence of each trigger.
4. Record symmetry and step-ups.
5. Record cure provisions.
6. Write the trigger summary with the aggregate exposure.

## Anti-patterns

- Assuming a rating change affects only the bond's price.
- Missing the agency specified in the contract.
- Ignoring asymmetric triggers that bite on downgrade only.
- Treating cure provisions as unlimited.
- Counting each trigger separately without the aggregate.

## Done checklist

- [ ] Contracts and thresholds recorded.
- [ ] Referenced agency recorded.
- [ ] Consequences recorded.
- [ ] Symmetry recorded.
- [ ] Cure provisions recorded.
- [ ] Aggregate exposure written.

A further exposure that is easy to miss is the second-order trigger: a collateral agreement on a derivative may reference the rating of a party whose own rating depends on the rating of an affiliate, so a downgrade at one entity can require posting at another, and the record should trace the chain rather than stop at the first contract.

## Sources

- Contractual and disclosure context: <https://www.sec.gov/investor>
- Derivatives documentation and rating triggers: <https://www.isda.org/>
- Regulatory framework for ratings: <https://www.bis.org/>
