---
name: thresholds-and-registration
domain: software-engineering/thresholds-and-registration
trigger: "Deciding when collecting a jurisdiction's tax becomes mandatory."
anti_trigger: "Not for filing returns; not legal advice on registration timing."
scope: "When collecting becomes mandatory: distance-selling thresholds, currency conversion, retrospective liability."
status: seedling
---

# Thresholds and registration

## Standard

Most jurisdictions do not require a foreign seller to register and collect from the first sale. They set a threshold — an annual amount of sales into that jurisdiction — below which the seller has no local obligation, and above which registration becomes mandatory. The threshold is usually measured in the local currency over a rolling or calendar-year window, which means the seller must convert its own sales figures into the local currency and watch the running total.

The mechanism this skill describes is the predictable part: define each jurisdiction's threshold, track sales into it in local currency, alert when the trajectory crosses before the obligation crystallises, and treat crossing as a registration project, not a tax-rate patch. Registration means filing, remittance, and often a local fiscal representative — the date of first compliant collection is rarely the day the threshold was crossed.

Primary sources: <https://stripe.com/docs/tax> and <https://en.wikipedia.org/wiki/Value-added_tax>.

## Decision rules

- Record each supported jurisdiction's threshold with its currency, window, and official source, dated.
- Track sales into each jurisdiction in the local currency of that jurisdiction, converting at a documented rate on a documented date.
- Alert well before crossing — 60 to 80 percent of the threshold — because registration is a project with lead time.
- Treat a crossed threshold as a registration project: filings, remittance, representative, first filing period.
- Check whether sales before registration create retrospective liability, and record the answer per jurisdiction.
- Deregistration, a downgrade, or sustained absence below the threshold — each has a rule, not a single switch.

## Procedure

1. List the jurisdictions the product is sold into, with their thresholds and window definitions.
2. Implement the sales-per-jurisdiction ledger with currency conversion recorded per entry.
3. Set alerting at set fractions of the threshold with the trajectory, not the total alone.
4. On crossing, open a registration project and record the crossing date and first compliant-collection date separately.
5. Research and record retrospective-liability treatment per jurisdiction.
6. Review thresholds on a schedule; they change more often than headline rates do.

## Anti-patterns

- Tracking sales in the seller's currency only, so thresholds are measured in the wrong unit.
- Alerting at the threshold crossing itself, when the needed action takes weeks.
- Treating registration as a rate change in the billing table.
- Assuming one window definition — rolling twelve months or calendar year — for all jurisdictions.
- Ignoring that a jurisdiction can change the threshold, the window, or the currency basis.

## Done checklist

- [ ] Thresholds recorded with sources and dates.
- [ ] Per-jurisdiction ledger in local currency.
- [ ] Conversion rate and date recorded per entry.
- [ ] Early-alert fractions configured.
- [ ] Registration project templated with the two dates separated.
- [ ] Retrospective treatment recorded per jurisdiction.

## Sources

- Stripe Tax, registrations and thresholds: <https://stripe.com/docs/tax>
- Value-added tax and threshold concepts: <https://en.wikipedia.org/wiki/Value-added_tax>
- Tax residence concepts: <https://en.wikipedia.org/wiki/Tax_residence>
