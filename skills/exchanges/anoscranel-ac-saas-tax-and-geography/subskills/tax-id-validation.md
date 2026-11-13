---
name: tax-id-validation
domain: software-engineering/tax-id-validation
trigger: "Validating and storing VAT, GST, and EORI identifiers for business customers."
anti_trigger: "Not for legal determination of whether an ID is valid for a given transaction; not tax advice."
scope: "VAT and EORI identifiers: checksums, registry confirmation, blocked formats, the customer's role in attestation."
status: seedling
---

# Tax ID validation

## Standard

A tax identifier is the pivot on which a B2B sale's treatment turns, so its validation splits into layers with different costs and different meanings. The format layer — country prefix, length, and checksum algorithm — is pure computation and can run inline at checkout. The registry layer — whether the identifier exists and is active — requires a lookup against an authoritative database and is slower, rate-limited, and not always available at checkout speed. The attestation layer is the customer's own claim, and it belongs to the customer until an authoritative answer replaces it.

The honest model here is a validation ladder: format checks instantly, registry checks asynchronously, attestation as the fallback when the registry is unavailable, and the recording of which rung cleared each identifier on each sale. A single "tax ID valid" boolean without its rung is a claim about an exact determination, and it compresses away the information that mattered.

Primary sources: <https://en.wikipedia.org/wiki/VAT_identification_number> and <https://stripe.com/docs/tax>.

## Decision rules

- Validate the format inline at checkout: country prefix, expected length, and the checksum algorithm where the scheme publishes one.
- Queue a registry check for every new or changed identifier; never call the registry on every charge.
- Record which layer cleared each identifier — format, registry, or attestation — with a date.
- Store the identifier so that downstream invoices can display it; it is the B2B documentation anchor.
- When the registry says inactive or nonexistent, treat the sale as a consumer sale for tax and notify the customer; do not silently block the purchase.
- Re-validate on a schedule; an identifier that was valid last year may have been deregistered.

## Procedure

1. Parse the identifier's country prefix and apply that country's format and checksum rules.
2. On first entry or change, queue the registry lookup.
3. Record the validation result, its layer, and its date beside the identifier.
4. At charge time, use the last validation's outcome; do not re-call the registry synchronously.
5. On a failed registry result, re-route the sale as consumer treatment and surface the failure to the customer.
6. Schedule periodic re-validation of all stored identifiers.

## Anti-patterns

- A regex that accepts any letters and digits as a valid VAT number.
- Calling the registry synchronously in the checkout path.
- Storing only the last-four or a masked form when invoices must display the full identifier.
- Silently downgrading a B2B sale to consumer treatment without notifying the customer.
- Treating a format-valid identifier as proof of business status.

## Done checklist

- [ ] Format validation inline with per-country rules.
- [ ] Registry checks queued and rate-limited.
- [ ] Validation layer and date recorded per identifier.
- [ ] Failed lookups routed and surfaced, not blocked.
- [ ] Periodic re-validation scheduled.
- [ ] Full identifier available to the invoice path.

## Sources

- VAT identification number and format structure: <https://en.wikipedia.org/wiki/VAT_identification_number>
- Stripe Tax, customer tax IDs: <https://stripe.com/docs/tax>
- EORI number overview: <https://en.wikipedia.org/wiki/EORI>
