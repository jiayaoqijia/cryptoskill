---
name: format-currency-after-rounding
description: Use when displaying money to a user or in an export. Rounds to the currency's display scale first, then formats with the right symbol, separators, sign and locale — never formats before rounding.
---

# Format currency after rounding

Formatting is the last step and it must round first. `f"{x:.2f}"` on an unrounded value prints a string that disagrees with the stored amount; round to the currency exponent, then format that value.

## Procedure

1. Round to the currency's exponent before formatting: USD 2, JPY 0, KWD 3. Formatting `%.2f` on a KWD amount silently drops the third fils.
2. Use a locale-aware formatter, not string concatenation: `Intl.NumberFormat('en-US',{style:'currency',currency:'USD'})` in JS, `babel.numbers.format_currency` in Python, `NumberFormat.getCurrencyInstance` in Java.
3. Pass the amount as a decimal or a minor-unit integer; never a float you already know is inexact.
4. Decide negative presentation: `-$1.23` (US), `($1.23)` (accounting), `-1,23 €` (EU suffix). Match the audience's convention.
5. Keep sign and magnitude separable so a refund can render `(€1.234,56)` without string surgery.
6. For exports (CSV), emit minor units or an unformatted exact decimal in a fixed locale — never the display string with symbols; a spreadsheet mangles `"1.234,56 €"`.
7. For very small or large amounts, do not fall into scientific notation: 1 satoshi must print as a decimal string, not `1e-8`.
8. Show the currency in every non-ambiguous context; a bare `1,234.56` in a multi-currency table is a bug.
9. Cache formatter instances — constructing `Intl.NumberFormat` per row is slow — rather than rebuilding for every value.
10. For a multi-currency column, format each row with that row's currency, never one currency for the whole table.

## Pitfalls

- `f"{2.675:.2f}"` prints `2.67` (binary float), not `2.68`; round the exact decimal first.
- Using the wrong exponent: formatting a 3-decimal currency at 2 decimals loses the smallest unit every time.
- Thousands separators from one locale in a CSV parsed by another shift the value by 1000x.
- Passing an unrounded `Number` into `Intl.NumberFormat` lets the formatter round, hiding a discrepancy with the ledger.
- Stripping a trailing zero to "tidy" `$1.50` into `$1.5` changes the implied precision.
- Formatting a total before summing its parts, so the displayed sum differs from the sum of displayed parts (see `aggregate-before-you-round`).
- Some locales place the sign after the number (`1,23 €-`) or inside the parentheses; do not assume a leading `-`.

## Verification

    python3 -c "from decimal import Decimal as D, ROUND_HALF_UP; import babel.numbers as b; v=D('2.675').quantize(D('0.01'),ROUND_HALF_UP); print(b.format_currency(v,'USD','en_US'))"
    # $2.68, not $2.67
    node -e "console.log(new Intl.NumberFormat('de-DE',{style:'currency',currency:'EUR'}).format(1234.56))"

Report the display scale used and one formatted example, with the rounded exact value behind it.
