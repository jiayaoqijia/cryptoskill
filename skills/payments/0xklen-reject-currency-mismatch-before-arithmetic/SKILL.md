---
name: reject-currency-mismatch-before-arithmetic
description: Use when combining or subtracting money values that may be in different currencies or units. Checks the currency and scale of both operands before any arithmetic and refuses a mismatch.
---

# Reject currency mismatch before arithmetic

Adding `100 USD` to `100 EUR` yields `200` of nothing. Every operation on money must first assert both operands share a currency and a scale; a mismatch is an error, not a coercion opportunity.

## Procedure

1. Make the type carry the unit: a `Money {amount_minor, currency}` record, so `+` is only defined when the currencies match.
2. Assert at the top of every operation: `if a.currency != b.currency: raise CurrencyMismatch(a, b)`. Convert to a common currency explicitly first (see `snapshot-fx-rates-at-posting-time`), never implicitly.
3. Guard the **scale** too: two operands of the same currency must share the minor-unit convention (both cents, or both a fixed-point scale). A column that stores dollars-float on some rows and cents on others is a scale mismatch under one currency.
4. In SQL, store the currency code with the amount and check it in the join: `ON a.currency = b.currency`; fail a query that groups mixed currencies rather than summing them.
5. In a multi-currency aggregate, group by currency and sum within each group; never `SUM` across the group boundary.
6. A ratio of two Money values of the same currency is dimensionless, not Money — type it so it cannot be added back to an amount.
7. Reject an empty or unknown currency code (`""`, `None`) at the boundary.
8. Log both currency codes on any refused operation so the source of the bad value is traceable.
9. Unit-test the mismatch path itself: assert that adding USD to EUR raises, so the guard is not optimized away.
10. Expose the currency in every log line for a money operation so a mismatch is visible in production traces.
11. For a migration that backfills a currency column, fail the migration on any NULL rather than defaulting.

## Pitfalls

- Dropping the currency from a DTO and re-adding a default is how a EUR value gets relabelled USD downstream.
- `SUM()` over a mixed-currency column returns digits that look plausible and mean nothing.
- A "currency" that is really a testnet flag or a token symbol aliases two different assets (`USDC` on two chains); include the chain or issuer.
- An implicit join to a base-currency table hides a missing rate as a `0` or `NULL`.
- Adding Money to a plain number (an integer count) compiles in loosely typed languages and silently treats the count as money.
- Comparing two currencies "because they're close" after a stale conversion masks a real currency bug.
- A `CASE` in SQL that coalesces a missing currency to a default silently relabels foreign amounts; leave it NULL and fail the query.

## Verification

    python3 -c "a=('USD',1234); b=('EUR',1234); print('ok' if a[0]==b[0] else 'CurrencyMismatch')"   # CurrencyMismatch
    psql -c "SELECT currency, SUM(amount_minor) FROM post GROUP BY currency"   # never sum across gaps

Report the currency codes checked and any operation refused for a mismatch.
