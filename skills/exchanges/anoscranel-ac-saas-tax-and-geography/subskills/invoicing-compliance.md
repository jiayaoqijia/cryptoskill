---
name: invoicing-compliance
domain: software-engineering/invoicing-compliance
trigger: "Generating invoices that satisfy the destination jurisdiction's requirements."
anti_trigger: "Not for the invoice's prose as a document design task; not legal advice."
scope: "What a compliant invoice requires per jurisdiction, and why invoicing is not a cosmetic step."
status: seedling
---

# Invoicing compliance

## Standard

An invoice is the tax system's primary document: in many jurisdictions it is a legally defined artefact whose required fields, sequencing, and storage terms are set by regulation, not by the company's document taste. Common requirements include a sequential invoice number from a defined series, the seller's registration identifier, the customer's identifier for B2B sales, the date, the place of supply, the rate and amount of tax per rate band, and the mechanism for any zero-rated treatment. Some jurisdictions add archival terms — a decade or more — and authenticity requirements.

A SaaS treating invoicing as a cosmetic step — a template, a thanks message, a PDF — discovers the difference when a customer's audit asks for the sequence-gap register or an amendment trail that does not exist. The invoice is a per-jurisdiction contract with the tax authority, and its production belongs in the billing pipeline where the sale's evidence lives, not in a downstream document renderer that only sees a total.

Primary sources: <https://stripe.com/docs/tax> and <https://en.wikipedia.org/wiki/Value-added_tax>.

## Decision rules

- Enumerate the destination jurisdiction's required invoice fields and treat them as a schema, not as template layout.
- Issue invoice numbers from a gapless sequence with a documented register; a gap is a finding, not a cosmetic bug.
- Include per-band tax amounts — rate, base, and amount — not a single blended tax line.
- Record the mechanism for zero-rated and reverse-charge sales on the invoice.
- Store the invoice for the jurisdiction's archival period, in a form that can be re-presented unaltered.
- For corrections, issue credit notes and replacements per the jurisdiction's rules; never edit an issued invoice.

## Procedure

1. Collate the required fields per jurisdiction into an invoice schema keyed by place of supply.
2. Implement the numbering sequence with a register that records every issue and every gap.
3. Render tax per band from the sale's stored treatment, not from a recomputed amount.
4. Include the mechanism and identifier fields for zero-rated and reverse-charge sales.
5. Store the rendered artefact with its metadata — sale ID, sequence number, issue date, basis.
6. Implement corrections as credit notes and replacements with their own sequence.

## Anti-patterns

- Editing an issued invoice to fix a mistake.
- A single blended tax line drawn from a rate lookup at render time rather than the sale's stored treatment.
- Invoice numbers assigned per customer, which breaks jurisdictional gaplessness.
- Storing invoices only in the email system the customer received them from.
- Fields absent from the document because the template's design did not have room for them.

## Done checklist

- [ ] Per-jurisdiction invoice schema implemented.
- [ ] Gapless numbering with a gap register.
- [ ] Per-band tax from stored treatment.
- [ ] Mechanism recorded for zero-rated sales.
- [ ] Archival implemented with re-presentation.
- [ ] Corrections via credit notes and replacements.

## Sources

- Stripe Tax, invoices and reporting: <https://stripe.com/docs/tax>
- Value-added tax and invoicing context: <https://en.wikipedia.org/wiki/Value-added_tax>
- Postal and address standards context: <https://en.wikipedia.org/wiki/Postal_address>
