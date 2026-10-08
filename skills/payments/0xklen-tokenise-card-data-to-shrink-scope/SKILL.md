---
name: tokenise-card-data-to-shrink-scope
description: Use when a system touches card numbers, CVV, or cardholder data and the compliance scope is too wide. Replace the PAN with a token at the boundary and prove no PAN is stored.
---

# Tokenise card data to shrink scope

Storing a card number drags the whole system into card-data rules. This skill replaces the PAN with a token at the boundary so your systems never hold it.

## Procedure

1. Draw the trust boundary: any component that reads, transmits, or stores the PAN is in scope. Move the boundary to the provider's hosted fields or element.

2. Use provider-hosted fields so the PAN never becomes a value in your JavaScript: an iframe or element that posts directly to the processor.

3. For server-side flows, exchange the PAN for a token immediately and never persist the PAN or the CVV. The CVV must never be stored, even encrypted.

4. Store only the token plus the display metadata the processor allows: `card_brand`, `last4`, `exp_month`, `exp_year`.

5. Confirm what you store against the card-data rules: full track data, CVV, and PIN block are never storable; a stored PAN requires encryption and heavy scope.

6. Log nothing sensitive; mask to the last four in every log line and error message.

7. Attribute retention: the token lives as long as the customer relationship while the provider holds the PAN under its own scope.

8. Run the provider's scope-assessment wizard and record the resulting SAQ level; re-run it after any flow change.

9. Verify no PAN remains anywhere: scan a sample dump for Luhn-valid 13-19 digit runs that are not order or invoice ids.

## Pitfalls

- A "masked" PAN stored in a notes field is still a PAN if the mask keeps more than the last four digits.
- Reintroducing the PAN for a refund by asking the user to re-enter it is fine; storing it again is not.
- Copy-pasting a card into a support ticket is a common leak path; train agents and scrub tickets.
- A provider token migration changes the token format; a botched migration can force re-collection of every card.
- Client-side "just check Luhn" validation runs on the PAN inside your page and pulls it into scope.

## Verification

    rg -n "\b[0-9][0-9 -]{11,}[0-9]\b" /var/dumps/sample.sql | grep -vE "last4|order_id|invoice" || echo "no PAN-like sequences"

Report the in-scope components, the SAQ level, and the result of the PAN scan.
