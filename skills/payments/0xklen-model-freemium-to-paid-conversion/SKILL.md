---
name: model-freemium-to-paid-conversion
description: Use when a product has a free tier and you must judge whether it pays for itself. Models free-user cost against paid conversion and finds the conversion rate that merely breaks even.
---

# Model freemium to paid conversion

A free user is a cost centre until proven otherwise. Freemium is a bet that a small paid slice pays for the whole free base; compute the conversion rate at which that bet breaks even.

## Procedure

1. Measure the per-free-user monthly cost: hosting, storage, support, and email, summed and divided by active free users. Say $0.08 per free MAU per month.
2. Measure the paid plan's gross profit per month: price minus the variable serving cost. $15.00 price less $1.50 cost is $13.50.
3. Write the break-even condition: paid_count * gross_profit >= (free_count + paid_count) * free_cost.

       ```
       python3 -c "from decimal import Decimal as D
       free=D('100000'); gp=D('13.50'); fc=D('0.08')
       print((fc*free)/(gp-fc))"
       # 596 paying users to cover free-user cost -> 0.60% conversion
       ```

4. Compare to the observed rate. At 3% converting you are well past break-even on servicing; the real cost is usually acquisition spend, not hosting.
5. Add the support tail. Heavy free users cost far more than the average; bucket by P95 usage and re-run so one abused free tier does not hide in the mean.
6. Cap the free tier's expensive resource (compute, seats, storage) so per-free-user cost is bounded by design, not by hope.
7. Keep the conversion rate an exact ratio of integer counts, and prices in minor units; a float percentage hides the point where the tier tips to a net loss.
8. Recompute when infrastructure cost per free user moves 25% or more, since it, not price, usually drives the sign.
9. Distinguish free-to-paid within a window from free-to-paid ever; the second is larger and easier to fool yourself with.
10. Decide the free tier's job explicitly — acquisition, virality, or a loss-leader — and measure against that job.

## Pitfalls

- Dividing free-user cost by all users and understating it per free user.
- Assuming the average free user's cost when the P95 user can be a hundred times dearer.
- Counting conversions at any time rather than within a window, overstating the rate.
- Leaving an expensive free resource, such as exports or compute, uncapped.
- Treating support cost as fixed when it scales with free-user count.
- Float percentages that hide the sign flip exactly at the break-even point.

## Verification

    ```
    python3 -c "from decimal import Decimal as D; print((D('0.08')*D('100000'))/(D('13.50')-D('0.08')))"
    # ~596 paying users, i.e. 0.60% of a 100k free base
    ```

Pass when the break-even conversion rate and the observed rate are both stated. Report the break-even rate, the observed rate, and the per-free-user cost bucket behind it.
