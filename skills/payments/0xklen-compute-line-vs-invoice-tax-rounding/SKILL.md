---
name: compute-line-vs-invoice-tax-rounding
description: Use when tax or a pro-rated charge must be computed per line or per invoice and the two give different totals. Picks the basis the rule requires and reconciles the totals consistently.
---

# Compute line vs invoice tax rounding

Tax on `100*0.19 + 200*0.19` computed per line rounds twice; computed on the invoice base it rounds once. The two differ by cents and both can be "correct" — the filing rule decides which you must use.

## Procedure

1. Determine the required basis from the jurisdiction's rule: some require tax **per line item** then summed, others **per invoice** on the taxable subtotal. Write the choice down before coding.
2. Per-line: `for line: tax_i = round(line_base_i * rate)`, then `total = sum(tax_i)` — N rounding operations.
3. Per-invoice: `total = round(sum(line_base_i) * rate)` — one rounding operation on the summed base.
4. Keep the taxable base and the rate as integers or exact decimals; the difference between the two methods is pure rounding, not base error.
5. Reconcile the two methods' outputs and record the delta. When the filing uses one, the invoice must present the same figure or the sales ledger will not tie out.
6. For mixed tax rates, group by rate and apply the chosen basis within each group; you cannot sum across rates before multiplying.
7. VAT-inclusive pricing ("gross of tax") requires extracting the tax: `tax = gros * rate / (1 + rate)`, computed in exact arithmetic — `gros * 0.19 / 1.19` as a float is wrong.
8. Store the tax basis on the invoice so any future recompute uses the same method.
9. Keep both the per-line and per-invoice figures for a period cross-check; the two tying out is evidence the base is right.
10. For a discount, decide whether it reduces the base before or after tax and encode that order in the invoice model.
11. Test with a 0% rate and a three-decimal rate to catch truncation of small bases.

## Pitfalls

- Applying an invoice-level discount after per-line tax re-runs the tax on a different base; the order matters and jurisdictions differ.
- `gros * rate / (1 + rate)` with a float rate drifts; use `mulDiv(gros, 1900, 11900)`-style integer maths.
- A 0% or exempt line still participates in allocating a document-level charge; excluding it skews the split.
- Comparing a per-line total against a per-invoice figure and treating the 1-cent gap as an error closes the books incorrectly.
- Rounding the rate (0.19) rather than the result loses precision when the rate has more decimals (0.075).
- Mixed-rate invoices summed before multiplication break the per-invoice basis.
- A line-rounded total that a filing re-derives per-invoice shows a phantom adjustment every period; pick one basis and audit against it.

## Verification

    python3 -c "from decimal import Decimal as D, ROUND_HALF_UP; q=lambda x:x.quantize(D('0.01'),ROUND_HALF_UP); print('per-line', q(D('0.05')*D('0.10'))*2, 'per-invoice', q(D('0.10')*D('0.10')))"
    # per-line 0.02, per-invoice 0.01 -> a 1-cent gap from rounding alone

Report the basis chosen, both totals, and the delta by which they differ.
