---
name: anchor-prices-with-a-tier-ladder
description: Use when designing a good/better/best price menu. Orders the tiers so the middle is the obvious choice, uses the top tier as an anchor, and keeps every tier price in exact minor units.
---

# Anchor prices with a tier ladder

Buyers judge a price against the alternatives on the same page, not against an absolute number. A ladder built around a deliberate high anchor makes the middle tier look reasonable and moves mix without cutting the list price.

## Procedure

1. Put three tiers on the page, not two: a low entry, the target, and a high anchor. Two options invite a yes/no; three invite a which-one.
2. Make the anchor genuinely superior, not fake. The top tier must be something a real segment buys, or the decoy is transparent and the anchor fails.
3. Set the target tier nearer the anchor than the floor: Starter $19, Growth $49, Scale $99.
4. Keep the gaps non-linear. $19 / $49 / $99 (gaps 30 and 50) reads as a ladder; $19 / $29 / $39 reads as three versions of cheap.
5. Model the revenue mix, not just the chosen price. If 60% take Growth, 25% Starter, 15% Scale:

       ```
       python3 -c "from decimal import Decimal as D; print(D('0.25')*1900 + D('0.60')*4900 + D('0.15')*9900)"
       # 4900 blended minor units = $49.00 per buyer
       ```

6. Stress the mix: remove the anchor and re-run with Scale at zero share to find the floor of the ladder's revenue.
7. Gate the jumps with a capability the buyer recognises, not a seat count alone — see `gate-features-to-shape-packaging`.
8. Name the target tier's value in one line a buyer can repeat to their boss; a tier nobody can summarise does not get chosen.
9. Keep every tier price an integer minor unit in the price table (`price_minor=4900`); never store `49.0` as a float.
10. Review the ladder when the middle-tier share passes 85% or falls below 40% — both mean the ladder is no longer steering.
11. Do not discount the anchor to sell it. If the top tier needs a discount to move, it was mispriced or mis-scoped.

## Pitfalls

- A fake anchor nobody ever buys, which buyers see through and which drags the whole page's credibility.
- Linear tiers that read as three versions of the same cheap thing.
- Gating the activation feature, so nobody reaches the middle tier at all.
- Discounting the anchor, which collapses the reference point the ladder depends on.
- A middle tier priced just above the entry, so almost everyone takes the entry.
- Tier prices stored as floats in the CMS, so the displayed price and the billed price diverge by a cent.

## Verification

    ```
    python3 -c "from decimal import Decimal as D; print(D('0.25')*1900+D('0.60')*4900+D('0.15')*9900)"
    # 4900 -> blended revenue per buyer at the assumed mix
    ```

Pass when each tier carries a named value metric and the blend is computed. Report the ladder, the expected mix, and the blended revenue per buyer with the anchor's share stated.
