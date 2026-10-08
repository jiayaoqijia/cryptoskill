---
name: handle-digital-sales-tax-thresholds
description: Use when selling digital goods across jurisdictions. Tracks economic-nexus thresholds, computes tax on the taxable base, and keeps collected tax out of revenue.
---

# Handle digital sales tax thresholds

Digital sales tax is not one rate in one place — it is a per-jurisdiction threshold that, once crossed, obligates you to register, charge and remit. The work is tracking thresholds and never treating collected tax as revenue.

## Procedure

1. List the jurisdictions you sell into and each threshold in its local unit and window. Examples: many US states use $100,000 in sales or 200 transactions over 12 months; the EU applies a single EUR 10,000 cross-border threshold.
2. Compute rolling-window sales per jurisdiction in integer minor units and compare to the threshold:
   `ytd_minor = sum(amount_minor for sales in jurisdiction over trailing 12 months)`.
3. Flag jurisdictions at risk when `ytd_minor > 0.8 * threshold_minor`, so registration happens before the crossing date, not after.
4. Once registered, compute tax on the taxable base. Not every line is taxable: digital services, SaaS and ebooks differ by state.
   `tax_minor = taxable_base_minor * rate_bp // 10000`.
5. Worked example: 50,000 minor taxable at 625 bp (6.25%): `tax = 50000*625//10000 = 3125` minor = USD 31.25.
6. Locate the buyer with two non-contradictory pieces of evidence (billing address plus IP or card country). A mismatch means resolve it, do not guess the lowest rate.
7. Keep tax in its own liability account: it is collected on behalf of the state, never revenue and never gross margin.
8. Remit on the jurisdiction's cadence (monthly, quarterly) and file a zero return where one is required.
9. Re-check thresholds annually: they change, and a marketplace-facilitator law can move the obligation to the platform.

10. Keep location evidence for each sale; an audit asks how you determined the rate, not only that you charged one.
11. Monitor marketplace-facilitator registrations; where the platform collects, remove your own tax line to avoid double-charging.
12. Recompute the threshold on a rolling window, not a calendar year, where the jurisdiction mandates rolling.
13. Distinguish taxable and exempt customers (resale certificates, non-profits) at the line level, not the invoice level.
14. Reconcile the tax liability account to the filings each period; an unexplained balance is either unremitted or double-collected.
15. Set a filing calendar on the jurisdiction's cadence so a zero return is filed where one is required.

## Pitfalls

- Counting gross including the tax itself toward the nexus threshold; most regimes measure thresholds on sales, not tax-inclusive receipts.
- Booking collected tax as revenue inflates MRR while the tax you owe stays the same.
- Registering after crossing the threshold leaves a period of uncollected, unremittable liability.
- Charging the wrong rate because the billing address and card country disagree and you picked one.
- Missing marketplace-facilitator rules and double-charging where the platform already collects.

- Without stored location evidence, a rate charged correctly is unprovable and gets reassessed.
- Charging tax where the platform already remits doubles the customer's tax and creates refund requests.
- A calendar-year threshold computation misses a rolling-window crossing and leaves a liability period.
- Exempting a whole invoice because one line is exempt under-collects on the rest.

## Verification

    python3 -c "base=50000; rate_bp=625; print(base*rate_bp//10000, 'minor tax on', base)"
    # 3125 -> 6.25% of a $500.00 taxable sale, held as a liability not revenue

Report: per-jurisdiction trailing-12-month sales against threshold, the flagged at-risk list, and the tax liability balance to remit.
