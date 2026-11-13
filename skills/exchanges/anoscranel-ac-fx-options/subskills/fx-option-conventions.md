---
name: fx-option-conventions
domain: investing/fx-option-conventions
trigger: "Reading an FX option quote and turning it into money."
anti_trigger: "Not for generic option pricing, and not for spot FX mechanics."
scope: "Premium in vol points, expiry cuts, and settlement conventions."
status: seedling
---

# FX option conventions

## Standard

An FX option premium is quoted in one of two ways: as an amount of the premium currency per unit of the base currency, or in volatility points, which is the premium expressed as a percentage of the spot rate and then quoted in vol terms. The second convention dominates interdealer markets because it makes quotes comparable across pairs and across spot levels, but it means the number on the screen is not the number that will be paid.

The second convention that decides the cash flow is the expiry cut. FX options expire at a stated time in a stated financial centre — commonly ten in the morning New York for the major pairs — and the option is exercised or not against the rate at that moment, not at the end of the day. A position that is in the money at the London close and out of the money at the cut expires worthless, and the record should state the cut rather than the date.

Primary sources: <https://www.bis.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the pair, the strike, and whether the premium is in vol points or currency.
- Convert a vol-point premium into the premium currency and record the calculation.
- Record the expiry date, the cut time, and the financial centre of the cut.
- Record the settlement date and whether it is spot or forward.
- Record the premium payment date, which is usually before settlement.
- Record any fixing source named in the confirmation.

## Procedure

1. Record the trade terms and the quote convention.
2. Convert the premium into the payment currency and check it against the indicative amount.
3. Record the expiry, cut time, and centre.
4. Record settlement and premium dates.
5. Record the fixing source.
6. Write the terms summary the position will be managed against.

## Anti-patterns

- Reading a vol-point premium as a currency amount.
- Assuming expiry at the end of the expiry day.
- Confusing the premium date with the settlement date.
- Ignoring the fixing source when the option settles against a published rate.
- Comparing premiums across pairs without a common convention.

## Done checklist

- [ ] Pair, strike, and convention recorded.
- [ ] Premium converted and checked.
- [ ] Expiry and cut recorded.
- [ ] Settlement and premium dates recorded.
- [ ] Fixing source recorded.
- [ ] Terms summary written.

## Sources

- Foreign exchange market conventions: <https://www.bis.org/>
- Market rates and settlement context: <https://www.federalreserve.gov/>
- Investor education on currency products: <https://www.investor.gov/introduction-investing>
