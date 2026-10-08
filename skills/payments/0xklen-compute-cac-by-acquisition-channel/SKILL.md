---
name: compute-cac-by-acquisition-channel
description: Use when evaluating what a customer costs to acquire. Computes fully-loaded CAC per channel including salaries and tools, and keeps blended and paid CAC apart so neither flatters the other.
---

# Compute CAC by acquisition channel

The number that matters is fully loaded: ad spend plus the people and tools that produced the customers. A channel is only cheap if you divide by the customers it actually sourced.

## Procedure

1. Define the numerator: program spend (ads, events, sponsorships) plus the fully-loaded cost of the marketers, SDRs and tools that run the channel, over the period.
2. Define the denominator carefully: new customers acquired, not leads, not trials, not influenced pipeline.
3. Compute per channel and blended:

       ```
       python3 -c "from decimal import Decimal as D; print((D('40000')+D('15000'))/D('250'))"
       # 220.00 fully-loaded CAC
       ```

4. Report both. A blended figure mixes a cheap organic channel with an expensive paid one; quoting the blend to justify the paid channel hides the gap.
5. Exclude organic and referral from a paid-channel denominator only if the attribution is trustworthy; otherwise keep the channels separate entirely.
6. Compare CAC to gross-profit payback, not to revenue: a $220 CAC against $55 monthly gross profit is four months of payback.
7. Watch marginal CAC, not just average CAC. The next $10,000 in a saturating channel often costs twice the average; plot CAC against cumulative spend.
8. Keep spend and counts as exact values; a float per-customer average hides the cents that matter when CAC approaches gross profit.
9. Re-baseline quarterly and after any channel change; a channel that failed on old creative is worth a retry, not a retirement.
10. Report CAC with the channel, the window and the denominator named, or it will be compared next quarter to a different definition.

## Pitfalls

- Dividing spend by leads or trials instead of acquired customers.
- Omitting salaries and tools, which can double the headline CAC.
- Reporting per-channel CAC without a matching attribution rule.
- Quoting blended CAC to justify a paid channel that is far dearer on its own.
- Using average CAC after marginal CAC has already doubled.
- Float spend arithmetic that drifts the cents when CAC nears gross profit.

## Verification

    ```
    python3 -c "from decimal import Decimal as D; print((D('40000')+D('15000'))/D('250'))"
    # 220.00 -> $220 fully-loaded CAC for 250 new customers
    ```

Pass when each channel has a named numerator and denominator. Report CAC per channel and blended, with the window and the customer definition behind each.
