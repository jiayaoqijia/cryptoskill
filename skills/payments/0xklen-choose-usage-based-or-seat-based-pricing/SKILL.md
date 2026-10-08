---
name: choose-usage-based-or-seat-based-pricing
description: Use when picking the billing dimension for a product. Weighs usage-based against seat-based on value alignment, revenue predictability and expansion, with worked numbers for the same customer.
---

# Choose usage-based or seat-based pricing

The billing dimension decides who grows your revenue for you. Seats expand with headcount; usage expands with value delivered. Pick the one that tracks what the buyer actually gets.

## Procedure

1. Name the value metric: the unit that grows as the customer gets more value — API calls, GB stored, documents sent, or human seats.
2. Score alignment. If value rises with usage but you bill seats, a heavy user is undercharged and a light user is overcharged; that mismatch leaks in both directions.
3. Quantify predictability. Seat-based invoices are flat and vary only with churn; usage-based revenue can swing 30-50% month to month and must be forecast as a range.
4. Compare expansion for the same customer. A team of 10 seats at $30.00 grows to 14 seats = $420.00. The same team doubling API calls from 2M to 4M at $0.05 per 1,000 grows from $100.00 to $200.00.

       ```
       python3 -c "from decimal import Decimal as D; print(D(5)*D(4000000)/D(1000))"
       # 20000 minor units = $200.00
       ```

5. Weight the operational cost. Usage billing needs metering, dunning on overage, and dispute handling; seat pricing fits on one line of an invoice.
6. Consider a hybrid: a platform fee per seat plus a usage component. This caps the swing while still charging for growth.
7. Model the worst case under usage billing — a spike you serve at a loss — and add a committed minimum so the floor holds.
8. Store metered quantities as integers and unit rates as integer minor units per quantity, and multiply exactly; never a float dollar rate across millions of units.
9. Re-price the dimension when customers admit they are managing consumption to fit the bill; that signals the meter is misaligned with value.
10. Publish the value metric on the pricing page. A dimension buyers cannot see is one they cannot grow into.

## Pitfalls

- Choosing usage billing without metering, dunning and dispute handling in place.
- Ignoring usage volatility, so finance forecasts a point when the number swings 40%.
- Letting a heavy user pay the light-user rate under a seat model.
- A usage rate so small the monthly invoice is dominated by rounding noise.
- No committed minimum, so a usage spike is served at a loss.
- Storing a per-unit rate as a float dollar figure and multiplying it across millions of units.

## Verification

    ```
    python3 -c "from decimal import Decimal as D; print(D(5)*D(4000000)/D(1000))"
    # 20000 -> $200.00 for 4M calls at $0.05 per 1,000
    ```

Pass when the value metric is chosen and the expansion and worst-case invoices are shown. Report the value metric, the expansion it produces for a doubling customer, and the worst-case monthly invoice.
