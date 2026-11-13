---
name: tax-address-evidence
domain: software-engineering/tax-address-evidence
trigger: "Collecting and weighing the evidence of a customer's tax location."
anti_trigger: "Not for address formatting and internationalisation; not for geolocation in the marketing sense."
scope: "Address, billing country, phone prefix, IP, and bank country as location evidence with staleness rules."
status: seedling
---

# Tax address evidence

## Standard

Place-of-supply rules are only as good as the location evidence beneath them. The evidence a SaaS can practically collect is layered: the customer's declared billing country and address, the payment instrument's country, the IP address at the time of purchase, the phone prefix, and the bank country. Jurisdictions weigh these differently, and some publish an explicit hierarchy — two non-contradictory pieces of evidence, one of which is typically the billing address.

The engineering model is an evidence record: capture the layers at the moment of sale, record which were used for the determination, and re-evaluate when they drift apart. Evidence is a snapshot, not an attribute — a customer's IP today says nothing about their billing country next month — so each sale carries its own evidence set, and a change in the evidence triggers a re-evaluation of the treatment, not a silent assumption of continuity.

Primary sources: <https://stripe.com/docs/tax> and <https://en.wikipedia.org/wiki/Postal_address>.

## Decision rules

- Capture the primary evidence set at the moment of the sale, not at signup and not on a schedule.
- Record which evidence pieces supported each sale's place-of-supply determination.
- Apply the jurisdiction's stated evidence hierarchy where one exists; do not invent a default weighting.
- When pieces of evidence contradict, apply the hierarchy and record the contradiction rather than discarding either.
- Treat evidence as per-sale; a subscription's each charge inherits evidence, but a change re-opens the determination.
- Never use marketing geolocation as tax evidence; the precision that matters here is jurisdictional, not city-level.

## Procedure

1. Enumerate the evidence layers the checkout and billing systems can capture.
2. Implement per-sale capture with the timestamp of each piece.
3. Implement the applicable evidence hierarchy, including contradiction handling.
4. Record on each sale which pieces were used, and at what values.
5. Define the drift triggers — country change, payment-instrument change, address change — and re-evaluate on them.
6. Store the evidence with the sale record, and keep it for the same archival term as the invoice.

## Anti-patterns

- Using the signup country as the sale's evidence for years of charges.
- Evidence captured once and refreshed silently without re-evaluating the treatment.
- A single evidence layer — IP alone, or declared country alone — where the rules require two.
- Contradicting evidence resolved by discarding the less convenient piece, unrecorded.
- Marketing-grade geolocation standing in for tax-grade evidence.

## Done checklist

- [ ] Evidence layers enumerated for capture.
- [ ] Per-sale capture with timestamps.
- [ ] Hierarchy and contradiction handling implemented.
- [ ] Used-evidence recorded per sale.
- [ ] Drift triggers defined and wired.
- [ ] Evidence archived with the sale.

## Sources

- Stripe Tax, customer location and evidence: <https://stripe.com/docs/tax>
- Postal address structure: <https://en.wikipedia.org/wiki/Postal_address>
- ISO 3166 country codes: <https://en.wikipedia.org/wiki/ISO_3166>
