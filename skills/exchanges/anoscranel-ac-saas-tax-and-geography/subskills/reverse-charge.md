---
name: reverse-charge
domain: software-engineering/reverse-charge
trigger: "Handling the B2B case where the buyer, not the seller, owes the tax."
anti_trigger: "Not for computing the buyer's self-assessment; not tax advice."
scope: "When the buyer self-assesses: B2B services and why the VAT number is the pivotal test."
status: seedling
---

# Reverse charge

## Standard

The reverse-charge mechanism moves the tax obligation from the seller to the buyer. For cross-border B2B services, the seller issues an invoice with no tax charged and a statement that the tax is being self-assessed by the customer, who then accounts for it in their own jurisdiction. The seller's duty is documentation: correct customer details, the customer's registered tax identifier, and an invoice that names the mechanism rather than silently omitting the tax.

The failure mode is not the mechanism's complexity but its evidence trail. Because the seller does not collect tax, the boundary of the exemption is invisible to the payment pipeline, and precisely for that reason it must be visibly coded in the sale record: the customer's identifier status, the place of supply, the mechanism's name, and the invoice's reference to it. A B2B sale handled as reverse-charge with no mechanism named on the invoice is indistinguishable, in an audit, from a sale where tax should have been collected and was not.

Primary sources: <https://stripe.com/docs/tax> and <https://en.wikipedia.org/wiki/VAT_identification_number>.

## Decision rules

- Treat the customer's tax identifier, registry-confirmed, as a prerequisite for reverse-charge treatment.
- Compute an amount for the service, then zero the collection line, and record the mechanism's name on the sale record.
- Print the reverse-charge statement on the invoice where required, and store the invoice number with the sale.
- Verify the customer's jurisdiction is one where the reverse charge is permitted for the specific service being sold.
- If the identifier later fails, re-evaluate the sale's treatment and record the change; the original treatment became unreliable, not the sale.
- Keep the reverse-charge flag distinct from the currency, country, or product-type flags — it is a treatment decision with its own evidence chain.

## Procedure

1. Check the sale is B2B and the product is a service in the eligible class.
2. Verify the customer's tax identifier is registry-confirmed at the time of the sale.
3. Determine the destination jurisdiction's reverse-charge rule before zeroing the collection.
4. Issue the invoice with the mechanism stated and the identifier displayed.
5. Record the flag, the evidence chain, and the invoice number on the sale record.
6. Re-evaluate the treatment when the identifier status changes.

## Anti-patterns

- Zero tax charged, with no record that the reason was the reverse charge.
- Applying reverse charge because the customer self-declared as a business without an identifier check.
- Treating reverse charge as a jurisdiction-wide rule, when eligibility depends on the product type too.
- Invoices that name the mechanism but not the customer's identifier.
- Blocking a sale when the identifier fails registry, rather than re-routing to consumer treatment.

## Done checklist

- [ ] B2B and product eligibility confirmed before treatment is set.
- [ ] Registry-confirmed identifier at sale time.
- [ ] Destination rule verified per sale class.
- [ ] Mechanism named and identifier displayed on the invoice.
- [ ] Evidence chain on the sale record.
- [ ] Re-evaluation on identifier status change.

## Sources

- Stripe Tax, B2B handling: <https://stripe.com/docs/tax>
- VAT identification number structure: <https://en.wikipedia.org/wiki/VAT_identification_number>
- EORI and business identifier context: <https://en.wikipedia.org/wiki/EORI>
