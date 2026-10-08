---
name: price-a-discount-by-its-margin-cost
description: Use when sales proposes a discount and finance needs to know what volume it must buy back. Converts a discount into the extra units required to hold gross profit before it is approved.
---

# Price a discount by its margin cost

A discount comes out of margin, not revenue, so its true cost is far larger than the percentage suggests. Convert every discount into the volume it must buy back before you approve it.

## Procedure

1. Establish the gross margin before the discount, m. Use 0.40 for a $40 margin on a $100 price.
2. Convert the discount d into the margin it destroys. A 10% cut on a 40% margin leaves 33.3% when the cost stays fixed at $60.
3. Compute the volume uplift needed to hold the same gross profit: `uplift = d / (m - d)`.

       ```
       python3 -c "from decimal import Decimal as D; print(D('0.10')/(D('0.40')-D('0.10')))"
       # 0.3333 -> 33.3% more units to hold profit
       ```

4. Compare that to the uplift you actually expect. If the pipeline will not grow 33%, the discount destroys profit even though revenue may rise.
5. Note the erosion compounds at depth: at 20% off on a 40% margin the required uplift is `0.20/0.20` = 100%, doubling the volume.
6. At or below the margin the discount is unrecoverable: any `d >= m` cannot be bought back by any volume.
7. Price the discount in integer minor units too: 10% off 10000 minor units is 1000 off, and the new price is 9000, computed exactly.
8. Cap the discount list in policy, with a maximum depth per deal size, so approval is a lookup rather than a negotiation.
9. Attach an expiry to every discount; a permanent discount is just the lower price with extra steps.
10. Record the uplift actually achieved after the deal closes and feed it back into the next approval.

## Pitfalls

- Approving a discount on the percentage and never computing the uplift it needs.
- Forgetting that the denominator (m - d) goes to zero as the discount approaches the margin.
- Comparing discount cost to revenue instead of to gross profit.
- Letting discounts stack — a promo plus a deal discount — until they exceed the margin.
- Making discounts permanent by never expiring them.
- Float discount arithmetic whose rounding shifts the approved depth.

## Verification

    ```
    python3 -c "from decimal import Decimal as D; print(D('0.20')/(D('0.40')-D('0.20')))"
    # 1.0 -> double the volume at 20% off, or the deal loses money
    ```

Pass when the margin before and after and the required uplift are both shown. Report the margin before and after the discount and the volume uplift it must buy back.
