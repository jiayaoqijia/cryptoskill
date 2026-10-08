---
name: parse-locale-money-input
description: Use when accepting an amount typed by a user (a form field, a CSV, an SMS). Parses locale-specific separators into exact minor units without float, and rejects ambiguous input.
---

# Parse locale money input

`"1.234,56"` (German) and `"1,234.56"` (US) are the same number written two ways, and `"1.234"` alone is ambiguous. Parse with an explicit locale into exact minor units; never `float()` a user string.

## Procedure

1. Require the currency alongside the number — parsing `"1.234"` without knowing EUR vs USD cannot decide whether it means 1.234 or 1234.
2. Take a locale, or better a declared decimal separator, and map `,` and `.` explicitly rather than guessing.
3. Strip the currency symbol and thousands separators by the locale's rules: US groups with `,` every 3 digits; FR/DE use spaces or `.`; Indian grouping is `1,00,000`.
4. Reject ambiguous forms: a string with two candidate separators where neither groups correctly (`"1.234"`, `"1,234"`), or a lone separator with 1–2 trailing digits and no grouping.
5. Convert to minor units with exact arithmetic: `int(Decimal(cleaned).scaleb(exp))`, never `round(float(s) * 100)`.
6. Validate the fraction length against the currency's exponent: `"1.999"` in USD has a third decimal that must be rejected or explicitly rounded per policy, not silently dropped.
7. Handle negative forms: a leading sign, a trailing `-`, and accounting parentheses `("1.234,56")`.
8. Return a `Money {currency, amount_minor}` or an error — never a bare number.
9. Fuzz the parser with mixed-separator strings to confirm it raises rather than guessing.
10. Normalise non-breaking and narrow spaces (`\u00a0`, `\u202f`) to a plain space before parsing.
11. Round-trip each parse through the display format in the same locale as a test.

## Pitfalls

- `float("1.234")` yields `1.234` when the user meant 1234; the ambiguity is the bug, not the float.
- `parseFloat("1,234.56")` stops at the comma and yields `1` — silent truncation.
- Excel/LibreOffice CSV exports use the *displayed* locale format; importing with the wrong locale multiplies by 1000.
- Unicode non-breaking spaces as thousands separators (fr-FR) survive a plain `.strip()` and break the number.
- Accepting `"1e6"` or `"+1_000"` from a form field; restrict to digits, one separator and a sign.
- Silently rounding a third decimal changes a legal amount; reject it or flag it.
- A leading `+`, a currency prefix, and trailing whitespace can arrive together; strip known affixes in a defined order rather than `strip()`-ing everything.

## Verification

    python3 -c "from decimal import Decimal as D; print(int(D('1.234,56'.replace('.','').replace(',','.'))*100))"   # 123456
    # assert parse('1,234.56','en_US') == parse('1.234,56','de_DE')

Report the locale/decimal separator assumed, the parsed minor-unit value, and any input rejected as ambiguous.
