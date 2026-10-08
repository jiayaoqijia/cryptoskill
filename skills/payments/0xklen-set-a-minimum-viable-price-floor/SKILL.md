---
name: set-a-minimum-viable-price-floor
description: Use when a deal or a client sits at the edge of profitability, or someone asks you to take work below cost. Sets a floor from variable cost plus a minimum contribution, and holds it or declines.
---

# Set a minimum viable price floor

A price below variable cost is a loss on every unit, and no volume fixes it. Set the floor once from the cost structure, write it down, and decline or renegotiate anything under it rather than absorbing it as a favour.

## Procedure

1. Compute the hard floor: variable cost per unit, below which every sale destroys cash. If a unit costs $12.00 in materials and fulfilment, $12.00 is the line you never cross.
2. Compute the soft floor: variable cost plus the contribution needed to cover fixed cost at the realistic volume. Fixed $84,000 over 10,500 units adds $8.00, so $20.00 is break-even and the floor for normal work.
3. Apply the floor by decision tier: an incremental order with spare capacity may sit at the hard floor; a new commitment with dedicated cost must clear the soft floor.
4. Price a suspect engagement through its full cost, not the headline rate. A fixed-fee job at $4,000 whose fully-loaded cost is $4,600 burns $600 before any overrun.

       ```
       python3 -c "from decimal import Decimal as D; print(D('4000')-D('4600'))"
       # -600 -> decline, or reprice to cost plus margin
       ```

5. Check the floor against the walk-away: a client who demands $3,000 for work costing $3,800 has priced you below cost; the answer is a written decline, not a discount.
6. Say no with the number: "Our cost on this scope is $3,800; we cannot do it at $3,000." A cost-anchored refusal is a fact, not an insult, and keeps the relationship repairable.
7. Offer a smaller scope at or above the floor instead of the same scope at a loss; that compromise nearly always exists.
8. Watch for the disguised below-floor deal: a discount plus free change work plus delayed payment is a below-cost deal wearing three hats.
9. Keep the floor in integer minor units and re-derive it when variable or fixed cost moves 10%; a stale floor is how a book slides into unprofitable work one favour at a time.
10. Record declined engagements with the price offered and your cost, so the floor is defensible when someone asks why you walked away.

## Pitfalls

- Taking a deal below variable cost because the client is strategic; the loss is real on every unit.
- Setting the floor from a rounded cost and then shaving just under it.
- Letting change requests and slow payment turn a floor deal into a loss.
- Mistaking discount plus free work plus a delayed invoice for a healthy deal.
- Never revisiting the floor after costs move.
- Storing the floor as a float, so a boundary deal slips under it by a cent.

## Verification

    ```
    python3 -c "from decimal import Decimal as D; print(D('4000')-D('4600'))"
    # -600 -> the engagement is below cost; decline or reprice
    ```

Pass when the hard and soft floors and the deal's fully-loaded cost are all stated. Report the hard and soft floors, the deal's cost, and the written decision taken against it.
