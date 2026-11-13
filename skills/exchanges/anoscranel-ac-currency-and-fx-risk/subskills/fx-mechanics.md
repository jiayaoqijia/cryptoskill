---
name: fx-mechanics
domain: investing/fx-mechanics
trigger: "Reading FX quotes and understanding what a forward price contains."
anti_trigger: "Not for forecasting exchange rates, and not for choosing a hedge ratio."
scope: "Spot and forward quotes, conventions, settlement, and what a forward price contains."
status: seedling
---

# FX mechanics

## Standard

An FX quote is a ratio of two currencies, and the convention matters: which currency is the base, which is the term, and whether the quote is direct or indirect from your perspective. Getting the convention wrong produces an error that is invisible in the arithmetic and wrong by the inverse.

A forward is a spot rate adjusted by the interest-rate differential between the two currencies over the period. That is why a forward is not a forecast: it is the spot rate plus the cost of carrying one currency against the other, and it will differ from the future spot rate whenever the differential differs from the actual change.

Primary sources: <https://fred.stlouisfed.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the pair in a stated convention: base currency first, term currency second.
- Record whether the quote is direct or indirect relative to the portfolio's reporting currency.
- Convert amounts with the same convention used to quote, and show the direction.
- A forward is recorded as spot plus the differential, with the differential's source.
- Settlement dates are recorded; a forward's value date is not the trade date.
- Never compare quotes from two sources without confirming the convention matches.

## Procedure

1. Identify the base and term currencies.
2. Record the spot quote, its source, and the timestamp.
3. State the direction of conversion and the arithmetic.
4. For a forward, record the differential and the implied forward.
5. Record the value date.
6. Verify the convention against one known conversion.

## Anti-patterns

- Multiplying where the quote requires dividing.
- Treating a forward as a forecast.
- Mixing quotes from sources with different conventions.
- Ignoring the value date.
- Quoting a rate without a timestamp in a fast market.

## Done checklist

- [ ] Base and term identified.
- [ ] Spot recorded with source and timestamp.
- [ ] Direction and arithmetic stated.
- [ ] Forward differential and implied rate recorded.
- [ ] Value date recorded.
- [ ] One conversion verified.

## Sources

- Exchange-rate and rate data: <https://fred.stlouisfed.org/>
- Investor education on currency mechanics: <https://www.investor.gov/introduction-investing>
- Regulatory context for FX disclosure: <https://www.sec.gov/investor>

The practical check is a round trip: convert an amount out of the reporting currency and back, and verify you arrive at the original number. A convention error survives one direction and disappears in the round trip, which is why the check catches it cheaply rather than at the position level.
