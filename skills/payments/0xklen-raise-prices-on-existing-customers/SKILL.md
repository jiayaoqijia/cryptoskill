---
name: raise-prices-on-existing-customers
description: Use when a book of existing accounts must move to higher renewal pricing. Models the churn break-even, sets notice and grandfathering, and keeps old and new prices in exact minor units.
---

# Raise prices on existing customers

New-customer pricing is easy; raising an existing book is where trust and revenue collide. Do the churn arithmetic first, because the lift only wins if the accounts that leave cost less than the lift on those that stay.

## Procedure

1. Compute the gross-profit lift if nobody churns. A $99.00 to $129.00 rise on 500 accounts at 70% margin adds `(129-99)*0.70*500 = $10,500` a month.
2. Compute the churn break-even: the fraction of accounts that may leave before the lift is wiped out.

       ```
       python3 -c "from decimal import Decimal as D; print(D('30')*D('0.70')/(D('129')*D('0.70')))"
       # 0.2326 -> 23.3% churn erases the entire lift
       ```

3. Segment the book: annual contracts with notice windows, month-to-month accounts, and heavily discounted legacy seats. They tolerate the change differently.
4. Decide grandfathering: freeze renewals for 12 months, or lift everyone at the renewal date. Permanent grandfathering turns the old price into a second list price forever.
5. Give notice that matches the contract and the norm: 90 days for business software, longer for anything the customer has built on.
6. Pair the rise with an added capability so the change has a story. A naked percentage is a cost conversation; a new tier is a value conversation.
7. Migrate at renewal rather than mid-term, and change only one thing at a time — not price and value metric together.
8. Keep old and new prices in the price book as integer minor units (`price_minor_legacy=9900`, `price_minor_new=12900`) so the migration is a table lookup, never a float edit.
9. Track cohort retention after the rise by original price, not in aggregate, so the churn is attributable.
10. Set a decision date: if realised churn exceeds the break-even within two cycles, pause and re-price.

## Pitfalls

- Raising price without computing the churn break-even, then discovering the answer in a bad quarter.
- Grandfathering forever, which creates a permanent second price list.
- Lifting mid-contract, which is often a breach and always a trust event.
- Announcing a naked percentage with no added capability to attach it to.
- Raising the price and the old value metric at once, compounding the change.
- Float price edits that leave the old and new prices off by a cent in the book.

## Verification

    ```
    python3 -c "from decimal import Decimal as D; print(D('30')*D('0.70')/(D('129')*D('0.70')))"
    # 0.2326 -> 23.3% of accounts may churn before the lift is lost
    ```

Pass when the revenue lift and the churn break-even are both computed. Report the monthly lift, the churn break-even, the notice period, and the grandfathering decision.
