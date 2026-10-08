---
name: tear-down-a-competitor-price-sheet
description: Use when comparing your price to a competitor's. Normalises both sheets to a common unit and term, pulls add-ons out of the headline, and computes a like-for-like total cost under a named profile.
---

# Tear down a competitor price sheet

A competitor's headline price is a marketing number, not a comparison. Normalise both sides to the same unit, seat count and term before drawing any conclusion from it.

## Procedure

1. Capture the full sheet, not the headline: base price, per-seat or per-usage rates, overages, onboarding, support tier, and minimum term.
2. Normalise the unit. Vendor A charges $99 per seat with a 20-seat minimum; Vendor B charges $2,400 a month flat for "unlimited". Turn both into cost per active user per month.
3. Normalise the term. An annual prepay at $990/seat is $82.50/seat/month only if you use it all twelve months; a nine-month user pays $110.00/seat/month.
4. Add the add-ons people actually buy: onboarding, SSO, priority support. A $99 headline often lands past $130 with the governance features a serious account needs.
5. Compute the like-for-like three-year total for a stated profile, say 40 users:

       ```
       python3 -c "from decimal import Decimal as D
       A=D('99')*40*36 + D('2000'); B=D('2400')*36
       print(A, B)"
       # 144560 vs 86400 minor-unit dollars -> A is 67% dearer over three years
       ```

6. Confirm the profile matches real usage; the crossover often sits at a seat count where per-seat pricing loses to flat pricing.
7. Solve for the crossover: the seat count where per-seat total equals flat total, and hand it to sales as a competitive fact.
8. Keep both sheets as integer minor units with the unit and term recorded; a float per-seat figure times seats drifts the crossover seat count.
9. Check the "unlimited" clause for fair-use caps before treating it as unbounded.
10. Re-run quarterly; headline prices change and the add-on list changes more.

## Pitfalls

- Comparing headline to headline and missing the add-ons that flip the ranking.
- Ignoring the term; a monthly list price against an annual prepay is not a comparison.
- Picking a seat count that flatters your own pricing rather than the profile customers have.
- Forgetting onboarding, which is often 10-20% of first-year cost.
- Assuming "unlimited" is unlimited without reading the fair-use clause.
- Float per-seat figures that drift the crossover seat count.

## Verification

    ```
    python3 -c "from decimal import Decimal as D; print(D('99')*40*36+D('2000'), D('2400')*36)"
    # 144560 vs 86400 -> the three-year gap at the stated profile
    ```

Pass when both sheets share a unit, a term and a named profile. Report the like-for-like total, the add-ons included, and the crossover seat count.
