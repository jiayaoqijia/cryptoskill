---
name: dividends-and-distributions
domain: investing/dividends-and-distributions
trigger: "Recording a dividend or distribution correctly across dates and currencies."
anti_trigger: "Not for dividend strategy, and not for tax computation."
scope: "Ex-dates, record dates, withholding, and the difference between income and total return."
status: seedling
---

# Dividends and distributions

## Standard

A dividend has a timetable: declaration, ex-date, record date, payment date. The ex-date is when the price adjusts for the distribution, the record date determines who is entitled, and the payment date is when cash arrives. Confusing them produces the two common errors: expecting the cash before payment, and treating the ex-date price drop as a loss.

The other distinction is between income and total return. A price series that ignores dividends understates return by the yield; a total-return series reinvests them. Which one is appropriate depends on the question, and the record must say which was used.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record all four dates and the amount per share, with the issuer's announcement as the source.
- Distinguish ordinary income from return of capital and from capital gains distributions; the treatment differs.
- Record withholding at source where it applies, with the document.
- Use total-return series for performance questions and price series for price questions; label which.
- Reinvestment is recorded as a purchase with its own basis, not as free shares.
- Foreign-currency dividends are recorded at the payment-date rate with the rate stated.

## Procedure

1. Record declaration, ex, record, and payment dates.
2. Record amount per share and its classification.
3. Record withholding and the document.
4. Decide whether the analysis needs a total-return or price series and label it.
5. Record any reinvestment as a separate purchase.
6. Note the currency and rate for foreign dividends.

## Anti-patterns

- Treating the ex-date price drop as a loss.
- Counting reinvested shares as free.
- Mixing total-return and price series in one comparison.
- Ignoring withholding.
- Using the declaration-date rate for a foreign dividend.

## Done checklist

- [ ] Four dates and amount recorded with source.
- [ ] Classification recorded.
- [ ] Withholding recorded with document.
- [ ] Series type labelled.
- [ ] Reinvestment recorded as purchase.
- [ ] Currency and rate recorded where applicable.

## Sources

- Regulatory context for dividend disclosure: <https://www.sec.gov/investor>
- Investor education on dividends and total return: <https://www.investor.gov/introduction-investing>
- Rule context for distribution processing: <https://www.finra.org/rules-guidance>

The classification matters more than the amount: an ordinary dividend, a return of capital, and a capital-gains distribution have different basis effects and different reporting. Recording the issuer's classification at the time is cheap; reconstructing it two years later is not.

The reinvestment case deserves its own line because it is where basis quietly multiplies: each reinvested dividend creates a small purchase with its own date and price, and the sum of those purchases is what a later disposal is measured against. Treating them as free shares destroys that trail.
