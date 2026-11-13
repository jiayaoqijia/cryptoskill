---
name: tax-inclusive-and-display
domain: software-engineering/tax-inclusive-and-display
trigger: "Deciding whether the displayed price already contains the tax."
anti_trigger: "Not for computing the amount; not for marketing pricing strategy."
scope: "Tax-exclusive pricing, tax-inclusive pricing, and the line between a legal display choice and unit-of-measure confusion."
status: seedling
---

# Tax-inclusive and display

## Standard

A tax-exclusive price shows the product's price and adds tax at checkout; a tax-inclusive price embeds the tax in the displayed figure and itemises it on the invoice. Which mode is correct depends on the jurisdiction and the customer type: consumer-facing retail in most VAT countries expects tax-inclusive display by law, while B2B and US sales-tax conventions often expect tax-exclusive. A SaaS serving both worlds must support both modes, chosen by the sale's attributes rather than by a single global setting.

The engineering consequence is unit confusion. A tax-inclusive price is a different number from a tax-exclusive one, and every system downstream — the plan's recurring amount, the ledger's recorded revenue, the proration calculation — must know which basis a figure carries. The display mode is a presentation decision; the basis of every stored amount is a data contract, and mixing the two produces silently-wrong invoices that look right in isolation.

Primary sources: <https://stripe.com/docs/tax> and <https://en.wikipedia.org/wiki/Value-added_tax>.

## Decision rules

- Choose the display mode per jurisdiction and customer type from a documented rule, not a global constant.
- Store every price with its basis — tax-exclusive or tax-inclusive — as an attribute of the amount.
- Convert between bases only at the presentation boundary, with the computation recorded alongside.
- For recurring subscriptions, decide the basis once and carry it through upgrades, downgrades, and proration.
- Never compare a tax-inclusive figure to a tax-exclusive one in reports; normalise to one basis first.
- State the display mode in the product's per-jurisdiction configuration so a jurisdiction's law change is a config change.

## Procedure

1. Document each jurisdiction's expected display mode for B2C and B2B.
2. Add the basis attribute to every price field in the billing model.
3. Compute the display figure at the presentation boundary, recording the basis used.
4. Thread the basis through plan changes and proration so upgrades do not change basis mid-cycle.
5. Normalise to a single basis in reporting queries, with the conversion recorded.
6. Test the display of a price through both modes with a single underlying amount.

## Anti-patterns

- A single global display mode with a boolean override nobody remembers.
- Storing prices with no basis attribute because the mode was chosen at signup.
- Proration computed on a tax-inclusive base then displayed tax-exclusive.
- Comparing revenues across jurisdictions with mixed bases.
- Changing the mode for a live customer mid-subscription without a migration.

## Done checklist

- [ ] Display mode per jurisdiction and customer type documented.
- [ ] Basis attribute on every stored price.
- [ ] Conversion at the presentation boundary only.
- [ ] Basis carried through plan changes and proration.
- [ ] Reporting normalised to one basis.
- [ ] Both modes tested on one underlying amount.

## Sources

- Stripe Tax, tax-inclusive and exclusive behaviour: <https://stripe.com/docs/tax>
- Value-added tax display conventions: <https://en.wikipedia.org/wiki/Value-added_tax>
- Consumption tax basics: <https://en.wikipedia.org/wiki/Consumption_tax>
