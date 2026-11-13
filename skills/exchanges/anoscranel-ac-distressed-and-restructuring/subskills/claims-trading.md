---
name: claims-trading
domain: investing/claims-trading
trigger: "Trading claims in a distressed situation and settling the resulting book."
anti_trigger: "Not for legal advice, and not for predicting a plan outcome."
scope: "Buying and selling claims, trade claims, assignment, and the settlement of a book."
status: seedling
---

# Claims trading

## Standard

A claim in a bankruptcy is an asset that can be bought and sold, and a market exists for both bond claims and trade claims. The economics are the same as any purchase — price against expected recovery — but the mechanics are not: the buyer takes an assignment of the claim, becomes a creditor of record, and inherits the claim's defects, including disputes over its amount, its documentation, and whether it has been impaired by prior conduct.

The practical risks are specific. A trade claim may be disputed, may be subject to a preference period challenge, or may carry a recoupment defence that reduces its value. A bond claim settles through the depository and is cleaner, but its price reflects the market's view of recovery, which is the same view the buyer has. In either case, the buyer's position in the voting classes and in the plan negotiation changes with the purchase.

Primary sources: <https://www.uscourts.gov/> and <https://www.sec.gov/edgar/search/>.

## Decision rules

- Record the claim type: bond claim, trade claim, or other.
- Record the face amount and the purchase price, and the implied recovery.
- Record any dispute, preference exposure, or counterclaim affecting the claim.
- Record the transfer mechanics and whether the court or the agent must approve.
- Record the voting class the claim falls into and the voting implications.
- Record the settlement date and the accrual of interest or fees.

## Procedure

1. Identify the claim and its documentation.
2. Record face, price, and implied recovery.
3. Check for disputes and preference exposure.
4. Record the transfer process and approvals required.
5. Record the voting class and the plan implications.
6. Write the trade record with the defects noted.

## Anti-patterns

- Pricing a trade claim as if it were undisputed.
- Ignoring preference-period exposure that could claw back value.
- Forgetting that the transfer may need court approval.
- Overlooking the voting rights the claim carries.
- Treating a bond claim's price as the recovery itself.

## Done checklist

- [ ] Claim type and documentation recorded.
- [ ] Face, price, and implied recovery recorded.
- [ ] Disputes and preference exposure checked.
- [ ] Transfer mechanics recorded.
- [ ] Voting class recorded.
- [ ] Settlement and accrual recorded.

## Sources

- Court information on claims process: <https://www.uscourts.gov/>
- Filing search for claims registers: <https://www.sec.gov/edgar/search/>
- Statutory reference: <https://www.law.cornell.edu/>
