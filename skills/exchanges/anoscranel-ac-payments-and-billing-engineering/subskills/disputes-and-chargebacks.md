---
name: disputes-and-chargebacks
domain: software-engineering/disputes-and-chargebacks
trigger: "Responding to a dispute as a designed evidence-assembly process."
anti_trigger: "Not for fraud screening, and not for the ledger's accounting of the reversal."
scope: "Evidence assembly as a designed output; the economics of represent-or-accept."
status: seedling
---

# Disputes and chargebacks

## Standard

A dispute is the issuer reversing a captured charge on the customer's behalf, and the merchant's response window is short and fixed. The work is evidence assembly: a coherent story of the transaction — what was sold, what the customer did, what the merchant's records show — submitted in the network's required format before the deadline. The merchant who assembled this evidence at design time has a folder, a narrative, and a submission; the merchant who assembles it at dispute time is archaeology.

The economics deserve the same explicitness as the engineering. Representing a dispute carries a fee and a chance of loss; accepting carries a certainty of loss and sometimes a lower fee. The decision is a written rule tied to the transaction's evidence class — a small-value charge with thin evidence may always be accepted, a fraud-flagged transaction may always be represented — not an emotional reaction per incident. And whatever the decision, the ledger records the reversal and its fee as transactions in their own right, so the books stay invariant under events nobody wanted.

Primary sources: <https://stripe.com/docs/disputes> and <https://www.pcisecuritystandards.org/document_library/>.

## Decision rules

- The evidence package's components — what to collect at transaction time so disputes can be answered quickly — are designed features of the payment flow.
- A represent-or-accept rule exists per evidence class, with its rationale written down.
- The dispute window deadline drives a scheduled escalation; humans never discover it late.
- The ledger records the reversal, the fee, and the outcome as transactions with the zero-sum invariant intact.
- Dispute outcomes feed the risk rules of future transactions as labeled history, not as one merchant's feelings.
- Repeat-dispute customers and products are visible as aggregates; the pattern is data, not anecdote.

## Procedure

1. At transaction time, capture the evidence components by design: customer interaction logs, delivery confirmation, terms acceptance, product fulfilment records.
2. On dispute arrival, log it in the state machine with its class and deadline.
3. Assemble the evidence package from the stored components; no manual archaeology as the primary path.
4. Apply the represent-or-accept rule for its evidence class; record the decision and its reason.
5. Submit within the window; log the submission and the response.
6. Reconcile the ledger: reversal, fee, and outcome recorded as entries; the zero-sum check passes.

## Anti-patterns

- Evidence assembled from scattered logs after the dispute arrived.
- Representing every dispute on principle, ignoring the economics of fees versus loss odds.
- Accepting every dispute to avoid the work; the pattern of concession is a signal to fraudsters.
- The reversal recorded as a balance edit rather than a ledger transaction.
- Deadline discovery by a human reading email; the escalation is scheduled.

## Done checklist

- [ ] Evidence components captured at transaction time.
- [ ] Represent-or-accept rule written per evidence class.
- [ ] Deadline escalation scheduled.
- [ ] Submission format and response logged.
- [ ] Ledger records reversal and fee with invariant intact.
- [ ] Dispute patterns reviewed as aggregates.

## Sources

- Dispute lifecycle and evidence: <https://stripe.com/docs/disputes>
- PCI standards library: <https://www.pcisecuritystandards.org/document_library/>
- EMVCo 3-D Secure: <https://www.emvco.com/emv-technologies/3-d-secure/>
