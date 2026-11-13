---
name: place-of-supply
domain: software-engineering/place-of-supply
trigger: "Deciding which jurisdiction's rules decide the tax on a SaaS sale."
anti_trigger: "Not for choosing the tax rate once the place is set; not legal advice."
scope: "Which rules apply: destination versus origin, B2B versus B2C, the customer's location as the trigger."
status: seedling
---

# Place of supply

## Standard

The first question is not "what rate" but "which rules". Place of supply is the legal convention that assigns a sale to a jurisdiction, and for SaaS — a cross-border service delivered electronically — most of the world has converged on destination-based treatment: the customer's location decides the tax treatment, not the seller's. The United States sales-tax system is origin-shaped at the state level but modifies itself with nexus rules that pull the obligation to the seller when the seller has sufficient presence.

The second axis is who the customer is. Business-to-consumer sales make the seller the collector: the tax appears on the consumer's invoice and the seller remits it. Business-to-business sales in much of the world shift the assessment to the buyer through the reverse-charge mechanism, and the seller's obligation becomes documentation rather than collection. A SaaS's billing system must decide, per customer, which of these two worlds the sale lives in, because the same transaction can require opposite treatments on either side of that line.

Primary sources: <https://stripe.com/docs/tax> and <https://en.wikipedia.org/wiki/Value-added_tax>.

## Decision rules

- Record the customer type — business or consumer — as a first-class billing field, decided at checkout from evidence, not assumed from the signup form.
- Treat the customer's location, not the seller's, as the default trigger for tax treatment in destination regimes.
- Route each sale through the place-of-supply rules of the jurisdictions the product has chosen to support; record which rule decided the outcome.
- Keep the B2B and B2C paths separate in code; a single "has tax ID" boolean is not a place-of-supply determination.
- Treat a change in the customer's country or business status as a re-evaluation event, not an attribute update.

## Procedure

1. Capture the customer's type, location evidence, and tax identifiers at checkout.
2. Determine the place of supply under the applicable regime: destination default, origin exceptions, nexus overlays.
3. Decide the customer's role: consumer (seller collects) or business (reverse charge or zero-rate with documentation).
4. Compute the applicable treatment from the place-of-supply rules and the customer's role.
5. Record the rule identifiers used, the evidence relied on, and the outcome.
6. Re-evaluate when any input changes: country, customer type, tax identifier, product classification.

## Anti-patterns

- Deciding tax from the seller's country alone.
- One code path for B2B and B2C sales because they usually look the same.
- Treating the tax-ID-present boolean as the place-of-supply answer, rather than as an input to it.
- Recomputing tax on every charge without recording the place-of-supply determination once.
- Rendering the treatment in the UI as fixed, when the underlying determination is provisional and evidence-based.

## Done checklist

- [ ] Customer type recorded as a billing field with evidence.
- [ ] Place-of-supply rule identifier recorded per sale.
- [ ] B2B and B2C paths separate and tested.
- [ ] Location evidence captured at checkout, not backfilled.
- [ ] Re-evaluation triggers documented.
- [ ] Outcome recorded with the rule and evidence IDs.

## Sources

- Stripe Tax documentation, how tax is calculated: <https://stripe.com/docs/tax>
- Value-added tax and destination-based treatment: <https://en.wikipedia.org/wiki/Value-added_tax>
- Consumption-tax comparison across regimes: <https://en.wikipedia.org/wiki/Consumption_tax>
