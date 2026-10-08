---
name: research-willingness-to-pay-with-van-westendorp
description: Use when you need a defensible acceptable price range from survey data. Runs the four van Westendorp questions, builds the cumulative curves, and reads the range where the curves cross.
---

# Research willingness to pay with van Westendorp

Asking "would you pay $20?" gets a polite yes that means nothing. Four anchored questions locate the range a buyer considers fair, and the crossings give a band to place a real price inside.

## Procedure

1. Ask four open price questions about one concrete product, in this order: at what price is it so cheap you doubt its quality; a bargain; getting expensive; so expensive you would never buy.
2. Collect open numeric answers, not ranges or choices. You need n >= 150 for stable curves; 200 is comfortable.
3. Build four cumulative curves: too-cheap and bargain ascending, expensive and too-expensive descending.
4. Find the two crossings. Point of marginal cheapness (PMC) is where too-cheap meets expensive; point of marginal expensiveness (PME) is where bargain meets too-expensive.
5. Take the midpoint of the range as the hypothesis, then test it:

       ```
       python3 -c "from decimal import Decimal as D
       PMC=D('24'); PME=D('61'); print('range', PMC, 'to', PME, 'mid', (PMC+PME)/2)"
       # range 24 to 61 mid 42.5
       ```

6. Read the shape, not only the crossings. A flat cheap curve means the category is price-insensitive; a steep expensive curve means one more dollar loses a lot.
7. Segment before you trust the result. Run the curves per segment; a blend of enterprise and hobby answers fits neither.
8. Watch for a range wider than 3x. That usually means the question described a fuzzy product, so rewrite and re-run.
9. Store every answer as an integer minor unit (`price_minor`) from collection onward; averaging floats will not reproduce the survey UI's rounding.
10. Re-run when the product changes materially or when the median answer moves more than 20% year over year.

## Pitfalls

- Using yes/no or a fixed price list instead of open numeric answers; the curves need numbers.
- Running it on a blend of segments, so the range fits no one.
- Reading the optimum as the price to publish rather than a hypothesis to test.
- Collapsing the range to one answer in a rushed questionnaire and skipping the crossings.
- A sample under about 150, which makes the crossings jump around.
- Averaging prices as floats, which does not match the number the survey respondent saw.

## Verification

    ```
    python3 -c "from decimal import Decimal as D; print('mid', (D('24')+D('61'))/2)"
    # mid 42.5 -> the price to test, not to publish
    ```

Pass when PMC, PME and the midpoint are reported with the segment attached. Report PMC, PME, the midpoint, and the population the range describes.
