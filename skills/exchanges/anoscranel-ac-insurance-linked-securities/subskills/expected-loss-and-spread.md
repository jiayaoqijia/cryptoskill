---
name: expected-loss-and-spread
domain: investing/expected-loss-and-spread
trigger: "Reading an ILS spread against the expected loss it compensates."
anti_trigger: "Not for predicting loss, and not for comparing across perils without adjustment."
scope: "Expected loss, the multiple of it, and what the spread compensates."
status: seedling
---

# Expected loss and spread

## Standard

An insurance-linked security is priced as a spread over a funding rate, and the spread is quoted alongside an expected loss. The comparison that matters is the ratio: spread divided by expected loss gives a multiple, and that multiple is what the market is paying for bearing the risk. A bond with a five percent expected loss and a seven percent spread offers a multiple of one point four; one with a one percent expected loss and a three percent spread offers three.

The multiple is not a return. It is a compensation ratio, and it must be read against the model that produced the expected loss, the peril's tail behaviour, and the correlation the position adds. A high multiple on a peril that can produce a total loss in a single event is not the same offer as a high multiple on a frequency peril whose losses arrive in small increments, and the record should state which it is.

Primary sources: <https://www.sec.gov/investor> and <https://www.artemis.bm/>.

## Decision rules

- Record the expected loss, the model version, and the vendor.
- Record the spread and the funding reference.
- Compute the multiple and record it.
- Record the loss distribution: frequency, severity, and the probability of total loss.
- Record the correlation with other positions and with the portfolio's other risks.
- Record the multiple against comparable bonds on the same peril.

## Procedure

1. Record expected loss with its model and vendor.
2. Record the spread and its reference rate.
3. Compute the multiple.
4. Record the loss distribution's shape.
5. Record correlation and concentration.
6. Write the pricing summary with the multiple and its shape.

## Anti-patterns

- Comparing spreads without the expected losses behind them.
- Treating the multiple as an expected return.
- Ignoring the model version behind the expected loss.
- Assuming a frequency peril and a tail peril are comparable at the same multiple.
- Overlooking the correlation with an existing book.

## Done checklist

- [ ] Expected loss and model recorded.
- [ ] Spread and reference recorded.
- [ ] Multiple computed.
- [ ] Loss distribution recorded.
- [ ] Correlation recorded.
- [ ] Comparable multiples recorded.

A further comparison worth making is the multiple against the same peril in prior years: a market where the multiple has compressed across several seasons is telling you that capital has arrived and the compensation has fallen, which is information about the cycle rather than about any individual bond, and it belongs in the record beside the position's own pricing.

## Sources

- Catastrophe bond market data: <https://www.artemis.bm/>
- Securities disclosure context: <https://www.sec.gov/investor>
- Investor education on risk premia: <https://www.investor.gov/introduction-investing>
