---
name: pci-and-card-boundaries
domain: software-engineering/pci-and-card-boundaries
trigger: "Deciding where card data may live and what engineering avoids the compliance surface."
anti_trigger: "Not for full compliance programs, and not for legal advice."
scope: "Card data boundaries: what you never store and what remains out of scope."
status: seedling
---

# PCI and card boundaries

## Standard

PCI DSS is a compliance regime about cardholder data, and its heaviest obligations attach to systems that store or process the primary account number. The engineering decision with the highest leverage is therefore architectural: keep card data out. Tokenization through a processor-hosted field or a redirect to a hosted payment page moves the primary account number out of your environment, and the difference in audit surface between \"we never touch it\" and \"we store it encrypted\" is not a detail; it changes what your systems must prove, log, scan, and restrict.

The boundary the skill draws is honest about what remains in scope even under tokenization: the customer's experience, the state machines, the reconciliation, the dispute evidence. Those are engineering obligations with or without card data, and they are where the payments investment actually lives. What tokenization buys is the exclusion of the cardholder-data environment — the secure storage, the key ceremony, the network segmentation around PAN storage — which is the part whose failure is both catastrophic and, if excluded, no longer yours.

Primary sources: <https://www.pcisecuritystandards.org/document_library/> and <https://www.emvco.com/emv-technologies/3-d-secure/>.

## Decision rules

- The store-or-tokenize decision is made once, deliberately, at architecture time; the default direction is out.
- Any system that will touch the primary account number is named in the design document with its justification; surprises later mean redesign.
- Tokenized environments still log access, still verify webhook signatures, and still reconcile; the reduction is in scope, not in discipline.
- Logs, error traces, analytics, and support tools are included in the boundary audit; a number in a stack trace breaches the boundary with no code written for it.
- Boards display card data classification on every relevant data source; unclassified storage of free-form customer input is treated as a finding.
- The written record names the boundary decision, its date, its assumptions, and whatever the organization formally accepted in scope.

## Procedure

1. Write the boundary decision — tokenize versus store — with the justification and who decided.
2. Trace the card data path across the design; name every system that touches it.
3. For the in-scope set, list the PCI obligations the organization accepted; record it as the audit-facing register.
4. Add a scanning path for traces, logs, and analytics that may hold noncompliant copies.
5. Verify the tokenized flow: primary account number never persists anywhere you control, in logs or memory dumps where avoidable.
6. Review annually against the current standard version and the processor's own guidance.

## Anti-patterns

- Choosing integration libraries first, discovering later that a \"self-hosted\" option brought the primary account number into your boundary.
- A boundary audit that checks the application database but not the logs.
- Copying a processor dashboard's raw number into internal support tooling.
- Treating a tokenization decision as permanent; processor migrations require a re-review.
- Assuming out-of-scope where a third-party iframe is used without verifying the integration shape.

## Done checklist

- [ ] Boundary decision documented with owner and date.
- [ ] Card data path traced; every touching system named.
- [ ] Obligations register updated for whatever was accepted in scope.
- [ ] Traces, logs, and analytics in the boundary audit.
- [ ] Tokenized flow verified for non-persistence.
- [ ] Annual review against the current standard.

## Sources

- PCI DSS document library: <https://www.pcisecuritystandards.org/document_library/>
- EMVCo 3-D Secure: <https://www.emvco.com/emv-technologies/3-d-secure/>
- Billing subscription lifecycle: <https://docs.stripe.com/billing/subscriptions/overview>
